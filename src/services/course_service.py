from datetime import datetime, timezone
from typing import List
from uuid import UUID, uuid4

from src.domain.entities.course import Course
from src.domain.unit_of_work import AbstractUnitOfWork


class CourseService:
    def list_courses(self, uow: AbstractUnitOfWork) -> List[Course]:
        with uow:
            return uow.courses.list()

    def create_course(
        self, name: str, tech_quota: int, hum_quota: int, uow: AbstractUnitOfWork
    ) -> Course:
        with uow:
            if uow.courses.get_by_name(name):
                raise ValueError("Course name already exists")
            now = datetime.now(timezone.utc)
            course = Course(
                id=uuid4(),
                name=name,
                tech_quota=tech_quota,
                hum_quota=hum_quota,
                created_at=now,
                updated_at=now,
            )
            uow.courses.add(course)
            return course
