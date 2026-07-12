"""
FastAPI application entry point for the Car Dealership Inventory System.

Configures CORS, registers API routers, and exposes a health-check
endpoint at the root path.
"""

import logging
import sys

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import auth, inventory, vehicles
from app.core.config import settings

# ── Structured logging ──────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.DEBUG if settings.debug else logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    stream=sys.stdout,
)
logger = logging.getLogger(__name__)

# ── Application ─────────────────────────────────────────────────────────────
app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description="A production-style car dealership inventory management API.",
)

# Allow the Vite dev server and common local origins.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Route registration ───────────────────────────────────────────────────────
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(vehicles.router, prefix="/api/vehicles", tags=["vehicles"])
app.include_router(inventory.router, prefix="/api/vehicles", tags=["inventory"])


@app.get("/", tags=["health"])
def root():
    """Root health-check — confirms the API is running."""
    return {"message": "Car Dealership Inventory System API is running"}


@app.get("/api/health", tags=["health"])
def health_check():
    """Detailed health-check endpoint suitable for load-balancer probes."""
    return {"status": "ok", "app": settings.app_name}