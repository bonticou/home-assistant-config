# Dehumidifier Air Filter Reminder

## Symptom And Impact

Trevor wanted the same lightweight recurring reminder profile as the garden
fertilizer reminder, but on the alternate Fridays, starting Friday, June 12,
2026. The notification should say `Clean dehumidifier air filter`, support
Done and next-morning Snooze, and appear in Notification Center.

## Relevant Prior Context

- Notification changes should follow `docs/notification-reliability-patterns.md`.
- The garden fertilizer reminder established the paired every-other-Friday
  growing-season pattern.
- Notification Center should show action-window work in Needs Attention and real
  due dates in Upcoming.

## Evidence Collected

- The fertilizer reminder uses durable datetime helpers plus a cycle helper to
  avoid duplicate or missed cycle notifications.
- Existing basement humidity alerts are separate guardrails and should not own
  this maintenance reminder.

## Ranked Findings

1. High confidence: this should use its own durable helpers, not share fertilizer
   helper state.
2. High confidence: the anchor date should be Friday, June 12, 2026 so it lands
   on the off weeks from fertilizer.
3. Medium confidence: the same May 1 through October 31 growing-season guard is
   appropriate because the request was to use the same profile.

## Changes Made

- Added helpers for:
  - last dehumidifier air filter completion timestamp;
  - last notification timestamp;
  - snooze-until timestamp;
  - last notified cycle;
  - notification enablement.
- Added `sensor.dehumidifier_air_filter_status`.
- Added `binary_sensor.dehumidifier_air_filter_due`.
- Added scripts to send, mark done, snooze, and clear the dehumidifier air
  filter notification.
- Added mobile notification actions for `Done` and `Snooze`.
- Added a 7:00 AM alternate-Friday reminder automation with startup/reload
  catch-up.
- Added a Notification Center item with an air/wind cue, Upcoming visibility,
  and Needs Attention actions only when due.

## Checks And Live Validation

- Local YAML parsing passed for:
  - `configuration.yaml`;
  - `automations/30-maintenance-environment.yaml`;
  - `scripts.yaml`.

## Deployment Status

- Pending live deployment and validation.

## Residual Risks And Next Follow-Ups

- After deployment, verify the live status sensor reports the next due date as
  `2026-06-12`.
- Verify Notification Center shows the upcoming dehumidifier air filter item
  before the first due cycle.
- Verify mobile actions call the new scripts after the first reminder.
