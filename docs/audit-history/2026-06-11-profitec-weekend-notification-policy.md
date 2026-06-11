# Profitec GO Weekend Notification Policy

## Symptom And Impact

Trevor received a Profitec GO cleaning notification on Thursday, June 11, 2026.
That is a weekday, and the espresso cleaning workflow is intended to be a
weekend chore unless a prior weekend alert was snoozed or a due weekend was
missed because Trevor was away.

## Relevant Prior Context

- `docs/notification-reliability-patterns.md` requires durable timestamp or
  cycle helpers for important notification idempotency.
- The espresso due sensors should continue to represent maintenance reality:
  water backflush and Cafiza cleaning can become due on any date.
- The notification policy is stricter than the due policy:
  first reminders should be weekend-first and home-only.

## Evidence Collected

- `automation.espresso_morning_maintenance_reminder` was gated by:
  - espresso maintenance enabled;
  - `binary_sensor.espresso_maintenance_due`;
  - Trevor home;
  - a morning or coffee-window catch-up trigger;
  - not already notified today.
- It did not check whether today was a weekend.
- It had no durable memory of a due weekend being reached while Trevor was away.
- `script.espresso_send_maintenance_notification` stamps
  `input_datetime.espresso_maintenance_last_notified_at` after the push send,
  which remains the correct idempotency pattern.

## Ranked Findings

1. High confidence: the Thursday notification was allowed because the automation
   treated `espresso_maintenance_due` as sufficient for a weekday push.
2. High confidence: the due sensors should remain unchanged so dashboards still
   show the true maintenance state.
3. High confidence: the notification automation needs a separate weekend-first
   policy gate.

## Changes Made

- Added `input_datetime.espresso_maintenance_weekend_gate_at`.
- Updated `sensor.espresso_maintenance_status` attributes to expose the weekend
  gate timestamp and notification policy.
- Updated `automation.espresso_morning_maintenance_reminder` so a notification
  can send only when:
  - it is Saturday or Sunday;
  - or the current cycle was already introduced by a weekend alert and then
    snoozed;
  - or a due weekend opportunity was recorded while Trevor was away.
- The automation records the weekend gate while maintenance is due on a weekend
  even before checking whether Trevor is home, so away-weekend deferrals can
  turn into weekday nudges later.
- The existing home check remains in place, so weekend alerts still do not send
  while Trevor is away.

## Checks And Live Validation

- Local YAML parsing passed for:
  - `configuration.yaml`;
  - `automations/20-climate-commute.yaml`;
  - `scripts.yaml`.
- `git diff --check` passed for the touched YAML files.
- `python3 tools/check_device_inventory_coverage.py` passed.
- `python3 tools/generate_device_inventory.py --config-dir . --output-dir docs`
  could not run from this checkout because the local repo does not include the
  live `.storage` registry files.

## Deployment Status

- Pending live deployment and validation.

## Residual Risks And Next Follow-Ups

- After deployment, reload input datetime helpers, templates, scripts, and
  automations, then verify `input_datetime.espresso_maintenance_weekend_gate_at`
  exists live.
- Clear the invalid Thursday Profitec GO notification tag.
- If the weekend gate helper is not created by reload, schedule or perform a
  Home Assistant restart before Saturday morning.
