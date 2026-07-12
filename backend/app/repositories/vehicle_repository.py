"""
Vehicle repository — data access layer for vehicle entities.

Encapsulates all direct database queries for the Vehicle model,
keeping the service layer free of SQLAlchemy specifics.
"""

from decimal import Decimal
from typing import Any

from sqlalchemy.orm import Session

from app.models.vehicle import Vehicle


class VehicleRepository:
    """Repository handling CRUD operations for Vehicle records."""

    def __init__(self, db: Session):
        self.db = db

    def create(self, vehicle: Vehicle) -> Vehicle:
        """Persist a new vehicle and return the refreshed instance."""
        self.db.add(vehicle)
        self.db.commit()
        self.db.refresh(vehicle)
        return vehicle

    def get_by_id(self, vehicle_id: int) -> Vehicle | None:
        """Retrieve a single vehicle by its primary key, or None."""
        return self.db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()

    def list(
        self,
        make: str | None = None,
        model: str | None = None,
        category: str | None = None,
        price_min: Decimal | None = None,
        price_max: Decimal | None = None,
        skip: int = 0,
        limit: int = 1000,
    ) -> list[Vehicle]:
        """
        Return vehicles matching the given optional filters.

        Supports partial-match (case-insensitive) filtering on make, model,
        and category, plus exact price-range bounds.
        """
        query = self.db.query(Vehicle)

        if make:
            query = query.filter(Vehicle.make.ilike(f"%{make}%"))
        if model:
            query = query.filter(Vehicle.model.ilike(f"%{model}%"))
        if category:
            query = query.filter(Vehicle.category.ilike(f"%{category}%"))
        if price_min is not None:
            query = query.filter(Vehicle.price >= price_min)
        if price_max is not None:
            query = query.filter(Vehicle.price <= price_max)

        return query.order_by(Vehicle.id).offset(skip).limit(limit).all()

    def update(self, vehicle: Vehicle, data: dict[str, Any]) -> Vehicle:
        """Apply a dictionary of field updates to a vehicle and commit."""
        for field, value in data.items():
            if value is not None:
                setattr(vehicle, field, value)
        self.db.commit()
        self.db.refresh(vehicle)
        return vehicle

    def update_quantity_atomic(self, vehicle_id: int, delta: int) -> Vehicle | None:
        """
        Atomically update the quantity of a vehicle to prevent race conditions.
        Ensures the resulting quantity does not drop below 0.
        Returns the updated vehicle, or None if the vehicle doesn't exist or stock is insufficient.
        """
        result = self.db.query(Vehicle).filter(
            Vehicle.id == vehicle_id,
            Vehicle.quantity + delta >= 0
        ).update(
            {"quantity": Vehicle.quantity + delta},
            synchronize_session="evaluate"
        )
        if result == 0:
            return None
        self.db.commit()
        return self.get_by_id(vehicle_id)

    def delete(self, vehicle: Vehicle) -> None:
        """Permanently remove a vehicle record from the database."""
        self.db.delete(vehicle)
        self.db.commit()