from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import engine, Base, SessionLocal

# Import ALL models first so relationships resolve
from app.models.user import (
    User,
    TechnicianProfile,
    ServiceCategory,
    TechnicianService,
    Certificate,
)
from app.models.job import Job, JobStatusHistory, Review
from app.models.spare import SpareCategory, SparePart, Order, OrderItem
from app.models.media import Media
from app.models.enums import UserRole

from app.core.security import get_password_hash
from app.routers import auth, users, technicians, categories, admin
# from app.routers import job, spare, upload, ws   # uncomment when ready


def seed_data():
    """Create tables and seed development data."""
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        # ... your existing seed code stays the same ...
        db.commit()
    finally:
        db.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    seed_data()
    yield
    # Shutdown


app = FastAPI(
    title=settings.APP_NAME,
    description="PataFundi — Find the Right Technician, at the Right Time. Tanzanian Technician & Services Marketplace.",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix=settings.API_V1_PREFIX)
app.include_router(users.router, prefix=settings.API_V1_PREFIX)
app.include_router(technicians.router, prefix=settings.API_V1_PREFIX)
app.include_router(categories.router, prefix=settings.API_V1_PREFIX)
app.include_router(admin.router, prefix=settings.API_V1_PREFIX)
# app.include_router(job.router, prefix=settings.API_V1_PREFIX)  # uncomment when ready

@app.get("/")
def root():
    return {
        "success": True,
        "message": "Karibu PataFundi API — Version 1",
        "docs": "/api/docs",
        "payment_mode": settings.PAYMENT_MODE,
        "infrastructure_mode": settings.INFRASTRUCTURE_MODE,
    }


@app.get("/health")
def health():
    return {"status": "ok", "app": settings.APP_NAME}