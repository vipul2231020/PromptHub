from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.user import User, UserHistory
from app.schemas.prompt import PromptGenerateRequest, PromptGenerateResponse
from app.services.ai_service import AIService
from app.core.logger import get_logger

router = APIRouter(prefix="/generate", tags=["Generate"])
logger = get_logger(__name__)


@router.post("/", response_model=PromptGenerateResponse)
def generate_prompt(
    payload: PromptGenerateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Generate an optimized AI prompt from user input.
    Saves to user history automatically.
    """
    logger.info(f"Generating prompt for user {current_user.id}")

    ai_service = AIService()
    result = ai_service.generate_prompt(
        user_input=payload.user_input,
        tone=payload.tone,
        style=payload.style,
    )

    # Save to user history
    history_entry = UserHistory(
        user_id=current_user.id,
        user_input=payload.user_input,
        generated_prompt=result["generated_prompt"],
    )
    db.add(history_entry)
    db.commit()

    logger.info(f"Prompt generated and saved for user {current_user.id}")
    return PromptGenerateResponse(**result)
