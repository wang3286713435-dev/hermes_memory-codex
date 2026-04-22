from __future__ import annotations

import os
import sys

from opensearchpy import OpenSearch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.core.config import settings
from app.services.embedding import AliyunTextEmbeddingV3
from app.services.retrieval.dense import QdrantDenseRetriever


EVAL_CORPUS = [
    {
        "chunk_id": "c1011111-1111-1111-1111-111111111111",
        "document_id": "doc-tender-park",
        "version_id": "ver-tender-park-v1",
        "chunk_index": 1,
        "text": "智慧园区项目需要支持统一身份认证、知识检索和权限治理，覆盖园区安防、运维和访客场景，建设周期为6个月。",
        "source_name": "智慧园区招标资料",
        "source_uri": "memory://eval/doc-tender-park",
        "source_type": "tender",
        "document_type": "tender",
        "version_name": "v1",
        "heading_path": ["第一章", "项目背景"],
        "page_start": 1,
        "page_end": 1,
        "metadata_json": {"dataset": "phase23_eval", "doc_group": "tender"},
        "status": "active",
        "is_latest": True,
    },
    {
        "chunk_id": "c1022222-2222-2222-2222-222222222222",
        "document_id": "doc-tender-park",
        "version_id": "ver-tender-park-v1",
        "chunk_index": 2,
        "text": "投标方应具备软件开发能力、项目实施经验和信息安全管理能力，具备ISO9001或同等质量管理体系认证，并提供近三年类似园区项目案例。",
        "source_name": "智慧园区招标资料",
        "source_uri": "memory://eval/doc-tender-park",
        "source_type": "tender",
        "document_type": "tender",
        "version_name": "v1",
        "heading_path": ["第二章", "资质要求"],
        "page_start": 2,
        "page_end": 2,
        "metadata_json": {"dataset": "phase23_eval", "doc_group": "tender"},
        "status": "active",
        "is_latest": True,
    },
    {
        "chunk_id": "c1033333-3333-3333-3333-333333333333",
        "document_id": "doc-tender-park",
        "version_id": "ver-tender-park-v1",
        "chunk_index": 3,
        "text": "投标截止日期为2026年5月20日17时，答疑截止日期为2026年5月15日18时，开标时间为2026年5月21日09时30分。",
        "source_name": "智慧园区招标资料",
        "source_uri": "memory://eval/doc-tender-park",
        "source_type": "tender",
        "document_type": "tender",
        "version_name": "v1",
        "heading_path": ["第三章", "时间安排"],
        "page_start": 3,
        "page_end": 3,
        "metadata_json": {"dataset": "phase23_eval", "doc_group": "tender"},
        "status": "active",
        "is_latest": True,
    },
    {
        "chunk_id": "c1044444-4444-4444-4444-444444444444",
        "document_id": "doc-tender-park",
        "version_id": "ver-tender-park-v1",
        "chunk_index": 4,
        "text": "投标保证金为20万元，投标有效期90天，故障响应时限不超过2小时，重大故障需在24小时内提交整改报告。",
        "source_name": "智慧园区招标资料",
        "source_uri": "memory://eval/doc-tender-park",
        "source_type": "tender",
        "document_type": "tender",
        "version_name": "v1",
        "heading_path": ["第四章", "商务条款"],
        "page_start": 4,
        "page_end": 4,
        "metadata_json": {"dataset": "phase23_eval", "doc_group": "tender"},
        "status": "active",
        "is_latest": True,
    },
    {
        "chunk_id": "c1055555-5555-5555-5555-555555555555",
        "document_id": "doc-tender-park",
        "version_id": "ver-tender-park-v1",
        "chunk_index": 5,
        "text": "评分标准中技术部分45分，商务部分25分，价格部分30分；技术方案需覆盖统一身份认证、知识检索和权限治理三项能力。",
        "source_name": "智慧园区招标资料",
        "source_uri": "memory://eval/doc-tender-park",
        "source_type": "tender",
        "document_type": "tender",
        "version_name": "v1",
        "heading_path": ["第五章", "评分标准"],
        "page_start": 5,
        "page_end": 5,
        "metadata_json": {"dataset": "phase23_eval", "doc_group": "tender"},
        "status": "active",
        "is_latest": True,
    },
    {
        "chunk_id": "c1066666-6666-6666-6666-666666666666",
        "document_id": "doc-company-qualification",
        "version_id": "ver-company-qualification-v1",
        "chunk_index": 1,
        "text": "公司已通过ISO9001、ISO27001和CMMI3认证，具备安防工程企业一级资质，可承接智慧园区与城市治理类项目。",
        "source_name": "公司资质手册",
        "source_uri": "memory://eval/doc-company-qualification",
        "source_type": "company_doc",
        "document_type": "qualification",
        "version_name": "v1",
        "heading_path": ["第一章", "资质概览"],
        "page_start": 1,
        "page_end": 1,
        "metadata_json": {"dataset": "phase23_eval", "doc_group": "company"},
        "status": "active",
        "is_latest": True,
    },
    {
        "chunk_id": "c1077777-7777-7777-7777-777777777777",
        "document_id": "doc-wechat-cityline",
        "version_id": "ver-wechat-cityline-v1",
        "chunk_index": 1,
        "text": "公众号文章《城市生命线一体化平台案例》提到，公司通过AI知识助手将方案知识上线周期从三周缩短到7天，并沉淀巡检问答模板。",
        "source_name": "公众号：城市生命线一体化平台案例",
        "source_uri": "memory://eval/doc-wechat-cityline",
        "source_type": "wechat",
        "document_type": "article",
        "version_name": "v1",
        "heading_path": ["正文", "实施成效"],
        "page_start": 1,
        "page_end": 1,
        "metadata_json": {"dataset": "phase23_eval", "doc_group": "wechat"},
        "status": "active",
        "is_latest": True,
    },
    {
        "chunk_id": "c1088888-8888-8888-8888-888888888888",
        "document_id": "doc-wechat-security",
        "version_id": "ver-wechat-security-v1",
        "chunk_index": 1,
        "text": "公众号文章《智慧园区安全运营实践》提到，项目通过视频监控、周界报警和门禁联动满足等保三级要求，并每月组织一次应急演练。",
        "source_name": "公众号：智慧园区安全运营实践",
        "source_uri": "memory://eval/doc-wechat-security",
        "source_type": "wechat",
        "document_type": "article",
        "version_name": "v1",
        "heading_path": ["正文", "安全运营"],
        "page_start": 1,
        "page_end": 1,
        "metadata_json": {"dataset": "phase23_eval", "doc_group": "wechat"},
        "status": "active",
        "is_latest": True,
    },
    {
        "chunk_id": "c1099999-9999-9999-9999-999999999999",
        "document_id": "doc-policy-hr",
        "version_id": "ver-policy-hr-v1",
        "chunk_index": 1,
        "text": "员工年假制度规定：累计工作满1年不足10年的年假5天，满10年不足20年的年假10天，满20年的年假15天；当年未休年假可顺延至次年第一季度末。",
        "source_name": "员工年假制度",
        "source_uri": "memory://eval/doc-policy-hr",
        "source_type": "policy",
        "document_type": "policy",
        "version_name": "v1",
        "heading_path": ["第三章", "休假规则"],
        "page_start": 3,
        "page_end": 3,
        "metadata_json": {"dataset": "phase23_eval", "doc_group": "policy"},
        "status": "active",
        "is_latest": True,
    },
    {
        "chunk_id": "c1101010-1010-1010-1010-101010101010",
        "document_id": "doc-contract-payment",
        "version_id": "ver-contract-payment-v1",
        "chunk_index": 1,
        "text": "合同付款条款约定：合同生效后支付30%预付款，项目验收通过后支付40%，剩余30%作为质保金在12个月质保期结束后支付。",
        "source_name": "项目合同付款条款",
        "source_uri": "memory://eval/doc-contract-payment",
        "source_type": "contract",
        "document_type": "contract",
        "version_name": "v1",
        "heading_path": ["第六条", "付款安排"],
        "page_start": 6,
        "page_end": 6,
        "metadata_json": {"dataset": "phase23_eval", "doc_group": "contract"},
        "status": "active",
        "is_latest": True,
    },
    {
        "chunk_id": "c1111112-1112-1112-1112-111211121112",
        "document_id": "doc-project-xinghe",
        "version_id": "ver-project-xinghe-v1",
        "chunk_index": 1,
        "text": "星河项目交付报告显示，平台于2025年11月18日正式上线，接入120个站点，告警与工单数据同步时延控制在5分钟以内。",
        "source_name": "星河项目交付报告",
        "source_uri": "memory://eval/doc-project-xinghe",
        "source_type": "project_doc",
        "document_type": "project_report",
        "version_name": "v1",
        "heading_path": ["第二章", "上线与运行"],
        "page_start": 2,
        "page_end": 2,
        "metadata_json": {"dataset": "phase23_eval", "doc_group": "project"},
        "status": "active",
        "is_latest": True,
    },
    {
        "chunk_id": "c1121212-1212-1212-1212-121212121212",
        "document_id": "doc-proposal-multitenant",
        "version_id": "ver-proposal-multitenant-v1",
        "chunk_index": 1,
        "text": "多租户平台方案提出，数据按租户逻辑隔离，操作日志保留180天，审计日志支持按项目、部门和用户维度查询。",
        "source_name": "多租户平台方案",
        "source_uri": "memory://eval/doc-proposal-multitenant",
        "source_type": "proposal",
        "document_type": "proposal",
        "version_name": "v1",
        "heading_path": ["第四章", "数据与审计"],
        "page_start": 4,
        "page_end": 4,
        "metadata_json": {"dataset": "phase23_eval", "doc_group": "proposal"},
        "status": "active",
        "is_latest": True,
    },
]


