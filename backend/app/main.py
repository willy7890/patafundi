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
from app.routers import auth, users, technicians, categories, admin, job, spare, upload


def seed_data():
    """Create tables and seed development data."""
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        # Seed service categories
        if db.query(ServiceCategory).count() == 0:
            categories = [
                ("Electrician", "Fundi Umeme", "electrician", "zap"),
                ("Plumber", "Fundi Mabomba", "plumber", "droplet"),
                ("AC Technician", "Fundi AC", "ac-technician", "wind"),
                ("Refrigerator Technician", "Fundi Friji", "refrigerator", "snowflake"),
                ("Phone Repair", "Fundi Simu", "phone-repair", "smartphone"),
                ("Computer Technician", "Fundi Kompyuta", "computer", "monitor"),
                ("Car Mechanic", "Fundi Gari", "car-mechanic", "car"),
                ("Motorcycle Mechanic", "Fundi Pikipiki", "motorcycle", "bike"),
                ("Welder", "Fundi Uungaji", "welder", "flame"),
                ("Painter", "Fundi Rangi", "painter", "paintbrush"),
                ("Carpenter", "Fundi Seremala", "carpenter", "hammer"),
                ("Mason", "Fundi Ujenzi", "mason", "brick"),
                ("Solar Technician", "Fundi Solar", "solar", "sun"),
                ("CCTV Technician", "Fundi CCTV", "cctv", "camera"),
                ("Generator Technician", "Fundi Generator", "generator", "battery"),
                ("Locksmith", "Fundi Funguo", "locksmith", "key"),
                ("Tiler", "Fundi Tile", "tiler", "grid"),
                ("Roofer", "Fundi Paa", "roofer", "home"),
                ("Cleaner", "Msafi", "cleaner", "sparkles"),
                ("Gardener", "Fundi Bustani", "gardener", "leaf"),
            ]
            for i, (en, sw, slug, icon) in enumerate(categories):
                cat = ServiceCategory(
                    name_en=en,
                    name_sw=sw,
                    slug=slug,
                    icon=icon,
                    sort_order=i,
                    is_active=True,
                )
                db.add(cat)

        # Seed super admin
        if not db.query(User).filter(User.email == "admin@patafundi.co.tz").first():
            admin = User(
                full_name="PataFundi Admin",
                email="admin@patafundi.co.tz",
                phone="+255750394671",
                hashed_password=get_password_hash("Admin@123"),
                role=UserRole.SUPER_ADMIN,
                is_verified_phone=True,
                is_verified_email=True,
                language="sw",
            )
            db.add(admin)

        # Seed sample customer
        if not db.query(User).filter(User.email == "customer@example.com").first():
            customer = User(
                full_name="Amina Juma",
                email="customer@example.com",
                phone="+255712345678",
                hashed_password=get_password_hash("Customer1!"),
                role=UserRole.CUSTOMER,
                is_verified_phone=True,
                language="sw",
            )
            db.add(customer)

        # Seed sample technician
        if not db.query(User).filter(User.email == "fundi@example.com").first():
            tech_user = User(
                full_name="John Mwakalinga",
                email="fundi@example.com",
                phone="+255750394671",
                hashed_password=get_password_hash("Fundi123!"),
                role=UserRole.TECHNICIAN,
                is_verified_phone=True,
                language="sw",
            )
            db.add(tech_user)
            db.flush()
            profile = TechnicianProfile(
                user_id=tech_user.id,
                professional_title="Electrician",
                bio="Fundi umeme mwenye uzoefu wa miaka 8. Ninashughulika na wiring, sockets, na matatizo ya umeme ya nyumbani.",
                years_experience=8,
                region="Dar es Salaam",
                district="Kinondoni",
                ward="Msasani",
                latitude=-6.7655,
                longitude=39.2689,
                service_radius_km=15.0,
                is_available=True,
                average_rating=4.8,
                total_reviews=42,
                completed_jobs=127,
                profile_completion=85,
            )
            db.add(profile)

        db.commit()
    finally:
        db.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    seed_data()
    yield


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

# Routers
# Routers
app.include_router(auth.router, prefix=settings.API_V1_PREFIX)
app.include_router(users.router, prefix=settings.API_V1_PREFIX)
app.include_router(technicians.router, prefix=settings.API_V1_PREFIX)
app.include_router(categories.router, prefix=settings.API_V1_PREFIX)
app.include_router(admin.router, prefix=settings.API_V1_PREFIX)

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