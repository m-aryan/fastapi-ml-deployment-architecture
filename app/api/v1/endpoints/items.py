from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.schemas.item import ItemCreate, ItemUpdate, ItemResponse
from app.services.item_service import ItemService

router = APIRouter()

@router.post("/", response_model=ItemResponse)
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    service = ItemService(db)
    return service.create_item(item)

@router.get("/", response_model=List[ItemResponse])
def get_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    service = ItemService(db)
    return service.get_items(skip=skip, limit=limit)

@router.get("/{item_id}", response_model=ItemResponse)
def get_item(item_id: int, db: Session = Depends(get_db)):
    service = ItemService(db)
    item = service.get_item(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.put("/{item_id}", response_model=ItemResponse)
def update_item(item_id: int, item_update: ItemUpdate, db: Session = Depends(get_db)):
    service = ItemService(db)
    item = service.update_item(item_id, item_update)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.delete("/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    service = ItemService(db)
    success = service.delete_item(item_id)
    if not success:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Item deleted successfully"}