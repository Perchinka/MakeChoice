from typing import List, Dict
from uuid import uuid4, UUID
from datetime import datetime, timezone

from src.domain.entities.choice import Choice
from src.domain.exceptions import (
    DuplicateChoiceError,
    ChoiceNotFoundError,
    ElectiveNotFoundError,
)
from src.domain.unit_of_work import AbstractUnitOfWork


class ChoiceService:
    def list_user_choices(self, user_id: UUID, uow: AbstractUnitOfWork) -> List[Choice]:
        """Fetch all choices for a user, ordered by ascending priority."""
        with uow:
            return sorted(uow.choices.list_by_user(user_id), key=lambda c: c.priority)

    def replace_user_choices(
        self, user_id: UUID, elective_ids: List[UUID], uow: AbstractUnitOfWork
    ) -> List[Choice]:
        """
        Delete all this user’s existing choices, then insert exactly `elective_ids`
        in the given order.  First item → priority=1, second → 2, etc.

        Raises:
          - DuplicateChoiceError if the list contains the same elective twice.
          - electiveNotFoundError if any ID isn’t in the electives table.
        """
        with uow:
            if len(elective_ids) != len(set(elective_ids)):
                raise DuplicateChoiceError("No duplicates allowed")

            for elective_id in elective_ids:
                if uow.electives.get(elective_id) is None:
                    raise ElectiveNotFoundError(f"elective '{elective_id}' not found")

            for existing in uow.choices.list_by_user(user_id):
                uow.choices.delete(existing.id)

            now = datetime.now(timezone.utc)
            created: List[Choice] = []
            for idx, elective_id in enumerate(elective_ids, start=1):
                choice = Choice(
                    id=uuid4(),
                    user_id=user_id,
                    elective_id=elective_id,
                    priority=idx,
                    created_at=now,
                    updated_at=now,
                )
                uow.choices.add(choice)
                created.append(choice)

            return created

    def remove_choice(
        self, user_id: UUID, priority: int, uow: AbstractUnitOfWork
    ) -> List[Choice]:
        """
        Delete the choice at `priority`.
        Shifts existing choices with priority > this up by one.
        """
        with uow:
            choices = sorted(
                uow.choices.list_by_user(user_id), key=lambda c: c.priority
            )

            to_del = next((c for c in choices if c.priority == priority), None)
            if to_del is None:
                raise ChoiceNotFoundError(f"No choice at priority {priority}")
            uow.choices.delete(to_del.id)

            now = datetime.now(timezone.utc)
            for choice in choices:
                if choice.priority > priority:
                    choice.priority -= 1
                    choice.updated_at = now
                    uow.choices.update(choice)

            return sorted(uow.choices.list_by_user(user_id), key=lambda c: c.priority)
