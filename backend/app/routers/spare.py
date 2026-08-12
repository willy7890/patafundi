from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field

from app.core.database import get_db
from app.core.security import get_current_user, get_current_admin
from app.models.user import User
from app.models.spare import SpareCategory, SparePart, Order, OrderItem
from app.models.enums import UserRole

router = APIRouter(prefix="/spares", tags=["Spare Parts"])


# ==================== SCHEMAS ====================

class SpareCategoryCreate(BaseModel):
    name_en: str
    name_sw: str
    slug: str
    icon: Optional[str] = None
    sort_order: int = 0


class SpareCategoryOut(BaseModel):
    id: int
    name_en: str
    name_sw: str
    slug: str
    icon: Optional[str]
    sort_order: int
    is_active: bool

    class Config:
        from_attributes = True


class SparePartCreate(BaseModel):
    category_id: int
    name_en: str
    name_sw: str
    description_en: Optional[str] = None
    description_sw: Optional[str] = None
    price: float = Field(..., gt=0)
    stock_quantity: int = Field(0, ge=0)
    image_url: Optional[str] = None
    brand: Optional[str] = None
    sku: Optional[str] = None
    is_available: bool = True


class SparePartUpdate(BaseModel):
    name_en: Optional[str] = None
    name_sw: Optional[str] = None
    description_en: Optional[str] = None
    description_sw: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)
    stock_quantity: Optional[int] = Field(None, ge=0)
    image_url: Optional[str] = None
    brand: Optional[str] = None
    is_available: Optional[bool] = None


class SparePartOut(BaseModel):
    id: int
    category_id: int
    name_en: str
    name_sw: str
    description_en: Optional[str]
    description_sw: Optional[str]
    price: float
    stock_quantity: int
    image_url: Optional[str]
    brand: Optional[str]
    sku: Optional[str]
    is_available: bool

    class Config:
        from_attributes = True


class OrderItemCreate(BaseModel):
    spare_part_id: int
    quantity: int = Field(..., gt=0)


class OrderCreate(BaseModel):
    items: List[OrderItemCreate]
    delivery_address: str
    phone: str
    notes: Optional[str] = None


# ==================== CATEGORIES ====================

@router.get("/categories", response_model=dict, summary="List spare categories")
def list_categories(db: Session = Depends(get_db)):
    cats = db.query(SpareCategory).filter(SpareCategory.is_active == True).order_by(SpareCategory.sort_order).all()
    return {
        "success": True,
        "data": [SpareCategoryOut.model_validate(c) for c in cats],
    }


@router.post("/categories", summary="Create spare category (Admin)")
def create_category(
    payload: SpareCategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin),
):
    if db.query(SpareCategory).filter(SpareCategory.slug == payload.slug).first():
        raise HTTPException(status_code=400, detail="Slug already exists")

    cat = SpareCategory(**payload.model_dump(), is_active=True)
    db.add(cat)
    db.commit()
    db.refresh(cat)
    return {"success": True, "data": SpareCategoryOut.model_validate(cat)}


# ==================== SPARE PARTS ====================

