"""
Inventory API routes — purchase and restock operations.

Purchase is available to any authenticated user.
Restock is restricted to ADMIN users only, per the specification.
"""

from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.core.security import get_current_user, require_roles
from app.dependencies import get_vehicle_service
from app.models.user import User, UserRole
from app.schemas.vehicle import InventoryUpdate, VehicleResponse
from app.services.vehicle_service import VehicleService

router = APIRouter()


@router.post(
    "/{vehicle_id}/purchase",
    response_model=VehicleResponse,
    summary="Purchase a vehicle",
    description="Decrease a vehicle's stock quantity. Available to any authenticated user.",
)
def purchase_vehicle(
    vehicle_id: int,
    data: InventoryUpdate,
    service: Annotated[VehicleService, Depends(get_vehicle_service)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    """Purchase a vehicle — any authenticated user can purchase."""
    return service.purchase_vehicle(vehicle_id, data)


@router.post(
    "/{vehicle_id}/restock",
    response_model=VehicleResponse,
    summary="Restock a vehicle",
    description="Increase a vehicle's stock quantity. Admin only.",
)
def restock_vehicle(
    vehicle_id: int,
    data: InventoryUpdate,
    service: Annotated[VehicleService, Depends(get_vehicle_service)],
    current_user: Annotated[User, Depends(require_roles(UserRole.ADMIN))],
):
    """Restock a vehicle — Admin only."""
    return service.restock_vehicle(vehicle_id, data)