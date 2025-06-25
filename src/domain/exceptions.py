"""
Domain-level error hierarchy.

Every custom exception derives from AppError so the FastAPI exception
handler can convert it to an HTTP status code.
"""

from uuid import UUID
from typing import List


# ────────────────────────── base classes ──────────────────────────
class AppError(Exception):
    """Base-class for every application-level error."""


class ValidationError(AppError):
    """The client supplied semantically invalid input."""


# ──────────────────────────── auth ────────────────────────────────
class NotAuthenticatedError(AppError):
    """No valid session / JWT supplied."""


class AdminRequiredError(AppError):
    """Caller must be an administrator."""


# ─────────────────────────── users ────────────────────────────────
class UserNotFoundError(AppError):
    """User could not be located."""


# ───────────────────────── electives ──────────────────────────────
class DuplicateElectiveCodeError(ValidationError):
    """An elective with the same code already exists."""


class ElectiveNotFoundError(AppError):
    """Referenced elective could not be found."""


class UnknownCourseIDsError(ValidationError):
    """At least one supplied course UUID does not exist."""

    def __init__(self, missing: List[UUID]) -> None:  # noqa: D401
        super().__init__(f"Unknown course IDs: {', '.join(map(str, missing))}")
        self.missing = missing


# ────────────────────────── courses ───────────────────────────────
class DuplicateCourseNameError(ValidationError):
    """A course with the same name already exists."""


class CourseNotFoundError(AppError):
    """Referenced course could not be found."""


# ────────────────────────── choices ───────────────────────────────
class DuplicateChoiceError(ValidationError):
    """
    The same elective appears more than once in a student’s submitted
    choice list.  Each elective can only be chosen once per user.
    """


class ChoiceNotFoundError(AppError):
    """No choice exists at the requested priority."""
