# Codex Mac mini 安装与 Git 更新 Prompt

## 1. 用法说明

这份文档给 Mac mini 上的 Codex 使用。

目标：

1. 在新的 Mac mini 上安装当前 Hermes 最小可用版。
2. 安装后可通过 Git 拉取远端最新代码并完成受控更新。
3. 整个流程尽量不改业务代码，只做部署、配置、启动、校验。

边界：

1. 这是内部受控 MVP，不是 production rollout。
2. 不允许自动执行 repair、cleanup、backfill、reindex、delete。
3. 不允许暴露 `.env` 真值、密钥或令牌到聊天输出。
4. 不允许在 Mac mini 上直接手改业务代码来“修部署”。
5. 遇到 dirty worktree、migration 不明确、secret 缺失、repo URL 不明、权限不足时必须停止并汇报。

推荐目录：

```text
/Users/hermes/code/Hermes_memory
/Users/hermes/code/hermes-agent
/Users/hermes/env
```

---

## 2. 安装 Prompt

把下面整段发给 Mac mini 上的 Codex：

```text
你现在在一台新的 Mac mini 上，目标是安装我们当前的 Hermes 内部受控 MVP，并做到后续可以通过 Git 在线更新。

你必须严格按下面规则执行：

一、目标
1. 安装两个仓库：
   - Hermes_memory
   - hermes-agent
2. 让 Hermes_memory 后端服务可运行。
3. 让 hermes-agent CLI 可运行，并正确接到本机的 Hermes_memory。
4. 最后做最小 smoke check。

二、绝对边界
1. 不要修改业务代码来规避部署问题。
2. 不要暴露任何 secret、token、.env 真值到聊天输出。
3. 不要执行 repair、cleanup、backfill、reindex、delete、destructive migration。
4. 不要假装成功；任何失败都必须明确报告。
5. 遇到以下情况必须暂停并汇报，不要继续硬做：
   - repo URL、branch、tag、commit 不明确
   - 本机已有同路径仓库且 worktree dirty
   - 缺少 Docker、uv、git 或权限
   - 需要新 secret 但未提供
   - 发现需要执行不明确 migration

三、默认安装路径
1. /Users/hermes/code/Hermes_memory
2. /Users/hermes/code/hermes-agent
3. /Users/hermes/env

四、你先做 preflight，再安装，不要跳步
按顺序执行：

Step 1. 机器与依赖检查
- 检查并报告：
  - macOS 基本信息
  - 当前用户
  - git 是否可用
  - uv 是否可用
  - docker 是否可用
  - 磁盘空间是否足够
- 检查目标目录是否已存在
- 如果目录不存在，创建：
  - /Users/hermes/code
  - /Users/hermes/env

Step 2. 仓库检查与拉取
- 如果仓库不存在：
  - clone Hermes_memory 到 /Users/hermes/code/Hermes_memory
  - clone hermes-agent 到 /Users/hermes/code/hermes-agent
- 如果仓库已存在：
  - 先检查 git status 是否干净
  - 只有 worktree 干净时才允许继续 pull/fetch
  - 如果不干净，停止并汇报具体文件
- 明确记录并汇报：
  - 当前 branch
  - 当前 commit
  - 如果提供了 tag/branch/commit，必须 checkout 到指定版本

Step 3. Hermes_memory 环境文件
- 以 Hermes_memory/.env.example 为模板
- 创建 Hermes_memory 仓库根目录 .env
- 同时在 /Users/hermes/env/ 下保存一份外部 env 备份
- 不要在聊天里输出 secret 真值
- 必须重点检查这些 key 是否存在：
  - DATABASE_URL
  - OPENSEARCH_URL
  - QDRANT_URL
  - QDRANT_COLLECTION
  - ALIYUN_EMBEDDING_API_KEY
  - 可选 ALIYUN_RERANK_API_KEY
- 如果缺少必要 secret，就停止并汇报缺哪个 key，不要伪造

Step 4. 启动 Hermes_memory
- 进入 /Users/hermes/code/Hermes_memory
- 用 docker compose 启动服务
- 优先使用仓库自带 docker-compose.yml
- 启动后检查：
  - docker compose ps
  - http://127.0.0.1:8000/health
- 只有 health 成功才进入下一步

Step 5. 安装 hermes-agent
- 进入 /Users/hermes/code/hermes-agent
- 优先按仓库 README 的推荐方式安装
- 如果仓库中 setup-hermes.sh 可用，优先使用它
- 如果不用 setup-hermes.sh，则使用仓库自身推荐的 uv/venv 安装方式
- 必须确保命令可用：
  - hermes chat --help

Step 6. 将 hermes-agent 接到 Hermes_memory
- 为当前 shell 或受控启动方式设置：
  - HERMES_MEMORY_KERNEL_ENABLED=1
  - HERMES_MEMORY_PATH=/Users/hermes/code/Hermes_memory
- 确认 hermes-agent 使用的是本机这个 Hermes_memory 路径

Step 7. 最小 smoke check
- 执行并汇报：
  - curl http://127.0.0.1:8000/health
  - hermes chat --help
- 如果当前机器上已有测试文件和既有会话能力，再补充说明是否已具备 alias/session 使用条件
- 不要擅自上传真实业务文件
- 不要擅自写 DB、facts、OpenSearch、Qdrant 测试数据，除非本地已经有现成数据且是只读验证

五、输出格式
按下面结构汇报，简洁但完整：

1. Preflight
- git:
- uv:
- docker:
- 目录状态:

2. Repo
- Hermes_memory: branch / commit / status
- hermes-agent: branch / commit / status

3. Env
- 已检查 key:
- 缺失 key:
- 是否因 secret 缺失暂停:

4. Runtime
- docker compose:
- /health:
- hermes chat --help:

5. Decision
- Go / Pause / No-Go
- 原因
- 下一步建议

六、如果一切成功
请额外给出后续 Git 更新的精确执行建议，但不要现在执行更新。
```

