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

## 4. Git 策略

可提交为协作基线：

1. `docs/AGENT_OPERATING_PROTOCOL.md`。
2. `docs/ACTIVE_PHASE.md`。
3. `docs/HANDOFF_LOG.md`。
4. `docs/PHASE_BACKLOG.md`。
5. 必要的 reports / agent_runs README 或 `.gitignore`。

不得提交：

1. `reports/agent_runs/latest.json`。
2. 真实 agent run JSON。
3. 真实 report JSON。
4. 真实 review record JSON / Markdown。

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

## 6. Overnight Sprint 规则

1. 每个 autonomous sprint 最多 60-120 分钟。
2. 每轮只能完成一个 phase 子任务。
3. planning / implementation / validation / baseline 必须分阶段。
4. 遇到硬停止条件必须停下并写交接文件。
5. 不得连续跨多个 phase 自动推进。
6. baseline 前必须等待 Codex B 审核，除非用户明确授权。

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
