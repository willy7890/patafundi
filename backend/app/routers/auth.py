from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import get_current_active_user
from app.schemas.user import (
    UserRegister,
    TechnicianRegister,
    UserOut,
    Token,
    MessageResponse,
)
from app.services.auth_service import (
    authenticate_user,
    register_user,
    register_technician,
    create_tokens,
)
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(data: UserRegister, db: Session = Depends(get_db)):
    """Register a new customer (or other non-technician role)."""
    user = register_user(db, data)
    return user


@router.post(
    "/register/technician",
    response_model=UserOut,
    status_code=status.HTTP_201_CREATED,
)
def register_as_technician(data: TechnicianRegister, db: Session = Depends(get_db)):
    """
    Register as a Technician.
    Certificates are OPTIONAL — a technician can start working immediately
    without any formal certificate.
    """
    user = register_technician(db, data)
    return user


@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    """Login with phone or email + password. Returns JWT access + refresh tokens."""
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect phone/email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return create_tokens(user)


@router.get("/me", response_model=UserOut)
def get_me(current_user: User = Depends(get_current_active_user)):
    """Get current authenticated user profile."""
    return current_user


@router.post("/logout", response_model=MessageResponse)
def logout(current_user: User = Depends(get_current_active_user)):
    """
    Client-side logout (discard tokens).
    Server-side token blacklist can be added later with Redis.
    """
    return MessageResponse(success=True, message="Logged out successfully")
