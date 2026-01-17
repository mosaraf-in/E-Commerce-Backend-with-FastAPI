from jose import JWTError,jwt
from fastapi import Depends
from datetime import timedelta, datetime, timezone
from sqlalchemy.orm import Session
import app.schemas as schemas, app.database as database, app.models as models
from app.config import settings


SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = int(settings.access_token_expire_minutes)


def create_token( data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    
    to_encode.update({"exp": expire, "sub":data.get("user_email")}) # payload
    
    # Create jwt
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str, credential_exception , db: Session = Depends(database.get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        email_from_jwt = payload.get("sub")
        
        if  email_from_jwt is None:
            raise credential_exception
        token_data = schemas.TokenData(email=email_from_jwt)
    
    except JWTError:
        raise credential_exception
    
    user = db.query(models.User).filter(models.User.email == email_from_jwt).first()
    
    if user is None:
        raise credential_exception
    
    
    return user
    
        
    
    