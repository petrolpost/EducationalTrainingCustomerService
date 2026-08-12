# CLI Contract

## Purpose

Defines the minimum v1 CLI interface for replay submission, inspection, validation, and feedback-oriented review workflows.

## Command Principles

- CLI is a first-class interface, not a debug afterthought
- commands must support both human-readable output and JSON output
- non-zero exit codes indicate validation or processing failure

## Commands

### `edu-cs replay run`

Run a replay session from a protocol input file.

**Example**

```bash
edu-cs replay run --input ./fixtures/replay.json --output json
```

**Behavior**
- validates protocol payload
- processes replay session
- writes normalized results to storage
- prints summary or JSON result

### `edu-cs replay show`

Show replay session summary.

**Example**

```bash
edu-cs replay show --session replay_001 --output json
```

### `edu-cs replay timeline`

Show ordered replay events and normalized evaluations for a session.

### `edu-cs config validate`

Validate baseline configuration against schema and consistency rules.

### `edu-cs config diff`

Compare two baseline configuration versions.

### `edu-cs review feedback add`

Attach review feedback to a replay session, evaluation, or attribution record.

## Output Contract

### Human Output

- concise summary of replay status
- route label
- anomaly summary
- counts of evaluations and feedback references

### JSON Output

Commands supporting `--output json` must emit machine-readable structures that match the normalized replay and feedback records used by the API.

## Exit Codes

- `0`: success
- `1`: general processing failure
- `2`: validation failure
- `3`: unauthorized or out-of-scope operation
