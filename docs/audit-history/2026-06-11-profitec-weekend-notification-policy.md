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
- Gave the weekend gate helper an explicit neutral initial value of
  `1970-01-01 00:00:00`.
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
- The automation only treats the weekend gate as valid if the gate timestamp is
  itself a Saturday or Sunday, so a default/restored weekday helper value cannot
  unlock weekday notifications.
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
- Deployed `configuration.yaml` and `automations/20-climate-commute.yaml`
  through the Nabu Casa Remote UI File Editor ingress.
- File Editor write/read-back succeeded for both files.
- Home Assistant config check returned `valid` with no warnings.
- Live frontend API verification showed:
  - `input_datetime.espresso_maintenance_weekend_gate_at` exists and was reset
    to `1970-01-01 00:00:00`;
  - `sensor.espresso_maintenance_status` exposes the weekend-first notification
    policy;
  - `automation.espresso_morning_maintenance_reminder` includes both the
    `weekend_gate_current_cycle` policy gate and the explicit weekend-day check.
- Cleared the invalid Thursday Profitec GO notification tag.
- Follow-up live reset after Trevor clarified not to wipe maintenance history:
  - preserved actual maintenance timestamps:
    - `input_datetime.espresso_last_water_backflush` =
      `2026-06-04 10:22:34`;
    - `input_datetime.espresso_last_cafiza_clean` =
      `2026-04-25 07:00:00`;
  - reset only notification-policy helper state:
    - `input_datetime.espresso_maintenance_snooze_until` =
      `1970-01-01 00:00:00`;
    - `input_datetime.espresso_maintenance_last_notified_at` =
      `1970-01-01 00:00:00`;
    - `input_datetime.espresso_maintenance_weekend_gate_at` =
      `1970-01-01 00:00:00`;
  - live status remained `Water due`, which is correct maintenance state, but
    there was no remaining notification helper evidence that would justify a
    weekday push before a valid weekend/home window.

## Deployment Status

- Deployed live and verified on 2026-06-11.

## Residual Risks And Next Follow-Ups

- The helper-domain reload path behaved inconsistently through the browser
  service-call promise path, but the final frontend API verification confirmed
  the helper exists and the automation config is loaded.
- Watch the next Saturday morning due cycle to confirm the first valid reminder
  arrives only when Trevor is home.