---

## 3. 更新 Prompt

当 Mac mini 已经装好，只想同步到 Git 最新版本时，把下面整段发给 Mac mini 上的 Codex：

```text
你现在在已经部署好的 Mac mini 上，目标是把 Hermes 内部受控 MVP 更新到 Git 远端最新版本，但必须确保过程可回滚、可验证、不过度自动化。

你必须严格按下面规则执行：

一、目标
1. 更新两个仓库：
   - /Users/hermes/code/Hermes_memory
   - /Users/hermes/code/hermes-agent
2. 同步到指定 branch 的最新远端提交，或指定 tag/commit。
3. 重启必要服务。
4. 做最小 health / CLI 校验。

二、绝对边界
1. 不要在本机手改业务代码。
2. 不要用 destructive git 命令：
   - 不要 git reset --hard
   - 不要 git checkout -- 覆盖用户改动
3. 如果 worktree 不干净，立即停止并汇报。
4. 如果更新后发现需要不明确 migration，立即停止并汇报。
5. 不要泄露 secret。
6. 不要执行 repair、cleanup、backfill、reindex、delete。

三、更新步骤

Step 1. 仓库状态检查
- 分别进入两个仓库
- 执行 git status --short
- 执行 git branch --show-current
- 执行 git rev-parse HEAD
- 如果任一仓库 dirty，停止并汇报，不允许 pull

Step 2. 获取远端最新代码
- 对两个仓库执行 git fetch --all --tags
- 如果用户指定 branch：
  - checkout 到该 branch
  - git pull --ff-only
- 如果用户指定 tag/commit：
  - checkout 到指定 ref
- 汇报更新前后 commit

Step 3. 依赖与配置检查
- 检查 Hermes_memory 的：
  - pyproject.toml
  - uv.lock
  - docker-compose.yml
  - .env 是否仍存在
- 检查 hermes-agent 的：
  - pyproject.toml
  - uv.lock
  - setup-hermes.sh 或既有安装方式
- 如果依赖文件变化，按仓库推荐方式刷新依赖
- 但不要改动 secret 内容

Step 4. 重启服务
- 进入 /Users/hermes/code/Hermes_memory
- 重启 Hermes_memory 相关服务
- 推荐使用 docker compose up -d --build
- 如果 hermes-agent 需要重新安装或刷新环境，按仓库推荐方式处理

Step 5. 最小校验
- curl http://127.0.0.1:8000/health
- hermes chat --help
- 汇报：
  - 更新前 commit
  - 更新后 commit
  - /health 结果
  - CLI 结果

四、停止条件
只要出现任一情况就 Pause：
1. git worktree 不干净
2. pull 不是 fast-forward
3. 依赖刷新失败
4. /health 失败
5. hermes chat --help 失败
6. 发现需要额外 migration 但未被明确授权

五、输出格式
1. Before
- Hermes_memory: branch / commit / dirty?
- hermes-agent: branch / commit / dirty?

2. Update
- fetch:
- pull/checkout:
- dependency refresh:

3. After
- Hermes_memory: new commit
- hermes-agent: new commit
- /health:
- hermes chat --help:

4. Decision
- Go / Pause / No-Go
- 原因
- 如果失败，停在什么步骤
```

---

## 4. 这件事是否可行

可以，但要满足下面几个条件：

1. 测试机上的两个仓库必须保持“只通过 Git 更新”，不要在本机手改业务代码。
2. `.env` 和 secret 要放在 Git 外部受控管理，更新时只复用，不要每次重建。
3. 更新流程必须坚持：
   - `git fetch --all --tags`
   - `git pull --ff-only`
   - 重启服务
   - 跑最小 smoke
4. 如果未来某次版本引入了数据库 migration、额外 secret、新服务或目录结构变化，就不能保证“零干预 update”。

最适合你们现在的方式是：

1. 先把这次安装做成一台干净的 Mac mini 基线。
2. 后续所有更新都走：
   - 开发机验证
   - push 到远端
   - Mac mini 上的 Codex 执行上面的“更新 Prompt”

---

## 5. 当前最推荐的运维口径

不是“Mac mini 上直接开发”，而是：

1. 开发机开发。
2. Git push。
3. Mac mini 上 Codex 只负责：
   - pull
   - restart
   - health check
   - smoke check

这样最稳，也最接近你说的“直接在 Mac mini 中 update 就可以更新到推送的最新版本”。

