from typing import Any, Dict, List
from uuid import UUID
from fastapi import APIRouter, Depends, File, HTTPException, Request, UploadFile, status

from src.api.models import (
    CourseCreateRequest,
    CourseResponse,
    ImportCoursesReport,
    SkippedCourse,
)
from src.api.routers.auth import get_current_user, require_admin

from src.domain.unit_of_work import AbstractUnitOfWork
from src.services import CourseService

from src.api.dependencies import get_uow

import csv
import io

router = APIRouter()


@router.get("/")
async def courses(
    request: Request,
    course_service: CourseService = Depends(CourseService),
    uow=Depends(get_uow),
) -> List[CourseResponse]:
    return course_service.list_courses(uow=uow)


@router.get("/{course_id}", response_model=CourseResponse)
async def get_course(
    course_id: UUID,
    course_service: CourseService = Depends(CourseService),
    uow: AbstractUnitOfWork = Depends(get_uow),
):
    course = course_service.get_course(course_id, uow)
    if not course:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Course not found")
    return course


@router.put(
    "/{course_id}",
    response_model=CourseResponse,
    dependencies=[Depends(require_admin)],
)
async def update_course(
    course_id: UUID,
    payload: CourseCreateRequest,
    course_service: CourseService = Depends(CourseService),
    uow: AbstractUnitOfWork = Depends(get_uow),
):
    updated = course_service.update_course(course_id, **payload.model_dump(), uow=uow)
    if not updated:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Course not found")
    return updated


@router.delete(
    "/{course_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_admin)],
)
async def delete_course(
    course_id: UUID,
    course_service: CourseService = Depends(CourseService),
    uow: AbstractUnitOfWork = Depends(get_uow),
):
    if not course_service.delete_course(course_id, uow):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Course not found")


@router.delete(
    "/",
    dependencies=[Depends(require_admin)],
)
async def delete_all_courses(
    course_service: CourseService = Depends(CourseService),
    uow: AbstractUnitOfWork = Depends(get_uow),
):
    count = course_service.delete_all_courses(uow)
    return {"deleted": count}


@router.post(
    "/from_file",
    response_model=ImportCoursesReport,
    dependencies=[Depends(require_admin)],
)
async def import_courses_from_file(
    file: UploadFile = File(...),
    course_service: CourseService = Depends(CourseService),
    uow: AbstractUnitOfWork = Depends(get_uow),
):
    raw = await file.read()
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        raise HTTPException(400, "File must be UTF-8 encoded")

    reader = csv.DictReader(io.StringIO(text))
    courses_data: List[Dict[str, Any]] = []
    for row in reader:
        try:
            row["max_seats"] = int(row["max_seats"])
        except Exception as e:
            raise HTTPException(422, f"Invalid data in CSV row: {e}")
        courses_data.append(row)

    if not courses_data:
        raise HTTPException(400, "No course records found in file")

    with uow:
        imported, skipped = course_service.import_courses(courses_data, uow)
        uow._commit()

    imported_out = [CourseResponse(**c.__dict__) for c in imported]
    skipped_out = [
        SkippedCourse(
            input=CourseCreateRequest(**inp),
            existing=CourseResponse(**existing.__dict__),
        )
        for inp, existing in skipped
    ]

    return ImportCoursesReport(imported=imported_out, skipped=skipped_out)
