from dataclasses import dataclass
from pathlib import Path
from uuid import uuid4

from minio import Minio

from app.core.config import settings


@dataclass(frozen=True)
class StoredFile:
    storage_uri: str
    local_path: Path
    file_name: str
    content_type: str | None


class DocumentStorageService:
    def save_upload(self, file_name: str, content: bytes, content_type: str | None) -> StoredFile:
        safe_name = Path(file_name).name
        object_name = f"{uuid4()}-{safe_name}"
        local_path = self._write_local_copy(object_name, content)

        if settings.storage_backend == "minio":
            self._write_minio(object_name, local_path, content_type)
            storage_uri = f"minio://{settings.minio_bucket_documents}/{object_name}"
        else:
            storage_uri = str(local_path)

        return StoredFile(
            storage_uri=storage_uri,
            local_path=local_path,
            file_name=safe_name,
            content_type=content_type,
        )

    def _write_local_copy(self, object_name: str, content: bytes) -> Path:
        storage_dir = Path(settings.local_storage_path)
        storage_dir.mkdir(parents=True, exist_ok=True)
        path = storage_dir / object_name
        path.write_bytes(content)
        return path

    def _write_minio(self, object_name: str, local_path: Path, content_type: str | None) -> None:
        client = Minio(
            settings.minio_endpoint,
            access_key=settings.minio_access_key,
            secret_key=settings.minio_secret_key,
            secure=settings.minio_secure,
        )
        if not client.bucket_exists(settings.minio_bucket_documents):
            client.make_bucket(settings.minio_bucket_documents)
        client.fput_object(
            settings.minio_bucket_documents,
            object_name,
            str(local_path),
            content_type=content_type,
        )

