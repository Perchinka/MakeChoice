from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from src.domain.entities import Elective


class AbstractElectiveRepository(ABC):
    """Interface for Elective persistence."""

    @abstractmethod
    def add(self, elective: Elective) -> None: ...
    @abstractmethod
    def get(self, elective_id: UUID) -> Optional[Elective]: ...
    @abstractmethod
    def get_by_code(self, code: str) -> Optional[Elective]: ...
    @abstractmethod
    def list(self) -> List[Elective]: ...
    @abstractmethod
    def update(self, elective: Elective) -> None: ...
    @abstractmethod
    def delete(self, elective_id: UUID) -> None: ...

    @abstractmethod
    def set_courses(self, elective_id: UUID, course_ids: List[UUID]) -> None:
        """
        Replace the (many-to-many) course list for the given elective.
        """
        ...
