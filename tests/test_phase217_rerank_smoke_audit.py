from scripts.phase217_rerank_smoke_audit import RerankSmokeCase, evaluate_rerank_response


def test_rerank_audit_accepts_executed_provider_call():
    case = RerankSmokeCase(id="tender", query="资质要求", filters={}, expect_policy_match=True)
    result = evaluate_rerank_response(
        case,
        {
            "rerank_status": "executed",
            "rerank": {
                "provider": "aliyun_text_rerank",
                "model": "gte-rerank-v2",
                "output_count": 3,
                "elapsed_ms": 123.4,
                "fail_open": False,
                "api_key_source": "ALIYUN_RERANK_API_KEY",
            },
            "rerank_policy": {"enabled": True, "reason": "local_default_enablement_matched", "candidate_count": 5},
        },
        [_Result("doc-1")],
        latency_ms=200,
    )

    assert result.passed is True
    assert result.rerank_status == "executed"
    assert result.rerank_returned == 3


def test_rerank_audit_accepts_fail_open_with_reason():
    case = RerankSmokeCase(id="tender", query="资质要求", filters={}, expect_policy_match=True)
    result = evaluate_rerank_response(
        case,
        {
            "rerank_status": "failed_open",
            "rerank": {
                "provider": "aliyun_text_rerank",
                "status": "failed_open",
                "fail_open": True,
                "reason": "timeout",
                "error_type": "timeout",
                "output_count": 2,
            },
            "rerank_policy": {"enabled": True, "reason": "local_default_enablement_matched", "candidate_count": 4},
        },
        [_Result("doc-1")],
        latency_ms=200,
    )

    assert result.passed is True
    assert result.fail_open is True
    assert result.fail_open_reason == "timeout"


def test_rerank_audit_allows_structured_file_skipped_with_reason():
    case = RerankSmokeCase(id="xlsx", query="付款比例", filters={}, allow_skipped=True)
    result = evaluate_rerank_response(
        case,
        {
            "rerank_status": "skipped",
            "rerank": {"provider": "noop", "reason_if_skipped": "local_default_enablement_not_matched"},
            "rerank_policy": {"enabled": False, "reason": "local_default_enablement_not_matched"},
        },
        [_Result("doc-1")],
        latency_ms=20,
    )

    assert result.passed is True
    assert result.policy_reason == "local_default_enablement_not_matched"


def test_rerank_audit_rejects_expected_policy_match_skipped():
    case = RerankSmokeCase(id="tender", query="资质要求", filters={}, expect_policy_match=True)
    result = evaluate_rerank_response(
        case,
        {
            "rerank_status": "skipped",
            "rerank": {"provider": "noop", "reason_if_skipped": "local_default_enablement_not_matched"},
            "rerank_policy": {"enabled": False, "reason": "local_default_enablement_not_matched"},
        },
        [_Result("doc-1")],
        latency_ms=20,
    )

    assert result.passed is False


class _Result:
    def __init__(self, document_id: str) -> None:
        self.document_id = document_id
