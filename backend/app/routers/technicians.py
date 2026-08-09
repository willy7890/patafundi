from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from app.core.database import get_db
from app.core.dependencies import get_current_active_user, require_roles
from app.models.user import User, TechnicianProfile, Certificate
from app.models.enums import UserRole, CertificateStatus
from app.schemas.user import (
    TechnicianProfileOut,
    TechnicianProfileUpdate,
    CertificateCreate,
    CertificateOut,
    MessageResponse,
)

router = APIRouter(prefix="/technicians", tags=["Technicians"])


@router.get("/", response_model=List[TechnicianProfileOut])
def list_technicians(
    skip: int = 0,
    limit: int = 20,
    region: Optional[str] = None,
    available_only: bool = False,
    db: Session = Depends(get_db),
):
    """
    Public list of technicians.
    Ranking is NOT based on certificates alone.
    Certificates are optional and only add a trust indicator.
    """
    query = (
        db.query(TechnicianProfile)
        .options(joinedload(TechnicianProfile.user))
        .join(User)
        .filter(User.is_active == True)
    )
    if region:
        query = query.filter(TechnicianProfile.region.ilike(f"%{region}%"))
    if available_only:
        query = query.filter(TechnicianProfile.is_available == True)

    # Simple ranking: rating + completed jobs (certificates do NOT dominate)
    profiles = (
        query.order_by(
            TechnicianProfile.average_rating.desc(),
            TechnicianProfile.completed_jobs.desc(),
        )
        .offset(skip)
        .limit(limit)
        .all()
    )
    return profiles


@router.get("/{technician_id}", response_model=TechnicianProfileOut)
def get_technician(technician_id: int, db: Session = Depends(get_db)):
    profile = (
        db.query(TechnicianProfile)
        .options(joinedload(TechnicianProfile.user))
        .filter(TechnicianProfile.id == technician_id)
        .first()
    )
    if not profile:
        raise HTTPException(status_code=404, detail="Technician not found")
    return profile


@router.get("/me/profile", response_model=TechnicianProfileOut)
def get_my_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.TECHNICIAN)),
):
    profile = (
        db.query(TechnicianProfile)
        .options(joinedload(TechnicianProfile.user))
        .filter(TechnicianProfile.user_id == current_user.id)
        .first()
    )
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile


@router.patch("/me/profile", response_model=TechnicianProfileOut)
def update_my_profile(
    data: TechnicianProfileUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.TECHNICIAN)),
):
    profile = (
        db.query(TechnicianProfile)
        .filter(TechnicianProfile.user_id == current_user.id)
        .first()
    )
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(profile, field, value)

    # Recalculate simple profile completion
    completion = 20
    if profile.professional_title:
        completion += 15
    if profile.bio:
        completion += 15
    if profile.years_experience > 0:
        completion += 10
    if profile.region:
        completion += 10
    if profile.latitude and profile.longitude:
        completion += 15
    if profile.is_available is not None:
        completion += 5
    profile.profile_completion = min(completion, 100)

    db.commit()
    db.refresh(profile)
    return profile


# ---------- Optional Certificates ----------
@router.post("/me/certificates", response_model=CertificateOut, status_code=201)
def upload_certificate(
    data: CertificateCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.TECHNICIAN)),
):
    """
    Upload an optional certificate.
    Status starts as PENDING_REVIEW.
    The document itself is never shown publicly — only a "Verified" badge after admin approval.
    """
    cert = Certificate(
        technician_id=current_user.id,
        title=data.title,
        issuing_organization=data.issuing_organization,
        certificate_number=data.certificate_number,
        issue_date=data.issue_date,
        expiry_date=data.expiry_date,
        status=CertificateStatus.PENDING_REVIEW,
    )
    db.add(cert)
    db.commit()
    db.refresh(cert)
    return cert


@router.get("/me/certificates", response_model=List[CertificateOut])
def list_my_certificates(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.TECHNICIAN)),
):
    certs = (
        db.query(Certificate)
        .filter(Certificate.technician_id == current_user.id)
        .all()
    )
    return certs


@router.get("/{technician_id}/certificates", response_model=List[CertificateOut])
def list_public_certificates(technician_id: int, db: Session = Depends(get_db)):
    """
    Public view of certificates.
    Only VERIFIED certificates are returned, and no document_path is exposed.
    """
    certs = (
        db.query(Certificate)
        .filter(
            Certificate.technician_id == technician_id,
            Certificate.status == CertificateStatus.VERIFIED,
        )
        .all()
    )
    return certs
