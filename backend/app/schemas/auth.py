"""
Pydantic schemas for authentication requests and responses.

These schemas handle input validation and serialization for
the /api/auth endpoints.
"""

from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    """Schema for the user registration request body."""

    name: str = Field(min_length=2, max_length=100, description="User's full name")
    email: EmailStr = Field(description="Valid email address")
    password: str = Field(min_length=8, description="Password (minimum 8 characters)")
    role: Optional[str] = Field(
        default=None,
        description="User role: ADMIN, SALESPERSON, or CUSTOMER (defaults to CUSTOMER)",
    )


class UserLogin(BaseModel):
    """Schema for the user login request body."""

    email: EmailStr = Field(description="Registered email address")
    password: str = Field(description="Account password")


class TokenResponse(BaseModel):
    """Schema containing the JWT access token."""

    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    """Public user profile information (no sensitive data)."""

    id: int
    name: str
    email: str
    role: str


class AuthResponse(UserResponse, TokenResponse):
    """Combined user profile + token response returned after register/login."""

    pass