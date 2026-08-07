# Laundry Notification Miss And ThinQ Fallback

Date: 2026-08-07

## Symptom And User Impact

Trevor reported that a routine laundry-finished notification did not arrive
overnight. This is part of a concerning run of missed routine-but-essential
notifications, including irrigation starts and Ring motion/doorbell alerts.

The impact is practical reliability: completion notices are the visible prompt
to move or unload laundry, and a silent miss means the house model is not
trustworthy enough for daily routines.

## Relevant Prior Context

- `docs/notification-reliability-patterns.md` requires durable timestamps,
  cycle keys, and post-send stamps for important notifications.
- `2026-07-20-washer-cycle-notifications.md` added durable washer ThinQ
  completion and error notifications.
- `2026-07-28-washer-presence-aware-notifications.md` made washer notices
  presence-aware while still recording every ThinQ completion.
- `2026-07-29-dryer-cycle-notifications.md` added dryer completion, follow-up,
  housekeeper-window, and washer-to-dryer handoff handling.
- `2026-08-05-ring-realtime-notifications.md` found a separate routine
  notification failure where the upstream event feed stopped while the shared
  Trevor phone notification path still worked.
- `2026-08-06-irrigation-start-notification-miss.md` found stale helper state
  suppressing a real routine push.

## Evidence Collected

- The repo already uses durable washer/dryer completion helpers and records
  completion timestamps before attempting the user-facing push.
- The open Safari Home Assistant tabs all reported `hass.connected=false`,
  meaning their entity data could be stale.
- The stale entity snapshot still showed the washer ThinQ completion path had
  fired for a prior completion on 2026-08-06 in the morning:
  - `event.washer_notification` held `washing_is_complete`;
  - `automation.laundry_washer_cycle_complete_notification` had triggered;
  - `script.washer_send_completion_notification` had triggered;
  - `script.washer_send_follow_up_notification` had later triggered.
- The same stale snapshot did not show a later dryer completion after
  2026-08-04, nor a later washer completion after the 2026-08-06 morning event.
- Fresh authenticated API checks could not complete through the Nabu Casa route
  from the Mac during the audit. The redacted probe result reached DNS and TCP
  but failed during TLS with `UNEXPECTED_EOF_WHILE_READING`.
- Local/LAN probes from the Mac also timed out, so a fresh live state or
  automation trace could not be captured in this pass.

## Ranked Findings

1. **High confidence: the existing laundry notification logic has durable
   fingerprints when it fires.** The previous completion path stamped helpers
   and script timestamps, so future misses can be compared against those
   durable fields.

2. **Medium-high confidence: the reported overnight miss was not captured by
   the available stale snapshot.** If the machine really finished after that
   snapshot, HA either did not receive a fresh ThinQ completion event or the
   current HA connection was too stale/unavailable to prove it.

3. **Medium confidence: the ThinQ event feed is a single point of failure for
   completion detection.** The Ring incident showed the same architectural
   class: an upstream event feed can stop while ordinary device state still
   exists. Washer and dryer completions should not depend exclusively on event
   entities when current-status entities are also available.

4. **Medium confidence: Remote UI/TLS instability is currently blocking
   diagnosis and may also contribute to missed daily trust.** The audit could
   not collect fresh traces through the remote path even though stale frontend
   state remained visible.

## Changes Made

- Added washer completion fallback detection from
  `sensor.washer_current_status` reaching `end` for two minutes.
- Added dryer completion fallback detection from
  `sensor.dryer_current_status` reaching `end` or `wrinkle_care` for two
  minutes.
- Preserved the existing official ThinQ event triggers as the primary path.
- Preserved all existing notification content, presence gates, quiet-hour
  behavior, housekeeper-window handling, follow-up timing, mobile actions, and
  durable helper names.
- Added a 15-minute duplicate guard so a current-status fallback does not
  duplicate an official ThinQ completion event that already recorded the same
  cycle.
- Required status fallback transitions to come from a known prior state, so an
  integration restore from `unknown`/`unavailable` does not create a stale
  completion notice after restart.

## Checks

- Parsed `automations/30-maintenance-environment.yaml` with Ruby/Psych.
- Ran `python3 tools/check_device_inventory_coverage.py`; coverage passed.
- Ran the external remote health probe against the redacted Nabu Casa origin;
  it failed at TLS before reaching HA.

## Deployment Status

Prepared locally but not yet deployed at the time of this entry because fresh
Nabu Casa and LAN access from the Mac were failing. Deployment still requires:

- Home Assistant config check;
- byte-for-byte live read-back of
  `automations/30-maintenance-environment.yaml`;
- `automation.reload` or a guarded restart;
- live verification that the washer and dryer completion automations contain
  both the official ThinQ event trigger and the current-status fallback trigger.

## Residual Risks And Follow-Ups

- Observe the next real washer and dryer cycles to confirm the actual
  `current_status` finish sequence for each appliance.
- If completions are still missed after this fallback is deployed, investigate
  the shared mobile notification service and companion-app delivery path rather
  than adding more appliance-specific gates.
- Add a low-noise diagnostic surface for "last detected completion" versus
  "last notified completion" so routine notification misses are visible without
  relying on chat memory.
- Continue the broader Remote UI/Core availability work because stale tabs and
  TLS failures can block both diagnosis and daily confidence.
