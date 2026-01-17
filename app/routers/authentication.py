from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import database, schemas
from fastapi.security import OAuth2PasswordRequestForm
from app.services import auth_service



router = APIRouter()

get_db = database.get_db

@router.post('/register', tags=["Authentication"], response_model=schemas.UserResponse)
def user_register(request: schemas.UserCreate, db: Session = Depends(get_db)):
    return auth_service.user_register(request, db)


@router.post('/login', tags=["Authentication"])
def login(form_request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return auth_service.login(form_request, db)