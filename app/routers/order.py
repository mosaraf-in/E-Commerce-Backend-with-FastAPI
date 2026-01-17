from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app import database, schemas, oauth2
from app.services import order_service


router = APIRouter(
    prefix='/orders',
    tags=["Orders"]
)
get_db = database.get_db

# Create order by an user- POST
@router.post('/', response_model=schemas.OrderResponse)
def create_order(order_data: schemas.OrderCreate, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)): 
    return order_service.create_order(order_data, db, current_user)

# Get Order by Id- GET
@router.get('/{id}', response_model=schemas.OrderResponse)
def get_order(id: int, db: Session = Depends(get_db),current_user = Depends(oauth2.get_current_user)):
    return order_service.get_order(id, db, current_user)
    
# Get my orders- GET
@router.get('/', response_model=List[schemas.OrderResponse])
def my_orders(db: Session = Depends(get_db),current_user = Depends(oauth2.get_current_user)):
    return order_service.my_orders(db, current_user)

# Cancel order- PATCH
@router.patch('/{order_id}')
def cancel_order(order_id: int, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    return order_service.cancel_order(order_id, db, current_user)
        
        

# Update order status- PATCH
@router.patch('/{order_id}/status')
def update_order_status(order_id: int, new_status: str, db: Session = Depends(get_db), current_user = Depends(oauth2.current_admin_only)):
    return order_service.update_order_status(order_id, new_status, db)