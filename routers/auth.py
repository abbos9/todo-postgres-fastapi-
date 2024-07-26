from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError
from datetime import timedelta

from config import ACCESS_TOKEN_EXPIRE_MINUTES
from database import SessionLocal
from models import UsersTable
from schemas import CreateUserSchema, TokenSchema, UserResponseSchema
from utils.auth_utils import bcrypt_context, authenticate_user, create_access_token, get_current_user

router = APIRouter(
    prefix="/auth",
    tags=['Auth']
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(create_user_schema: CreateUserSchema, db: Session = Depends(get_db)):
    try:
        create_user_model = UsersTable(
            username=create_user_schema.username,
            hashed_password=bcrypt_context.hash(create_user_schema.password),
            first_name=create_user_schema.first_name,
            last_name=create_user_schema.last_name,
            role=create_user_schema.role,
            phone_num=create_user_schema.phone_num
        )
        db.add(create_user_model)
        db.commit()
        return {"message": f"Successfully registered {create_user_schema.first_name} {create_user_schema.last_name}"}
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username or phone number already exists")

@router.post('/token/', response_model=TokenSchema)
async def signin_by_access_token(data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, data.username, data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user.")
    token = create_access_token(username=user.username, user_id=user.id,
    first_name=user.first_name, last_name=user.last_name,
    role=user.role,expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    return {
        'access_token': token,
        'token_type': 'bearer'
    }

@router.get("/users/me/", response_model=UserResponseSchema)
def auth_user_check_self_info(user: UserResponseSchema = Depends(get_current_user)):
    return user
