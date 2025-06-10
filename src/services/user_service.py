from uuid import UUID, uuid4
from datetime import datetime, timedelta, timezone
from typing import List
import jwt

from src.domain.entities import User
from src.domain.exceptions import UserNotFoundError
from src.domain.unit_of_work import AbstractUnitOfWork
from src.config import settings


class UserService:
    def promote(self, username: str, uow: AbstractUnitOfWork) -> User:
        with uow:
            user = uow.users.get_by_sso_id(username)
            if not user:
                raise UserNotFoundError(f"User '{username}' not found")
            user.is_admin = True
            user.updated_at = datetime.now(timezone.utc)
            uow.users.update(user)
            return user

    def list_users(self, uow: AbstractUnitOfWork) -> List[User]:
        with uow:
            return uow.users.list()

    def register_sso(
        self,
        *,
        sso_id: str,
        name: str,
        email: str,
        is_admin: bool,
        uow: AbstractUnitOfWork,
    ) -> User:
        with uow:
            user = uow.users.get_by_sso_id(sso_id)
            if user:
                user.name = name
                user.email = email
                user.is_admin = is_admin
                uow.users.update(user)
                return user

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
            uow.users.add(user)
            return user

    def is_admin(self, user_id: UUID, uow: AbstractUnitOfWork) -> bool:
        with uow:
            user = uow.users.get(user_id)
            return bool(user and user.is_admin)

    def create_access_token(self, user: User) -> str:
        payload = {
            "sub": str(user.id),
            "email": user.email,
            "name": user.name,
            "exp": datetime.now(timezone.utc)
            + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        }
        return jwt.encode(
            payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
        )
