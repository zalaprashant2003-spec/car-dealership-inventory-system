"""
Vehicle API routes — CRUD operations for the vehicle catalog.

All endpoints require authentication.  Create and update require
ADMIN or SALESPERSON role.  Delete requires ADMIN role.
"""

from decimal import Decimal
from typing import Annotated

from fastapi import APIRouter, Depends, Query, status

from app.core.security import get_current_user, require_roles
from app.dependencies import get_vehicle_service
from app.models.user import User, UserRole
from app.schemas.vehicle import VehicleCreate, VehicleResponse, VehicleUpdate
from app.services.vehicle_service import VehicleService

router = APIRouter()


@router.post(
    "",
    response_model=VehicleResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Add a new vehicle",
)
def create_vehicle(
    vehicle_data: VehicleCreate,
    service: Annotated[VehicleService, Depends(get_vehicle_service)],
    current_user: Annotated[User, Depends(require_roles(UserRole.ADMIN, UserRole.SALESPERSON))],
):
    """Create a new vehicle in the inventory. Requires ADMIN or SALESPERSON role."""
    return service.create_vehicle(vehicle_data)


@router.get(
    "",
    response_model=list[VehicleResponse],
    summary="List all vehicles",
)
def list_vehicles(
    service: Annotated[VehicleService, Depends(get_vehicle_service)],
    current_user: Annotated[User, Depends(get_current_user)],
    make: str | None = Query(default=None, description="Filter by make (partial match)"),
    model: str | None = Query(default=None, description="Filter by model (partial match)"),
    category: str | None = Query(default=None, description="Filter by category (partial match)"),
    price_min: Decimal | None = Query(default=None, gt=0, description="Minimum price filter"),
    price_max: Decimal | None = Query(default=None, gt=0, description="Maximum price filter"),
    skip: int = Query(default=0, ge=0, description="Number of records to skip for pagination"),
    limit: int = Query(default=1000, ge=1, le=1000, description="Maximum number of records to return"),
):
    """Retrieve all vehicles, optionally filtered by make, model, category, or price range."""
    return service.list_vehicles(
        make=make, model=model, category=category,
        price_min=price_min, price_max=price_max,
        skip=skip, limit=limit,
    )


@router.put(
    "/{vehicle_id}",
    response_model=VehicleResponse,
    summary="Update a vehicle",
)
def update_vehicle(
    vehicle_id: int,
    vehicle_data: VehicleUpdate,
    service: Annotated[VehicleService, Depends(get_vehicle_service)],
    current_user: Annotated[User, Depends(require_roles(UserRole.ADMIN, UserRole.SALESPERSON))],
):
    """Update a vehicle's details. Requires ADMIN or SALESPERSON role."""
    return service.update_vehicle(vehicle_id, vehicle_data)


@router.delete(
    "/{vehicle_id}",
    summary="Delete a vehicle",
)
def delete_vehicle(
    vehicle_id: int,
    service: Annotated[VehicleService, Depends(get_vehicle_service)],
    current_user: Annotated[User, Depends(require_roles(UserRole.ADMIN))],
):
    """Delete a vehicle from the inventory. Requires ADMIN role."""
    return service.delete_vehicle(vehicle_id)