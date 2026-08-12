# Data Model - Educational Training Customer Service Core

## 1. ReplaySession

**Purpose**: Represents a single offline replay run and its governing context.

**Fields**
- `session_id` - stable unique identifier
- `protocol_version` - active replay protocol version
- `tenant_id` - tenant scope
- `school_id` - optional school scope
- `created_at`
- `created_by`
- `status` - `pending | running | completed | failed`
- `source_kind` - `simulated | imported | historical`
- `event_count`
- `current_route_label`
- `anomaly_level`
- `storage_revision`

**Validation Rules**
- `tenant_id` is required
- `school_id` may be null only for tenant-wide sessions
- `protocol_version` must map to a supported reader
- `event_count` must equal the number of stored replay events

**Relationships**
- Has many `ConversationEvent`
- Has many `EvaluationRecord`
- Has many `FeedbackRecord`

**State Transitions**
- `pending -> running -> completed`
- `pending -> running -> failed`
- `failed -> running` only through explicit replay retry

## 2. ConversationEvent

**Purpose**: Represents an immutable timestamped event in a replay stream.

**Fields**
- `event_id`
- `session_id`
- `seq`
- `occurred_at`
- `event_type` - `message | stage_change | action | feedback | system_note`
- `actor_kind` - `customer | staff | system | reviewer`
- `actor_id`
- `content`
- `channel`
- `metadata_json`
- `extension_json`

**Validation Rules**
- `seq` must be unique within a session
- `occurred_at` must be present even if original ordering is recovered later
- raw event payload must remain immutable after storage

**Relationships**
- Belongs to `ReplaySession`

## 3. EvaluationRecord

**Purpose**: Stores normalized evaluation outputs generated from replay processing.

**Fields**
- `evaluation_id`
- `session_id`
- `event_id` - optional when evaluation is session-level
- `evaluation_kind` - `route | signal | risk | summary | action_recommendation`
- `label`
- `signal_key` - optional strong reference to `SignalProfile.signal_key` when this evaluation depends on a governed signal
- `value_json`
- `signal_config_version` - snapshot of `SignalProfile.current_config_version` when `signal_key` is present
- `consumption_tier_snapshot` - snapshot of signal consumption tier when `signal_key` is present
- `lifecycle_state_snapshot` - snapshot of signal lifecycle state when `signal_key` is present
- `confidence`
- `produced_at`
- `rule_or_model_revision`
- `is_primary_for_session_state`

**Validation Rules**
- `evaluation_kind` and `label` are required
- `label` is the evaluation's display/classification label and does not need to be globally unique
- `signal_key` is a strong reference only for evaluations that depend on a governed signal; it may be null for route, summary, and other non-signal-governed evaluations
- if `signal_key` is present, it must exactly match an existing `SignalProfile.signal_key`
- if `signal_key` is present, `signal_config_version` must be recorded as the snapshot of `SignalProfile.current_config_version` at production time
- if `signal_key` is present, `consumption_tier_snapshot` must be one of the approved tiers; otherwise it must be null
- if `signal_key` is present, `lifecycle_state_snapshot` must be one of the approved lifecycle states; otherwise it must be null

**Relationships**
- Belongs to `ReplaySession`
- May reference one `ConversationEvent`
- May reference one `SignalProfile` through `signal_key`
- Has one or more `AttributionRecord`

## 4. AttributionRecord

**Purpose**: Captures provenance for a single evaluation or decision.

**Fields**
- `attribution_id`
- `evaluation_id`
- `source_role` - `primary | contributing`
- `contribution_kind` - `trigger | support | verify | override`
- `source_type` - `rag | rule | model | human`
- `source_ref`
- `source_version`
- `evidence_excerpt`
- `evidence_ref`
- `recorded_at`

**Validation Rules**
- every evaluation must have exactly one primary attribution
- contributing attribution may have many entries
- `source_version` is required for any non-human source

**Relationships**
- Belongs to `EvaluationRecord`

## 5. SignalProfile

**Purpose**: Represents governance state for an independent signal family such as attention change.

