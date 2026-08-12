# Feature Specification: Educational Training Customer Service Core

**Feature Branch**: `001-edu-cs-core`

**Created**: 2026-08-12

**Status**: Approved

**Input**: User-approved design in `docs/superpowers/specs/2026-08-12-educational-training-customer-service-design.md`

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Run Offline Conversation Replay Through the Core (Priority: P1)

As a product or engineering team member, I can feed timestamped conversation events into a CLI or API driven replay flow and receive structured evaluation results, so that we can verify routing, signal production, and feedback loop behavior without depending on a production client.

**Why this priority**: This is the minimum viable slice for the approved v1 direction. If replay cannot run end to end, none of the later routing, signal, control-plane, or UI work is trustworthy.

**Independent Test**: Can be fully tested by sending a replay session with timestamped dialogue events into the core service and confirming that the system produces structured outputs, persists traceable records, and supports replay review without any real-time channel integration.

**Acceptance Scenarios**:

1. **Given** a timestamped conversation event stream and session metadata, **When** the replay is submitted through the CLI or API, **Then** the system returns structured evaluation outputs including route suggestions, signals, and source attribution.
2. **Given** a replay that has completed processing, **When** an operator loads the session for review, **Then** the system can show the replay timeline, evaluation outputs, and recorded provenance for the same session.

---

### User Story 2 - Govern Independent Signals Without Hard-Wiring Them (Priority: P1)

As a system designer, I can let independent signals such as attention change enter the system before they are fully mature, while controlling whether they affect display, prompts, routing, or combined decisions through configuration and lifecycle governance.

**Why this priority**: The project explicitly requires learning-friendly structure. Signal production and signal consumption must be decoupled early or the architecture will lock unstable research signals into the main decision path.

**Independent Test**: Can be fully tested by configuring a signal to different consumption tiers, replaying the same session, and confirming that the signal is still produced and recorded while its downstream effects change according to configuration and lifecycle state.

**Acceptance Scenarios**:

1. **Given** an independent signal in an experimental lifecycle state, **When** replay runs, **Then** the signal is recorded and traceable even if it is configured only for observation.
2. **Given** the same signal configured for a higher consumption tier, **When** replay runs, **Then** the system uses it in the configured downstream layers without changing the signal definition itself.

---

### User Story 3 - Review Replay Outcomes Through a Lightweight Control Console (Priority: P2)

As a manager, QA reviewer, or analyst, I can use a lightweight web console to inspect replay sessions, route outputs, signals, anomalies, and source traces, so that I can validate the core service and provide feedback before any production UI is built.

**Why this priority**: The approved design makes the UI a validation and review surface, not the primary asset. This story proves that the headless service can be inspected and governed.

**Independent Test**: Can be fully tested by loading processed replay sessions in the console and confirming that an operator can inspect timeline, route outcomes, anomaly indicators, and source trails without requiring a production seat client.

**Acceptance Scenarios**:

1. **Given** a processed replay session, **When** a reviewer opens it in the control console, **Then** the console shows replay timeline, core outputs, and traceable source details.
2. **Given** multiple replay sessions in the same tenant scope, **When** a reviewer uses the control console, **Then** available views respect tenant and role-based visibility rules.

---

### User Story 4 - Enforce Baseline Configuration and Tenant Isolation (Priority: P2)

As a platform owner, I can govern baseline configuration and tenant-aware visibility rules through versioned default configuration, so that v1 remains stable, testable, and safe while still allowing future override layers.

**Why this priority**: Configuration governance and tenant-aware visibility are both high-return structural decisions. If they are postponed, later extension work becomes fragile and expensive.

**Independent Test**: Can be fully tested by loading baseline configuration under version control, validating schema and tests, and confirming that query and review surfaces enforce tenant and role visibility boundaries by default.

**Acceptance Scenarios**:

1. **Given** a baseline configuration change, **When** the change is validated, **Then** schema checks, tests, and version history confirm whether it is safe to adopt.
2. **Given** two different tenant scopes, **When** a reviewer queries replay data, **Then** data and aggregated views are restricted according to tenant, school, and role policy.

## Edge Cases

