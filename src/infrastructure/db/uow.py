from typing import Optional, Type, Any
from src.domain.unit_of_work import AbstractUnitOfWork
from src.infrastructure.db.session import create_session

from src.infrastructure.db.repositories import (
    SqlAlchemyUserRepo,
    SqlAlchemyCourseRepo,
    SqlAlchemyChoiceRepo,
)


class UnitOfWork(AbstractUnitOfWork):
    """
    SQLAlchemy-backed UoW. Creates a new Session on enter,
    provides repo implementations, and handles commit/rollback.
    """

    def __enter__(self) -> "UnitOfWork":
        self.session = create_session()
        self.users = SqlAlchemyUserRepo(self.session)
        self.courses = SqlAlchemyCourseRepo(self.session)
        self.choices = SqlAlchemyChoiceRepo(self.session)
        return self

    def _commit(self) -> None:
        self.session.commit()

    def rollback(self) -> None:
        self.session.rollback()

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[Any],
    ) -> None:
        super().__exit__(exc_type, exc_val, exc_tb)
        self.session.close()
