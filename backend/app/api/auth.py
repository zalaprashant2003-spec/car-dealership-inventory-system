"""
Authentication API routes — register and login.

These endpoints are public (no authentication required).
"""

from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.schemas.auth import AuthResponse, UserCreate, UserLogin
from app.services.auth_service import AuthService

router = APIRouter()


@router.post(
    "/register",
    response_model=AuthResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
)
def register_user(user_data: UserCreate, db: Annotated[Session, Depends(get_db)]):
    """Create a new user account and return a JWT access token."""
    service = AuthService(db)
    return service.register(user_data)


@router.post(
    "/login",
    response_model=AuthResponse,
    summary="Log in an existing user",
)
def login_user(credentials: UserLogin, db: Annotated[Session, Depends(get_db)]):
    """Authenticate with email and password, returning a JWT access token."""
    service = AuthService(db)
    return service.login(credentials)