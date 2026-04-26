from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class PromptCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=500)
    content: str = Field(..., min_length=10)
    category: str = Field(..., min_length=2, max_length=100)
    tags: Optional[List[str]] = []


class PromptUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    category: Optional[str] = None
    tags: Optional[List[str]] = None


class PromptResponse(BaseModel):
    id: int
    title: str
    content: str
    category: str
    tags: List[str]
    rating: float
    usage_count: int
    created_at: datetime

    class Config:
        from_attributes = True


class PromptSearchRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=500)
    top_k: Optional[int] = Field(default=10, ge=1, le=50)
    category: Optional[str] = None


class PromptGenerateRequest(BaseModel):
    user_input: str = Field(..., min_length=5, max_length=1000)
    tone: Optional[str] = "professional"
    style: Optional[str] = "detailed"


class PromptGenerateResponse(BaseModel):
    generated_prompt: str
    detected_intent: str
    template_used: str


class CollectionCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=300)
    description: Optional[str] = None
    prompt_ids: Optional[List[int]] = []


class CollectionResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    created_at: datetime
    prompts: Optional[List[PromptResponse]] = []

    class Config:
        from_attributes = True
