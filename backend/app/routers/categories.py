from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import ServiceCategory
from app.schemas.user import ServiceCategoryOut

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
