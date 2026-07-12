"""
Database engine and session configuration.

Creates the SQLAlchemy engine from the application settings and
provides a session factory used by the dependency injection layer.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# Import Base and all models so that Alembic and create_all can discover tables.
from app.models.base import Base  # noqa: F401
import app.models.user  # noqa: F401
import app.models.vehicle  # noqa: F401

engine = create_engine(
    settings.database_url,
    echo=settings.debug,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)