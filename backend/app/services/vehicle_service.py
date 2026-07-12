"""
Vehicle service — business logic for vehicle CRUD and inventory operations.

Orchestrates calls to the VehicleRepository and translates domain
objects into response schemas.  Purchase and restock logic lives here
to keep the API layer thin.
"""

from decimal import Decimal

from fastapi import HTTPException, status


from app.models.vehicle import Vehicle
from app.repositories.vehicle_repository import VehicleRepository
from app.schemas.vehicle import InventoryUpdate, VehicleCreate, VehicleResponse, VehicleUpdate


class VehicleService:
    """Service layer for vehicle and inventory operations."""

    def __init__(self, repository: VehicleRepository):
        self.repository = repository

    def create_vehicle(self, vehicle_data: VehicleCreate) -> VehicleResponse:
        """Create a new vehicle record and return its response representation."""
        vehicle = Vehicle(
            make=vehicle_data.make,
            model=vehicle_data.model,
            category=vehicle_data.category,
            image_url=vehicle_data.image_url,
            price=vehicle_data.price,
            quantity=vehicle_data.quantity,
        )
        created_vehicle = self.repository.create(vehicle)
        return self._to_response(created_vehicle)

    def list_vehicles(
        self,
        make: str | None = None,
        model: str | None = None,
        category: str | None = None,
        price_min: Decimal | None = None,
        price_max: Decimal | None = None,
        skip: int = 0,
        limit: int = 1000,
    ) -> list[VehicleResponse]:
        """
        Return all vehicles matching the optional filter criteria.

        Supports partial-match on make/model/category and exact
        bounds on price range.
        """
        vehicles = self.repository.list(
            make=make,
            model=model,
            category=category,
            price_min=price_min,
            price_max=price_max,
            skip=skip,
            limit=limit,
        )
        return [self._to_response(vehicle) for vehicle in vehicles]

    def get_vehicle(self, vehicle_id: int) -> VehicleResponse:
        """
        Retrieve a single vehicle by ID.

        Raises:
            HTTPException 404: If the vehicle does not exist.
        """
        vehicle = self._get_or_404(vehicle_id)
        return self._to_response(vehicle)

    def update_vehicle(self, vehicle_id: int, vehicle_data: VehicleUpdate) -> VehicleResponse:
        """
        Partially update a vehicle's details.

        Only fields present in the request body are updated.

        Raises:
            HTTPException 404: If the vehicle does not exist.
        """
        vehicle = self._get_or_404(vehicle_id)
        update_data = vehicle_data.model_dump(exclude_unset=True)
        updated_vehicle = self.repository.update(vehicle, update_data)
        return self._to_response(updated_vehicle)

    def delete_vehicle(self, vehicle_id: int) -> dict[str, str]:
        """
        Delete a vehicle record permanently.

        Raises:
            HTTPException 404: If the vehicle does not exist.
        """
        vehicle = self._get_or_404(vehicle_id)
        self.repository.delete(vehicle)
        return {"message": "Vehicle deleted successfully"}

    def purchase_vehicle(self, vehicle_id: int, data: InventoryUpdate) -> VehicleResponse:
        """
        Decrease a vehicle's stock by the requested quantity.

        Raises:
            HTTPException 404: If the vehicle does not exist.
            HTTPException 400: If the requested quantity exceeds available stock.
        """
        # Ensure vehicle exists first
        self._get_or_404(vehicle_id)

        updated_vehicle = self.repository.update_quantity_atomic(vehicle_id, -data.quantity)
        if not updated_vehicle:
            # If update failed but vehicle exists, it must be insufficient stock
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Insufficient inventory to fulfill request of {data.quantity}",
            )

        return self._to_response(updated_vehicle)

    def restock_vehicle(self, vehicle_id: int, data: InventoryUpdate) -> VehicleResponse:
        """
        Increase a vehicle's stock by the requested quantity.

        Raises:
            HTTPException 404: If the vehicle does not exist.
        """
        self._get_or_404(vehicle_id)
        updated_vehicle = self.repository.update_quantity_atomic(vehicle_id, data.quantity)
        
        # In case the vehicle was deleted in the split second between check and update
        if not updated_vehicle:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Vehicle not found",
            )
            
        return self._to_response(updated_vehicle)

    # ------------------------------------------------------------------ #
    # Private helpers
    # ------------------------------------------------------------------ #

    def _get_or_404(self, vehicle_id: int) -> Vehicle:
        """Fetch a vehicle by ID or raise a 404 HTTPException."""
        vehicle = self.repository.get_by_id(vehicle_id)
        if vehicle is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Vehicle not found",
            )
        return vehicle

    @staticmethod
    def _to_response(vehicle: Vehicle) -> VehicleResponse:
        """Convert a Vehicle ORM instance to a VehicleResponse schema."""
        return VehicleResponse(
            id=vehicle.id,
            make=vehicle.make,
            model=vehicle.model,
            category=vehicle.category,
            price=vehicle.price,
            quantity=vehicle.quantity,
        )