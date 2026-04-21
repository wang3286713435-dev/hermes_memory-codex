from app.core.logging import get_logger
from app.worker.celery_app import celery_app

logger = get_logger(__name__)


@celery_app.task(name="documents.ingest")
def ingest_document_task(job_id: str) -> dict:
    logger.info("document_ingestion_task_started", extra={"job_id": job_id})
    return {"job_id": job_id, "status": "not_implemented"}

