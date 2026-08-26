# Evening Scene Stale Helper

Date: 2026-08-26

## Symptom

Evening lights had not been coming on under the normal schedule.

## Relevant Prior Context

- `2026-06-12-front-stairs-cloudy-evening-threshold.md` tuned the dark-hours
  threshold and clarified that Evening should start when the schedule is active
  and Trevor or Casey is home.
- `2026-06-22-overnight-evening-retrigger.md` blocked presence recovery blips
  from re-running Evening overnight.
- `2026-08-03-evening-mode-catchup.md` added startup, reload, and refresh
  catch-up and made the Evening script fault-tolerant.

## Evidence

- On 2026-08-26, live state showed:
  - `binary_sensor.front_stairs_schedule_active`: `on`;
  - `binary_sensor.foyer_chandelier_schedule_active`: `on`;
  - `person.bonticou`: `home`;
  - `person.casey`: `home`;
  - `input_boolean.vacation_mode`: `off`;
  - `input_boolean.interior_lights_guest_override`: `off`;
  - `input_boolean.tv_lighting_scene_hold`: `off`.
- `automation.lights_interior_evening_mode_schedule_sync` was enabled, but its
  `last_triggered` was still 2026-08-23 6:33 PM ET.
- `input_select.lighting_active_scene` had stayed `Evening` from an earlier
  cycle, so the dusk branch treated the scene as already active and refused to
  start a new Evening scene.
- The Evening script did run on 2026-08-26 at 6:51 PM ET from another path or
  manual action, and the expected common lights were on afterward.

## Finding

High confidence: the normal schedule was blocked by a stale scene helper. The
automation guard correctly avoids re-running Evening while current-day Evening
is already active, but it did not distinguish today's Evening from a previous
day's stale `input_select.lighting_active_scene` value.

## Changes Made

- Updated `automation.lights_interior_evening_mode_schedule_sync` so a stale
  `Evening` scene no longer blocks a new day.
- The automation now computes whether `script.lights_evening_scene` last ran
  after noon today:
  - startup/reload can repair stale `Evening`;
  - refresh can start Evening if the helper is stale from a prior day;
  - dusk/arrival can start Evening if the helper says `Evening` but the script
    has not run today.
- Current-day `Evening`, `TV`, and `Bedtime` protections remain intact.

## Checks And Deployment Status

- Local Ruby YAML parse passed for `automations/10-lighting-security.yaml`.
- `git diff --check` passed.
- Live File Editor write/read-back succeeded for
  `/homeassistant/automations/10-lighting-security.yaml`.
- Home Assistant config check returned `valid`.
- `automation.reload` returned HTTP 200.
- Live state confirmed
  `automation.lights_interior_evening_mode_schedule_sync` is `on`.

## Residual Risk

This fix does not explain why `input_select.lighting_active_scene` remained
`Evening` across days. If that helper continues to drift, consider adding a
separate morning scene-state cleanup after the dawn lighting release.
