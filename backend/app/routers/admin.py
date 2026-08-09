from typing import List
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import require_roles
from app.models.user import User, Certificate
from app.models.enums import UserRole, CertificateStatus
from app.schemas.user import CertificateAdminOut, MessageResponse, UserOut
from app.core.config import settings

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/stats")
def platform_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.ADMIN, UserRole.SUPER_ADMIN)),
):
    total_users = db.query(User).count()
    total_technicians = (
        db.query(User).filter(User.role == UserRole.TECHNICIAN).count()
    )
    total_customers = db.query(User).filter(User.role == UserRole.CUSTOMER).count()
    pending_certs = (
        db.query(Certificate)
        .filter(Certificate.status == CertificateStatus.PENDING_REVIEW)
        .count()
    )

    # 1,000 user milestone notification (admin only)
    milestone_alert = None
    if total_users >= 1000 and settings.INFRASTRUCTURE_MODE == "FREE":
        milestone_alert = (
            "PataFundi has reached 1,000+ registered users. "
            "Review infrastructure usage and decide whether an upgrade is necessary. "
            "No automatic upgrade or charging will occur."
        )

    return {
        "success": True,
        "data": {
            "total_users": total_users,
            "total_technicians": total_technicians,
            "total_customers": total_customers,
            "pending_certificates": pending_certs,
            "infrastructure_mode": settings.INFRASTRUCTURE_MODE,
            "payment_mode": settings.PAYMENT_MODE,
            "milestone_alert": milestone_alert,
        },
    }


@router.get("/certificates/pending", response_model=List[CertificateAdminOut])
def list_pending_certificates(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.ADMIN, UserRole.SUPER_ADMIN)),
):
    certs = (
        db.query(Certificate)
        .filter(Certificate.status == CertificateStatus.PENDING_REVIEW)
        .all()
    )
    return certs


@router.post("/certificates/{cert_id}/verify", response_model=MessageResponse)
def verify_certificate(
    cert_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.ADMIN, UserRole.SUPER_ADMIN)),
):
    cert = db.query(Certificate).filter(Certificate.id == cert_id).first()
    if not cert:
        raise HTTPException(status_code=404, detail="Certificate not found")
    cert.status = CertificateStatus.VERIFIED
    cert.verified_by = current_user.id
    cert.verified_at = datetime.utcnow()
    db.commit()
    return MessageResponse(
        success=True, message="Certificate verified successfully. Badge will now appear on profile."
    )


@router.post("/certificates/{cert_id}/reject", response_model=MessageResponse)
def reject_certificate(
    cert_id: int,
    reason: str = "Does not meet verification standards",
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.ADMIN, UserRole.SUPER_ADMIN)),
):
    cert = db.query(Certificate).filter(Certificate.id == cert_id).first()
    if not cert:
        raise HTTPException(status_code=404, detail="Certificate not found")
    cert.status = CertificateStatus.REJECTED
    cert.rejection_reason = reason
    cert.verified_by = current_user.id
    cert.verified_at = datetime.utcnow()
    db.commit()
    return MessageResponse(success=True, message="Certificate rejected.")
