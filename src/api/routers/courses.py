from fastapi import APIRouter, Depends, Request

from src.api.models import UserResponse
from src.api.routers.auth import get_current_user

from src.services import CourseService

from src.api.dependencies import get_uow

router = APIRouter()


@router.get("/")
async def courses(
    request: Request,
    user: UserResponse = Depends(get_current_user),
    course_service: CourseService = Depends(CourseService),
    uow=Depends(get_uow),
):
    return course_service.list_courses(uow=uow)
