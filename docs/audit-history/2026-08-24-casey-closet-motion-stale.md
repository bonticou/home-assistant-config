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

- Added `automation.lights_casey_s_closet_motion_stale_recovery`.
- The recovery automation runs on startup, automation reload, and at 9:05 AM
  and 3:05 PM. During 7:00 AM to 10:00 PM, if the Casey closet motion sensor
  has not changed for at least 18 hours while motion detection is enabled, it
  cycles `switch.casey_s_closet_motion_detection` off and back on, then sends
  one lighting notification.
- The notification clears when motion is next detected.
- A first draft used `button.casey_s_closet_restart`, but live HA no longer has
  that entity. The deployed version uses the motion-detection switch that is
  present live.

## Checks And Deployment Status

- Local Ruby YAML parse passed for `configuration.yaml` and
  `automations/10-lighting-security.yaml`.
- The initial 2026-08-24 live deploy was not completed because the Nabu Casa
  Remote UI tab lost its Home Assistant session and returned to the login
  screen.
- Follow-up on 2026-08-26 used the authenticated local Home Assistant route:
  `/homeassistant/automations/10-lighting-security.yaml` was written through
  File Editor, read back byte-for-byte, Home Assistant config check returned
  `valid`, and `automation.reload` returned HTTP 200.
- Live state confirmed
  `automation.lights_casey_s_closet_motion_stale_recovery` is `on`.
- The recovery automation was manually triggered once after deploy.
- Reloading the UniFi Protect and Lutron config entries for
  `binary_sensor.casey_s_closet_motion` and `light.master_casey_s_closet`
  succeeded.
- After reload, the UniFi motion entity refreshed to `off`, battery refreshed
  to `92`, and motion detection remained `on`, but no actual motion event could
  be verified without someone physically entering the closet.
- A direct `light.turn_on` test against `light.master_casey_s_closet` did not
  produce an `on` state in Home Assistant. The Lutron config entry still
  reported `loaded`, and no duplicate/new Casey closet Lutron entity was found.

## Residual Risks And Next Follow-Ups

- After someone can physically walk into the closet, confirm that
  `binary_sensor.casey_s_closet_motion` changes to `on` and the light turns on.
- If the sensor feed remains stale after the motion-detection cycle, inspect or
  replace the UniFi motion sensor rather than further changing the lighting
  automation.
- Because a direct Lutron command did not move `light.master_casey_s_closet` to
  `on`, also physically check the Casey closet Caseta switch/load. If the
  switch responds physically but HA still cannot command it, re-pair or replace
  the Lutron device entry.
