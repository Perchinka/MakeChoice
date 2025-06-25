from abc import ABC, abstractmethod
from typing import Optional, Type, Any

from src.domain.repositories import (
    AbstractUserRepository,
    AbstractElectiveRepository,
    AbstractChoiceRepository,
)


class AbstractUnitOfWork(ABC):
    users: AbstractUserRepository
    electives: AbstractElectiveRepository
    choices: AbstractChoiceRepository

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
            self._commit()

    @abstractmethod
    def _commit(self) -> None:
        """Persist all changes."""
        ...

    @abstractmethod
    def rollback(self) -> None:
        """Revert all changes."""
        ...
