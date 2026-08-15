# Greenroom

Client-side web apps for running a church service. No build step, no backend — open the HTML directly in a browser.

- [`index.html`](index.html) — **Greenroom**, the parent app. People profiles, teams and positions, services, order-of-service planning by drag-and-drop, and team scheduling. Embeds Chart Builder as a tab.
- [`chart-builder/`](chart-builder/index.html) — chord/lyric chart editor with Nashville Number System support, transposition, and PDF/print export. Sample song exports live in `chart-builder/sample-data/`.
- [`service-planner/`](service-planner/index.html) — an earlier standalone cue-sheet prototype, superseded by Greenroom. Kept only for reference.

## How the two main apps relate

Chart Builder stays the single source of truth for charts. Greenroom does not reimplement any chart editing — it reads Chart Builder's song library (read-only) and embeds the editor itself in the **Chart Builder** tab, so the same app serves both the standalone and the embedded use.

Opening a song from a service plan or the song library deep-links into the editor via `chart-builder/index.html?song=<id>`.

## Branding

Greenroom uses the mint green Chart Builder already uses for its Lyrics mode (`#6fe0a0` on `#0d2b1a`) as its accent; Chart Builder keeps amber. Neutrals, spacing, and control styling are shared token-for-token, so the two read as one product while staying distinguishable when one is running inside the other.

Amber survives in Greenroom as `--warn` (partial team coverage, a library that's connected but empty) — against a green accent, a green caution state would read as success.

## Storage

| Database | Owner | Contents |
| --- | --- | --- |
| `GreenroomDB` | parent app | people, services, imported songs, preferences |
| `WorshipChartBuilderDB` | Chart Builder | songs, preferences (read-only from the parent) |

Both are IndexedDB, and **IndexedDB is scoped per origin**. The parent app can only see Chart Builder's library when both are served from the same origin — which `file://` does not provide. Serve the folder over HTTP instead.

## Running it

Double-click [`run.cmd`](run.cmd). It starts a local server and opens the app; leave the window open while you work, close it to stop.

Equivalently, from the repo folder:

```bash
python -m http.server 8777
```

Then visit `http://127.0.0.1:8777/`. Bookmark that — it's the app's address.

Opening `index.html` directly from Explorer mostly works, but the Songs tab won't see Chart Builder's library. In that case the banner says so and offers a JSON import of chart exports instead; everything else is unaffected. Chart Builder's PDF export also needs an internet connection, since it pulls its PDF library from a CDN.

## Settings

The ⚙ button in the top bar opens a drawer, matching Chart Builder's own Settings drawer:

- **Organization** — the name shown beside the logo.
- **Service types** — see below.
- **Scheduling** — whether auto-fill may schedule guests, whether it skips people blocked out on the date, and whether double-booking is flagged. These change what auto-fill *offers*; they never move anyone already scheduled.
- **Song library** — connection status and a refresh.
- **Data** — export a full backup (people, services, positions, preferences), restore one, or clear the local database and start over from the sample roster.

Backups do not include charts; those live in Chart Builder and back up from its own Settings.

## Service types

A type is both a **template** and a **grouping**. Sunday ships as the default; add Wednesday, Youth, Good Friday or anything else in Settings.

Each type carries a **color**, weekday, start time, default title and venue. The color shows as a dot on the section heading and a spine down the leading edge of every service card in that type — a different form from the teams' round pips, so the two color scales never read as the same thing. Colors come from a fixed eight-swatch palette that is contrast-checked against the dark background, and new types take the first unused one automatically. A new service of that type opens on the next occurrence of its weekday, pre-filled — so a Wednesday type lands on Wednesday at 6:30pm without you touching the date field.

The Services tab sections by type, and each section has its own **+ New** that pre-selects it. Empty types still show a section, so a type you just created has somewhere to add its first service.

Changing a service's type (the dropdown in the plan toolbar) only re-files it under a different heading — it never rewrites a title, date or time you have already set. Deleting a type moves its services to another type rather than deleting them.

## Teams

Scoped to the six that run a service: Preacher, Worship, Audio, Visual, Tech, Streaming. Positions within each are editable in the Teams tab and drive both what you can schedule and what a profile can be qualified for.
