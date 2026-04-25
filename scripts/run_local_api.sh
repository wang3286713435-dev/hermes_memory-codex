#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

# Local developer helper for running the API against local Docker services.
# Do not place real secrets in this script; override sensitive values in the shell.
export NO_PROXY="${NO_PROXY:-127.0.0.1,localhost,::1}"
export no_proxy="${no_proxy:-127.0.0.1,localhost,::1}"

export DATABASE_URL="postgresql+psycopg://hermes:hermes@127.0.0.1:5432/hermes_memory"
export REDIS_URL="redis://127.0.0.1:6379/0"
export CELERY_BROKER_URL="redis://127.0.0.1:6379/1"
export CELERY_RESULT_BACKEND="redis://127.0.0.1:6379/2"
export OPENSEARCH_URL="http://127.0.0.1:9200"
export OPENSEARCH_INDEX_CHUNKS="hermes_chunks"
export MINIO_ENDPOINT="127.0.0.1:9000"
export QDRANT_URL="http://127.0.0.1:6333"

if [[ ! -x "$ROOT_DIR/.venv-phase21/bin/python" ]]; then
  echo "Missing Python runtime: $ROOT_DIR/.venv-phase21/bin/python" >&2
  exit 1
fi

exec "$ROOT_DIR/.venv-phase21/bin/python" -m uvicorn app.main:app --host 127.0.0.1 --port 8000
