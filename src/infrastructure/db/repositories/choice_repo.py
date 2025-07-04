from typing import List, Optional, cast
from uuid import UUID
from datetime import datetime, timezone
from sqlalchemy.orm import Session

from src.domain.repositories import AbstractChoiceRepository
from src.domain.entities.choice import Choice
from src.infrastructure.db.models import ChoiceModel


class SqlAlchemyChoiceRepo(AbstractChoiceRepository):
    def __init__(self, session: Session):
        self.session = session

    def add(self, choice: Choice) -> None:
        model = ChoiceModel(
            id=choice.id,
            user_id=choice.user_id,
            elective_id=choice.elective_id,
            priority=choice.priority,
            created_at=choice.created_at,
            updated_at=choice.updated_at,
        )
        self.session.add(model)

    def update(self, choice: Choice) -> None:
        m = self.session.query(ChoiceModel).filter_by(id=choice.id).one()
        m.priority = choice.priority  # type: ignore
        m.updated_at = datetime.now(timezone.utc)  # type: ignore

    def get(self, choice_id: UUID) -> Optional[Choice]:
        m = self.session.query(ChoiceModel).filter_by(id=choice_id).one_or_none()
        if m is None:
            return None
        return Choice(
            id=cast(UUID, m.id),
            user_id=cast(UUID, m.user_id),
            elective_id=cast(UUID, m.elective_id),
            priority=cast(int, m.priority),
            created_at=cast(datetime, m.created_at),
            updated_at=cast(datetime, m.updated_at),
        )

    def list(self) -> List[Choice]:
        models = self.session.query(ChoiceModel).all()
        return [
            Choice(
                id=cast(UUID, m.id),
                user_id=cast(UUID, m.user_id),
                elective_id=cast(UUID, m.elective_id),
                priority=cast(int, m.priority),
                created_at=cast(datetime, m.created_at),
                updated_at=cast(datetime, m.updated_at),
            )
            for m in models
        ]

    def list_by_user(self, user_id: UUID) -> List[Choice]:
        models = (
            self.session.query(ChoiceModel)
            .filter_by(user_id=user_id)
            .order_by(ChoiceModel.priority)
            .all()
        )
        return [
            Choice(
                id=cast(UUID, m.id),
                user_id=cast(UUID, m.user_id),
                elective_id=cast(UUID, m.elective_id),
                priority=cast(int, m.priority),
                created_at=cast(datetime, m.created_at),
                updated_at=cast(datetime, m.updated_at),
            )
            for m in models
        ]

    def list_by_elective(self, elective_id: UUID) -> List[Choice]:
        models = (
            self.session.query(ChoiceModel).filter_by(elective_id=elective_id).all()
        )
        return [
            Choice(
                id=cast(UUID, m.id),
                user_id=cast(UUID, m.user_id),
                elective_id=cast(UUID, m.elective_id),
                priority=cast(int, m.priority),
                created_at=cast(datetime, m.created_at),
                updated_at=cast(datetime, m.updated_at),
            )
            for m in models
        ]

    def delete(self, choice_id: UUID) -> None:
        self.session.query(ChoiceModel).filter_by(id=choice_id).delete(
            synchronize_session=False
        )
