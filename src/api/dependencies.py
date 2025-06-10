from src.infrastructure.db.uow import UnitOfWork


def get_uow():
    return UnitOfWork()
