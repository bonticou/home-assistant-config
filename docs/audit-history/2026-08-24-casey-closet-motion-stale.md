# Casey Closet Motion Stale

Date: 2026-08-24

## Symptom

Casey's closet light stopped automatically turning on during testing over the
prior day or so.

## Relevant Prior Context

- `2026-06-11-casey-closet-stale-on.md` added the twelve-minute hard cap and
  watchdog for stale-on behavior.
- `2026-06-25-casey-closet-lutron-bridge-disconnect.md` showed a previous
  failure where the motion event arrived and the automation matched, but Lutron
  returned `BridgeDisconnectedError` during the light service call.

## Evidence Collected

- Live Nabu access initially showed:
  - `automation.lights_casey_s_closet_auto_off`: `on`;
  - `light.master_casey_s_closet`: available and `off`;
  - Lutron hub tracker: `home`;
  - `switch.casey_s_closet_motion_detection`: `on`;
  - `sensor.casey_s_closet_battery`: `92`;
  - `binary_sensor.casey_s_closet_motion`: `off`, last changed
    2026-08-23 10:18 AM ET.
- History for the prior three days showed repeated successful
  `binary_sensor.casey_s_closet_motion` events through 2026-08-22 8:40 AM ET,
  with corresponding closet light on/off behavior.
- No motion `on` events were recorded after 2026-08-22 8:40 AM ET in the
  history window.
- Several companion UniFi sensor entities were unavailable, while battery and
  the motion-detection switch remained available.
- The UniFi Protect device registry identified the device as a Ubiquiti
  `USL Motion` sensor named Casey's Closet.
- A live `button.press` against `button.casey_s_closet_restart` was accepted at
  2026-08-24 9:06 AM ET. The Nabu session then fell back to the Home Assistant
  login screen before post-restart verification could complete.

## Ranked Findings

1. High confidence: the current missed auto-on behavior is caused by the UniFi
   motion feed not producing motion events, not by the Casey closet automation
   being disabled or ignoring valid triggers.
2. High confidence: the Lutron command path was available during the live
   snapshot, so the June bridge-disconnect failure mode was not the immediate
   evidence this time.
3. Medium confidence: restarting the UniFi sensor is the right first recovery
   step, but live verification was blocked by the Remote UI session returning
   to login.

## Changes Made

- Added `input_datetime.casey_closet_motion_last_recovery_at` as a durable
  throttle.
- Added `automation.lights_casey_s_closet_motion_stale_recovery`.
- The recovery automation runs on startup, automation reload, and every two
  hours. During 7:00 AM to 10:00 PM, if the Casey closet motion sensor has not
  changed for at least 18 hours while motion detection is enabled, it presses
  the sensor restart button, stamps the recovery helper, and sends one lighting
  notification.
- The notification clears when motion is next detected.

## Checks And Deployment Status

- Local Ruby YAML parse passed for `configuration.yaml` and
  `automations/10-lighting-security.yaml`.
- Live deploy was not completed during this pass because the Nabu Casa Remote
  UI tab lost its Home Assistant session and returned to the login screen.

## Residual Risks And Next Follow-Ups

- After Remote UI auth is restored, deploy `configuration.yaml` and
  `automations/10-lighting-security.yaml`, run HA config check, reload
  automations, and verify the new helper and automation are loaded.
- After someone can physically walk into the closet, confirm that
  `binary_sensor.casey_s_closet_motion` changes to `on` and the light turns on.
- If the sensor feed remains stale after restart, inspect or replace the UniFi
  motion sensor rather than further changing the lighting automation.
