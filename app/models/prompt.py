from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ARRAY
from sqlalchemy.orm import relationship
from datetime import datetime

from app.db.base import Base

# pgvector support
try:
    from pgvector.sqlalchemy import Vector
    VECTOR_AVAILABLE = True
except ImportError:
    VECTOR_AVAILABLE = False

# VECTOR for semantic search instead od normal search 

class Prompt(Base):
    __tablename__ = "prompts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), nullable=False, index=True)
    content = Column(Text, nullable=False)
    category = Column(String(100), nullable=False, index=True)
    tags = Column(ARRAY(String), default=[])
    rating = Column(Float, default=0.0)
    usage_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    # # pgvector embedding column (384-dim for all-MiniLM-L6-v2)
    # if VECTOR_AVAILABLE:
    #     embedding = Column(Vector(384), nullable=True)
    # disable vector for now
    embedding = None
    # Relationships
    collection_links = relationship(
        "CollectionPrompt",
        back_populates="prompt",
        cascade="all, delete"
    )
