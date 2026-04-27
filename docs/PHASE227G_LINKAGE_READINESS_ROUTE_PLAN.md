# Phase 2.27g Linkage Readiness Route Plan

## 1. 当前基线

Phase 2.27f 已完成 archive / review / audit 只读 linkage summary baseline：

1. commit：`b921361e4c6a8ae71728bf39a77e4475dcba10ca`。
2. tag：`phase-2.27f-review-audit-linkage-baseline`。
3. `main` 与 `origin/main` 已对齐。
4. 已具备只读 linkage summary runner。
5. 已覆盖临时目录 fake inputs smoke。
6. 已关闭 audit event 顶层 unsafe 字段漏检。
7. 输出保持 `dry_run=true`、`destructive_actions=[]`、`executable=false`、`repair_executed=false`。

Phase 2.27f 当前能力只证明 archive / review / audit 三者可被安全地做只读关联诊断，不代表 repair 已执行，也不代表 readiness audit 默认需要扫描真实 reports / reviews。

## 2. 规划问题

本轮评审 linkage summary 下一步是否应显式参数化接入 readiness audit。

目标不是继续追加 2.27 子阶段，而是为 Phase 2.29 MVP readiness freeze 形成清晰边界：

1. 什么可以作为 readiness 人工验收输入。
2. 什么可以后续通过显式参数接入。
3. 什么不应默认扫描或自动修复。

## 3. 候选方向评审

### A. 保持独立脚本，不接入 readiness audit

结论：可作为默认安全状态保留，但不是最终最优。

优点：

1. 风险最低。
2. 不读取真实 reports / reviews。
3. 不影响现有 readiness audit 行为。
4. 不增加未使用 review workflow 环境的噪声。

缺点：

1. readiness audit 无法统一展示 review linkage 状态。
2. 人工验收需要额外记住运行 linkage 脚本。

适用：作为当前默认状态继续保留。

### B. 显式参数化接入 readiness audit

结论：推荐作为后续最小实现候选，但不在本轮实现。

建议形态：

1. 增加显式参数，例如 `--review-linkage-summary <path>`。
2. 只有用户传入 linkage summary 文件时才检查。
3. readiness audit 读取 summary 后只输出 pass / warn / fail 与少量安全计数。
4. 不读取真实 `reports/` / `reviews/` 目录。
5. 不扫描 audit_logs 大量记录。
6. 不输出本机路径、notes、reason、approved_action、完整 item_decisions 或 item-level entity details。

优点：

1. 与 readiness audit 主入口形成轻量衔接。
2. 保持 opt-in，不影响未使用 review workflow 的环境。
3. 适合纳入 Phase 2.29 MVP readiness freeze 的 checklist。

风险：

1. 如果参数设计不清，可能被误解为默认扫描。
2. 若直接读取原始 report/review 文件，可能泄露本机路径或业务实体。

控制方式：

1. 只读取 linkage summary，不读取原始 review / report。
2. linkage summary 继续由 Phase 2.27f runner 生成。
3. 缺失参数时不检查、不 fail。

### C. 默认扫描 reports / reviews / audit records

结论：不推荐。

原因：

1. 真实 reports / reviews 目录可能包含本机路径、人工 notes、reason、item decisions。
2. 未启用 review workflow 的环境会产生无意义 warning。
3. 自动扫描 audit records 容易扩大 DB 读取范围。
4. 与 Phase 2.27f 的只读、fake-input-first 边界冲突。

### D. 纳入 Phase 2.29 MVP readiness freeze 人工验收清单

结论：推荐。

建议：

1. 在 Phase 2.29 中把 linkage summary 作为人工 readiness checklist 项。
2. 验收时可要求人工提供一份 sanitized linkage summary。
3. 检查重点：
   - archive / review hash 是否能对齐。
   - review / audit trace 是否能对齐。
   - 是否存在 unsafe payload。
   - `repair_executed=false` 是否稳定。
4. 不要求 Phase 2.29 默认读取真实 reports / reviews。

优点：

1. 能体现治理链路闭环证据。
2. 不扩大代码改动面。
3. 适合 Phase 2.29 做 MVP readiness freeze，而不是继续无限延长 2.27x。

### E. 直接进入 repair executor 或 rollout

结论：禁止。

原因：

1. linkage summary 只是只读诊断。
2. review approval 不等于 executed。
3. 当前没有自动 repair 的人工确认、回滚、安全验证链路。
4. rollout readiness 仍需单独阶段冻结与验收。

## 4. 推荐路线

推荐 B + D：

1. 短期保持 Phase 2.27f runner 独立。
2. Phase 2.29 MVP readiness freeze 中把 linkage summary 纳入人工验收清单。
3. 若后续需要代码衔接，只做显式参数化读取 linkage summary。
4. 不默认扫描 `reports/` / `reviews/`。
5. 不读取真实 report / review 原文。
6. 不进入 repair executor。

不建议继续追加新的 Phase 2.27x 实现，除非 Codex B 明确认为 Phase 2.29 freeze 前必须补一个极小参数化入口。

## 5. 是否进入实现

当前不建议立即实现。

原因：

1. Phase 2.27f 已完成只读 linkage summary。
2. 当前最重要的是结束 2.27 审计链路扩张，进入 Phase 2.29 readiness freeze planning。
3. 显式参数化接入 readiness audit 可作为 Phase 2.29 checklist 的候选补丁，而不是 2.27 继续扩展。

若必须实现，边界必须限定为：

1. readiness audit 新增显式参数。
2. 仅读取 linkage summary JSON。
3. 缺参时不检查、不 fail。
4. 不读取真实 reports / reviews。
5. 不写 DB、不写 audit_logs。

## 6. 与 Phase 2.29 的关系

Phase 2.27g 建议作为 2.27 审计链路的路线裁决收口。

Phase 2.29 建议定位为 MVP readiness freeze planning：

1. 汇总 Phase 2.10-2.27 的能力基线。
2. 明确哪些能力进入 MVP freeze checklist。
3. 把 linkage summary 作为人工验收项之一。
4. 确认 readiness audit、repair plan、review record、audit payload、linkage summary 的非破坏性证据链。
5. 明确仍不进入 production rollout。

## 7. 非目标与硬边界

本阶段不做：

1. 功能代码实现。
2. 修改 `scripts/phase225_readiness_audit.py`。
3. 修改 `scripts/phase227f_review_audit_linkage.py`。
4. 写 `audit_logs`。
5. 写业务 DB。
6. 修改 facts。
7. 修改 document_versions。
8. 修改 OpenSearch / Qdrant。
9. 读取真实 reports / reviews 业务内容。
10. 默认扫描本机 reports / reviews 目录。
11. repair / backfill / reindex / cleanup / delete。
12. rollout。
13. repair executor。
14. retrieval contract 或 memory kernel 主架构修改。

## 8. 当前结论

Phase 2.27g 路线规划结论：

1. 推荐把 linkage summary 作为 Phase 2.29 readiness freeze 的人工验收项。
2. 不推荐继续默认扫描真实 reports / reviews。
3. 不推荐进入 repair executor 或 rollout。
4. 不建议本轮进入实现。
5. 下一步建议完成 Phase 2.27g planning baseline 后进入 Phase 2.29 MVP readiness freeze planning。
