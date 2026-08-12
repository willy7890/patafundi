from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict
from app.models.enums import MediaType, MediaOwnerType


class MediaOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    uploader_id: int
    owner_type: MediaOwnerType
    job_id: Optional[int] = None
    spare_part_id: Optional[int] = None
    user_id: Optional[int] = None
    media_type: MediaType
    filename: str
    original_filename: Optional[str] = None
    file_path: str
    mime_type: Optional[str] = None
    file_size: Optional[int] = None
    caption: Optional[str] = None
    is_primary: bool = False
    sort_order: int = 0
    created_at: datetime
    url: Optional[str] = None


class MediaUploadResponse(BaseModel):
    media: MediaOut
    message: str = "Uploaded successfully"