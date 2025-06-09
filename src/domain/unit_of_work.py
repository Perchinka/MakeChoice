from abc import ABC, abstractmethod
from typing import Optional, Type, Any

from src.domain.repositories import UserRepository, CourseRepository, ChoiceRepository


class AbstractUnitOfWork(ABC):
    users: UserRepository
    courses: CourseRepository
    choices: ChoiceRepository

    def __enter__(self) -> "AbstractUnitOfWork":
        """
        Begin a transaction.
        """
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[Any],
    ) -> None:
        """
        On exit, commit if no exception, else rollback.
        """
        if exc_type:
            self.rollback()
        else:
            self.commit()

    @abstractmethod
    def commit(self) -> None:
        """Persist all changes."""
        ...

    @abstractmethod
    def rollback(self) -> None:
        """Revert all changes."""
        ...
