from datetime import datetime
from sqlalchemy import (
    Boolean, Column, DateTime, Enum, Integer, String, Text, Float, ForeignKey,
)
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.enums import OrderStatus


class SpareCategory(Base):
    __tablename__ = "spare_categories"

    id = Column(Integer, primary_key=True, index=True)
    name_en = Column(String(100), nullable=False)
    name_sw = Column(String(100), nullable=False)
    slug = Column(String(120), unique=True, index=True)
    description_en = Column(Text, nullable=True)
    description_sw = Column(Text, nullable=True)
    icon = Column(String(50), nullable=True)
    parent_id = Column(Integer, ForeignKey("spare_categories.id"), nullable=True)
    is_active = Column(Boolean, default=True)
    sort_order = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    parent = relationship("SpareCategory", remote_side=[id], backref="children")
    parts = relationship("SparePart", back_populates="category")


class SparePart(Base):
    __tablename__ = "spare_parts"

    id = Column(Integer, primary_key=True, index=True)
    seller_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    category_id = Column(Integer, ForeignKey("spare_categories.id"), nullable=True)

    title = Column(String(200), nullable=False)
    title_sw = Column(String(200), nullable=True)
    description = Column(Text, nullable=True)
    description_sw = Column(Text, nullable=True)

    brand = Column(String(100), nullable=True)
    model_compatibility = Column(String(255), nullable=True)
    condition = Column(String(50), default="new")
    sku = Column(String(100), nullable=True)

    price = Column(Float, nullable=False)
    currency = Column(String(3), default="TZS")
    stock_quantity = Column(Integer, default=1)
    is_available = Column(Boolean, default=True)

    region = Column(String(100), nullable=True)
    district = Column(String(100), nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    views_count = Column(Integer, default=0)
    sold_count = Column(Integer, default=0)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    seller = relationship("User", back_populates="spare_parts")
    category = relationship("SpareCategory", back_populates="parts")
    media = relationship("Media", back_populates="spare_part", cascade="all, delete-orphan")
    order_items = relationship("OrderItem", back_populates="spare_part")


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    buyer_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    seller_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)

    status = Column(Enum(OrderStatus), default=OrderStatus.PENDING, nullable=False, index=True)
    total_amount = Column(Float, nullable=False)
    currency = Column(String(3), default="TZS")

    delivery_method = Column(String(50), default="pickup")
    delivery_address = Column(Text, nullable=True)
    delivery_phone = Column(String(20), nullable=True)
    delivery_notes = Column(Text, nullable=True)

    payment_reference = Column(String(100), nullable=True)
    paid_at = Column(DateTime, nullable=True)
    cancellation_reason = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    buyer = relationship("User", foreign_keys=[buyer_id], back_populates="orders_as_buyer")
    seller = relationship("User", foreign_keys=[seller_id], back_populates="orders_as_seller")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    spare_part_id = Column(Integer, ForeignKey("spare_parts.id"), nullable=False)
    quantity = Column(Integer, default=1)
    unit_price = Column(Float, nullable=False)
    subtotal = Column(Float, nullable=False)

    order = relationship("Order", back_populates="items")
    spare_part = relationship("SparePart", back_populates="order_items")