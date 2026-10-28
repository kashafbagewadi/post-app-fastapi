from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# Base schema for Posts table
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

# Extending base schema to be used for API Requested - uses the same fields from base
class PostRequest(PostBase):
    pass

# Extending base schema to be used for API Response - adds new fields to the existing base fields
class PostResponse(PostBase):
    id: int
    created_at: datetime
    class Config:
        orm_model = True

class User(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    class Config:
        orm_model = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str