from fastapi import APIRouter, Depends, HTTPException, Request, status

from src.api.models import CourseCreateRequest, UserResponse
from src.api.routers.auth import get_current_user, require_admin

from src.domain.exceptions import AppError, DuplicateCourseCodeError
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


@router.post("/", dependencies=[Depends(require_admin)])
async def create_course_endpoint(
    payload: CourseCreateRequest,
    user: UserResponse = Depends(get_current_user),
    course_service: CourseService = Depends(CourseService),
    uow=Depends(get_uow),
):
    return course_service.create_course(**payload.model_dump(), uow=uow)
