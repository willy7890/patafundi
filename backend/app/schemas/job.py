from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict
from app.models.enums import JobStatus


class JobCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=200)
    description: Optional[str] = None
    category_id: Optional[int] = None
    technician_id: Optional[int] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    region: Optional[str] = None
    district: Optional[str] = None
    ward: Optional[str] = None
    street: Optional[str] = None
    address_notes: Optional[str] = None
    estimated_price: Optional[float] = None
    preferred_date: Optional[datetime] = None
    preferred_time_slot: Optional[str] = None
    contact_phone: Optional[str] = None


class JobStatusUpdate(BaseModel):
    status: JobStatus
    note: Optional[str] = None
    final_price: Optional[float] = None
    scheduled_at: Optional[datetime] = None
    rejection_reason: Optional[str] = None
    cancellation_reason: Optional[str] = None


class JobOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    customer_id: int
    technician_id: Optional[int] = None
    category_id: Optional[int] = None
    title: str
    description: Optional[str] = None
    status: JobStatus
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    region: Optional[str] = None
    district: Optional[str] = None
    ward: Optional[str] = None
    street: Optional[str] = None
    address_notes: Optional[str] = None
    estimated_price: Optional[float] = None
    final_price: Optional[float] = None
    currency: str = "TZS"
    preferred_date: Optional[datetime] = None
    preferred_time_slot: Optional[str] = None
    scheduled_at: Optional[datetime] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    contact_phone: Optional[str] = None
    cancellation_reason: Optional[str] = None
    rejection_reason: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class ReviewCreate(BaseModel):
    rating: int = Field(..., ge=1, le=5)
    comment: Optional[str] = None
    is_public: bool = True


class ReviewOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    job_id: int
    customer_id: int
    technician_id: int
    rating: int
    comment: Optional[str] = None
    is_public: bool
    created_at: datetime


class JobStatusHistoryOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    job_id: int
    from_status: Optional[JobStatus] = None
    to_status: JobStatus
    changed_by_id: Optional[int] = None
    note: Optional[str] = None
    created_at: datetime


class MessageResponse(BaseModel):
    message: str