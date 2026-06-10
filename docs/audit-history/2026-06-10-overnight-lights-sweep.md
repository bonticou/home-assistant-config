# Overnight Lights Sweep

Date: 2026-06-10

## Symptom And Goal

The existing late-night lighting rule only watched exterior and garage utility
lights. The requested behavior is a whole-house overnight safety net: notify at
midnight when non-exempt lights look left on, allow a deliberate snooze when the
house is hosting or people are up late, and turn the lights off at 1:00 AM only
if the reminder was not snoozed.

The front door sconces and front stairs light should remain excluded from the
overnight sweep.

## Relevant Prior Context

- The 2026-06-08 late-night exterior lighting work added an exterior/garage
  reminder and a garage auto-off watchdog.
- The existing Guest Lighting Override is the correct hosting guard and already
  pauses parts of the lighting schedule.
- Notification reliability guidance prefers durable timestamp helpers for
  idempotency and action state.

## Changes Made

- Added durable helpers:
  - `input_datetime.overnight_lights_last_notified_at`
  - `input_datetime.overnight_lights_snooze_until`
- Added `sensor.overnight_lights_left_on`, which counts physical on lights and
  light-like switches while excluding:
  - `light.stairs_front_stairs`
  - `switch.front_foyer_sconces`
  - `switch.master_lantern`
- Added `script.lights_overnight_sweep_off`, which turns off the current
  non-exempt overnight-light target list.
- Added a midnight notification with actions:
  - `Snooze tonight`
  - `Turn off now`
- Added a 1:00 AM auto-off that only runs when:
  - the midnight notice was sent during the current overnight cycle;
  - the reminder was not snoozed;
  - Guest Lighting Override is off;
  - vacation mode is off;
  - the TV/up-late media guard is clear.
- Added a clear automation so the midnight notification disappears once the
  watched non-exempt lights are off.

## Checks

Local checks passed:

- Ruby YAML parse for `configuration.yaml`, `scripts.yaml`, and
  `automations/10-lighting-security.yaml`.
- `python3 tools/check_device_inventory_coverage.py`
- `git diff --check`

Live checks passed:

- File Editor deploy helper wrote and read back `configuration.yaml`,
  `scripts.yaml`, and `automations/10-lighting-security.yaml`.
- Home Assistant config check returned `valid` with no warnings.
- Reloaded `template`, `script`, `automation`, and `input_datetime`.
- Verified live entities:
  - `sensor.overnight_lights_left_on`
  - `input_datetime.overnight_lights_last_notified_at`
  - `input_datetime.overnight_lights_snooze_until`
  - `script.lights_overnight_sweep_off`
  - the three new overnight-light automations plus the clear automation
- Reset the two new `input_datetime` helpers to `2000-01-01 00:00:00` after
  live creation so the first 1:00 AM auto-off cannot treat a default helper
  value as a real midnight notification.

## Deployment Status

Deployed live on 2026-06-10 through the connected File Editor route. Reloads
completed without requiring a Core restart.

## Residual Risks And Follow-Ups

- The dynamic target list intentionally excludes grouped lights and uses the
  underlying physical light entities.
- Up-late protection is conservative but not omniscient. Guest Override is the
  explicit hosting guard; the midnight notification snooze is the explicit
  up-late guard; active TV mode/media also blocks the 1:00 AM sweep.
