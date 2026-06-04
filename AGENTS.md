# AGENTS.md

This repository contains a Home Assistant configuration.

The goal of this system is to maintain a **beautiful, calm, and reliable smart home interface** while preserving clean, maintainable configuration.

Agents working in this repository should prioritize **design clarity, reliability, and elegant configuration**.

---

# Core Priorities

1. Reliability of the home system
2. Visual clarity and calm interface design
3. Maintainable, readable configuration
4. Thoughtful use of the Home Assistant ecosystem

Changes should always favor **minimal safe improvements** over large refactors.

---

# Audit And Diagnostic Memory

When running an audit, diagnostic, incident review, or reliability investigation,
start by checking the repo's historical context before forming a fresh theory.
At minimum, review `docs/audit-history/README.md`, any relevant dated entries in
`docs/audit-history/`, and nearby runbooks such as remote-access, UI hardening,
device inventory, or dashboard audit notes.

Use that history actively:

- compare the current symptom to prior incidents and fixes;
- look for repeated entities, integrations, dashboards, add-ons, network paths,
  and deployment tools;
- preserve earlier evidence even when a newer hypothesis looks stronger;
- avoid rediscovering or undoing prior decisions without a deliberate reason.

After a meaningful audit or diagnostic fix, add a dated Markdown entry under
`docs/audit-history/` with the symptom, evidence, ranked findings, changes made,
checks run, deployment status, residual risks, and next follow-ups. Keep secrets,
tokens, private URLs, raw logs, and exact sensitive identifiers out of committed
reports.

---

# Design Philosophy

The user interface should feel **calm, modern, and minimal**, inspired by the design language used in Apple products.

Preferred characteristics include:

- minimal visual clutter
- generous spacing
- strong visual hierarchy
- subtle color use
- fluid and polished interactions

Dashboards should feel closer to a **well-designed mobile application** than a traditional control panel.

The interface should prioritize **clarity, elegance, and glanceability**.

Users should be able to understand the state of the home in **2–3 seconds**.

---

# Visual Design Principles

Prefer:

- simple layouts
- consistent spacing
- limited color palettes
- clean typography
- subtle visual hierarchy

Avoid:

- dense grids of controls
- flashing or highly saturated colors
- cluttered dashboards
- overly decorative UI elements

Whitespace and grouping should be used intentionally to guide attention.

---

# Dashboard Layout Guidelines

Dashboards should be:

- **mobile-first**
- vertically readable
- grouped by room or purpose
- easy to scan quickly

Preferred layout patterns:

- vertical stacks
- small grouped card clusters
- consistent card widths
- strong visual grouping

Avoid dashboards that require excessive scrolling or contain large control matrices.

Favor **fewer, higher-quality dashboards** over many fragmented ones.

---

# Preferred UI Components

Well-maintained community components are encouraged when they improve usability or aesthetics.

Preferred components include:

- Mushroom cards
- ApexCharts
- Button-card
- Mini-graph-card
- card-mod

Use HACS responsibly and prefer widely adopted components.

Avoid custom cards that:

- are unmaintained
- introduce unnecessary visual complexity
- significantly degrade performance.

---

# Visualization Philosophy

Charts should communicate **meaningful trends**, not raw telemetry.

Prefer:

- clean time-series charts
- restrained color palettes
- clear labeling and units
- sensible time windows (day / week / month)

Avoid charts that are:

- too small to read
- redundant
- visually noisy.

For ApexCharts and other dashboard chart edits, follow
`docs/dashboard-chart-audit.md`. If a phone screenshot looks unchanged after a
YAML edit, first verify whether Home Assistant is serving the updated dashboard
before changing chart values again.

---

# Notification Style

Notifications should feel personal, warm, and immediately scannable.

When creating or changing notification automations, follow
`docs/notification-reliability-patterns.md`. Important alerts must use durable
timestamp or cycle helpers for idempotency; do not rely on a restored boolean as
the only "already notified" or "handled this cycle" guard.

When creating or changing push notifications for Trevor, include a small, appropriate emoji cue in the title. The emoji should match the notification's job:

- use gentle, cute icons for routine care and reminders
- use clearer attention icons for issues that need prompt action
- name the specific action or issue in the title so similar reminders are easy to distinguish at a glance
- avoid excessive emoji or decorative clutter