**Fields**
- `signal_key`
- `display_name`
- `default_consumption_tier` - `observe | prompt | decision`
- `lifecycle_state` - `experimental | validated | frozen | retired`
- `validation_status`
- `promotion_policy_ref`
- `retirement_policy_ref`
- `current_config_version`
- `notes`

**Validation Rules**
- `signal_key` must be unique
- `default_consumption_tier` must map to an allowed tier template
- lifecycle transitions cannot be applied directly by runtime replay processing
- promotion, downgrade, freeze, and retirement are governance actions on `SignalProfile`, not on historical `EvaluationRecord` snapshots

**Relationships**
- Referenced by `EvaluationRecord`
- Governed by `BaselineConfig`
- Has many `SignalLifecycleEvent`

## 6. BaselineConfig

**Purpose**: Defines the versioned default behavior of routing, prompting, provenance, and signal consumption.

**Fields**
- `config_version`
- `spec_version`
- `created_at`
- `change_summary`
- `rollback_target`
- `schema_version`
- `config_payload`
- `status` - `draft | validated | active | superseded`

**Validation Rules**
- configuration must pass schema validation before activation
- only one baseline config can be active at a time
- active config must reference a compatible spec version

**Relationships**
- Governs `SignalProfile`
- Governs replay processing defaults

## 7. FeedbackRecord

**Purpose**: Stores human review, adoption, correction, or outcome data linked to replay results.

**Fields**
- `feedback_id`
- `session_id`
- `evaluation_id` - optional when feedback applies to session outcome
- `attribution_id` - optional when feedback targets provenance
- `feedback_type` - `adopted | corrected | rejected | outcome | audit_note`
- `feedback_actor_kind`
- `feedback_actor_id`
- `feedback_payload`
- `recorded_at`

**Validation Rules**
- feedback must attach to at least one of `session_id`, `evaluation_id`, or `attribution_id`
- write permissions depend on role template and scope policy

**Relationships**
- Belongs to `ReplaySession`
- May reference `EvaluationRecord`
- May reference `AttributionRecord`

## 8. SignalLifecycleEvent

**Purpose**: Records a governance action that changes a signal's lifecycle state and/or default consumption tier.

**Fields**
- `lifecycle_event_id`
- `signal_key`
- `signal_config_version`
- `governance_tier` - `minor | major`
- `change_type` - `upgrade | downgrade | freeze | retire`
- `from_lifecycle_state`
- `to_lifecycle_state`
- `from_consumption_tier`
- `to_consumption_tier`
- `validation_report_ref`
- `approved_by`
- `approved_at`
- `decision_note`
- `recorded_at`

**Validation Rules**
- `signal_key` must reference an existing `SignalProfile`
- at least one governance axis must change: lifecycle state or consumption tier
- `major` governance events must include `validation_report_ref`
- a lifecycle event only becomes effective if it is approved
- writing an effective lifecycle event must synchronously update `SignalProfile.lifecycle_state`, `SignalProfile.default_consumption_tier`, and `SignalProfile.current_config_version`

**Relationships**
- Belongs to `SignalProfile`

## 9. RoleTemplate

**Purpose**: Encodes default query and aggregation scope for a class of users.

**Fields**
- `role_template_key` - `seat_school | school_manager | tenant_manager | platform_auditor`
- `scope_level` - `self | school | tenant | explicit_grant`
- `read_mode` - `read_only | scoped_operate`
- `can_cross_school`
- `can_cross_tenant`
- `requires_explicit_grant`

**Validation Rules**
- platform auditor defaults to `read_only`
- cross-school and cross-tenant visibility require explicit grant unless covered by tenant scope policy

**Relationships**
- Applied to authenticated reviewers and operators

## 10. ScopeGrant

**Purpose**: Represents explicit authorization that widens visibility beyond default least-visible scope.

**Fields**
- `grant_id`
- `principal_id`
- `role_template_key`
- `tenant_id`
- `school_id`
- `grant_scope`
- `granted_by`
- `granted_at`
- `expires_at`

**Validation Rules**
- grants cannot widen privilege beyond the role template's allowed ceiling
- expired grants must not participate in scope resolution

**Relationships**
- Works with `RoleTemplate` during scope resolution
