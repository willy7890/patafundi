import os
import uuid
from pathlib import Path
from typing import List, Optional

from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, status, Form, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.media import Media
from app.models.enums import MediaType, MediaOwnerType, UserRole

router = APIRouter(prefix="/upload", tags=["Upload"])

# ==================== CONFIG ====================
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

ALLOWED_IMAGE_TYPES = {
    "image/jpeg", "image/jpg", "image/png", "image/webp", "image/gif"
}
ALLOWED_VIDEO_TYPES = {
    "video/mp4", "video/quicktime", "video/webm", "video/x-msvideo", "video/mpeg"
}

MAX_IMAGE_SIZE = 10 * 1024 * 1024    # 10 MB
MAX_VIDEO_SIZE = 100 * 1024 * 1024   # 100 MB


def _save_file(file: UploadFile, subfolder: str) -> tuple[str, str, int]:
    """
    Save file to disk.
    Returns: (filename, relative_file_path, file_size)
    """
    original_name = file.filename or "unknown"
    ext = Path(original_name).suffix.lower() or ".bin"
    filename = f"{uuid.uuid4().hex}{ext}"

    folder = UPLOAD_DIR / subfolder
    folder.mkdir(parents=True, exist_ok=True)

    file_path = folder / filename
    content = file.file.read()
    file_size = len(content)

    with open(file_path, "wb") as f:
        f.write(content)

    # Relative path that will be stored in DB (and used by frontend)
    relative_path = f"uploads/{subfolder}/{filename}"
    return filename, relative_path, file_size


# ==================== IMAGE UPLOAD ====================

@router.post("/image", summary="Upload image")
async def upload_image(
    file: UploadFile = File(...),
    owner_type: MediaOwnerType = Form(...),          # required
    job_id: Optional[int] = Form(None),
    spare_part_id: Optional[int] = Form(None),
    user_id: Optional[int] = Form(None),             # e.g. profile picture
    caption: Optional[str] = Form(None),
    is_primary: bool = Form(False),
    sort_order: int = Form(0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Validate mime
    if file.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Aina ya file haikubaliki. Tumia JPEG, PNG, WebP au GIF.",
        )

    # Read + size check
    content = await file.read()
    if len(content) > MAX_IMAGE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Image ni kubwa mno. Max 10MB.",
        )
    await file.seek(0)

    # Decide subfolder
    subfolder = f"images/{owner_type.value.lower()}"

    filename, file_path, file_size = _save_file(file, subfolder)

    media = Media(
        uploader_id=current_user.id,
        owner_type=owner_type,
        job_id=job_id,
        spare_part_id=spare_part_id,
        user_id=user_id,
        media_type=MediaType.IMAGE,
        filename=filename,
        original_filename=file.filename,
        file_path=file_path,
        mime_type=file.content_type,
        file_size=file_size,
        caption=caption,
        is_primary=is_primary,
        sort_order=sort_order,
    )
    db.add(media)
    db.commit()
    db.refresh(media)

    return {
        "success": True,
        "message": "Image imepakiwa vizuri",
        "data": {
            "id": media.id,
            "file_path": media.file_path,
            "filename": media.filename,
            "original_filename": media.original_filename,
            "media_type": media.media_type.value,
            "owner_type": media.owner_type.value,
            "mime_type": media.mime_type,
            "file_size": media.file_size,
            "is_primary": media.is_primary,
            "created_at": media.created_at,
        },
    }


# ==================== VIDEO UPLOAD ====================

@router.post("/video", summary="Upload video")
async def upload_video(
    file: UploadFile = File(...),
    owner_type: MediaOwnerType = Form(...),
    job_id: Optional[int] = Form(None),
    spare_part_id: Optional[int] = Form(None),
    user_id: Optional[int] = Form(None),
    caption: Optional[str] = Form(None),
    is_primary: bool = Form(False),
    sort_order: int = Form(0),
    duration_seconds: Optional[int] = Form(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if file.content_type not in ALLOWED_VIDEO_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Aina ya video haikubaliki. Tumia MP4, MOV, WebM au AVI.",
        )

    content = await file.read()
    if len(content) > MAX_VIDEO_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Video ni kubwa mno. Max 100MB.",
        )
    await file.seek(0)

    subfolder = f"videos/{owner_type.value.lower()}"
    filename, file_path, file_size = _save_file(file, subfolder)

    media = Media(
        uploader_id=current_user.id,
        owner_type=owner_type,
        job_id=job_id,
        spare_part_id=spare_part_id,
        user_id=user_id,
        media_type=MediaType.VIDEO,
        filename=filename,
        original_filename=file.filename,
        file_path=file_path,
        mime_type=file.content_type,
        file_size=file_size,
        duration_seconds=duration_seconds,
        caption=caption,
        is_primary=is_primary,
        sort_order=sort_order,
    )
    db.add(media)
    db.commit()
    db.refresh(media)

    return {
        "success": True,
        "message": "Video imepakiwa vizuri",
        "data": {
            "id": media.id,
            "file_path": media.file_path,
            "filename": media.filename,
            "original_filename": media.original_filename,
            "media_type": media.media_type.value,
            "owner_type": media.owner_type.value,
            "mime_type": media.mime_type,
            "file_size": media.file_size,
            "duration_seconds": media.duration_seconds,
            "is_primary": media.is_primary,
            "created_at": media.created_at,
        },
    }


