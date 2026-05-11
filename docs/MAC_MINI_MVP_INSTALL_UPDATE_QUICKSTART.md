# Mac mini MVP Install / Update Quickstart

## 1. 用途

这份 quickstart 给 Mac mini operator / Mac mini Codex 使用，用于安装、更新和回滚 Hermes 内部受控 MVP。

这不是 production rollout，不授权真实 DB smoke、NAS scan、repair、cleanup、backfill、reindex、delete、migration 或 Data Steward feature activation。

## 2. 推荐目录

```text
/Users/hermes/code/Hermes_memory
/Users/hermes/code/hermes-agent
/Users/hermes/env
/Users/hermes/reports
```

`/Users/hermes/env` 用于保存本机 `.env` 备份或模板说明，不能提交 Git。

## 3. 当前建议安装 Ref

| repo | ref | 结论 |
|---|---|---|
| Hermes_memory | `phase-2.64b-data-steward-selective-integration-baseline` | 可用于安装规划 |
| hermes-agent | `phase-2.56e-natural-import-real-upload-smoke-baseline` | 可用于安装规划 |

如果缺少 hermes-agent reviewed ref，必须暂停，不能猜测 branch、tag 或 commit。

## 4. 安装前检查

在 Mac mini 上先检查：

```bash
sw_vers
whoami
git --version
uv --version
docker --version
df -h /Users/hermes
```

检查目录：

```bash
mkdir -p /Users/hermes/code /Users/hermes/env /Users/hermes/reports
ls -ld /Users/hermes/code /Users/hermes/env /Users/hermes/reports
```

检查 `.env` 必要 key 是否存在，但不要输出值：

```text
DATABASE_URL
OPENSEARCH_URL
QDRANT_URL
QDRANT_COLLECTION
ALIYUN_EMBEDDING_API_KEY
```

可选：

```text
ALIYUN_RERANK_API_KEY
```

## 5. Release Manifest

在开发机或 Mac mini 上可生成只读 manifest：

```bash
cd /Users/hermes/code/Hermes_memory
uv run python scripts/phase265_mvp_release_manifest.py \
  --hermes-memory-ref phase-2.64b-data-steward-selective-integration-baseline \
  --hermes-agent-ref phase-2.56e-natural-import-real-upload-smoke-baseline \
  --operator mac-mini
```

如果需要保存，必须显式传入本地 ignored 路径：

```bash
uv run python scripts/phase265_mvp_release_manifest.py \
  --hermes-memory-ref phase-2.64b-data-steward-selective-integration-baseline \
  --hermes-agent-ref <reviewed-hermes-agent-ref> \
  --operator mac-mini \
  --output-json /Users/hermes/reports/release_manifest.json
```

该 helper 不读取 `.env`，不输出 secret，不启动服务，不执行 git pull，不修改仓库状态。

## 6. 安装流程

只有 reviewed refs 明确后才能执行。

```bash
cd /Users/hermes/code
git clone <Hermes_memory_repo_url> Hermes_memory
git clone <hermes_agent_repo_url> hermes-agent

cd /Users/hermes/code/Hermes_memory
git fetch origin --tags
git checkout phase-2.64b-data-steward-selective-integration-baseline
git status --short

cd /Users/hermes/code/hermes-agent
git fetch --all --tags
git checkout phase-2.56e-natural-import-real-upload-smoke-baseline
git status --short
```

如果任一 worktree dirty，停止。

## 7. 启动后检查

```bash
cd /Users/hermes/code/Hermes_memory
docker compose ps
curl http://127.0.0.1:8000/health

cd /Users/hermes/code/hermes-agent
hermes chat --help
```

只有 `/health` 和 `hermes chat --help` 通过，才可进入后续内部 MVP smoke。

## 8. 更新流程

```bash
cd /Users/hermes/code/Hermes_memory
git status --short
git fetch origin --tags
git checkout <reviewed-hermes-memory-ref>

cd /Users/hermes/code/hermes-agent
git status --short
git fetch --all --tags
git checkout <reviewed-hermes-agent-ref>
```

更新后检查：

```bash
cd /Users/hermes/code/Hermes_memory
docker compose ps
curl http://127.0.0.1:8000/health

cd /Users/hermes/code/hermes-agent
hermes chat --help
```

## 9. 回滚流程

回滚只能回到 previous known-good reviewed tag / commit。

```bash
cd /Users/hermes/code/Hermes_memory
git checkout <previous-known-good-hermes-memory-ref>

cd /Users/hermes/code/hermes-agent
git checkout <previous-known-good-hermes-agent-ref>
```

回滚后必须重新执行 health smoke。

## 10. 禁止事项

1. 不进入 production rollout。
2. 不执行 repair / cleanup / backfill / reindex / delete / migration。
3. 不执行真实 DB smoke。
4. 不扫描 NAS。
5. 不启用 Data Steward feature。
6. 不在 Mac mini 上手改业务代码。
7. 不输出 secret、token 或 `.env` 真值。
