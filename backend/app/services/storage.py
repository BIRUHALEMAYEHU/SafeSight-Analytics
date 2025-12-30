"""
Storage abstractions for handling uploaded files.
Currently implements local filesystem storage with basic metadata capture.
"""
from dataclasses import dataclass
from datetime import datetime
import hashlib
from pathlib import Path
from typing import Optional

from fastapi import UploadFile


@dataclass
class StoredFile:
    """Metadata about a stored file."""
    path: str
    public_path: str
    mime_type: str
    size: int
    checksum: str
    uploaded_at: datetime


class LocalStorage:
    """Local filesystem storage implementation."""

    def __init__(self, base_path: str = "static", public_prefix: str = "/static"):
        self.base_path = Path(base_path)
        self.public_prefix = public_prefix.rstrip("/")
        self.base_path.mkdir(parents=True, exist_ok=True)

    async def save_upload(self, file: UploadFile, subdir: str, filename: str) -> StoredFile:
        """Persist an UploadFile to disk and return metadata."""
        dest_dir = self.base_path / subdir
        dest_dir.mkdir(parents=True, exist_ok=True)

        content = await file.read()
        size = len(content)
        checksum = hashlib.sha256(content).hexdigest()

        dest_path = dest_dir / filename
        with open(dest_path, "wb") as f:
            f.write(content)

        mime_type = file.content_type or "application/octet-stream"
        public_path = f"{self.public_prefix}/{subdir}/{filename}"

        return StoredFile(
            path=str(dest_path),
            public_path=public_path,
            mime_type=mime_type,
            size=size,
            checksum=checksum,
            uploaded_at=datetime.utcnow(),
        )
