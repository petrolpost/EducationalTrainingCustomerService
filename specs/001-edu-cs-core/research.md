# Phase 0 Research - Educational Training Customer Service Core

## Decision 1: Use a Python-first core service with a lightweight TypeScript web console

**Decision**: Build the v1 replay core, CLI, API, governance logic, and persistence layer in `Python 3.12`; build the lightweight validation console in `TypeScript 5.x` with React. Use `FastAPI`, `Typer`, `Pydantic v2`, and `SQLAlchemy`/`sqlite` on the backend.

**Rationale**:
- The approved design prioritizes a headless replay/evaluation core, protocol evolution, and later AI-facing signal work. Python keeps the core close to future LLM, RAG, and experimentation needs.
- `FastAPI` and `Pydantic` provide strong schema and OpenAPI generation for the API surface, while `Typer` keeps CLI contracts explicit and testable.
- The web console is intentionally lightweight and replaceable; using a small React/Vite frontend keeps it easy to swap later with a data-platform style shell.

**Alternatives considered**:
- **All-TypeScript stack**: stronger type sharing with the frontend, but less aligned with likely future AI-heavy experimentation.
- **Python-only with server-rendered UI**: simpler runtime, but weaker for the timeline-heavy validation console experience.

## Decision 2: Keep the replay protocol narrow, versioned, and extension-friendly

**Decision**: Adopt a `narrow core protocol + namespaced extension slots + read-layer normalization` approach. Core fields cover replay identity, ordering, essential outcomes, and audit/provenance. Experimental signals and evolving details live under extensions until proven stable.

**Rationale**:
- The design explicitly separates stable system structure from evolving signals.
- A narrow core avoids promoting unstable research signals into the permanent top-level contract too early.
- Read-layer normalization supports TDD, replay regression, and compatibility testing across protocol versions.

**Alternatives considered**:
- **Wide core protocol**: easier direct access, but fragile when signal definitions are still evolving.
- **Almost everything in extensions**: flexible, but weakens contracts and makes replay regression harder to govern.

## Decision 3: Treat configuration as versioned baseline behavior, not an online control plane

**Decision**: Use `baseline configuration under version control` as the only active configuration source in v1. Back it with schema validation, version records, rollback targets, and Spec consistency checks. Keep a future-ready override structure, but do not build online configuration management in v1.

**Rationale**:
- The approved design already treats configuration as an architectural decoupling mechanism, not an operator-facing dashboard.
- Keeping configuration code-owned aligns with the required `Spec + TDD + traceability` discipline.
- This avoids turning v1 into a configuration platform project.

**Alternatives considered**:
- **Online configuration dashboard in v1**: more flexible, but dramatically increases governance and testing complexity.
- **No override-ready structure**: simpler now, but pushes known evolution pressure into later rework.

## Decision 4: Use unified scope resolution for multi-tenant query safety

**Decision**: Enforce tenant-aware visibility through a `single scope-resolution layer` used by query interfaces, aggregation interfaces, replay review views, and console read paths. Least visibility is the default; role templates and explicit authorization widen scope.

**Rationale**:
- Multi-tenant risk is most likely to leak through query and aggregation paths, not just persistence.
- One scope-resolution path reduces drift between list views, detail views, aggregates, and replay review.
- This matches the approved `role template + explicit authorization + least visibility` model.

**Alternatives considered**:
- **Per-endpoint permission checks**: fast to start, but drifts quickly and is difficult to audit.
- **Database-only row-level security**: useful as a lower guardrail, but not sufficient for aggregates, joins, replay review, and cached views.

## Decision 5: Use SQLite-backed local persistence for v1 replay, feedback, and provenance

**Decision**: Store v1 replay sessions, evaluation outputs, signal states, feedback links, and provenance records in `SQLite`, with raw replay payloads and normalized records persisted together under the same local service boundary.

**Rationale**:
- v1 is offline replay-first and does not need distributed runtime infrastructure.
- SQLite is sufficient for deterministic replay development, contract testing, and local validation.
- Keeping persistence simple reduces friction during signal and protocol iteration.

**Alternatives considered**:
- **PostgreSQL**: stronger for long-term scale, but unnecessary complexity for the approved v1 scope.
- **Filesystem-only JSON records**: easy to start, but weaker for query isolation, traceability, and relationship-heavy review workflows.

## Decision 6: Validate v1 through contract, integration, replay regression, and UI smoke tests

**Decision**: Use `pytest` as the main backend test runner, with contract tests for CLI/API/protocol surfaces, integration tests for replay-to-recording flows, replay regression tests with golden samples, and a minimal Playwright smoke suite for the web console.

**Rationale**:
- The design requires TDD and closed-loop validation; replay and protocol stability are central, so contract and regression tests matter more than broad UI coverage.
- The console is a validation surface, so smoke tests are enough for v1.

**Alternatives considered**:
- **Unit tests only**: too weak for protocol evolution, provenance, and replay-chain guarantees.
- **Heavy end-to-end UI focus**: misaligned with the console's deliberately lightweight role in v1.
