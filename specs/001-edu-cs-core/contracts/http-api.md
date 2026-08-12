# HTTP API Contract

## Purpose

Defines the minimum v1 API surface for replay submission, replay inspection, feedback attachment, and scoped review.

## Base Principles

- API is tenant-aware by default
- visibility is resolved server-side from role template + scope grant
- request filters cannot expand authorization
- all write operations remain subject to role and scope policy

## Endpoints

### `POST /api/replays`

Submit a replay session for processing.

**Request**
- body follows replay protocol input contract

**Response**
- `202 Accepted`

```json
{
  "session_id": "replay_001",
  "status": "pending"
}
```

### `GET /api/replays/{session_id}`

Retrieve replay session summary and current processing status.

**Response**
- `200 OK` when authorized
- `404` or equivalent hidden-not-found behavior when outside authorized scope

### `GET /api/replays/{session_id}/timeline`

Retrieve ordered replay events and normalized evaluations for review.

**Response**
- ordered event list
- evaluation list
- provenance summary

### `GET /api/replays`

List replay sessions within authorized scope.

**Query Parameters**
- `tenant_id` (optional filter only)
- `school_id` (optional filter only)
- `status`
- `route_label`
- `page`
- `page_size`

**Rules**
- query filters intersect with server-resolved scope
- cross-school or cross-tenant access requires explicit authorization

### `GET /api/reviews/aggregates`

Return scoped aggregate views for management or QA review.

**Query Parameters**
- `group_by` - must be in an allowlist
- `from`
- `to`
- `route_label`

**Rules**
- aggregates must be computed from authorized data only
- unauthorized group dimensions must be rejected

### `POST /api/feedback`

Attach review feedback to a replay session, evaluation, or attribution record.

**Request**

```json
{
  "session_id": "replay_001",
  "evaluation_id": "eval_001",
  "feedback_type": "corrected",
  "feedback_payload": {
    "note": "应降为观察型"
  }
}
```

**Response**
- `201 Created`

## Authorization Contract

- default role templates:
  - `seat_school`
  - `school_manager`
  - `tenant_manager`
  - `platform_auditor`
- platform auditor is read-only by default
- scope resolution applies to:
  - list queries
  - detail queries
  - aggregate queries
  - replay review views

## Error Contract

- invalid protocol payload: `400`
- invalid configuration version or unsupported schema version: `422`
- unauthorized write operation: `403`
- out-of-scope read: hidden `404` behavior is acceptable
