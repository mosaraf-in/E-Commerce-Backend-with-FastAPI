from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from  app import schemas, database
from app.services import user_service




router = APIRouter(
    prefix='/users',
    tags=['Users']
    
)

get_db = database.get_db

# Create user by admin
@router.post('/', response_model=schemas.UserResponse)
def create_admin(request: schemas.UserCreate, db: Session = Depends(get_db)):
    return user_service.create_user(request, db)


@router.get('/{id}', response_model=schemas.UserResponse)
def get_user(id: int,  db: Session = Depends(get_db)):
    return user_service.get_user(id, db)