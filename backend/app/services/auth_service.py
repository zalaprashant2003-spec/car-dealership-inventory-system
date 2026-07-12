"""
Authentication service for user registration and login.

Handles password hashing with bcrypt, user creation via the
repository layer, and JWT token generation on successful
authentication.
"""

import bcrypt
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.security import create_access_token
from app.models.user import User, UserRole
from app.repositories.user_repository import UserRepository
from app.schemas.auth import AuthResponse, UserCreate, UserLogin


class AuthService:
    """Service layer for authentication operations."""

    def __init__(self, db: Session):
        self.db = db
        self.repository = UserRepository(db)

    def register(self, user_data: UserCreate) -> AuthResponse:
        """
        Register a new user.

        Validates that the email is not already taken, hashes the
        password with bcrypt, persists the user, and returns an
        AuthResponse containing the JWT access token.

        Raises:
            HTTPException 400: If email is already registered or role is invalid.
        """
        if self.repository.get_by_email(user_data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )

        role = UserRole.CUSTOMER
        if user_data.role:
            try:
                role = UserRole(user_data.role.upper())
            except ValueError as exc:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid role",
                ) from exc

        user = User(
            name=user_data.name,
            email=user_data.email,
            password_hash=self._hash_password(user_data.password),
            role=role,
        )
        try:
            user = self.repository.create(user)
        except IntegrityError:
            # Handle race condition where user is created between get_by_email and create
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )
            
        token = create_access_token({"sub": user.email})

        return AuthResponse(
            id=user.id,
            name=user.name,
            email=user.email,
            role=user.role.value,
            access_token=token,
        )

    def login(self, credentials: UserLogin) -> AuthResponse:
        """
        Authenticate an existing user.

        Verifies email exists and password matches the stored bcrypt
        hash.  Returns an AuthResponse with a fresh JWT on success.

        Raises:
            HTTPException 401: If credentials are invalid.
        """
        user = self.repository.get_by_email(credentials.email)
        if not user or not self._verify_password(credentials.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
            )

        token = create_access_token({"sub": user.email})
        return AuthResponse(
            id=user.id,
            name=user.name,
            email=user.email,
            role=user.role.value,
            access_token=token,
        )

    @staticmethod
    def _hash_password(password: str) -> str:
        """Hash a plaintext password using bcrypt."""
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")

    @staticmethod
    def _verify_password(plain_password: str, hashed_password: str) -> bool:
        """
        Verify a plaintext password against a hashed password.

        Supports bcrypt hashes, falling back to legacy SHA256 hashes for
        backward compatibility with existing user databases.
        """
        import hashlib

        # Bcrypt hashes typically start with $2a$, $2b$, or $2y$
        if hashed_password.startswith("$2a$") or hashed_password.startswith("$2b$") or hashed_password.startswith("$2y$"):
            try:
                return bcrypt.checkpw(
                    plain_password.encode("utf-8"),
                    hashed_password.encode("utf-8"),
                )
            except ValueError:
                pass

        # Fallback to legacy SHA256 hash comparison
        legacy_hash = hashlib.sha256(plain_password.encode("utf-8")).hexdigest()
        return legacy_hash == hashed_password