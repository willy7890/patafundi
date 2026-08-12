from datetime import datetime
from sqlalchemy import (
    Boolean, Column, DateTime, Enum, Integer, String, Text, Float, ForeignKey,
)
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.enums import JobStatus


class Job(Base):
    """Customer booking request for a technician service."""

    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    technician_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    category_id = Column(Integer, ForeignKey("service_categories.id"), nullable=True)

    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(Enum(JobStatus), default=JobStatus.PENDING, nullable=False, index=True)

    # Location of the job
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    region = Column(String(100), nullable=True)
    district = Column(String(100), nullable=True)
    ward = Column(String(100), nullable=True)
    street = Column(String(150), nullable=True)
    address_notes = Column(Text, nullable=True)

    # Pricing
    estimated_price = Column(Float, nullable=True)
    final_price = Column(Float, nullable=True)
    currency = Column(String(3), default="TZS")

    # Scheduling
    preferred_date = Column(DateTime, nullable=True)
    preferred_time_slot = Column(String(50), nullable=True)
    scheduled_at = Column(DateTime, nullable=True)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)

    contact_phone = Column(String(20), nullable=True)
    cancellation_reason = Column(Text, nullable=True)
    rejection_reason = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    customer = relationship("User", foreign_keys=[customer_id], back_populates="jobs_as_customer")
    technician = relationship("User", foreign_keys=[technician_id], back_populates="jobs_as_technician")
    category = relationship("ServiceCategory")
    media = relationship("Media", back_populates="job", cascade="all, delete-orphan")
    status_history = relationship("JobStatusHistory", back_populates="job", cascade="all, delete-orphan")
    review = relationship("Review", back_populates="job", uselist=False)

    def __repr__(self):
        return f"<Job {self.id} {self.title} ({self.status})>"


class JobStatusHistory(Base):
    __tablename__ = "job_status_history"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False, index=True)
    from_status = Column(Enum(JobStatus), nullable=True)
    to_status = Column(Enum(JobStatus), nullable=False)
    changed_by_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    note = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    job = relationship("Job", back_populates="status_history")
    changed_by = relationship("User")


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id"), unique=True, nullable=False)
    customer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    technician_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    rating = Column(Integer, nullable=False)  # 1-5
    comment = Column(Text, nullable=True)
    is_public = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    job = relationship("Job", back_populates="review")
    customer = relationship("User", foreign_keys=[customer_id])
    technician = relationship("User", foreign_keys=[technician_id])
    category = relationship("ServiceCategory")
    media = relationship("Media", back_populates="job", cascade="all, delete-orphan")
    status_history = relationship("JobStatusHistory", back_populates="job", cascade="all, delete-orphan")
    review = relationship("Review", back_populates="job", uselist=False)