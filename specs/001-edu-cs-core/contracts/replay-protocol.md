# Replay Protocol Contract

## Purpose

Defines the v1 contract for timestamped replay events and normalized replay outputs consumed by CLI, API, recorder, and review surfaces.

## Versioning Model

- Protocol uses `schema_version`
- Core fields stay stable across minor evolution
- Experimental and research-oriented fields live under `extensions.<namespace>`
- Readers must normalize data with priority: `core -> legacy extension -> default`

## Replay Input Envelope

```json
{
  "schema_version": "1.0",
  "session": {
    "session_id": "replay_001",
    "tenant_id": "tenant_a",
    "school_id": "school_01",
    "source_kind": "simulated"
  },
  "events": [
    {
      "event_id": "evt_001",
      "seq": 1,
      "occurred_at": "2026-08-12T12:00:00Z",
      "event_type": "message",
      "actor_kind": "customer",
      "actor_id": "cust_001",
      "content": "我今天想请假，但是不知道规则。",
      "channel": "simulator",
      "metadata": {},
      "extensions": {}
    }
  ]
}
```

## Required Core Fields

### Session
- `session_id`
- `tenant_id`
- `source_kind`

### Event
- `event_id`
- `seq`
- `occurred_at`
- `event_type`
- `actor_kind`

## Replay Output Contract

```json
{
  "schema_version": "1.0",
  "session_id": "replay_001",
  "status": "completed",
  "route": {
    "label": "in_service.leave_consultation",
    "confidence": 0.87
  },
  "evaluations": [
    {
      "evaluation_id": "eval_001",
      "evaluation_kind": "signal",
      "label": "attention_shift",
      "consumption_tier": "observe",
      "lifecycle_state": "experimental",
      "value": {
        "summary": "客服连续两轮未正面回应主诉"
      },
      "primary_source": {
        "source_type": "rule",
        "source_ref": "attention-rule.v1",
        "source_version": "1.0"
      },
      "contributing_sources": [
        {
          "contribution_kind": "support",
          "source_type": "model",
          "source_ref": "dialog-model",
          "source_version": "0.3"
        }
      ],
      "extensions": {
        "signals.attention": {
          "raw_score": 0.62
        }
      }
    }
  ]
}
```

## Compatibility Rules

- New required core fields require a protocol version bump
- Fields promoted from `extensions` into core must remain readable from historical records through normalization
- Historical replay records are not required to backfill experimental fields

## Validation Rules

- `seq` must be unique inside a session
- replay events must be processed in `seq` order
- all evaluations must include one primary source
- any scope-bearing replay must carry `tenant_id`