For coffee and espresso maintenance, prefer concise coffee-themed emoji pairs and explicit titles, such as `☕💧 Profitec GO water backflush` and `☕🧼 Profitec GO Cafiza clean`.

Notification and attention controls should also be immediately legible in the
dashboard. Prefer plain-language labels and inline actions tied to the specific
item that needs attention. Avoid shorthand chips, unlabeled utility controls, or
notification snooze/toggle controls mixed into unrelated care dashboards; put
those in the notification center or a clearly labeled settings surface.
Never attach durable state-changing actions to large summary/hero cards where a
stray tap can mutate the home model. Use an expand/caret action drawer, a
clearly labeled button with confirmation, or a durable dropdown/select control.

The Notification Center's Recent section is for meaningful notifications and
important state changes, not routine action receipts. Do not show low-signal
completion taps such as `Water done`, `Done`, `Captured`, `Snoozed`, or `Opened`
as recent notifications by default. Record them only as internal history unless
there is a clear audit or safety reason to surface the action; opt into Recent
explicitly with action/event metadata such as `recent: true` or
`keep_recent: true` / `history: recent`.

For deadline-based notices, keep the due date and the action window separate.
Upcoming is a timeline: if an item has a meaningful due, expiration, review, or
deadline date and that date is inside the current Upcoming horizon, it should
appear there by the actual due date, not by the first reminder date. Needs
Attention is the action queue: it should appear when the current cycle's work is
ready to be handled, paid, renewed, checked, or scheduled. It is acceptable and
often preferred for the same current-cycle item to appear in both Needs
Attention and Upcoming when the action window is open and the due date remains
inside the timeline horizon. In those cases, use the real due date in the meta
line and show the reminder/opening date only as supporting context.

Recurring deadline notices must clear only the current period when marked done.
For annual or periodic items such as property taxes, franchise tax, passport
renewals, maintenance, or reviews, the completion action should stamp the active
cycle and stop current notifications without suppressing future cycles.

Reminder and task "Details" surfaces must be bespoke to the content. Do not
route them to stock Home Assistant `more-info` history/activity popups unless
the purpose is explicitly diagnostic. Use calm sheets or designed inline panels
that fit the notice. Actionable reminders should explain the task, trigger
facts, primary action, what changes after acting, and what the home keeps
watching. Ambient notes, FYIs, seasonal observations, and fun facts may use
softer labels and omit action-heavy sections. If the detail is data-based, use a
beautiful compact chart; if it is educational, provide a rich explainer; if it
is sequence-based, use a polished timeline rather than the raw HA log. Follow
`docs/notification-detail-surfaces.md` for project-wide detail-surface rules.
When a notice has an `Open page` affordance, point it to the actual next useful
destination whenever possible, such as the official tax payment page, renewal
portal, source document, or relevant dashboard. Avoid placeholder self-links.
If opening that destination requires an identifier, account number, file number,
serial number, or confirmation code, include it in the detail facts with a
copyable value.

---

# Code Quality

Configuration should emphasize **clarity and maintainability**.

Guidelines:

- YAML must remain readable
- avoid unnecessary complexity
- prefer simple and explicit logic
- comment non-obvious logic
- use reusable patterns where appropriate

When editing configuration:

- avoid clever but fragile solutions
- avoid large structural refactors unless requested.
- when adding or renaming real Home Assistant devices/entities, update
  `docs/device-inventory.json` and `docs/device-inventory.md`, then run
  `python3 tools/check_device_inventory_coverage.py` so active config
  references cannot drift away from the inventory.

## Configuration Structure / Decomposition

Treat configuration structure as reliability work, not mere tidiness.
`configuration.yaml` should stay close to a table of contents plus truly global
settings. Large or steadily growing domains should live in included files with
coherent ownership, such as `sensors.yaml`, `templates.yaml`, `lights.yaml`,
`command_line.yaml`, `shell_commands.yaml`, or purpose-specific helper files.

Split configuration when any of the following are true:

