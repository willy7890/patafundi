from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from app.models.enums import UserRole, CertificateStatus, ThemeName, AppearanceMode


# ---------- Auth ----------
class UserRegister(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=150)
    phone: str = Field(..., min_length=9, max_length=20)
    email: Optional[EmailStr] = None
    password: str = Field(..., min_length=8, max_length=100)
    role: UserRole = UserRole.CUSTOMER


class TechnicianRegister(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=150)
    phone: str = Field(..., min_length=9, max_length=20)
    email: Optional[EmailStr] = None
    password: str = Field(..., min_length=8, max_length=100)
    professional_title: Optional[str] = None
    years_experience: int = 0
    region: Optional[str] = None
    district: Optional[str] = None
    service_category_ids: List[int] = []


class UserLogin(BaseModel):
    phone_or_email: str
    password: str


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    sub: Optional[str] = None
    type: Optional[str] = None


# ---------- User ----------
class UserBase(BaseModel):
    full_name: str
    phone: str
    email: Optional[EmailStr] = None
    role: UserRole
    language: str = "sw"
    theme: ThemeName = ThemeName.CLASSIC
    appearance: AppearanceMode = AppearanceMode.SYSTEM


class UserOut(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    is_active: bool
    is_verified_phone: bool
    is_verified_email: bool
    is_verified_identity: bool
    profile_photo: Optional[str] = None
    created_at: datetime


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    language: Optional[str] = None
    theme: Optional[ThemeName] = None
    appearance: Optional[AppearanceMode] = None
    profile_photo: Optional[str] = None


# ---------- Technician Profile ----------
class TechnicianProfileBase(BaseModel):
    professional_title: Optional[str] = None
    bio: Optional[str] = None
    years_experience: int = 0
    service_radius_km: float = 10.0
    region: Optional[str] = None
    district: Optional[str] = None
    ward: Optional[str] = None
    street: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    is_available: bool = True


class TechnicianProfileOut(TechnicianProfileBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    average_rating: float
    total_reviews: int
    completed_jobs: int
    response_rate: float
    profile_completion: int
    user: Optional[UserOut] = None


class TechnicianProfileUpdate(BaseModel):
    professional_title: Optional[str] = None
    bio: Optional[str] = None
    years_experience: Optional[int] = None
    service_radius_km: Optional[float] = None
    region: Optional[str] = None
    district: Optional[str] = None
    ward: Optional[str] = None
    street: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    is_available: Optional[bool] = None


# ---------- Certificate (Optional) ----------
class CertificateCreate(BaseModel):
    title: str
    issuing_organization: Optional[str] = None
    certificate_number: Optional[str] = None
    issue_date: Optional[datetime] = None
    expiry_date: Optional[datetime] = None


class CertificateOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    issuing_organization: Optional[str] = None
    status: CertificateStatus
    verified_at: Optional[datetime] = None
    # Note: document_path is NEVER exposed publicly
    created_at: datetime


class CertificateAdminOut(CertificateOut):
    document_path: Optional[str] = None
    rejection_reason: Optional[str] = None
    technician_id: int


# ---------- Service Category ----------
class ServiceCategoryOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name_en: str
    name_sw: str
    slug: str
    icon: Optional[str] = None
    is_active: bool


# ---------- Settings ----------
class UserSettingsUpdate(BaseModel):
    language: Optional[str] = None
    theme: Optional[ThemeName] = None
    appearance: Optional[AppearanceMode] = None


class MessageResponse(BaseModel):
    success: bool = True
    message: str
    data: Optional[dict] = None


class ErrorResponse(BaseModel):
    success: bool = False
    message: str
    error_code: Optional[str] = None
