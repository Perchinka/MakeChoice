from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple
from uuid import UUID, uuid4

from src.domain.entities import Elective
from src.domain.exceptions import (
    DuplicateElectiveCodeError,
    UnknownCourseIDsError,
    ElectiveNotFoundError,
)
from src.domain.unit_of_work import AbstractUnitOfWork


class ElectiveService:
    # ─────────────────────── queries ───────────────────────
    def list_electives(self, uow: AbstractUnitOfWork) -> List[Elective]:
        with uow:
            return uow.electives.list()

    def get_elective(
        self, elective_id: UUID, uow: AbstractUnitOfWork
    ) -> Optional[Elective]:
        with uow:
            return uow.electives.get(elective_id)

    # ─────────────────────── commands ──────────────────────
    def _validate_course_ids(
        self, course_ids: List[UUID], uow: AbstractUnitOfWork
    ) -> None:
        missing = [cid for cid in course_ids if uow.courses.get(cid) is None]
        if missing:
            raise UnknownCourseIDsError(missing)

    def create_elective(
        self,
        *,
        code: str,
        title: str,
        description: Optional[str],
        instructor: str,
        category: str,
        course_ids: List[UUID],
        uow: AbstractUnitOfWork,
    ) -> Elective:
        with uow:
            if uow.electives.get_by_code(code):
                raise DuplicateElectiveCodeError(
                    f"Elective code '{code}' already exists"
                )

            self._validate_course_ids(course_ids, uow)

            now = datetime.now(timezone.utc)
            elective = Elective(
                id=uuid4(),
                code=code,
                title=title,
                description=description,
                instructor=instructor,
                category=category,
                course_ids=course_ids,
                created_at=now,
                updated_at=now,
            )
            uow.electives.add(elective)
            uow.electives.set_courses(elective.id, course_ids)
            return elective

    def update_elective(
        self,
        elective_id: UUID,
        *,
        code: str,
        title: str,
        description: Optional[str],
        instructor: str,
        category: str,
        course_ids: List[UUID],
        uow: AbstractUnitOfWork,
    ) -> Elective | None:
        with uow:
            elective = uow.electives.get(elective_id)
            if not elective:
                return None

            if (other := uow.electives.get_by_code(code)) and other.id != elective_id:
                raise DuplicateElectiveCodeError(
                    f"Elective code '{code}' already exists"
                )

            self._validate_course_ids(course_ids, uow)

            elective.code = code
            elective.title = title
            elective.description = description
            elective.instructor = instructor
            elective.category = category
            elective.course_ids = course_ids
            elective.updated_at = datetime.now(timezone.utc)

            uow.electives.update(elective)
            uow.electives.set_courses(elective.id, course_ids)
            return elective

    # ──────────────────── bulk import helper ────────────────────
    def import_electives(
        self, data: List[Dict[str, Any]], uow: AbstractUnitOfWork
    ) -> Tuple[List[Elective], List[Tuple[Dict[str, Any], Elective]]]:
        imported: List[Elective] = []
        skipped: List[Tuple[Dict[str, Any], Elective]] = []

        for payload in data:
            try:
                imported.append(self.create_elective(**payload, uow=uow))
            except DuplicateElectiveCodeError:
                if existing := uow.electives.get_by_code(payload["code"]):
                    skipped.append((payload, existing))

        return imported, skipped
