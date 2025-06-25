from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID
from src.domain.entities.choice import Choice


class AbstractChoiceRepository(ABC):
    """Interface for Choice persistence."""

    @abstractmethod
    def add(self, choice: Choice) -> None:
        """Insert a new Choice."""
        ...

    @abstractmethod
    def update(self, choice: Choice) -> None:
        """Persist changes to an existing Choice."""
        ...

    @abstractmethod
    def get(self, choice_id: UUID) -> Optional[Choice]:
        """Fetch a Choice by its UUID."""
        ...

    @abstractmethod
    def list(self) -> List[Choice]:
        """Return all Choices."""
        ...

    @abstractmethod
    def list_by_user(self, user_id: UUID) -> List[Choice]:
        """Return all Choices for a given user (ordered by priority)."""
        ...

    @abstractmethod
    def list_by_elective(self, elective_id: UUID) -> List[Choice]:
        """Return all Choices for a given elective."""
        ...

    @abstractmethod
    def delete(self, choice_id: UUID) -> None:
        """Remove a Choice by its UUID."""
        ...
