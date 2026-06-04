# Casey Closet Unexpected Light-On

## Symptom And Impact

Casey's closet light turned on even though nobody had been in the closet. The
reported event was in the prior one to two hours, and the light later turned
off on its own.

## Relevant Prior Context

- Earlier on 2026-06-04, the Casey closet automation was repaired after the
  UniFi Protect motion entity changed.
- The current automation uses `binary_sensor.casey_s_closet_motion`, turns on
  `light.master_casey_s_closet` when motion is detected, and turns it off after
  three quiet minutes.
- The device inventory already records the Casey's Closet UniFi Protect device
  and its motion sensitivity control.

## Evidence Collected

- Live HA state showed the motion sensor was `off`, the closet light was `off`,
  and the automation was enabled when checked.
- Live history for the prior two hours showed the original unexplained light-on
  happened around 5:22:58pm ET, before the first related closet motion event.
- The most relevant later activity was around 5:28pm ET:
  - motion turned on at about 5:28:11pm ET;
  - the closet light turned off at about 5:28:16pm ET;
  - the closet light turned on again at about 5:28:38pm ET;
  - motion cleared at about 5:28:41pm ET;
  - the closet light turned off at about 5:31:41pm ET.
- The motion sensitivity entity was set to `100`, the maximum value, before the
  calibration change.

## Ranked Findings

1. High confidence: the original mystery light-on was not caused by the closet
   motion-on automation, because the light was already on before the first
   related motion event in history.
2. Medium confidence: the original light-on likely came from a manual control,
   UI action, scene, service call, or device-level state change. The exact
   context was not confirmed during the live check.
3. High confidence: the quiet timer worked; after motion cleared, the light shut
   off after the expected three-minute window.
4. Medium confidence: sensitivity `100` was still aggressive for this closet,
   but it was not proven to be the root cause of the original light-on.
5. Lower confidence: the sensor may need additional calibration if phantom
   motion events continue after lowering sensitivity.

## Changes Made

- Set `number.casey_s_closet_motion_sensitivity` from `100` to `70` live in
  Home Assistant as a conservative calibration change.
- No YAML behavior change was required; the repo automation already references
  `binary_sensor.casey_s_closet_motion`.

## Checks And Live Validation

- Confirmed live HA accepted the sensitivity change and reflected state `70`.
- Confirmed live motion state remained `off` and closet light remained `off`
  after the change.
- Parsed `automations/10-lighting-security.yaml` successfully with Ruby YAML.
- Ran `python3 tools/check_device_inventory_coverage.py` successfully:
  inventory coverage ok for 72 active control entity references.
- Ran `git diff --check` against the relevant automation and inventory files.

## Deployment Status

- No file deployment was needed for this incident.
- The live UniFi Protect motion sensitivity setting was updated directly through
  Home Assistant.

## Residual Risks And Follow-Ups

- If the closet misses real entry motion, raise sensitivity slightly from `70`.
- If unexplained light-ons continue without preceding motion, inspect the light
  state-change context and nearby scene/script/service calls before changing the
  motion automation again.
- If phantom motion events continue, lower sensitivity again or add a second
  confirmation signal before turning on the light.
- Keep the current three-minute quiet-off template; it handled the observed
  already-on case correctly.
