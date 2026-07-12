"""
Pydantic schemas for vehicle requests and responses.

These schemas handle input validation and serialization for
the /api/vehicles endpoints.
"""

from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field


class VehicleCreate(BaseModel):
    """Schema for creating a new vehicle."""

    make: str = Field(min_length=1, max_length=50, description="Vehicle manufacturer")
    model: str = Field(min_length=1, max_length=100, description="Vehicle model name")
    category: str = Field(min_length=1, max_length=50, description="Vehicle category (e.g. Sedan, SUV)")
    image_url: Optional[str] = Field(default=None, max_length=300, description="Optional image URL for the vehicle")
    price: Decimal = Field(gt=0, lt=1000000000, max_digits=12, decimal_places=2, description="Vehicle price (must be positive)")
    quantity: int = Field(default=0, ge=0, description="Initial stock quantity")


class VehicleUpdate(BaseModel):
    """Schema for partially updating a vehicle's details."""

    make: Optional[str] = Field(default=None, min_length=1, max_length=50)
    model: Optional[str] = Field(default=None, min_length=1, max_length=100)
    category: Optional[str] = Field(default=None, min_length=1, max_length=50)
    image_url: Optional[str] = Field(default=None, max_length=300)
    price: Optional[Decimal] = Field(default=None, gt=0, lt=1000000000, max_digits=12, decimal_places=2)
    quantity: Optional[int] = Field(default=None, ge=0)


class InventoryUpdate(BaseModel):
    """Schema for purchase/restock operations (quantity to add or remove)."""

    quantity: int = Field(gt=0, description="Number of units to purchase or restock")


class VehicleResponse(BaseModel):
    """Schema for vehicle data returned to the client."""

    id: int
    make: str
    model: str
    category: str
    price: Decimal
    quantity: int