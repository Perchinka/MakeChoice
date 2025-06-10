from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, Body, status, Path

from src.api.models import ChoiceItem, UserResponse
from src.api.routers.auth import get_current_user
from src.api.dependencies import get_uow
from src.services.choice_service import ChoiceService

router = APIRouter(prefix="/choices", tags=["choices"])


@router.get("/", response_model=List[ChoiceItem])
async def list_choices(
    user: UserResponse = Depends(get_current_user),
    svc: ChoiceService = Depends(ChoiceService),
    uow=Depends(get_uow),
):
    """Return this student’s choices, ordered by priority ascending."""
    user_id = UUID(user.sub)
    choices = svc.list_user_choices(user_id, uow)
    return [
        ChoiceItem(priority=choice.priority, course_id=choice.course_id)
        for choice in choices
    ]


@router.post(
    "/",
    response_model=List[ChoiceItem],
    status_code=status.HTTP_200_OK,
    summary="Replace all choices by ordered list of course IDs",
)
async def replace_choices(
    course_ids: List[UUID] = Body(
        ...,
        description="Ordered list of course UUIDs (first = priority 1, next = 2, …)",
        example=[
            "ed51f07e-afb5-4c9e-ba6e-150869922073",
            "fc2dcd26-3b69-4fdd-ad30-c0f1a7c4b595",
        ],
    ),
    user: UserResponse = Depends(get_current_user),
    svc: ChoiceService = Depends(ChoiceService),
    uow=Depends(get_uow),
):
    user_id = UUID(user.sub)
    created = svc.replace_user_choices(user_id=user_id, course_ids=course_ids, uow=uow)

    return [
        ChoiceItem(priority=choice.priority, course_id=choice.course_id)
        for choice in created
    ]


@router.delete(
    "/{priority}",
    response_model=List[ChoiceItem],
    status_code=status.HTTP_200_OK,
    summary="Remove one choice by priority",
)
async def delete_choice(
    priority: int = Path(..., ge=1),
    user: UserResponse = Depends(get_current_user),
    svc: ChoiceService = Depends(ChoiceService),
    uow=Depends(get_uow),
):
    """
    Deletes the choice at `priority` and shifts lower priorities up.
    """
    user_id = UUID(user.sub)
    updated = svc.remove_choice(user_id=user_id, priority=priority, uow=uow)

    return [ChoiceItem(priority=c.priority, course_id=c.course_id) for c in updated]
