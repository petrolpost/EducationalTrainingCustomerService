# Frontend

This lightweight console is the validation surface for replay review and scoped aggregate inspection in `001-edu-cs-core`.

## Setup

- `npm install`
- `npm run dev -- --host 127.0.0.1 --port 5173`

## Validation Commands

- `npm run build`
- `npm run test:smoke`

## Developer Notes

- Smoke tests now start Vite automatically through the Playwright `webServer` setting and reuse an existing local server when one is already running.
- Smoke validation uses the locally installed Microsoft Edge channel, which avoids blocking on Playwright browser downloads during local setup.
- The console falls back to local sample data when backend APIs are unavailable, which keeps the review UI testable during early integration.
- The app is intentionally small and can later be replaced by a broader control-plane shell without changing backend contracts.
