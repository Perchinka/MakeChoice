from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from uuid import UUID

from src.domain.unit_of_work import AbstractUnitOfWork
from src.api.routers.auth import get_current_admin
from src.infrastructure.db.uow import UnitOfWork
from src.api.models.selection import SelectionItem

router = APIRouter()


def get_uow() -> AbstractUnitOfWork:
    return UnitOfWork()


@router.get(
    "/users/{user_id}/selection",
    response_model=List[SelectionItem],
    dependencies=[Depends(get_current_admin)],
)
def read_user_selection(
    user_id: UUID,
    uow: AbstractUnitOfWork = Depends(get_uow),
):
    # verify the user even exists (optional)
    from domain.repositories.user_repository import UserRepository

    if uow.users.get(user_id) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    return get_user_selection(uow, user_id)
