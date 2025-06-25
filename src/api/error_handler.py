from fastapi import status

from src.domain.exceptions import (
    # generic
    ValidationError,
    AdminRequiredError,
    # users
    UserNotFoundError,
    # electives
    DuplicateElectiveCodeError,
    ElectiveNotFoundError,
    UnknownCourseIDsError,
    # choices
    ChoiceNotFoundError,
    DuplicateChoiceError,
    # courses
    DuplicateCourseNameError,
    CourseNotFoundError,
)

# Maps domain exceptions to HTTP status codes
code_map = {
    # ─── validation ───
    ValidationError: status.HTTP_422_UNPROCESSABLE_ENTITY,
    DuplicateElectiveCodeError: status.HTTP_400_BAD_REQUEST,
    DuplicateCourseNameError: status.HTTP_400_BAD_REQUEST,
    UnknownCourseIDsError: status.HTTP_400_BAD_REQUEST,
    DuplicateChoiceError: status.HTTP_400_BAD_REQUEST,
    # ─── auth / authz ───
    AdminRequiredError: status.HTTP_403_FORBIDDEN,
    # ─── not-found ───
    UserNotFoundError: status.HTTP_404_NOT_FOUND,
    ElectiveNotFoundError: status.HTTP_404_NOT_FOUND,
    ChoiceNotFoundError: status.HTTP_404_NOT_FOUND,
    CourseNotFoundError: status.HTTP_404_NOT_FOUND,
}
