# Phase 2.39 Data Steward Product Line Plan

## 1. 定位

Phase 2.39 是 Data Steward / 数据管家后置产品线规划，不并入当前 MVP Pilot，也不打断 Phase 2.38d 人员要求召回主线。

Data Steward 的目标是把 Hermes 企业内核能力封装成可售卖的楼宇 / 园区 / 项目数据管家应用。它首先解决“有哪些数据、在哪里、属于哪个项目、谁负责、是否过期、能否检索和引用”，再逐步接入 BIM、IoT、运维和业务系统的派生数据。

## 2. 产品形态

### 2.1 内部形态

公司级 Hermes 数据内核，统一管理企业文档、BIM 模型文件、图纸、会议、合同、运维资料、业务系统导出数据和后续 IoT 派生数据。

### 2.2 外部形态

面向单栋楼、园区或项目交付的楼宇数据管家应用，提供资产目录、语义检索、空间查询入口、数据质量审计、运维问答和子 Agent 监控面板。

## 3. 四层数据规划

1. 文件资产目录：统一记录 BIM、图纸、表格、会议、合同、运维资料的路径、版本、hash、责任人、项目归属和权限标签。
2. 建筑本体：定义项目、楼栋、楼层、空间、构件、设备、传感器、系统、工单、责任人、合同等实体与关系。
3. 知识图谱：将派生实体和关系写成可审计三元组，例如“消防泵 P001 位于 B1 消防泵房”“消防泵 P001 连接至供水干管 M001”“消防泵 P001 当前状态为运行”。
4. 空间索引：为构件、设备、空间和点云派生边界盒、坐标、楼层、区域索引，后续支持空间查询、近邻检索和区域筛选入口。

## 4. Agent 规划

1. Data Steward Supervisor：统一接收任务、分配子 Agent、汇总证据、风险和人工复核项。
2. Catalog Agent：扫描文件目录，生成资产记录、hash、版本、路径和责任人。
3. Ontology Agent：按建筑本体抽取实体、属性和关系。
4. Spatial Index Agent：从 IFC、RVT、NWD、DWG、点云或派生文件中生成空间索引元数据。
5. Monitoring Agent：监控数据 freshness、失败任务、权限拒绝、索引漂移和长期质量趋势。
6. Review Agent：生成待人工确认的数据质量问题，不自动修复真实数据。

## 5. 最小商业价值

Data Steward 的第一阶段不承诺完整数字孪生，也不承诺自动 BIM 审查。第一阶段价值是：

1. 让客户知道数据在哪里。
2. 让客户知道数据属于哪个项目、楼栋、楼层、专业和责任人。
3. 让客户知道哪些数据过期、重复、缺责任人或权限不清。
4. 让客户可以基于 evidence 查询文件、版本、路径和派生元数据。
5. 让客户看到子 Agent 任务状态、失败原因和人工审阅队列。

## 6. 当前非目标

1. 不解析全量 TB 级 BIM 原始模型内容。
2. 不做 BIM 在线查看器。
3. 不做碰撞检测。
4. 不做自动算量。
5. 不做自动设计审查。
6. 不替代 BIM 协同平台、文件服务器、NAS、楼宇自控系统或运维系统。
7. 不新增 Neo4j、PostGIS、空间索引代码、生产级 scheduler 或 DB schema。
8. 不把原始模型二进制、点云或 IoT 实时流直接送入向量库或 LLM 上下文。
9. 不让子 Agent 自动修复、删除、搬迁或重写真实业务数据。

## 7. 与当前 MVP Pilot 的关系

当前 MVP Pilot 仍以审标、文件内容提取、会议记忆、confirmed facts 辅助上下文和受控反馈闭环为主。Data Steward 是后置产品线，对当前主线代码侵入度应保持 0%-5%，对文档 / 产品规划侵入度可提升到 15%-20%。

Phase 2.38d 仍优先完成人员要求召回与答案边界收口。Data Steward 不抢当前审标 MVP 的实现资源，不作为当前内部试用的阻塞项。

## 8. 后续路线候选

1. Phase 2.39a：Data Steward 文档 baseline 与样本字段表。
2. Phase 2.40：Building Asset Catalog MVP planning，选择一个楼宇或项目目录做 dry-run。
3. Phase 2.41：资产目录 dry-run fixture，验证路径、hash、版本、责任人、权限标签和质量问题。
4. Phase 2.42：建筑本体 / 知识图谱 pilot planning。
5. Phase 2.43：空间索引 metadata pilot planning。
6. Phase 2.44：Data Steward Supervisor / subagent monitoring planning。

## 9. 验收边界

文档阶段只要求 PRD、ROADMAP、TECHNICAL_DESIGN、TODO、DEV_LOG 和 PHASE_BACKLOG 术语一致，并明确 Data Steward 是后置产品线。任何实现阶段必须先定义 dry-run fixture 和人工审阅规则，再考虑真实数据接入。
