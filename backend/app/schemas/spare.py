from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict
from app.models.enums import OrderStatus


class SpareCategoryOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name_en: str
    name_sw: str
    slug: str
    icon: Optional[str] = None
    is_active: bool
    sort_order: int


class SparePartCreate(BaseModel):
    title: str = Field(..., min_length=2, max_length=200)
    title_sw: Optional[str] = None
    description: Optional[str] = None
    description_sw: Optional[str] = None
    category_id: Optional[int] = None
    brand: Optional[str] = None
    model_compatibility: Optional[str] = None
    condition: str = "new"
    sku: Optional[str] = None
    price: float = Field(..., gt=0)
    stock_quantity: int = Field(1, ge=0)
    region: Optional[str] = None
    district: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class SparePartUpdate(BaseModel):
    title: Optional[str] = None
    title_sw: Optional[str] = None
    description: Optional[str] = None
    description_sw: Optional[str] = None
    category_id: Optional[int] = None
    brand: Optional[str] = None
    model_compatibility: Optional[str] = None
    condition: Optional[str] = None
    sku: Optional[str] = None
    price: Optional[float] = None
    stock_quantity: Optional[int] = None
    is_available: Optional[bool] = None
    region: Optional[str] = None
    district: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class SparePartOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    seller_id: int
    category_id: Optional[int] = None
    title: str
    title_sw: Optional[str] = None
    description: Optional[str] = None
    description_sw: Optional[str] = None
    brand: Optional[str] = None
    model_compatibility: Optional[str] = None
    condition: str
    sku: Optional[str] = None
    price: float
    currency: str = "TZS"
    stock_quantity: int
    is_available: bool
    region: Optional[str] = None
    district: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    views_count: int
    sold_count: int
    created_at: datetime
    updated_at: datetime


class OrderItemCreate(BaseModel):
    spare_part_id: int
    quantity: int = Field(1, ge=1)


class OrderCreate(BaseModel):
    seller_id: int
    items: List[OrderItemCreate] = Field(..., min_length=1)
    delivery_method: str = "pickup"
    delivery_address: Optional[str] = None
    delivery_phone: Optional[str] = None
    delivery_notes: Optional[str] = None


class OrderStatusUpdate(BaseModel):
    status: OrderStatus
    cancellation_reason: Optional[str] = None
    payment_reference: Optional[str] = None


class OrderItemOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    spare_part_id: int
    quantity: int
    unit_price: float
    subtotal: float


class OrderOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    buyer_id: int
    seller_id: int
    status: OrderStatus
    total_amount: float
    currency: str
    delivery_method: str
    delivery_address: Optional[str] = None
    delivery_phone: Optional[str] = None
    delivery_notes: Optional[str] = None
    payment_reference: Optional[str] = None
    paid_at: Optional[datetime] = None
    cancellation_reason: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    items: List[OrderItemOut] = []