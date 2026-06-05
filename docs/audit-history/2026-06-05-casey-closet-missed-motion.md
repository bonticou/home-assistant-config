# Casey Closet Missed Motion

## Symptom And Impact

Trevor walked into Casey's closet and the closet light did not turn on. The
expected behavior is motion-on, then off after three quiet minutes.

## Relevant Prior Context

- On 2026-06-04, the Casey closet automation was repaired after entity drift.
- The current automation is `automation.lights_casey_s_closet_auto_off`.
- The motion trigger is `binary_sensor.casey_s_closet_motion`.
- The light is `light.master_casey_s_closet`.
- After a prior unexpected light-on report, the UniFi Protect motion sensitivity
  was lowered live from `100` to `70`. That earlier report did not prove motion
  sensitivity was the root cause.

## Evidence Collected

- `homeassistant.local` and the direct Home Assistant IP briefly refused fresh
  connections to port `8123`.
- The Home Assistant Observer on port `4357` reported Supervisor connected,
  supported, and healthy while Core HTTP was not accepting connections.
- After Home Assistant Core was reachable again, Safari showed
  `hass.connected: true`.
- Live state after recovery showed:
  - `automation.lights_casey_s_closet_auto_off`: `on`;
  - `light.master_casey_s_closet`: `off`;
  - `binary_sensor.casey_s_closet_motion`: `off`;
  - `switch.casey_s_closet_motion_detection`: `on`;
  - `sensor.casey_s_closet_battery`: `94`;
  - `number.casey_s_closet_motion_sensitivity`: `70`.
- The automation `last_triggered` timestamp was still from the prior evening,
  so the reported walk-in did not trigger the automation.
- The last 90 minutes of history showed the closet motion sensor stayed `off`
  and did not report an `on` event during the reported walk-in.

## Ranked Findings

1. High confidence: the automation did not fail after receiving motion; HA did
   not receive a closet motion-on event.
2. High confidence: Home Assistant Core had an availability problem during the
   investigation window. The host and Supervisor were alive, but Core HTTP on
   `8123` was temporarily unavailable.
3. Medium-high confidence: motion sensitivity `70` was too conservative for
   reliable walk-in detection in this closet.
4. Medium confidence: the missed light may have been caused by the Core
   availability window, the motion sensitivity setting, or both.

## Changes Made

- Raised `number.casey_s_closet_motion_sensitivity` live from `70` to `90`.
- No YAML automation change was made. The existing YAML still expresses the
  desired behavior when the motion entity reports `on`.

## Checks And Live Validation

- Confirmed Home Assistant local frontend later had `hass.connected: true`.
- Confirmed the sensitivity change was accepted and live state showed `90`.
- Confirmed the automation remained enabled.
- Confirmed no fresh closet motion event had appeared immediately after the
  sensitivity change.

## Deployment Status

- No file deployment was needed.
- The UniFi Protect sensor setting was changed live through Home Assistant.

## Residual Risks And Follow-Ups

- Retest with a fresh physical walk-in after sensitivity `90` is live.
- If the sensor still misses real entries, raise sensitivity back to `100` or
  add a faster physical trigger source, such as a door/contact sensor.
- If unexplained light-ons return at `90`, inspect the light state-change
  context before lowering sensitivity again.
- During the next Core availability recurrence, capture Core/Supervisor logs
  while the Observer is healthy but port `8123` is refused or unavailable.
