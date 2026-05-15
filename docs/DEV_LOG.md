# DEV_LOG

- [Phase 2.87b Codex B Review] Review 通过：`EvidenceOnlyWriter` 只通过 injected test-local SQLAlchemy session 写入 `Document`、`DocumentVersion`、`Chunk`、`CitationRecord`，未增加 API / CLI runtime wiring，未调用 parser、NAS、OpenSearch、Qdrant、MinIO、audit log 或 Agent answer。复跑目标测试 `7 passed`、py_compile 通过、Data Steward regression `133 passed`，`git diff --check`、latest JSON 与 ignore checks 通过。已写入 Phase 2.87b selective Git baseline prompt；真实 DB smoke 与 Phase 2.87c 仍需单独授权。

- [Phase 2.87b Evidence-only Writer Service] 完成首轮 test-local writer implementation：新增 `app/services/asset_catalog/evidence_writer.py`，提供 `EvidenceOnlyWriter`、`EvidenceWriteDecision`、`EvidenceWriteRollbackPlan` 与 `build_evidence_write_result()`；只通过注入 SQLAlchemy session 写入 test-local `Document`、`DocumentVersion`、`Chunk`、`CitationRecord`。实现 fail-closed gates、1 document / 1 version / <=20 chunks 限制、forbidden raw-field 拒绝、idempotency duplicate / conflict 判定与 run-scoped rollback dry-run。TDD RED 已观察；目标测试 `7 passed`；py_compile 通过；Data Steward regression `133 passed`。本轮未接 API / CLI runtime，未运行真实 DB smoke，未写 OpenSearch / Qdrant / MinIO / audit table，未执行 parser / file copy / NAS scan / Agent answer integration / rollout。下一步需要 Codex B review。

- [Phase 2.87b Prompt] Phase 2.87a baseline 已确认：commit `fb7baba`，tag `phase-2.87a-write-target-discovery-baseline`，pushed=true。Codex B 已写入 Phase 2.87b Evidence-only Writer Service Implementation prompt，下一步以 TDD 实现 dedicated evidence-only writer service，只在 test-local DB/session 中验证 `Document`、`DocumentVersion`、`Chunk`、`CitationRecord` 写入边界、approval gates、idempotency 与 rollback dry-run。本轮仍不接 API / CLI runtime、不运行真实 DB smoke、不执行 parser、不复制文件、不扫描 NAS、不写 OpenSearch / Qdrant / MinIO、不接入 Agent answer、不 rollout。

- [Phase 2.87a Codex B Review] Review 通过：`docs/PHASE287A_EXACT_WRITE_TARGET_DISCOVERY.md` 完成 read-only discovery，识别候选 evidence targets：`documents`、`document_versions`、`chunks`、`citations` 与可选 `ingestion_jobs`。确认直接复用 `DocumentIngestionService.ingest_uploaded_file()` 为 No-Go，因为该路径耦合 file bytes、parser/chunker、OpenSearch 与 Qdrant。Direct real write 仍为 `Pause`，后续必须先设计 dedicated evidence-only writer、idempotency metadata location 与 run-scoped rollback / invalidation dry-run。已写入 Phase 2.87a selective docs baseline prompt。

- [Phase 2.87a Exact Write Target Discovery] 完成 docs-only / read-only discovery：新增 `docs/PHASE287A_EXACT_WRITE_TARGET_DISCOVERY.md`，识别候选 DB evidence targets 为 `Document/documents`、`DocumentVersion/document_versions`、`Chunk/chunks`、`CitationRecord/citations`，可选 bookkeeping `IngestionJob/ingestion_jobs`。发现关键阻塞：现有 `DocumentIngestionService.ingest_uploaded_file()` 读取 file bytes、执行 parser/chunker，并会调用 OpenSearch / Qdrant indexer，不适合直接复用为 first real evidence-only smoke；当前 direct real write 仍为 `Pause`。本轮未实现 writer、未执行真实 `documents/chunks/document_versions` 写入、未运行 parser、未复制真实文件、未扫描 NAS、未写 DB/index/object-store、未接入 Agent answer、未 rollout。下一步需要 Codex B review；不得自动进入 Phase 2.87b。

- [Phase 2.87a Prompt] Phase 2.87 baseline 已确认：commit `069fbec`，tag `phase-2.87-first-real-evidence-write-smoke-plan-baseline`，pushed=true。Codex B 已写入 Phase 2.87a Exact Write Target Discovery / Implementation Gate prompt，下一步只做 read-only code discovery 与 docs 记录，定位未来真实 evidence write smoke 的 exact model/table/repository/transaction/rollback boundary。本轮仍不实现 writer、不执行真实写入、不运行 parser、不复制文件、不扫描 NAS、不写 DB/index/object-store、不接入 Agent answer、不 rollout。

- [Phase 2.87 Codex B Review] Review 通过：`docs/PHASE287_FIRST_REAL_EVIDENCE_WRITE_SMOKE_PLAN.md` 保持 docs-only planning，覆盖 tiny scope、later operator approval、exact write target gate、feature flags default off、rollback boundary、sanitized report boundary、Go / Pause / No-Go、DB platform handoff 与 2.87a / 2.88 / 2.89 follow-up split。本轮未实现 writer、未执行真实写入、未运行 parser / copy / DB / index / object-store / Agent answer smoke。已写入 Phase 2.87 selective docs baseline prompt。

- [Phase 2.87 First Real Evidence Write Smoke Planning] 完成 docs-only 规划：新增 `docs/PHASE287_FIRST_REAL_EVIDENCE_WRITE_SMOKE_PLAN.md`，定义未来 Mac mini / 测试机第一次真实 Hermes evidence write smoke 的安全门槛。规划固定 tiny scope（最多 1 source asset、1 document version、20 chunks）、operator approval JSON、feature flags default off、exact write target gate、rollback boundary、sanitized report boundary、Go / Pause / No-Go、DB platform handoff 与 2.87a / 2.88 / 2.89 follow-up split。本轮未实现 writer、未执行真实 `documents/chunks/document_versions` 写入、未运行 parser、未复制真实文件、未扫描 NAS、未写 DB/index/object-store、未接入 Agent answer、未 rollout。下一步需要 Codex B review；不得自动进入 Phase 2.87a。

- [Phase 2.87 Prompt] Phase 2.86a baseline 已确认：commit `c5372fc`，tag `phase-2.86a-evidence-write-rehearsal-baseline`，pushed=true。Codex B 已写入 Phase 2.87 First Real Hermes Evidence Write Smoke Planning prompt，下一步只规划未来 Mac mini / 测试机第一次真实 Hermes evidence write smoke 的 tiny scope、operator approval、feature flags、exact write targets、rollback boundary、sanitized report 与 Go / Pause / No-Go。本轮仍不实现 writer、不执行真实 `documents/chunks/document_versions` 写入、不运行 parser、不复制真实文件、不扫描 NAS、不写 DB/index/object-store、不接入 Agent answer、不 rollout。

- [Phase 2.86a Codex B Review] Review 通过：temp evidence write rehearsal implementation 只使用 in-memory / temp SQLite repository，覆盖 temp-only document / version / chunk / citation insert ordering、duplicate detection、idempotency conflict、rollback dry-run 与 sanitized CLI summary。复跑验证通过：target tests `7 passed`，py_compile 通过，Data Steward regression `126 passed`，`git diff --check`、latest JSON 和 ignore checks 通过。本轮未写真实 `documents/chunks/document_versions` / DB / OpenSearch / Qdrant / MinIO，未执行 parser，未复制真实文件，未扫描 NAS，未接入 Agent answer，未 rollout。已写入 Phase 2.86a selective Git baseline prompt。

- [Phase 2.86a Temp Evidence Write Rehearsal] 完成首轮最小实现：新增 `app/services/asset_catalog/evidence_write_rehearsal.py`、`scripts/phase286a_temp_evidence_write_rehearsal.py`、target tests、ignored `reports/nas_evidence_write_rehearsal/` 与 Phase 2.86a docs。Runner 从 ignored local `nas_evidence_write_dry_run.v0` report 生成 ignored local `nas_evidence_write_rehearsal.v0` report，使用 in-memory / temp SQLite repository rehearsal，覆盖 document / version / chunk / citation write ordering、duplicate idempotency detection、idempotency conflict no-go、rollback dry-run 与 sanitized CLI summary。TDD RED 已观察到 missing module / CLI；target tests `7 passed`；py_compile 通过；Data Steward regression `126 passed`；CLI `/tmp` smoke 输出 `rehearsal_go` 且所有 real write flags false。本轮未写真实 Hermes DB / platform DB / OpenSearch / Qdrant / MinIO，未执行 parser，未复制真实文件，未读取 raw content，未扫描 NAS，未接入 Agent answer，未进入 rollout。

- [Phase 2.86a Prompt] Phase 2.86 baseline 已完成：commit `8455d4a`，tag `phase-2.86-controlled-real-evidence-write-plan-baseline`。Codex B 已写入 Phase 2.86a Temp Evidence Write Rehearsal Implementation prompt，下一步实现 local temp SQLite / in-memory repository rehearsal：从 ignored local `nas_evidence_write_dry_run.v0` report 生成 ignored local `nas_evidence_write_rehearsal.v0` report，验证写入顺序、idempotency、rollback dry-run 与 sanitized CLI summary。本轮仍不写真实 `documents/chunks` / DB / OpenSearch / Qdrant / MinIO、不执行 parser、不复制真实文件、不扫描 NAS、不接入 Agent answer、不 rollout。

- [Phase 2.86 Codex B Review] Review 通过：`docs/PHASE286_CONTROLLED_REAL_EVIDENCE_WRITE_PLAN.md` 保持 docs-only planning，明确 future first real write smoke 必须 test-machine-only、小批、operator-approved，并保留 feature flags default off、exact write target、rollback dry-run、citation metadata、Go / Pause / No-Go 与后续 phase split。本轮未实现 writer、未写 `documents/chunks` / DB / OpenSearch / Qdrant / MinIO、未执行 parser、未复制真实文件、未扫描 NAS、未接入 Agent answer、未 rollout。已写入 Phase 2.86 selective docs baseline prompt。

- [Phase 2.86 Controlled Real Evidence Write Planning] 完成 docs-only 规划：新增 `docs/PHASE286_CONTROLLED_REAL_EVIDENCE_WRITE_PLAN.md`，明确 future first real Hermes evidence write smoke 只能在 test-machine tiny scope 下进行，建议上限为 1 source asset、1 document version、20 chunks；规划覆盖 permission proof、operator approval、feature flags default off、write target boundary、citation metadata、idempotency、locks、rollback dry-run 与 Go / Pause / No-Go。本轮未实现 writer，未执行真实写入，未写 `documents/chunks` / DB / OpenSearch / Qdrant / MinIO，未执行 parser，未复制真实文件，未读取 raw content，未扫描 NAS，未接入 Agent answer，未进入 rollout。下一步需要 Codex B review 后再决定 docs-only baseline。

- [Phase 2.86 Prompt] Phase 2.85a baseline 已完成：commit `380e7a0`，tag `phase-2.85a-evidence-write-dry-run-baseline`。Codex B 已写入 Phase 2.86 Controlled Small-batch Real Hermes Evidence Write Planning prompt，下一步只规划 future test-machine controlled real evidence write smoke 的权限证明、operator approval、feature flags、write target boundary、citation metadata、idempotency、locks、rollback dry-run 与 Go / Pause / No-Go。本轮仍不实现 writer、不写 `documents/chunks` / DB / OpenSearch / Qdrant / MinIO、不执行 parser、不复制真实文件、不读 raw text、不扫描 NAS、不接入 Agent final answer、不 rollout。

- [Phase 2.85a Local Evidence Write Dry-run Runner] 完成最小实现：新增 `app/services/asset_catalog/evidence_write_dry_run.py`、`scripts/phase285a_evidence_write_dry_run.py`、target tests、ignored `reports/nas_evidence_write_dry_run/` 与 Phase 2.85a docs。Runner 从 ignored local preflight report 生成 ignored local `nas_evidence_write_dry_run.v0` report，覆盖 ready / not allowed / no-go、forbidden input keys、deterministic refs、duplicate idempotency detection、same-run rollback dry-run 与 sanitized CLI summary。TDD RED 已观察到 missing module / CLI；target tests `8 passed`。本轮未写 `documents/chunks` / DB / OpenSearch / Qdrant / MinIO，未运行 parser，未复制真实文件，未读取 raw content，未扫描 NAS，未接入 Agent answer，未进入 rollout。

- [Phase 2.84 Controlled Evidence Write Preflight Planning] 完成 controlled evidence write preflight 规划：新增 `docs/PHASE284_CONTROLLED_EVIDENCE_WRITE_PREFLIGHT_PLAN.md`，定义未来真正接近写入前必须满足的 operator approval、write scope、idempotency、rollback、citation coverage、locks 与 decision states。Review 结论：preflight contract 仍是 planning artifact，不是 write authorization；本轮不实现 preflight runner、不生成 preflight artifact、不写 DB / `documents/chunks` / OpenSearch / Qdrant / MinIO、不执行 parser、不复制真实文件、不读 raw text、不接入 Agent final answer、不 rollout。已写入 selective docs baseline prompt。

- [Phase 2.83a Evidence Write Payload Dry-run] 完成最小实现：新增 `app/services/asset_catalog/evidence_payload.py` 与 `scripts/phase283a_evidence_write_payload.py`，从 ignored local eligibility report 生成 `nas_evidence_write_payload.v0` dry-run payload plan；新增 `reports/nas_evidence_payloads/.gitignore` / `README.md`，确保真实 payload artifacts 默认 ignored。TDD red 已观察：缺少 `evidence_payload` module 时目标测试失败；实现后目标测试通过。当前仍不执行 parser、不复制真实文件、不读 raw text、不写 DB / `documents/chunks` / OpenSearch / Qdrant / MinIO、不接入 Agent final answer、不 rollout。

- [Phase 2.83 Evidence Write Payload Contract Planning] 完成 future evidence-write payload contract 规划：新增 `docs/PHASE283_EVIDENCE_WRITE_PAYLOAD_CONTRACT_PLAN.md`，定义未来从 eligibility report 到候选 `documents/chunks` payload dry-run 前必须满足的 schema、source、candidate document、candidate chunk、citation contract 与 decision states。Review 结论：payload contract 仍是 planning artifact，不是 document evidence；本轮不实现 payload builder、不生成 payload artifact、不写 DB / `documents/chunks` / OpenSearch / Qdrant / MinIO、不执行 parser、不复制真实文件、不读 raw text、不接入 Agent final answer、不 rollout。已写入 selective docs baseline prompt。

- [Phase 2.82a Evidence Write Eligibility Dry-run] 完成最小实现：新增 `app/services/asset_catalog/evidence_eligibility.py` 与 `scripts/phase282a_evidence_write_eligibility.py`，从 ignored local sanitized manifest 生成 `nas_evidence_write_eligibility.v0` dry-run report；新增 `reports/nas_evidence_eligibility/.gitignore` / `README.md`，确保真实 eligibility report artifacts 默认 ignored。TDD red 已观察：缺少 `evidence_eligibility` module 时目标测试失败；实现后目标测试通过。当前仍不执行 parser、不复制真实文件、不读 raw text、不写 DB / `documents/chunks` / OpenSearch / Qdrant / MinIO、不接入 Agent final answer、不 rollout。

- [Phase 2.82 Evidence Write Eligibility Planning] 完成 evidence-write eligibility review 规划：新增 `docs/PHASE282_EVIDENCE_WRITE_ELIGIBILITY_PLAN.md`，定义 NAS-derived sanitized manifest 进入未来 evidence-write planning 前必须满足的 gates。Review 结论：manifest 仍是 review-only，不是 document evidence；`approved` 不代表已写入、已索引或 Agent 可回答。当前仍不实现 evaluator、不生成 report artifact、不执行 parser、不复制真实文件、不写 DB / `documents/chunks` / OpenSearch / Qdrant / MinIO、不接入 Agent final answer、不 rollout。已写入 selective docs baseline prompt。

- [Phase 2.81a Sanitized Evidence Manifest Dry-run] 进入最小实现：新增 `app/services/asset_catalog/evidence_manifest.py` 与 `scripts/phase281a_sanitized_evidence_manifest.py`，从 sanitized parser preview metadata 生成 `nas_evidence_manifest.v0`；新增 `reports/nas_evidence_manifests/.gitignore` / `README.md`，确保真实 manifest artifact 默认 ignored。TDD red 已观察：缺少 `evidence_manifest` module 与缺少 CLI script 时目标测试失败；实现后目标测试通过。当前仍不执行 parser、不复制真实文件、不读 raw text、不写 DB / `documents/chunks` / OpenSearch / Qdrant / MinIO、不接入 Agent final answer、不 rollout。

- [Phase 2.81a Codex B Review] Review 通过：实现只处理 sanitized parser-preview metadata，unsafe raw fields 会 fail fast，write / Agent answer flags 会产生 `no_go`，manifest artifacts 默认 ignored。已写入 selective Git baseline prompt；baseline 后不得进入 evidence-write planning 或 Agent answer integration。

- [Phase 2.81 Codex B Review] Review 通过：Phase 2.81 只规划 sanitized evidence manifest，不实现 runner、不生成真实 manifest artifact、不执行 parser、不复制真实文件、不读 raw text、不写 DB / `documents/chunks` / OpenSearch / Qdrant / MinIO、不接入 Agent final answer、不 rollout。已写入 selective docs baseline prompt；Phase 2.81a manifest dry-run implementation 仍需用户单独授权。

- [Phase 2.81 Sanitized Evidence Manifest Planning] 完成 sanitized evidence manifest 后置规划：新增 `docs/PHASE281_SANITIZED_EVIDENCE_MANIFEST_PLAN.md`，定义从 sanitized parser preview 到 ignored local manifest 的 schema、Go / Pause / No-Go、cleanup / safety 字段与硬边界。Phase 2.81 只做 planning，不生成真实 manifest artifact、不执行 parser、不复制新文件、不读 raw text、不写 DB / `documents/chunks` / OpenSearch / Qdrant / MinIO、不接入 Agent final answer、不 rollout。下一步需 Codex B review；Phase 2.81a manifest runner 必须单独授权。

- [Phase 2.80a Controlled Scratch Parser Dry-run Result] Mac mini / 测试机 Phase 2.80a controlled scratch parser dry-run 返回 `Go`：`sample_count=3`、`copied_count=3`、`parsed_preview_count=3`、`cleanup_status=all_deleted`、`parser_dry_run_only=true`。报告确认未输出 raw text、secret、raw row、真实文件名、真实 NAS 路径或真实业务数据；未写 DB / `documents/chunks` / OpenSearch / Qdrant / MinIO；未接入 Agent final answer；未 rollout。测试机补充确认 scratch 与 parser preview 临时目录已删除且无残留。已新增 `docs/PHASE280A_CONTROLLED_SCRATCH_PARSER_DRY_RUN_RESULT.md`。当前能力只证明 parser preview；下一步建议 Phase 2.81 sanitized evidence manifest planning。

- [Phase 2.80 Codex B Review] Review 通过：Phase 2.80 仅规划 controlled scratch parser dry-run，未执行 parser、未复制或读取真实文件、未写 DB / `documents/chunks` / OpenSearch / Qdrant / MinIO、未进入 Agent final answer 或 rollout。规划明确 Phase 2.80a 必须单独授权，且 parser preview 只能输出 sanitized preview / manifest。已写入 selective docs baseline prompt，baseline 后停止，不进入 Phase 2.80a。

- [Phase 2.80 Planning] 完成 Controlled Scratch Parser Dry-run Planning：新增 `docs/PHASE280_CONTROLLED_SCRATCH_PARSER_DRY_RUN_PLAN.md`，明确 parser dry-run 只能在 Phase 2.79a 小批授权样本、scratch copy、hash、cleanup 边界内运行；输出只允许 local sanitized preview / manifest，不得写 `documents/chunks`、OpenSearch、Qdrant、MinIO、platform DB 或 Hermes DB，不得接入 Agent final answer。本轮未执行 parser、未复制真实文件、未读取真实正文、未写 DB/index/object-store、未进入 rollout。下一步需 Codex B review；Phase 2.80a 必须单独授权。

- [Phase 2.79a Small Batch NAS Smoke Result] Mac mini / 测试机 Phase 2.79a small batch NAS scratch-copy smoke 返回 `Go`：`sample_count=3`、`copied_count=3`、`hashes_computed=3`、`cleanup_status=all_deleted`。报告确认未输出 secret、raw row、真实 NAS 路径或真实业务数据；未写 DB / `documents/chunks` / OpenSearch / Qdrant / MinIO；未调用 parser；未进入 Agent final answer integration 或 rollout。已新增 `docs/PHASE279A_SMALL_BATCH_NAS_SMOKE_RESULT.md`。当前能力只证明小批授权样本 copy -> sha256 -> cleanup；下一步建议 Phase 2.80 controlled scratch parser dry-run planning，仍不直接执行 parser。

- [Phase 2.79 Planning] 完成 Small Batch Real Smoke Planning：新增 `docs/PHASE279_SMALL_BATCH_REAL_SMOKE_PLAN.md` 与 `docs/CODEX_MAC_MINI_SMALL_BATCH_NAS_SMOKE_PROMPT.md`，明确 Mac mini / 测试机 1-3 个小型非敏感样本的权限证明、样本大小、文件类型白名单、allowed actions、forbidden actions、stop conditions、sanitized report 与 Go / Pause / No-Go。当前只是 planning，未执行真实 NAS copy、未读取真实企业文件、未调用 parser、未写 DB / `documents/chunks` / OpenSearch / Qdrant / MinIO，未进入 Agent CRUD 或 rollout。下一步需 Codex B review；Phase 2.79a 必须单独授权。

