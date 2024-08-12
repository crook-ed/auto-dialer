from sqlalchemy.orm import Session
from ..services.user_service import UserService
from ..repositories.user_repository import UserRepository
from ..schemas.user import UserCreate, UserLogin, UserResponse
from ..utils.auth import create_access_token

class UserHandler:
    def __init__(self, db: Session):
        self.db = db
        self.user_repo = UserRepository(db)
        self.user_service = UserService(self.user_repo)

    async def register_user(self, user: UserCreate):
        new_user = self.user_service.create_user(user.username, user.email, user.password)
        return UserResponse.from_orm(new_user)

    async def login_user(self, user: UserLogin):
        authenticated_user = self.user_service.authenticate_user(user.username, user.password)
        access_token = create_access_token(data={"sub": authenticated_user.username})
        return {"access_token": access_token, "token_type": "bearer"}