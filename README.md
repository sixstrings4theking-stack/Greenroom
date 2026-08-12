# WorshipTools

Two standalone, client-side web apps for running a church service.

- [`chart-builder/`](chart-builder/index.html) — chord/lyric chart editor with Nashville Number System support, transposition, and PDF/print export. Sample song exports live in `chart-builder/sample-data/`.
- [`service-planner/`](service-planner/index.html) — cue sheet / service scheduler for building an order of service and assigning teams (preacher, musicians, audio, visual).

Each app is a single self-contained `index.html` (no build step, no backend) — open it directly in a browser. Data is stored client-side (IndexedDB for Chart Builder, in-memory for Service Planner).
