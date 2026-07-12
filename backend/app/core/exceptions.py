"""
Custom exception classes for the Car Dealership Inventory System.

These exceptions represent business-logic errors and are translated
into appropriate HTTP responses by the API layer.  Keeping them
separate from FastAPI's HTTPException follows the Single
Responsibility Principle and makes the service layer testable
independently of the web framework.
"""


class AppException(Exception):
    """Base exception for all application-specific errors."""

    def __init__(self, detail: str = "An unexpected error occurred"):
        self.detail = detail
        super().__init__(self.detail)


class NotFoundError(AppException):
    """Raised when a requested resource does not exist."""

    def __init__(self, resource: str = "Resource", identifier: str | int = ""):
        detail = f"{resource} not found"
        if identifier:
            detail = f"{resource} with id '{identifier}' not found"
        super().__init__(detail)


class ConflictError(AppException):
    """Raised when a creation or update conflicts with existing data."""

    def __init__(self, detail: str = "Resource already exists"):
        super().__init__(detail)


class InsufficientInventoryError(AppException):
    """Raised when a purchase request exceeds available stock."""

    def __init__(self, requested: int = 0, available: int = 0):
        detail = f"Insufficient inventory: requested {requested}, available {available}"
        super().__init__(detail)


class ForbiddenError(AppException):
    """Raised when the user lacks permission for the requested action."""

    def __init__(self, detail: str = "Not authorized to perform this action"):
        super().__init__(detail)


class InvalidCredentialsError(AppException):
    """Raised when login credentials are invalid."""

    def __init__(self, detail: str = "Invalid email or password"):
        super().__init__(detail)
