# Garbage Recycling Home Sticky Bar

## Symptom And Impact

Trevor wanted the garbage and recycling reminder to stay visible on the Home
tab, not only as a push notification. The bar should appear the night before
pickup, remain through the next morning until the current pickup is marked
taken out, and show a holiday-delay notice instead on evenings and mornings
where the normal pickup would otherwise be expected.

## Relevant Prior Context

- Notification changes should follow `docs/notification-reliability-patterns.md`.
- Garbage and recycling reminders already use the North Castle Zone 4 schedule,
  `sensor.garbage_recycling_next_pickup`, and
  `input_text.garbage_recycling_last_taken_out_pickup` as durable cycle state.
- `script.garbage_recycling_mark_taken_out` is the existing completion path for
  push actions.

## Evidence Collected

- `sensor.garbage_recycling_next_pickup` exposes the actual pickup date,
  scheduled Thursday, recycling stream, holiday exception, and last taken-out
  state.
- `automation.garbage_recycling_reminders` already distinguishes normal
  evening, morning, and holiday-delay notification stages.
- `dashboards/calm_mobile.yaml` Home view already uses conditional cards and
  confirmed small action buttons for important state changes.

## Ranked Findings

1. High confidence: the sticky bar should derive from the existing schedule and
   taken-out helpers so it cannot drift from the notification logic.
2. High confidence: the large bar should not directly mark the bins taken out;
   completion needs a small confirmed action.
3. Medium confidence: on holiday-delay weeks, the no-pickup bar should cover
   the usual pickup eve and usual pickup morning, then yield to the real takeout
   bar after 4:00 PM the day before the delayed pickup.

## Changes Made

- Added `sensor.garbage_recycling_home_sticky_bar` with `Quiet`,
  `Holiday notice`, and `Take out` states plus dashboard title/message/action
  metadata.
- Added a sticky Home-tab conditional card at the top of
  `dashboards/calm_mobile.yaml`.
- The card opens Notification Center when tapped and exposes a confirmed
  `Taken out` button only during real takeout windows.
- Holiday-delay notices have no completion action because they mean not to put
  bins out yet.

## Checks And Live Validation

- Local YAML parsing passed for:
  - `configuration.yaml`;
  - `dashboards/calm_mobile.yaml`.
- `git diff --check` passed for the touched files.
- `python3 tools/check_device_inventory_coverage.py` passed.
- Live File Editor deployment wrote and read back:
  - `/homeassistant/configuration.yaml`;
  - `/homeassistant/dashboards/calm_mobile.yaml`.
- Live Home Assistant config check returned valid.
- `template.reload` completed successfully after the final deploy.
- `lovelace.reload` is not available on this instance and returned 400, but the
  dashboard YAML read-back matched the repo byte-for-byte.
- Live validation showed:
  - `sensor.garbage_recycling_home_sticky_bar` exists;
  - current state is `Quiet` because pickup `2026-06-11` is already marked
    taken out;
  - next pickup is `2026-06-18`;
  - the sticky-bar attributes are quiet/future-safe:
    `title = Garbage + recycling`;
    `message = Next pickup is Thursday, June 18.`;
  - reminders remain enabled.

## Deployment Status

- Deployed live and validated on June 11, 2026.

## Residual Risks And Next Follow-Ups

- Validate on the live dashboard that the sticky position works cleanly on
  mobile Home view and does not obscure the existing commute card when both are
  active.
