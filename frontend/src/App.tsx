import { useMemo, useState } from "react";
import { ReplayReviewPage } from "./pages/ReplayReviewPage";
import { ReviewDashboardPage } from "./pages/ReviewDashboardPage";
import { createDefaultReviewScope } from "./state/reviewScope";

type RouteKey = "replay" | "dashboard";

export default function App() {
  const [route, setRoute] = useState<RouteKey>("replay");
  const scope = useMemo(() => createDefaultReviewScope(), []);

  return (
    <div style={{ fontFamily: "sans-serif", padding: 24 }}>
      <header style={{ display: "flex", gap: 12, marginBottom: 24 }}>
        <button onClick={() => setRoute("replay")}>Replay Review</button>
        <button onClick={() => setRoute("dashboard")}>Review Dashboard</button>
      </header>
      {route === "replay" ? <ReplayReviewPage scope={scope} /> : <ReviewDashboardPage scope={scope} />}
    </div>
  );
}
