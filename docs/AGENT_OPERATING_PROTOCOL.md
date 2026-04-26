# Agent Operating Protocol

## 1. 目的

本协议用于 Hermes_memory / Hermes 主仓库的 Codex 多会话协作。

目标是减少人工复制 Codex A / Codex B / Codex C 会话内容，让阶段状态、下一步建议和风险判断落到固定文件中。

该协议不改变 PRD、ROADMAP、TECHNICAL_DESIGN、retrieval contract 或 memory kernel 主架构。

## 2. 角色职责

### 2.1 Codex A

Codex A 是主实现 agent。

职责：

1. 按 Phase 推进开发。
2. 每轮只推进一个 bounded phase 或一个明确 phase 子任务。
3. 严格对齐 PRD、ROADMAP、TECHNICAL_DESIGN、TODO、DEV_LOG、ACTIVE_PHASE 和 PHASE_BACKLOG。
4. 不擅自扩大范围。
5. 不进入 rollout，除非 Phase 文档明确要求。
6. 不执行 destructive repair，除非经过单独 Phase 规划、人工确认和显式指令。

每轮开始必须读取：

1. `docs/PRD.md`。
2. `docs/ROADMAP.md`。
3. `docs/TECHNICAL_DESIGN.md`。
4. `docs/TODO.md`。
5. `docs/DEV_LOG.md`。
6. `docs/ACTIVE_PHASE.md`。
7. `docs/PHASE_BACKLOG.md`。

如果涉及 Hermes 主仓库，也必须读取：

1. `/Users/Weishengsu/.hermes/hermes-agent/docs/TODO.md`。
2. `/Users/Weishengsu/.hermes/hermes-agent/docs/DEV_LOG.md`。

每轮结束必须更新：

1. `docs/ACTIVE_PHASE.md`。
2. `docs/HANDOFF_LOG.md`。
3. `reports/agent_runs/latest.json`。

### 2.2 Codex B

Codex B 是监督、审查、路线裁决与 prompt 生成 agent。

职责：

1. 读取 `ACTIVE_PHASE.md`、`HANDOFF_LOG.md`、`reports/agent_runs/latest.json`。
2. 判断 Codex A 是否偏离 PRD、ROADMAP、TECHNICAL_DESIGN 或当前 Phase 文档。
3. 给用户和 Codex A 生成下一轮 bounded prompt。
4. 必要时做 review 或小范围修复。
5. 标记是否需要重新规划、是否需要 Codex C 验收。

Codex B 默认不承担主实现工作。

### 2.3 Codex C

Codex C 是真实终端验收与 live smoke agent。

职责：

1. 真实 Hermes CLI / API / 终端验证。
2. live smoke。
3. 验证用户侧行为是否符合 Phase 验收标准。
4. 回传具体成功 / 失败证据。

Codex C 默认不做主实现，除非用户明确要求。

## 3. 文件语义

### 3.1 `docs/ACTIVE_PHASE.md`

当前 phase 状态文件，允许每轮覆盖更新。

必须包含：

1. 当前 phase。
2. 本轮目标。
3. 修改文件。
4. 完成内容。
5. 测试结果。
6. live smoke 结果。
7. 当前结论。
8. 阻塞点 / 风险点。
9. 是否建议 baseline。
10. 是否建议进入下一阶段。
11. 下一轮建议。
12. 是否需要 Codex B 审核。
13. 是否需要 Codex C 真实终端验收。

### 3.2 `docs/HANDOFF_LOG.md`

追加式交接日志，不覆盖历史。

每轮追加格式：

```md
## YYYY-MM-DD HH:mm Phase X
- goal:
- changed_files:
- tests:
- validation:
- risks:
- next:
- commit/tag if any:
```

### 3.3 `docs/PHASE_BACKLOG.md`

当前优先级与永久边界。

用于告诉下一轮 Codex A：

1. 当前最重要的 1-3 个候选方向。
2. 哪些事项后置。
3. 哪些边界永久有效。

### 3.4 `reports/agent_runs/latest.json`

本地运行状态文件，默认 ignored，不提交 Git。

字段：

```json
{
  "phase": "",
  "status": "planning|implemented|validated|baseline|blocked",
  "changed_files": [],
  "tests": [],
  "live_smoke": [],
  "risks": [],
  "next_recommendation": "",
  "needs_codex_b_review": true,
  "needs_codex_c_validation": false,
  "git": {
    "commit": "",
    "tag": "",
    "pushed": false
  }
}
```

`reports/agent_runs/` 可作为本地状态目录，不提交真实运行 JSON。

### 3.5 `docs/NEXT_CODEX_A_PROMPT.md`

Codex A 的下一轮固定任务入口文件。

当用户说“执行 `docs/NEXT_CODEX_A_PROMPT.md`”或给出该文件绝对路径时，Codex A 必须：

1. 读取该文件完整内容。
2. 按该文件中的 phase 目标、边界、测试和文档同步要求执行。
3. 不依赖聊天窗口中的长 prompt 作为唯一任务来源。
4. 若该文件与聊天最新指令冲突，以用户最新显式指令为准，并在 `ACTIVE_PHASE.md` 中记录偏差。

