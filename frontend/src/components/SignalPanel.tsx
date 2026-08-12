type SignalPanelProps = {
  signalKey: string;
  primarySource?: string;
};

export function SignalPanel({ signalKey, primarySource }: SignalPanelProps) {
  return (
    <section aria-label="signal-panel" style={{ border: "1px solid #ddd", padding: 12, borderRadius: 8 }}>
      <h3>Signal Panel</h3>
      <div>Signal: {signalKey}</div>
      <div>Primary source: {primarySource ?? "n/a"}</div>
    </section>
  );
}
