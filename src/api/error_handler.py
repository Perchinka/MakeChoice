from fastapi import status
from src.domain.exceptions import (
    DuplicateCourseCodeError,
    UserNotFoundError,
    AdminRequiredError,
)


code_map = {
    DuplicateCourseCodeError: status.HTTP_400_BAD_REQUEST,
    UserNotFoundError: status.HTTP_404_NOT_FOUND,
    AdminRequiredError: status.HTTP_403_FORBIDDEN,
}
