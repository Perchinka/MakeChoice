from datetime import timezone
from typing import List
from domain.entities.course import Course
from domain.unit_of_work import AbstractUnitOfWork

from uuid import uuid4
from datetime import datetime


class CourseService:
    def __init__(self, uow: AbstractUnitOfWork):
        self.uow = uow

    def list_courses(self) -> List[Course]:
        with self.uow as uow:
            return uow.courses.list()

    def create_course(
        self,
        code: str,
        title: str,
        description: str,
        max_seats: int,
    ) -> Course:

        with self.uow as uow:
            if uow.courses.get_by_code(code):
                raise ValueError("Course code already exists")
            course = Course(
                id=uuid4(),
                code=code,
                title=title,
                description=description,
                max_seats=max_seats,
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc),
            )
            uow.courses.add(course)
            return course

    def import_courses(self, courses_data: List[dict]) -> int:
        imported = 0
        for cd in courses_data:
            try:
                self.create_course(**cd)
                imported += 1
            except ValueError:
                continue  # skip duplicates
        return imported
