# Washer Cycle Notifications

## Symptom And Goal

The LG ThinQ washer exposed useful cycle and error telemetry in Home Assistant,
but the house had no washer-cycle notifications. The requested behavior was:

- notify when washing completes;
- remind again if the finished laundry is not acknowledged;
- send a clearer high-priority notification when the washer reports an error.

The existing Flo puck near the washer already participates in the house-wide
critical leak automation and remains the water-leak source of truth.

## Relevant Prior Context

- Notification changes follow `docs/notification-reliability-patterns.md`.
- Durable timestamps and event keys must own notification idempotency; restored
  booleans are not sufficient.
- Low-signal completion and snooze actions should remain audit history rather
  than becoming Notification Center Recent items.
- The LG ThinQ integration is cloud-push. Its official washer notification
  event types include `washing_is_complete` and `error_during_washing`.

## Evidence Collected

- The washer device exposes `event.washer_notification`,
  `event.washer_error`, `sensor.washer_cycles`, current status, remaining time,
  total time, delayed start, remote start, and power control.
- Home Assistant's official LG ThinQ event entity records the event occurrence
  timestamp as the entity state and the ThinQ code as the `event_type`
  attribute.
- This browser session reached the Home Assistant login page but did not have
  an authenticated live session, so a real cycle trace and device-specific
  error payload were not available during implementation.

## Changes Made

- Added durable helpers for the last completion, handled action, snooze,
  follow-up, error notification, event keys, and last cycle name.
- Added a washer-notification enable switch. It controls routine completion and
  follow-up pushes; error pushes remain enabled as exception alerts.
- Added a tagged `🧺 Washer finished` push with `Laundry handled` and
  `Remind me in 20 min` actions.
- Added one unattended follow-up after 45 minutes. A requested snooze replaces
  that schedule with a 20-minute reminder, and repeated snoozes remain
  supported.
- Added a sticky, high-priority `⚠️ Washer needs attention` push for the
  dedicated error event and the notification entity's
  `error_during_washing` event.
- Added a 60-second mirrored-error throttle so the two ThinQ event entities do
  not create duplicate user-facing notices for the same machine error.
- Preserved the existing washer-area Flo leak automation without duplication.

## Checks Run

- Ruby YAML parsing passed for:
  - `configuration.yaml`;
  - `scripts.yaml`;
  - `automations/30-maintenance-environment.yaml`.
- `python3 tools/check_device_inventory_coverage.py` passed.
- `tools/generate_recorder_inventory.py` completed through a Python 3.10
  `datetime.UTC` compatibility alias; the generated inventory timestamp was
  refreshed and no Recorder policy changes were produced.
- A focused structure check confirmed all washer helpers, scripts, and
  automation IDs are present and that automation IDs remain unique.
- `git diff --check` passed.
- A local Home Assistant installation was not available for an offline Core
  config check.

## Deployment Status

Partially written but not activated on 2026-07-21. After the File Editor login
was restored, `configuration.yaml` was copied into the live editor, compared
exactly with the local 420,843-character source before saving, and the editor
reported a successful save. The file's size then caused the browser-mediated
read-back route to stall, matching the repository's known large-file
fragility.

Before `scripts.yaml` or
`automations/30-maintenance-environment.yaml` could be written, Home Assistant
Core stopped accepting connections on port 8123. The host remained reachable
and the Observer continued to report Supervisor connected, supported, and
healthy. No reload or restart was requested by this deployment, no live Core
config check completed, and no push notifications were sent. The running
behavior therefore must not be treated as deployed. Do not reload or restart
from this partial file set; first restore Core access, deploy and read back the
two remaining files, and obtain a valid Core config check.

## Residual Risks And Next Follow-Ups

- Restore Home Assistant Core access, then deploy and read back `scripts.yaml`
  and `automations/30-maintenance-environment.yaml` through authenticated File
  Editor ingress.
- Reconcile the live `configuration.yaml` with the committed source and obtain
  a valid Home Assistant Core config check before any reload or restart.
- Only after a valid check, reload helpers, scripts, and automations and verify
  the resulting live entities.
- Observe one real washer cycle in Activity to confirm the exact cycle-name and
  current-status values for this model.
- Confirm the first completion push, both mobile actions, the 45-minute
  follow-up, and one simulated or real error event.
- Do not add a current-status completion fallback until the real status sequence
  is known; the official completion event is the safer initial trigger.
