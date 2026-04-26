from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List

from app.db.session import get_db
from app.schemas.prompt import PromptResponse
from app.models.prompt import Prompt
from app.core.logger import get_logger

router = APIRouter(prefix="/analytics", tags=["Analytics"])
logger = get_logger(__name__)


@router.get("/trending", response_model=List[PromptResponse])
def get_trending_prompts(
    limit: int = Query(default=10, ge=1, le=50),
    db: Session = Depends(get_db),
):
    """Get top trending prompts by usage count."""
    prompts = (
        db.query(Prompt)
        .order_by(Prompt.usage_count.desc(), Prompt.rating.desc())
        .limit(limit)
        .all()
    )
    return prompts


@router.get("/stats")
def get_stats(db: Session = Depends(get_db)):
    """Get overall platform statistics."""
    total_prompts = db.query(func.count(Prompt.id)).scalar()
    total_usage = db.query(func.sum(Prompt.usage_count)).scalar() or 0
    avg_rating = db.query(func.avg(Prompt.rating)).scalar() or 0.0

    categories = (
        db.query(Prompt.category, func.count(Prompt.id))
        .group_by(Prompt.category)
        .all()
    )

    return {
        "total_prompts": total_prompts,
        "total_usage": total_usage,
        "average_rating": round(float(avg_rating), 2),
        "categories": {cat: count for cat, count in categories},
    }
