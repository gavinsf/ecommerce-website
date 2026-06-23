from fastapi import APIRouter, Depends, HTTPException, Body
from app.schemas import AuthResponse, UserCreate, UserResponse, TokenResponse, UserLogin, RefreshRequest
from app.dependencies import get_db
from app.models import User
from app.services.auth import hash_pwd, create_access_token, create_refresh_token, verify_pwd, decode_token
from sqlalchemy import select
import traceback
from app.config import settings

router = APIRouter(tags=["auth"])


@router.post("/register", response_model=AuthResponse)
async def register(payload: UserCreate = Body(...), db=Depends(get_db)):
    try:
        sel = select(User).where(User.email == payload.email)
        res = await db.execute(sel)
        user = res.scalars().first()

        if user:
            raise HTTPException(status_code=409, detail="Email already in use")

        new_user = User(
            email = payload.email,
            hash = hash_pwd(payload.password)
        )
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)

        return AuthResponse(
            user = UserResponse.model_validate(new_user),
            tokens = _issue_tokens(new_user)
        )
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
    

@router.post("/login", response_model=AuthResponse)
async def login(payload: UserLogin = Body(...), db=Depends(get_db)):
    try:
        sel = select(User).where(User.email == payload.email)
        res = await db.execute(sel)
        user = res.scalars().first()

        if not user or not verify_pwd(payload.password, user.hash):
            raise HTTPException(status_code=401)

        return AuthResponse(
            user=UserResponse.model_validate(user),
            tokens=_issue_tokens(user),
        )
    except HTTPException:
        raise
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(payload: RefreshRequest, db=Depends(get_db)):
    claims = decode_token(payload.refresh_token)
    if claims["type"] != "refresh":
        raise HTTPException(status_code=401, detail="Token type isn't refresh")

    sel = select(User).where(User.id == claims["sub"])
    res = await db.execute(sel)
    user = res.scalars().first()
    return _issue_tokens(user)

def _issue_tokens(user):
    groups = ["admin"] if user.is_admin == 1 else ["user"]

    return TokenResponse(
        access_token = create_access_token(user.id, groups),
        refresh_token = create_refresh_token(user.id),
        expires_in = settings.ACCESS_TOKEN_EXPIRE
    )