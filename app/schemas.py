from pydantic import BaseModel, EmailStr, Field
from typing import Literal
import uuid
import datetime

class ProductCreate(BaseModel):
    name        : str
    cost_price  : float
    sell_price  : float

class UserCreate(BaseModel):
    email       : EmailStr
    password    : str = Field(min_length=8)

class UserLogin(BaseModel):
    email       : EmailStr
    password    : str

class TokenResponse(BaseModel):
    access_token  : str
    refresh_token : str
    token_type    : Literal["Bearer"] = "Bearer"
    expires_in    : str

class UserResponse(BaseModel):
    id          : uuid.UUID
    email       : str
    created_at  : datetime.datetime

class AuthResponse(BaseModel):
    user    : UserResponse
    tokens  : TokenResponse