from fastapi import Depends
from domain.unit_of_work import AbstractUnitOfWork
from src.infrastructure.db.uow import SqlAlchemyUnitOfWork


def get_uow() -> AbstractUnitOfWork:
    with SqlAlchemyUnitOfWork() as uow:
        yield uow
