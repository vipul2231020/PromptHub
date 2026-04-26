from sqlalchemy.orm import Session, joinedload
from typing import List, Optional

from app.models.prompt import Prompt
from app.models.collection import Collection, CollectionPrompt
from app.schemas.prompt import PromptCreate, PromptUpdate, CollectionCreate
from app.core.logger import get_logger

logger =  get_logger(__name__)

# here we are implementing prompt CURD 

class PromptService:
    def __init__(self, db: Session):
        self.db = db

    
    def get_prompts(
        self,
        skip: int = 0,
        limit: int = 20,
        category: Optional[str] = None,
    ) -> List[Prompt]:
        query = self.db.query(Prompt)

        if category:
            query = query.filter(Prompt.category == category)
        return query.offset(skip).limit(limit).all()
    

    def get_prompt_by_id(self, prompt_id: int)-> Optional[Prompt]:
        return self.db.query(Prompt).filter(Prompt.id == prompt_id).first()
    
    def create_prompt(self, payload: PromptCreate)-> Prompt:
        prompt = Prompt(
            title = payload.title,
            content = payload.content,
            category = payload.category,
            tags = payload.tags or [],
        )
        self.db.add(prompt)
        self.db.commit()
        self.db.refresh(prompt)
        logger.info(f"Created prompt : {prompt.id}")

    def update_prompt(
            self, prompt_id: int, payload:PromptUpdate
    )-> Optional[Prompt]:
        prompt = self.get_prompt_by_id(prompt_id)
        if not prompt:
            return None
        
        update_data = payload.model_dump(exclude_unset=True)
        for feild, value in update_data.items():
            setattr(prompt, feild, value)

        self.db.commit()
        self.db.refresh(prompt)
        return prompt
    
    def delete_prompt(self, prompt_id: int) -> bool:
        prompt = self.get_prompt_by_id(prompt_id)
        if not prompt:
            return False
        self.db.delete(prompt)
        self.db.commit()
        return True

    def increment_usage(self, prompt_id: int) -> None:
        prompt = self.get_prompt_by_id(prompt_id)
        if prompt:
            prompt.usage_count += 1
            self.db.commit()

#  Collection CRUD
    def get_collections(self, skip: int = 0, limit: int = 20) -> List[Collection]:
        return self.db.query(Collection).offset(skip).limit(limit).all()

    def get_collection_by_id(self, collection_id: int) -> Optional[Collection]:
        return (
            self.db.query(Collection)
            .options(
                joinedload(Collection.prompt_links).joinedload(
                    CollectionPrompt.prompt
                )
            )
            .filter(Collection.id == collection_id)
            .first()
        )

    def create_collection(self, payload: CollectionCreate) -> Collection:
        collection = Collection(
            name=payload.name,
            description=payload.description,
        )
        self.db.add(collection)
        self.db.flush()  # get ID before linking prompts

        # Link prompts to collection
        for prompt_id in payload.prompt_ids or []:
            link = CollectionPrompt(
                collection_id=collection.id,
                prompt_id=prompt_id,
            )
            self.db.add(link)

        self.db.commit()
        self.db.refresh(collection)
        logger.info(f"Created collection: {collection.id}")
        return collection



    

    
