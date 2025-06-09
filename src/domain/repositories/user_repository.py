from abc import ABC, abstractmethod
from typing import Optional, List
from uuid import UUID
from src.domain.entities.user import User


class UserRepository(ABC):
    """Interface for User persistence."""

    @abstractmethod
    def add(self, user: User) -> None:
        """Insert a new User."""
        ...

    @abstractmethod
    def get(self, user_id: UUID) -> Optional[User]:
        """Fetch a User by its UUID."""
        ...

    @abstractmethod
    def get_by_sso_id(self, sso_id: str) -> Optional[User]:
        """Fetch a User by their SSO identifier."""
        ...

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]:
        """Fetch a User by email address."""
        ...

    @abstractmethod
    def list(self) -> List[User]:
        """Return all Users."""
        ...

    @abstractmethod
    def update(self, user: User) -> None:
        """Persist changes to an existing User."""
        ...