- [Phase 2.79 Prompt] Phase 2.78 baseline 已完成：commit `5da558e`，tag `phase-2.78-local-scratch-runtime-baseline`。已写入 Phase 2.79 Small Batch Real Smoke Planning prompt，下一步只规划 Mac mini / 测试机 1-3 个小型非敏感样本真实 smoke 的授权门槛、样本范围、stop conditions 与 sanitized report。本轮仍不执行真实 NAS copy、不调用 parser、不写 DB / `documents/chunks` / OpenSearch / Qdrant、不进入 Agent CRUD 或 rollout。数据库团队二期前半段可继续推进；真实正文联调等待 Phase 2.79a 授权。
- [Phase 2.79 Codex B Review] Review 通过：Phase 2.79 仅规划小批真实 smoke，不执行真实 NAS copy；样本限制为 1-3 个小型非敏感文件，排除 BIM 大模型和整项目目录；parser、ingestion、DB / index write、Agent final answer integration 均后置。已写入 docs selective baseline prompt，Phase 2.79a 必须另获用户显式授权。

- [Phase 2.78 Controlled Local Scratch Runtime] 完成本地 fixture runtime 首轮实现：新增 `AssetScratchRuntime` 与目标测试，只在 explicit authorization 和 scratch / batch feature flags 均开启时处理 `would_copy` item；仅允许 local path / `file://` fixture，执行 copy、sha256、sanitized run record 与 cleanup。当前不连接真实 NAS、不复制真实企业文件、不调用 parser、不写 DB / documents / chunks / OpenSearch / Qdrant / MinIO、不启用 runtime flags 默认值。验证通过：py_compile 通过，scratch copy plan + runtime 目标测试 `10 passed`，Data Steward asset catalog regression `87 passed`，`git diff --check` 与 latest JSON 校验通过。
- [Phase 2.78 Prompt] Phase 2.76 / 2.77 baseline 已完成：commit `8aa94f3`，tag `phase-2.76-2.77-nas-scratch-copy-dry-run-baseline`。已写入 Phase 2.78 Controlled Local Scratch Runtime implementation prompt，下一步实现本地 fixture runtime：`would_copy` item copy 到 scratch、计算 sha256、生成 sanitized run record、成功或失败均 cleanup。仍禁止真实 NAS、真实企业文件复制、parser、DB / `documents/chunks` / OpenSearch / Qdrant 写入、Agent CRUD 与 rollout。数据库团队二期前半段可继续推进 REST/API Key `project_scope`、权限证明、资产目录 UI 与 Agent 查询入口。
- [Phase 2.78 Codex B Review] Review 通过：`AssetScratchRuntime` 保持本地 fixture runtime，要求 explicit authorization 与 scratch / batch flags；未授权或 flags off 时 fail closed；成功路径 copy -> sha256 -> cleanup，失败路径 best-effort cleanup；sanitized run record 不包含 source path / scratch path；parser / DB / documents / chunks / OpenSearch / Qdrant / MinIO / NAS write flags 恒为 false。已复跑 py_compile、目标测试 `10 passed`、Data Steward regression `87 passed`、`git diff --check` 与 latest JSON 校验，已写入 selective Git baseline prompt。

- [Phase 2.76 / 2.77 NAS Scratch Copy Pipeline Dry-run] 完成最小实现：新增只读 `AssetScratchCopyPlanner` 与 copy plan DTO，按 `project_scope`、`index_eligibility`、`lifecycle_status`、file type、size limit、storage locator 生成 `would_copy` / `skipped_requires_review` / `denied` dry-run plan。默认 feature flags `PLATFORM_ASSET_SCRATCH_COPY_ENABLED=false`、`PLATFORM_ASSET_BATCH_COPY_ENABLED=false`；当前不连接真实 NAS、不复制、不解析、不删除临时文件、不写 `documents/chunks/OpenSearch/Qdrant`、不启用 Data Steward runtime / Agent CRUD。验证通过：py_compile 通过，scratch copy plan tests `5 passed`，Data Steward asset catalog regression `82 passed`，`git diff --check` 通过。
- [Phase 2.76 / 2.77 Codex B Review] Review 通过：planner 保持 dry-run-only，真实 NAS copy / parser / indexing / Agent CRUD 均未启用；默认 feature flags 关闭；BIM 大模型仍 metadata-only。已写入 selective Git baseline prompt，baseline 后再进入 Phase 2.78 controlled local scratch runtime。

- [Phase 2.75 Data Steward Catalog Query Preview] 完成主线最小实现：明确 Phase 2.74 只完成真实 DB v1.1 结构 / 脱敏统计 / Hermes adapter contract 级耦合，尚不能让企业 Agent 通过数据库无损查询 NAS 文件正文。新增 `AssetCatalogQueryPreviewer`，catalog lookup 只返回资产目录元数据 preview，content answer 返回 `asset_catalog_only` Missing Evidence；缺少 REST/API Key `project_scope` 时 fail-closed；不连接真实 DB、不扫描 NAS、不写 `documents/chunks/OpenSearch/Qdrant`、不启用 runtime / mirror / indexing / Agent CRUD。验证通过：py_compile 通过，Data Steward 目标 pytest `77 passed`，`git diff --check` 通过。
- [Phase 2.75 Codex B Review] Review 通过：实现未越过 catalog preview 边界，未把 DB/NAS catalog metadata 变成 document evidence，未启用 runtime / mirror / indexing / Agent CRUD。已写入 `docs/NEXT_CODEX_A_PROMPT.md` selective Git baseline 任务；baseline 前仍需复跑 py_compile、Data Steward target pytest、`git diff --check` 与 latest JSON 校验。

- [Phase 2.72b DB LIMIT 30 Redacted Statistics Smoke Result] 测试机 `LIMIT 30` 脱敏统计 smoke 返回 `Go`：ProjectAssetView 观察 18 行，FileAssetView / ModelAssetView / AuditEventView 各观察 30 行，仅输出聚合统计；`permission_tags` 缺失数为 0，`confidentiality_level` 当前全为 `UNKNOWN`，`index_eligibility` 当前全为 `catalog_only`，`AuditEventView.event_id` 单调检查通过。未输出 raw row、secret、真实项目名 / 文件名 / NAS 路径、ID 原值或 `permission_tags` 原值，未写任何系统。已新增 `docs/PHASE272B_DB_LIMIT30_REDACTED_SMOKE_RESULT.md`。下一步建议规划 Hermes v1.1 readonly adapter contract update，继续禁止 mirror / indexing / Agent CRUD。

- [Phase 2.72a DB LIMIT 30 Redacted Statistics Smoke Planning] 已新增 `docs/CODEX_DB_LIMIT30_REDACTED_SMOKE_PROMPT.md`，并更新 `docs/DB_LIMIT30_REDACTED_SMOKE_PLAN.md` 为 prompt ready。该 prompt 仅允许测试机最多观察 30 行并输出聚合统计，禁止 raw row、真实项目名、文件名、NAS 路径、ID 原值、`permission_tags` 原值、summary JSON 原文、secret、写操作、NAS scan、mirror、indexing、Agent CRUD 和 rollout。本仓库未执行 `LIMIT 30`，未读取真实行，未写任何系统。

- [Phase 2.72 DB v1.1 Structure-only Smoke Result] 测试机已完成 `delivery_platform.asset_views.v1.1` structure-only smoke，结果 `Go`：DB 可达、database 匹配、四个 View 存在、v1.1 字段均存在、四个 `WHERE 1=0` 通过；未读取真实行、未输出 secret / 真实业务数据、未写任何系统。已新增 `docs/PHASE272_DB_V11_STRUCTURE_SMOKE_RESULT.md`。当前完成的是真实 DB v1.1 结构级只读耦合；完整 Data Steward 耦合、`LIMIT 30` 脱敏统计、mirror、indexing、Agent CRUD 仍未授权。

- [Phase 2.71 DB v1.1 Contract Alignment] 数据库团队已返回 sanitized schema gap response，并补充第 6 节确认：推进 `delivery_platform.asset_views.v1.1`，`project_scope` 以 REST / API Key 调用者上下文为主，`permission_tags` 使用固定粗粒度枚举，`confidentiality_level` 默认 `UNKNOWN`，`lifecycle_status` 包含 `active` / `archived` / `unknown` / `deleted_candidate` / `stale_unverified`，`index_eligibility` 默认 `catalog_only`。已更新 `docs/DB_SCHEMA_GAP_SANITIZED_RESPONSE.md`、`docs/PHASE271_DB_V11_CONTRACT_ALIGNMENT_PLAN.md`、`docs/CODEX_DB_V11_FIELD_CONFIRMATION_PROMPT.md` 与 `docs/CODEX_DB_V11_STRUCTURE_ONLY_SMOKE_PROMPT.md`。本轮仍未执行新 SQL、未读取真实行、未写 DB / index、未扫描 NAS、未启用 Data Steward runtime、未进入 rollout。
- [Phase 2.71 Pause Update] 数据库团队确认 `delivery_platform.asset_views.v1.1` 尚未完成目标环境部署：`v1_1_db_apply_status=NOT_APPLIED_BY_THIS_TASK`，V17 migration / REST contract 仍为本地补丁状态。已新增 `docs/DB_V11_DEPLOYMENT_BLOCKER_STATUS.md`，明确 Hermes 侧不得更新测试机 contract env，不得重跑 v1.1 structure-only smoke，直到数据库团队回传 `APPLIED_TO_TARGET_DB` 与后端部署完成。
- [Phase 2.71 Deployment Go Update] 数据库团队已回传 v1.1 脱敏部署报告：`V17__asset_views_v1_1.sql` 已由 Flyway 应用成功，目标 DB 记录 version `17` success，四个 View 均包含 v1.1 字段，后端测试实例健康检查 `UP`，Hermes 测试机 contract version key 已安全更新。已更新 `docs/DB_V11_DEPLOYMENT_BLOCKER_STATUS.md`，下一步允许测试机执行 `docs/CODEX_DB_V11_STRUCTURE_ONLY_SMOKE_PROMPT.md`；仍不授权 `LIMIT 30`、真实行读取、mirror、indexing 或 Agent CRUD。

- [Phase 2.69b] 完成 DB structure-only precondition runbook / prompt planning：新增 `CODEX_DB_STRUCTURE_ONLY_PRECONDITION_PROMPT.md`，用于测试机 Codex / operator 在不连接 DB、不执行 SQL、不安装工具的前提下确认 Hermes_memory install / version、secure env key names、readonly credential key name、contract version、MySQL client 或 Hermes readonly tooling。结论 `ready_for_test_machine_precondition_check`；下一步需 Codex B review 后再交测试机执行。即使前置条件 Go，也不得自动运行 DB smoke，必须等待用户显式指令。
- [Phase 2.69] 完成 DB structure-only smoke runbook / prompt planning：新增 `CODEX_DB_STRUCTURE_ONLY_SMOKE_PROMPT.md`，限定测试机只执行 `SELECT 1`、`SELECT DATABASE()`、View 列表、四个 `SHOW COLUMNS` 与四个 `WHERE 1 = 0` 空结构查询；明确禁止真实行读取、`LIMIT 1/30`、secret / 真实项目名 / 文件名 / NAS 路径 / raw row 输出、DB CRUD、migration、mirror write、NAS scan、index 写入与 rollout。本轮未连接 DB、未执行 SQL、未写 DB/index；结论 `ready_for_test_machine_structure_only_smoke`，需 Codex B review 后再交测试机执行。
- [Phase 2.68] 完成 Data Steward DB Branch Intake / Merge Readiness Review：确认 DB 支线 `/Users/Weishengsu/Hermes_memory_db0` 位于 branch `codex/data-steward-db0-contract`，HEAD `a272081`，tag `phase-db-branch-closeout-merge-readiness-baseline`；主线 Data Steward feature flags 默认关闭，catalog-only 不写 `documents/chunks/OpenSearch/Qdrant`，Missing Evidence 支持 `asset_catalog_only`，权限缺失保持 deny / fail-closed。验证：`tests/test_data_steward_*.py` 为 `71 passed`，MVP runner regression target `32 passed`，`git diff --check` 通过。结论 `ready_for_mainline_acceptance`；下一步只建议规划测试机真实 DB `structure_only` smoke，不授权真实样本、NAS scan、DB CRUD、migration、index 写入或 rollout。
- [Phase 2.66] 完成 Mac mini 侧受控安装规划：新增 `PHASE266_MAC_MINI_CONTROLLED_INSTALL_PLAN.md`，明确下一步先做 Mac mini preflight-only，检查机器依赖、目录、Git refs 与 env key 名称；不得直接 full install、不得启动 Docker、不得运行 API/CLI smoke、不得上传文件、不得写 DB/index、不得 repair/backfill/reindex/delete/migration、不得进入 production rollout。本轮为 docs-only planning，未运行测试。
- [Phase 2.65 Review Fix] 完成 reviewed hermes-agent ref pinning：Mac mini landing plan、quickstart、Codex Mac mini prompt 与 operator sheet 均从占位符改为 `phase-2.56e-natural-import-real-upload-smoke-baseline`；补测试确认 reviewed tag manifest 为 `ready_for_operator_review`，占位符仍为 `pause/missing_reviewed_hermes_agent_ref`。验证：py_compile 通过，目标测试 `41 passed`，reviewed / placeholder manifest smoke、diff check、latest JSON check 均通过。本轮未执行真实 Mac mini deployment、未启动 Docker、未运行 API / CLI smoke、未连接真实 DB、未扫描 NAS、未写 DB / OpenSearch / Qdrant、未进入 rollout。
- [Phase 2.65] 完成 Mac mini MVP Landing Acceleration Pack 首轮实现：新增只读 release manifest helper 与目标测试，新增 install/update quickstart，并更新 Mac mini install/update prompt 与 operator command sheet。验证：py_compile 通过，Phase 2.65 / 2.60 / 2.63 / 2.62 / 2.61a 目标测试 `40 passed`，manifest sample 输出 `pause`，原因是 hermes-agent reviewed ref 仍为 `NEEDS_REVIEWED_AGENT_REF`。本轮未执行真实 Mac mini deployment、未启动 Docker、未运行 API / CLI smoke、未连接真实 DB、未扫描 NAS、未写 DB / OpenSearch / Qdrant、未进入 rollout，等待 Codex B review。
- [Phase 2.64b] 完成 Selective Data Steward DB Integration 首轮实现：未执行 raw merge，按白名单接入 `app/services/asset_catalog/**`、`tests/test_data_steward_*.py`、Data Steward / DB contract docs，并在 `app/core/config.py` 最小加入默认关闭的 Data Steward feature flags；明确排除 `.claude/**`、DB 支线交接文件、未跟踪 QA probe、真实 DB/NAS 输出和任何会回退主线 Phase 2.57-2.63 MVP 文件的变更。验证：Data Steward pytest `71 passed`，target ruff `All checks passed!`，Phase 2.63 / 2.62 / 2.61a regression `28 passed`。本轮未连接真实 DB、未扫描 NAS、未写 migration / documents / chunks / OpenSearch / Qdrant、未创建 PR、未 commit / tag / push，等待 Codex B review。
- [Phase 2.64] 完成 Data Steward DB Branch Intake / PR Review：复核 DB 支线 `/Users/Weishengsu/Hermes_memory_db0`，确认 branch `codex/data-steward-db0-contract`、HEAD `a272081`、tag `phase-db-branch-closeout-merge-readiness-baseline`；DB 支线 `npm test` 为 `71 passed`，`npm run lint` 为 `All checks passed!`，`git diff --check` 通过；branch 与 tag 已推送到 origin。主线新增 `PHASE264_DATA_STEWARD_DB_BRANCH_INTAKE_PLAN.md` 记录 merge gates、测试机真实 DB smoke 后置条件和 12 个未跟踪 QA probe 文件。本轮未连接真实 DB、未扫描 NAS、未写 migration / documents / chunks / OpenSearch / Qdrant、未 merge、未创建 PR，等待 Codex B review。
- [Phase 2.63] 完成 Internal MVP Operator Daily Summary Workflow 首轮实现：新增只读 `phase263_mvp_operator_daily_summary.py`，可读取 Phase 2.62 summary 或直接复用 Phase 2.62 issue summary 逻辑聚合 issue JSON，输出每日 `ready` / `pause` / `no_go` operator summary；Markdown 输出脱敏，不包含 raw query、notes、expected/actual behavior、full path、document ids 或 chunk ids。目标验证：py_compile 通过，Phase 2.63/2.62/2.61a 测试 `28 passed`；本轮未读取真实 issue records、未创建外部 issue、未调用 API/CLI、未写 DB/index、未执行 repair 或 rollout。
- [Phase 2.62] 完成 Internal MVP Issue Triage Summary Runner 首轮实现：新增只读 `phase262_mvp_issue_triage_summary.py`，复用 Phase 2.61a validator 语义，支持显式 JSON / ignored issue 目录输入，输出脱敏 P0/P1/P2/P3 与 ready/pause/no_go summary；目标测试当前 `10 passed`，本轮未读取真实 issue records、未创建外部 issue、未调用 API/CLI、未写 DB/index、未执行 repair 或 rollout。
- [Phase 2.62 Prompt] Phase 2.61c baseline 已完成：commit `959ac78`，tag `phase-2.61c-internal-mvp-issue-storage-baseline`。Codex B 已写入 Phase 2.62 Internal MVP Issue Triage Summary Runner prompt，目标是把 ignored issue JSON 脱敏聚合为 Go / Pause / No-Go summary；本轮不创建外部 issue、不写 DB/index、不 repair、不 rollout。
- [Phase 2.61c Review] Codex B review 通过 Local Issue Storage Artifact：`.gitignore` 默认忽略真实 issue JSON / Markdown / 截图 / 日志 / 表格 / 文档，`README.md` 明确敏感边界、外部 issue 与 repair / rollout 均未授权；已写入 selective Git baseline prompt，仍禁止真实 issue records、DB/index 写入、外部 issue 创建或 rollout。
- [Phase 2.61c] 完成 Local Issue Storage Artifact：新增 `reports/internal_mvp_issues/.gitignore` 与 `README.md`，真实 operator issue JSON / Markdown / 截图 / 日志 / 表格 / 文档默认 ignored；本轮未生成真实 issue records、未创建外部 issue、未调用 API/CLI、未写 DB/index、未执行 repair 或 rollout。
- [Phase 2.61c Prompt] Phase 2.61b baseline 已完成：commit `d62b8a6`，tag `phase-2.61b-issue-storage-policy-baseline`。Codex B 已写入 Phase 2.61c Local Issue Storage Artifact prompt，目标是新增 `reports/internal_mvp_issues/.gitignore` 与 `README.md`；本轮不生成真实 issue records、不创建外部 issue、不写 DB、不 repair、不 rollout。
- [Phase 2.61b Review] Codex B review 通过 Local Issue Storage Policy Planning：`reports/internal_mvp_issues/` ignored storage policy、Git policy、review flow 与 Phase 2.61c artifact 边界清楚；已写入 selective docs-only Git baseline prompt，仍禁止真实 issue records、外部 issue 创建、DB/index 写入、repair 或 rollout。
- [Phase 2.61b] 完成 Local Issue Storage Policy docs-only planning：新增 `PHASE261B_ISSUE_STORAGE_POLICY_PLAN.md`，建议真实 operator issue records 默认保存在 ignored `reports/internal_mvp_issues/`，后续 Phase 2.61c 只提交 `.gitignore` / `README.md` 策略文件；本轮未写代码、未运行 API/CLI smoke、未写 DB/index、未创建外部 issue、未进入 repair 或 rollout。
- [Phase 2.61b Prompt] Phase 2.61a baseline 已完成：commit `b60d4d7`，tag `phase-2.61a-mvp-issue-intake-baseline`。Codex B 已写入 Phase 2.61b Local Issue Storage Policy Planning prompt，目标是规划真实 operator issue records 的本地 ignored 存储策略；本轮只做 docs-only planning，不写代码、不写 DB、不创建外部 issue、不 repair、不 rollout。
- [Phase 2.61a] 完成 Internal MVP issue intake runner 最小实现：新增只读 `phase261a_mvp_issue_intake.py`，支持生成 issue 模板、校验单条 / 批量 issue、统计 P0/P1/P2/P3，并按 ready / pause / no_go 输出 operator next steps；目标测试 `9 passed`，本轮未上传、未运行 API/CLI smoke、未写 DB/index、未创建外部 issue、未进入 repair 或 rollout。
- [Phase 2.61a Prompt] Codex B review Phase 2.61 planning 通过，已写入 Phase 2.61a Local Issue Intake Runner prompt。目标是用只读本地模板 / validator / summary generator 回收 Mac mini 真实试用问题；本阶段不写 DB、不创建外部 issue、不 repair、不 rollout。
- [Phase 2.61] 完成 Internal MVP Operator Flow / Issue Intake docs-only planning：新增 `PHASE261_INTERNAL_MVP_OPERATOR_FLOW_PLAN.md`，定义 readiness gate、使用中 issue 记录字段、P0/P1/P2/P3 分级、Codex A/B/C/D 分工和 Phase 2.61a local issue intake dry-run 候选；本轮未写代码、未运行 API/CLI smoke、未上传、未写 DB/index、未进入 rollout。
- [Phase 2.61 Prompt] Phase 2.60 baseline 已完成：commit `f445182`，tag `phase-2.60-mvp-local-readiness-pack-baseline`。Codex B 已写入 Phase 2.61 docs-only planning prompt，目标是规划内部 MVP operator flow / issue intake，让 Mac mini 真实试用问题可结构化回收；本轮仍不进入真实上传、API/CLI smoke、DB/index 写入、Data Steward 或 rollout。
- [Phase 2.60 Prompt] 用户明确要求暂不做第二真实文件 smoke，优先让 Mac mini 本地 MVP 尽快进入真实内部使用场景。Codex B 已写入 Phase 2.60 Internal MVP Launch Readiness Pack：新增只读 readiness runner、目标测试和 operator 文档同步；不上传文件、不跑真实 API/CLI smoke、不写 DB/index、不进入 Data Steward 或 rollout。
- [Phase 2.59 Baseline] Phase 2.59 docs-only planning 已 baseline：commit `2603a87`，tag `phase-2.59-natural-import-second-smoke-plan-baseline`。第二真实文件 smoke 仍需用户提供具体小型非敏感文件路径并明确授权后，由 Codex C 执行 `docs/NEXT_CODEX_C_PROMPT.md`。
- [Phase 2.57a Prompt] Phase 2.57 baseline 已完成，下一步进入 Natural Import Evidence Template / Runbook Dry-run：只做本地 dry-run 脚本、测试与文档同步，不上传文件、不运行 API/CLI smoke、不写 DB/index。
- [Phase 2.57] 完成 Natural Import MVP Usability / Evidence docs-only planning：新增 `docs/PHASE257_NATURAL_IMPORT_MVP_USABILITY_PLAN.md`，明确单文件自然语言导入 operator flow、evidence pack 字段、Go / Pause / No-Go、Mac mini runbook outline 与非目标。本轮未上传文件、未运行 API / CLI、未写 DB / OpenSearch / Qdrant，未进入 DB/NAS/Data Steward 或 rollout。
- [Phase 2.56e] 完成 Natural Import Real Upload Client + Real Smoke：Hermes 主仓新增真实 upload client，feature flag 开启时调用 Hermes_memory `/api/v1/documents/upload`；自然语言导入用户授权 `.docx` 成功，`document_id=ee54b72c-b88b-4fad-be54-007240285356`，`version_id=950da5fe-dd7c-4eba-8764-916b556d14ce`，alias `@C塔人力测算` 持久化后同 session retrieval 只命中新导入文档。Hermes 主仓目标测试 `34 passed`；本轮未 cleanup/delete/repair/backfill/reindex，未进入 rollout。
- [Phase 2.56e Prompt] Phase 2.56d baseline 已确认：Hermes 主仓 `65089d5c8`、Hermes_memory `4773abe`、tag `phase-2.56d-natural-import-runtime-wiring-baseline`。下一步进入真实 upload client wiring + 用户授权文件自然语言导入 smoke；必须由 CLI 自然语言命令触发，不得绕普通 upload path 声称成功；cleanup/delete/repair/backfill/reindex、Data Steward、production rollout 仍禁止。
- [Phase 2.56d Review] Codex B review 通过：runtime hook 已接入 `run_agent.py`，默认 disabled 与 enabled-without-client 均 fail-closed；复跑 py_compile、targeted pytest `28 passed`、disabled-path CLI smoke、enabled-without-client CLI smoke 均通过。已写入双仓 selective Git baseline prompt；baseline 后停止，不进入 Phase 2.56e。
- [Phase 2.56d] 完成 Natural Import Runtime Wiring 最小实现：Hermes 主仓 `run_agent.py` 在普通 memory kernel retrieval / LLM answer 前调用 natural import runtime hook；默认真实 upload disabled，明确导入 intent 返回 structured diagnostics 并 fail-closed，不进入普通 retrieval 乱答。新增 fake adapter runtime tests，py_compile 通过，natural import 目标测试 `28 passed`；disabled-path CLI smoke 通过。本轮未调用真实 upload API、未上传文件、未写 DB / OpenSearch / Qdrant。
- [Phase 2.56d] Codex B review 确认 Phase 2.56c blocked 结果成立：自然语言导入 parser 命中，但 Hermes 主仓 runtime 尚未接入 `run_natural_file_import_preflight()` 或真实 upload adapter；Codex A 没有绕普通 upload path 声称成功，边界正确。
- [Phase 2.56d] 已写入下一轮 Codex A 任务：只做 runtime wiring minimum implementation、fake / mocked adapter tests 与交接文档同步；默认真实 upload 关闭，不复用用户授权文件，不调用真实 Hermes_memory upload API，不写 DB / OpenSearch / Qdrant。

