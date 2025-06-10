from uuid import uuid4
from datetime import datetime, timedelta, timezone
from typing import Optional, List
import jwt

from src.domain.entities.user import User
from src.domain.unit_of_work import AbstractUnitOfWork
from src.config import settings


class UserService:
    def __init__(self, uow: AbstractUnitOfWork):
        self.uow = uow

    def promote(self, username: str) -> User:
        user = self.uow.users.get_by_sso_id(username)
        if not user:
            raise ValueError("User not found")
        user.is_admin = True
        user.updated_at = datetime.now(timezone.utc)
        self.uow.users.update(user)
        self.uow.commit()
        return user

    def list_users(self) -> List[User]:
        return self.uow.users.list()

    def register_sso(
        self, *, sso_id: str, name: str, email: str, is_admin: bool
    ) -> User:
        if self.uow.users.get_by_sso_id(sso_id):
            raise ValueError("SSO user already exists")

        now = datetime.now(timezone.utc)
        user = User(
            id=uuid4(),
            sso_id=sso_id,
            name=name,
            email=email,
            is_admin=is_admin,
            created_at=now,
            updated_at=now,
        )
        self.uow.users.add(user)
        self.uow.commit()
        return user

    def create_access_token(self, user: User) -> str:
        payload = {
            "sub": str(user.id),
            "is_admin": user.is_admin,
            "exp": datetime.now(timezone.utc)
            + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        }
        return jwt.encode(
            payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
        )
