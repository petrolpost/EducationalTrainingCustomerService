# Quickstart - Educational Training Customer Service Core

## Purpose

Validate the approved v1 slice end to end: baseline configuration, replay processing, provenance, scoped review, and feedback attachment.

## Prerequisites

- Python 3.12 available
- Node.js 20+ available
- repository dependencies installed for backend and frontend
- SQLite available through the Python standard runtime

## Validation Scenarios

### Scenario 1: Validate baseline configuration

1. Prepare the backend environment.
2. Run configuration validation against the active baseline config.

```bash
edu-cs config validate
```

**Expected Outcome**
- configuration passes schema checks
- version metadata and rollback target are visible
- invalid config exits non-zero

### Scenario 2: Run a replay session through the core

1. Prepare a replay payload matching the [replay protocol contract](./contracts/replay-protocol.md).
2. Run replay through the CLI.

```bash
edu-cs replay run --input ./fixtures/replay-session.json --output json
```

**Expected Outcome**
- a replay session is created
- ordered events are processed
- route, signals, and provenance records are generated
- normalized results can be queried later

### Scenario 3: Inspect replay timeline and provenance

1. Start the API service.
2. Query replay summary and timeline.

```bash
curl http://localhost:8000/api/replays/replay_001
curl http://localhost:8000/api/replays/replay_001/timeline
```

**Expected Outcome**
- replay summary is returned for authorized scope
- timeline includes structured evaluations and provenance
- primary and contributing sources are visible

### Scenario 4: Verify scoped query behavior

1. Authenticate as different role templates.
2. Query replay list and aggregate views.

```bash
curl http://localhost:8000/api/replays
curl "http://localhost:8000/api/reviews/aggregates?group_by=route_label"
```

**Expected Outcome**
- seat/school role sees only allowed scope
- school manager sees school-wide scope only
- tenant manager sees tenant-wide scope
- platform auditor remains read-only by default

### Scenario 5: Attach feedback and verify closed-loop traceability

1. Submit feedback to a replay result.

```bash
curl -X POST http://localhost:8000/api/feedback \
  -H "Content-Type: application/json" \
  -d "{\"session_id\":\"replay_001\",\"evaluation_id\":\"eval_001\",\"feedback_type\":\"corrected\",\"feedback_payload\":{\"note\":\"降为观察型\"}}"
```

**Expected Outcome**
- feedback is stored successfully
- feedback links back to replay result and provenance
- replay review surfaces can show that the conclusion was corrected

## What to Check During Validation

- Route correctness signals are produced and traceable
- Independent signals can be recorded without being forced into decision participation
- Closed-loop traceability works across session, evaluation, attribution, and feedback
- Query and aggregation responses obey least-visibility scope rules
- Protocol readers remain stable for the current baseline version
