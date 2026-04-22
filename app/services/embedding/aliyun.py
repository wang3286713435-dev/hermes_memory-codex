from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import httpx

from app.core.config import settings


@dataclass
class EmbeddingOutcome:
    vector: list[float] | None
    status: str
    trace: dict[str, Any] = field(default_factory=dict)


class AliyunTextEmbeddingV3:
    """Minimal DashScope text-embedding-v3 client.

    This client is intentionally narrow: it generates a single 1024-dimensional
    query vector for Qdrant dense retrieval. Batch indexing remains outside
    Phase 2.1-Qdrant.
    """

    def embed_query(self, text: str) -> EmbeddingOutcome:
        if not settings.aliyun_embedding_api_key:
            return EmbeddingOutcome(
                vector=None,
                status="unavailable",
                trace={"reason": "ALIYUN_EMBEDDING_API_KEY is not configured"},
            )

        payload = {
            "model": settings.aliyun_embedding_model,
            "input": {"texts": [text]},
            "parameters": {"dimension": settings.aliyun_embedding_dimension},
        }
        headers = {
            "Authorization": f"Bearer {settings.aliyun_embedding_api_key}",
            "Content-Type": "application/json",
        }
        try:
            response = httpx.post(
                settings.aliyun_embedding_base_url,
                json=payload,
                headers=headers,
                timeout=15,
            )
            response.raise_for_status()
            data = response.json()
        except Exception as exc:
            return EmbeddingOutcome(vector=None, status="failed", trace={"error": str(exc)})

        embeddings = (data.get("output") or {}).get("embeddings") or []
        if not embeddings:
            return EmbeddingOutcome(
                vector=None,
                status="failed",
                trace={"reason": "empty_embedding_response"},
            )

        vector = embeddings[0].get("embedding") or []
        if len(vector) != settings.aliyun_embedding_dimension:
            return EmbeddingOutcome(
                vector=None,
                status="failed",
                trace={
                    "reason": "embedding_dimension_mismatch",
                    "expected_dimension": settings.aliyun_embedding_dimension,
                    "actual_dimension": len(vector),
                },
            )
        return EmbeddingOutcome(
            vector=[float(value) for value in vector],
            status="executed",
            trace={
                "provider": "aliyun",
                "model": settings.aliyun_embedding_model,
                "dimension": settings.aliyun_embedding_dimension,
            },
        )