- [Phase 2.56c] 执行用户授权的自然语言单文件真实导入 smoke 到 stop condition：文件 preflight、API `/health`、Hermes CLI help、parser preflight 均通过；但 Hermes 主仓 runtime 尚未接入 `run_natural_file_import_preflight()` / 真实 upload adapter，故记录 `runtime_not_wired_to_real_upload_adapter` 并停止。本轮未绕过普通 upload path，未上传文件，未写 DB / OpenSearch / Qdrant，未执行 alias bind 或 retrieval smoke。
- [Phase 2.56c Authorization] 用户已授权单文件自然语言导入真实 smoke：`C塔项目人力配置及成本测算表0506.docx`，metadata preflight 为 regular file、`16885 bytes`、Microsoft Word 2007+。已写入 Codex A 执行 prompt；要求优先验证自然语言导入路径，若 runtime 未接真实 upload adapter 则报告 blocked，不得绕过成普通 upload 后声称通过。
- [Phase 2.56c Gate] Phase 2.56b baseline 已确认：`683cf02` / `phase-2.56b-natural-import-real-smoke-plan-baseline`。已将下一步设置为 Phase 2.56c 授权等待状态：真实自然语言导入 smoke 必须由用户重新提供小型非敏感文件路径并明确授权；未授权前不调用 upload API、不上传、不运行 API / CLI smoke。
- [Phase 2.56b Review] Codex B review 通过：planning 覆盖授权门槛、样本要求、执行步骤、验收字段、stop conditions、run record 与非目标；本轮无真实 upload / API / CLI / DB-index 行为。已写入 docs-only baseline prompt。
- [Phase 2.56b] 完成 Natural Import Real Smoke docs-only planning：新增 `PHASE256B_NATURAL_IMPORT_REAL_SMOKE_PLAN.md`，明确自然语言触发真实小文件导入 smoke 的授权门槛、样本要求、执行步骤、验收字段、stop conditions 与 sanitized run record。未执行 upload、未运行 API / CLI smoke、未写 DB / OpenSearch / Qdrant。
- [Phase 2.56b Prompt] Phase 2.56a baseline 已确认：Hermes 主仓 `0264ca079`，Hermes_memory `dea0523`，tag `phase-2.56a-natural-import-adapter-skeleton-baseline`。已写入 Phase 2.56b docs-only planning prompt，下一步只规划自然语言触发真实小文件导入 smoke 的授权门槛、执行步骤、验收字段与 stop conditions；不执行真实 upload。
- [Phase 2.56a Review] Codex B review 通过：`FeatureFlaggedHermesMemoryUploadAdapter` 默认 disabled，fake adapter 只有 `real_upload_enabled=True` 才执行；import diagnostics 不作为 retrieval evidence。已复跑 Hermes 主仓 py_compile 与 targeted pytest，`25 passed`；Hermes_memory 静态 / latest JSON / ignore 检查通过。已写入 dual-repo selective baseline prompt。
- [Phase 2.56a] 完成 natural import real adapter skeleton：Hermes 主仓新增 feature-flagged upload adapter，默认 `enabled=false`；有效导入请求未显式启用时 fail-closed 为 `real_upload_disabled`，fake adapter success 需 `real_upload_enabled=True`。主仓目标测试 `25 passed`；本轮未调用真实 upload API、未上传文件、未写 DB / OpenSearch / Qdrant。
- [Phase 2.56a Prompt] Phase 2.55a baseline 已确认：`1a41475` / `phase-2.55a-internal-mvp-upload-smoke-baseline`。下一步主线进入 Natural Import Real Adapter Skeleton：只做 feature-flagged adapter skeleton 与 fake / disabled tests，真实 upload 默认关闭，不触发 API / CLI smoke，不写 DB / OpenSearch / Qdrant，不进入 Data Steward / DB / NAS / BIM 分支。
- [Phase 2.55a Review] Codex B review 通过：单文件真实 upload / ingestion / retrieval smoke 已验证；不需要 Codex C targeted validation；已写入 selective Git baseline prompt。保留 P2 展示尾项：API 顶层 `citations=[]`，但 result-level / CLI citations 可见。
- [Phase 2.55a] 完成用户授权单个 `.docx` 文件内部 MVP upload smoke：既有 `/api/v1/documents/upload` 成功生成 `document_id=06e59241-95e9-44ff-a73d-35d2f52a359b`、`version_id=7dc57676-c707-4f44-9688-0b77058f07a0`、`chunk_count=26`；DB/version/chunk、OpenSearch、Qdrant dense 均可诊断；API hybrid retrieval 与 Hermes CLI alias / retrieval smoke 只返回新上传文件 evidence，safety flags 保持 false/required，未发现第三文件污染。已写入 ignored sanitized run record；本轮不 cleanup / delete / repair / backfill / reindex，不 baseline，等待 Codex B review。

- [Phase 2.55a] 用户已提供并授权一个小型 `.docx` 文件用于内部 MVP 真实 upload smoke：`/Users/Weishengsu/Library/Containers/com.tencent.xinWeChat/Data/Documents/xwechat_files/wxid_sn2cczdp4u2l12_c2fd/msg/file/2026-05/卓羽智能核心技术能力汇报 PPT 大纲V1.0.docx`（`49894 bytes`）。Codex B 已写入 `docs/NEXT_CODEX_A_PROMPT.md`，授权范围仅限单文件 upload / ingestion / retrieval smoke 与 ignored sanitized run record；不授权 cleanup / delete / repair / backfill / reindex / migration，不进入 Data Steward / BIM / NAS / TB 文件池或 production rollout。本轮 Codex B 未上传、未运行 API / CLI smoke、未写 DB / OpenSearch / Qdrant。

