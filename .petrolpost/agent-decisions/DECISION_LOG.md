# 决策历史日志

> 本文件由 `decisions.yaml` 渲染整理而来，请优先维护结构化源文件。

## DEC-20260812-01 · 2026-08-12 · [已确认]
**变更**: 从零开始讨论泛化的教培智能客服目标与边界 → 长期目标保持全链路内部坐席辅助，一期聚焦在读服务助手，采用离线回放、半自动执行、双台联动验证  
**触发**: 项目从泛客服自动化收敛为教培在读服务场景的一期验证，强调先把内部坐席辅助骨架搭稳。  
**理由**: 用户明确希望优先验证消息分流和坐席辅助，同时把结构、记录和反馈闭环搭起来，而不是过早追求全自动替代。  
**关联**: `docs/superpowers/specs/2026-08-12-educational-training-customer-service-design.md` · `offline-replay-first` · `dual-console-validation`  
**后续措施**:
- [x] 将一期边界固化进 feature spec、plan 和 tasks
- [x] 以 replay-first 方式完成首版实现验证

---

## DEC-20260812-02 · 2026-08-12 · [已确认]
**变更**: 一期 UI 形态尚未确定，存在桌面程序、插件、Web 等多种可能 → 确定 CLI/API 优先，配对话模拟器和轻量 Web 控制台；后期生产 UI 优先复用数据中台或管理后台框架  
**触发**: 用户追问 service 的交付与使用形式，希望先讨论应用承载，而不是具体页面。  
**理由**: 先把评估、辅助、记录、来源追溯做成与客户端解耦的 headless service，避免宿主形态反向绑架核心结构。  
**关联**: `docs/superpowers/specs/2026-08-12-educational-training-customer-service-design.md` · `specs/001-edu-cs-core/contracts/cli.md` · `specs/001-edu-cs-core/contracts/http-api.md` · `headless-service`  
**后续措施**:
- [x] 定义 replay protocol 与 simulator 输入输出
- [x] 实现轻量验证控制台，不将其当作生产坐席端

---

## DEC-20260812-03 · 2026-08-12 · [已确认]
**变更**: 可能把判断逻辑、提示呈现和记录混在同一层处理 → 确立评估层、辅助层、记录层分离，提示以状态化/仪表盘式信息为主，来源标注作为一级能力  
**触发**: 讨论一期系统分层和提示形态时，用户认可“评估和辅助分离”，并要求来源标注与状态化展示。  
**理由**: 通过结构分层减少界面与判断逻辑耦合，让评估结果可追溯、可复盘，并让常规提示与特别警告分层消费。  
**关联**: `docs/superpowers/specs/2026-08-12-educational-training-customer-service-design.md` · `evaluation-assistance-record-separation` · `pressure-state-lamp` · `source-attribution`  
**后续措施**:
- [x] 在 replay 输出中保留结构化评估结果与 provenance
- [x] 在轻量控制台中以回放、异常、来源追溯视图承载验证

---

## DEC-20260812-04 · 2026-08-12 · [已确认]
**变更**: 不成熟信号可能被排除在核心结构之外，等待充分验证后再接入 → 独立信号先进入系统和反馈闭环，信号生产与消费解耦，是否展示/提示/参与路由由消费侧配置控制  
**触发**: 用户强调注意力变化等信号本身是独立研究主题，不应因为不成熟就被挡在系统外。  
**理由**: 用户明确坚持“先有反馈，再做优化”，认为只有让信号参与记录与验证，才能形成真实的学习闭环。  
**关联**: `docs/superpowers/specs/2026-08-12-educational-training-customer-service-design.md` · `signal-production-consumption-decoupling` · `attention-shift-signal`  
**后续措施**:
- [x] 在数据模型中拆出 SignalProfile、EvaluationRecord 与治理留痕实体
- [x] 在运行时通过 signal snapshot 保留历史判断所依赖的配置快照

---

