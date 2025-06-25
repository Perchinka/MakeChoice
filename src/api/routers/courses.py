from datetime import datetime
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, Field

from src.api.dependencies import get_uow
from src.api.routers.auth import require_admin
from src.domain.unit_of_work import AbstractUnitOfWork
from src.services.course_service import CourseService

router = APIRouter(prefix="/courses", tags=["courses"])


class CourseCreateRequest(BaseModel):
    name: str = Field(..., min_length=1, description="Course code, e.g. BS1")
    tech_quota: int = Field(..., ge=0, description="How many Tech electives allowed")
    hum_quota: int = Field(..., ge=0, description="How many Hum electives allowed")


class CourseResponse(CourseCreateRequest):
    id: UUID
    created_at: datetime
    updated_at: datetime


@router.post(
    "/",
    response_model=CourseResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[require_admin],
)
def create_course(
    payload: CourseCreateRequest,
    svc: CourseService = Depends(),
    uow: AbstractUnitOfWork = Depends(get_uow),
):
    course = svc.create_course(
        name=payload.name,
        tech_quota=payload.tech_quota,
        hum_quota=payload.hum_quota,
        uow=uow,
    )
    return CourseResponse(**course.model_dump())


@router.get("/", response_model=List[CourseResponse])
def list_courses(
    svc: CourseService = Depends(),
    uow: AbstractUnitOfWork = Depends(get_uow),
):
    return [CourseResponse(**c.model_dump()) for c in svc.list_courses(uow)]
