from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.schemas.prompt import PromptSearchRequest, PromptResponse
from app.services.search_service import SearchService
from app.core.logger import get_logger

router = APIRouter(prefix="/search", tags=["Search"])
logger = get_logger(__name__)


@router.post("/", response_model=List[PromptResponse])
def semantic_search(
    payload: PromptSearchRequest,
    db: Session = Depends(get_db),
):
    """
    Semantic search using sentence embeddings.
    Returns top-k most relevant prompts.
    """
    logger.info(f"Search query: {payload.query}")
    service = SearchService(db)
    results = service.semantic_search(
        query=payload.query,
        top_k=payload.top_k,
        category=payload.category,
    )
    return results
