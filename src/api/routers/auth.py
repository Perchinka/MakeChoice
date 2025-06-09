import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

router = APIRouter()

# This is only for the OpenAPI “Authorize” button
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/admin/auth/login")


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


@router.post(
    "/signup", response_model=TokenResponse, status_code=status.HTTP_201_CREATED
)
def signup():
    """
    Issue a random token for a "new" admin.
    """
    token = str(uuid.uuid4())
    return {"access_token": token, "token_type": "bearer"}


@router.post("/login", response_model=TokenResponse)
def login():
    """
    Issue a random token for an existing admin.
    """
    token = str(uuid.uuid4())
    return {"access_token": token, "token_type": "bearer"}


def get_current_admin(token: str = Depends(oauth2_scheme)) -> bool:
    """
    Mock verification: accept any non-empty token as authenticated.
    """
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )
    # You could decode/inspect the token here if you wanted.
    return True
