# Tesla Overnight Plug Reminder

Date: 2026-08-03

## Symptom And Impact

Trevor wants an after-10 PM reminder when he is home, the Tesla is home, and
the Tesla is not plugged into the charger. The reminder should include the
current battery percentage so the decision is easy at a glance.

## Relevant Prior Context

- `2026-08-02-unexpected-core-restart-during-tesla-setup.md`

That entry records that Tesla Fleet setup was interrupted before Home Assistant
finished credential storage.

## Evidence Collected

- Live Home Assistant state shows `person.bonticou` is home and backed by
  Trevor's iPhone tracker.
- Live entity and device registry checks show only the UniFi-discovered
  `device_tracker.tesla` and disabled UniFi link-speed telemetry for the Tesla.
- The current Tesla tracker is `unavailable`; no Tesla Fleet battery-level or
  charge-cable entity is active yet.
- Home Assistant's Tesla Fleet documentation lists vehicle `Battery level` and
  `Charge cable` entities, which are the two facts needed for this reminder.

## Ranked Findings

1. **High confidence:** the requested rule cannot honestly send the requested
   battery-aware notification until Tesla Fleet vehicle telemetry is available
   in Home Assistant.
2. **High confidence:** UniFi presence alone is not enough for this rule because
   it cannot provide battery percentage or charger plug state, and the Tesla
   Wi-Fi tracker may be unavailable when the car is asleep.
3. **Medium confidence:** once Tesla Fleet is completed, the default entity names
   are likely to include Tesla, Battery level, and Charge cable; the automation
   uses conservative discovery around those names and refuses to notify without
   both facts.

## Changes Made

- Added `input_datetime.tesla_charge_reminder_last_notified_at` as the durable
  once-per-overnight-cycle send guard.
- Added `input_datetime.tesla_charge_reminder_setup_issue_last_notified_at` so
  missing Tesla telemetry produces one explicit setup-blocked notice per
  overnight cycle instead of failing silently.
- Added `input_boolean.tesla_charge_reminder_notifications_enabled` for a clean
  enable/disable control.
- Added `Vehicle — Tesla Overnight Plug Reminder` with time, reload, startup,
  Trevor-home, and Tesla-home triggers.
- The automation only sends when:
  - Trevor is home;
  - the local time is between 10 PM and 2 AM;
  - a Tesla-named tracker is home;
  - a Tesla Battery level sensor is available;
  - a Tesla Charge cable binary sensor is explicitly `off`;
  - the current overnight cycle has not already been notified.
- If Trevor is home after 10 PM but Tesla battery/charge-cable telemetry is
  missing, the automation sends `Tesla reminder needs setup` once for that
  overnight cycle instead of silently doing nothing.

## Checks And Deployment Status

- Local Ruby YAML parsing passed for `configuration.yaml` and
  `automations/30-maintenance-environment.yaml`.
- `python3 tools/check_device_inventory_coverage.py` passed.
- Live File Editor ingress deployment wrote and read back:
  - `/homeassistant/configuration.yaml`;
  - `/homeassistant/automations/30-maintenance-environment.yaml`.
- Home Assistant config check returned `valid` with no warnings.
- `input_datetime.reload`, `input_boolean.reload`, and `automation.reload`
  returned HTTP 200.
- Live state confirmed the new helper entities and automation are loaded.
- Live template probe at 10:18 PM showed Trevor home, but no Tesla home tracker,
  no Tesla Battery level sensor, and no Tesla Charge cable binary sensor, so
  the automation correctly evaluated `would_notify: false`.
- Follow-up after the missed user-visible reminder added the setup-blocked
  fallback. A second live deployment wrote/read back `configuration.yaml` and
  `automations/30-maintenance-environment.yaml`, config check returned `valid`,
  and `input_datetime.reload` plus `automation.reload` returned HTTP 200.
- Trace `b3070167aaa32316be6a9ae4c4086962` showed the fallback branch selected
  at 10:34:25 PM, called `script.notify_trevor_phone` with title
  `Tesla reminder needs setup`, and stamped
  `input_datetime.tesla_charge_reminder_setup_issue_last_notified_at` to
  `2026-08-03 22:34:25`.
- Child script trace `9e0df0358bc7577c7e0a0b6430d56f19` finished cleanly and
  called `notify.mobile_app_tk_iphone_16_pro` with the same Tesla setup message.

Deployed live on 2026-08-03 through the authenticated File Editor ingress path.

## Residual Risks And Follow-Ups

- Complete Tesla Fleet setup so Home Assistant has real battery and charge-cable
  telemetry.
- After Tesla Fleet entities appear, verify the automation discovers the exact
  entities; if the vehicle display name does not include Tesla, replace the
  discovery template with explicit entity IDs.