- [Phase 2.55] Codex B review 通过 Internal MVP real upload smoke planning：规划保持 docs-only，真实 upload 后置到 Phase 2.55a，且必须由用户提供非敏感文件路径并显式授权。已写入 docs-only baseline prompt；不运行 API/CLI、不上传、不写 DB/index、不进入 Data Steward。
- [Phase 2.55] 完成 Internal MVP real upload smoke docs-only planning：新增 `PHASE255_INTERNAL_MVP_REAL_UPLOAD_SMOKE_PLAN.md`，明确小型非敏感单文件、pre-flight、upload/ingestion/index/alias/evidence smoke steps、trace/citation 字段、stop conditions、sanitized run record 与 Phase 2.55a 授权门槛。本轮未执行 upload、未运行 API/CLI、未写 DB/index、不进入 Data Steward 或 rollout。
- [Phase 2.55] Phase 2.54c baseline 已完成，开始进入 Internal MVP real upload smoke planning。已写入 Codex A docs-only planning prompt：只规划小型非敏感文件真实导入 smoke，不执行 upload、不运行 API/CLI、不写 DB/index、不进入 Data Steward / BIM / NAS / TB 文件池。
- [Phase 2.54c] Codex C targeted re-smoke 通过：session `20260508_181817_c7c9a3` 中 `@主标书` 绑定正常，Q3 file answer metadata 可见 required fields、echo required、title/source_name/source_type/citation_count 与 `metadata_as_answer=false` / `facts_as_answer=false` / `snapshot_as_answer=false` / `requires_retrieval_evidence=true`；无 metadata/facts/transcript/snapshot 替代 evidence，无第三文件污染。已写入 selective Git baseline prompt。
- [Phase 2.54c] Codex B review 通过 display-tail fix：主仓 diff 只涉及 `ContextBuilder` 展示层与目标测试，未改 retrieval contract / adapter contract / memory kernel 主架构；复跑 py_compile 与 targeted pytest `74 passed`，Hermes_memory 静态检查通过。已写入 Codex C Q3 targeted re-smoke prompt，暂不 baseline、不进入 Phase 2.55。
- [Phase 2.54c] 完成 File Steward UX file answer metadata 展示尾项修复：`ContextBuilder` 在 `file_answer_metadata` 分支稳定输出 required fields、echo required、source fields present 与 safety flags，并为 `source_name` 增加 metadata fallback。主仓 py_compile 通过，targeted pytest `74 passed`；本轮未运行真实 CLI、未上传文件、未写 DB/index、未改 retrieval contract。
- [Phase 2.54c] Codex C targeted CLI smoke 已完成：Q1 alias missing 与 Q2 active document continuation 均通过，Q3 file answer metadata 为 partial。核心 evidence 边界安全，但 source/title 与 `metadata_as_answer=false` / `facts_as_answer=false` / `snapshot_as_answer=false` 未在最终 CLI 输出中稳定透出。已写入 Codex A display-tail fix prompt；下一步只允许最小展示层修复与目标测试，不进入真实 upload、Data Steward、DB/index 写入或 rollout。
- [Phase 2.54c] Phase 2.54b baseline 已完成：Hermes 主仓 `5e824a884`，Hermes_memory `12dc641`，tag `phase-2.54b-file-steward-context-display-baseline`。已写入 Codex C targeted CLI smoke prompt，用于验证 File Steward UX diagnostics 真实终端展示；本轮不写新功能、不上传文件、不写 DB / index、不进入 Data Steward 或 rollout。
- [Phase 2.54b] Codex B review 通过 File Steward UX runtime display integration：`ContextBuilder` 新增 `File steward diagnostics:`，目标测试 `73 passed`，未改 retrieval contract、未调用 API、未真实 upload、未写 DB / index。已写入 selective Git baseline prompt。
- [Phase 2.54b] 完成 File Steward UX runtime display integration：`ContextBuilder` 新增 `File steward diagnostics:` 分区，alias missing / retrieval suppressed、active document continuation、file answer metadata 均可在 enterprise context 中展示；目标测试 `73 passed`。本轮未改 retrieval contract、未调用 API、未真实 upload、未写 DB / index。
- [Phase 2.54b] Codex B 确认 Phase 2.54a 双仓 baseline 完成：Hermes 主仓 `a34954c85`，Hermes_memory `eadb3ff`，tag `phase-2.54a-file-steward-ux-helper-baseline`。已写入 Phase 2.54b display integration prompt；本轮只允许接入 `ContextBuilder` 展示层，不改 retrieval contract、不真实 upload、不写 DB / index。
- [Phase 2.54a] Codex B review 通过 File Steward UX helper：`file_steward_ux.py` 为纯 helper，目标测试 `6 passed`，未接 runtime、未真实 upload、未调用 API、未写 DB / index。已写入 selective Git baseline prompt。
- [Phase 2.54a] 完成 File Steward UX helper 首轮最小实现：新增 alias failure helper、active document continuation hint、file answer metadata structure，固定保留 facts/transcript/snapshot/metadata 不作为 answer 且需要 retrieval evidence；主仓目标测试 `6 passed`。本轮未接真实 upload、API、DB、索引或 runtime integration。
- [Phase 2.54a] Codex B 确认 Phase 2.53c 双仓 baseline 完成：Hermes 主仓 `1f4309abe`，Hermes_memory `4a06ef9`，tag `phase-2.53c-natural-import-mocked-integration-baseline`。已写入 Phase 2.54a File Steward UX helper implementation prompt；本轮只允许纯 helper + unit tests，不接真实 upload / API / DB / index / Data Steward / rollout。
- [Phase 2.53c] Codex B review 通过 mocked natural import integration + Enterprise Memory Native UX bridge；主仓目标测试 `21 passed`。已写入 selective Git baseline prompt，仍禁止真实 upload、API / CLI smoke、DB / index 写入、Data Steward 和 rollout。
- [Phase 2.54] 采纳本地 PR `LOCAL_PR_ENTERPRISE_MEMORY_USABILITY_PROPOSAL.md`：后续主线从“只做可检索”提升到 Enterprise Memory Native UX / File Steward UX。新增 Phase 2.54 规划，并把下一步 Codex A 任务调整为 Phase 2.53c mocked natural import integration + UX bridge；不真实上传、不运行 API / CLI smoke、不进入 Data Steward。
- [Phase 2.53b] Codex B review 通过 natural import integration planning；已写入 docs-only Git baseline prompt。baseline 只允许规划文档与交接文档，不进入 Phase 2.53c、不写代码、不真实 upload、不运行 API / CLI smoke、不进入 Data Steward。
- [Phase 2.53b] Phase 2.53a baseline 已完成，当前写入 adapter / kernel integration planning prompt；下一轮只做 docs-only planning，明确 parser 调用位置、upload adapter 接口、alias seed、diagnostics 与 fail-closed 边界，仍禁止真实 upload、API / CLI smoke、DB / index 写入、Data Steward 和 rollout。
- [Phase 2.53a] Codex B review 通过 natural file import parser / dry-run planner review-fix；否定导入 intent 已 fail closed，目标测试 `10 passed`。已写入 Phase 2.53a selective Git baseline prompt，仍禁止真实 upload、API / CLI smoke、DB / index 写入、adapter / kernel integration、Data Steward 与 rollout。
- [Phase 2.51b] 完成 minimal Mac Mini operator command sheet artifact：新增一页式操作单，覆盖 pre-check、repo state、hot update、health checks、run record、review command、rollback、stop conditions 与 never-do；本轮 docs-only，未执行真实命令或部署。
- [Phase 2.52] 完成 Phase 2.51 runbook baseline 后路线规划：推荐下一步优先做 Phase 2.51b minimal operator command sheet；2.51a fake deployment record dry-run smoke 与 2.50b evidence pack planning 后置候选。
- [Phase 2.51] Codex B review 通过 Mac Mini operator / hot update runbook 及 review-fix；当前执行 docs-only Git baseline，仍不执行真实 Mac Mini deployment、API / CLI smoke、DB / index 写入、repair、rollout 或 Data Steward。
- [Phase 2.51] Codex B review-fix 已完成：Mac Mini operator runbook 现在明确 canonical run record 是 `reports/internal_mvp_runs/<YYYYMMDD>_<session>.json`；Markdown 只作为 optional human notes，不得作为 Phase 2.49 bridge `--input-run-record`。
- [Phase 2.46c] Codex B review 通过 Codex C Mac mini local MVP smoke prompt artifact；已写入 docs-only Git baseline prompt，仍禁止实际发起 Codex C、运行 smoke、启动服务、生成真实 evidence、DB/index 写入和 rollout。
- [Phase 2.46c] Codex B 已确认 Phase 2.46b baseline 完成，写入下一步 Codex C local MVP smoke prompt artifact 提示词；本阶段仍只做 docs artifact，不运行 smoke、不启动服务、不生成真实 evidence、不写 DB/index 或 rollout。
- [Phase 2.46b] Codex B review 通过 Mac mini evidence attachment planning artifact；已写入 docs-only Git baseline prompt，仍禁止真实 evidence、health-check runner、API/CLI smoke、DB/index 写入和 rollout。
- [Phase 2.46b] Codex B 已确认 Phase 2.46a baseline 完成，写入下一步 human-run evidence attachment planning 提示词；本阶段仍只做 docs planning，不生成真实 evidence、不运行 health-check runner、API/CLI smoke、DB/index 写入或 rollout。
- [Phase 2.46a] Codex B review 通过 Mac mini Day-0 setup checklist artifact；已写入 docs-only Git baseline prompt，仍禁止真实 setup、health-check runner、API/CLI smoke、DB/index 写入和 rollout。
- [Phase 2.46a] Codex B 已确认 Phase 2.46 baseline 完成，写入下一步 Day-0 setup checklist artifact 提示词；本阶段仍只做 docs/template，不执行真实 Mac mini setup、API/CLI smoke、DB/index 写入或 rollout。
- [Phase 2.46] Codex B review 通过 Mac mini Day-0 setup planning artifact；已写入 docs-only Git baseline prompt，仍禁止真实部署、API/CLI smoke、DB/index 写入、repair、rollout 与 Phase 2.46a 自动推进。
- [Phase 2.1] 固化 dense backend `/search` 请求格式，传递 query、top_k、filters 与 1024 维约束，状态：完成。
- [Phase 2.1] 增强 dense result 规范化，支持 snippet、metadata、embedding 与 dense 来源标记，状态：验证通过。
- [Phase 2.1] 新增本地 HTTP vector backend 集成测试，覆盖 dense 与 hybrid 合并链路，状态：完成。
- [Phase 2.1] 验证 dense backend 异常时 hybrid fail-open，sparse 结果不受影响，状态：验证通过。
- [Phase 2.1-gate] 检查真实 VECTOR_STORE_URL，当前环境未配置，无法执行外部 dense/hybrid 实测，已列入 TODO。
- [Phase 2.1-gate] 核查 context_builder 与 citation 统一字段依赖，dense/sparse/hybrid 消费一致，状态：代码检查通过。
- [Phase 2.1-gate] 复核 memory trace 字段，route、retrieval_mode、dense/sparse 与 filters 均可诊断，状态：通过。
- [Phase 2.1-Qdrant] 将 dense backend 主路线切换为 Qdrant，新增 collection、upsert、search 与 filter 映射，状态：代码完成。
- [Phase 2.1-Qdrant] 接入阿里云 text-embedding-v3 查询向量客户端，支持 1024 维校验，真实 API key 待配置验证。
- [Phase 2.1-Qdrant] 完成 fake Qdrant dense 与 hybrid 测试，context/citation 消费一致，真实容器验证待执行。
- [Phase 2.1-Qdrant-real-gate] 本机无 docker 且出网受限，无法连通真实 Qdrant/阿里云；已补齐待办并待换环境实测。
- [Phase 2.1-Qdrant-real-gate] 接通本地 Qdrant+OpenSearch，完成真实 dense-only/hybrid/fail-open 实测（query_vector 路径），embedding 仍待验证。
- [Phase 2.1-Qdrant-real-gate] Hermes 主仓库 hermes-agent 已能消费真实 dense/hybrid 结果并注入 context block（query_vector 路径），状态：通过。
- [Phase 2.1-Qdrant-real-gate] 复跑阿里云 text-embedding-v3 真调用成功，返回 1024 维向量；dense-only 与 hybrid embedding 路径均通过。
- [Phase 2.2] Codex C 完成文档/代码阅读与现状复述要点整理，状态：完成。
- [Phase 2.2] Codex C 输出 Phase 2.2（rerank 前置）结构与 contract 方案，状态：完成。
- [Phase 2.2] 引入 candidate pool 与 rerank hook，固定 rerank 在候选合并后、final results 前执行，状态：完成。
- [Phase 2.2] 定义 RerankRequest/RerankOutcome，NoopReranker 返回可诊断 trace，真实模型仍未接入。
- [Phase 2.2] 增加 rerank fail-open、candidate pool trace 与最小评测入口测试，状态：验证通过。
- [Phase 2.2] 补齐 rerank/candidate pool 诊断字段，覆盖 elapsed、fail-open 与候选计数别名，状态：完成。
- [Phase 2.2-closeout] 完成 rerank 前置结构收口，新增真实 reranker adapter 前置方案，明确仍未接入真实模型。
- [Phase 2.3] 选定阿里云 Text Rerank API 作为真实 reranker spike 主路线，完成边界与验证方案设计。
- [Phase 2.3] 实现阿里云 Text Rerank 最小 adapter，默认关闭，完成 mock 排序映射与 fail-open 测试。
- [Phase 2.3] 补充阿里云 rerank key 回退逻辑，优先专用 key，缺省复用 embedding key，保留分离能力。
- [Phase 2.3-real-gate] 执行真实 smoke test，当前环境缺少 rerank/embedding key，adapter 按预期 failed_open。
- [Phase 2.3-real-gate] 复测确认 rerank 已回退读取 embedding key，但真实请求在网络/DNS 阶段失败，未拿到 provider 响应。
- [Phase 2.3-real-gate] 修正 rerank base_url/endpoint 诊断链路，真实请求已命中 DashScope 并返回 200，gate 通过。
- [Phase 2.6-gray-env] 恢复 Docker/Qdrant/OpenSearch 并复跑灰度脚本，环境已通；当前未命中 rerank 为 local_default_enablement_not_matched。
- [Phase 2.3-real-gate] 补 6 条 gate 样本黄金 query 并完成 baseline/experiment，top-1 从 0.8333 提升到 1.0。
- [Phase 2.3b] 扩充 36 条脱敏近真实黄金 query，复用原 spike 路径完成 baseline/experiment；top-1 从 0.9444 提升到 1.0，暂无回归。
- [Phase 2.4] 扩样到 48 条并完成默认启用策略评估；收益仍集中在招标资质/条款类 query，建议进入局部默认启用实施评估。
- [Phase 2.5] 落地局部默认启用灰度规则，仅对招标资料高收益 query 启用 rerank；补齐全局关闭、fail-open 与策略 trace 验证。
- [Phase 2.6] 完成灰度脚本与回滚演练验证；当前 Qdrant/OpenSearch 不可用，真实灰度闭环被环境阻塞，trace 与关闭路径已确认。
- [Phase 2.6] 修正灰度脚本 request 上下文传递，招标类 query 已可命中局部默认启用；灰度开启、关闭与 timeout fail-open 均完成真实脚本验证。
- [Phase 2.6] 连续三轮观察命中率与回退率稳定，但发现少量非招标误命中；根因是 candidate_source_types 参与放行，当前不宜直接进入更长期灰度运行。
- [Phase 2.6] 收紧局部默认启用到 request 侧 source_type/route_type 命中，连续三轮复跑后误命中清零，目标招标 query 仍稳定命中。
- [Phase 2.6] 延长灰度观察到 4 次完整运行，命中集与回退链路保持稳定，误命中未再出现，当前适合继续小流量长期观察但不扩大范围。
- [Phase 2.6] 继续延长到 5 次完整真实灰度观察，命中集仍未漂移、误命中持续为零；当前重点转为继续盯 p95/p99 长尾延迟，而不是扩大启用范围。
- [Phase 2.6] 新增观察窗口里出现一次 dense 全量失败，48 条 query 全部落到 candidate_pool_below_min_threshold；下一轮已恢复正常，当前需继续观察后端瞬时波动。
- [Phase 2.6] 将后端瞬时失败窗口正式纳入长期观察项；累计 9 次完整观察中正常窗口命中集仍稳定，当前主要风险已转为后端瞬时波动而非规则漂移。
- [Phase 2.6] 完成退出标准与最后 3 次完整观察判定：规则层与回退机制稳定，延迟满足当前阶段标准，异常窗口未重复出现，Phase 2.6 可正式收口。
- [Phase 2.7] 开始收口局部默认启用运行基线，新增 runbook 并固化开关、观测项、回滚条件与运行前 checklist，准备进入更长期小流量运行。
- [Phase 2.8] 在保持当前范围与规则不变的前提下，完成 3 次完整小流量运行窗口；命中集稳定、误命中为零、未复现后端异常，但 p99 仍有长尾尖峰。
- [Phase 2.8] 完成退出标准与最后 3 次完整观察判定；运行基线、回退机制、延迟和后端异常控制均满足收口条件，Phase 2.8 正式收口。
- [Phase 2.9] 整理当前运行基线、运行风险与 rollout 评估前提，新增 readiness 文档，为更高一级 rollout 评估准备输入，暂不进入实施。
- [Phase 2.9] 将 readiness 前提进一步细化为逐项判定、风险分层状态与 rollout 准入/阻断条件，明确当前处于“已具备 rollout readiness 输入”状态。
- [Phase 2.9] 执行固定长窗口 readiness 观察时提前失败：run1 出现 dense 失败、命中集漂移与高延迟，run2 出现 OpenSearch 重复超时，当前不满足 rollout 评估准入条件。
- [Phase 2.9b] 在加装散热器、清空应用后的 Air 8GB 上完成 8+12 次长窗口压力验证；业务链路未失稳，但 12 次窗口已出现明显 p99 长尾尖峰，瓶颈更像宿主机内存 / swap 与 Docker 资源竞争。
- [Phase 2.9] 明确后续执行节奏为“白天继续开发、晚上跑长窗口验证”，并新增小批量脱敏企业资料受控验证计划，先做低敏、代表性样本接入，不改变当前规则与启用范围。
- [Phase 2.9-真实文件测试] 已完成多份真实企业文件接入与 Hermes 联调，覆盖单文件、多文件、大型标书三类场景；确认当前具备“AI 标书初筛助手”能力，当时高可信度灰度仍待补证。
- [Phase 2.9c] 新增大标书章节定向召回增强，针对资质/项目经理/工期/付款结算/工程量清单类查询引入 section scope 推断与 heading_path boosting；资质与工程量清单相关问题召回明显改善，但合同专用条款与深层商务参数仍未稳定覆盖。
- [Phase 2.9c] 继续增强合同专用条款与前附表定向检索，真实大标书中“付款/结算/质保金/缺陷责任期/误期赔偿”已开始稳定打到第三章合同补充条款；当时高可信长窗口仍待独立机器补证。
- [Phase 2.9c] 补入“工期要求/计划开工日期/计划竣工日期/关键工期节点”等真实标题词后，schedule 查询已能稳定进入 section scope；当时合同深层参数在逼近，灰度仍待补证。
- [Phase 2.9c] 完成当时统一收口判断：资质等级、项目经理门槛、不平衡报价已进入“稳定够用”，合同深层参数维持“逼近但不稳”；当时判断仍需补证。
- [Phase 2.9c] 修复 RetrievalService 的 db=None 兼容性回归：_infer_document_scope() 与 database fallback 已在无 DB 模式下安全返回，phase26 灰度补证入口不再被 NoneType.query 直接打断；当时恢复继续推进 2.9c。
- [Phase 2.9c] 继续只盯“总工期/关键节点”：补入工期要求、计划开竣工日期、关键工期节点等真实标题词后，schedule 查询能更稳定进入 scope，但 top 结果仍多落在合同邻近段落或技术要求中的进度/延误段落；当前只能判定为“有提升但仍不稳定”。
- [Phase 2.9c] 本轮只攻“总工期/关键节点”：新增 schedule 参数短语精确加权后，真实大标书中工期要求 chunk 升到 top1、合同工期定义 chunk 升到 top2，已从明显打不进去提升为有提升但仍不稳定。
- [Phase 2.9c] Codex C 完成 Windows + WSL2 高可信补证：长窗口 20/20 成功，连续真实工作流 60/60 成功，OpenSearch/dense/sparse/漂移/后端异常均为零；Phase 2.9c 稳定性收口证据已补齐，建议收口，Aliyun provider smoke 作为非阻塞尾项保留。
- [Phase 2.9d] 完成非阻塞尾项首轮收敛：Aliyun embedding 与 rerank provider smoke 真调用通过，rerank 使用 embedding key fallback；大型标书工期类 10 条真实问法扩样全部命中工期要求目标 chunk。
- [Phase 2.9d] 完成文档基线固化：Phase 2.9c 收口与 2.9d 首轮尾项完成已统一写入 TODO/readiness；专用 rerank key smoke 可选保留，不进入生产级 rollout，PRD 核心缺口继续建账。
- [Vision] 将企业级全功能 Agent 愿景写入 PRD/Roadmap/技术设计，明确多模态资料、会议记忆和经营辅助分析为后续阶段能力，不打断当前记忆底座主线。
- [Phase 2.11] 新增企业上下文治理与多模态规划文档，明确本阶段只做架构与验收标准，不直接实现完整摄取或会议记忆。
- [Phase 2.11] 补齐上下文治理、Excel、PPTX、会议音频四块详细设计与验收样本，仍不进入功能实现。
- [Phase 2.11a] 完成 MVP 最小切口评审，建议优先做企业上下文治理增强，Excel/PPTX ingestion 后置。
- [Phase 2.11a] Hermes 主仓库完成最小上下文治理实现，Hermes_memory 保持无状态，仅同步阶段状态。
- [Phase 2.11a] 同步 history_memory_as_evidence 语义修复结论，历史记忆不得作为本轮 evidence。
- [Phase 2.11a] 同步真实终端验收通过结论：文件延续与 A/B 对比均未出现历史记忆伪 evidence。
- [Phase 2.11b] 同步企业文件别名规划状态，alias 绑定 document_id，暂不改检索契约。
- [Phase 2.11b] 同步 Hermes 主仓库 session-level 文件别名最小实现完成状态，Hermes_memory 仍保持无状态。
- [Phase 2.11b] 同步 alias 真实终端修复状态：会话层绑定已打通，Hermes_memory 不改契约。
- [Phase 2.11b] 同步真实终端验收通过结论，文件别名可绑定、使用、对比并抑制 missing 检索。
- [Phase 2.11c] 同步基础信息召回规划，metadata snapshot 仅作检索辅助和引用导航。
- [Phase 2.11c] 完成 tender metadata snapshot 最小实现，真实大标书工程地点、建设单位、代建单位 query 已锚定目标 chunk。
- [Phase 2.11c] 补强 snapshot trace 回归测试，确认 OpenSearch 与 DB fallback 路径均不把 snapshot 当作 answer evidence。
- [Phase 2.11c] 真实终端复验通过，基础信息召回 evidence 正确且 snapshot_as_answer 保持 false。
- [Phase 2.11d] 同步综合回归规划，后续需新增第二份大型标书与制度/合同文件验证跨文件防污染。
- [Phase 2.11d] 完成三份新增真实文件入库与索引，并通过 15 条上下文治理综合回归。
- [Phase 2.11e] 同步遗留 dirty 治理规划，文档、协作、DX、运行产物与 lockfile 分开处理。
- [Phase 2.11e] 完成 repo hygiene 收口：.run 作为本地运行产物忽略，uv.lock 保留为依赖治理尾项。
- [Phase 2.12] 完成 Excel/PPTX ingestion MVP 立项评审草案，先定依赖治理、样本需求与 citation 验收边界。
- [Phase 2.12] 完成 uv.lock 依赖治理裁决，lockfile 校验通过且无敏感路径，纳入依赖基线。
- [Phase 2.12] 完成 Excel/PPTX ingestion 最小闭环，6 个真实样本均完成上传、索引与 sheet/cell 或 slide citation 检索验证。
- [Phase 2.12a] Hermes 主仓库已补 structured citation 消费与展示最小修复；Hermes_memory 本轮仅同步阶段状态，不改 parser、retrieval contract 或 memory kernel 架构。
- [Phase 2.12] 真实 Hermes 终端验收收口：Excel/PPTX structured citation 5 条复验全部通过，跨类型切换无污染，Phase 2.12 进入 Git baseline 固化。
- [Phase 2.12] 完成后置 Git 核对：主仓库 origin 为上游 HTTPS，backup2 为当前有效可写基线远端，Phase 2.12 branch/tag 已在 backup2 固化。
- [Phase 2.13] 新增会议纪要 / 转写文本 ingestion MVP 规划，建议先处理 docx/txt/md 会议资料，不直接进入原始音频 ASR。
- [Phase 2.13] 完成会议纪要 / 转写文本 ingestion 首轮最小实现，真实会议纪要行动项、决策、风险检索通过，未污染主标书 evidence。
- [Phase 2.13] 修复会议纪要 trace 语义，transcript_as_fact 恒为 false，会议内容只作 retrieval evidence。
- [Phase 2.13] 真实终端验收通过：会议纪要绑定、行动项/决策/风险提取、主标书对比防污染均收口。
- [Phase 2.14] 完成企业记忆回归评测规划，建议先做 API 确定性评测，再补少量 Hermes CLI smoke。
- [Phase 2.14] 完成 API 级回归评测 runner 首轮实现，真实本地评测 10/10 通过，1 条 alias 用例跳过。
- [Phase 2.14b] 同步 CLI smoke 收口状态：Hermes 主仓库 live runner 4/4 通过，Hermes_memory 保持无状态。
- [Phase 2.15] 完成项目状态审计与路线裁决，建议下一阶段优先补 dense ingestion 与 hybrid 闭环。
- [Phase 2.16] 完成 dense ingestion 边界规划：上传链路当前未写 Qdrant，下一步限定为新上传 dense upsert 与显式文件池回填。
- [Phase 2.16] 完成新上传 dense ingestion 与显式 backfill 最小实现；答疑文件 12/12 回填成功，dense-only retrieval 已返回真实候选。
- [Phase 2.16] 登记 Rerank Smoke Audit 为后续独立尾项，本轮 dense ingestion 不混入 rerank 策略修改。
- [Phase 2.16] 完成 6 文件真实池 dense backfill，1360/1360 成功；hybrid smoke 全部命中目标文件，Phase 2.14 eval 复跑无回归。
- [Phase 2.17] 完成 Rerank Smoke Audit 与 dense/hybrid eval 扩展规划，下一步只验证可观测性和无污染，不改策略。
- [Phase 2.17] 完成 Rerank Smoke Audit runner 与 Phase 2.14 dense/hybrid eval 扩展；live smoke 5/5 通过，API eval 11/11 执行通过，未发现污染。
- [Phase 2.18] 完成下一阶段路线评审，建议优先进入权限与审计最小闭环；facts、增量更新、音频 ASR 与 rerank 质量评测后置。
- [Phase 2.18a] 完成权限与审计最小闭环：soft ACL 可过滤 evidence，audit log 写入可 fail-open，当前不做完整 RBAC/ABAC。
- [Phase 2.18a] 完成 live smoke：无 ACL、requester allow、tenant mismatch deny 与 audit_logs 三条写入均通过，可进入 Git baseline。
- [Phase 2.19] 完成版本治理路线裁决，建议优先做同名版本识别、latest 标记、superseded 诊断与默认 latest retrieval；facts 后置。
- [Phase 2.19a] 完成版本治理最小闭环：同名上传生成新版本，旧版本 superseded，默认检索 latest，显式 version_id 可查历史。
- [Phase 2.19a] 修复 OpenSearch 旧版本同步问题，supersede 时按 document_id+version_id 限定更新 is_latest=false，避免 sparse 泄露旧版本。
- [Phase 2.19a] 完成 live smoke 复验：默认 sparse/dense/hybrid 只返回 latest v2，显式旧 version_id 返回 v1，audit 默认 latest 只记录 v2。
- [Phase 2.19b] 同步 alias stale version 联调规划，Hermes_memory 保持版本治理 trace 输出，主仓库负责 alias 侧诊断与用户提示。
- [Phase 2.19b] 同步主仓库最小实现完成状态，alias stale version live smoke 已通过；Hermes_memory 不改 retrieval contract。
- [Phase 2.20] 完成治理类 eval 扩展规划：access/audit/version 进入 API deterministic eval，alias stale version 保持 CLI smoke。
- [Phase 2.20a] 完成治理类 eval 最小实现：API governance 5/5 通过，CLI stale alias smoke 5/5 通过；全量 core dense 失败另列尾项。
- [Phase 2.20a] 定位 full eval dense 假失败为本机 .env 指向旧 Qdrant collection；改回 hermes_chunks 后 full eval 16/16 通过。
- [Phase 2.21] 完成下一阶段路线裁决，建议优先进入 evidence-backed 结构化 facts 最小闭环。
- [Phase 2.21a] 完成 evidence-backed facts 最小实现，fact 必须绑定 source chunk/version/audit，默认 unverified。
- [Phase 2.21b] 完成 facts governance 边界规划，下一步只推进 facts eval、查询权限过滤与人工确认工作流，不让 facts 参与回答生成。
- [Phase 2.21b] 完成 facts eval 第一阶段实现，Phase 2.14 runner 新增 facts group，live eval 5/5 通过，full eval 21/21 执行通过。
- [Phase 2.21b] 完成 facts 查询权限过滤与 audit，source document ACL 可控制 fact 返回，denied fact 不泄露，full eval 无回归。
- [Phase 2.21b] 完成人工确认字段增强，confirm/reject 写入操作者、时间、拒绝原因与 audit，建议 Git baseline 后收口。
- [Phase 2.22] 完成 facts 使用路线裁决，建议先增强 facts 管理与确认查询入口，暂不让 facts 参与回答生成或自动抽取。
- [Phase 2.22a] 完成 facts 管理查询与 review history 最小实现，支持状态、来源、创建人、确认人过滤，权限与 audit 语义保持不变。
- [Phase 2.23] 完成 confirmed facts 使用路线裁决，建议先做只读检索与引用展示，不让 facts 直接进入 Agent 最终回答。
- [Phase 2.23a] 完成 confirmed facts 只读检索最小实现，返回 citation/stale 信息并写入 fact.search audit，仍不参与 Agent 回答。
- [Phase 2.24] 完成 facts 进入 Agent 上下文路线裁决，建议仅作为辅助上下文进入，并强制 facts_as_answer=false。
- [Phase 2.24a] 同步主仓库最小实现状态：confirmed facts 可作辅助上下文，但必须有 retrieval evidence，且 facts_as_answer=false。
- [Phase 2.24a] 同步终端验收修复：facts 独立分区，stale fact source 可检出，会议 transcript 不作为 facts。
- [Phase 2.24a] 同步二次修复：fact-only 与 stale 诊断无作用域时抑制 retrieval，防止无关文档污染。
- [Phase 2.24a] 同步 alias 绑定展示尾项修复，retrieval-only 场景稳定显示 facts false/[]/false。
- [Phase 2.24a] 同步 Codex C 真实终端复验通过结论，5 条验收全过，stale fact 检出且 facts_as_answer 恒 false。
- [Phase 2.25] 完成项目状态审计与路线裁决，建议下一阶段做 readiness audit 与数据维护诊断 dry-run，不直接 rollout 或自动抽取 facts。
- [Phase 2.25a] 新增只读 readiness audit runner，覆盖服务、版本、索引、dense、facts、audit 与 eval readiness；本机覆写 127 后 dry-run 为 warn，无失败。
- [Phase 2.26] 完成 repair plan dry-run 边界规划，下一步只生成不可执行修复计划，不修改 facts、索引或版本数据。
- [Phase 2.26a] 完成 repair plan dry-run 最小实现，已检出已知 stale fact，输出不可执行计划且无破坏动作。
- [Phase 2.26b] 完成报告归档路线规划，建议先沉淀 readiness 与 repair plan JSON 留痕，不进入 repair executor。
- [Phase 2.26b] 完成报告归档最小实现，临时目录 smoke 通过；真实 reports JSON 默认忽略，不入 Git。
- [Phase 2.27] 完成报告人工审阅流规划，建议先做本地 review record，不写 DB、不执行 repair。
- [Phase 2.27a] 完成 report review dry-run 最小实现，临时目录 smoke 通过；真实 review JSON 默认忽略。
- [Phase 2.27b] 完成 review audit 路线规划，建议先做 sanitized payload preview，不直接写 audit_logs。
- [Phase 2.28] 固化 Codex A/B/C 文件化交接协议，明确每轮读写状态文件、硬停止条件与 baseline 节奏。
- [Phase 2.28b] 新增 NEXT_CODEX_A_PROMPT 固定任务入口，后续 Codex A 可直接读取文件执行下一轮任务。
- [Phase 2.28c] 新增 Nightly Sprint 协议与队列，限定夜间只执行 bounded Green Lane 任务，禁止 repair 和 rollout。
- [Phase 2.27b] 按 NEXT_CODEX_A_PROMPT 完成 sanitized audit payload preview，单测与临时 smoke 均通过，未写 audit_logs。
- [Phase 2.27c] 夜间 Green Lane 完成真实写 audit_logs 路线规划，建议仅 report-level sanitized 写入且需显式授权。
- [Phase 2.27d] 完成 report-level sanitized audit 写入最小实现，默认 preview-only，显式 --write-audit 可写 audit_logs；临时 SQLite smoke 通过。
- [Phase 2.27e] 完成 review audit 是否纳入 readiness / eval 的路线规划，建议优先补安全断言与只读 readiness 检查。
- [Phase 2.27e] 完成最小实现：readiness audit 只读检查 report.review.created 脱敏摘要，26 条相关测试通过。
- [Phase 2.27f] 完成 archive / review / audit 关联诊断规划，建议先做只读链路摘要，不碰 DB 或 repair。
- [Phase 2.27f] 规划 baseline 收口，下一步需 Codex B 审核后再决定是否实现只读 linkage summary。
- [Phase 2.27f] 完成只读 linkage summary 最小实现，9 条单测与临时 smoke 通过，未写 DB 或 audit_logs。
- [Phase 2.27f] 修复 audit event 顶层 unsafe 字段漏检，顶层 document_id/fact_id/path 现在会 fail 且不泄露值。
- [Phase 2.27g] 完成 linkage readiness 路线规划，建议纳入 Phase 2.29 人工 freeze 清单，不默认扫描 reports。
- [Phase 2.27g] 进入 planning baseline 收口，下一步建议转入 Phase 2.29 MVP readiness freeze 规划。
- [Phase 2.29] 完成 MVP readiness freeze 路线规划，已冻结候选 MVP 能力、复验清单、人工验收项与 Go/No-Go 标准；建议下一步仅做 Phase 2.29a freeze checklist / freeze report dry-run，不进入 rollout。
- [Phase 2.29] planning baseline 收口，NEXT_CODEX_A_PROMPT 已推进为 Phase 2.29a freeze checklist / freeze report dry-run 入口。
- [Phase 2.29a] 完成 freeze report dry-run 最小实现，生成只读 MVP freeze report，显式读取 evidence JSON，默认不扫描真实 reports/reviews，不进入 rollout 或 repair executor；目标测试 8 passed。
- [Phase 2.29a] baseline 收口，NEXT_CODEX_A_PROMPT 已推进为 Phase 2.29b readiness freeze baseline decision planning 入口。
- [Phase 2.29b] 完成 readiness freeze baseline decision 路线规划，明确 pass/warn/fail 映射、No-Go 条件与最小 decision record 边界；仍不进入 rollout、repair 或 DB 写入。
- [Phase 2.29b] planning baseline 收口，NEXT_CODEX_A_PROMPT 已推进为 Phase 2.29b decision record dry-run 最小实现入口。
- [Phase 2.29b] 完成 decision record dry-run 最小实现：显式读取 freeze report JSON，pass/warn/fail 映射到 candidate/manual review/no-go，unsafe rollout/repair/destructive actions 强制 No-Go；目标测试 8 passed，临时 smoke 通过。
- [Phase 2.29b] Git baseline 收口准备完成：复跑 py_compile 与目标 pytest 8 passed，提交范围限定为 runner、测试和阶段文档，下一轮入口推进为 Phase 2.29c 路线规划。
- [Phase 2.29c] 完成 docs drift cleanup：TODO 中 rerank、dense ingestion、Aliyun provider smoke、audit_logs 的旧状态已改为历史状态并指向后续完成事实；Nightly Sprint Queue 已归档 Phase 2.27b/2.27c 旧队列并切换到当前 2.29 docs-only 队列。
- [Phase 2.29c] docs drift cleanup baseline 收口准备完成：未修改代码、脚本或测试，下一轮入口推进为 Phase 2.29d release candidate checklist planning。
- [Phase 2.29d] 完成 MVP freeze candidate 人工复核 / release candidate checklist 路线规划，明确 candidate 不等于 production rollout，checklist 只做只读证据、Go/No-Go、Codex B 审核与可选 Codex C 抽样复验。
- [Phase 2.29d] planning baseline 收口准备完成：提交范围限定为 release candidate checklist 规划与交接文档；下一步建议进入 Phase 2.29e checklist dry-run 最小实现规划 / 评审。
- [Phase 2.30a] 完成 Practical MVP Pilot Pack 文档：面向内部试运行整理标书审查、文件内容提取、公司方向辅助分析三类 playbook 与 12 条 Codex C 真实终端验收 query；本轮 docs-only，不进入 rollout。
- [Phase 2.30a] Codex C 完成 12 条 Pilot 真实终端验收：4 pass、8 partial、0 failed；核心业务能力可用但 alias/session 不稳定阻塞试用，下一步进入 Phase 2.30b alias / session stability fix。
- [Phase 2.30b] 主仓库完成 alias/session 最小修复：标题类 alias 绑定在 resolver 未命中时不再 suppress retrieval，可通过同轮唯一 retrieval evidence 完成 alias bind；direct assertion tests 48 个测试函数通过。
- [Phase 2.30b] 完成 Codex B follow-up：补齐无书名号 / 自然语言 alias bind 识别，覆盖会议纪要、硬件清单、C塔方案与当前主标书 runbook prompt；direct assertion tests 53 个测试函数通过。
- [Phase 2.30b] Codex C 真实终端复验通过：12 条 Pilot query 为 10 pass、2 partial、0 failed；四个 alias 后续 query 均稳定，未出现 alias_missing / retrieval_suppressed 误阻断，建议 baseline 并进入内部受控 MVP Pilot。
- [Phase 2.31] 完成内部受控 MVP Pilot 操作规划，新增试用流程、使用者指南、反馈模板与 known risks checklist；本轮 docs-only，不写代码、不运行测试、不进入 production rollout。
- [Phase 2.31] Codex B review 确认 Pilot ops 文档可 baseline，并补强 Nightly Sprint 启动入口：新增 NIGHTLY_CODEX_A_PROMPT，澄清协议文件不会自动唤醒 Codex A，队列改为可执行 docs-only baseline + feedback intake planning。
- [Phase 2.31] Nightly Sprint Item 1 docs-only baseline 已完成，commit 184533a，tag phase-2.31-pilot-ops-nightly-launcher-baseline，已推送 origin/main 与 tag。
- [Phase 2.32] 完成 MVP Pilot feedback intake planning，定义反馈来源、triage 字段、P0/P1/P2/P3、Go / No-Go 与非目标；本轮 docs-only，不写代码、不提交 Git、不进入 rollout。
- [Phase 2.32] docs baseline 已完成：commit 160ce62，tag phase-2.32-feedback-intake-plan-baseline；下一步推进 Phase 2.33 Day-1 Pilot run sheet，不进入 rollout。
- [Phase 2.33] 完成 Day-1 Pilot execution packet planning，新增 run sheet、10 条最小 query set、输出保存字段、人工复核规则与 Go / Pause 检查点；本轮 docs-only，不写代码、不提交 Git、不进入 rollout。
- [Phase 2.33] Codex B 已审核 Day-1 run sheet，当前执行 docs-only baseline；提交范围限定为 run sheet 与交接文档，不写代码、不进入 rollout。
- [Phase 2.33] Day-1 run sheet baseline 已完成：commit `bb9656b`，tag `phase-2.33-pilot-day1-run-sheet-baseline`，已推送 `origin/main` 与 tag。
- [Phase 2.34] Codex B 吸收 Codex C Day-1 真实终端报告：10 条 query 为 `7 pass / 3 partial / 0 fail`，P0 为 `0`，alias/session 稳定，无 facts 替代 evidence，无 transcript_as_fact，无实际第三文件污染。
- [Phase 2.34] 当前 bounded fix 入口已写入 `docs/NEXT_CODEX_A_PROMPT.md`：优先修复 `@会议纪要 vs @主标书` compare 输出层误报 `third_document_mixed=true`；主标书深层字段召回与长输出延迟进入 backlog，不在本轮扩大。
- [Phase 2.34] 完成 compare false-positive 最小修复：最终 evidence 在 compare 文档集合内时不再输出第三文件污染；真实 scope 外 evidence 仍会标记；主标书深层召回与延迟优化未扩做。
- [Phase 2.34] Git baseline 完成：Hermes_memory commit `789ed22`，Hermes 主仓库 commit `5de49bf5`，tag `phase-2.34-compare-contamination-baseline`。
- [Phase 2.35] Codex B 已写入主标书深层字段召回专项入口：优先处理最高投标限价 / 招标控制价、资质 / 项目经理 / 联合体 / 业绩 / 人员等 Day-1 P1 字段；本阶段只改善 retrieval evidence，不进入自动审标或 rollout。
- [Phase 2.34] Codex C 真实终端复验通过：`@会议纪要 vs @主标书` compare evidence 仅含两份目标文档，`third_document_mixed=false`，无第三文件污染误报；facts/transcript 边界抽样正常。
- [Phase 2.35] 完成主标书深层字段召回最小实现：新增 price ceiling 与 qualification deep-field metadata anchors，扩展最高投标限价 / 招标控制价 / 资质 / 项目经理 / 联合体 / 业绩 / 人员要求的 section hints 与 phrase boosts，并新增 deep-field trace；目标测试 22 passed，等待 Codex B review 与 Codex C Q1/Q2 复验。
- [Phase 2.35] Codex C 真实终端复验显示安全边界通过但效果仍 partial：最高投标限价仍 Missing Evidence，具体资质等级未命中，项目经理 / 联合体 / 业绩 / 人员要求需人工复核；首次 session 出现 alias 绑定后丢失，第二次 session 正常。
- [Phase 2.35b] Codex B 已写入 bounded follow-up：对齐 `deep_field_profile` trace，增强 price ceiling / qualification metadata precision，并诊断 alias 首次绑定不稳定；暂不 baseline，不进入 rollout。
- [Phase 2.35b] 完成 bounded follow-up 最小实现：`SearchResponse.trace` 顶层新增 metadata profile/status 字段；限价 metadata strong match 要求具体金额，资质 metadata strong match 要求具体等级 + 类别；目标测试 26 passed，`git diff --check` 通过。
- [Phase 2.35b] 完成主仓库 alias 首次绑定诊断：`.venv` 缺 pytest，改用 direct assertion diagnostics，alias bind / persistence / same-turn retrieval fallback 相关 10 个路径通过，未复现首次绑定丢失，未修改主仓库代码。
- [Phase 2.35c] Codex C 真实 CLI 复验复现阻塞：`@主标书` binding turn 返回成功且 document/version 正确，但正式 Q1/Q2 均变为 `alias_missing=true / retrieval_suppressed=true`，未进入 retrieval；当前不建议 Phase 2.35b baseline。
- [Phase 2.35c] Codex B 已写入下一轮主仓库 alias/session 最小修复入口，限定修复 bind success 后同 session 后续 query 丢失问题；不扩大 deep-field retrieval、不进入自动审标或 rollout。
- [Phase 2.35c] 完成主仓库 alias/session 最小修复：`上一轮已锁定的当前文件` 类绑定提示进入 current-document bind / retrieval fallback，并通过 direct assertion 覆盖跨 store resume 与 run_agent 预解析路径。
- [Phase 2.35c] Codex C 真实终端复验通过：`@主标书` bind 后 Q1/Q2 均为 alias_resolved 且未 suppressed；限价金额、具体资质等级、业绩与人员要求仍为 retrieval recall / Missing Evidence 尾项。
- [Phase 2.36] 完成主标书 deep-field recall tail planning，将限价、资质、项目经理、联合体、业绩、人员与 trace 展示缺口分类为真实缺字段 / 章节召回不足 / trace polish / 人工确认，并建议 2.36a 先做 trace + diagnostics。
- [Phase 2.36a] 完成 retrieval-layer trace polish + section diagnostics：新增 `deep_field_missing_reason` / `deep_field_diagnostics`，区分 concrete price / qualification evidence 与 Missing Evidence；目标测试 `17 passed`，未做真实 CLI smoke。
- [Phase 2.36b] 完成主仓库 trace display / alias prompt 最小修复：deep-field trace 从 Hermes_memory retrieval trace 提升到顶层并进入 context block；`锁定“标题”，并绑定为 @alias` 可识别为 alias bind；主仓目标测试 `59 passed`。
- [Phase 2.36c] 完成 diagnostics / answer boundary 语义一致性修复：限价 concrete evidence 需最终 retrieval evidence 含具体金额，电子证书格式条款不再推断为项目经理等级；目标测试 `33 passed`。
- [Phase 2.36c] Codex B review 与 Codex C 真实终端复验均已通过：Step 1 alias binding 成功，Q1 限价 diagnostics 与 Missing Evidence 一致，Q2 项目经理等级边界正确；当前进入 Git baseline，不进入自动审标或 rollout。
- [Phase 2.37] Codex B 已写入 MVP Pilot issue intake / triage planning 入口：下一步先结构化记录真实试用反馈与 P0/P1/P2/P3 分流，不直接进入自动修复、自动审标或 rollout。
- [Phase 2.37] 完成 Pilot issue intake / triage 路线规划，推荐 Phase 2.37a 先做 local issue schema、template 与 dry-run validator / summary generator；deep-field recall 尾项进入 issue 分流，不直接盲修。
- [Phase 2.37] planning baseline 已完成：commit `8fd10b7`，tag `phase-2.37-pilot-issue-triage-plan-baseline`，已推送 origin/main 与 tag。
- [Phase 2.37a] Codex B 已写入下一轮执行入口：实现 local issue intake schema / template / dry-run validator + summary generator；本阶段仍禁止 DB 写入、外部 issue 自动创建、repair、rollout 与自动审标。
- [Phase 2.37a] 完成 local issue intake dry-run 最小实现：支持 template、单文件 / 目录 JSON 读取、schema / enum 校验、triage summary 与 strict invalid exit；目标测试 `9 passed`，临时 dry-run smoke 通过。
- [Phase 2.37a] Git baseline 已完成：commit `1e1ca45`，tag `phase-2.37a-pilot-issue-intake-baseline`。
- [Phase 2.37b] 完成 Pilot issue intake runbook 与本地存储约定：`reports/pilot_issues/*.json` / `*.md` 默认 ignored，真实试用反馈不入 Git；template / strict dry-run 验证通过。
- [Phase 2.37b] Git baseline 已完成：commit `e8c0631`，tag `phase-2.37b-pilot-issue-intake-runbook-baseline`。
- [Phase 2.37c] 完成 Pilot issue triage summary 路线规划：后续可将本地 issue records 汇总为 ignored daily / per-round summary，P0 pause、P1 进入 bounded fix planning 候选、P2/P3 入 backlog / polish；本轮 planning-only，未创建真实 issue records。
- [BIM Data Steward] 完成 PRD / Roadmap / Technical Design 轻量扩展规划：新增 BIM 文件资产目录治理方向，明确初期只做项目、楼栋、楼层、专业、版本、路径、hash、责任人、权限标签和派生元数据管理，不并入当前 MVP Pilot，不做 TB 级原始模型全量解析、在线查看、碰撞检测、自动算量或自动设计审查。
- [Phase 2.37d] 完成本地 Pilot issue triage summary generator：读取 `reports/pilot_issues/*.json`，输出 dry-run summary 与 ignored JSON/Markdown；目标测试 9 passed，未创建真实 issue、未写 DB、未进入 repair 或 rollout。
- [Phase 2.38a] 完成 Tender P1 source availability audit 最小实现：新增只读 runner 与目标测试 10 passed；live dry-run 因本机 `postgres` 主机名不可解析返回 skipped_live_unavailable，未写 DB、未改索引、未生成真实报告。
- [Phase 2.38b] 完成 Tender P1 concrete source recall diagnostics 最小实现：新增只读 runner 与目标测试 9 passed；localhost read-only preview 显示资质 / 业绩 candidate 在 top-k，人员 candidate 低排名，限价继续 Missing Evidence，项目经理等级继续人工复核。
- [Phase 2.38b] Codex B review 通过：复跑 py_compile、目标 pytest 9 passed、git diff --check 与 ignore 检查均通过；localhost read-only preview 复核显示人员要求 candidate 低排名，下一步只做 Git baseline。
- [Phase 2.38b] Git baseline 已完成：commit `a8c93f1`，tag `phase-2.38b-tender-recall-diagnostics-baseline`，已推送 origin/main 与 tag。
- [Phase 2.38c] Codex B 已写入下一轮 planning 入口：只规划 `personnel_requirement` 低排名尾项，不写代码、不改 retrieval、不进入 rollout。
- [Phase 2.38a] Git baseline 已完成：commit `456b32d`，tag `phase-2.38a-tender-p1-source-audit-baseline`。
- [Phase 2.38b] Codex B 补做 localhost 覆写 read-only live audit preview：限价为 anchor_only，项目经理等级为 ambiguous，资质 / 业绩 / 人员为 concrete_source_found；下一步只做 concrete source recall diagnostics，不直接修 retrieval ranking。
- [Phase 2.38c] 完成人员要求召回尾项规划：人员 candidate 已存在但低排名，推荐后续仅做 personnel-only aliases / section hints / candidate-pool diagnostics，不处理限价、项目经理等级、broad retrieval tuning 或 rollout。
- [Phase 2.38c] Codex B review 通过：规划限定为 docs-only，`git diff --check` 通过；下一步只做 docs baseline，不直接进入 2.38d。
- [Phase 2.38c] 执行 docs-only Git baseline：提交范围限定为 Phase 2.38c 规划与交接文档；不写代码、不运行 pytest、不进入 2.38d。
- [Phase 2.38d] 完成人员要求低排名最小实现：新增 `personnel_scope`、人员 aliases / section hints / boosted phrases 与 diagnostics expanded query；目标测试 28 passed，新增测试 6 passed，未运行 DB-backed live preview。
- [Phase 2.38c] Git baseline 已完成：commit `ff49941`，tag `phase-2.38c-personnel-recall-tail-plan-baseline`，`origin/main` 对齐。
- [Phase 2.38d] Codex B 已写入下一轮执行入口：只处理 `personnel_requirement` low-rank 的 personnel-only bounded recall implementation；不处理限价、项目经理等级、broad retrieval tuning、repair、reindex 或 rollout。
- [Phase 2.38d] Codex B review 未通过：`personnel_scope` 首轮实现仍让 personnel-focused query 混入 broad qualification aliases / sections（如项目经理、联合体、类似业绩）；已写入最小 review-fix prompt。
- [Phase 2.38d] 完成 review-fix：personnel-focused query 现在按人员 allowlist 收敛 aliases / sections，不再混入项目经理、联合体、类似业绩、资信标等 broad qualification 信号；目标测试 28 passed，等待 Codex B 复审。
- [Phase 2.38d] Review-fix 通过 Codex B 复审：personnel-focused query 不再混入 broad qualification aliases / sections，broad qualification query 仍保持 `qualification_scope`；下一步建议 Codex C 定向复验 Q2 人员要求。
- [Phase 2.38d] Codex C 定向复验反馈：Q2 人员要求与 Q3 broad query 通过；Q1 带“不要回答投标资质、项目经理、联合体、业绩”的人员 query 仍落到 `qualification_scope`。Codex B 已写入下一轮 bounded fix，只处理否定/排除句 intent parsing。
- [Phase 2.38d] 完成 Q1 intent fix：`不要回答...` / `不回答...` 等排除语中的资质、项目经理、联合体、业绩不再触发 `qualification_scope`；Q1/Q2 为 `personnel_scope` 且 metadata fields 仅 `personnel_requirement`，Q3 broad query 仍为 `qualification_scope`；目标测试 30 passed。
- [Phase 2.38d] Q1 intent fix 通过 Codex B 复审：带“不要回答投标资质、项目经理、联合体、业绩”的人员 query 现在保持 `personnel_scope` 且 metadata fields 仅 `personnel_requirement`；下一步需 Codex C 重跑 Q1/Q2/Q3 真实终端复验。
- [Phase 2.38d] Codex C 复验显示 retrieval / trace 层已修复但最终回答边界仍过度表述；主仓库补 `personnel_scope` answer-boundary context，禁止 personnel-only 回答混入项目经理 / 注册建造师 / B证或推断“每类1人”；主仓目标测试 `11 passed`，等待 Codex B review 与 Codex C Q1/Q2/Q3 复验。
- [Phase 2.38d] Codex C 第二轮复验仍显示 final answer guard 不够硬：Q1/Q2 会输出项目经理 / 每个项目只能1个 / 类似工程业绩。主仓库已将 `personnel_answer_boundary` 强化为 strict guard，并补 broad qualification 不误套 personnel boundary 测试；主仓目标测试 `12 passed`。
- [Phase 2.38d] 第三轮最小修复按 NEXT_CODEX_A_PROMPT 执行：在主仓 `personnel_scope` context 中补 `personnel_forbidden_answer_terms`、`personnel_count_inference_forbidden=true`、`ignore_non_personnel_content_in_mixed_chunks=true`；未改 retrieval / DB / 索引，主仓目标测试 `12 passed`。
- [Phase 2.38d] 第四轮最小修复补 safe fallback contract：违规答案草稿需丢弃并输出 Missing Evidence / 人工复核模板；因本轮白名单不含 `run_agent.py`，未接入真正 post-answer retry / replacement，仍需 Codex C 复验。
- [Phase 2.38d] 第五轮最小修复已接入 runtime post-answer guard：`personnel_scope` + personnel-only query 的最终回答若含禁词或隐式数量推断，会替换为 Missing Evidence / 人工复核 fallback；主仓 py_compile 通过，目标测试 `65 passed`，等待 Codex B review 与 Codex C Q1/Q2/Q3 复验。
- [Phase 2.38d] Codex C 真实终端复验通过：Q1/Q2 personnel-only safe fallback 触发且无禁词 / 数量推断，Q3 broad qualification 未被压扁；本轮执行 Phase 2.38d Git baseline，Data Steward dirty 单独后置。
- [Phase 2.39] Data Steward 后置产品线规划已落到 PRD / Roadmap / Technical Design：BIM 是首个高价值垂直场景，当前只做资产目录、本体、知识图谱、空间索引和子 Agent 监控的产品规划，不并入 Phase 2.38d 或 MVP Pilot。
- [Phase 2.39] 新增 `docs/PHASE239_DATA_STEWARD_PRODUCT_PLAN.md`：明确 Data Steward 可作为楼宇 / 园区 / 项目数据管家应用对外封装，但当前不做全量 BIM 解析、在线查看器、碰撞检测、自动算量、自动设计审查、Neo4j/PostGIS/schema 或 scheduler 实现。
- [Phase 2.39] 执行 docs-only baseline：复核 Data Steward / 数据管家术语与边界，不写功能代码、不运行 pytest、不进入 Data Steward 实现；下一步建议 PRD Acceptance Matrix / MVP Evidence Pack planning。
- [Phase 2.40] 完成 PRD Acceptance Matrix / MVP Evidence Pack docs-only planning：定义 done / partial / planned / deferred 状态、evidence_ref、known_gap、not_claimable 字段；明确不可宣称 production rollout ready、自动审标、repair executor ready、facts 自动抽取或替代 evidence、Data Steward 已实现、TB BIM 全量解析等能力。
- [Phase 2.40a] 完成 PRD Acceptance Matrix / MVP Evidence Pack docs-only artifact：新增 `docs/PRD_ACCEPTANCE_MATRIX.md`，按能力域列出 status、evidence、known gap、next phase candidate 与 not claimable；明确当前可内部受控 Pilot，但不是 production rollout。
- [Phase 2.41] 完成 MVP Pilot Evidence Review / Go-No-Go docs-only planning：新增 `docs/PHASE241_MVP_PILOT_EVIDENCE_REVIEW_PLAN.md`，定义 Go / Pause / No-Go、P0/P1/P2/P3 handling、人工复核要求与 not-claimable checklist；不写代码、不运行 API/CLI、不进入 rollout。
- [Phase 2.41a] 完成 MVP Pilot Evidence Review Checklist docs-only artifact：新增 `docs/MVP_PILOT_EVIDENCE_REVIEW_CHECKLIST.md`，用于人工填写 Go / Pause / No-Go、P0/P1、evidence policy、citation、governance、human review 与 not-claimable；本轮不写代码、不运行 API/CLI、不提交 Git。
- [Phase 2.42] 完成 MVP Pilot Review Dry-run Report docs-only planning：新增 `docs/PHASE242_MVP_PILOT_REVIEW_DRY_RUN_PLAN.md`，规划后续只读 report 的输入、输出、Go/Pause/No-Go decision logic、P0/P1/P2/P3 aggregation、evidence policy、citation 与 Missing Evidence summary；不写代码、不生成真实 report、不进入 rollout。
- [Phase 2.42a] 完成 MVP Pilot Review Dry-run Report Generator 最小实现：新增显式输入、本地只读 generator 与目标测试，真实 report JSON / Markdown 默认 ignored；不扫描真实 reports / reviews，不运行 API/CLI，不进入 rollout 或 repair。
- [Phase 2.42b] 完成 MVP Pilot Review Dry-run sanitized input template 与 runbook artifact：模板只含占位符，runbook 说明人工整理输入、dry-run 命令与 Go/Pause/No-Go 解读；本轮不生成真实 report、不运行 API/CLI、不写 DB、不进入 rollout、repair 或 Data Steward 实现。
- [Phase 2.43] 完成 Internal MVP Pilot Launch Candidate docs-only planning：串联 runbook、user guide、Day-1 run sheet、feedback template、evidence review checklist、dry-run report runbook / template 与 PRD acceptance matrix；本轮不启动真实 Pilot、不生成真实 report、不运行 API/CLI、不写 DB、不进入 rollout、repair 或 Data Steward 实现。
- [Phase 2.43a] 完成 MVP Pilot Launch Packet / Operator Checklist artifact：新增内部受控 Pilot 操作包，覆盖角色、启动前 checklist、session execution、evidence review、Go / Pause / No-Go、输出归档、人工决策声明、停止条件与后续流转；本轮不启动真实 Pilot、不生成真实 report、不运行 API/CLI、不写 DB、不进入 rollout、repair 或 Data Steward 实现。
- [Phase 2.43a] Git baseline 已完成：commit `5423497`，tag `phase-2.43a-mvp-pilot-launch-packet-baseline`，`origin/main` 对齐；保留遗留无关 dirty `docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md`。
- [Phase 2.43b] Codex B 已写入下一轮 docs-only artifact 入口：新增 Codex C MVP Pilot pre-flight smoke prompt / runbook，先验收 API / CLI、alias/session、citation、evidence policy、Missing Evidence 与 No-Go / Pause / Go 边界，不启动真实 Pilot。
- [Phase 2.43b] 完成 MVP Pilot pre-flight smoke prompt / runbook artifact：新增 `docs/MVP_PILOT_PREFLIGHT_SMOKE_PROMPT.md`，覆盖 Codex C API / CLI 预检、alias 绑定、主标书 / structured citation / 会议纪要 / facts 边界 / compare 小样本、P0/P1/P2/P3 与 Go / Pause / No-Go 规则；本轮不运行真实 API / CLI、不生成真实 report、不上传、不写 DB / facts / document_versions / OpenSearch / Qdrant、不进入 rollout、repair 或 Data Steward 实现。
- [Phase 2.43b] Codex B review 通过：pre-flight smoke prompt 覆盖 Codex C 真实终端验收边界、query subset、P0 / P1 / P2 / P3、No-Go / Pause / Go 与 no-data-write；下一步只做 Git baseline，不自动发起 Codex C。
- [Phase 2.43b] Git baseline 已完成：commit `ef2e43f`，tag `phase-2.43b-mvp-pilot-preflight-smoke-prompt-baseline`，`origin/main` 对齐。
- [Phase 2.43c] Codex C pre-flight smoke 返回 `Go`：API / CLI 可用，四个 alias 稳定，P0 为 0；P1 保留主标书限价 Missing Evidence，P2 保留部分 trace display；下一步可启动内部受控 MVP Pilot Day-1，不等于 production rollout。
- [Phase 2.43c] Day-1 Pilot 按 run sheet 触发 `Pause`：session `20260506_132914_521b45` 中 `@主标书` 绑定阶段出现 `alias_bind_failed`，正式 Q1 变成 `alias_missing=true / retrieval_suppressed=true`，Q2-Q10 未继续执行；`@硬件清单`、`@C塔方案`、`@会议纪要` 均绑定稳定。
- [Phase 2.43d] Codex B 已写入下一轮 bounded fix 入口：只修 `@主标书` alias/session Pause blocker，不处理限价 Missing Evidence、资质等级、深层召回、repair、rollout 或 Data Steward。
- [Phase 2.43d] Codex A 完成 bounded fix：`alias_bind_pending_current_retrieval` 在 retrieval 返回多个候选时采用 top document 完成绑定并记录 `alias_bind_ambiguous_retrieval_document_ids`，同时保留 title bind 多候选失败语义；主仓 session scope 测试 `51 passed`，等待 Codex B review 与 Codex C 复验。
- [Phase 2.43d] Codex B review 通过并新增 `docs/NEXT_CODEX_C_PROMPT.md`：下一步只做 Codex C Day-1 Q1 alias/session 真实终端复验，不 baseline、不 rollout、不 repair。
- [Phase 2.43d] Codex C Day-1 断点续跑通过：`@主标书` Q1-Q2 resolved，`alias_missing=false`，`retrieval_suppressed=false`；Day-1 10 条 query 为 `6 pass / 4 partial / 0 fail`，P0 为 0，Decision 为 `Go`；下一步只做双仓 Git baseline。
- [Phase 2.43d] 双仓 Git baseline 已完成：Hermes_memory commit `d62852b`，Hermes 主仓库 commit `9e8e5667`，tag `phase-2.43d-main-tender-alias-session-baseline`；`@主标书` alias/session Pause blocker 收口。
- [Phase 2.44] Codex B 已写入下一轮 docs-only planning 入口：将 Day-1 continuation 的 P1/P2 尾项转为 MVP Pilot continuation / issue intake plan；不写代码、不生成真实 issue records、不进入 repair、rollout 或 Data Steward。
- [Phase 2.44] 完成 MVP Pilot continuation / issue intake docs-only planning：新增 `docs/PHASE244_MVP_PILOT_CONTINUATION_ISSUE_INTAKE_PLAN.md`，记录 Day-1 issue candidates、Go / Pause / No-Go、人工复核责任与下一阶段候选；本轮未生成真实 issue records / Pilot report，未写 DB / facts / document_versions / OpenSearch / Qdrant，未进入 repair、rollout 或 Data Steward。
- [Phase 2.44] Codex B review 通过：规划边界正确，符合内部受控 MVP Pilot continuation / issue intake，不进入实现、真实 report、真实 issue records、repair、rollout 或 Data Steward；下一步只做 docs-only Git baseline。
- [Phase 2.44a] 完成 MVP Pilot Day-1 issue intake worksheet / sanitized template artifact：新增人工 worksheet 与脱敏 JSON template，覆盖 Day-1 P1/P2 quick-fill、validator-compatible issue_type 映射、P0/P1/P2/P3、Go / Pause / No-Go 与 strict validator 命令；本轮未生成真实 issue records / Pilot report，未运行 API / CLI，未写 DB / facts / document_versions / OpenSearch / Qdrant，未进入 repair、rollout 或 Data Steward。
- [Phase 2.44] Git baseline 已完成：commit `afb5a29`，tag `phase-2.44-pilot-continuation-issue-intake-plan-baseline`；下一步转入 Phase 2.44a issue intake worksheet / sanitized template artifact，不进入 retrieval fix、repair、rollout 或 Data Steward。
- [Phase 2.44a] Codex B 已写入下一轮 artifact 入口：新增 Day-1 issue intake worksheet 与 sanitized JSON template，供人工 recorder 后续整理 ignored local issue records；本阶段不生成真实 issue records / Pilot report。
- [Phase 2.44a] Codex B review 通过：worksheet / sanitized template 边界正确，template 通过 `phase237a_pilot_issue_intake.py --input ... --strict`，可进入 docs-only Git baseline。
- [Phase 2.44a] Git baseline 已完成：commit `14c5640`，tag `phase-2.44a-pilot-issue-intake-worksheet-baseline`；下一步转入 Phase 2.44b sanitized issue intake dry-run / recorder workflow planning，不生成真实 issue records / Pilot report。
- [Phase 2.44b] 完成 sanitized issue intake dry-run / recorder workflow docs-only planning：新增 `docs/PHASE244B_SANITIZED_ISSUE_INTAKE_DRY_RUN_PLAN.md`，明确输入脱敏、recorder workflow、strict validation commands、本地 ignored storage、review gate 与 stop conditions；本轮未写代码、未生成真实 issue records、未运行 API / CLI、未写 DB / facts / document_versions / OpenSearch / Qdrant，未进入 repair、rollout 或 Data Steward。
- [Phase 2.44a] Git baseline 已完成：commit `14c5640`，tag `phase-2.44a-pilot-issue-intake-worksheet-baseline`；worksheet 与 sanitized JSON template 已固化，未生成真实 issue records / Pilot report。
- [Phase 2.44b] Codex B 已写入下一轮 docs-only planning 入口：规划 sanitized issue intake dry-run / recorder workflow；只定义人工 recorder 如何整理脱敏输入和后续 dry-run，不生成真实 records、不修 retrieval、不进入 rollout / repair / Data Steward。
- [Phase 2.44b] Codex B review 通过：planning 明确 sanitized input、recorder workflow、strict validation、ignored local storage、review gate 与 stop conditions；下一步只做 docs-only Git baseline，不进入真实 issue generation、retrieval fix、repair、rollout 或 Data Steward。
- [Phase 2.44b] Git baseline 已完成：commit `0241c4d`，tag `phase-2.44b-sanitized-issue-intake-dry-run-plan-baseline`；下一步转入 Phase 2.44c fake/temp-data dry-run artifact，不使用真实 Pilot raw output。
- [Phase 2.44c] 完成 fake-data sanitized issue intake dry-run artifact：新增 fake issue input 与 dry-run runbook，使用现有 `phase237a_pilot_issue_intake.py` strict validator 验证通过，`total=2`、`valid_records=2`、`invalid_count=0`、`go_pause_recommendation=continue_with_manual_review`；本轮未生成真实 issue records / Pilot report，未运行 API / CLI，未写 DB / facts / document_versions / OpenSearch / Qdrant，未进入 repair、rollout 或 Data Steward。
- [Phase 2.44c] Codex B 已写入下一轮 artifact 入口：新增 fake issue input 与 dry-run runbook，使用现有 `phase237a_pilot_issue_intake.py` 验证 workflow；不生成真实 issue records、不扫描真实 reports、不进入 rollout / repair / Data Steward。
- [Phase 2.44c] Codex B review 通过：fake issue input 完全使用 placeholder alias/document/version/citation/source location/sanitized behavior，strict validator 通过，`continue_with_manual_review` 明确不是 rollout approval；下一步只做 docs-only Git baseline。
- [Phase 2.44c] Git baseline 已完成：commit `cb29ed4`，tag `phase-2.44c-fake-issue-intake-dry-run-baseline`；下一步转入 Phase 2.44d planning，评估 explicit ignored local input 是否可用于真实 recorder workflow dry-run。
- [Phase 2.44d] Codex B 已写入下一轮 docs-only planning 入口：只评估后续是否允许人工 recorder 创建 ignored local issue input；本轮不生成真实 issue records、不扫描真实 reports、不进入 rollout / repair / Data Steward。
- [Phase 2.44d] 完成 explicit ignored local issue input dry-run route planning：新增 `docs/PHASE244D_EXPLICIT_LOCAL_ISSUE_DRY_RUN_PLAN.md`，明确后续真实 recorder workflow dry-run 必须用户显式授权、人工准备、路径明确且 Git ignored；本轮未生成真实 issue records / Pilot report，未扫描真实 reports/reviews，未运行 API / CLI，未写 DB / facts / document_versions / OpenSearch / Qdrant，未进入 repair、rollout 或 Data Steward。
- [Phase 2.44d] Codex B review 通过：explicit local input 前置条件、local-only 字段、recorder workflow、validation commands、review gate、Git/storage policy 与 stop conditions 边界清楚；下一步只做 docs-only Git baseline，不进入 Phase 2.44e，不生成真实 issue records / Pilot report。
- [Phase 2.44d] Git baseline 已完成：commit `dcdb7b4`，tag `phase-2.44d-explicit-local-issue-dry-run-plan-baseline`；下一步转入 Phase 2.45 Mac mini MVP server deployment planning，不执行真实部署、不进入 production rollout。
- [Phase 2.45] Codex B 已写入下一轮 docs-only planning 入口：规划 Mac mini M4 / 24GB / 512GB / 10GbE 作为公司内部 Hermes MVP 节点的部署封装、热更新、NAS / 外接 SSD 边界、health check 与 smoke checklist；不写代码、不运行 API / CLI、不进入 Data Steward 或 production rollout。
- [Phase 2.45] Codex B review 通过：Mac mini MVP server planning 保持 internal controlled MVP server 边界，服务拓扑、NAS / 外接 SSD、热更新、health / smoke、备份 / 回滚与 stop conditions 清楚；下一步只做 docs-only Git baseline，不进入真实部署或 Phase 2.45a。
- [Phase 2.45] 完成 Mac mini MVP server deployment docs-only planning：新增 `docs/PHASE245_MAC_MINI_MVP_SERVER_PLAN.md`，明确服务拓扑、目录策略、NAS / 外接 SSD 边界、环境变量 / secrets checklist、开发机 -> Git -> Mac mini 热更新流程、health / smoke、备份 / 回滚与 stop conditions；本轮未写代码、未新增 deployment script、未运行 API / CLI、未执行真实部署、未写 DB / facts / document_versions / OpenSearch / Qdrant，未进入 production rollout 或 Data Steward。
- [Phase 2.45] Git baseline 已完成：commit `fa6aff4`，tag `phase-2.45-mac-mini-mvp-server-plan-baseline`；下一步转入 Phase 2.45a Mac mini MVP deployment runbook artifact，不执行真实部署、不新增 deployment script。
- [Phase 2.45a] Codex B 已写入下一轮 docs-only artifact 入口：新增 Mac mini MVP deployment runbook / checklist，覆盖 Day-0 准备、目录创建、服务启动顺序、热更新、smoke、备份 / 回滚、stop conditions 与 operator sign-off；不写代码、不运行 API / CLI、不进入 production rollout。
- [Phase 2.45a] Codex B review 通过：deployment runbook 是人工 checklist，不是 deployment script 或 production rollout；覆盖 Day-0、目录、env/secrets、service order、hot update、smoke、backup/rollback、stop conditions 与 operator sign-off；下一步只做 docs-only Git baseline。
- [Phase 2.45a] 完成 Mac mini MVP deployment runbook artifact：新增 `docs/MAC_MINI_MVP_DEPLOYMENT_RUNBOOK.md`，覆盖 Day-0 准备、目录创建、环境变量与 secrets、repo checkout、服务启动顺序、部署 / 热更新、minimum smoke、备份 / 回滚、stop conditions 与 operator sign-off；本轮未写代码、未新增 deployment script、未运行 API / CLI、未执行真实部署、未写 DB / facts / document_versions / OpenSearch / Qdrant，未进入 production rollout 或 Data Steward。
- [Phase 2.45a] Git baseline 已完成：commit `585d534`，tag `phase-2.45a-mac-mini-deployment-runbook-baseline`；下一步转入 Phase 2.45b health-check / deploy-smoke dry-run planning，不新增脚本、不运行真实 API / CLI。
- [Phase 2.45b] Codex B 已写入下一轮 docs-only planning 入口：规划只读 health-check / deploy-smoke dry-run 检查项、输出 schema 与 stop conditions；不写代码、不新增 health-check script、不运行 API / CLI、不执行真实部署。
- [Phase 2.45b] 完成 health-check / deploy-smoke dry-run docs-only planning：新增 `docs/PHASE245B_HEALTH_CHECK_DRY_RUN_PLAN.md`，规划 Git / env key / storage mounts / service reachability / ignored runtime path 检查、MVP smoke candidates、JSON output schema、stop conditions 与 human-only / future bounded script 边界；本轮未写代码、未新增脚本、未运行 API / CLI、未执行真实部署、未写 DB / facts / document_versions / OpenSearch / Qdrant。
- [Phase 2.45b] Codex B review 通过：planning 边界正确，保持 read-only / no deployment / no script / no API/CLI smoke / no DB-index writes / no rollout / no Data Steward；下一步只做 docs-only Git baseline。
- [Phase 2.45b] Git baseline 已完成：commit `d70497c`，tag `phase-2.45b-health-check-dry-run-plan-baseline`；下一步转入 Phase 2.45c read-only health-check script 最小实现，不执行真实部署、不运行真实 API / CLI smoke。
- [Phase 2.45c] Codex B 已写入下一轮实现入口：新增只读 health-check dry-run runner 与单元测试；默认不访问真实 API / CLI，不写 DB / facts / document_versions / OpenSearch / Qdrant，不进入 rollout / Data Steward。
- [Phase 2.45c] Codex A 已完成 read-only health-check dry-run runner 最小实现：新增 `scripts/phase245c_health_check_dry_run.py` 与 `tests/test_phase245c_health_check_dry_run.py`，输出 JSON summary 并固定 `dry_run=true`、`writes_db=false`、`repairs=false`、`rollout_approved=false`；默认只做 Git / env key-name / ignored path 检查，mount / URL 均需显式参数，不运行真实 API / CLI smoke。
- [Phase 2.45c] 目标验证通过：py_compile 通过，`tests/test_phase245c_health_check_dry_run.py` 为 `9 passed`，default `--json` dry-run 与 json.tool 通过，`git diff --check` 通过；默认 dry-run 状态为 `warn`，原因是当前 worktree dirty，未访问真实 API / CLI / DB / OpenSearch / Qdrant。
- [Phase 2.45c] Codex B review 通过：runner 只读边界正确，默认不访问真实 API / CLI / DB / OpenSearch / Qdrant，`--check-url` 仅显式 HEAD / GET reachability；下一步只做 Git baseline。
- [Phase 2.45c] Git baseline 已完成：commit `fbad94f`，tag `phase-2.45c-health-check-dry-run-baseline`；下一步转入 Phase 2.45d Mac mini real-machine deployment record planning，不执行真实部署、不运行真实 API / CLI smoke。
- [Phase 2.45d] Codex B 已写入下一轮 docs-only planning 入口：规划 Mac mini 实机部署记录 / operator sign-off；不运行 Phase 2.45c runner，不执行真实部署，不写 DB / facts / document_versions / OpenSearch / Qdrant。
- [Phase 2.45d] 完成 Mac mini real-machine deployment record docs-only planning：新增 `docs/PHASE245D_MAC_MINI_DEPLOYMENT_RECORD_PLAN.md`，定义 record inputs、output schema、operator checklist、stop conditions、storage policy 与 future phase candidates；本轮未写代码、未运行 runner、未运行 API / CLI、未执行真实部署、未写 DB / facts / document_versions / OpenSearch / Qdrant。
- [Phase 2.45d] 目标验证通过：`git diff --check` 通过，`reports/agent_runs/latest.json` JSON 校验通过，latest ignore 检查通过；当前 worktree 仅包含 Phase 2.45d 文档变更与遗留无关 dirty `docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md`。
- [Phase 2.45d] Codex B review 通过：deployment record planning 是人工记录 / operator sign-off 模板，不是 deployment script 或真实部署授权；下一步只做 docs-only Git baseline，不进入 Phase 2.45e。
- [Phase 2.45d] Git baseline 已完成：commit `e12f82a`，tag `phase-2.45d-deployment-record-plan-baseline`；下一步转入 Phase 2.45e sanitized deployment record template artifact，不执行真实部署、不运行 API / CLI smoke。
- [Phase 2.45e] Codex B 已写入下一轮 artifact 入口：新增 sanitized deployment record template 与 `reports/deployment_records/` ignored storage policy；不运行 Phase 2.45c runner、不执行真实部署、不写 DB / facts / document_versions / OpenSearch / Qdrant。
- [Phase 2.45e] Codex B review 通过：template / ignored storage policy 边界正确，真实 deployment records 默认不入 Git；Mac mini 已到货，baseline 后主线可切入 Phase 2.46 Day-0 real-machine setup / internal MVP application prep，但本轮仍只做 docs-only baseline。
- [Phase 2.45e] 完成 sanitized deployment record template artifact：新增 `docs/MAC_MINI_DEPLOYMENT_RECORD_TEMPLATE.md`、`reports/deployment_records/.gitignore` 与 `reports/deployment_records/README.md`；真实 deployment record JSON / Markdown / latest / log 默认 ignored，本轮未生成真实 deployment record，未运行 runner、API / CLI 或真实部署。
- [Phase 2.45e] Git baseline 已完成：commit `8bd7616`，tag `phase-2.45e-deployment-record-template-baseline`；Mac mini 已到货，下一步转入 Phase 2.46 Day-0 real-machine setup / internal MVP application prep planning。
- [Phase 2.46] Codex B 已写入下一轮 planning 入口：规划 Mac mini 到货后的人工 Day-0 实机准备、目录/Git/env/NAS/SSD/network/runtime checklist、evidence artifacts 与 stop conditions；本轮不执行真实部署、不运行 API / CLI smoke、不写 DB / index。
- [Phase 2.46] 完成 Day-0 real-machine setup planning artifact：新增 `docs/PHASE246_MAC_MINI_DAY0_SETUP_PLAN.md`，明确人工 operator actions、Git/env/storage/network/runtime checklist、evidence placeholders、stop conditions、Go/Pause/No-Go 与后续 Phase 2.46a/2.46b/2.46c 候选；本轮未运行 runner、API / CLI smoke 或真实部署，未写 DB / facts / document_versions / OpenSearch / Qdrant。
- [Phase 2.46] Git baseline 已完成：commit `13e2206`，tag `phase-2.46-mac-mini-day0-setup-plan-baseline`；下一步转入 Phase 2.46a Day-0 setup checklist artifact。
- [Phase 2.46a] 完成 Mac mini Day-0 setup checklist artifact：新增 `docs/MAC_MINI_DAY0_SETUP_CHECKLIST.md`，覆盖 operator metadata、物理检查、macOS 初始设置、目录结构、Git checkout、env key-name inventory、NAS / SSD、网络、runtime readiness、evidence placeholders、stop conditions 与 Go / Pause / No-Go sign-off；本轮未运行 runner、API / CLI smoke 或真实 setup，未写 DB / facts / document_versions / OpenSearch / Qdrant。
- [Phase 2.46a] Git baseline 已完成：commit `e78c08e`，tag `phase-2.46a-mac-mini-day0-checklist-baseline`；下一步转入 Phase 2.46b human-run evidence attachment planning。
- [Phase 2.46b] 完成 Mac mini evidence attachment planning：新增 `docs/PHASE246B_MAC_MINI_EVIDENCE_ATTACHMENT_PLAN.md`，明确 filled checklist、health-check JSON、env inventory、storage evidence、MVP smoke result、deployment record 的 ignored path、sanitized summary fields、Git policy、review workflow、Go/Pause/No-Go 与 stop conditions；本轮未生成真实 evidence，未运行 runner、API / CLI smoke 或真实 setup，未写 DB / facts / document_versions / OpenSearch / Qdrant。
- [Phase 2.46b] Git baseline 已完成：commit `01af018`，tag `phase-2.46b-mac-mini-evidence-attachment-plan-baseline`；下一步转入 Phase 2.46c Codex C local MVP smoke prompt artifact。
- [Phase 2.46c] 完成 Codex C local MVP smoke prompt artifact：新增 `docs/CODEX_C_MAC_MINI_LOCAL_MVP_SMOKE_PROMPT.md`，覆盖 API / CLI pre-flight、四个 alias、核心 smoke query、P0/P1/P2/P3、Go/Pause/No-Go 与 report format；本轮未运行真实 smoke，未启动服务，未生成真实 evidence，未写 DB / facts / document_versions / OpenSearch / Qdrant。
- [Phase 2.46c] Git baseline 已完成：commit `595c51d`，tag `phase-2.46c-codex-c-mac-mini-smoke-prompt-baseline`；后续 Codex C 真实终端 smoke 已由用户 / Codex B 提供 sanitized result。
- [Phase 2.46d] 记录 Mac mini local MVP smoke sanitized result：Codex C smoke 返回 `Go`，P0=0，P1=0，P2=2；本轮只写 `docs/PHASE246D_MAC_MINI_LOCAL_MVP_SMOKE_RESULT.md`，未重跑 smoke、未启动服务、未写 DB / facts / document_versions / OpenSearch / Qdrant，且 `Go` 不代表 production rollout 或自动决策授权。
- [Phase 2.46d] Git baseline 已完成：commit `255c2e97fa6d644c2d83655e7ac919c8401f54f2`，tag `phase-2.46d-mac-mini-local-mvp-smoke-result-baseline`，`origin/main` 与 tag 已推送。
- [Phase 2.47] 完成 Internal Controlled MVP Operating Loop docs-only planning：新增 `docs/PHASE247_INTERNAL_MVP_OPERATING_LOOP_PLAN.md`，明确内部受控 MVP 可开始、production rollout 仍禁止、Day 0 / Day 1-2 / Day 3-5 / Week 2 节奏、每日检查、人工角色、issue intake、热更新原则和低人工干预 baseline 策略；本轮未运行 smoke、未启动服务、未写 DB / facts / document_versions / OpenSearch / Qdrant，未进入 rollout。
- [Phase 2.47a] 完成 Internal MVP Daily Operator Checklist artifact：新增 `docs/INTERNAL_MVP_DAILY_OPERATOR_CHECKLIST.md`，覆盖每日基本信息、启动前检查、固定 alias、fixed daily query、evidence boundary、issue intake、Go/Pause/No-Go 与 closeout；本轮未运行 smoke、未启动服务、未写 DB / facts / document_versions / OpenSearch / Qdrant，未进入 rollout。
- [Phase 2.47b] 完成 Local Ignored Pilot Run Record Template artifact：新增 `docs/INTERNAL_MVP_PILOT_RUN_RECORD_TEMPLATE.md` 与 `reports/internal_mvp_runs/.gitignore` / `README.md`，真实 run records 默认 ignored；本轮未生成真实 run record、未运行 smoke、未启动服务、未写 DB / facts / document_versions / OpenSearch / Qdrant，未进入 rollout。
- [Phase 2.47] Combined docs artifact baseline 已完成：commit `bfe7981`，tag `phase-2.47-internal-mvp-operating-artifacts-baseline`；internal controlled MVP 可继续，production rollout 仍禁止。
- [Phase 2.48] 完成 P2 display tails triage docs-only planning：新增 `docs/PHASE248_P2_DISPLAY_TAILS_TRIAGE_PLAN.md`，将 Excel citation broad range + row hint 与 meeting transcript `transcript_as_fact=false` display gap 归为 P2；规划 2.48a Excel display polish、2.48b meeting transcript boundary display polish、2.48c Codex C targeted smoke；本轮未写代码、未运行 smoke、未启动服务、未写 DB / facts / document_versions / audit_logs / OpenSearch / Qdrant，未进入 rollout。
- [Phase 2.48a] 完成 Excel citation display polish 最小实现：主仓 `ContextBuilder` 在 Excel structured citation 中输出 `citation_precision=cell_range`、`citation_precision=multi_row_range` 或 `citation_precision=row_range_fallback`；row-only fallback 同时输出 `row_range_fallback=true`；主仓目标测试 `17 passed`，未改 parser / ingestion / retrieval contract / memory kernel 主架构，未运行真实 smoke，未写 DB / index。
- [Phase 2.48b] 完成 Meeting transcript boundary trace display polish 最小实现：主仓 `ContextBuilder` 新增 `Meeting transcript diagnostics:` 分区，会议纪要证据场景稳定输出 `meeting_transcript_used=true`、`transcript_as_fact=false`、`evidence_required=true`、`meeting_transcript_as_confirmed_fact=false`；主仓目标测试 `30 passed`，未改 meeting ingestion contract / retrieval contract / memory kernel 主架构，未运行真实 smoke，未写 DB / index。

