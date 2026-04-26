from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db.session import get_db
from app.api.deps import get_current_user, get_admin_user
from app.models.user import User 
from app.schemas.prompt import PromptCreate, PromptUpdate, PromptResponse 
from app.services.prompt_service import PromptService
from app.core.logger import get_logger

router = APIRouter(prefix = "/prompts", tags = ["Prompts"])
logger =  get_logger(__name__)

# total 5 apis for prompts - get all, get by id, create, update, delete

@router.get("/", response_model= List[PromptResponse])
def get_all_prompts( # for filtering and pagination
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    category : Optional[str] = Query(default=None),
    db: Session = Depends(get_db),
):
    """Get all prompts with optional category"""

    service = PromptService(db)
    return service.get_prompts(skip=skip, limit=limit, category=category)

@router.get("/{prompt_id}", response_model=PromptResponse)
def get_prompt(prompt_id: int, db: Session = Depends(get_db)):
    """Get a single prompt by ID."""
    service = PromptService(db)
    prompt = service.get_prompt_by_id(prompt_id)
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")

    # Increment usage count
    service.increment_usage(prompt_id)
    return prompt

@router.post("/", response_model=PromptResponse, status_code=201)
def create_prompt(
    payload: PromptCreate,
    db: Session = Depends(get_db),
    admin: User = Depends(get_admin_user),
):
    """Create a new prompt (admin only)."""
    service = PromptService(db)
    prompt = service.create_prompt(payload)
    logger.info(f"Prompt created: {prompt.id} by admin {admin.email}")
    return prompt

@router.put("/{prompt_id}", response_model=PromptResponse)
def update_prompt(
    prompt_id: int,
    payload: PromptUpdate,
    db: Session = Depends(get_db),
    admin: User = Depends(get_admin_user),
):
    """Update a prompt (admin only)."""
    service = PromptService(db)
    prompt = service.update_prompt(prompt_id, payload)
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")
    return prompt

@router.delete("/{prompt_id}", status_code=204)
def delete_prompt(
    prompt_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(get_admin_user),
):
    """Delete a prompt (admin only)."""
    service = PromptService(db)
    deleted = service.delete_prompt(prompt_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Prompt not found")