"""
OcchioEsperto.it — Utility functions.
"""
from __future__ import annotations

import os
import uuid
from pathlib import Path
from typing import Optional

from fastapi import HTTPException, UploadFile, status
from PIL import Image, ImageStat

from .config import MAX_UPLOAD_MB, UPLOAD_DIR


ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
ALLOWED_CONTENT_TYPES = {"image/jpeg", "image/png", "image/webp"}


async def save_upload_file(upload_file: UploadFile, subdir: str = "") -> str:
    """Validate and save an uploaded image. Returns web-relative path under /uploads."""
    ext = os.path.splitext(upload_file.filename or "photo.jpg")[1].lower()
    if ext not in ALLOWED_EXTENSIONS or upload_file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Formato immagine non supportato. Usa JPG, PNG o WEBP.",
        )

    content = await upload_file.read()
    max_bytes = MAX_UPLOAD_MB * 1024 * 1024
    if len(content) > max_bytes:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File troppo grande. Limite: {MAX_UPLOAD_MB}MB.",
        )

    filename = f"{uuid.uuid4().hex}{ext}"
    target_dir = Path(UPLOAD_DIR) / subdir
    target_dir.mkdir(parents=True, exist_ok=True)
    filepath = target_dir / filename
    filepath.write_bytes(content)

    # Verify it is a real image and normalize EXIF/orientation by reopening.
    try:
        with Image.open(filepath) as img:
            img.verify()
    except Exception as exc:
        filepath.unlink(missing_ok=True)
        raise HTTPException(status_code=400, detail="Il file caricato non sembra un'immagine valida.") from exc

    return str(Path("uploads") / subdir / filename) if subdir else str(Path("uploads") / filename)


def absolute_upload_path(relative_path: str) -> str:
    rel = relative_path.replace("\\", "/").lstrip("/")
    if rel.startswith("uploads/"):
        rel = rel[len("uploads/"):]
    return str(Path(UPLOAD_DIR) / rel)


def extract_dominant_hex(image_path: str) -> Optional[str]:
    """Return an approximate dominant body color from an uploaded image."""
    try:
        with Image.open(image_path) as img:
            img = img.convert("RGB")
            img.thumbnail((180, 180))
            # Crop central area to avoid too much background.
            w, h = img.size
            crop = img.crop((int(w * 0.15), int(h * 0.15), int(w * 0.85), int(h * 0.85)))
            # Quantize to a small palette and ignore very bright/dark neutral background pixels.
            colors = crop.quantize(colors=8, method=Image.Quantize.MEDIANCUT).convert("RGB").getcolors(180 * 180)
            if not colors:
                stat = ImageStat.Stat(crop)
                r, g, b = [int(v) for v in stat.mean]
                return f"#{r:02X}{g:02X}{b:02X}"
            scored = []
            for count, (r, g, b) in colors:
                saturation = max(r, g, b) - min(r, g, b)
                brightness = (r + g + b) / 3
                if 25 < brightness < 240:
                    scored.append((count * (1 + saturation / 255), r, g, b))
            _, r, g, b = max(scored or [(c, *rgb) for c, rgb in colors], key=lambda x: x[0])
            return f"#{r:02X}{g:02X}{b:02X}"
    except Exception:
        return None


def get_plan_features(plan: str) -> list:
    """Get feature list for a plan."""
    from .config import PLANS
    return PLANS.get(plan, PLANS["free"])["features"]
