from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import app.JWToken as JWToken, app.database as database
from sqlalchemy.orm import Session
from app.models import UserRole


oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "login")


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return JWToken.verify_token(token, credentials_exception, db)

def current_admin_only(current_user =  Depends (get_current_user)):
    if current_user.role != UserRole.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin permission required")
    
    return current_user  