"""
File upload helpers for images, videos and documents.
"""
import os
import uuid
import mimetypes
from pathlib import Path
from typing import Optional, Tuple
from fastapi import UploadFile, HTTPException, status
from app.core.config import settings
from app.models.enums import MediaType

ALLOWED_IMAGE_TYPES = {
    "image/jpeg", "image/jpg", "image/png", "image/webp", "image/gif",
}
ALLOWED_VIDEO_TYPES = {
    "video/mp4", "video/webm", "video/quicktime", "video/x-msvideo",
}
ALLOWED_DOCUMENT_TYPES = {
    "application/pdf",
    "application/msword",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "image/jpeg", "image/png",
}

MAX_IMAGE_MB = 8
MAX_VIDEO_MB = 50
MAX_DOCUMENT_MB = 15


def _ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def detect_media_type(content_type: Optional[str], filename: str) -> MediaType:
    ct = (content_type or "").lower()
    if ct in ALLOWED_IMAGE_TYPES or filename.lower().endswith(
        (".jpg", ".jpeg", ".png", ".webp", ".gif")
    ):
        return MediaType.IMAGE
    if ct in ALLOWED_VIDEO_TYPES or filename.lower().endswith(
        (".mp4", ".webm", ".mov", ".avi")
    ):
        return MediaType.VIDEO
    if ct in ALLOWED_DOCUMENT_TYPES or filename.lower().endswith(
        (".pdf", ".doc", ".docx")
    ):
        return MediaType.DOCUMENT
    return MediaType.OTHER


def validate_file(
    file: UploadFile,
    allowed_types: Optional[set] = None,
    max_mb: Optional[int] = None,
) -> Tuple[MediaType, str]:
    content_type = file.content_type or mimetypes.guess_type(file.filename or "")[0] or ""
    media_type = detect_media_type(content_type, file.filename or "")

    if allowed_types is not None and content_type not in allowed_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File type '{content_type}' not allowed. Allowed: {sorted(allowed_types)}",
        )
    return media_type, content_type


async def save_upload(
    file: UploadFile,
    subfolder: str = "general",
    allowed_types: Optional[set] = None,
    max_mb: Optional[int] = None,
) -> dict:
    if not file.filename:
        raise HTTPException(status_code=400, detail="No filename provided")

    media_type, content_type = validate_file(file, allowed_types, max_mb)

    content = await file.read()
    size = len(content)
    limit_mb = max_mb
    if limit_mb is None:
        if media_type == MediaType.IMAGE:
            limit_mb = MAX_IMAGE_MB
        elif media_type == MediaType.VIDEO:
            limit_mb = MAX_VIDEO_MB
        else:
            limit_mb = MAX_DOCUMENT_MB
    if size > limit_mb * 1024 * 1024:
        raise HTTPException(
            status_code=400,
            detail=f"File too large. Max {limit_mb} MB for this type.",
        )

    original = file.filename
    ext = Path(original).suffix.lower() or {
        MediaType.IMAGE: ".jpg",
        MediaType.VIDEO: ".mp4",
        MediaType.DOCUMENT: ".pdf",
    }.get(media_type, ".bin")

    unique_name = f"{uuid.uuid4().hex}{ext}"
    relative_dir = Path(subfolder)
    absolute_dir = Path(settings.UPLOAD_DIR) / relative_dir
    _ensure_dir(absolute_dir)

    absolute_path = absolute_dir / unique_name
    with open(absolute_path, "wb") as f:
        f.write(content)

    relative_path = str(relative_dir / unique_name).replace("\\", "/")

    return {
        "filename": unique_name,
        "original_filename": original,
        "file_path": relative_path,
        "mime_type": content_type,
        "file_size": size,
        "media_type": media_type,
    }


def get_absolute_path(relative_path: str) -> Path:
    return Path(settings.UPLOAD_DIR) / relative_path


def delete_file(relative_path: str) -> bool:
    try:
        p = get_absolute_path(relative_path)
        if p.exists() and p.is_file():
            p.unlink()
            return True
    except Exception:
        pass
    return False