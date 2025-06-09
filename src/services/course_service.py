from datetime import timezone
from typing import List
from domain.entities.course import Course
from domain.unit_of_work import AbstractUnitOfWork


class CourseService:
    def __init__(self, uow: AbstractUnitOfWork):
        self.uow = uow

    def list_courses(self) -> List[Course]:
        return self.uow.courses.list()

    def create_course(
        self,
        code: str,
        title: str,
        description: str,
        max_seats: int,
    ) -> Course:
        from uuid import uuid4
        from datetime import datetime

        if self.uow.courses.get_by_code(code):
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
        self.uow.courses.add(course)
        self.uow.commit()
        return course

    def import_courses(self, courses_data: List[dict]) -> int:
        """
        Bulk-import: courses_data is list of dict(code, title, description, max_seats).
        Returns number imported.
        """
        imported = 0
        for cd in courses_data:
            try:
                self.create_course(**cd)
                imported += 1
            except ValueError:
                continue  # skip duplicates
        return imported

    def export_courses(self) -> List[Course]:
        return self.list_courses()
