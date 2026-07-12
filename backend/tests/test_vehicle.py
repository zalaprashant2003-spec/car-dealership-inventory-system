"""
Tests for the vehicle CRUD API (/api/vehicles).

Covers:
- Create, list, search (by make, model, category, price range), update, delete
- Authorization enforcement (Admin-only delete, unauthenticated access)
- Not-found scenarios
"""


# ------------------------------------------------------------------ #
# Create
# ------------------------------------------------------------------ #


def test_create_vehicle_as_admin(client, admin_headers):
    """An ADMIN should be able to create a new vehicle (201)."""
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
    data = response.json()
    assert data["make"] == "Toyota"
    assert data["model"] == "Corolla"
    assert data["quantity"] == 5


def test_create_vehicle_as_salesperson(client, salesperson_headers):
    """A SALESPERSON should be able to create vehicles."""
    response = client.post(
        "/api/vehicles",
        json={
            "make": "Honda",
            "model": "Civic",
            "category": "Sedan",
            "price": "19500.00",
            "quantity": 3,
        },
        headers=salesperson_headers,
    )
    assert response.status_code == 201


def test_create_vehicle_as_customer_forbidden(client, customer_headers):
    """A CUSTOMER should NOT be able to create vehicles (403)."""
    response = client.post(
        "/api/vehicles",
        json={
            "make": "Ford",
            "model": "Focus",
            "category": "Sedan",
            "price": "18000.00",
            "quantity": 2,
        },
        headers=customer_headers,
    )
    assert response.status_code == 403


def test_create_vehicle_unauthenticated(client):
    """Creating a vehicle without a token should return 401."""
    response = client.post(
        "/api/vehicles",
        json={
            "make": "Ford",
            "model": "Focus",
            "category": "Sedan",
            "price": "18000.00",
            "quantity": 2,
        },
    )
    assert response.status_code == 401


# ------------------------------------------------------------------ #
# List
# ------------------------------------------------------------------ #


def test_list_vehicles(client, admin_headers, sample_vehicle):
    """GET /api/vehicles should return all vehicles."""
    response = client.get("/api/vehicles", headers=admin_headers)
    assert response.status_code == 200
    assert len(response.json()) >= 1


def test_list_vehicles_empty(client, admin_headers):
    """GET /api/vehicles with no data returns an empty list."""
    response = client.get("/api/vehicles", headers=admin_headers)
    assert response.status_code == 200
    assert response.json() == []


# ------------------------------------------------------------------ #
# Search
# ------------------------------------------------------------------ #


def test_search_by_make(client, admin_headers, sample_vehicle):
    """Search should return vehicles matching the make parameter."""
    response = client.get("/api/vehicles?make=Toyota", headers=admin_headers)
    assert response.status_code == 200
    results = response.json()
    assert len(results) == 1
    assert results[0]["make"] == "Toyota"


def test_search_by_model(client, admin_headers, sample_vehicle):
    """Search should return vehicles matching the model parameter."""
    response = client.get("/api/vehicles?model=Corolla", headers=admin_headers)
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_search_by_category(client, admin_headers, sample_vehicle):
    """Search should return vehicles matching the category parameter."""
    response = client.get("/api/vehicles?category=Sedan", headers=admin_headers)
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_search_by_price_range(client, admin_headers, sample_vehicle):
    """Search should return vehicles within the given price range."""
    # sample_vehicle has price 21000.00
    response = client.get(
        "/api/vehicles?price_min=20000&price_max=25000",
        headers=admin_headers,
    )
    assert response.status_code == 200
    assert len(response.json()) == 1

    # Out of range
    response = client.get(
        "/api/vehicles?price_min=30000&price_max=40000",
        headers=admin_headers,
    )
    assert response.status_code == 200
    assert len(response.json()) == 0


def test_search_no_results(client, admin_headers, sample_vehicle):
    """Search with a non-matching make should return an empty list."""
    response = client.get("/api/vehicles?make=Ferrari", headers=admin_headers)
    assert response.status_code == 200
    assert response.json() == []


# ------------------------------------------------------------------ #
# Update
# ------------------------------------------------------------------ #


def test_update_vehicle_price(client, admin_headers, sample_vehicle):
    """Updating a vehicle's price should persist the change."""
    vehicle_id = sample_vehicle["id"]
    response = client.put(
        f"/api/vehicles/{vehicle_id}",
        json={"price": "22000.00"},
        headers=admin_headers,
    )
    assert response.status_code == 200
    assert response.json()["price"] == "22000.00"


def test_update_vehicle_not_found(client, admin_headers):
    """Updating a non-existent vehicle should return 404."""
    response = client.put(
        "/api/vehicles/9999",
        json={"price": "22000.00"},
        headers=admin_headers,
    )
    assert response.status_code == 404


# ------------------------------------------------------------------ #
# Delete
# ------------------------------------------------------------------ #


def test_delete_vehicle_as_admin(client, admin_headers, sample_vehicle):
    """An ADMIN should be able to delete a vehicle."""
    vehicle_id = sample_vehicle["id"]
    response = client.delete(f"/api/vehicles/{vehicle_id}", headers=admin_headers)
    assert response.status_code == 200

    # Verify it's gone
    get_response = client.get("/api/vehicles", headers=admin_headers)
    assert len(get_response.json()) == 0


def test_delete_vehicle_as_salesperson_forbidden(client, admin_headers, salesperson_headers, sample_vehicle):
    """A SALESPERSON should NOT be able to delete vehicles (403)."""
    vehicle_id = sample_vehicle["id"]
    response = client.delete(f"/api/vehicles/{vehicle_id}", headers=salesperson_headers)
    assert response.status_code == 403


def test_delete_vehicle_not_found(client, admin_headers):
    """Deleting a non-existent vehicle should return 404."""
    response = client.delete("/api/vehicles/9999", headers=admin_headers)
    assert response.status_code == 404