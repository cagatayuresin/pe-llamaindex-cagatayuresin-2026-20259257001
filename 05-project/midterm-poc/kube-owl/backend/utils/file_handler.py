"""
KubeOps Agent — Dosya İşleme Yardımcıları
Dosya kaydetme, format kontrolü, boyut kontrolü.
"""

import logging
import os
from pathlib import Path
from fastapi import UploadFile

from ..config import settings

logger = logging.getLogger(__name__)

# İzin verilen dosya uzantıları
ALLOWED_EXTENSIONS = {".pdf", ".md", ".txt"}


def validate_file(file: UploadFile) -> tuple[bool, str]:
    """
    Yüklenen dosyanın geçerliliğini kontrol eder.

    Args:
        file: FastAPI UploadFile objesi

    Returns:
        (is_valid, error_message)
    """
    if not file.filename:
        return False, "Dosya adı boş olamaz."

    # Uzantı kontrolü
    ext = Path(file.filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        return False, (
            f"Desteklenmeyen dosya formatı: {ext}. "
            f"İzin verilen formatlar: {', '.join(ALLOWED_EXTENSIONS)}"
        )

    return True, ""


async def save_uploaded_file(file: UploadFile) -> str:
    """
    Yüklenen dosyayı diske kaydeder.

    Args:
        file: FastAPI UploadFile objesi

    Returns:
        Kaydedilen dosyanın tam yolu
    """
    upload_dir = settings.upload_path
    upload_dir.mkdir(parents=True, exist_ok=True)

    file_path = upload_dir / file.filename

    # Aynı isimde dosya varsa üzerine yaz
    content = await file.read()

    # Boyut kontrolü
    if len(content) > settings.max_file_size_bytes:
        raise ValueError(
            f"Dosya boyutu çok büyük: {len(content) / (1024*1024):.1f}MB. "
            f"Maksimum: {settings.max_file_size_mb}MB"
        )

    with open(file_path, "wb") as f:
        f.write(content)

    logger.info(f"Dosya kaydedildi: {file_path} ({len(content)} bytes)")
    return str(file_path)
