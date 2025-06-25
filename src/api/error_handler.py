from fastapi import status
from src.domain.exceptions import (
    ChoiceNotFoundError,
    ElectiveNotFoundError,
    DuplicateChoiceError,
    DuplicateElectiveCodeError,
    UserNotFoundError,
    AdminRequiredError,
)


code_map = {
    DuplicateElectiveCodeError: status.HTTP_400_BAD_REQUEST,
    UserNotFoundError: status.HTTP_404_NOT_FOUND,
    AdminRequiredError: status.HTTP_403_FORBIDDEN,
    ElectiveNotFoundError: status.HTTP_404_NOT_FOUND,
    ChoiceNotFoundError: status.HTTP_404_NOT_FOUND,
    DuplicateChoiceError: status.HTTP_400_BAD_REQUEST,
}
