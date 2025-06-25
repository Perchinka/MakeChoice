from typing import Optional, List, cast
from uuid import UUID
from datetime import datetime
from sqlalchemy.orm import Session

from src.domain.repositories import AbstractElectiveRepository
from src.domain.entities import Elective
from src.infrastructure.db.models import ElectiveModel


class SqlAlchemyElectiveRepo(AbstractElectiveRepository):
    def __init__(self, session: Session):
        self.session = session

    def add(self, elective: Elective) -> None:
        model = ElectiveModel(
            id=elective.id,
            code=elective.code,
            title=elective.title,
            description=elective.description,
            max_seats=elective.max_seats,
            created_at=elective.created_at,
            updated_at=elective.updated_at,
        )
        self.session.add(model)

    def get(self, elective_id: UUID) -> Optional[Elective]:
        m = self.session.query(ElectiveModel).filter_by(id=elective_id).one_or_none()
        if m is None:
            return None
        return Elective(
            id=cast(UUID, m.id),
            code=cast(str, m.code),
            title=cast(str, m.title),
            description=cast(Optional[str], m.description),
            max_seats=cast(int, m.max_seats),
            created_at=cast(datetime, m.created_at),
            updated_at=cast(datetime, m.updated_at),
        )

    def get_by_code(self, code: str) -> Optional[Elective]:
        m = self.session.query(ElectiveModel).filter_by(code=code).one_or_none()
        if m is None:
            return None
        return Elective(
            id=cast(UUID, m.id),
            code=cast(str, m.code),
            title=cast(str, m.title),
            description=cast(Optional[str], m.description),
            max_seats=cast(int, m.max_seats),
            created_at=cast(datetime, m.created_at),
            updated_at=cast(datetime, m.updated_at),
        )

    def list(self) -> List[Elective]:
        models = self.session.query(ElectiveModel).all()
        return [
            Elective(
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

    def update(self, elective: Elective) -> None:
        m = self.session.query(ElectiveModel).filter_by(id=elective.id).one()
        for attr in ("code", "title", "description", "max_seats", "updated_at"):
            setattr(m, attr, getattr(elective, attr))

    def delete(self, elective_id: UUID) -> None:
        self.session.query(ElectiveModel).filter_by(id=elective_id).delete(
            synchronize_session=False
        )
