class AppError(Exception):
    """Base-class for every application-level exception."""


# --- Auth ---
class NotAuthenticatedError(AppError):
    """No valid session / JWT supplied."""


class AdminRequiredError(AppError):
    """Caller must be an administrator."""


# --- Users ---
class UserNotFoundError(AppError):
    """User could not be located."""


# --- Electives ---
class DuplicateElectiveCodeError(AppError):
    """A Elective with the same code already exists."""


class ElectiveNotFoundError(AppError):
    """Referenced Elective could not be found."""


# --- Choices ---
class DuplicateChoiceError(AppError):
    """User already has that Elective selected."""


class ChoiceNotFoundError(AppError):
    """No choice exists at the requested priority."""
