from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from database import SessionLocal
from models import UsersTable
from schemas import UserResponseSchema
from config import SECRET_KEY, ALGORITHM

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = HTTPBearer()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_access_token(username: str, user_id: int, first_name: str, last_name: str, expires_delta: timedelta, role:str):
    encode = {
        "sub": username,
        "id": user_id,
        "first_name": first_name,
        "last_name": last_name,
        "role":role,
        "exp": datetime.utcnow() + expires_delta
    }
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

def authenticate_user(db: Session, username: str, password: str):
    db_user = db.query(UsersTable).filter(UsersTable.username == username).first()
    if not db_user or not bcrypt_context.verify(password, db_user.hashed_password):
        return False
    return db_user

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(oauth2_bearer), db: Session = Depends(get_db)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        role:str = payload.get("role")
        if username is None or user_id is None or role is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user.")
        db_user = db.query(UsersTable).filter(UsersTable.id == user_id).first()
        if db_user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user.")
        return UserResponseSchema.from_orm(db_user)
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user.")
