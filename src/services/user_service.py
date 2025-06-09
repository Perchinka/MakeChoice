from uuid import uuid4
from datetime import datetime, timedelta
from typing import Optional, List
import jwt

from domain.entities.user import User
from domain.unit_of_work import AbstractUnitOfWork
from src.config import settings


class UserService:
    def __init__(self, uow: AbstractUnitOfWork):
        self.uow = uow

    def register(self, username: str, password: str) -> User:
        if self.uow.users.get_by_sso_id(username):
            raise ValueError("User already exists")
        user = User(
            id=uuid4(),
            sso_id=username,
            name=username,
            email="",
            is_admin=False,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        self.uow.users.add(user)
        self.uow.commit()
        return user

    def promote(self, username: str) -> User:
        user = self.uow.users.get_by_sso_id(username)
        if not user:
            raise ValueError("User not found")
        user.is_admin = True
        user.updated_at = datetime.utcnow()
        self.uow.users.update(user)
        self.uow.commit()
        return user

    def list_users(self) -> List[User]:
        return self.uow.users.list()

    def create_access_token(self, user: User) -> str:
        payload = {
            "sub": str(user.id),
            "is_admin": user.is_admin,
            "exp": datetime.utcnow()
            + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        }
        return jwt.encode(
            payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
        )
