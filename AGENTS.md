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

Reminder and task "Details" surfaces must be bespoke to the content. Do not
route them to stock Home Assistant `more-info` history/activity popups unless
the purpose is explicitly diagnostic. Use calm sheets or designed inline panels
that explain the task, the trigger facts, the primary action, what changes after
acting, and what the home will keep watching. If the detail is data-based, use a
beautiful compact chart; if it is educational, provide a rich explainer; if it
is sequence-based, use a polished timeline rather than the raw HA log. Follow
`docs/notification-detail-surfaces.md` for project-wide detail-surface rules.

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
