from datetime import timezone
from typing import Any, Dict, List, Optional, Tuple
from src.domain.entities.course import Course
from src.domain.exceptions import DuplicateCourseCodeError
from src.domain.unit_of_work import AbstractUnitOfWork

from uuid import UUID, uuid4
from datetime import datetime


class CourseService:
    def list_courses(self, uow: AbstractUnitOfWork) -> List[Course]:
        with uow:
            return uow.courses.list()

    def create_course(
        self,
        code: str,
        title: str,
        description: str,
        max_seats: int,
        uow: AbstractUnitOfWork,
    ) -> Course:

        with uow:
            if uow.courses.get_by_code(code):
                raise DuplicateCourseCodeError(f"Course code '{code}' already exists")
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

    def import_courses(
        self, courses_data: List[Dict[str, Any]], uow: AbstractUnitOfWork
    ) -> Tuple[List[Course], List[Tuple[Dict[str, Any], Course]]]:
        """
        Returns a tuple:
         - List of newly created Course objects
         - List of (input_dict, existing_course) for duplicates
        """
        imported: List[Course] = []
        skipped: List[Tuple[Dict[str, Any], Course]] = []

        for cd in courses_data:
            try:
                new_course = self.create_course(**cd, uow=uow)
                imported.append(new_course)
            except DuplicateCourseCodeError:
                existing = uow.courses.get_by_code(cd["code"])

                # existing should never be None here, but guard just in case
                if existing:
                    skipped.append((cd, existing))

        return imported, skipped

    def get_course(self, course_id: UUID, uow: AbstractUnitOfWork) -> Optional[Course]:
        with uow:
            return uow.courses.get(course_id)

    def update_course(
        self,
        course_id: UUID,
        code: str,
        title: str,
        description: str,
        max_seats: int,
        uow: AbstractUnitOfWork,
    ) -> Optional[Course]:
        with uow:
            course = uow.courses.get(course_id)
            if not course:
                return None

            existing = uow.courses.get_by_code(code)
            if existing and existing.id != course_id:
                raise DuplicateCourseCodeError(f"Course code '{code}' already exists")

            course.code = code
            course.title = title
            course.description = description
            course.max_seats = max_seats
            course.updated_at = datetime.now(timezone.utc)

            uow.courses.update(course)
            return course

    def delete_course(self, course_id: UUID, uow: AbstractUnitOfWork) -> bool:
        with uow:
            course = uow.courses.get(course_id)
            if not course:
                return False
            uow.courses.delete(course_id)
            return True

    def delete_all_courses(self, uow: AbstractUnitOfWork) -> int:
        with uow:
            courses = uow.courses.list()
            for c in courses:
                uow.courses.delete(c.id)
            return len(courses)
