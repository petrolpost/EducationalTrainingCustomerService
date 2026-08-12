# Backend

This backend provides a replay-first service core for the `001-edu-cs-core` feature.

## Setup

- `python -m pip install -e ".\\backend[dev]"`
- `edu-cs bootstrap-db`
- `python -m uvicorn edu_cs_core.api.app:create_app --factory --host 127.0.0.1 --port 8000`

## Validation Commands

- `python -m pytest backend/tests`
- `edu-cs replay run --input backend/tests/fixtures/replay_session.json --output json`
- `edu-cs replay show --session replay-001 --output json`
- `edu-cs replay timeline --session replay-001 --output json`
- `edu-cs review feedback add --session-id replay-001 --evaluation-id replay-001:route --attribution-id replay-001:route:primary --feedback-type corrected --payload "{\"note\":\"需要人工复核\"}" --output json`
- `edu-cs config validate --input backend/tests/fixtures/baseline_config_a.json`
- `edu-cs config diff --left backend/tests/fixtures/baseline_config_a.json --right backend/tests/fixtures/baseline_config_b.json --output json`

## Developer Notes

- SQLite is used as the local persistence layer during the current implementation stage.
- The default local database lives at `backend/.data/edu_cs_core.sqlite3`.
- Governed signal snapshots are persisted with replay evaluations.
- Scope-sensitive review endpoints honor tenant-level least visibility by default.
- Replay, governance, and review flows emit structured JSON logs through `edu_cs_core.services.logging`.
