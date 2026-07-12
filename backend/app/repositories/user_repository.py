"""
User repository — data access layer for user entities.

Encapsulates all direct database queries for the User model.
"""

from sqlalchemy.orm import Session

from app.models.user import User


class UserRepository:
    """Repository handling CRUD operations for User records."""

    def __init__(self, db: Session):
        self.db = db

    def get_by_email(self, email: str) -> User | None:
        """Look up a user by their email address, or return None."""
        return self.db.query(User).filter(User.email == email).first()

    def create(self, user: User) -> User:
        """Persist a new user and return the refreshed instance."""
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user