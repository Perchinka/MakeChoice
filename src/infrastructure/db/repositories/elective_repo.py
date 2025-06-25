from datetime import datetime, timezone
from typing import List, Optional, cast
from uuid import UUID

from sqlalchemy.orm import Session

from src.domain.entities import Elective
from src.domain.exceptions import ElectiveNotFoundError
from src.domain.repositories import AbstractElectiveRepository
from src.infrastructure.db.models import CourseModel, ElectiveModel


class SqlAlchemyElectiveRepo(AbstractElectiveRepository):
    """
    SQLAlchemy implementation of the Elective repository.
    """

    def __init__(self, session: Session) -> None:
        self.session = session

    @staticmethod
    def _row_to_entity(row: ElectiveModel) -> Elective:
        return Elective(
            id=cast(UUID, row.id),
            code=cast(str, row.code),
            title=cast(str, row.title),
            description=cast(Optional[str], row.description),
            instructor=cast(str, row.instructor),
            category=cast(str, row.category),
            course_ids=[cast(UUID, c.id) for c in row.courses],
            created_at=cast(datetime, row.created_at),
            updated_at=cast(datetime, row.updated_at),
        )

    def add(self, elective: Elective) -> None:
        """
        Insert a new elective row based on the domain entity.
        """
        self.session.add(
            ElectiveModel(  # type: ignore[call-arg]
                id=elective.id,
                code=elective.code,
                title=elective.title,
                description=elective.description,
                instructor=elective.instructor,
                category=elective.category,
                created_at=elective.created_at,
                updated_at=elective.updated_at,
            )
        )

    def get(self, elective_id: UUID) -> Optional[Elective]:
        row = self.session.get(ElectiveModel, elective_id)
        return self._row_to_entity(row) if row else None

    def get_by_code(self, code: str) -> Optional[Elective]:
        row = self.session.query(ElectiveModel).filter_by(code=code).one_or_none()
        return self._row_to_entity(row) if row else None

    def list(self) -> List[Elective]:
        return [self._row_to_entity(r) for r in self.session.query(ElectiveModel).all()]

    def update(self, elective: Elective) -> None:
        """
        Persist attribute changes from the domain entity.
        """
        row: Optional[ElectiveModel] = self.session.get(ElectiveModel, elective.id)
        if row is None:
            raise ElectiveNotFoundError(f"Elective '{elective.id}' not found")

        row.code = elective.code  # type: ignore[assignment]
        row.title = elective.title  # type: ignore[assignment]
        row.description = elective.description  # type: ignore[assignment]
        row.instructor = elective.instructor  # type: ignore[assignment]
        row.category = elective.category  # type: ignore[assignment]
        row.updated_at = elective.updated_at  # type: ignore[assignment]

    def delete(self, elective_id: UUID) -> None:
        self.session.query(ElectiveModel).filter_by(id=elective_id).delete(
            synchronize_session=False
        )

    def set_courses(self, elective_id: UUID, course_ids: List[UUID]) -> None:
        """
        Replace all linked courses for the given elective.

        Flush first so the newly-inserted elective row (if any) is visible
        to SELECT; otherwise `session.get()` would return `None`.
        """
        self.session.flush()

        row: Optional[ElectiveModel] = self.session.get(ElectiveModel, elective_id)
        if row is None:
            raise ElectiveNotFoundError(f"Elective '{elective_id}' not found")

        row.courses = [
            self.session.get(CourseModel, cid)  # type: ignore[arg-type]
            for cid in course_ids
            if cid is not None
        ]
        row.updated_at = datetime.now(timezone.utc)  # type: ignore[assignment]
