# Notification Reliability Patterns

Use this playbook when creating or changing Home Assistant notifications,
alerts, reminders, commute notices, and other user-facing pushes.

## Core Rule

Important notifications must be durable, idempotent, and observable. A restored
boolean alone is not a reliable guard for "notified today" or "handled this
cycle" behavior.

## Durable State

Use helpers that encode time or cycle identity:

- `input_datetime.*_last_notified_at` for once-per-day or time-window alerts.
- `input_datetime.*_handled_at` for completion of a dated cycle.
- `input_text.*_active_cycle_id` or a derived cycle id when the same reminder
  repeats across yearly, monthly, or event-based periods.

Booleans are acceptable for dashboard display, temporary toggles, enable/disable
controls, or low-stakes UI state. They should not be the sole source of truth
for whether an important notification can fire.

## Send Flow

For a notification automation:

1. Compute the current cycle or today's date.
2. Check a timestamp/cycle helper, not only a boolean latch.
3. Refresh any data sources needed for the message.
4. Send the notification.
5. Stamp the notification timestamp or cycle only after the send action.
6. Update optional UI booleans from that durable stamp.

Avoid setting a latch before the data fetch and notification send. If the fetch
or send fails after an early latch, the user can miss the alert with no visible
reason.

## Reset And Self-Healing

Daily reset automations are convenience, not correctness. A missed reset must
not suppress future alerts.

Reset helpers should:

- run on the intended clock schedule;
- also run on Home Assistant start and `automation_reloaded` when practical;
- derive display booleans from durable timestamp/cycle helpers;
- leave the dated/cycle helper intact for auditability.

## Observability

Every meaningful alert should have enough state to answer:

- When did it last send?
- What cycle/day did it send for?
- What data source did it use?
- Was it skipped because it had already sent?
- Is the user-facing notification enabled or intentionally paused?

Prefer surfacing this in helper attributes, a status sensor, or a short audit
entry for larger systems.

## Testing

Before considering a notification change done:

- test the normal trigger path;
- test the already-notified path;
- test restart/reload behavior with the helper restored;
- test stale helper behavior from a prior day/cycle;
- verify the live entity state after deployment, not only the repo diff.

For commute and other time-sensitive alerts, run a same-day recovery test:
simulate or manually send the current notification once, then confirm the
durable timestamp prevents a duplicate.
