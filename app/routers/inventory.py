from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app import database, schemas, oauth2
from app.services import inventory_service

router = APIRouter(
    prefix='/inventories',
    tags=['Inventories']
)

get_db = database.get_db

# Product add into Inventory
# Product stock Update
# Stock Reduce when order
# Out of stock check



# Create inventory item- POST
@router.post('/', response_model=schemas.InventoryResponse)
def create_inventory(item: schemas.InventoryCreate, db: Session = Depends(get_db), current_user = Depends(oauth2.current_admin_only)):
    return inventory_service.created_inventory(item, db)

# Show Inventory by product id
@router.get('/{id}', response_model=schemas.InventoryResponse)
def show_inventory(id: int, db: Session = Depends(get_db), current_user = Depends(oauth2.current_admin_only)):
    return inventory_service.show_inventory(id, db)

# Show all inventories GET
@router.get('/', response_model=List[schemas.InventoryResponse])
def show_inventories(db: Session = Depends(get_db),current_user = Depends(oauth2.current_admin_only)):
    return inventory_service.show_inventories(db)

# inventory update by product id - PUT
@router.put('/{id}', response_model=schemas.InventoryResponse)
def update_inventory(id: int, request: schemas.InventoryCreate, db: Session = Depends(get_db),current_user = Depends(oauth2.current_admin_only)):
    return inventory_service.update_inventory(id, request, db)
