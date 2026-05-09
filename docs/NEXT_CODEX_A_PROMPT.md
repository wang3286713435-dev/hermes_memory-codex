# NEXT_CODEX_A_PROMPT

当前 DB-0a contract baseline 尚未完成，Codex A 暂停。

baseline 完成后，下一轮建议任务为 DB-1a Fake View Fixtures / Fake Adapter Contract Tests，边界如下：

1. 只使用 fake JSON fixtures，不连接真实 MySQL。
2. 不连接真实 NAS，不扫描 `/Volumes/zyzn/卓羽智能项目`。
3. 不写 `documents` / `chunks`。
4. 不写 OpenSearch / Qdrant。
5. 不做正文解析。
6. 不改 retrieval contract。
7. 不改 memory kernel 主架构。
8. 所有能力默认 feature flag off。

等待 Codex B 完成 DB-0a baseline 后，再写入正式 bounded prompt。
