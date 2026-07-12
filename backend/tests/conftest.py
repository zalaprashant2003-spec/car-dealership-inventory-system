"""
Shared test fixtures for the Car Dealership Inventory System test suite.

Provides a fresh in-memory SQLite database for every test, a FastAPI
TestClient, and convenience helpers for obtaining auth tokens and
creating sample vehicles.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.database import Base
from app.dependencies import get_db
from app.main import app


@pytest.fixture
def client():
    """
    Yield a TestClient backed by a fresh in-memory SQLite database.

    The database is created before each test and torn down afterwards,
    ensuring full isolation between test functions.
    """
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(
        bind=engine,
        autoflush=False,
        autocommit=False,
    )
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


# ------------------------------------------------------------------ #
# Auth helper fixtures
# ------------------------------------------------------------------ #

def _register_user(client: TestClient, name: str, email: str, password: str, role: str) -> dict:
    """Register a user and return the full response JSON (includes access_token)."""
    response = client.post(
        "/api/auth/register",
        json={"name": name, "email": email, "password": password, "role": role},
    )
    assert response.status_code == 201, f"Registration failed: {response.json()}"
    return response.json()


@pytest.fixture
def admin_token(client) -> str:
    """Register an ADMIN user and return a valid Bearer token."""
    data = _register_user(client, "Admin User", "admin@example.com", "adminpassword123", "ADMIN")
    return data["access_token"]


@pytest.fixture
def admin_headers(admin_token) -> dict:
    """Return Authorization headers for the ADMIN user."""
    return {"Authorization": f"Bearer {admin_token}"}


@pytest.fixture
def customer_token(client) -> str:
    """Register a CUSTOMER user and return a valid Bearer token."""
    data = _register_user(client, "Customer User", "customer@example.com", "customerpassword123", "CUSTOMER")
    return data["access_token"]


@pytest.fixture
def customer_headers(customer_token) -> dict:
    """Return Authorization headers for the CUSTOMER user."""
    return {"Authorization": f"Bearer {customer_token}"}


@pytest.fixture
def salesperson_token(client) -> str:
    """Register a SALESPERSON user and return a valid Bearer token."""
    data = _register_user(client, "Sales User", "sales@example.com", "salespassword123", "SALESPERSON")
    return data["access_token"]


@pytest.fixture
def salesperson_headers(salesperson_token) -> dict:
    """Return Authorization headers for the SALESPERSON user."""
    return {"Authorization": f"Bearer {salesperson_token}"}


@pytest.fixture
def sample_vehicle(client, admin_headers) -> dict:
    """
    Create a sample Toyota Corolla and return its response data.

    Requires the admin_headers fixture (creates an ADMIN user first).
    """
    response = client.post(
        "/api/vehicles",
        json={
            "make": "Toyota",
            "model": "Corolla",
            "category": "Sedan",
            "price": "21000.00",
            "quantity": 5,
        },
        headers=admin_headers,
    )
    assert response.status_code == 201
    return response.json()