- What happens when a replay session contains out-of-order or duplicated timestamps?
- How does the system handle a signal that is produced successfully but fails lifecycle validation across repeated review rounds?
- What happens when a structured conclusion has multiple contributing sources but no single dominant driver is obvious?
- How does the control console behave when a protocol version includes an extension field that older replay records do not contain?
- What happens when a reviewer attempts to access aggregated or replay data outside the scope allowed by tenant and role policy?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST accept timestamped conversation event streams through both CLI and API entry points.
- **FR-002**: System MUST support offline replay processing without depending on a production chat client or real-time service integration.
- **FR-003**: System MUST produce structured evaluation outputs for each replay session, including route-related outcomes, signal outputs, recommended actions, and source attribution.
- **FR-004**: System MUST keep evaluation logic, assistance consumption, and record-keeping separated as distinct architectural responsibilities.
- **FR-005**: System MUST allow independent signals to be produced and recorded even when their downstream business impact is limited by configuration.
- **FR-006**: System MUST model signal lifecycle separately from signal consumption tier.
- **FR-007**: System MUST support at least these consumption tiers for independent signals: observation, prompting, and decision participation.
- **FR-008**: System MUST support at least these lifecycle states for independent signals: experimental, validated, frozen, and retired.
- **FR-009**: System MUST ensure runtime signal handling remains open loop; lifecycle upgrades, downgrades, freezes, and retirements MUST be governed outside runtime execution.
- **FR-010**: System MUST support mixed governance for signal lifecycle changes, where minor changes can use threshold-plus-review and major changes require validation reporting plus human sign-off.
- **FR-011**: System MUST support graded signal exit behavior, allowing downgrade to observation or freeze before final retirement.
- **FR-012**: System MUST provide baseline configuration under version control as the default system behavior.
- **FR-013**: System MUST validate baseline configuration through schema checks, tests, version history, and Spec alignment before adoption.
- **FR-014**: System MUST keep the baseline configuration model ready for future override layers without requiring online configuration management in v1.
- **FR-015**: System MUST version the replay protocol and provide extension slots so experimental fields can evolve without forcing immediate core-protocol changes.
- **FR-016**: System MUST preserve compatibility for core audit, replay, and trace fields across protocol evolution.
- **FR-017**: System MUST record source attribution using a primary-source plus contributing-sources model.
- **FR-018**: System MUST record contribution roles for contributing sources, including at least trigger, support, verify, and override.
- **FR-019**: System MUST record enough provenance to trace conclusions back to source objects, evidence snippets, version context, and lifecycle-relevant feedback.
- **FR-020**: System MUST allow feedback to be attached to the conclusion itself and to its primary and contributing sources.
- **FR-020a**: System MUST preserve signal-governed evaluation snapshots so historical conclusions can be traced to the signal definition and signal configuration version used at production time.
- **FR-020b**: System MUST record signal lifecycle governance events, including whether the change was minor or major, what changed, which evidence supported it, and who approved it.
- **FR-021**: System MUST provide a lightweight web console for replay inspection, anomaly review, provenance tracing, and QA/management review.
- **FR-022**: System MUST treat the lightweight web console as a validation and review surface, not as a production seat client.
- **FR-023**: System MUST support minimum tenant isolation for v1, including baseline data isolation and configuration isolation.
- **FR-024**: System MUST enforce tenant-aware visibility not only at storage level but also across query interfaces, aggregation interfaces, review views, and command surfaces.
- **FR-025**: System MUST apply least-visibility defaults for query and aggregation behavior.
- **FR-026**: System MUST define role templates for seat/school, school management, tenant management, and platform audit access.
- **FR-027**: System MUST keep platform audit access read-only by default in v1, even when broader visibility is explicitly granted.

### Key Entities *(include if feature involves data)*

- **Replay Session**: A timestamped offline conversation replay unit with tenant scope, school scope, source metadata, protocol version, and processing status.
- **Conversation Event**: A single timestamped message or event in a replay stream, including actor, content, event type, and ordering context.
- **Evaluation Result**: Structured outputs produced from replay processing, such as route outcomes, signal outputs, anomaly markers, summaries, and recommended actions.
- **Independent Signal**: A research-capable signal such as attention change, with lifecycle state, consumption tier, validation evidence, and configuration-controlled downstream usage.
- **Signal Lifecycle Event**: An auditable governance event that changes a signal's lifecycle state and/or default consumption tier, backed by review evidence and approval metadata.
- **Source Attribution Record**: Provenance data describing primary and contributing sources, their roles, evidence snippets, and version context for a conclusion.
- **Feedback Record**: Human or downstream feedback linked to replay sessions, conclusions, signals, and provenance records.
- **Baseline Configuration**: Versioned default configuration describing routing, thresholds, prompt strategy, source behavior, and signal consumption policy.
- **Role Template**: A visibility policy template defining default query and aggregation scope for seat/school, school management, tenant management, or platform audit usage.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Route correctness MUST be evaluated with a combined metric set that includes manual-label agreement, same-class sample stability, and human route-overrule rate.
- **SC-002**: Closed-loop usability MUST be evaluated with a combined metric set that includes end-to-end replay run success, trace completeness, and feedback attachment success.
- **SC-003**: Assist usefulness MUST be evaluated as a secondary metric set that at minimum measures replay review efficiency improvement and anomaly detection lead time; suggestion adoption MAY be tracked but MUST NOT be the primary v1 outcome.
- **SC-004**: Independent signals promoted beyond observation MUST satisfy lifecycle validation evidence that includes manual labeling consistency and stable production behavior before higher-consumption use is allowed.
- **SC-005**: Query and review behavior MUST respect least-visibility defaults so that no replay or aggregated view leaks outside authorized tenant or school scope during validation scenarios.

## Assumptions

- v1 starts from offline replay and simulation flows rather than production real-time seat integration.
- Knowledge accuracy support can rely on future RAG-backed sources without making RAG the only decision mechanism for the core service.
- The repository will use the lightweight web console as a validation and review surface; a production-facing seat UI can be introduced later on top of the same core service.
- The project may need future tenant-, school-, environment-, or experiment-specific overrides, but v1 only requires baseline configuration plus an override-ready structure.
- The current constitution file is still template-shaped, so concrete planning gates in this feature will rely on the approved design document and this feature specification until a project-specific constitution is finalized.
