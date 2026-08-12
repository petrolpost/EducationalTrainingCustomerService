import { useEffect, useState } from "react";
import { SignalPanel } from "../components/SignalPanel";
import { fetchReplayTimeline, type ReplayTimeline } from "../services/replays";
import type { ReviewScope } from "../state/reviewScope";

export function ReplayReviewPage({ scope }: { scope: ReviewScope }) {
  const [timeline, setTimeline] = useState<ReplayTimeline | null>(null);

  useEffect(() => {
    fetchReplayTimeline("replay-001").then(setTimeline);
  }, []);

  const signalEvaluation = timeline?.evaluations.find((evaluation) => evaluation.evaluation_kind === "signal");
  const anomalyEvaluations = timeline?.evaluations.filter((evaluation) => evaluation.evaluation_kind === "risk") ?? [];

  return (
    <main>
      <h1>Replay Review</h1>
      <p>
        Scope: {scope.roleTemplate} / {scope.tenantId}
      </p>
      <section aria-label="timeline">
        <h2>Timeline</h2>
        <ul>
          {timeline?.events.map((event) => (
            <li key={event.event_id}>
              {event.seq}. {event.actor_kind}: {event.content}
            </li>
          ))}
        </ul>
      </section>
      <section aria-label="anomalies">
        <h2>Anomalies</h2>
        <ul>
          {anomalyEvaluations.map((evaluation) => (
            <li key={evaluation.evaluation_id}>
              {evaluation.label}: {evaluation.value?.summary ?? "n/a"}
            </li>
          ))}
        </ul>
      </section>
      <section aria-label="provenance">
        <h2>Provenance</h2>
        <ul>
          {timeline?.evaluations.map((evaluation) => (
            <li key={evaluation.evaluation_id}>
              {evaluation.label} via {evaluation.primary_source?.source_ref ?? "n/a"}
            </li>
          ))}
        </ul>
      </section>
      {signalEvaluation ? (
        <SignalPanel
          signalKey={signalEvaluation.signal_key ?? signalEvaluation.label}
          primarySource={signalEvaluation.primary_source?.source_ref}
        />
      ) : null}
    </main>
  );
}
