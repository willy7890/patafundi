from datetime import timedelta
from typing import Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    create_refresh_token,
)
from app.core.config import settings
from app.models.user import User, TechnicianProfile, TechnicianService
from app.models.enums import UserRole
from app.schemas.user import UserRegister, TechnicianRegister


def authenticate_user(db: Session, phone_or_email: str, password: str) -> Optional[User]:
    user = (
        db.query(User)
        .filter((User.phone == phone_or_email) | (User.email == phone_or_email))
        .first()
    )
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def register_user(db: Session, data: UserRegister) -> User:
    # Check existing
    existing = (
        db.query(User)
        .filter((User.phone == data.phone) | (User.email == data.email if data.email else False))
        .first()
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Phone or email already registered",
        )

    user = User(
        full_name=data.full_name,
        phone=data.phone,
        email=data.email,
        hashed_password=get_password_hash(data.password),
        role=data.role,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def register_technician(db: Session, data: TechnicianRegister) -> User:
    # Check existing
    existing = (
        db.query(User)
        .filter((User.phone == data.phone) | (User.email == data.email if data.email else False))
        .first()
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Phone or email already registered",
        )

    user = User(
        full_name=data.full_name,
        phone=data.phone,
        email=data.email,
        hashed_password=get_password_hash(data.password),
        role=UserRole.TECHNICIAN,
    )
    db.add(user)
    db.flush()

    # Create technician profile (certificates are OPTIONAL - none created here)
    profile = TechnicianProfile(
        user_id=user.id,
        professional_title=data.professional_title,
        years_experience=data.years_experience,
        region=data.region,
        district=data.district,
        profile_completion=30 if data.professional_title else 20,
    )
    db.add(profile)
    db.flush()

    # Attach service categories if provided
    for cat_id in data.service_category_ids:
        ts = TechnicianService(
            technician_profile_id=profile.id,
            category_id=cat_id,
            is_primary=True,
        )
        db.add(ts)

    db.commit()
    db.refresh(user)
    return user


def create_tokens(user: User) -> dict:
    access = create_access_token(subject=user.id)
    refresh = create_refresh_token(subject=user.id)
    return {
        "access_token": access,
        "refresh_token": refresh,
        "token_type": "bearer",
    }
