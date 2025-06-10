from typing import List, Dict, Any
from src.domain.entities.choice import Choice
from src.domain.unit_of_work import AbstractUnitOfWork
from uuid import uuid4, UUID
from datetime import datetime, timezone


class ChoiceService:
    def set_user_selection(
        self, user_id: UUID, selection: List[Dict[str, Any]], uow: AbstractUnitOfWork
    ) -> None:
        with uow:
            existing = uow.choices.list_by_user(user_id)
            for choice in existing:
                uow.choices.delete(choice.id)

            for item in selection:
                choice = Choice(
                    id=uuid4(),
                    user_id=user_id,
                    course_id=item["course_id"],
                    priority=item["priority"],
                    created_at=datetime.now(timezone.utc),
                    updated_at=datetime.now(timezone.utc),
                )
                uow.choices.add(choice)

    def get_user_selection(
        self, user_id, uow: AbstractUnitOfWork
    ) -> List[Dict[str, Any]]:
        with uow:
            choices = uow.choices.list_by_user(user_id)
            choices.sort(key=lambda c: c.priority)
            return [
                {"priority": c.priority, "course_id": str(c.course_id)} for c in choices
            ]

    def export_all_choices(self, uow: AbstractUnitOfWork) -> List[Choice]:
        with uow:
            return uow.choices.list()
