from fastapi import status
from src.domain.exceptions import (
    ChoiceNotFoundError,
    CourseNotFoundError,
    DuplicateChoiceError,
    DuplicateCourseCodeError,
    UserNotFoundError,
    AdminRequiredError,
)


code_map = {
    DuplicateCourseCodeError: status.HTTP_400_BAD_REQUEST,
    UserNotFoundError: status.HTTP_404_NOT_FOUND,
    AdminRequiredError: status.HTTP_403_FORBIDDEN,
    CourseNotFoundError: status.HTTP_404_NOT_FOUND,
    ChoiceNotFoundError: status.HTTP_404_NOT_FOUND,
    DuplicateChoiceError: status.HTTP_400_BAD_REQUEST,
}