## DEC-20260812-05 · 2026-08-12 · [已确认]
**变更**: 配置可能作为实现细节散落在流程中，测试和 Spec 约束不突出 → 默认配置随代码走，优先用固定档位承载差异，局部复杂度再由分层开关兜底，并以 Spec+TDD+闭环验证约束实现  
**触发**: 一期成功标准和实施风险讨论后，用户补充配置优先、Spec 驱动、TDD 和闭环验证约束。  
**理由**: 用户将配置视为吸收局部变化、避免结构耦合的主要治理手段，同时要求实现不能脱离 Spec 和验证链路漂移。  
**关联**: `specs/001-edu-cs-core/spec.md` · `specs/001-edu-cs-core/plan.md` · `baseline-config-with-code` · `spec-driven-tdd`  
**后续措施**:
- [x] 补齐 baseline config schema、validate/diff 和版本记录能力
- [x] 用测试与 quickstart 验证核心链路、配置治理和反馈挂接

---

## DEC-20260812-06 · 2026-08-12 · [已确认]
**变更**: Signal 生命周期、消费档位、历史判断与治理动作的关系表达不完整 → 确立双轴治理模型：消费档位与生命周期状态解耦，运行时开环、治理层闭环，并通过 SignalLifecycleEvent 保留治理审计  
**触发**: 用户逐项审阅 planning 工件时，指出数据模型里对信号治理的实体关系还不闭合，要求在 tasks 生成前修补。  
**理由**: 如果不先补齐 `signal_key`、signal snapshot 和治理留痕关系，后续 tasks 与实现都会带着结构性断层进入代码。  
**关联**: `specs/001-edu-cs-core/spec.md` · `specs/001-edu-cs-core/data-model.md` · `dual-axis-signal-governance` · `signal-lifecycle-event`  
**后续措施**:
- [x] 在 spec 和 data model 中补齐 SignalLifecycleEvent、signal snapshot 与 current_config_version
- [x] 在后端实现 lifecycle service、snapshot service 和相关测试

---

## DEC-20260812-07 · 2026-08-12 · [已确认]
**变更**: 多租户风险主要被理解为数据或配置隔离问题 → 将最小可见原则扩展到查询接口、聚合接口、复盘与指挥台视图，并定义四类角色模板承载默认可见范围  
**触发**: 用户要求多租户隔离不能只停留在存储层，必须覆盖查询、聚合、指挥台和复盘视图，并采用默认最小可见。  
**理由**: 用户把查询和聚合层越权视为高风险返工点，希望一期就把租户/校区/平台审计的可见性边界写清楚。  
**关联**: `specs/001-edu-cs-core/spec.md` · `least-visibility-default` · `role-template-seat-school` · `role-template-platform-auditor`  
**后续措施**:
- [x] 在 review 查询、aggregate 接口和控制台视图中落实 scope 解析
- [x] 种子化四类角色模板并验证跨范围授权行为

---

## DEC-20260812-08 · 2026-08-12 · [已确认]
**变更**: 来源信息、反馈挂接和验收指标可能只是补充说明 → 确立主来源+贡献来源的归因模型，允许贡献角色标注，并将路由正确性与闭环可用性并列为第一主指标，辅助有效性退居辅指标  
**触发**: 围绕来源标注、学习闭环和验收指标的讨论逐步收敛为可追溯的归因与分层验收体系。  
**理由**: 用户希望先保证“对/稳/改”和“跑/查/挂”，再逐步优化建议采纳等效果指标，避免一期被表面智能感牵着走。  
**关联**: `specs/001-edu-cs-core/spec.md` · `primary-plus-contributing-sources` · `feedback-attachment-loop` · `layered-success-metrics`  
**后续措施**:
- [x] 在协议、数据模型和实现里保留 attribution 与 feedback attachment
- [x] 在 quickstart 与测试中验证 replay、review、feedback 主链

---

## ⚠️ 潜在冲突

本次基于现有会话摘要与设计工件梳理，暂未发现需要立刻升级处理的显式冲突。当前更像是从“未定”逐步收敛到“已定”，而不是出现了两套互斥方案同时生效。
