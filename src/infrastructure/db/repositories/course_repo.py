from datetime import datetime, timezone
from typing import List, Optional, cast
from uuid import UUID
from sqlalchemy.orm import Session

from src.domain.entities.course import Course
from src.domain.repositories.abstract_course_repository import AbstractCourseRepository
from src.infrastructure.db.models import CourseModel


class SqlAlchemyCourseRepo(AbstractCourseRepository):
    def __init__(self, session: Session):
        self.session = session

    def add(self, course: Course) -> None:
        self.session.add(CourseModel(**course.model_dump()))

    def get(self, course_id: UUID) -> Optional[Course]:
        m = self.session.get(CourseModel, course_id)
        return Course(**m.__dict__) if m else None

    def get_by_name(self, name: str) -> Optional[Course]:
        m = self.session.query(CourseModel).filter_by(name=name).one_or_none()
        return Course(**m.__dict__) if m else None

    def list(self) -> List[Course]:
        return [Course(**m.__dict__) for m in self.session.query(CourseModel).all()]

    def update(self, course: Course) -> None:
        self.session.merge(course.model_dump())

    def delete(self, course_id: UUID) -> None:
        self.session.query(CourseModel).filter_by(id=course_id).delete(
            synchronize_session=False
        )
