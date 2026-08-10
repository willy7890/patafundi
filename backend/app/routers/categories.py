from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import require_roles
from app.models.user import ServiceCategory, User
from app.models.enums import UserRole
from app.schemas.user import ServiceCategoryOut, ServiceCategoryCreate

router = APIRouter(prefix="/categories", tags=["Service Categories"])


@router.get("/", response_model=List[ServiceCategoryOut])
def list_categories(db: Session = Depends(get_db)):
    """Public list of active service categories (Electrician, Plumber, etc.)."""
    cats = (
        db.query(ServiceCategory)
        .filter(ServiceCategory.is_active == True)
        .order_by(ServiceCategory.sort_order)
        .all()
    )
    return cats


@router.post("/", response_model=ServiceCategoryOut)
def create_category(
    data: ServiceCategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.ADMIN, UserRole.SUPER_ADMIN)),
):
    if data.slug:
        existing = db.query(ServiceCategory).filter(ServiceCategory.slug == data.slug).first()
        if existing:
            raise HTTPException(status_code=400, detail="Category slug already exists")

    slug = data.slug or data.name_en.lower().replace(" ", "-")
    category = ServiceCategory(
        name_en=data.name_en,
        name_sw=data.name_sw,
        slug=slug,
        icon=data.icon,
        description_en=data.description_en,
        description_sw=data.description_sw,
        is_active=data.is_active,
    )
    db.add(category)
    db.commit()
    db.refresh(category)
    return category
