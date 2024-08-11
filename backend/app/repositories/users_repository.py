from sqlalchemy.orm import Session
from ..models.user import User

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, username: str, email: str, hashed_password: str):
        db_user = User(username=username, email=email, hashed_password=hashed_password)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def get_by_username(self, username: str):
        return self.db.query(User).filter(User.username == username).first()

    def get_by_email(self, email: str):
        return self.db.query(User).filter(User.email == email).first()