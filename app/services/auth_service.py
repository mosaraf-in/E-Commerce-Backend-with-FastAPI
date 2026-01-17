from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app import schemas, JWToken
from datetime import timedelta
from app.hashing import Hash
from fastapi.security import OAuth2PasswordRequestForm
from app.repositories import auth_repo




def user_register(request: schemas.UserCreate, db: Session):
    hashed_password = Hash.password_hashing(request.password)
    
    user_data = {
        "name": request.name,
        "email": request.email,
        "password_hash": hashed_password
    }
    
    return auth_repo.user_register(user_data, db)


def login(form_request: OAuth2PasswordRequestForm, db: Session):
    user = auth_repo.login(form_request, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Invalid Credentials")
    if not Hash.verify_password(form_request.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Incorrect password")
    
    # generate a jwt token and return
    access_token = JWToken.create_token(
        data = {"user_email": user.email, "role":user.role},
        expires_delta = timedelta(JWToken.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    
    return {'access_token': access_token, "token_type":"bearer"}
