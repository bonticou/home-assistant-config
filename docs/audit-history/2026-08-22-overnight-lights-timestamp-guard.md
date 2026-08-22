# Overnight Lights Timestamp Guard

Date: 2026-08-22

## Symptom And Impact

The office light remained on overnight even though the midnight lights-left-on
reminder had fired and the 1:00 AM overnight sweep should have turned off
non-exempt lights.

User impact: a normal room light was still on in the morning, defeating the
whole-house overnight safety net.

## Relevant Prior Context

- `2026-06-10-overnight-lights-sweep.md` added the midnight reminder, snooze,
  and guarded 1:00 AM auto-off.
- `2026-06-22-overnight-evening-retrigger.md` confirmed that the 1:00 AM sweep
  had previously served as the last-resort recovery path.
- The office light was added to the normal Home Assistant light inventory and is
  not exempt from the overnight sweep.

## Evidence Collected

- Live `light.office_office_main_lights` was still `on` in the morning.
- Live `sensor.overnight_lights_left_on` included the office light as a
  non-exempt target.
- The midnight reminder automation triggered at 12:00 AM and stamped
  `input_datetime.overnight_lights_last_notified_at` to `2026-08-22 00:00:05`.
- The snooze helper remained at its old reset value, so the reminder had not
  been snoozed.
- Guest override, vacation mode, active TV scene, and family-room TV media guard
  were all clear.
- The 1:00 AM auto-off trace existed and showed:
  - trigger: time at 1:00 AM;
  - condition 0, lights-left-on count, passed;
  - condition 1, midnight-notification timestamp guard, failed.

## Ranked Findings

1. **Fragile timestamp guard blocked the safety net. Confidence: high.**

   The 1:00 AM automation ran and saw lights still on, but stopped on the guard
   requiring the midnight notification helper to parse between midnight and
   1:00 AM. The helper value was a plain local datetime string; the comparison
   against `today_at()` timestamps was fragile enough to fail even though the
   visible helper state was correct.

2. **Office light inclusion was not the bug. Confidence: high.**

   The office light appeared in `sensor.overnight_lights_left_on` and was not in
   the exempt list.

3. **The 1:00 AM rule needed a watchdog, not just a narrower fix. Confidence:
   high.**

   Overnight lights should not depend on a single exact scheduler moment or a
   notification timestamp. If lights are still on after 1:00 AM, the sweep
   should retry while guards remain clear.

## Changes Made

- Removed the midnight-notification timestamp requirement from
  `automation.lights_overnight_left_on_auto_off`.
- Kept the important safety gates:
  - non-exempt lights must be on;
  - snooze must be expired;
  - `auto_off_guard` must be `clear`.
- Added an overnight operating window from 1:00 AM through 5:59 AM.
- Added watchdog triggers every 15 minutes, plus Home Assistant start and
  automation reload triggers, so the rule recovers after missed scheduler ticks
  or reloads.
- Turned off the then-current overnight target lights through the existing
  `script.lights_overnight_sweep_off`.

## Checks And Validation

- Ruby YAML parse passed for:
  - `automations/10-lighting-security.yaml`;
  - `configuration.yaml`;
  - `scripts.yaml`.
- Live File Editor/direct-ingress deployment wrote and read back
  `/homeassistant/automations/10-lighting-security.yaml` with matching SHA-256.
- Home Assistant config check returned `valid`.
- `automation.reload` returned HTTP 200.
- Live state confirmed `automation.lights_overnight_left_on_auto_off` was `on`
  after reload.

## Deployment Status

Deployed live on 2026-08-22. No Core restart was required.

## Residual Risks And Follow-Ups

- The next overnight cycle should confirm the 1:00 AM sweep or 15-minute
  watchdog clears any non-exempt lights when snooze and guards are clear.
- The current guard still intentionally preserves hosting/up-late/vacation
  behavior through the existing `auto_off_guard` and snooze paths.
