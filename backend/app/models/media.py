from datetime import datetime
from sqlalchemy import (
    Boolean, Column, DateTime, Enum, Integer, String, Text, ForeignKey,
)
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.enums import MediaType, MediaOwnerType


class Media(Base):
    __tablename__ = "media"

    id = Column(Integer, primary_key=True, index=True)
    uploader_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)

    owner_type = Column(Enum(MediaOwnerType), nullable=False, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=True, index=True)
    spare_part_id = Column(Integer, ForeignKey("spare_parts.id"), nullable=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    media_type = Column(Enum(MediaType), default=MediaType.IMAGE, nullable=False)
    filename = Column(String(255), nullable=False)
    original_filename = Column(String(255), nullable=True)
    file_path = Column(String(500), nullable=False)
    mime_type = Column(String(100), nullable=True)
    file_size = Column(Integer, nullable=True)
    width = Column(Integer, nullable=True)
    height = Column(Integer, nullable=True)
    duration_seconds = Column(Integer, nullable=True)

    caption = Column(Text, nullable=True)
    is_primary = Column(Boolean, default=False)
    sort_order = Column(Integer, default=0)

    created_at = Column(DateTime, default=datetime.utcnow)

    uploader = relationship("User", foreign_keys=[uploader_id])
    job = relationship("Job", back_populates="media")
    spare_part = relationship("SparePart", back_populates="media")