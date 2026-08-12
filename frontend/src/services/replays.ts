export type ReplayTimeline = {
  session_id: string;
  status: string;
  events: Array<{ event_id: string; seq: number; actor_kind: string; content?: string }>;
  evaluations: Array<{
    evaluation_id: string;
    evaluation_kind: string;
    label: string;
    value?: { summary?: string; severity?: string; recommended_action?: string };
    signal_key?: string | null;
    primary_source?: { source_type: string; source_ref: string } | null;
  }>;
};

export type ReviewAggregate = {
  session_count: number;
  completed_count: number;
};

const fallbackTimeline: ReplayTimeline = {
  session_id: "replay-001",
  status: "completed",
  events: [{ event_id: "evt-001", seq: 1, actor_kind: "customer", content: "我今天想请假，但是不知道规则。" }],
  evaluations: [
    {
      evaluation_id: "replay-001:risk:leave_followup_gap",
      evaluation_kind: "risk",
      label: "leave_followup_gap",
      value: { severity: "medium", summary: "Leave request may remain unresolved without follow-up." },
      primary_source: { source_type: "rule", source_ref: "risk-leave-followup.v1" }
    },
    {
      evaluation_id: "replay-001:signal:attention_shift",
      evaluation_kind: "signal",
      label: "attention_shift",
      signal_key: "attention_shift",
      primary_source: { source_type: "rule", source_ref: "signal-attention.v1" }
    }
  ]
};

const fallbackAggregate: ReviewAggregate = {
  session_count: 1,
  completed_count: 1
};

export async function fetchReplayTimeline(sessionId: string): Promise<ReplayTimeline> {
  try {
    const response = await fetch(`/api/replays/${sessionId}/timeline`);
    if (!response.ok) throw new Error("timeline request failed");
    return (await response.json()) as ReplayTimeline;
  } catch {
    return fallbackTimeline;
  }
}

export async function fetchReviewAggregate(): Promise<ReviewAggregate> {
  try {
    const response = await fetch("/api/review/aggregate");
    if (!response.ok) throw new Error("aggregate request failed");
    return (await response.json()) as ReviewAggregate;
  } catch {
    return fallbackAggregate;
  }
}
