# Quickstart - Educational Training Customer Service Core

## Purpose

Validate the approved v1 slice end to end: baseline configuration, replay processing, provenance, feedback attachment, scoped review, and console validation.

## Prerequisites

- Python 3.12 available
- Node.js 20+ available
- repository dependencies installed for backend and frontend
- SQLite available through the Python standard runtime
- Microsoft Edge available locally for Playwright smoke validation

## Environment Setup

```bash
python -m pip install -e ".\backend[dev]"
npm install --prefix frontend
edu-cs bootstrap-db
```

## Validation Scenarios

### Scenario 1: Validate baseline configuration

1. Prepare the backend environment.
2. Run configuration validation and diff against the included fixture configs.

```bash
edu-cs config validate --input backend/tests/fixtures/baseline_config_a.json
edu-cs config diff --left backend/tests/fixtures/baseline_config_a.json --right backend/tests/fixtures/baseline_config_b.json --output json
```

**Expected Outcome**
- configuration passes schema checks
- config diff reports `changed: true`
- invalid config exits non-zero

### Scenario 2: Run a replay session through the core

1. Prepare a replay payload matching the [replay protocol contract](./contracts/replay-protocol.md).
2. Run replay through the CLI.

```bash
edu-cs replay run --input backend/tests/fixtures/replay_session.json --output json
edu-cs replay show --session replay-001 --output json
edu-cs replay timeline --session replay-001 --output json
```

**Expected Outcome**
- a replay session is created
- ordered events are processed
- route, recommended actions, signals, and provenance records are generated
- normalized results can be queried later

### Scenario 3: Inspect replay timeline and provenance

1. Start the API service.
2. Query replay summary and timeline.

```bash
python -m uvicorn edu_cs_core.api.app:create_app --factory --host 127.0.0.1 --port 8000
```

**Expected Outcome**
- service starts cleanly and bootstraps the local schema plus default role templates
- replay summary is returned for authorized scope
- timeline includes structured evaluations, anomaly/risk markers, and provenance
- primary and contributing sources are visible

**Example Requests**

```bash
curl http://127.0.0.1:8000/api/replays/replay-001
curl http://127.0.0.1:8000/api/replays/replay-001/timeline
```

### Scenario 4: Verify scoped query behavior

1. Authenticate as different role templates.
2. Query replay list and aggregate views.

```bash
curl -H "x-principal-id: tenant-manager-a" -H "x-role-template: tenant_manager" -H "x-tenant-id: tenant-a" http://127.0.0.1:8000/api/review/replays
curl -H "x-principal-id: tenant-manager-a" -H "x-role-template: tenant_manager" -H "x-tenant-id: tenant-a" http://127.0.0.1:8000/api/review/aggregate
```

**Expected Outcome**
- seat/school role sees only allowed scope
- school manager sees school-wide scope only
- tenant manager sees tenant-wide scope
- platform auditor remains read-only by default

### Scenario 5: Validate the lightweight console

1. Attach feedback to a replay conclusion and its primary source.
2. Confirm the record is accepted by the API.

```bash
edu-cs review feedback add --session-id replay-001 --evaluation-id replay-001:route --attribution-id replay-001:route:primary --feedback-type corrected --payload "{\"note\":\"需要人工复核\"}" --output json
curl -X POST http://127.0.0.1:8000/api/feedback \
  -H "Content-Type: application/json" \
  -d "{\"session_id\":\"replay-001\",\"evaluation_id\":\"replay-001:route\",\"attribution_id\":\"replay-001:route:primary\",\"feedback_type\":\"corrected\",\"feedback_actor_kind\":\"reviewer\",\"feedback_actor_id\":\"qa-001\",\"feedback_payload\":{\"note\":\"保留来源反馈链路\"}}"
```

**Expected Outcome**
- feedback can be attached to the replay conclusion itself
- feedback can also target the primary source attribution for the same conclusion
- the stored feedback keeps session, evaluation, and attribution linkage intact

### Scenario 6: Validate the lightweight console

1. Build the frontend bundle.
2. Run the smoke suite.

```bash
npm run build --prefix frontend
npm run test:smoke --prefix frontend
```

**Expected Outcome**
- the replay review page renders timeline, anomaly, and provenance sections
- the review dashboard page renders scoped aggregate counts
- smoke tests pass using the local Microsoft Edge channel

## Execution Notes

- Verified on 2026-08-12 in the local workspace.
- Backend validation passed with `python -m pytest backend/tests` (13 tests).
- Frontend validation passed with `npm run build --prefix frontend` and `npm run test:smoke --prefix frontend`.
- Feedback attachment was verified through both `edu-cs review feedback add` and `POST /api/feedback`.
- Replay, governance, and review flows now emit structured JSON logs; CLI JSON output remains available but is preceded by log lines for replay commands.
- The earlier Playwright Chromium download path was interrupted by `ECONNRESET`, so smoke validation was switched to the locally installed Microsoft Edge channel.

## What to Check During Validation

- Route correctness signals are produced and traceable
- Independent signals can be recorded without being forced into decision participation
- Closed-loop traceability works across session, evaluation, attribution, and feedback
- Query and aggregation responses obey least-visibility scope rules
- Protocol readers remain stable for the current baseline version