@router.get("/", summary="List / search spare parts")
def list_spares(
    category_id: Optional[int] = None,
    search: Optional[str] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    query = db.query(SparePart).filter(SparePart.is_available == True)

    if category_id:
        query = query.filter(SparePart.category_id == category_id)
    if search:
        like = f"%{search}%"
        query = query.filter(
            (SparePart.name_en.ilike(like)) |
            (SparePart.name_sw.ilike(like)) |
            (SparePart.brand.ilike(like))
        )

    total = query.count()
    items = query.offset(skip).limit(limit).all()

    return {
        "success": True,
        "total": total,
        "data": [SparePartOut.model_validate(i) for i in items],
    }


@router.get("/{spare_id}", summary="Get single spare part")
def get_spare(spare_id: int, db: Session = Depends(get_db)):
    spare = db.query(SparePart).filter(SparePart.id == spare_id).first()
    if not spare:
        raise HTTPException(status_code=404, detail="Spare part haipatikani")
    return {"success": True, "data": SparePartOut.model_validate(spare)}


@router.post("/", summary="Create spare part (Admin / Technician)")
def create_spare(
    payload: SparePartCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role not in [UserRole.SUPER_ADMIN, UserRole.ADMIN, UserRole.TECHNICIAN]:
        raise HTTPException(status_code=403, detail="Huna ruhusa")

    category = db.query(SpareCategory).filter(SpareCategory.id == payload.category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category haipatikani")

    spare = SparePart(**payload.model_dump())
    db.add(spare)
    db.commit()
    db.refresh(spare)
    return {"success": True, "data": SparePartOut.model_validate(spare)}


@router.patch("/{spare_id}", summary="Update spare part")
def update_spare(
    spare_id: int,
    payload: SparePartUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role not in [UserRole.SUPER_ADMIN, UserRole.ADMIN, UserRole.TECHNICIAN]:
        raise HTTPException(status_code=403, detail="Huna ruhusa")

    spare = db.query(SparePart).filter(SparePart.id == spare_id).first()
    if not spare:
        raise HTTPException(status_code=404, detail="Spare part haipatikani")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(spare, field, value)

    db.commit()
    db.refresh(spare)
    return {"success": True, "data": SparePartOut.model_validate(spare)}


@router.delete("/{spare_id}", summary="Delete spare part (Admin)")
def delete_spare(
    spare_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin),
):
    spare = db.query(SparePart).filter(SparePart.id == spare_id).first()
    if not spare:
        raise HTTPException(status_code=404, detail="Spare part haipatikani")

    db.delete(spare)
    db.commit()
    return {"success": True, "message": "Spare part imefutwa"}


# ==================== ORDERS ====================

@router.post("/orders", summary="Place order for spare parts")
def create_order(
    payload: OrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not payload.items:
        raise HTTPException(status_code=400, detail="Order lazima iwe na angalau item 1")

    total_amount = 0.0
    order_items = []

    for item in payload.items:
        spare = db.query(SparePart).filter(SparePart.id == item.spare_part_id).first()
        if not spare or not spare.is_available:
            raise HTTPException(status_code=400, detail=f"Spare part {item.spare_part_id} haipatikani")
        if spare.stock_quantity < item.quantity:
            raise HTTPException(
                status_code=400,
                detail=f"Stock haitoshi kwa {spare.name_en}. Available: {spare.stock_quantity}",
            )

        line_total = spare.price * item.quantity
        total_amount += line_total
        order_items.append({
            "spare": spare,
            "quantity": item.quantity,
            "unit_price": spare.price,
            "line_total": line_total,
        })

    order = Order(
        user_id=current_user.id,
        total_amount=total_amount,
        delivery_address=payload.delivery_address,
        phone=payload.phone,
        notes=payload.notes,
        status="pending",
    )
    db.add(order)
    db.flush()

    for oi in order_items:
        db.add(OrderItem(
            order_id=order.id,
            spare_part_id=oi["spare"].id,
            quantity=oi["quantity"],
            unit_price=oi["unit_price"],
            line_total=oi["line_total"],
        ))
        # Reduce stock
        oi["spare"].stock_quantity -= oi["quantity"]

    db.commit()
    db.refresh(order)

    return {
        "success": True,
        "message": "Order imewekwa vizuri",
        "data": {
            "order_id": order.id,
            "total_amount": order.total_amount,
            "status": order.status,
        },
    }


@router.get("/orders/my", summary="My spare orders")
def my_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    orders = db.query(Order).filter(Order.user_id == current_user.id).order_by(Order.created_at.desc()).all()
    return {
        "success": True,
        "data": [
            {
                "id": o.id,
                "total_amount": o.total_amount,
                "status": o.status,
                "delivery_address": o.delivery_address,
                "created_at": o.created_at,
            }
            for o in orders
        ],
    }