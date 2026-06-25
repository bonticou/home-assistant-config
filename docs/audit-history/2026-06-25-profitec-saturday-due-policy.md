# Profitec Saturday Due Policy

## Symptom And Impact

Cafiza became due on a weekday. Trevor clarified that Profitec GO water
backflush and Cafiza maintenance should not first become due Monday-Friday, and
that a Sunday due date should be pulled forward to Saturday so there is more
weekend time to handle the work.

## Relevant Prior Context

- The June 11 Profitec weekend notification fix made phone pushes weekend-first
  but deliberately left the due sensors as raw interval dates.
- Trevor's clarified policy is stricter: the visible due state itself should
  open on a weekend, not merely the push notification.
- Weekday reminders remain acceptable only after a weekend-originated due cycle
  is still open because it was snoozed, ignored, missed while away, or otherwise
  not handled.

## Evidence Collected

- `binary_sensor.espresso_water_backflush_due` used `last_water_backflush + 7`
  directly.
- `binary_sensor.espresso_cafiza_clean_due` used `last_cafiza_clean + 60`
  directly.
- `sensor.espresso_maintenance_status`, the care overview, and the Notification
  Center item each had their own duplicated raw espresso date calculations.
- `automation.espresso_morning_maintenance_reminder` allowed weekday reminders
  after a snoozed weekend alert or away-weekend deferral, but not after a normal
  weekend alert was simply ignored.

## Ranked Findings

1. High confidence: raw `+7` and `+60` date math let water or Cafiza first
   become due on weekdays.
2. High confidence: Sunday should be treated as too late in the weekend and
   pulled back one day to Saturday.
3. Medium confidence: duplicated date math made the dashboard and Notification
   Center vulnerable to showing old dates even after the binary sensors changed.

## Changes Made

- Updated espresso date calculations so:
  - Monday-Friday raw interval dates roll forward to Saturday;
  - Sunday raw interval dates pull back to Saturday;
  - Saturday raw interval dates stay Saturday.
- Applied that policy to:
  - `sensor.espresso_maintenance_status` date attributes;
  - care overview `next_short` and `next_at`;
  - Notification Center espresso item dates;
  - `binary_sensor.espresso_water_backflush_due`;
  - `binary_sensor.espresso_cafiza_clean_due`.
- Updated `automation.espresso_morning_maintenance_reminder` so an open cycle
  whose due date began on a weekend may continue to send weekday reminders until
  handled.

## Checks And Live Validation

- Ruby YAML syntax parse passed for:
  - `configuration.yaml`;
  - `automations/20-climate-commute.yaml`;
  - `scripts.yaml`;
  - `dashboards/calm_mobile.yaml`;
  - this audit entry and the audit-history index.
- `git diff --check` passed for the touched files.
- `python3 tools/check_device_inventory_coverage.py` passed.
- Local date arithmetic sanity check confirmed:
  - Monday-Friday raw dates map to Saturday;
  - Saturday remains Saturday;
  - Sunday maps back to Saturday.
- Full local Home Assistant `check_config` was not available because
  `homeassistant` is not installed in this checkout.
- Live deployment not yet performed in this audit entry.

## Deployment Status

- Repository change prepared locally.

## Residual Risks And Next Follow-Ups

- Consider extracting the repeated Saturday-opening date math into a template
  helper if Home Assistant templating allows a clean local pattern without
  making the configuration harder to read.
