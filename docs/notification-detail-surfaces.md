# Notification detail surfaces

Notification and task details should be designed surfaces, not raw Home
Assistant entity popups. A person opening "Details" is asking what the home
knows, why it matters now, and what should happen next.

## Core rule

Do not send reminder, task, or workflow "Details" actions to HA `more-info`
unless the surface is explicitly diagnostic. Raw entity history is for
telemetry inspection; it is not the right UX for deciding whether to plant,
clean, check, renew, snooze, or resolve something.

For Notification Center, render custom calm detail sheets inside
`www/house-notices-card.js`. Other dashboards may use designed inline panels,
browser-mod dialogs, or domain-specific custom cards, but they should follow
the same content standard.

## What a detail surface should answer

Every task/reminder detail should make these clear:

- What this means: one plain-language explanation of the situation.
- Why now: the facts or thresholds that triggered the notice.
- What to do: the primary action, plus useful secondary actions like snooze.
- What happens next: how Home Assistant state, future notifications, and the
  dashboard narrative change after the action.
- What will be watched afterward: the concise rule or sensor set that remains
  active.

If a detail view cannot answer those questions, improve the notice data before
adding more UI.

## Choose the right surface

Use a bespoke surface based on the message:

- Action and rationale: best for reminders and tasks. Use summary, compact
  facts, after-action text, and direct buttons.
- Data and trend: use a beautiful compact chart when the trend changes the
  decision. Prefer ApexCharts or a custom chart with restrained colors, clear
  units, visible thresholds, and a sensible time window.
- Timeline: use a calm visual timeline or bulleted history when sequence
  matters. Do not expose the stock HA activity/history view as the primary
  explanation.
- Education: use a short explainer with facts, care notes, and confidence
  context when the purpose is understanding.
- Diagnostics: use HA `more-info` only for raw entities, troubleshooting,
  calibration, and telemetry-focused dashboard cards where the user expects
  history/debug controls.

## Data contract

Notice items in `sensor.house_notice_timeline` may include:

- `date`: the real date the item is due, expires, should be reviewed, or should
  otherwise appear on the Upcoming timeline.
- `due_prefix`: the label for `date`, usually `Due`, `Expires`, `Review`, or
  `Check`.
- `basis_date` / `basis_prefix`: supporting context, such as when reminders
  start, when the bill opens, or the prior maintenance record.
- `show_in_upcoming`: true when an action-window item should still appear in
  Upcoming by its real `date`.
- `details.summary`: calm explanation of the notice.
- `details.facts`: short facts or thresholds that justify the notice.
- `details.after_action`: what changes after the primary action.
- `details.tracking`: what the home will continue watching.
- `details.timeline`: optional concise timeline entries when history matters.

When details are missing, the UI may fall back to the notice narrative, due
metadata, group, and existing actions. Fallbacks are acceptable for generic
notices, but high-frequency or confusing reminders should get bespoke details.

## Deadline and action-window model

For notices with a real due date, model two concepts separately:

- Timeline date: the actual due, expiration, review, or maintenance date. This
  drives Upcoming, sorting, and the visible `Due ...` line.
- Action window: when Trevor should start doing something. This drives Needs
  Attention, push reminders, snoozes, and completion actions.

If the action window is open and the due date is still inside the Upcoming
horizon, show the same current-cycle notice in both sections. Needs Attention
answers "what do I need to handle now?" Upcoming answers "what is coming when?"
Do not replace the due date with the reminder-open date just to make it appear
sooner.

Completion should clear the current cycle only. For recurring notices, stamp the
specific bill/month/year, tax year, document renewal window, or maintenance
cycle that was handled; do not turn off future periods. Future cycles should
continue to appear when their own due dates and action windows arrive.

## Design standards

Detail surfaces should feel like part of the calm mobile dashboard:

- mobile-first bottom sheet or focused panel
- strong title, group, and status hierarchy
- compact facts instead of dense tables
- direct actions in the sheet, not hidden in raw entity controls
- restrained colors with only meaningful severity accents
- no overlapping HA debug/history/activity content behind the sheet

If a chart is used, it should be legible at phone width, show only the series
needed for the decision, and include threshold context when a threshold caused
the notification.

## Notification Center standard

The Notification Center's `Details` action must open the custom detail sheet in
`house-notices-card`. It must not dispatch `hass-more-info` for reminder/task
items. `Open page` may navigate to the relevant dashboard, and diagnostic
entity popups may still exist elsewhere for non-task dashboard cards.

## Recent feed standard

Recent is not an action receipt log. It should help Trevor reconstruct
meaningful notices from the last couple of weeks, not list every button tap.

Hide routine action events from Recent by default, including:

- completion acknowledgements such as `Done`, `Water done`, `Mark captured`,
  `Replaced`, or similar maintenance receipts
- snoozes and notification clears
- `Opened` or `URI` actions
- low-risk inline task handling where the visible result is that the active
  notice disappears

Routine actions may still be recorded in `sensor.house_notice_history` for
context, diagnostics, or future detail timelines. To show an action in Recent,
the action/event must opt in explicitly with metadata such as `recent: true`,
`keep_recent: true`, or `history: recent`, and the reason should be audit,
safety, money movement, access/security, or another user-visible consequence
that is genuinely worth seeing later.
