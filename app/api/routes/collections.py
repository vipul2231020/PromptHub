from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.api.deps import get_admin_user
from app.models.user import User
from app.schemas.prompt import CollectionCreate, CollectionResponse
from app.services.prompt_service import PromptService
from app.core.logger import get_logger

router = APIRouter(prefix="/collections", tags=["Collections"])
logger = get_logger(__name__)


@router.get("/", response_model=List[CollectionResponse])
def get_all_collections(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, le=100),
    db: Session = Depends(get_db),
):
    """Get all collections."""
    service = PromptService(db)
    return service.get_collections(skip=skip, limit=limit)


@router.get("/{collection_id}", response_model=CollectionResponse)
def get_collection(collection_id: int, db: Session = Depends(get_db)):
    """Get a single collection with all its prompts."""
    service = PromptService(db)
    collection = service.get_collection_by_id(collection_id)
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")
    return collection


@router.post("/", response_model=CollectionResponse, status_code=201)
def create_collection(
    payload: CollectionCreate,
    db: Session = Depends(get_db),
    admin: User = Depends(get_admin_user),
):
    """Create a new collection (admin only)."""
    service = PromptService(db)
    collection = service.create_collection(payload)
    logger.info(f"Collection created: {collection.id}")
    return collection
