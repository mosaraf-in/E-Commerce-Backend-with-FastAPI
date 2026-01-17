from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.repositories import inventory_repo
from app import schemas


def create_inventory(item: schemas.InventoryCreate, db: Session):
    product = inventory_repo.is_product_inventory(item, db)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
        
    existng = inventory_repo.is_exist_inventory(item, db)
    if existng:
        raise HTTPException(status_code=status.HTTP_303_SEE_OTHER , detail="Inventory Already exists")
        
    inventory_data = {
        "product_id": item.product_id,
        "available_qty": item.available_qty
    }
     
    return inventory_repo.create_inventory(db, inventory_data)

def show_inventory(id: int, db: Session):
    inventory = inventory_repo.fetch_inventory_by_id(id, db)
    if not inventory:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Inventory not found with id {id}")
    return inventory

def show_inventories(db: Session):
    return inventory_repo.fetch_inventories(db)

def update_inventory(id: int, request: schemas.InventoryCreate, db: Session):
    inventory = inventory_repo.update_inventory(id, request, db)
    if not inventory:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Inventory not found with id {id}")
    
    return inventory



 
    