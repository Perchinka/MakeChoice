from typing import Optional, List, cast
from uuid import UUID
from datetime import datetime, timezone
from sqlalchemy.orm import Session

from src.domain.repositories import AbstractUserRepository
from src.domain.entities.user import User
from src.infrastructure.db.models import UserModel


class SqlAlchemyUserRepo(AbstractUserRepository):
    def __init__(self, session: Session):
        self.session = session

    def add(self, user: User) -> None:
        model = UserModel(
            id=user.id,
            sso_id=user.sso_id,
            name=user.name,
            email=user.email,
            is_admin=user.is_admin,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )
        self.session.add(model)

    def get(self, user_id: UUID) -> Optional[User]:
        m = self.session.query(UserModel).filter_by(id=user_id).one_or_none()
        if m is None:
            return None
        return User(
            id=cast(UUID, m.id),
            sso_id=cast(str, m.sso_id),
            name=cast(str, m.name),
            email=cast(str, m.email),
            is_admin=cast(bool, m.is_admin),
            created_at=cast(datetime, m.created_at),
            updated_at=cast(datetime, m.updated_at),
        )

    def get_by_sso_id(self, sso_id: str) -> Optional[User]:
        m = self.session.query(UserModel).filter_by(sso_id=sso_id).one_or_none()
        if m is None:
            return None
        return User(
            id=cast(UUID, m.id),
            sso_id=cast(str, m.sso_id),
            name=cast(str, m.name),
            email=cast(str, m.email),
            is_admin=cast(bool, m.is_admin),
            created_at=cast(datetime, m.created_at),
            updated_at=cast(datetime, m.updated_at),
        )

    def get_by_email(self, email: str) -> Optional[User]:
        m = self.session.query(UserModel).filter_by(email=email).one_or_none()
        if m is None:
            return None
        return User(
            id=cast(UUID, m.id),
            sso_id=cast(str, m.sso_id),
            name=cast(str, m.name),
            email=cast(str, m.email),
            is_admin=cast(bool, m.is_admin),
            created_at=cast(datetime, m.created_at),
            updated_at=cast(datetime, m.updated_at),
        )

    def list(self) -> List[User]:
        models = self.session.query(UserModel).all()
        users: List[User] = []
        for m in models:
            users.append(
                User(
                    id=cast(UUID, m.id),
                    sso_id=cast(str, m.sso_id),
                    name=cast(str, m.name),
                    email=cast(str, m.email),
                    is_admin=cast(bool, m.is_admin),
                    created_at=cast(datetime, m.created_at),
                    updated_at=cast(datetime, m.updated_at),
                )
            )
        return users

    def update(self, user: User) -> None:
        m = self.session.query(UserModel).filter_by(id=user.id).one()
        for attr in ("name", "email", "is_admin"):
            setattr(m, attr, getattr(user, attr))
        object.__setattr__(m, "updated_at", datetime.now(timezone.utc))
