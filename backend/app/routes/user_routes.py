from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..handlers.user_handler import UserHandler
from ..schemas.user import UserCreate, UserLogin, UserResponse
from ..database import get_db

router = APIRouter()

@router.post("/register", response_model=UserResponse)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    handler = UserHandler(db)
    return await handler.register_user(user)

@router.post("/login")
async def login_user(user: UserLogin, db: Session = Depends(get_db)):
    handler = UserHandler(db)
    return await handler.login_user(user)