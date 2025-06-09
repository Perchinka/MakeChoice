from typing import List, Dict, Any
from domain.entities.choice import Choice
from domain.unit_of_work import AbstractUnitOfWork
from uuid import uuid4
from datetime import datetime, timezone


class ChoiceService:
    def __init__(self, uow: AbstractUnitOfWork):
        self.uow = uow

    def set_user_selection(
        self, user_id: uuid4, selection: List[Dict[str, Any]]
    ) -> None:
        """
        Overwrites a user's entire selection. `selection` is a list of
        {'course_id': UUID, 'priority': int}.
        """
        # delete existing choices
        existing = self.uow.choices.list_by_user(user_id)
        for choice in existing:
            self.uow.choices.delete(choice.id)

        # add new ones
        for item in selection:
            c = Choice(
                id=uuid4(),
                user_id=user_id,
                course_id=item["course_id"],
                priority=item["priority"],
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc),
            )
            self.uow.choices.add(c)

        self.uow.commit()

    def get_user_selection(self, user_id) -> List[Dict[str, Any]]:
        choices = self.uow.choices.list_by_user(user_id)
        choices.sort(key=lambda c: c.priority)
        return [
            {"priority": c.priority, "course_id": str(c.course_id)} for c in choices
        ]

    def export_all_choices(self) -> List[Choice]:
        return self.uow.choices.list()
