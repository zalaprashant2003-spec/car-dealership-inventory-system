"""
Tests for the inventory API (purchase and restock operations).

Covers:
- Successful purchase and restock
- Insufficient inventory on purchase
- Role-based access (any user can purchase, only Admin can restock)
- Non-existent vehicle handling
"""


# ------------------------------------------------------------------ #
# Purchase tests
# ------------------------------------------------------------------ #


def test_purchase_vehicle_success(client, admin_headers, sample_vehicle):
    """Purchasing should decrease the vehicle quantity."""
    vehicle_id = sample_vehicle["id"]
    response = client.post(
        f"/api/vehicles/{vehicle_id}/purchase",
        json={"quantity": 2},
        headers=admin_headers,
    )
    assert response.status_code == 200
    assert response.json()["quantity"] == 3  # 5 - 2


def test_purchase_vehicle_as_salesperson(client, admin_headers, salesperson_headers, sample_vehicle):
    """Any authenticated user (including SALESPERSON) should be able to purchase."""
    vehicle_id = sample_vehicle["id"]
    response = client.post(
        f"/api/vehicles/{vehicle_id}/purchase",
        json={"quantity": 1},
        headers=salesperson_headers,
    )
    assert response.status_code == 200
    assert response.json()["quantity"] == 4  # 5 - 1


def test_purchase_insufficient_inventory(client, admin_headers, sample_vehicle):
    """Purchasing more than available stock should return 400."""
    vehicle_id = sample_vehicle["id"]
    response = client.post(
        f"/api/vehicles/{vehicle_id}/purchase",
        json={"quantity": 100},
        headers=admin_headers,
    )
    assert response.status_code == 400
    assert "insufficient" in response.json()["detail"].lower()


def test_purchase_nonexistent_vehicle(client, admin_headers):
    """Purchasing a non-existent vehicle should return 404."""
    response = client.post(
        "/api/vehicles/9999/purchase",
        json={"quantity": 1},
        headers=admin_headers,
    )
    assert response.status_code == 404


def test_purchase_unauthenticated(client, admin_headers, sample_vehicle):
    """Purchasing without authentication should return 401."""
    vehicle_id = sample_vehicle["id"]
    response = client.post(
        f"/api/vehicles/{vehicle_id}/purchase",
        json={"quantity": 1},
    )
    assert response.status_code == 401


def test_purchase_zero_quantity_rejected(client, admin_headers, sample_vehicle):
    """Purchasing quantity of 0 should fail validation (422)."""
    vehicle_id = sample_vehicle["id"]
    response = client.post(
        f"/api/vehicles/{vehicle_id}/purchase",
        json={"quantity": 0},
        headers=admin_headers,
    )
    assert response.status_code == 422


# ------------------------------------------------------------------ #
# Restock tests
# ------------------------------------------------------------------ #


def test_restock_vehicle_as_admin(client, admin_headers, sample_vehicle):
    """An ADMIN should be able to restock a vehicle."""
    vehicle_id = sample_vehicle["id"]
    response = client.post(
        f"/api/vehicles/{vehicle_id}/restock",
        json={"quantity": 3},
        headers=admin_headers,
    )
    assert response.status_code == 200
    assert response.json()["quantity"] == 8  # 5 + 3


def test_restock_vehicle_as_customer_forbidden(client, admin_headers, customer_headers, sample_vehicle):
    """A CUSTOMER should NOT be able to restock (Admin only per spec)."""
    vehicle_id = sample_vehicle["id"]
    response = client.post(
        f"/api/vehicles/{vehicle_id}/restock",
        json={"quantity": 3},
        headers=customer_headers,
    )
    assert response.status_code == 403


def test_restock_vehicle_as_salesperson_forbidden(client, admin_headers, salesperson_headers, sample_vehicle):
    """A SALESPERSON should NOT be able to restock."""
    vehicle_id = sample_vehicle["id"]
    response = client.post(
        f"/api/vehicles/{vehicle_id}/restock",
        json={"quantity": 3},
        headers=salesperson_headers,
    )
    assert response.status_code == 403


def test_restock_nonexistent_vehicle(client, admin_headers):
    """Restocking a non-existent vehicle should return 404."""
    response = client.post(
        "/api/vehicles/9999/restock",
        json={"quantity": 5},
        headers=admin_headers,
    )
    assert response.status_code == 404


# ------------------------------------------------------------------ #
# Combined purchase + restock flow
# ------------------------------------------------------------------ #


def test_purchase_then_restock_flow(client, admin_headers, sample_vehicle):
    """Purchasing then restocking should update quantity correctly."""
    vehicle_id = sample_vehicle["id"]

    # Purchase 2 → quantity goes from 5 to 3
    purchase_response = client.post(
        f"/api/vehicles/{vehicle_id}/purchase",
        json={"quantity": 2},
        headers=admin_headers,
    )
    assert purchase_response.status_code == 200
    assert purchase_response.json()["quantity"] == 3

    # Restock 4 → quantity goes from 3 to 7
    restock_response = client.post(
        f"/api/vehicles/{vehicle_id}/restock",
        json={"quantity": 4},
        headers=admin_headers,
    )
    assert restock_response.status_code == 200
    assert restock_response.json()["quantity"] == 7