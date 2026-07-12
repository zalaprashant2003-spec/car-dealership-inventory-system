"""
Database session dependency for FastAPI route injection.
"""

from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.repositories.vehicle_repository import VehicleRepository
from app.services.vehicle_service import VehicleService


def get_db():
    """
    Yield a SQLAlchemy session and ensure it is closed after the request.

    Used as a FastAPI ``Depends()`` dependency in route handlers.
    """
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


def get_vehicle_service(db: Session = Depends(get_db)) -> VehicleService:
    """Dependency to inject the VehicleService with its required Repository."""
    repository = VehicleRepository(db)
    return VehicleService(repository)