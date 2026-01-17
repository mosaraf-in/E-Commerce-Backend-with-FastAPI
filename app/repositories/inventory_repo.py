from sqlalchemy.orm import Session
from app import schemas, models




def is_product_inventory(item: schemas.InventoryCreate, db: Session):
    product = db.query(models.Product).filter(models.Product.id==item.product_id).first()
    if not product:
        return None
    return product
        
def is_exist_inventory(item: schemas.InventoryCreate, db: Session):
    is_exist = db.query(models.Inventory).filter(models.Inventory.product_id==item.product_id).first()
    if not is_exist:
        return None
    return is_exist

def create_inventory(db: Session, inventory_data: dict):
    inventory = models.Inventory(** inventory_data)
    db.add(inventory)
    db.commit()
    db.refresh(inventory)
    
    return inventory
    
    
def fetch_inventory_by_id(id: int, db: Session):
    inventory = db.query(models.Inventory).filter(models.Inventory.product_id==id).first()
    if not inventory:
        return None
    return inventory
 
def fetch_inventories(db: Session):
    return db.query(models.Inventory).all()


def update_inventory(id: int, request: schemas.InventoryCreate, db: Session):
    inventory = fetch_inventory_by_id(id, db)
    
    if not inventory:
        return None
    
    inventory.available_qty = request.available_qty
    db.commit()
    db.refresh(inventory)
    return inventory


 