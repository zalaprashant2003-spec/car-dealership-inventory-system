"""
Tests for the authentication API (POST /api/auth/register and /login).

Covers:
- Successful registration and login
- Duplicate email rejection
- Missing/invalid fields
- Wrong password
- Non-existent email login
- CORS preflight
"""


# ------------------------------------------------------------------ #
# Registration tests
# ------------------------------------------------------------------ #


def test_register_success(client):
    """A new user should receive a 201 response with an access token."""
    response = client.post(
        "/api/auth/register",
        json={
            "name": "Alex Johnson",
            "email": "alex@example.com",
            "password": "strongpassword123",
        },
    )
    assert response.status_code == 201

    data = response.json()
    assert data["email"] == "alex@example.com"
    assert data["name"] == "Alex Johnson"
    assert data["role"] == "CUSTOMER"  # default role
    assert data["access_token"]
    assert data["token_type"] == "bearer"


def test_register_with_admin_role(client):
    """Users should be able to register with a specific role."""
    response = client.post(
        "/api/auth/register",
        json={
            "name": "Admin User",
            "email": "admin@example.com",
            "password": "adminpassword123",
            "role": "ADMIN",
        },
    )
    assert response.status_code == 201
    assert response.json()["role"] == "ADMIN"


def test_register_duplicate_email(client):
    """Registering with an already-taken email should return 400."""
    payload = {
        "name": "First User",
        "email": "duplicate@example.com",
        "password": "password12345",
    }
    client.post("/api/auth/register", json=payload)

    response = client.post("/api/auth/register", json=payload)
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"].lower()


def test_register_missing_name(client):
    """Registration without a name should return 422 (validation error)."""
    response = client.post(
        "/api/auth/register",
        json={"email": "noname@example.com", "password": "password123"},
    )
    assert response.status_code == 422


def test_register_short_password(client):
    """Registration with a password shorter than 8 chars should return 422."""
    response = client.post(
        "/api/auth/register",
        json={"name": "Short Pwd", "email": "short@example.com", "password": "abc"},
    )
    assert response.status_code == 422


def test_register_invalid_email(client):
    """Registration with a malformed email should return 422."""
    response = client.post(
        "/api/auth/register",
        json={"name": "Bad Email", "email": "not-an-email", "password": "password123"},
    )
    assert response.status_code == 422


def test_register_invalid_role(client):
    """Registration with a non-existent role should return 400."""
    response = client.post(
        "/api/auth/register",
        json={
            "name": "Bad Role",
            "email": "badrole@example.com",
            "password": "password123",
            "role": "SUPERUSER",
        },
    )
    assert response.status_code == 400
    assert "invalid role" in response.json()["detail"].lower()


def test_register_with_customer_role(client):
    """Users should be able to register with the CUSTOMER role."""
    response = client.post(
        "/api/auth/register",
        json={
            "name": "Customer User",
            "email": "customer@example.com",
            "password": "customerpassword123",
            "role": "CUSTOMER",
        },
    )
    assert response.status_code == 201
    assert response.json()["role"] == "CUSTOMER"


def test_register_with_salesperson_role(client):
    """Users should be able to register with the SALESPERSON role."""
    response = client.post(
        "/api/auth/register",
        json={
            "name": "Sales User",
            "email": "sales@example.com",
            "password": "salespassword123",
            "role": "SALESPERSON",
        },
    )
    assert response.status_code == 201
    assert response.json()["role"] == "SALESPERSON"


# ------------------------------------------------------------------ #
# Login tests
# ------------------------------------------------------------------ #


def test_login_success(client):
    """A registered user should be able to log in and receive a token."""
    client.post(
        "/api/auth/register",
        json={
            "name": "Login Test",
            "email": "login@example.com",
            "password": "password12345",
        },
    )

    response = client.post(
        "/api/auth/login",
        json={"email": "login@example.com", "password": "password12345"},
    )
    assert response.status_code == 200

    data = response.json()
    assert data["access_token"]
    assert data["token_type"] == "bearer"
    assert data["email"] == "login@example.com"


def test_login_wrong_password(client):
    """Login with an incorrect password should return 401."""
    client.post(
        "/api/auth/register",
        json={
            "name": "Wrong Pwd",
            "email": "wrongpwd@example.com",
            "password": "correctpassword",
        },
    )

    response = client.post(
        "/api/auth/login",
        json={"email": "wrongpwd@example.com", "password": "incorrectpassword"},
    )
    assert response.status_code == 401
    assert "invalid credentials" in response.json()["detail"].lower()


def test_login_nonexistent_email(client):
    """Login with an email that was never registered should return 401."""
    response = client.post(
        "/api/auth/login",
        json={"email": "ghost@example.com", "password": "password123"},
    )
    assert response.status_code == 401


# ------------------------------------------------------------------ #
# CORS test
# ------------------------------------------------------------------ #


def test_cors_preflight_allows_frontend_origin(client):
    """CORS preflight from the Vite dev server origin should be allowed."""
    response = client.options(
        "/api/auth/register",
        headers={
            "Origin": "http://localhost:5173",
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "content-type",
        },
    )
    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "http://localhost:5173"