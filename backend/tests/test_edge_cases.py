"""
Edge-case tests that complement the existing test suite.

Covers:
- Invalid / boundary price values (Pydantic validation)
- Pagination (skip / limit) correctness and rejection
- Health-check endpoint
- Update authorization boundaries (SALESPERSON / unauthenticated)
- Stock boundary purchase scenarios
"""


# ------------------------------------------------------------------ #
# Health check
# ------------------------------------------------------------------ #


def test_health_endpoint(client):
    """GET /api/health should return 200 with status ok."""
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"


# ------------------------------------------------------------------ #
# Price validation
# ------------------------------------------------------------------ #


def test_create_vehicle_price_too_large(client, admin_headers):
    """A price >= 1 000 000 000 should be rejected with 422."""
    response = client.post(
        "/api/vehicles",
        json={
            "make": "Lamborghini",
            "model": "Aventador",
            "category": "Supercar",
            "price": "9999999999.99",
            "quantity": 1,
        },
        headers=admin_headers,
    )
    assert response.status_code == 422


def test_create_vehicle_negative_price(client, admin_headers):
    """A negative price should be rejected with 422."""
    response = client.post(
        "/api/vehicles",
        json={
            "make": "Ghost",
            "model": "Car",
            "category": "Sedan",
            "price": "-100.00",
            "quantity": 1,
        },
        headers=admin_headers,
    )
    assert response.status_code == 422


def test_create_vehicle_zero_price(client, admin_headers):
    """A price of 0 should be rejected with 422."""
    response = client.post(
        "/api/vehicles",
        json={
            "make": "Ghost",
            "model": "Car",
            "category": "Sedan",
            "price": "0",
            "quantity": 1,
        },
        headers=admin_headers,
    )
    assert response.status_code == 422


def test_update_vehicle_price_too_large(client, admin_headers, sample_vehicle):
    """Updating a vehicle price to an overflowing value should return 422."""
    response = client.put(
        f"/api/vehicles/{sample_vehicle['id']}",
        json={"price": "9999999999.99"},
        headers=admin_headers,
    )
    assert response.status_code == 422


# ------------------------------------------------------------------ #
# Pagination
# ------------------------------------------------------------------ #


def _create_vehicles(client, headers, count: int):
    """Helper: bulk-create `count` dummy vehicles via the API."""
    for i in range(count):
        client.post(
            "/api/vehicles",
            json={
                "make": f"Make{i}",
                "model": f"Model{i}",
                "category": "Sedan",
                "price": "10000.00",
                "quantity": 1,
            },
            headers=headers,
        )


def test_pagination_limit(client, admin_headers):
    """limit=2 should return at most 2 vehicles even when more exist."""
    _create_vehicles(client, admin_headers, 5)
    response = client.get("/api/vehicles?limit=2", headers=admin_headers)
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_pagination_skip(client, admin_headers):
    """skip=3 should skip the first 3 records."""
    _create_vehicles(client, admin_headers, 5)
    all_ids = [v["id"] for v in client.get("/api/vehicles", headers=admin_headers).json()]
    skipped_ids = [v["id"] for v in client.get("/api/vehicles?skip=3", headers=admin_headers).json()]
    assert skipped_ids == all_ids[3:]


def test_pagination_skip_and_limit(client, admin_headers):
    """skip=1 + limit=2 returns precisely the second and third records."""
    _create_vehicles(client, admin_headers, 4)
    all_ids = [v["id"] for v in client.get("/api/vehicles", headers=admin_headers).json()]
    paged_ids = [v["id"] for v in client.get("/api/vehicles?skip=1&limit=2", headers=admin_headers).json()]
    assert paged_ids == all_ids[1:3]


def test_pagination_invalid_limit_zero(client, admin_headers):
    """limit=0 should be rejected with 422 (ge=1 validation)."""
    response = client.get("/api/vehicles?limit=0", headers=admin_headers)
    assert response.status_code == 422


def test_pagination_invalid_skip_negative(client, admin_headers):
    """skip=-1 should be rejected with 422 (ge=0 validation)."""
    response = client.get("/api/vehicles?skip=-1", headers=admin_headers)
    assert response.status_code == 422


# ------------------------------------------------------------------ #
# RBAC - Update authorization boundaries
# ------------------------------------------------------------------ #


def test_update_vehicle_as_salesperson_allowed(
    client, salesperson_headers, admin_headers, sample_vehicle
):
    """A SALESPERSON should be able to update vehicles (200)."""
    response = client.put(
        f"/api/vehicles/{sample_vehicle['id']}",
        json={"price": "25000.00"},
        headers=salesperson_headers,
    )
    assert response.status_code == 200
    assert response.json()["price"] == "25000.00"


def test_update_vehicle_as_customer_forbidden(
    client, customer_headers, admin_headers, sample_vehicle
):
    """A CUSTOMER should NOT be able to update vehicles (403)."""
    response = client.put(
        f"/api/vehicles/{sample_vehicle['id']}",
        json={"price": "25000.00"},
        headers=customer_headers,
    )
    assert response.status_code == 403


def test_update_vehicle_unauthenticated(client, admin_headers, sample_vehicle):
    """Updating without a token should return 401."""
    response = client.put(
        f"/api/vehicles/{sample_vehicle['id']}",
        json={"price": "25000.00"},
    )
    assert response.status_code == 401


# ------------------------------------------------------------------ #
# Purchase stock-boundary edge cases
# ------------------------------------------------------------------ #


def test_purchase_exact_stock(client, admin_headers, sample_vehicle):
    """Purchasing exactly the available quantity should succeed and set quantity to 0."""
    vehicle_id = sample_vehicle["id"]
    qty = sample_vehicle["quantity"]
    response = client.post(
        f"/api/vehicles/{vehicle_id}/purchase",
        json={"quantity": qty},
        headers=admin_headers,
    )
    assert response.status_code == 200
    assert response.json()["quantity"] == 0


def test_purchase_one_over_stock(client, admin_headers, sample_vehicle):
    """Purchasing one more than available stock should return 400."""
    vehicle_id = sample_vehicle["id"]
    qty = sample_vehicle["quantity"] + 1
    response = client.post(
        f"/api/vehicles/{vehicle_id}/purchase",
        json={"quantity": qty},
        headers=admin_headers,
    )
    assert response.status_code == 400
    assert "insufficient" in response.json()["detail"].lower()
