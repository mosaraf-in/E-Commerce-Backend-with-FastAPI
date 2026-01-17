from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models import OrderStatus
from app.repositories import order_repo
from app import models, schemas



def create_order(order_data: schemas.OrderCreate, db: Session, current_user):
    
    # Create empty order
    user_id = current_user.id
    order = models.Order(user_id = user_id, status="pending", total_amount=0)
    db.add(order)
    db.flush()
    
    total_amount = 0
    
    # Process each item (product check, inventory check, stock check, create_prder_item, reduce stock)
    for item in order_data.items:
        
        # Product Check
        product = db.query(models.Product).filter(models.Product.id==item.product_id).first()
        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with id {item.product_id} not found")
        
        # Inventory Check
        inventory = db.query(models.Inventory).filter(models.Inventory.product_id == item.product_id).first()
        if not inventory:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Inventory with id {item.product_id} not found")
        
        if inventory.available_qty < item.qty:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Insufficient stock for product {product.id}")
        
        # Create order item
        order_item = models.OrderItem(order_id=order.id, product_id=product.id, qty=item.qty, unit_price=product.price)
        db.add(order_item)
        
        # Reduce stock
        inventory.available_qty -= item.qty
        
        # Calculate total amount
        total_amount += product.price * item.qty
       
    order.total_amount = total_amount
    db.commit()
    db.refresh(order)
    
    return order



def get_order(id: int, db: Session, current_user):
    order =order_repo.get_order_by_id_and_user(db, id, current_user.id)
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Order with id {id} not found")
    return order

def my_orders(db: Session, current_user):
    return order_repo.get_orders_by_user(db, current_user.id)


def cancel_order(order_id: int, db: Session, current_user):
    order = order_repo.get_order_by_id_and_user(db, order_id, current_user.id)
    
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Order with id {order_id} not found")
    
    # delivered order would not cancel
    if order.status == "delivered":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="delivered order cannot be cancel")
    
    # Alredy cancel
    if order.status == "cancelled":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Order alredy cancelled")
    
    # Inventory restore
    for item in order.items:
        
        inventory = db.query(models.Inventory).filter(models.Inventory.product_id==item.product_id).with_for_update().first()
        if inventory:
            inventory.available_qty += item.qty
             
    # Update status
    order.status = "cancelled"
    db.commit()
    db.refresh(order)
    
    return {
        "message":"Order cancelled successfully",
        "order_id": order.id,
        "status": order.status
    }
    

def update_order_status(order_id: int, new_status: str, db: Session):
    order = order_repo.update_order_status(order_id, db)
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Order with id {order_id} not found")
    
    # Cancelled order would not update
    # if order.status == "cancelled": ---> string but we have enum
    if order.status == OrderStatus.cancelled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cancelled order cannot be update")
    
    allowed_status = [e.value for e in OrderStatus]
    
    if new_status not in allowed_status:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid status")
    order.status = OrderStatus(new_status)
    db.commit()
    db.refresh(order)
    
    return {
        "order_id": order.id,
        "status": order.status
    }
       
