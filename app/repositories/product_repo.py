from sqlalchemy.orm import Session
from app import models, schemas



def add_product(product_data: dict, db: Session):
    product = models.Product(**product_data)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

def get_prodcuts(db: Session):
    products = db.query(models.Product).all()
    return products

def update_product(product_id: int, product_data: schemas.ProductCreate, db: Session):
    product = db.query(models.Product).filter(models.Product.id==id).first()
    if not product:
        return None
    
    product.sku = product_data.sku
    product.name = product_data.name
    product.description = product_data.description
    product.price = product_data.price
    
    db.commit()
    db.refresh(product)
    return product

def delete_product(product_id: int, db: Session):
    product = db.query(models.Product).filter(models.Product.id==id).first()
    if not product:
        return None
    db.delete(product)
    db.commit()
    return product