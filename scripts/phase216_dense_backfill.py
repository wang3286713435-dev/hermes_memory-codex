#!/usr/bin/env python
from __future__ import annotations

import argparse
import json
from time import perf_counter
from typing import Any

import app.models  # noqa: F401 - ensure SQLAlchemy models are registered.
from app.db.session import SessionLocal
from app.models.chunk import Chunk
from app.models.document import Document, DocumentVersion
from app.services.indexing.dense import DenseChunkIndexer


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Backfill Qdrant dense vectors for explicitly selected documents.",
    )
    parser.add_argument(
        "--document-id",
        dest="document_ids",
        action="append",
        required=True,
        help="Document id to backfill. Repeat for multiple documents. No full-table default is allowed.",
    )
    parser.add_argument("--dry-run", action="store_true", help="List selected chunks without embedding/upsert.")
    return parser


def backfill_documents(document_ids: list[str], *, dry_run: bool = False) -> dict[str, Any]:
    db = SessionLocal()
    try:
        indexer = DenseChunkIndexer()
        documents: list[dict[str, Any]] = []
        for document_id in document_ids:
            started = perf_counter()
            document = db.get(Document, document_id)
            if document is None:
                documents.append({"document_id": document_id, "status": "not_found", "duration_ms": _elapsed_ms(started)})
                continue
            version = (
                db.query(DocumentVersion)
                .filter(DocumentVersion.document_id == document_id, DocumentVersion.is_latest.is_(True))
                .order_by(DocumentVersion.created_at.desc())
                .first()
            )
            if version is None:
                documents.append(
                    {"document_id": document_id, "status": "version_not_found", "duration_ms": _elapsed_ms(started)}
                )
                continue
            chunks = (
                db.query(Chunk)
                .filter(Chunk.document_id == document_id, Chunk.version_id == version.id)
                .order_by(Chunk.chunk_index.asc())
                .all()
            )
            if dry_run:
                documents.append(
                    {
                        "document_id": document_id,
                        "version_id": version.id,
                        "title": document.title,
                        "status": "dry_run",
                        "chunk_count": len(chunks),
                        "dense_attempted_count": 0,
                        "duration_ms": _elapsed_ms(started),
                    }
                )
                continue

            summary = indexer.index_chunks(chunks, document, version)
            version.metadata_json = {
                **(version.metadata_json or {}),
                "dense_ingestion": summary.as_dict(),
            }
            db.commit()
            documents.append(
                {
                    "document_id": document_id,
                    "version_id": version.id,
                    "title": document.title,
                    "chunk_count": len(chunks),
                    "dense_attempted_count": len(chunks),
                    "duration_ms": _elapsed_ms(started),
                    **summary.as_dict(),
                }
            )

        return {
            "total_documents": len(document_ids),
            "dry_run": dry_run,
            "documents": documents,
        }
    finally:
        db.close()


def main() -> int:
    args = build_parser().parse_args()
    summary = backfill_documents(args.document_ids, dry_run=args.dry_run)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


def _elapsed_ms(started: float) -> float:
    return round((perf_counter() - started) * 1000, 3)


if __name__ == "__main__":
    raise SystemExit(main())
