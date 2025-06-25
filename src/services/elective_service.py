from datetime import timezone
from typing import Any, Dict, List, Optional, Tuple
from src.domain.entities import Elective
from src.domain.exceptions import DuplicateElectiveCodeError
from src.domain.unit_of_work import AbstractUnitOfWork

from uuid import UUID, uuid4
from datetime import datetime


class ElectiveService:
    def list_electives(self, uow: AbstractUnitOfWork) -> List[Elective]:
        with uow:
            return uow.electives.list()

    def create_elective(
        self,
        code: str,
        title: str,
        description: str,
        max_seats: int,
        uow: AbstractUnitOfWork,
    ) -> Elective:

        with uow:
            if uow.electives.get_by_code(code):
                raise DuplicateelectiveCodeError(
                    f"elective code '{code}' already exists"
                )
            elective = Elective(
                id=uuid4(),
                code=code,
                title=title,
                description=description,
                max_seats=max_seats,
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc),
            )
            uow.electives.add(elective)
            return elective

    def import_electives(
        self, electives_data: List[Dict[str, Any]], uow: AbstractUnitOfWork
    ) -> Tuple[List[Elective], List[Tuple[Dict[str, Any], Elective]]]:
        """
        Returns a tuple:
         - List of newly created elective objects
         - List of (input_dict, existing_elective) for duplicates
        """
        imported: List[Elective] = []
        skipped: List[Tuple[Dict[str, Any], Elective]] = []

        for cd in electives_data:
            try:
                new_elective = self.create_elective(**cd, uow=uow)
                imported.append(new_elective)
            except DuplicateelectiveCodeError:
                existing = uow.electives.get_by_code(cd["code"])

                # existing should never be None here, but guard just in case
                if existing:
                    skipped.append((cd, existing))

        return imported, skipped

    def get_elective(
        self, elective_id: UUID, uow: AbstractUnitOfWork
    ) -> Optional[Elective]:
        with uow:
            return uow.electives.get(elective_id)

    def update_elective(
        self,
        elective_id: UUID,
        code: str,
        title: str,
        description: str,
        max_seats: int,
        uow: AbstractUnitOfWork,
    ) -> Optional[Elective]:
        with uow:
            elective = uow.electives.get(elective_id)
            if not elective:
                return None

            existing = uow.electives.get_by_code(code)
            if existing and existing.id != elective_id:
                raise DuplicateelectiveCodeError(
                    f"elective code '{code}' already exists"
                )

            elective.code = code
            elective.title = title
            elective.description = description
            elective.max_seats = max_seats
            elective.updated_at = datetime.now(timezone.utc)

            uow.electives.update(elective)
            return elective

    def delete_elective(self, elective_id: UUID, uow: AbstractUnitOfWork) -> bool:
        with uow:
            elective = uow.electives.get(elective_id)
            if not elective:
                return False
            uow.electives.delete(elective_id)
            return True

    def delete_all_electives(self, uow: AbstractUnitOfWork) -> int:
        with uow:
            electives = uow.electives.list()
            for c in electives:
                uow.electives.delete(c.id)
            return len(electives)
