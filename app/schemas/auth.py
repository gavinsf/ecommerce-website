from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Literal
import uuid
import datetime


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
    expires_in    : int

class UserResponse(BaseModel):
    id          : uuid.UUID
    email       : str
    created_at  : datetime.datetime
    is_admin    : int
    model_config = ConfigDict(from_attributes=True)

class AuthResponse(BaseModel):
    user    : UserResponse
    tokens  : TokenResponse

class RefreshRequest(BaseModel):
    refresh_token : str