def main() -> None:
    embedding = AliyunTextEmbeddingV3()
    qdrant = QdrantDenseRetriever(embedding=embedding)
    qdrant.ensure_collection()

    os_client = OpenSearch(settings.opensearch_url, timeout=10)
    if not os_client.indices.exists(index=settings.opensearch_index_chunks):
        os_client.indices.create(index=settings.opensearch_index_chunks)

    for item in EVAL_CORPUS:
        outcome = embedding.embed_query(item["text"])
        if outcome.status != "executed" or not outcome.vector:
            raise RuntimeError(f"failed to embed {item['chunk_id']}: {outcome.trace}")

        qdrant.upsert_chunk(
            chunk_id=item["chunk_id"],
            vector=outcome.vector,
            payload={
                "document_id": item["document_id"],
                "version_id": item["version_id"],
                "chunk_index": item["chunk_index"],
                "text": item["text"],
                "source_name": item["source_name"],
                "source_uri": item["source_uri"],
                "source_type": item["source_type"],
                "document_type": item["document_type"],
                "version_name": item["version_name"],
                "heading_path": item["heading_path"],
                "page_start": item["page_start"],
                "page_end": item["page_end"],
                "metadata": item["metadata_json"],
                "is_latest": item["is_latest"],
            },
        )
        os_client.index(index=settings.opensearch_index_chunks, id=item["chunk_id"], body=item, refresh=True)

    print(
        {
            "seeded_chunks": len(EVAL_CORPUS),
            "qdrant_collection": settings.qdrant_collection,
            "opensearch_index": settings.opensearch_index_chunks,
        }
    )


if __name__ == "__main__":
    main()
