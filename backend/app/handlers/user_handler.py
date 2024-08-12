from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..services.user_service import UserService
from ..repositories.user_repository import UserRepository
from ..schemas.user import UserCreate, UserLogin, UserResponse, Token
from ..utils.auth import create_access_token

class UserHandler:
    @staticmethod
    async def register_user(user: UserCreate, db: Session = Depends(get_db)):
        user_repo = UserRepository(db)
        user_service = UserService(user_repo)
        new_user = user_service.create_user(user.username, user.email, user.password)
        return UserResponse.from_orm(new_user)

    @staticmethod
    async def login_user(user: UserLogin, db: Session = Depends(get_db)):
        user_repo = UserRepository(db)
        user_service = UserService(user_repo)
        authenticated_user = user_service.authenticate_user(user.username, user.password)
        access_token = create_access_token(data={"sub": authenticated_user.username})
        return Token(access_token=access_token, token_type="bearer")