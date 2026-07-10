"""
OcchioEsperto.it — Utility functions.
"""
import os
import uuid
from fastapi import UploadFile
from .config import UPLOAD_DIR


ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}


async def save_upload_file(upload_file: UploadFile, subdir: str = "") -> str:
    """Save an uploaded file and return the relative path."""
    ext = os.path.splitext(upload_file.filename or "photo.jpg")[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        ext = ".jpg"

    filename = f"{uuid.uuid4().hex}{ext}"
    target_dir = os.path.join(UPLOAD_DIR, subdir)
    os.makedirs(target_dir, exist_ok=True)

    filepath = os.path.join(target_dir, filename)
    content = await upload_file.read()
    with open(filepath, "wb") as f:
        f.write(content)

    relative_path = os.path.join("uploads", subdir, filename) if subdir else os.path.join("uploads", filename)
    return relative_path


def get_plan_features(plan: str) -> list:
    """Get feature list for a plan."""
    from .config import PLANS
    return PLANS.get(plan, PLANS["free"])["features"]