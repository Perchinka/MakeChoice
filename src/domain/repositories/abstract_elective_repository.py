from abc import ABC, abstractmethod
from typing import Optional, List
from uuid import UUID
from src.domain.entities import Elective


class AbstractElectiveRepository(ABC):
    """Interface for Elective persistence."""

    @abstractmethod
    def add(self, elective: Elective) -> None:
        """Insert a new Elective."""
        ...

    @abstractmethod
    def get(self, elective_id: UUID) -> Optional[Elective]:
        """Fetch a Elective by its UUID."""
        ...

    @abstractmethod
    def get_by_code(self, code: str) -> Optional[Elective]:
        """Fetch a Elective by its unique code."""
        ...

    @abstractmethod
    def list(self) -> List[Elective]:
        """Return all Electives."""
        ...

    @abstractmethod
    def update(self, elective: Elective) -> None:
        """Persist changes to an existing Elective."""
        ...

    @abstractmethod
    def delete(self, elective_id: UUID) -> None:
        """Remove a Elective by its UUID."""
        ...
