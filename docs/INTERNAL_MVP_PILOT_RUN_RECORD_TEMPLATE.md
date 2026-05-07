# Internal MVP Pilot Run Record Template

This template is for sanitized local records of Hermes internal controlled MVP runs.

Real run records must be saved under `reports/internal_mvp_runs/` and are ignored by Git by default. This template is not a production rollout approval, customer delivery artifact, repair request, or automatic business decision.

## 1. Record Metadata

```json
{
  "record_type": "internal_mvp_pilot_run_record",
  "date": "YYYY-MM-DD",
  "run_window": "Day 0 | Day 1-2 | Day 3-5 | Week 2",
  "operator": "",
  "recorder": "",
  "reviewer": "",
  "business_owner": "",
  "machine": {
    "label": "mac-mini-internal-mvp",
    "sanitized_hostname": "",
    "lan_scope": "internal-lan-only",
    "sanitized_lan_ip": ""
  },
  "git": {
    "hermes_memory_commit": "",
    "hermes_memory_tag": "",
    "hermes_agent_commit": "",
    "hermes_agent_tag": ""
  }
}
```

Rules:

1. Do not paste secrets, `.env` values, tokens, passwords, raw logs, customer-sensitive text, or raw transcript into this record.
2. Commit / tag values should be reviewed Git refs, not ad-hoc Mac mini edits.
3. A run record does not prove production readiness.

## 2. Environment Summary

```json
{
  "environment_summary": {
    "api_health": "pass|warn|fail",
    "hermes_cli_help": "pass|warn|fail",
    "services": {
      "postgres": "pass|warn|fail|not_checked",
      "opensearch": "pass|warn|fail|not_checked",
      "qdrant": "pass|warn|fail|not_checked",
      "minio": "pass|warn|fail|not_used|not_checked",
      "redis": "pass|warn|fail|not_used|not_checked"
    },
    "env_key_names_present": true,
    "env_values_recorded": false,
    "qdrant_collection_status": "expected_hermes_chunks|deviation_recorded|not_checked",
    "notes": ""
  }
}
```

If a service needs repair / backfill / reindex / migration, stop and create a separate issue. Do not fix from this record.

## 3. Alias Summary

```json
{
  "alias_summary": [
    {
      "alias": "@主标书",
      "status": "pass|warn|fail",
      "alias_resolution_status": "",
      "document_id": "",
      "version_id": "",
      "alias_missing": false,
      "retrieval_suppressed": false
    },
    {
      "alias": "@会议纪要",
      "status": "pass|warn|fail",
      "alias_resolution_status": "",
      "document_id": "",
      "version_id": "",
      "alias_missing": false,
      "retrieval_suppressed": false
    },
    {
      "alias": "@硬件清单",
      "status": "pass|warn|fail",
      "alias_resolution_status": "",
      "document_id": "",
      "version_id": "",
      "alias_missing": false,
      "retrieval_suppressed": false
    },
    {
      "alias": "@C塔方案",
      "status": "pass|warn|fail",
      "alias_resolution_status": "",
      "document_id": "",
      "version_id": "",
      "alias_missing": false,
      "retrieval_suppressed": false
    }
  ]
}
```

Severity reminder:

1. Wrong document evidence is P0.
2. Persistent alias missing / retrieval suppressed on fixed aliases is P1.
3. Stale version warnings must be reviewed before business use.

## 4. Daily Query Summary

```json
{
  "daily_query_summary": [
    {
      "query_area": "main_tender_basic_fields",
      "result": "pass|partial|fail",
      "evidence_document_ids": [],
      "citation_summary": "",
      "missing_evidence_visible": true,
      "facts_as_answer": false,
      "transcript_as_fact": false,
      "snapshot_as_answer": false,
      "third_document_contamination": false,
      "notes": ""
    },
    {
      "query_area": "excel_structured_citation",
      "result": "pass|partial|fail",
      "evidence_document_ids": [],
      "citation_summary": "",
      "missing_evidence_visible": true,
      "facts_as_answer": false,
      "transcript_as_fact": false,
      "snapshot_as_answer": false,
      "third_document_contamination": false,
      "notes": ""
    },
    {
      "query_area": "pptx_structured_citation",
      "result": "pass|partial|fail",
      "evidence_document_ids": [],
      "citation_summary": "",
      "missing_evidence_visible": true,
      "facts_as_answer": false,
      "transcript_as_fact": false,
      "snapshot_as_answer": false,
      "third_document_contamination": false,
      "notes": ""
    },
    {
      "query_area": "meeting_actions_decisions_risks",
      "result": "pass|partial|fail",
      "evidence_document_ids": [],
      "citation_summary": "",
      "missing_evidence_visible": true,
      "facts_as_answer": false,
      "transcript_as_fact": false,
      "snapshot_as_answer": false,
      "third_document_contamination": false,
      "notes": ""
    },
    {
      "query_area": "optional_company_direction_analysis",
      "result": "pass|partial|fail|not_run",
      "evidence_document_ids": [],
      "citation_summary": "",
      "missing_evidence_visible": true,
      "facts_as_answer": false,
      "transcript_as_fact": false,
      "snapshot_as_answer": false,
      "third_document_contamination": false,
      "human_business_decision_required": true,
      "notes": ""
    }
  ]
}
```

Do not record raw model output unless it is sanitized and intentionally stored in a local ignored file.

## 5. Issue Summary

```json
{
  "issue_summary": {
    "p0_count": 0,
    "p1_count": 0,
    "p2_count": 0,
    "p3_count": 0,
    "issues": [
      {
        "issue_id": "internal-mvp-YYYYMMDD-001",
        "severity": "P0|P1|P2|P3",
        "issue_type": "retrieval_recall|citation_display|trace_ux|alias_session|latency|contamination|answer_boundary|operator_env|other",
        "affected_alias": "",
        "source_document_id": "",
        "source_version_id": "",
        "citation_or_source": "",
        "owner": "",
        "next_action": "",
        "manual_workaround": ""
      }
    ]
  }
}
```

Issue handling:

1. P0 means immediate Pause / No-Go.
2. P1 pauses expansion until fixed or manually worked around.
3. P2 can continue if human-reviewable and recorded.
4. P3 is backlog.

## 6. Decision

```json
{
  "decision": {
    "status": "Go|Pause|No-Go",
    "reviewer": "",
    "business_owner_ack": false,
    "allowed_next_day_scope": "same_users|small_expansion|pause|no_go",
    "reason": "",
    "not_production_rollout": true,
    "not_customer_delivery": true,
    "not_automatic_tender_review": true,
    "not_automatic_bid": true,
    "not_automatic_business_decision": true
  }
}
```

## 7. Boundary Attestation

```json
{
  "boundaries": {
    "not_production_rollout": true,
    "not_customer_delivery": true,
    "not_automatic_tender_review": true,
    "not_automatic_bid": true,
    "not_automatic_business_decision": true,
    "not_repair_cleanup_backfill_reindex_delete": true,
    "no_db_facts_document_versions_auditlogs_opensearch_qdrant_mutation": true,
    "no_data_steward_bim_implementation": true,
    "no_retrieval_contract_change": true,
    "no_memory_kernel_architecture_change": true
  }
}
```

If any boundary is false, classify the run as `No-Go` and stop expansion.

