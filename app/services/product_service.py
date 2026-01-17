from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.repositories import product_repo
from app import schemas



def add_product(request: schemas.ProductCreate , db: Session):
    product_data = {
        "sku": request.sku,
        "name": request.name,
        "description": request.description,
        "price": request.price
    }
    return product_repo.add_product(product_data, db)

def get_prodcuts(db: Session):
    products = product_repo.get_prodcuts(db)
    return products

def update_product(product_id: int, request: schemas.ProductCreate, db: Session):
    updated_product = product_repo.update_product(product_id, request, db)
    if not updated_product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with the id {id} not available")
    
    return {"Message": "Product update successfully", "product": updated_product}

def delete_product(product_id: int, db: Session):
    deleted_product = product_repo.delete_product(product_id, db)
    if not deleted_product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with the id {id} not available")
    
    return {"Message":"Product delete successfully"}