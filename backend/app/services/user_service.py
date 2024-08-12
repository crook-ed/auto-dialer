from ..repositories.user_repository import UserRepository
from ..models.user import User
from fastapi import HTTPException
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def create_user(self, username: str, email: str, password: str):
        if self.user_repository.get_by_username(username):
            raise HTTPException(status_code=400, detail="Username already registered")
        if self.user_repository.get_by_email(email):
            raise HTTPException(status_code=400, detail="Email already registered")
        
        hashed_password = pwd_context.hash(password)
        return self.user_repository.create(username, email, hashed_password)

    def authenticate_user(self, username: str, password: str):
        user = self.user_repository.get_by_username(username)
        if not user or not pwd_context.verify(password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Incorrect username or password")
        return user

    def get_user_by_username(self, username: str):
        user = self.user_repository.get_by_username(username)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user