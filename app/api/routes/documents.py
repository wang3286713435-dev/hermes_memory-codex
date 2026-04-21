from fastapi import APIRouter, Depends, File, Form, UploadFile
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.documents import DocumentIngestRequest, DocumentIngestResponse
from app.services.ingestion.service import DocumentIngestionService
from app.services.storage.service import DocumentStorageService

router = APIRouter()


@router.post("/ingest", response_model=DocumentIngestResponse)
def ingest_document(
    request: DocumentIngestRequest,
    db: Session = Depends(get_db),
) -> DocumentIngestResponse:
    service = DocumentIngestionService(db=db)
    job = service.create_ingestion_job(request)
    return DocumentIngestResponse(
        job_id=job.id,
        status=job.status,
        message="Document ingestion job accepted.",
    )


@router.post("/upload", response_model=DocumentIngestResponse)
async def upload_document(
    file: UploadFile = File(...),
    title: str | None = Form(default=None),
    source_type: str = Form(default="manual"),
    document_type: str | None = Form(default=None),
    owner_id: str | None = Form(default=None),
    department_id: str | None = Form(default=None),
    project_id: str | None = Form(default=None),
    confidentiality_level: str = Form(default="internal"),
    db: Session = Depends(get_db),
) -> DocumentIngestResponse:
    content = await file.read()
    stored_file = DocumentStorageService().save_upload(file.filename or "upload.bin", content, file.content_type)
    request = DocumentIngestRequest(
        source_uri=file.filename or stored_file.storage_uri,
        title=title,
        source_type=source_type,
        document_type=document_type,
        owner_id=owner_id,
        department_id=department_id,
        project_id=project_id,
        confidentiality_level=confidentiality_level,
    )
    job = DocumentIngestionService(db=db).ingest_uploaded_file(request, stored_file)
    message = "Document ingestion completed." if job.status == "completed" else "Document ingestion failed."
    return DocumentIngestResponse(
        job_id=job.id,
        status=job.status,
        message=message,
        document_id=job.document_id,
        version_id=job.version_id,
        chunk_count=job.chunk_count,
        indexed_count=job.indexed_count,
    )
