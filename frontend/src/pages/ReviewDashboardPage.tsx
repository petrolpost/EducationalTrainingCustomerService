import { useEffect, useState } from "react";
import { fetchReviewAggregate, type ReviewAggregate } from "../services/replays";
import type { ReviewScope } from "../state/reviewScope";

export function ReviewDashboardPage({ scope }: { scope: ReviewScope }) {
  const [aggregate, setAggregate] = useState<ReviewAggregate | null>(null);

  useEffect(() => {
    fetchReviewAggregate().then(setAggregate);
  }, []);

  return (
    <main>
      <h1>Review Dashboard</h1>
      <p>
        Scope: {scope.roleTemplate} / {scope.tenantId}
      </p>
      <section aria-label="aggregate-review">
        <h2>Aggregate Review</h2>
        <div>Session count: {aggregate?.session_count ?? 0}</div>
        <div>Completed count: {aggregate?.completed_count ?? 0}</div>
      </section>
    </main>
  );
}
