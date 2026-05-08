# NEXT_CODEX_C_PROMPT

当前没有 Codex C 真实终端复验任务。

Phase 2.54c File Steward UX display-tail targeted smoke 已通过：

1. session_id：`20260508_181817_c7c9a3`
2. `@主标书` 绑定通过。
3. Q3 file answer metadata：pass。
4. `file_answer_metadata_required_fields` 可见。
5. `file_answer_metadata_echo_required=true` 可见。
6. `title/source_name/source_type/citation_count` 字段可见。
7. `metadata_as_answer=false`、`facts_as_answer=false`、`snapshot_as_answer=false`、`requires_retrieval_evidence=true` 全部可见。
8. 未出现 metadata / facts / transcript / snapshot 替代 evidence。
9. 未出现第三文件污染。

当前下一步应由 Codex A 执行 selective Git baseline：

`/Users/Weishengsu/Hermes_memory/docs/NEXT_CODEX_A_PROMPT.md`

请 Codex C 暂停，不要继续复跑 smoke，不要修改代码或文档，不要上传文件，不要写 DB / facts / versions / OpenSearch / Qdrant，不要进入 rollout、repair 或 Data Steward。
