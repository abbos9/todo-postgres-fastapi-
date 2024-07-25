from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime
from config import Tashkent_tz

class CreateUserSchema(BaseModel):
    username: str
    first_name: str
    last_name: str
    password: str
    phone_num: str = Field(examples=['+998(90)145-44-77'], pattern=r'^\+\d{3}\(\d{2}\)\d{3}-\d{2}-\d{2}$')
    role: str = Field(examples=["PM/developer/employee"], pattern="^(PM|developer|employee)$")

    class Config:
        orm_mode = True

class TokenSchema(BaseModel):
    access_token: str
    token_type: str

class UserResponseSchema(BaseModel):
    id: int
    username: str
    first_name: str
    last_name: str
    role:str

    class Config:
        orm_mode = True
        from_attributes=True


class CrudAssignmentSchema(BaseModel):
    title: str
    description: str
    priority: str
    created_at: datetime = datetime.now(tz=Tashkent_tz)
    updated_at: datetime = datetime.now(tz=Tashkent_tz)

    class Config:
        orm_mode = True

class ResponseAssignmentSchema(BaseModel):
    id: int
    title: str
    description: str
    priority: str
    is_complete: bool
    owner: UserResponseSchema

    class Config:
        orm_mode = True
        from_attributes = True

class UpdateAssignmentSchema(BaseModel):
    title: str
    description: str
    priority: str
    is_complete: bool
    updated_at: datetime = datetime.now(tz=Tashkent_tz)

    class Config:
        orm_mode = True