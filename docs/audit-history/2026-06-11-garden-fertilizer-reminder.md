# Garden Fertilizer Reminder

## Symptom And Impact

Trevor wanted a lightweight tomato-icon fertilizer notification every other
Friday at 7:00 AM during growing season. The first fertilizer application was
Friday, June 5, 2026, so the first reminder should be Friday, June 19, 2026.

## Relevant Prior Context

- Notification changes should follow `docs/notification-reliability-patterns.md`.
- Notification Center should show action-window work in Needs Attention and real
  due dates in Upcoming.
- The reminder should be push-only plus Notification Center, with no dedicated
  dashboard card.

## Evidence Collected

- Existing maintenance reminders use durable datetime helpers for sent/snoozed
  state and scripts for mobile actions.
- Notification Center is driven by `sensor.house_notice_timeline`.

## Ranked Findings

1. High confidence: a durable cycle helper is needed so a restart does not
   duplicate or skip the current fertilizer Friday.
2. High confidence: `Done` should stamp completion without moving the cadence
   off Friday.
3. Medium confidence: May 1 through October 31 is a reasonable lightweight
   growing-season guard for this first version.

## Changes Made

- Added helpers for:
  - last fertilizer done timestamp;
  - last fertilizer notification timestamp;
  - fertilizer snooze-until timestamp;
  - last notified fertilizer cycle;
  - fertilizer notification enablement.
- Added `sensor.garden_fertilizer_status`.
- Added `binary_sensor.garden_fertilizer_due`.
- Added scripts to send, mark done, snooze, and clear the fertilizer
  notification.
- Added mobile notification actions for `Done` and `Snooze`.
- Added a 7:00 AM reminder automation with startup/reload catch-up.
- Added a Notification Center item with tomato emoji, Upcoming visibility, and
  Needs Attention actions only when due.

## Checks And Live Validation

- Local YAML parsing passed for:
  - `configuration.yaml`;
  - `automations/30-maintenance-environment.yaml`;
  - `scripts.yaml`.
- `git diff --check` passed for the touched YAML files.
- `python3 tools/check_device_inventory_coverage.py` passed.
- `python3 tools/generate_device_inventory.py --config-dir . --output-dir docs`
  could not run from this checkout because the local repo does not include the
  live `.storage` registry files.
- Live File Editor deployment wrote and read back:
  - `/homeassistant/configuration.yaml`;
  - `/homeassistant/automations/30-maintenance-environment.yaml`;
  - `/homeassistant/scripts.yaml`.
- Live Home Assistant config check returned valid.
- Reloaded the affected helper, template, script, and automation domains.
- Live validation showed:
  - `input_datetime.garden_fertilizer_last_done_at` =
    `2026-06-05 07:00:00`;
  - `sensor.garden_fertilizer_status` = `Scheduled`;
  - `sensor.garden_fertilizer_status.next_due_date` = `2026-06-19`;
  - `binary_sensor.garden_fertilizer_due` = `off`;
  - fertilizer scripts are loaded;
  - fertilizer automations are loaded and enabled;
  - Notification Center includes an upcoming `🍅 Fertilizer time` item for
    `2026-06-19`.
- No fertilizer push was sent during deployment; the first due cycle is still
  Friday, June 19, 2026 at 7:00 AM.

## Deployment Status

- Deployed live and validated on June 11, 2026.

## Residual Risks And Next Follow-Ups

- Verify mobile actions call the new scripts after the first reminder.