- [Phase 2.48c] Codex B review 已通过 Phase 2.48b，并写入 Codex C targeted smoke prompt；下一步只验证 Excel citation display 与 meeting transcript boundary display，不重跑 full Day-1，未写 DB / index，未进入 rollout。

- [Phase 2.48c] Codex C targeted smoke 已通过：session `20260507_215047_a81e78`，Excel citation display 与 meeting transcript boundary display 均 pass，未出现 facts 替代 evidence、会议纪要当 confirmed facts 或第三文件污染；已写入 Phase 2.48 combined baseline prompt。
- [Phase 2.49] 完成 Internal MVP Run Record Review Bridge 最小实现：新增显式输入 runner，将本地 ignored internal MVP run record JSON 转为 sanitized review payload，并可选在内存中生成 Phase 2.42a review dry-run report；目标测试 `9 passed`，未读取真实 run record，未运行 API / CLI，未写 DB / facts / document_versions / audit_logs / OpenSearch / Qdrant。

- [Phase 2.49 Review] Codex B review 发现两个阻塞点：`issue_summary.p0_count` 在 `issues=[]` 时未映射为 no-go；repair/data mutation boundary false 时 `decision_hint` 仍可能为 go。已写入 bounded review-fix prompt，暂不 baseline。
- [Phase 2.49 Review Fix] 完成决策一致性最小修复：count-only issue summary 会生成 P0/P1/P2/P3 placeholder；repair/data mutation boundary false 会生成 P0 boundary item 并输出 `decision_hint=no_go`；目标测试扩展后 `20 passed`，未读取真实 run record、未运行 API / CLI、未写 DB / index。

