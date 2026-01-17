from sqlalchemy.orm import Session
from app import models
from fastapi.security import OAuth2PasswordRequestForm



def user_register(user_data: dict, db: Session):
    
    user = models.User(**user_data)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
    
    
def login(form_request: OAuth2PasswordRequestForm, db: Session):
    user = db.query(models.User).filter(models.User.email == form_request.username).first()
    return user

