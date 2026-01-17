from sqlalchemy.orm import Session
from app import models


def create_user(user_data, db: Session ):
    user = models.User(** user_data)
    db.add(user)
    db.commit()
    db.refresh(user)    
    return user

def get_user(id: int, db: Session):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        return None
    return user