from fastapi import APIRouter, Depends, HTTPException, Body
from app.schemas import AuthResponse, UserCreate, UserResponse, TokenResponse
from app.dependencies import get_db
from app.models import User
from app.services.auth import hash_pwd, create_access_token, create_refresh_token
from sqlalchemy import select
import traceback

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
        print("\n=== CRITICAL API CRASH TRACEBACK ===")
        traceback.print_exc()
        print("====================================\n")
        raise HTTPException(status_code=500, detail=str(e))

def _issue_tokens(user):
    return TokenResponse(
        access_token = create_access_token(user.id, user.groups),
        refresh_token = create_refresh_token(user.id)
    )