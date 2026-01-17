from sqlalchemy.orm import Session
from app import models


def get_order_by_id_and_user(db: Session, order_id: int, user_id: int):
    order = db.query(models.Order).filter(models.Order.id==order_id, models.Order.user_id==user_id).first()
    return order

def get_orders_by_user(db: Session, user_id: int):
    return db.query(models.Order).filter(models.Order.user_id==user_id).all()

 
def update_order_status(order_id: int, db: Session):
    order = db.query(models.Order).filter(models.Order.id==order_id).first()
    if not order:
        return None
    return order
