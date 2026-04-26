from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from app.db.base import Base


class Collection(Base):
    __tablename__ = "collections"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(300), nullable=False, index=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    prompt_links = relationship(
        "CollectionPrompt",
        back_populates="collection",
        cascade="all, delete"
    )


class CollectionPrompt(Base):
    """Junction table for Collection <-> Prompt many-to-many."""
    __tablename__ = "collection_prompts"

    id = Column(Integer, primary_key=True, index=True)
    collection_id = Column(
        Integer, ForeignKey("collections.id", ondelete="CASCADE"), nullable=False
    )
    prompt_id = Column(
        Integer, ForeignKey("prompts.id", ondelete="CASCADE"), nullable=False
    )

    # Relationships
    collection = relationship("Collection", back_populates="prompt_links")
    prompt = relationship("Prompt", back_populates="collection_links")
