# Tasks: Educational Training Customer Service Core

**Input**: Design documents from `/specs/001-edu-cs-core/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Tests**: Tests are required for this feature because the approved plan explicitly requires Spec + TDD, contract tests, integration tests, replay regression, and console smoke validation.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this belongs to (`[US1]`, `[US2]`, `[US3]`, `[US4]`)
- Include exact file paths in descriptions

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Create the project skeleton and toolchain required by all later work.

- [ ] T001 Create backend project scaffold and package configuration in `backend/pyproject.toml`
- [ ] T002 [P] Create frontend project scaffold and package configuration in `frontend/package.json`
- [ ] T003 [P] Configure backend test tooling and pytest defaults in `backend/pytest.ini`
- [ ] T004 [P] Configure frontend build and smoke-test tooling in `frontend/vite.config.ts` and `frontend/playwright.config.ts`
- [ ] T005 Create backend and frontend entry scaffolds in `backend/src/edu_cs_core/__init__.py` and `frontend/src/main.tsx`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before any user story can be implemented.

**⚠️ CRITICAL**: No user story work should begin until this phase is complete.

- [ ] T006 Implement SQLite engine, session factory, and repository base in `backend/src/edu_cs_core/storage/database.py`
- [ ] T007 [P] Implement shared domain enums and value objects for signals, attribution, and scopes in `backend/src/edu_cs_core/domain/enums.py`
- [ ] T008 [P] Implement baseline configuration schema and loader in `backend/src/edu_cs_core/config/schema.py` and `backend/src/edu_cs_core/config/loader.py`
- [ ] T009 [P] Implement protocol registry and normalization entrypoints in `backend/src/edu_cs_core/protocol/registry.py`
- [ ] T010 [P] Implement scope resolution core with role-template and grant-aware visibility rules in `backend/src/edu_cs_core/services/scope_resolver.py`
- [ ] T011 Create storage models for replay, evaluation, provenance, signal governance, and scope entities in `backend/src/edu_cs_core/storage/models.py`
- [ ] T012 Create SQLite bootstrap and schema initialization flow in `backend/src/edu_cs_core/storage/bootstrap.py`
- [ ] T013 Create FastAPI app factory, middleware, and dependency wiring in `backend/src/edu_cs_core/api/app.py`
- [ ] T014 Create Typer CLI root entrypoint in `backend/src/edu_cs_core/cli/main.py`

**Checkpoint**: Foundation ready - user story work can proceed.

---

## Phase 3: User Story 1 - Run Offline Conversation Replay Through the Core (Priority: P1) 🎯 MVP

**Goal**: Accept timestamped replay input through CLI/API, process it deterministically, persist normalized results, and expose replay review data without any production client dependency.

**Independent Test**: Submit a replay session through CLI or API and confirm that replay processing, result persistence, provenance storage, and replay review retrieval work end to end.

### Tests for User Story 1 ⚠️

> **NOTE**: Write these tests first, verify they fail, then implement the story.

- [ ] T015 [P] [US1] Add CLI contract test for replay submission and summary output in `backend/tests/contract/test_cli_replay_run.py`
- [ ] T016 [P] [US1] Add API contract test for replay create/show/timeline endpoints in `backend/tests/contract/test_api_replays.py`
- [ ] T017 [P] [US1] Add integration test for replay processing and persistence flow in `backend/tests/integration/test_replay_pipeline.py`
- [ ] T018 [P] [US1] Add golden replay regression test and fixture in `backend/tests/regression/test_replay_golden_samples.py` and `backend/tests/fixtures/replay_session.json`

### Implementation for User Story 1

- [ ] T019 [P] [US1] Implement replay protocol schemas and normalized output models in `backend/src/edu_cs_core/protocol/schemas.py`
- [ ] T020 [P] [US1] Implement replay session and conversation event repositories in `backend/src/edu_cs_core/storage/repositories/replay_repository.py`
- [ ] T021 [P] [US1] Implement evaluation and attribution repositories in `backend/src/edu_cs_core/storage/repositories/evaluation_repository.py`
- [ ] T022 [US1] Implement replay ordering and normalization service in `backend/src/edu_cs_core/replay/normalizer.py`
- [ ] T023 [US1] Implement replay processing service that emits structured results and provenance in `backend/src/edu_cs_core/services/replay_processor.py`
- [ ] T024 [US1] Implement replay CLI commands in `backend/src/edu_cs_core/cli/replay.py`
- [ ] T025 [US1] Implement replay create/show API routes in `backend/src/edu_cs_core/api/routes/replays.py`
- [ ] T026 [US1] Implement replay timeline API route and serialization in `backend/src/edu_cs_core/api/routes/replay_timeline.py` and `backend/src/edu_cs_core/api/serializers/replay.py`

**Checkpoint**: User Story 1 should now be fully functional and independently testable.

---

## Phase 4: User Story 2 - Govern Independent Signals Without Hard-Wiring Them (Priority: P1)

**Goal**: Let governed signals enter the system, remain traceable through snapshot records, and evolve through explicit lifecycle governance instead of runtime auto-updates.

**Independent Test**: Replay the same session under different signal consumption tiers and lifecycle states, then verify that signal production remains stable while downstream effects and lifecycle audit trails follow configuration and governance rules.

### Tests for User Story 2 ⚠️

> **NOTE**: Write these tests first, verify they fail, then implement the story.

- [ ] T027 [P] [US2] Add contract test for governed signal snapshot fields in replay outputs in `backend/tests/contract/test_replay_signal_snapshots.py`
- [ ] T028 [P] [US2] Add integration test for signal lifecycle event approval and profile synchronization in `backend/tests/integration/test_signal_governance.py`

### Implementation for User Story 2

- [ ] T029 [P] [US2] Implement signal profile and lifecycle event repositories in `backend/src/edu_cs_core/storage/repositories/signal_repository.py`
- [ ] T030 [P] [US2] Implement governed signal schemas and snapshot mappers in `backend/src/edu_cs_core/governance/schemas.py`
- [ ] T031 [US2] Implement signal production and consumption policy resolver in `backend/src/edu_cs_core/governance/policy_resolver.py`
- [ ] T032 [US2] Implement governed signal snapshot persistence service in `backend/src/edu_cs_core/services/signal_snapshot_service.py`
- [ ] T033 [US2] Implement signal lifecycle governance service with minor/major approval rules in `backend/src/edu_cs_core/governance/lifecycle_service.py`
- [ ] T034 [US2] Implement signal governance CLI commands in `backend/src/edu_cs_core/cli/signals.py`
- [ ] T035 [US2] Implement signal governance API routes in `backend/src/edu_cs_core/api/routes/signals.py`

**Checkpoint**: User Story 2 should now support independent signal production, snapshot traceability, and governance auditability.

---

## Phase 5: User Story 3 - Review Replay Outcomes Through a Lightweight Control Console (Priority: P2)

**Goal**: Provide a lightweight web console for replay review, timeline inspection, anomaly understanding, and provenance tracing without turning v1 into a production seat client.

**Independent Test**: Open processed replay sessions in the web console and confirm that replay timeline, route results, governed signal outputs, anomaly indicators, and provenance details are visible within the caller's authorized scope.

### Tests for User Story 3 ⚠️

> **NOTE**: Write these tests first, verify they fail, then implement the story.

- [ ] T036 [P] [US3] Add smoke test for replay review timeline and provenance display in `frontend/tests/smoke/replay_review.spec.ts`
- [ ] T037 [P] [US3] Add smoke test for scoped aggregate review views in `frontend/tests/smoke/review_aggregates.spec.ts`

### Implementation for User Story 3

- [ ] T038 [P] [US3] Implement console app shell and routing in `frontend/src/App.tsx`
- [ ] T039 [P] [US3] Implement replay session and timeline API client in `frontend/src/services/replays.ts`
- [ ] T040 [P] [US3] Implement scope-aware review state store in `frontend/src/state/reviewScope.ts`
- [ ] T041 [US3] Build replay review page with timeline and provenance sections in `frontend/src/pages/ReplayReviewPage.tsx`
- [ ] T042 [US3] Build review dashboard page for scoped aggregate views in `frontend/src/pages/ReviewDashboardPage.tsx`
- [ ] T043 [US3] Build signal and anomaly display widgets in `frontend/src/components/SignalPanel.tsx`

**Checkpoint**: User Story 3 should now provide a lightweight, validation-focused review console.

---

## Phase 6: User Story 4 - Enforce Baseline Configuration and Tenant Isolation (Priority: P2)

**Goal**: Enforce code-owned baseline configuration, schema-backed validation, least-visibility query behavior, and tenant-aware review isolation.

**Independent Test**: Validate a baseline configuration version, compare config revisions, and confirm that replay queries and aggregate views are constrained by tenant, school, role template, and explicit grants.

### Tests for User Story 4 ⚠️

> **NOTE**: Write these tests first, verify they fail, then implement the story.

- [ ] T044 [P] [US4] Add CLI contract test for config validate and diff commands in `backend/tests/contract/test_cli_config.py`
- [ ] T045 [P] [US4] Add API contract test for scoped replay and aggregate authorization in `backend/tests/contract/test_api_scope_enforcement.py`
- [ ] T046 [P] [US4] Add integration test for explicit grants and read-only auditor behavior in `backend/tests/integration/test_scope_grants.py`

### Implementation for User Story 4

- [ ] T047 [P] [US4] Implement baseline configuration repository and version manifest handling in `backend/src/edu_cs_core/storage/repositories/config_repository.py`
- [ ] T048 [P] [US4] Implement configuration validation and diff services in `backend/src/edu_cs_core/config/service.py`
- [ ] T049 [US4] Implement query-scope enforcement service for list, detail, and aggregate requests in `backend/src/edu_cs_core/services/query_scope_service.py`
- [ ] T050 [US4] Implement aggregate review service over authorized datasets only in `backend/src/edu_cs_core/services/review_aggregate_service.py`
- [ ] T051 [US4] Implement config validation and diff CLI commands in `backend/src/edu_cs_core/cli/config.py`
- [ ] T052 [US4] Implement config management API routes in `backend/src/edu_cs_core/api/routes/config.py`
- [ ] T053 [US4] Implement scoped aggregate review API routes with auditor read-only safeguards in `backend/src/edu_cs_core/api/routes/review.py`
- [ ] T054 [US4] Seed default role templates and grant resolution helpers in `backend/src/edu_cs_core/storage/seed_role_templates.py`

**Checkpoint**: User Story 4 should now enforce baseline configuration governance and minimum tenant isolation.

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Finish cross-story quality work, tighten docs, and run the approved validation flow.

- [ ] T055 [P] Update implementation notes and developer instructions in `backend/README.md` and `frontend/README.md`
- [ ] T056 [P] Add cross-cutting observability and structured logging for replay, governance, and review flows in `backend/src/edu_cs_core/services/logging.py`
- [ ] T057 Run the full quickstart validation flow and update any execution notes in `specs/001-edu-cs-core/quickstart.md`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1: Setup** - no dependencies, can start immediately
- **Phase 2: Foundational** - depends on Setup completion and blocks all story work
- **Phase 3: US1** - depends on Foundational completion
- **Phase 4: US2** - depends on Foundational completion and uses the replay/evaluation infrastructure established in US1
- **Phase 5: US3** - depends on Foundational completion and consumes the replay/review APIs delivered by US1 and US4
- **Phase 6: US4** - depends on Foundational completion and can proceed in parallel with US1 after shared infrastructure is ready
- **Phase 7: Polish** - depends on all desired stories being complete

### User Story Dependencies

- **US1 (P1)**: MVP story; no dependency on other user stories once Foundational is complete
- **US2 (P1)**: builds on the replay/evaluation path from US1 but remains independently testable through governed replay scenarios
- **US3 (P2)**: depends on replay review APIs from US1 and scoped review behavior from US4
- **US4 (P2)**: depends only on Foundational work and can be delivered independently of the console

### Within Each User Story

- Tests MUST be written and fail before implementation
- Repository/data work comes before orchestration services
- Services come before CLI/API/UI wiring
- Story completion requires passing its independent test criteria before moving on

### Parallel Opportunities

- Setup tasks marked `[P]` can run in parallel
- Foundational tasks `T007` to `T010` can run in parallel after `T006`
- In **US1**, tests `T015` to `T018` can run in parallel, and repositories `T020` and `T021` can run in parallel
- In **US2**, tests `T027` and `T028` can run in parallel, and repository/schema tasks `T029` and `T030` can run in parallel
- In **US3**, tests `T036` and `T037` can run in parallel, and service/state tasks `T039` and `T040` can run in parallel
- In **US4**, tests `T044` to `T046` can run in parallel, and repository/service tasks `T047` and `T048` can run in parallel

---

## Parallel Example: User Story 1

```bash
# Run US1 contract and regression tests together
Task: "T015 [US1] Add CLI contract test in backend/tests/contract/test_cli_replay_run.py"
Task: "T016 [US1] Add API contract test in backend/tests/contract/test_api_replays.py"
Task: "T017 [US1] Add integration test in backend/tests/integration/test_replay_pipeline.py"
Task: "T018 [US1] Add regression test in backend/tests/regression/test_replay_golden_samples.py"

