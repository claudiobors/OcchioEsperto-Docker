"""
OcchioEsperto.it — Utility functions.
"""
import os
import uuid
import imghdr
from fastapi import UploadFile, HTTPException, status
from .config import UPLOAD_DIR

# Allowed image extensions and their MIME types
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
ALLOWED_MIME_TYPES = {
    "image/jpeg",
    "image/png",
    "image/gif",
    "image/webp",
}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB


async def save_upload_file(upload_file: UploadFile, subdir: str = "") -> str:
    """
    Save an uploaded file and return the relative path.
    Validates file type, size, and content before saving.
    """
    # Validate filename
    if not upload_file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Nessun file caricato",
        )

    # Validate extension
    ext = os.path.splitext(upload_file.filename or "photo.jpg")[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Estensione file non consentita: {ext}. "
                   f"Usa: {', '.join(ALLOWED_EXTENSIONS)}",
        )

    # Validate content type
    content_type = upload_file.content_type or ""
    if content_type and content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Tipo MIME non consentito: {content_type}",
        )

    # Read and validate size
    content = await upload_file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File troppo grande: {len(content) / 1024 / 1024:.1f} MB. "
                   f"Massimo consentito: {MAX_FILE_SIZE / 1024 / 1024:.0f} MB",
        )

    # Validate actual image content (magic bytes)
    if not _is_valid_image(content):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Il file non sembra essere un'immagine valida",
        )

    # Save file
    filename = f"{uuid.uuid4().hex}{ext}"
    target_dir = os.path.join(UPLOAD_DIR, subdir)
    os.makedirs(target_dir, exist_ok=True)

    filepath = os.path.join(target_dir, filename)
    with open(filepath, "wb") as f:
        f.write(content)

    relative_path = os.path.join("uploads", subdir, filename) if subdir else os.path.join("uploads", filename)
    return relative_path


def _is_valid_image(data: bytes) -> bool:
    """
    Basic magic bytes validation for common image formats.
    Checks the file header (first bytes) to confirm it's a real image.
    """
    if len(data) < 12:
        return False

    # JPEG: starts with \xFF\xD8\xFF
    if data[:3] == b'\xff\xd8\xff':
        return True

    # PNG: starts with \x89PNG
    if data[:8] == b'\x89PNG\r\n\x1a\n':
        return True

    # GIF: starts with GIF87a or GIF89a
    if data[:6] in (b'GIF87a', b'GIF89a'):
        return True

    # WebP: starts with RIFF....WEBP
    if data[:4] == b'RIFF' and data[8:12] == b'WEBP':
        return True

    return False


def sanitize_string(value: str, max_length: int = 255) -> str:
    """
    Sanitize a string input: strip whitespace, collapse multiple spaces,
    remove null bytes, and truncate to max_length.
    """
    if not value:
        return ""

    # Remove null bytes
    value = value.replace("\x00", "")

    # Strip leading/trailing whitespace
    value = value.strip()

    # Collapse multiple spaces/newlines into single space
    import re
    value = re.sub(r'\s+', ' ', value)

    # Truncate
    if len(value) > max_length:
        value = value[:max_length]

    return value


def get_plan_features(plan: str) -> list:
    """Get feature list for a plan."""
    from .config import PLANS
    return PLANS.get(plan, PLANS["free"])["features"]