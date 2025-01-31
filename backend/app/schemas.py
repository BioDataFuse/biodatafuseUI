from pydantic import BaseModel, EmailStr
from typing import Optional, Dict
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    name: str

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    preferences: Optional[Dict] = None

class PasswordUpdate(BaseModel):
    current_password: str
    new_password: str

class UserResponse(UserBase):
    id: int
    api_key: str
    is_active: bool
    preferences: Dict
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str