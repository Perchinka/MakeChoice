from typing import Optional, List, cast
from uuid import UUID
from datetime import datetime
from sqlalchemy.orm import Session

from src.domain.repositories import AbstractCourseRepository
from src.domain.entities.course import Course
from src.infrastructure.db.models import CourseModel


class SqlAlchemyCourseRepo(AbstractCourseRepository):
    def __init__(self, session: Session):
        self.session = session

    def add(self, course: Course) -> None:
        model = CourseModel(
            id=course.id,
            code=course.code,
            title=course.title,
            description=course.description,
            max_seats=course.max_seats,
            created_at=course.created_at,
            updated_at=course.updated_at,
        )
        self.session.add(model)

    def get(self, course_id: UUID) -> Optional[Course]:
        m = self.session.query(CourseModel).filter_by(id=course_id).one_or_none()
        if m is None:
            return None
        return Course(
            id=cast(UUID, m.id),
            code=cast(str, m.code),
            title=cast(str, m.title),
            description=cast(Optional[str], m.description),
            max_seats=cast(int, m.max_seats),
            created_at=cast(datetime, m.created_at),
            updated_at=cast(datetime, m.updated_at),
        )

    def get_by_code(self, code: str) -> Optional[Course]:
        m = self.session.query(CourseModel).filter_by(code=code).one_or_none()
        if m is None:
            return None
        return Course(
            id=cast(UUID, m.id),
            code=cast(str, m.code),
            title=cast(str, m.title),
            description=cast(Optional[str], m.description),
            max_seats=cast(int, m.max_seats),
            created_at=cast(datetime, m.created_at),
            updated_at=cast(datetime, m.updated_at),
        )

    def list(self) -> List[Course]:
        models = self.session.query(CourseModel).all()
        return [
            Course(
                id=cast(UUID, m.id),
                code=cast(str, m.code),
                title=cast(str, m.title),
                description=cast(Optional[str], m.description),
                max_seats=cast(int, m.max_seats),
                created_at=cast(datetime, m.created_at),
                updated_at=cast(datetime, m.updated_at),
            )
            for m in models
        ]

    def update(self, course: Course) -> None:
        m = self.session.query(CourseModel).filter_by(id=course.id).one()
        for attr in ("code", "title", "description", "max_seats", "updated_at"):
            setattr(m, attr, getattr(course, attr))

    def delete(self, course_id: UUID) -> None:
        self.session.query(CourseModel).filter_by(id=course_id).delete(
            synchronize_session=False
        )
