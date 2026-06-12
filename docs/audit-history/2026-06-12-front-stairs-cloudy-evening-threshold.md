# Front Stairs Cloudy Evening Threshold

Date: 2026-06-12

## Symptom

At about 7:12 PM EDT, the front stairs light had not turned on by automation
even though the evening was cloudy enough to feel dark. The interior Evening
scene appeared to be active already, making the missing front stairs light more
noticeable.

## Evidence

- The front stairs schedule is controlled by
  `binary_sensor.front_stairs_schedule_active`, which turns on when the sun
  elevation is at or below `sensor.lighting_evening_on_schedule_elevation_threshold`.
- The evening threshold previously used:
  - sunny / clear night: 8 degrees;
  - partly cloudy / baseline: 10 degrees;
  - cloudy / fog: 18 degrees;
  - rainy: 28 degrees.
- A local solar-position estimate for the area put sun elevation around
  12 degrees at 7:11 PM EDT on June 12.
- If Home Assistant classified the weather as partly cloudy, clear, unknown, or
  otherwise not fully cloudy, the schedule would not have started yet.
- `script.lights_evening_scene` also depended on
  `sensor.front_stairs_schedule_brightness` before turning on the front stairs.
  That meant the Evening scene could activate other evening lights while still
  skipping the front stairs whenever the separate stairs schedule considered
  itself inactive.
- Live Home Assistant verification was not available during the incident
  because local and remote access were failing.

## Finding

Two related issues caused the confusing behavior:

1. The front stairs schedule was likely tuned too conservatively for cloudy or
   partly cloudy early-summer evenings.
2. Evening mode incorrectly treated the adaptive front-stairs schedule as a
   gate. If Evening mode is active, the front stairs should participate at a
   calm minimum brightness even if the adaptive schedule has not crossed yet.

## Change

Updated `sensor.lighting_evening_on_schedule_elevation_threshold` so evening
lighting starts earlier without changing the morning release policy:

- baseline: 10 degrees to 12 degrees;
- sunny / clear night: 8 degrees to 10 degrees;
- partly cloudy: 10 degrees to 14 degrees;
- cloudy / fog: 18 degrees to 20 degrees;
- rainy: unchanged at 28 degrees.

This affects the shared evening schedule used by the front stairs, front door
lights, and related evening-lighting surfaces.

Updated `script.lights_evening_scene` so the front stairs target is at least
10 percent during Evening mode, or higher when the adaptive schedule asks for
more. This keeps the front stairs aligned with the rest of the Evening scene.

## Checks

- Ruby YAML parse passed for `configuration.yaml`,
  `automations/10-lighting-security.yaml`, and `scripts.yaml`.
- `git diff --check` passed.
- Live File Editor write/read-back succeeded for `configuration.yaml` and
  `scripts.yaml`.
- Home Assistant config check returned `valid` with no warnings or errors.
- `template.reload` and `script.reload` both completed successfully.
- Re-ran `script.lights_evening_scene` after deploy.

## Deployment Status

Deployed live on 2026-06-12. After deploy, live state showed:

- `input_select.lighting_active_scene`: `Evening`;
- `binary_sensor.front_stairs_schedule_active`: `on`;
- `sensor.lighting_evening_on_schedule_elevation_threshold`: `14`;
- `sensor.front_stairs_schedule_brightness`: `26`;
- `light.stairs_front_stairs`: `on`.

## Residual Risk

The threshold still depends on the weather integration's coarse condition
labels. If this remains annoying, the stronger fix is a dedicated twilight
helper or a reliable outdoor illuminance signal, but no currently available
outdoor lux entity was found in the inventory.