- [Phase 2.49 Review Fix] Codex B 复审通过：count-only P0、repair boundary false、data mutation boundary false 均正确映射为 no-go；目标测试 `20 passed`，已写入 Phase 2.49 baseline prompt。
- [Phase 2.49 Baseline] Git baseline 已完成：commit `f23f248`，tag `phase-2.49-internal-mvp-run-record-review-baseline`，`origin/main` 与 tag 已推送。
- [Phase 2.50] 完成 Internal MVP Daily Review Loop docs-only runbook artifact：新增 `docs/PHASE250_INTERNAL_MVP_DAILY_REVIEW_LOOP_PLAN.md`，串联 run query、ignored run record、review dry-run 与 issue intake；本轮未读取真实 run record、未运行 API / CLI、未写 DB / facts / document_versions / audit_logs / OpenSearch / Qdrant，未进入 rollout、repair 或 Data Steward。
- [Phase 2.50 Review] Codex B review 通过：runbook artifact 边界正确，`go` 未写成 rollout approval，真实 records / reports 默认 ignored；本轮执行 docs-only Git baseline，不进入 Phase 2.50a、Phase 2.51、repair、rollout 或 Data Steward。
- [Phase 2.50 Baseline] Git baseline 已完成：commit `569cb3a4b2bd6460d805f80353589ce0866876a6`，tag `phase-2.50-internal-mvp-daily-review-loop-baseline`，`origin/main` 与 tag 已推送。
- [Phase 2.50a] 完成 fake run record runbook smoke：使用 `mktemp` 临时目录验证 Phase 2.49 runner 的 explicit input / review report / explicit output-dir 链路；未复核 visible Missing Evidence => `pause`，显式复核 Missing Evidence => `go`，unsafe evidence / contamination => `no_go`；目标测试 `20 passed`，未读取真实 run record、未运行 API / CLI、未写 DB / index。
- [Phase 2.50a Baseline] Git baseline 已完成：commit `232acf36d563e8f18e3b55ff5981a7ed3c39d766`，tag `phase-2.50a-internal-mvp-runbook-smoke-baseline`，`origin/main` 与 tag 已推送。
- [Phase 2.51] 完成 Mac Mini Internal MVP Operator / Hot Update docs-only runbook artifact：新增 `docs/PHASE251_MAC_MINI_INTERNAL_MVP_OPERATOR_RUNBOOK.md`，明确 Mac Mini 只运行已 baseline refs，覆盖 day-start checks、hot update、rollback、records、stop conditions 与严禁事项；本轮未执行真实部署、未拉远端、未启动服务、未运行 API / CLI、未写 DB / index。
- [Phase 2.51b] Codex B review 通过 minimal Mac Mini operator command sheet；已写入 docs-only Git baseline prompt，baseline 仅允许 selective staging 白名单文档，仍禁止真实 Mac Mini deployment、API/CLI smoke、repair、rollout 或 Data Steward。
- [Phase 2.51a] Phase 2.51b command sheet baseline 已完成后，Codex B 写入下一步 fake deployment / internal MVP run record dry-run smoke prompt；下一轮仅允许 fake/temp 数据与 `/tmp` 输出，不执行真实 Mac Mini deployment、API/CLI smoke、DB/index 写入、repair、rollout 或 Data Steward。
- [Phase 2.51a] 完成 fake deployment / internal MVP run record dry-run smoke：在 `/tmp/hermes_phase251a_fake_smoke` 生成 fake deployment record、fake canonical JSON run record 与 fake Markdown notes；JSON checks 通过，Phase 2.49 bridge 对 fake JSON input 通过并只向 `/tmp` 写 review outputs，`decision_hint=go`、P0=0、P1=0、P2=2、P3=0；未读取真实 reports / run records，未运行 API / CLI smoke，未写 DB / facts / document_versions / audit_logs / OpenSearch / Qdrant，未进入 deployment、repair、rollout 或 Data Steward。
- [Phase 2.51a] Codex B review 通过 fake deployment / internal MVP run record dry-run artifact；已写入 docs-only Git baseline prompt，baseline 仅允许 selective staging 白名单文档，仍禁止真实 Mac Mini deployment、API/CLI smoke、真实 reports 读取、DB/index 写入、repair、rollout 或 Data Steward。
- [Phase 2.50b] 完成 Internal MVP Evidence Pack docs-only planning：新增 `docs/PHASE250B_INTERNAL_MVP_EVIDENCE_PACK_PLAN.md`，规划 canonical run record JSON、Phase 2.49 review payload/report、operator sign-off、issue intake / triage、Codex C smoke / Pilot summary、optional deployment summary、human notes、manifest 字段、ignored storage、PRD matrix linkage 与 Go / Pause / No-Go 语义；本轮未生成真实 evidence pack、未读取真实 reports、未运行 API / CLI、未写 DB / facts / document_versions / audit_logs / OpenSearch / Qdrant，未进入 deployment、repair、rollout 或 Data Steward。
- [Phase 2.50b] Phase 2.51a fake dry-run baseline 完成后，Codex B 写入下一步 evidence pack planning prompt；下一轮仅做 docs-only 规划，不生成真实 evidence pack、不读取真实 reports、不运行 API/CLI、不写 DB/index、不进入 repair、rollout 或 Data Steward。
- [Phase 2.50b] Codex B review 通过 Internal MVP Evidence Pack Planning；已写入 docs-only Git baseline prompt，baseline 仅允许 selective staging 白名单文档，仍禁止真实 evidence pack 生成、真实 reports 读取、API/CLI smoke、DB/index 写入、repair、rollout 或 Data Steward。
- [Phase 2.50c] Phase 2.50b evidence pack planning baseline 完成后，Codex B 写入下一步 sanitized evidence pack template / fake artifact prompt；下一轮仅创建 docs/template，不生成真实 evidence pack、不读取真实 reports、不运行 API/CLI、不写 DB/index、不进入 repair、rollout 或 Data Steward。
- [Phase 2.50c] 完成 sanitized internal MVP evidence pack template artifact：新增 JSON / Markdown template 与 Phase 2.50c boundary 文档；模板只含 placeholder / sanitized 字段，明确不是 rollout approval、customer delivery、automatic tender review、automatic bid、automatic business decision 或 repair authorization；本轮未生成真实 evidence pack、未读取真实 reports、未运行 API / CLI、未写 DB / index。
- [Phase 2.50c] Codex B review 通过 sanitized evidence pack JSON / Markdown templates；已写入 docs-only Git baseline prompt，baseline 仅允许 selective staging 白名单文档，仍禁止真实 evidence pack 生成、真实 reports 读取、API/CLI smoke、DB/index 写入、repair、rollout 或 Data Steward。
- [Phase 2.53] Phase 2.50c baseline 完成后，Codex B 将主线切回 Mac Mini 内部 MVP 实用入口：自然语言导入文件。已写入下一轮边界规划 / 代码入口勘查 prompt；本轮仍不写功能代码、不上传真实文件、不运行 API / CLI smoke、不写 DB / index、不进入 rollout 或 Data Steward。
- [Phase 2.53] 完成 Natural Language File Import MVP 边界规划与代码入口勘查：新增 `docs/PHASE253_NATURAL_LANGUAGE_FILE_IMPORT_PLAN.md`，确认未来实现应复用 Hermes_memory `/api/v1/documents/upload` / ingestion / version governance / OpenSearch / Qdrant 链路，并在 Hermes 主仓补 import intent、upload adapter、alias seed 与 diagnostics；本轮未写功能代码、未上传真实文件、未运行 API / CLI smoke、未写 DB / facts / document_versions / audit_logs / OpenSearch / Qdrant，未进入 repair、rollout 或 Data Steward。
- [Phase 2.53 Baseline] 执行 Natural Language File Import MVP Boundary Planning docs-only Git baseline；该 baseline 仅固化规划与交接状态，不代表自然语言导入能力已实现，不运行真实 upload smoke，不进入 rollout、repair、Data Steward 或 Hermes 主仓修改。
- [Phase 2.85] 完成 Controlled Evidence Write Dry-run docs-only planning：新增 `docs/PHASE285_CONTROLLED_EVIDENCE_WRITE_DRY_RUN_PLAN.md`，定义 future local temp SQLite / in-memory simulated document/chunk write、deterministic refs、idempotency、rollback dry-run、citation boundary、feature flags default off、Go / Pause / No-Go 与 Phase 2.85a / 2.86 split。本轮未实现 writer，未执行 write dry-run，未写 `documents/chunks` / DB / OpenSearch / Qdrant / MinIO，未运行 parser，未复制真实文件，未读取 raw content，未扫描 NAS，未接入 Agent answer，未进入 rollout。

