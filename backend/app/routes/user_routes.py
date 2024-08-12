from fastapi import APIRouter, Depends
from ..handlers.user_handler import UserHandler
from ..schemas.user import UserCreate, UserLogin, UserResponse

router = APIRouter()

@router.post("/register", response_model=UserResponse)
async def register_user(user: UserCreate, handler: UserHandler = Depends()):
    return await handler.register_user(user)

@router.post("/login")
async def login_user(user: UserLogin, handler: UserHandler = Depends()):
    return await handler.login_user(user)