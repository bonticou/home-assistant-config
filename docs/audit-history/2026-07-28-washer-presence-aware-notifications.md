# Washer Presence-Aware Notifications

## Symptom And Goal

Routine washer completion and unattended-laundry notifications were reaching
Trevor while he was away from home, when he could not physically move the
laundry. ThinQ machine-error notices had the same actionability problem. Water
leak alerts remain safety notifications and must not be presence-gated.

## Relevant Prior Context

- The durable washer notification system was added and deployed on 2026-07-21.
- `device_tracker.tk_iphone_16_pro` is the repository's established source for
  Trevor's home/away state.
- Notification timing and idempotency follow
  `docs/notification-reliability-patterns.md`.
- The Flo washer-area leak alert is independent of ThinQ completion and machine
  error handling.

## Changes Made

- Every official ThinQ completion event is recorded even when Trevor is away.
- A routine completion push sends immediately only when Trevor is `home`.
- An unnotified completion is delivered after Trevor has been home for five
  minutes, with language that explains the cycle finished while he was out.
- Added a durable `washer_last_completion_notified_at` timestamp. The 45-minute
  follow-up is now measured from the first user-facing push, not the physical
  cycle completion time.
- Follow-ups and snooze expirations require Trevor to have been home for at
  least five minutes.
- ThinQ machine errors are recorded while Trevor is away and delivered after
  he has been home for five minutes. A detected timestamp preserves mirrored
  event throttling before a notification is sent.
- Added durable state for the last ThinQ error detection and error type.
- Preserved all existing Flo leak behavior without a presence condition.
- Unknown or unavailable tracker state fails closed for routine and machine
  error pushes; only an explicit `home` state permits delivery.

## Checks Run

- Ruby YAML parsing passed for `configuration.yaml`, `scripts.yaml`, and
  `automations/30-maintenance-environment.yaml`.
- A focused structure check confirmed the record-before-send scripts, explicit
  Trevor-home gates, five-minute arrival path, notification-based 45-minute
  timer, and record-before-send ThinQ error flow.
- All 167 automation IDs remained unique.
- `python3 tools/check_device_inventory_coverage.py` passed with 91 active
  control entity references represented in the inventory.
- `python3 tools/generate_recorder_inventory.py` completed; it refreshed the
  generated timestamp without changing Recorder policy.
- `git diff --check` passed.
- A local Home Assistant installation was not available for an offline Core
  config check.

## Deployment Status

Not deployed. The repository change must pass local checks and then follow
`docs/home-assistant-deploy-runbook.md` for live write, read-back, Core config
validation, reload or guarded restart, and entity verification.

## Residual Risks And Next Follow-Ups

- Observe an away completion followed by a real arrival to verify the five-
  minute deferred notice and its wording.
- Verify the 45-minute follow-up starts from the deferred notice timestamp.
- Confirm that a ThinQ machine error is deferred while away and delivered on
  arrival, while a Flo leak alert remains immediate.
- The washer cannot determine whether another person unloaded it while Trevor
  was away; the existing `Done` action remains the durable acknowledgement.