- [Phase 2.53a] 完成 Natural Language File Import parser / dry-run planner 最小实现：Hermes 主仓新增 `agent/memory_kernel/natural_file_import.py` 与 `tests/agent/test_natural_file_import.py`，支持显式导入 intent、单文件路径、标题 / document_type / source_type / alias 解析，并对普通查看 / 总结、missing path、multiple paths、directory / bulk / NAS / BIM batch fail closed；本轮不访问文件系统、不调用 Hermes_memory API、不上传真实文件、不写 DB / index、不进入 adapter / kernel integration。
- [Phase 2.53a Review Fix] 修复否定导入 intent：`不要导入 / 不要上传 / 不要收录` 等返回 `detected=false`，不会进入导入 dry-run；补充测试后主仓 `test_natural_file_import.py` 为 `10 passed`。同时恢复非本轮删除的 `docs/MAC_MINI_MVP_DEPLOYMENT_RUNBOOK.md` 与 `docs/MVP_PILOT_RUNBOOK.md`，本轮仍不接真实 upload adapter、不调用 API、不写 DB / index。
- [Phase 2.53b] 完成 Natural Language File Import Adapter / Kernel Integration docs-only planning：新增 `docs/PHASE253B_NATURAL_IMPORT_INTEGRATION_PLAN.md`，建议 parser 作为 import preflight layer，在普通 retrieval / answer flow 前执行；规划 upload adapter 最小输入 / 输出、alias seed、diagnostics separation、fail-closed 策略与 Phase 2.53c / 2.53d 切分。本轮未写功能代码、未接真实 upload adapter、未运行 API / CLI smoke、未上传文件、未写 DB / facts / document_versions / audit_logs / OpenSearch / Qdrant。
- [Phase 2.53c] 完成 mocked natural import integration：主仓新增 `natural_file_import_flow.py` 与 flow tests，支持 no import intent 继续 normal flow、fail-closed diagnostics、mocked upload success、alias seed diagnostics、upload failure / missing document_id / missing version_id fail-closed；目标测试 `21 passed`。本轮仍未调用真实 Hermes_memory API、未上传文件、未写 DB / index。
- [Phase 2.53] Codex B review 通过 Natural Language File Import planning；因下一步将进入 Phase 2.53a mocked implementation 并可能跨 Hermes 主仓，已写入 docs-only Git baseline prompt，避免规划文档与实现代码混在一个提交。
- [Phase 2.53a] Phase 2.53 baseline 完成后，Codex B 写入自然语言导入文件 parser / dry-run planner 实现入口：仅允许新增 Hermes 主仓 parser 模块与测试，暂不接 upload adapter / kernel integration，不上传真实文件、不调用 API、不写 DB / index。
- [Phase 2.53a Review] Codex B review 暂不建议 baseline：parser 仍会把 `不要导入 / 不要上传 / 不要收录` 识别为有效导入；同时 Hermes_memory 出现 out-of-scope tracked docs deletion，需要恢复 `docs/MAC_MINI_MVP_DEPLOYMENT_RUNBOOK.md` 与 `docs/MVP_PILOT_RUNBOOK.md`。已写入最小 review-fix prompt。

- [Phase 2.56e] Codex B review passed: py_compile passed, targeted pytest `34 passed`, Hermes_memory diff/check JSON/ignore verification passed. Wrote selective dual-repo baseline prompt; no Codex C retest needed to avoid duplicate upload records.

- [Phase 2.57] Wrote Codex A docs-only planning prompt for Natural Import MVP evidence pack / Mac mini operator runbook after Phase 2.56e baseline.

- [Phase 2.57] Codex B review passed for docs-only planning; wrote selective baseline prompt. No Codex C needed.
- [Phase 2.57a] 完成 Natural Import Evidence Template / Runbook Dry-run 最小实现：新增 `scripts/phase257a_natural_import_evidence_template.py` 与 `tests/test_phase257a_natural_import_evidence_template.py`；runner 只读取文件 metadata，不读取正文，不上传、不调用 API / CLI、不写 DB / index，输出固定 dry-run / no-upload / no-repair flags，并将 `--output` 限定到 `reports/internal_mvp_runs/`。
- [Phase 2.57a] 验证通过：`uv run python -m py_compile scripts/phase257a_natural_import_evidence_template.py` 通过，`uv run pytest tests/test_phase257a_natural_import_evidence_template.py -q` 为 `7 passed`；dry-run 示例输出 `ReadyForAuthorizedSmoke`，无真实 upload / API / CLI / DB / index 写入。

