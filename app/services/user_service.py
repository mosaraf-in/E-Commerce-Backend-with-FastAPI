from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.hashing import Hash
from app.models import UserRole
from app.repositories import user_repo
from app import schemas


def create_user(request: schemas.UserCreate, db: Session ):
    hashed_password = Hash.password_hashing(request.password)
    
    # new_user = models.User(name = request.name, email = request.email, password_hash = hashed_password, role=UserRole.admin)
    user_data = {
        "name": request.name,
        "email": request.email,
        "password_hash": hashed_password,
        "role": UserRole.admin
    }
    return user_repo.create_user(user_data, db) 

def get_user(id: int,  db: Session):
    user = user_repo.get_user(id, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with the id {id} not available")
    return user