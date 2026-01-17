from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import database, schemas, oauth2
from typing import List
from app.services import product_service

router = APIRouter(
    prefix='/products',
    tags=['Products']
)

get_db = database.get_db

# Add Product
@router.post('/', response_model=schemas.ProductResponse)
def add_product(request: schemas.ProductCreate , db: Session = Depends(get_db), current_user = Depends(oauth2.current_admin_only)):
    return product_service.add_product(request, db)

# Show all Product
@router.get('/', response_model=List[schemas.ProductResponse])
def show_prodcuts(db: Session = Depends(get_db)):
    return product_service.get_prodcuts(db)

# Product update
@router.put('/{id}')
def update_product(id: int, request: schemas.ProductCreate, db: Session = Depends(get_db), current_user = Depends(oauth2.current_admin_only)):
    return product_service.update_product(id, request, db)

# Delete product
@router.delete('/{id}')
def delete_product(id: int, db: Session = Depends(get_db), current_user = Depends(oauth2.current_admin_only)):
    return product_service.delete_product(id, db)