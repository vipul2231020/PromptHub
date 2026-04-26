from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List, Optional

from app.models.prompt import Prompt
from app.core.logger import get_logger


logger = get_logger(__name__)

_embedding_model = None


def get_embeddding_model():
    """Load the sentence trfansformer model"""
    global _embedding_model
    if _embedding_model is None:
        try:
            from sentence_transformers import SentenceTransformer
            _embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
            logger.info("Sentence transformer model loaded sucessfully")
        except Exception as e:
            logger.error(f"Failed to load embedding model: {e}")
            _embedding_model = None
        
    return _embedding_model


class SearchService:
    def __init__(self, db: Session):
        self.db= db

    def generate_embedding(self, text:str) -> List[float]:
        """Generate embedding vector for given text"""
        model = get_embeddding_model()
        if model is None:
            return []
        embedding = model.encode(text, normalize_embeddings= True)
        return embedding.tolist()
    
    def semantic_search(
        self,
        query: str,
        top_k: int = 10,
        category: Optional[str] = None,
    ) -> List[Prompt]:
        """
        Perform semantic similarity search using pgvector.
        Falls back to text search if embeddings unavailable.
        """
        query_embedding = self.generate_embedding(query)

        if query_embedding:
            return self._vector_search(query_embedding, top_k, category)
        else:
            logger.warning("Falling back to text-based search")
            return self._text_search(query, top_k, category)


    def _vector_search(
        self,
        embedding: List[float],
        top_k: int,
        category: Optional[str],
    ) -> List[Prompt]:
        """Search using cosine similarity with pgvector."""
        try:
            # Build query with optional category filter
            base_query = self.db.query(Prompt).filter(
                Prompt.embedding.isnot(None)
            )

            if category:
                base_query = base_query.filter(Prompt.category == category)

            # Order by cosine distance (pgvector operator <=>)
            results = (
                base_query.order_by(
                    Prompt.embedding.cosine_distance(embedding)
                )
                .limit(top_k)
                .all()
            )
            return results
        except Exception as e:
            logger.error(f"Vector search failed: {e}")
            return self._text_search(" ".join(map(str, embedding[:5])), top_k, category)    
        
    
    def _text_search(
        self,
        query: str,
        top_k: int,
        category: Optional[str],
    ) -> List[Prompt]:
        """Fallback: basic ILIKE text search."""
        db_query = self.db.query(Prompt).filter(
            (Prompt.title.ilike(f"%{query}%")) |
            (Prompt.content.ilike(f"%{query}%"))
        )
        if category:
            db_query = db_query.filter(Prompt.category == category)

        return db_query.limit(top_k).all()
    
    def update_prompt_embedding(self, prompt_id: int, content: str) -> bool:
        """Generate and store embedding for a prompt."""
        prompt = self.db.query(Prompt).filter(Prompt.id == prompt_id).first()
        if not prompt:
            return False

        embedding = self.generate_embedding(content)
        if embedding:
            prompt.embedding = embedding
            self.db.commit()
            return True
        return False