from pydantic import BaseModel, EmailStr
from app.models.models import Role


class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    role: Role
    is_active: bool


class UserCreate(BaseModel):
    email: EmailStr
    full_name: str
    password: str
    role: Role


class User(UserBase):
    id: int

    class Config:
        from_attributes = True