`NEXT_CODEX_A_PROMPT.md` 可提交为协作入口基线；它不应包含密钥、真实敏感数据或本地运行产物。

### 3.6 `docs/NIGHTLY_SPRINT_PROTOCOL.md`

Codex A 夜间 bounded autonomous sprint 规则文件。

用于定义：

1. 每晚最多执行多少 queue item。
2. Green / Yellow / Red Lane。
3. 夜间硬停止条件。
4. 每个 sprint 必须写入的交接文件。
5. 早晨 Codex B 审核流程。

### 3.7 `docs/NIGHTLY_SPRINT_QUEUE.md`

Codex A 夜间 queue 文件。

每个 queue item 必须包含：

1. 类型：Green / Yellow / Red Lane。
2. 目标。
3. 允许动作。
4. 禁止动作。
5. 完成后的停止或交接要求。

Codex A 不得在夜间执行未列入 queue 的任务。

### 3.8 `reports/nightly_runs/*.json`

Codex A 夜间运行状态文件，默认 ignored，不提交 Git。

每个 sprint 结束可写入一份本地 JSON，记录 sprint_id、queue_item、start/end time、changed_files、tests、status、stop_reason 与 git status。

## 4. Git 策略

可提交为协作基线：

1. `docs/AGENT_OPERATING_PROTOCOL.md`。
2. `docs/ACTIVE_PHASE.md`。
3. `docs/HANDOFF_LOG.md`。
4. `docs/PHASE_BACKLOG.md`。
5. `docs/NEXT_CODEX_A_PROMPT.md`。
6. `docs/NIGHTLY_SPRINT_PROTOCOL.md`。
7. `docs/NIGHTLY_SPRINT_QUEUE.md`。
8. 必要的 reports / agent_runs / nightly_runs README 或 `.gitignore`。

不得提交：

1. `reports/agent_runs/latest.json`。
2. 真实 agent run JSON。
3. 真实 nightly run JSON。
4. 真实 report JSON。
5. 真实 review record JSON / Markdown。

baseline 前必须：

1. 测试通过。
2. 文档同步。
3. dirty 白名单复核。
4. 不混入无关文件。

## 5. 硬停止条件

遇到以下情况必须停止，不得继续实现：

1. 需要修改真实业务数据。
2. 需要执行 repair / delete / cleanup / migration。
3. 需要进入 rollout。
4. 需要新增权限模型或修改 retrieval contract。
5. 需要修改 memory kernel 主架构。
6. 测试失败超过 2 轮仍无法定位。
7. dirty 文件超出本 phase 范围。
8. 需要用户提供样本、密钥、真实终端结果。
9. 涉及自动 facts 抽取或 facts 替代 retrieval evidence。
10. 涉及生产 cron / 定时任务。
11. Codex B 标记为需要重新规划。

## 6. Nightly Sprint 规则

1. 每个 sprint 最长 60-120 分钟。
2. 每晚最多执行 1-3 个 queue item。
3. 每个 queue item 必须是 bounded task。
4. 不得跨多个大 phase 连续推进。
5. 每个 sprint 结束必须更新 ACTIVE_PHASE、HANDOFF_LOG、reports/agent_runs/latest.json 和 reports/nightly_runs/<timestamp>.json。
6. 遇到硬停止条件必须停止，不得继续下一个任务。
7. 早上由 Codex B 审核交接结果。

### 6.1 Green Lane

允许夜间自动推进：

1. 文档规划。
2. dry-run 工具。
3. 本地报告归档。
4. preview / sanitized payload。
5. 单元测试。
6. 临时目录 smoke。
7. 不写 DB 的脚本。
8. 不改 retrieval contract 的小工具。

### 6.2 Yellow Lane

完成后必须停止等待 Codex B：

1. 新 API endpoint。
2. `audit_logs` 真实写入。
3. 真实 DB smoke。
4. 多仓库联动。
5. 需要 Codex C 终端验收。
6. baseline / tag / push。

### 6.3 Red Lane

夜间禁止：

1. repair executor。
2. delete / cleanup。
3. migration。
4. production rollout。
5. facts 自动抽取。
6. facts 替代 retrieval evidence。
7. retrieval contract 修改。
8. memory kernel 主架构修改。
9. production cron / scheduler。
10. 真实业务数据 mutation。

### 6.4 早晨审核

Codex B 早晨读取 ACTIVE_PHASE、HANDOFF_LOG、reports/agent_runs/latest.json 与最新 nightly run JSON，判断是否偏离 PRD、是否需要 Codex C 验收、是否允许 baseline。

## 7. 当前默认边界

当前阶段默认不做：

1. repair executor。
2. rollout。
3. retrieval contract rewrite。
4. memory kernel 主架构重构。
5. production cron。
6. facts 自动抽取。
7. facts 替代 retrieval evidence。
8. 真实 review / report / agent run JSON 入 Git。