# ==================== MULTIPLE IMAGES ====================

@router.post("/images", summary="Upload multiple images at once")
async def upload_multiple_images(
    files: List[UploadFile] = File(...),
    owner_type: MediaOwnerType = Form(...),
    job_id: Optional[int] = Form(None),
    spare_part_id: Optional[int] = Form(None),
    user_id: Optional[int] = Form(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if len(files) > 12:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unaweza kupakia images 12 tu kwa wakati mmoja.",
        )

    results = []
    subfolder = f"images/{owner_type.value.lower()}"

    for idx, file in enumerate(files):
        if file.content_type not in ALLOWED_IMAGE_TYPES:
            continue

        content = await file.read()
        if len(content) > MAX_IMAGE_SIZE:
            continue

        await file.seek(0)
        filename, file_path, file_size = _save_file(file, subfolder)

        media = Media(
            uploader_id=current_user.id,
            owner_type=owner_type,
            job_id=job_id,
            spare_part_id=spare_part_id,
            user_id=user_id,
            media_type=MediaType.IMAGE,
            filename=filename,
            original_filename=file.filename,
            file_path=file_path,
            mime_type=file.content_type,
            file_size=file_size,
            is_primary=(idx == 0),
            sort_order=idx,
        )
        db.add(media)
        db.flush()

        results.append({
            "id": media.id,
            "file_path": media.file_path,
            "filename": media.filename,
            "original_filename": media.original_filename,
            "is_primary": media.is_primary,
        })

    db.commit()

    return {
        "success": True,
        "message": f"{len(results)} image(s) zimepakiwa",
        "data": results,
    }


# ==================== GET MEDIA ====================

@router.get("/my", summary="Get media I uploaded")
def get_my_media(
    media_type: Optional[MediaType] = None,
    owner_type: Optional[MediaOwnerType] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = db.query(Media).filter(Media.uploader_id == current_user.id)

    if media_type:
        query = query.filter(Media.media_type == media_type)
    if owner_type:
        query = query.filter(Media.owner_type == owner_type)

    items = query.order_by(Media.created_at.desc()).all()

    return {
        "success": True,
        "data": [
            {
                "id": m.id,
                "file_path": m.file_path,
                "filename": m.filename,
                "original_filename": m.original_filename,
                "media_type": m.media_type.value,
                "owner_type": m.owner_type.value,
                "mime_type": m.mime_type,
                "file_size": m.file_size,
                "is_primary": m.is_primary,
                "caption": m.caption,
                "created_at": m.created_at,
            }
            for m in items
        ],
    }


@router.get("/by-owner", summary="Get media by owner (job / spare / user)")
def get_media_by_owner(
    owner_type: MediaOwnerType = Query(...),
    job_id: Optional[int] = None,
    spare_part_id: Optional[int] = None,
    user_id: Optional[int] = None,
    db: Session = Depends(get_db),
):
    query = db.query(Media).filter(Media.owner_type == owner_type)

    if owner_type == MediaOwnerType.JOB and job_id:
        query = query.filter(Media.job_id == job_id)
    elif owner_type == MediaOwnerType.SPARE_PART and spare_part_id:
        query = query.filter(Media.spare_part_id == spare_part_id)
    elif owner_type == MediaOwnerType.USER and user_id:
        query = query.filter(Media.user_id == user_id)
    else:
        raise HTTPException(
            status_code=400,
            detail="Tuma job_id / spare_part_id / user_id kulingana na owner_type",
        )

    items = query.order_by(Media.sort_order, Media.created_at).all()

    return {
        "success": True,
        "data": [
            {
                "id": m.id,
                "file_path": m.file_path,
                "media_type": m.media_type.value,
                "is_primary": m.is_primary,
                "caption": m.caption,
                "sort_order": m.sort_order,
            }
            for m in items
        ],
    }


# ==================== DELETE ====================

@router.delete("/{media_id}", summary="Delete media")
def delete_media(
    media_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    media = db.query(Media).filter(Media.id == media_id).first()
    if not media:
        raise HTTPException(status_code=404, detail="Media haipatikani")

    # Only uploader or admin can delete
    if media.uploader_id != current_user.id and current_user.role not in [
        UserRole.SUPER_ADMIN,
        UserRole.ADMIN,
    ]:
        raise HTTPException(status_code=403, detail="Huna ruhusa kufuta media hii")

    # Delete physical file
    physical_path = Path(media.file_path)
    if physical_path.exists():
        physical_path.unlink(missing_ok=True)

    db.delete(media)
    db.commit()

    return {"success": True, "message": "Media imefutwa"}