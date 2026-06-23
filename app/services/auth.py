from jose import JWTError, jwt
import bcrypt
from app.config import settings
import uuid
from datetime import datetime, UTC, timedelta
from fastapi import HTTPException


def hash_pwd(password: str):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_pwd(plain: str, hashed: str):
    return bcrypt.checkpw(plain.encode(), hashed.encode())

def create_access_token(user_id: uuid.UUID, groups: list[str]):
    claims = {
        "sub"    : str(user_id),
        "groups" : groups,
        "type"   : "access",
        "exp"    : datetime.now(UTC) + timedelta(seconds=settings.ACCESS_TOKEN_EXPIRE)
    }
    return jwt.encode(claims, settings.JWT_SECRET, algorithm="HS256")

def create_refresh_token(user_id: uuid.UUID):
    claims = {
        "sub"   : str(user_id),
        "type"  : "refresh",
        "exp"   : datetime.now(UTC) + timedelta(seconds=settings.REFRESH_TOKEN_EXPIRE)
    }
    return jwt.encode(claims, settings.JWT_SECRET, algorithm="HS256")

def decode_token(token: str):
    try:
        return jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])
    except JWTError as e:
        print("JWT ERROR:", type(e).__name__, str(e))
        raise HTTPException(status_code=401, detail="Invalid or expired token")
