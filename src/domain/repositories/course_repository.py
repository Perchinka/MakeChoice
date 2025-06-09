from abc import ABC, abstractmethod
from typing import Optional, List
from uuid import UUID
from src.domain.entities.course import Course


class CourseRepository(ABC):
    """Interface for Course persistence."""

    @abstractmethod
    def add(self, course: Course) -> None:
        """Insert a new Course."""
        ...

    @abstractmethod
    def get(self, course_id: UUID) -> Optional[Course]:
        """Fetch a Course by its UUID."""
        ...

    @abstractmethod
    def get_by_code(self, code: str) -> Optional[Course]:
        """Fetch a Course by its unique code."""
        ...

    @abstractmethod
    def list(self) -> List[Course]:
        """Return all Courses."""
        ...

    @abstractmethod
    def update(self, course: Course) -> None:
        """Persist changes to an existing Course."""
        ...

    @abstractmethod
    def delete(self, course_id: UUID) -> None:
        """Remove a Course by its UUID."""
        ...
