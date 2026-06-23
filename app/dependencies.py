from app.database import SessionLocal
from fastapi.security import HTTPBearer
from fastapi import Depends, HTTPException
from app.services.auth import decode_token
from app.models import User
from sqlalchemy import select

bearer = HTTPBearer()

async def get_db():
    # yields an async DB session per request, auto-closes on exit
    async with SessionLocal() as session:
        yield session

async def get_current_user(token=Depends(bearer), db=Depends(get_db)):
    claims = decode_token(token.credentials)

    sel = select(User).where(User.id == claims["sub"])
    res = await db.execute(sel)
    user = res.scalars().first()

    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    
    user.groups = claims["groups"]
    return user

async def require_admin(user=Depends(get_current_user)):
    if "admin" not in user.groups:
        raise HTTPException(status_code=403, detail="Admin required")
    return user