# Build US1 storage pieces together
Task: "T020 [US1] Implement replay repository in backend/src/edu_cs_core/storage/repositories/replay_repository.py"
Task: "T021 [US1] Implement evaluation repository in backend/src/edu_cs_core/storage/repositories/evaluation_repository.py"
```

## Parallel Example: User Story 4

```bash
# Run US4 governance and scope tests together
Task: "T044 [US4] Add CLI config contract test in backend/tests/contract/test_cli_config.py"
Task: "T045 [US4] Add scope enforcement contract test in backend/tests/contract/test_api_scope_enforcement.py"
Task: "T046 [US4] Add grant integration test in backend/tests/integration/test_scope_grants.py"

# Build US4 config storage and validation pieces together
Task: "T047 [US4] Implement config repository in backend/src/edu_cs_core/storage/repositories/config_repository.py"
Task: "T048 [US4] Implement config service in backend/src/edu_cs_core/config/service.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: User Story 1
4. Stop and validate replay submission, persistence, and review retrieval
5. Demo the replay core before expanding governance or UI work

### Incremental Delivery

1. Build Setup + Foundational infrastructure
2. Deliver **US1** as the MVP replay core
3. Add **US2** to make governed signals traceable and auditable
4. Add **US4** to lock down configuration governance and tenant-safe review behavior
5. Add **US3** to expose the validation-oriented console on top of the stabilized APIs

### Suggested MVP Scope

- **Primary MVP**: Phase 1 + Phase 2 + Phase 3 (`US1`)
- **Recommended next increment**: Phase 4 (`US2`) because it completes the signal-governance structure before console-heavy work begins

---

## Notes

- `[P]` tasks touch separate files and can be parallelized safely
- `[US#]` labels map tasks directly to user stories for traceability
- Every story phase is designed to be independently testable
- Baseline configuration, governed signals, and scope isolation are treated as first-class implementation concerns, not polish work