- a section has a clear independent job or owner;
- a routine edit requires navigating a very large file;
- a section is more than roughly 50-100 lines and likely to keep growing;
- a file is approaching tooling or deploy-path fragility;
- the split reduces blast radius without making navigation harder.

Prefer domain- or purpose-based includes over arbitrary buckets. Avoid names
like `misc.yaml`, `part1.yaml`, or one-file-per-entity fragmentation unless
there is a strong operational reason.

For this repository, keep `configuration.yaml` comfortably below known
File Editor fragility thresholds. If it grows past roughly 150 KB, actively look
for coherent domains to move out. If it approaches 300 KB, treat decomposition
as reliability work that should happen before unrelated feature work. After any
include split, run local YAML parsing and Home Assistant config validation
before restart, and verify the live file read-back when deploying through File
Editor or any browser-mediated path.

For live deployment, follow `docs/home-assistant-deploy-runbook.md`. Do not run
the browser deploy helper from a normal dashboard page; it must run from a
mounted File Editor ingress iframe or it will hit the wrong `api/save` endpoint.
If local `homeassistant.local` is disconnected or File Editor does not mount,
try the Nabu Casa Remote UI File Editor route and verify `hass.connected ===
true` plus an iframe whose `src` contains `/api/hassio_ingress/` before writing.

Current split context:

- `configuration.yaml` remains the main table of contents and contains broad
  global configuration plus domains that have not yet justified a separate
  include.
- `automations.yaml` is intentionally a tiny `!include_dir_merge_list
  automations` pointer. The actual automation lists live in
  `automations/00-water-irrigation.yaml`,
  `automations/10-lighting-security.yaml`,
  `automations/20-climate-garden-commute.yaml`, and
  `automations/30-maintenance-environment.yaml`. Keep those chunks coherent and
  small enough for reliable browser/File Editor read-back; do not collapse them
  back into one large file.
- `scripts.yaml` and `scenes.yaml` remain the standard Home Assistant-managed
  includes.
- `sensors.yaml` contains the statistics sensor block that was split out after
  File Editor truncated the tail of a large `configuration.yaml` during live
  deploy.
- `lights.yaml` contains the YAML light group definitions that previously lived
  at the end of `configuration.yaml`.
- `dashboards/*.yaml` contains YAML Lovelace dashboards, including
  `dashboards/calm_mobile.yaml` for the primary calm mobile dashboard and
  `dashboards/ha_safe.yaml` for the stock diagnostic dashboard.

Do not fold `sensors.yaml` or `lights.yaml` back into `configuration.yaml`
without a deliberate reason and a successful live read-back/config-check plan.

---

# Git Hygiene / Commit Cadence

After completing a logical change and running the relevant checks, stage only
the files or hunks related to that change and commit before moving to unrelated
work.

Preferred cadence:

1. Inspect `git status --short` before editing.
2. Make one coherent change.
3. Run the smallest meaningful YAML, dashboard, script, or config checks.
4. Inspect the staged diff with `git diff --cached --stat` and `git diff --cached --check`.
5. Commit the logical slice with a clear message.

When the worktree already contains unrelated edits, preserve them. Use focused
staging instead of broad whole-file commits until each commit is thematically
clean.

Do not commit scratch files, local test payloads, `.DS_Store`, caches, logs, or
secrets.

---

# Community Ecosystem

The Home Assistant ecosystem is encouraged when used thoughtfully.

HACS integrations and community cards are acceptable when they:

- materially improve functionality or design
- are actively maintained
- integrate cleanly with Home Assistant.

Prefer mature, widely adopted integrations.

---

# YAML vs UI Configuration

Home Assistant stores configuration in both YAML and UI-managed `.storage` files.

Agents should:

- recognize that not all configuration exists in YAML
- avoid assuming dashboards or automations are fully represented in files
- avoid modifying `.storage` unless explicitly required.

---

# Safety Guidelines

Agents must:

- never expose secrets
- respect `.gitignore`
- avoid committing logs, databases, or sensitive tokens
- avoid breaking working automations or dashboards.

If uncertain about a change, explain the risk before modifying configuration.

---

# Expected Behavior

When reviewing the repository:

1. Identify the highest priority issues
2. Explain why they matter
3. Propose minimal safe improvements
4. Suggest optional higher-impact improvements afterward
