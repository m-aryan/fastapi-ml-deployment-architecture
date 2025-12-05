from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.item import Item
from app.schemas.item import ItemCreate, ItemUpdate

class ItemService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_item(self, item: ItemCreate) -> Item:
        db_item = Item(**item.dict())
        self.db.add(db_item)
        self.db.commit()
        self.db.refresh(db_item)
        return db_item
    
    def get_item(self, item_id: int) -> Optional[Item]:
        return self.db.query(Item).filter(Item.id == item_id).first()
    
    def get_items(self, skip: int = 0, limit: int = 100) -> List[Item]:
        return self.db.query(Item).offset(skip).limit(limit).all()
    
    def update_item(self, item_id: int, item_update: ItemUpdate) -> Optional[Item]:
        db_item = self.get_item(item_id)
        if db_item:
            update_data = item_update.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_item, field, value)
            self.db.commit()
            self.db.refresh(db_item)
        return db_item
    
    def delete_item(self, item_id: int) -> bool:
        db_item = self.get_item(item_id)
        if db_item:
            self.db.delete(db_item)
            self.db.commit()
            return True
        return False