- [Phase 2.58 Prompt] 为加快主线节奏，Phase 2.57a runner 不单独 baseline，继续打包进入 Natural Import Operator Pack：补 dry-run review helper、Mac mini operator checklist 与文档 runbook；仍不上传文件、不运行 API/CLI smoke、不写 DB/index。
- [Phase 2.58 Review] Codex B review 发现 dry-run review helper 需补齐 `plain_upload_bypass_used=true` 与 `real_file_uploaded=true` 阻断，已写入 review-fix prompt；不进入 baseline。
- [Phase 2.58] 完成 Natural Import Operator Pack 最小实现：`phase257a_natural_import_evidence_template.py` 新增 `--review-json` 只读 review helper，输出 `review_status`、`blocking_reasons`、`warning_reasons` 与 `safe_to_request_real_smoke_authorization`；新增 `docs/MAC_MINI_NATURAL_IMPORT_OPERATOR_CHECKLIST.md`，明确 preflight、授权、执行、evidence record、Go/Pause/No-Go 与 direct API upload 不算自然语言导入成功。
- [Phase 2.58] 验证通过：py_compile 通过，`uv run pytest tests/test_phase257a_natural_import_evidence_template.py -q` 为 `12 passed`；dry-run template 示例为 `ReadyForAuthorizedSmoke`，review-json 示例为 `ready_for_operator_authorization`；未上传文件、未调用 API / CLI、未写 DB / index。
- [Phase 2.58 Review Fix] 已补齐 `plain_upload_bypass_used=true` 与 `real_file_uploaded=true` 阻断；这两类记录现在均返回 `review_status=pause` 且 `safe_to_request_real_smoke_authorization=false`，避免 direct API bypass / 已发生 upload 记录被误当作 dry-run 授权模板。
- [Phase 2.58 Review Fix] 验证通过：`uv run python -m py_compile scripts/phase257a_natural_import_evidence_template.py` 通过，`uv run pytest tests/test_phase257a_natural_import_evidence_template.py -q` 为 `14 passed`；未上传文件、未调用 API / CLI、未写 DB / index。

- [Phase 2.58 Review] Codex B review passed: py_compile passed, targeted pytest `14 passed`, bypass/upload review guards verified. Wrote selective baseline prompt.

- [Phase 2.59 Prompt] Phase 2.58 baseline 完成后，写入第二个自然语言导入 smoke 的 planning prompt 与 Codex C 待授权模板；不自动上传。
- [Phase 2.59] 完成 Natural Import Second Smoke docs-only planning：补齐第二真实文件授权 gate、执行流程、Codex C 待授权模板、operator checklist 的 second-file smoke 流程与 Phase 2.57 计划同步；本轮未上传文件、未运行 API/CLI smoke、未写 DB / facts / versions / audit_logs / OpenSearch / Qdrant，未进入 cleanup / repair / backfill / reindex / Data Steward / rollout。
- [Phase 2.60] 完成 Internal MVP Launch Readiness Pack 最小实现：新增 `scripts/phase260_mvp_local_readiness_pack.py` 与 `tests/test_phase260_mvp_local_readiness_pack.py`，用于本地只读检查 Git / latest 状态、operator 文档、second-smoke gate、run_local_api helper、optional API health、危险授权 env flags 与 Data Steward not active；runner 固定 dry-run / read-only / no-upload / no-CLI-smoke / no-DB-index-write / no-rollout safety fields。本轮仅执行目标测试与 offline dry-run，未上传文件、未运行真实 API / CLI smoke、未写 DB / facts / versions / audit_logs / OpenSearch / Qdrant，未进入 repair / backfill / reindex / Data Steward / production rollout。

- [Data Steward DB Branch Intake] 将 DB / NAS / Data Steward 支线接收任务纳入后续主线开发线路：支线 `/Users/Weishengsu/Hermes_memory_db0` 当前 closeout baseline 为 `a272081` / `phase-db-branch-closeout-merge-readiness-baseline`。后续主线需单独开 Data Steward DB Branch Intake / PR Review 阶段，优先走 Draft PR / merge readiness review；合入前必须保持 feature flags 默认 off、catalog-only 不进入 `documents/chunks`、不写 OpenSearch / Qdrant、权限缺失默认 deny、probe 文件不合入。DB-5 / DB-6、真实 DB smoke、真实 NAS / BIM 扫描继续后置授权。

- [Phase 2.62 Review] Codex B review 通过 Internal MVP Issue Triage Summary Runner：复核 runner 复用 Phase 2.61a validator、只读 summary、安全字段、P0/P1/P2/P3 语义和 redacted `issue_refs`；复跑 py_compile、targeted pytest `19 passed`、`git diff --check` 与 latest JSON 校验均通过。已写入 selective Git baseline prompt；baseline 后停止，不自动进入 Phase 2.63 或 DB Branch Intake。

- [Phase 2.63 Prompt] Phase 2.62 baseline 完成后，写入 Internal MVP Operator Daily Summary Workflow 实现入口：基于 Phase 2.62 issue summary 或 ignored issue JSON，生成每日 operator / Codex B 可读的脱敏 Go / Pause / No-Go 摘要；本轮仍不读取真实 records 默认路径、不上传、不运行 API/CLI smoke、不写 DB/index、不创建外部 issue、不进入 repair、rollout 或 Data Steward。

- [Phase 2.63 Reprioritized] 用户要求尽快进入 Data Steward DB Branch Intake / PR Review，因为数据库开发团队正在等待企业 Agent 接入与测试数据库可用性。当前已将 `docs/NEXT_CODEX_A_PROMPT.md` 从 operator daily summary workflow 改为 DB Branch Intake / PR Review：验证 `/Users/Weishengsu/Hermes_memory_db0` closeout branch、复跑目标测试、如通过则 push DB branch/tag，并在主线写入 PR readiness 文档；不继续 DB 功能开发、不连接真实 DB、不扫描 NAS、不 merge 到 main。Operator daily summary workflow 延后。

- [Phase 2.63 Review] Codex B review 通过 Internal MVP Operator Daily Summary Workflow：`phase263_mvp_operator_daily_summary.py` 可从 Phase 2.62 summary 或 issue JSON 生成脱敏 daily summary，保持 read-only / dry-run / no rollout / no repair 安全字段；复跑 py_compile、targeted pytest `28 passed`、`git diff --check` 与 latest JSON 校验均通过。下一步只做 selective Git baseline；baseline 后建议 Phase 2.64 进入 Data Steward DB Branch Intake / PR Review。

- [Phase 2.64 Prompt] Phase 2.63 baseline 已完成后，Codex B 将主线切入 Data Steward DB Branch Intake / PR Review：下一轮仅审查 `/Users/Weishengsu/Hermes_memory_db0` closeout branch、复核测试与 probe 文件、推送 branch/tag（如需要）并写入主线 PR readiness 文档；不连接真实 DB、不扫描 NAS、不写 migration / documents / chunks / OpenSearch / Qdrant、不 merge 到 main。

- [Phase 2.64b Prompt] Codex B 复核 Phase 2.64 intake 后确认 DB 支线尚未合入主线；直接 raw merge 会冲突并回退近期 MVP 文件。已写入选择性合入提示词：仅接入 readonly asset catalog interface、DB contract docs、tests 与 feature flags 默认 off 的最小配置；排除 `.claude/**`、DB 支线交接文件、QA probe、真实 DB/NAS 输出及任何会回退主线的文件。本轮不连接真实 DB、不扫描 NAS、不写 migration / documents / chunks / OpenSearch / Qdrant、不创建 PR、不 commit/tag/push。

- [Phase 2.64b Review] Codex B review 通过 Selective Data Steward DB Integration：确认没有 raw merge，没有 `.claude/**` / `package.json` / QA probe 混入，feature flags 默认 off；复跑 Data Steward tests `71 passed`、Data Steward ruff passed、MVP runner regression `28 passed`、`git diff --check` 与 latest JSON 校验通过。已写入 selective Git baseline prompt；baseline 后停止，不进入真实 DB smoke、PR、merge 或 rollout。

- [Phase 2.65 Prompt] Phase 2.64b baseline 完成后，Codex B 将主线切入 Mac mini MVP Landing Acceleration Pack：下一轮生成 release manifest helper、Mac mini install/update quickstart 与 Codex Mac mini prompt 更新，用于把 reviewed Hermes 内核版安装到 Mac mini 测试机；本轮仍不执行真实部署、不启动服务、不上传、不连接真实 DB、不扫描 NAS、不写 DB / index、不进入 rollout。

- [Phase 2.65 Review Fix Prompt] Codex B review found the Mac mini landing pack still paused only because `hermes-agent` used `NEEDS_REVIEWED_AGENT_REF`. Verified reviewed tag `phase-2.56e-natural-import-real-upload-smoke-baseline` at hermes-agent HEAD `be4b3a375`; wrote `docs/NEXT_CODEX_A_PROMPT.md` for a bounded reviewed-ref fix. No deployment, no Docker startup, no API/CLI smoke, no DB/NAS, no upload, no DB/index writes, no repair/backfill/reindex/delete/migration, no commit/tag/push.

- [Phase 2.65 Review] Codex B review 通过 Mac mini MVP Landing Pack：复跑 py_compile、目标测试 `41 passed`、reviewed-ref manifest `ready_for_operator_review`、placeholder-ref manifest `pause/missing_reviewed_hermes_agent_ref`、diff check 与 latest JSON 校验均通过。已写入 selective Git baseline prompt；baseline 必须排除历史 `docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md`，不执行真实 Mac mini deployment、Docker startup、API/CLI smoke、DB/NAS、upload、DB/index write、repair/backfill/reindex/delete/migration 或 rollout。

- [Phase 2.66 Review] Codex B review 通过 Mac mini Controlled Install Planning：规划明确先执行 Mac mini side preflight-only，不直接 full install。已写入 Phase 2.66a preflight-only handoff，限制为机器/tool/repo/ref/env-key presence 检查；禁止 git checkout/pull、Docker startup、API/CLI smoke、upload、真实 DB/NAS、Data Steward activation、DB/index writes、repair/backfill/reindex/delete/migration、业务代码修改、secret 输出或 rollout。

- [Phase 2.66b Prompt] Mac mini preflight report returned `Pause`: machine/tools/env were available, but Hermes_memory checkout was old (`569cb3a4`) and Phase 2.65/2.66 handoff docs were missing because prior prompt forbade checkout/pull. Wrote controlled checkout/docs sync prompt: only fetch/checkout reviewed refs, verify handoff docs and env key names, then stop; still no Docker startup, API/CLI smoke, upload, real DB/NAS, Data Steward activation, DB/index writes, repair/backfill/reindex/delete/migration, code patch, secret output, or rollout.

- [Phase 2.66c Prompt] Mac mini controlled checkout/docs sync report returned refs/env/worktrees OK: Hermes_memory at `phase-2.65-mac-mini-mvp-landing-baseline`, hermes-agent at `phase-2.56e-natural-import-real-upload-smoke-baseline`, both clean, env keys present. The only missing `PHASE266` doc is expected because it is post-2.65 planning and not part of the checked-out 2.65 baseline. Wrote controlled runtime startup / health-check prompt: start Docker compose, check `docker compose ps`, API `/health`, and Hermes CLI help; still no upload, no business smoke, no true DB/NAS, no Data Steward activation, no DB/index writes, no repair/backfill/reindex/delete/migration, no code patch, no secret output, no git mutation, no rollout.

- [Phase 2.66d Prompt] Mac mini runtime health report returned `Go`: Docker compose up, API `/health` OK, Hermes CLI help OK, reviewed refs clean, env keys present. Wrote minimal MVP smoke prompt limited to existing sample alias/retrieval/citation/boundary checks; still no upload, no true DB/NAS, no Data Steward activation, no DB/index writes, no repair/backfill/reindex/delete/migration, no code patch, no secret output, no git mutation, no production rollout, no automatic tender/bid/business decision.

- [Phase 2.66e Prompt] Mac mini minimal MVP smoke returned `Go`: API/CLI healthy, four aliases resolved, existing sample retrieval/citation/facts/transcript boundaries passed, no P0/P1. Since that smoke avoided HTTP search to avoid audit writes, wrote HTTP/API retrieval smoke prompt allowing only normal `retrieval.query` audit log as a side effect. Still no upload, no manual DB writes, no facts/document_versions writes, no index writes, no real DB/NAS, no Data Steward activation, no repair/backfill/reindex/delete/migration, no code patch, no secret output, no git mutation, no rollout, no automatic tender/bid/business decision.

- [Phase 2.67 Prompt] Mac mini HTTP/API retrieval smoke returned `Go`: Q1-Q4 API search were 200, target-document-only, trace IDs present, no facts/transcript/snapshot substitution, no contamination, no P0/P1; only P3 is empty top-level `citations` array while source/chunk/version metadata remains manually checkable. Wrote Internal Controlled MVP Trial Runbook: allow internal sample-document use and local ignored issue/run records; still prohibit production rollout, customer delivery, automatic tender/bid/business decision, real DB/NAS/Data Steward, unauthorized upload, manual DB/index writes, repair/backfill/reindex/delete/migration, code patch, secret output, and git mutation.

- [Phase 2.68 Prompt] 用户确认下一步应把数据管家 DB 支线纳入主线，但采用低耦合接收路线，而不是直接让 Agent 增删改查真实数据库。已新增 `docs/PHASE268_DATA_STEWARD_DB_INTAKE_PLAN.md` 并写入 `docs/NEXT_CODEX_A_PROMPT.md`：Codex A 下一步只做 Data Steward DB Branch Intake / Merge Readiness Review，复核支线 closeout、主线 feature flags、catalog-only / evidence 分层、权限缺失默认 deny、目标测试与无 secret / 无真实样本混入。Phase 2.68 禁止真实 MySQL、NAS scan、migration、`documents/chunks` / OpenSearch / Qdrant 写入、Data Steward runtime activation、DB CRUD、retrieval contract / memory kernel 主架构修改和 production rollout。数据库团队配合点后置到 Phase 2.69 `structure_only` smoke。

- [Phase 2.69 Prompt] Phase 2.68 已回传 `ready_for_mainline_acceptance`，用户确认只授权 DB `structure_only` 检查，contract 仍为 `delivery_platform.asset_views.v1`，禁止输出真实项目名、文件名、NAS 路径或 raw row。已新增 `docs/PHASE269_DB_STRUCTURE_ONLY_SMOKE_PLAN.md` 并写入 `docs/NEXT_CODEX_A_PROMPT.md`：Codex A 下一步只生成测试机侧 `docs/CODEX_DB_STRUCTURE_ONLY_SMOKE_PROMPT.md` / runbook，不在开发机连接数据库。允许 SQL 形状仅限 `SELECT 1`、`SELECT DATABASE()`、`SHOW FULL TABLES WHERE Table_type='VIEW'`、四个 View 的 `SHOW COLUMNS` 与 `WHERE 1=0` 空结构检查；继续禁止 `LIMIT 1/30`、真实行读取、NAS scan、migration、DB/index 写入、Data Steward runtime activation、DB CRUD、secret 输出和 rollout。

- [Phase 2.69b Prompt] 测试机执行 structure-only prompt 后安全返回 `Pause`：未连接 DB、未执行 SQL、未读取真实行、未输出 secret / 真实业务数据、未执行写操作。Pause 原因为 Hermes_memory install/version 未确认、DB secure env keys 缺失、direct mysql client 不可用。已新增 `docs/PHASE269B_DB_STRUCTURE_ONLY_PRECONDITION_PLAN.md` 并写入 `docs/NEXT_CODEX_A_PROMPT.md`：Codex A 下一步只生成测试机前置条件检查 prompt，确认安装版本、secure env key names、readonly credential 注入状态、MySQL client 或 Hermes readonly tooling；仍禁止 DB 连接、SQL 执行、真实行读取、NAS scan、DB/index 写入、tool install、secret 输出、DB CRUD 和 rollout。

- [DB Direct Handoff] 用户确认后续 DB / Data Steward prompt 与测试机前置检查不再经由 Codex A。已新增 `docs/DB_TEAM_DIRECT_HANDOFF_PROTOCOL.md`：Codex B 可直接与用户 / 数据库团队 / 测试机 Codex 对接，编写或审核 DB prompt、接收 sanitized report、列出数据库团队配合项；Codex A 继续负责常规主线实现。该流程调整不放宽安全边界，仍禁止未授权 DB 连接、SQL 执行、真实行读取、secret 输出、真实业务数据输出、NAS scan、DB/index 写入、DB CRUD、migration、repair 和 rollout。

- [Phase 2.70 Schema Gap Review] 测试机 DB `structure_only` smoke 返回 `Go`：DB 可达、database 匹配、四个 View 存在、字段结构可读、四个 `WHERE 1=0` 通过，且未输出 secret / 真实业务数据、未读取真实行、未写任何系统。已新增 `docs/PHASE270_DB_SCHEMA_CONTRACT_GAP_REVIEW.md`、`docs/DB_SCHEMA_GAP_REQUEST_TO_DB_TEAM.md`、`docs/DB_LIMIT30_REDACTED_SMOKE_PLAN.md`。结论：已完成第一阶段只读结构级耦合，但还不是完整 Data Steward 耦合。P1 缺口包括权限标签、项目范围、密级、`ModelAssetView.project_id`、`last_seen_at`、lifecycle / moved / stale / missing、index eligibility 与 `AuditEventView.event_id` 单调递增语义。当前仍不授权 `LIMIT 30`、mirror、DB CRUD、NAS scan、indexing 或 rollout。

- [Phase 2.73] 完成 Hermes v1.1 readonly adapter contract update：`platform_asset_readonly_db_contract_version` 与 readonly contract 更新为 `delivery_platform.asset_views.v1.1`，required fields 增加 v1.1 governance 字段，fake adapter/fixtures/metadata DTO 同步输出 `permission_tags`、`confidentiality_level`、`last_seen_at`、`lifecycle_status`、`index_eligibility` 与 `ModelAssetView.project_id`。Preflight 继续 fail-closed：无 REST/API Key `project_scope` 证明时仍 `would_deny / missing_permission_contract`，`catalog_only` 不进入正文 evidence。验证通过：py_compile + Data Steward asset catalog target tests `73 passed`。本轮未连接真实 DB、未执行 SQL、未读取真实行、未扫描 NAS、未写 DB/index、未启用 mirror/indexing/Agent CRUD 或 rollout。

- [Phase 2.74] 准备测试机 v1.1 adapter reviewed-ref 复验交接：新增 `docs/PHASE274_TEST_MACHINE_V11_ADAPTER_SMOKE_PLAN.md` 与 `docs/CODEX_TEST_MACHINE_V11_ADAPTER_SMOKE_PROMPT.md`。测试机 prompt 要求先确认 Hermes ref 包含 Phase 2.73、contract version v1.1、feature flags off，再执行 structure-only smoke 与一次授权的 `LIMIT 30` 脱敏聚合统计 smoke；继续禁止 secret/raw row/真实业务数据输出、DB 写入、NAS scan、mirror/indexing/Agent CRUD、repair/backfill/reindex/delete/migration 和 rollout。本轮未连接真实 DB、未执行 SQL、未读取真实行。

- [Phase 2.84a] 完成 Evidence Write Preflight Dry-run 最小实现：新增 `evidence_preflight` service 与 CLI，从 ignored local payload plan + operator approval JSON 生成 ignored local `nas_evidence_write_preflight.v0` report；覆盖 payload ready / not allowed / no-go、operator approval mismatch、scope cap、sanitized artifact 与 CLI summary。TDD RED 已观察到 module / CLI missing；py_compile 通过，目标测试 `7 passed`，Data Steward regression `111 passed`，`git diff --check` / JSON / ignore checks 通过。本轮未执行 parser、未复制真实文件、未读取 raw text、未扫描 NAS、未写 DB / `documents/chunks` / OpenSearch / Qdrant / MinIO，未接入 Agent answer，未 rollout。

- [Phase 2.85 Prompt] Phase 2.84a baseline 完成后，Codex B 将主线推进到 Controlled Evidence Write Dry-run Planning：下一轮只创建 `docs/PHASE285_CONTROLLED_EVIDENCE_WRITE_DRY_RUN_PLAN.md` 并同步交接文件，定义 future local temp SQLite / in-memory simulated write、deterministic refs、idempotency、rollback 与 citation coverage；不实现 writer、不执行 dry-run、不写 `documents/chunks` / DB / OpenSearch / Qdrant / MinIO、不运行 parser、不复制文件、不接入 Agent answer、不 rollout。

- [Phase 2.85 Review] Codex B review 通过 Controlled Evidence Write Dry-run Planning：规划保持 docs-only，future runner 仅限 local temp SQLite / in-memory simulation，明确禁止真实 Hermes DB、OpenSearch、Qdrant、MinIO、parser、file copy、NAS scan、Agent answer integration、repair/reindex/rollout。已具备 selective docs baseline 条件；baseline 后再决定是否授权 Phase 2.85a。

- [Phase 2.85a Prompt] Phase 2.85 baseline 完成后，Codex B 将主线推进到 Local Evidence Write Dry-run Runner Implementation：下一轮实现 local temp SQLite / in-memory simulated documents/chunks/citations/idempotency/rollback runner，并输出 ignored local `nas_evidence_write_dry_run.v0` report；仍不写真实 `documents/chunks` / DB / OpenSearch / Qdrant / MinIO，不运行 parser，不复制文件，不接入 Agent answer，不 rollout。

- [Phase 2.85a Review] Codex B review 通过 Local Evidence Write Dry-run Runner：实现保持 local-only / in-memory simulation，输出 ignored local `nas_evidence_write_dry_run.v0` report；复跑 py_compile、目标测试 `8 passed`、Data Steward regression `119 passed`、`git diff --check`、latest JSON 与 ignore checks 均通过。已具备 selective baseline 条件；baseline 后再决定是否进入 Phase 2.86 controlled small-batch real Hermes evidence write planning。
