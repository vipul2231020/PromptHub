from worker.celery_app import celery_app
from app.core.logger import get_logger

logger = get_logger(__name__)


@celery_app.task(bind=True, max_retries=3)
def generate_embeddings_for_prompt(self, prompt_id: int):
    """
    Background task: generate and store embedding for a prompt.
    Runs asynchronously after prompt creation.
    """
    try:
        from app.db.session import SessionLocal
        from app.services.search_service import SearchService
        from app.models.prompt import Prompt

        db = SessionLocal()
        try:
            prompt = db.query(Prompt).filter(Prompt.id == prompt_id).first()
            if not prompt:
                logger.error(f"Prompt {prompt_id} not found for embedding")
                return

            search_service = SearchService(db)
            text_for_embedding = f"{prompt.title} {prompt.content}"
            success = search_service.update_prompt_embedding(
                prompt_id, text_for_embedding
            )

            if success:
                logger.info(f"Embedding generated for prompt {prompt_id}")
            else:
                logger.warning(f"Could not generate embedding for prompt {prompt_id}")
        finally:
            db.close()

    except Exception as exc:
        logger.error(f"Task failed for prompt {prompt_id}: {exc}")
        raise self.retry(exc=exc, countdown=60)


@celery_app.task
def update_trending_scores():
    """
    Periodic task: recalculate trending scores based on usage.
    Can be scheduled with Celery Beat.
    """
    try:
        from app.db.session import SessionLocal
        from app.models.prompt import Prompt

        db = SessionLocal()
        try:
            prompts = db.query(Prompt).all()
            for prompt in prompts:
                # Simple trending score: usage_count * 0.7 + rating * 0.3
                prompt.rating = min(
                    5.0,
                    (prompt.usage_count * 0.01) + prompt.rating * 0.5
                )
            db.commit()
            logger.info("Trending scores updated")
        finally:
            db.close()
    except Exception as e:
        logger.error(f"Failed to update trending scores: {e}")
