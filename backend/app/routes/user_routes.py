from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..handlers.user_handler import UserHandler
from ..schemas.user import UserCreate, UserLogin, UserResponse
from ..database import get_db
from ..utils.auth import get_current_user, create_access_token
from ..models.user import User
from datetime import timedelta
from ..config import settings

router = APIRouter()

@router.post("/register", response_model=UserResponse)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    handler = UserHandler(db)
    return await handler.register_user(user)

@router.post("/login")
async def login_user(user: UserLogin, db: Session = Depends(get_db)):
    handler = UserHandler(db)
    return await handler.login_user(user)

@router.post("/refresh-token")
async def refresh_token(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not current_user:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    new_access_token = create_access_token(
        data={"sub": current_user.username}, expires_delta=access_token_expires
    )
    return {"access_token": new_access_token, "token_type": "bearer"}