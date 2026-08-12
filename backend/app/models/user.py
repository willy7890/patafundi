from datetime import datetime
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum,
    Integer,
    String,
    Text,
    Float,
    ForeignKey,
)
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.enums import UserRole, CertificateStatus, ThemeName, AppearanceMode


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=True)
    phone = Column(String(20), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(150), nullable=False)
    role = Column(Enum(UserRole), default=UserRole.CUSTOMER, nullable=False)
    is_active = Column(Boolean, default=True)
    is_verified_phone = Column(Boolean, default=False)
    is_verified_email = Column(Boolean, default=False)
    is_verified_identity = Column(Boolean, default=False)
    profile_photo = Column(String(500), nullable=True)
    language = Column(String(5), default="sw")
    theme = Column(Enum(ThemeName), default=ThemeName.CLASSIC)
    appearance = Column(Enum(AppearanceMode), default=AppearanceMode.SYSTEM)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    technician_profile = relationship(
        "TechnicianProfile", back_populates="user", uselist=False
    )
        # Relationships
    technician_profile = relationship(
        "TechnicianProfile", back_populates="user", uselist=False
    )
    certificates = relationship(
        "Certificate",
        back_populates="technician",
        foreign_keys="[Certificate.technician_id]",
    )
    jobs_as_customer = relationship(
        "Job",
        foreign_keys="[Job.customer_id]",
        back_populates="customer",
    )
    jobs_as_technician = relationship(
        "Job",
        foreign_keys="[Job.technician_id]",
        back_populates="technician",
    )
    spare_parts = relationship(
        "SparePart",
        back_populates="seller",
        foreign_keys="[SparePart.seller_id]",
    )
    orders_as_buyer = relationship(
        "Order",
        foreign_keys="[Order.buyer_id]",
        back_populates="buyer",
    )
    orders_as_seller = relationship(
        "Order",
        foreign_keys="[Order.seller_id]",
        back_populates="seller",
    )
    def __repr__(self):
        return f"<User {self.full_name} ({self.role})>"


class TechnicianProfile(Base):
    __tablename__ = "technician_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    professional_title = Column(String(100), nullable=True)
    bio = Column(Text, nullable=True)
    years_experience = Column(Integer, default=0)
    service_radius_km = Column(Float, default=10.0)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    region = Column(String(100), nullable=True)
    district = Column(String(100), nullable=True)
    ward = Column(String(100), nullable=True)
    street = Column(String(150), nullable=True)
    is_available = Column(Boolean, default=True)
    average_rating = Column(Float, default=0.0)
    total_reviews = Column(Integer, default=0)
    completed_jobs = Column(Integer, default=0)
    response_rate = Column(Float, default=100.0)
    profile_completion = Column(Integer, default=20)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="technician_profile")
    services = relationship(
        "TechnicianService",
        back_populates="technician_profile",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    def __repr__(self):
        return f"<TechnicianProfile user_id={self.user_id}>"


class ServiceCategory(Base):
    __tablename__ = "service_categories"

    id = Column(Integer, primary_key=True, index=True)
    name_en = Column(String(100), nullable=False)
    name_sw = Column(String(100), nullable=False)
    slug = Column(String(120), unique=True, index=True)
    description_en = Column(Text, nullable=True)
    description_sw = Column(Text, nullable=True)
    icon = Column(String(50), nullable=True)
    is_active = Column(Boolean, default=True)
    sort_order = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    technicians = relationship(
        "TechnicianService", back_populates="category"
    )


class TechnicianService(Base):
    __tablename__ = "technician_services"

    id = Column(Integer, primary_key=True, index=True)
    technician_profile_id = Column(
        Integer, ForeignKey("technician_profiles.id"), nullable=False
    )
    category_id = Column(Integer, ForeignKey("service_categories.id"), nullable=False)
    base_price = Column(Float, nullable=True)
    is_primary = Column(Boolean, default=False)

    technician_profile = relationship(
        "TechnicianProfile", back_populates="services"
    )
    category = relationship("ServiceCategory", back_populates="technicians")


class Certificate(Base):
    __tablename__ = "certificates"

    id = Column(Integer, primary_key=True, index=True)
    technician_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(200), nullable=False)
    issuing_organization = Column(String(200), nullable=True)
    certificate_number = Column(String(100), nullable=True)
    issue_date = Column(DateTime, nullable=True)
    expiry_date = Column(DateTime, nullable=True)
    document_path = Column(String(500), nullable=True)
    status = Column(
        Enum(CertificateStatus), default=CertificateStatus.PENDING_REVIEW
    )
    verified_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    verified_at = Column(DateTime, nullable=True)
    rejection_reason = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    technician = relationship(
        "User",
        foreign_keys=[technician_id],
        back_populates="certificates"
    )

    def __repr__(self):
        return f"<Certificate {self.title} ({self.status})>"