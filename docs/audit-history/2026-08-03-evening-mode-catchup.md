# Evening Mode Catch-Up And Scene Resilience

Date: 2026-08-03

## Symptom

The normal Evening lighting did not appear to fully apply on the evening of
August 3, 2026. The house was dark enough for Evening mode, but key lights such
as the Kitchen Island and other common-area lights stayed off.

## Relevant Prior Context

- `2026-06-12-front-stairs-cloudy-evening-threshold.md` moved the evening
  threshold earlier for cloudy or dim evenings and made the front stairs part of
  Evening mode.
- `2026-06-22-overnight-evening-retrigger.md` prevented tracker recovery from
  re-running Evening mode while people were already home overnight.
- `2026-06-24-foyer-chandelier-overnight-schedule.md` separated the chandelier
  evening window from the longer front-stairs overnight schedule.

## Evidence

- `binary_sensor.front_stairs_schedule_active` turned on at 7:08:26 PM EDT.
- `automation.lights_interior_evening_mode_schedule_sync` triggered from that
  state change and started `script.lights_evening_scene`.
- `script.lights_evening_scene` set `input_select.lighting_active_scene` to
  `Evening`.
- Family Room main lights came on after the script started, but the Kitchen
  Island and later common-light groups did not change state.
- Home Assistant Core restarted at about 7:27 PM EDT and again around
  8:36 PM EDT. After restart, `input_select.lighting_active_scene` returned to
  `None`.
- Supervisor logs showed the later Core restarts. The retained Core log did not
  include a precise script-service exception for the 7:08 PM partial scene.

## Findings

1. High confidence: Evening mode did trigger, so the failure was not the dusk
   trigger itself.
2. High confidence: the Evening scene was too sequential. A slow or failed
   Lutron service call could prevent later scene steps such as Kitchen Island
   from running.
3. High confidence: the interior Evening automation had no startup/reload
   catch-up path. After Core restarted and the helper returned to `None`, the
   already-active evening window did not automatically reassert the scene.
4. Medium confidence: the weather-derived threshold was not the primary failure
   tonight, but the `clear-night` weather state may still understate subjective
   darkness on some evenings.

## Changes Made

- Changed `script.lights_evening_scene` from `single` to `restart` mode so a
  legitimate retry can reassert the scene.
- Split Evening scene light service calls into independent parallel chunks with
  `continue_on_error`, so Family Room, Kitchen Island, common areas, kitchen
  task lights, Mudroom interior lights, and Front Stairs no longer depend on one
  earlier service call succeeding.
- Added startup, automation-reload, and five-minute refresh triggers to
  `automation.lights_interior_evening_mode_schedule_sync`.
- Restricted catch-up to the existing evening-only chandelier schedule window,
  preventing the longer front-stairs overnight schedule from waking the house
  later at night.
- Kept TV, Bedtime, and All Off protected from periodic catch-up. Refresh only
  retries an already-started Evening scene for a short recent window when key
  expected lights are still missing.

## Checks

- Local Ruby YAML parse passed for `configuration.yaml`, `scripts.yaml`, and
  `automations/10-lighting-security.yaml`.
- `python3 tools/check_device_inventory_coverage.py` passed.
- `git diff --check` passed.
- Live File Editor ingress deployment wrote and read back:
  - `/homeassistant/scripts.yaml`;
  - `/homeassistant/automations/10-lighting-security.yaml`.
- Home Assistant config check returned `valid` with no warnings or errors.
- Targeted local API reloads returned HTTP 200 for `script.reload` and
  `automation.reload`.
- Live validation confirmed the newly loaded catch-up path ran and re-applied
  Evening mode. `input_select.lighting_active_scene` was `Evening`, Kitchen
  Island was on at full brightness, and Front Foyer Ceiling / Kitchen Main were
  on.

## Deployment Status

Deployed live on 2026-08-03 through the authenticated File Editor ingress path.
Initial reload calls over the Nabu path failed during a transient HA/Nabu stall,
but the local API recovered and targeted reloads completed successfully.

## Residual Risks

- The exact Lutron service failure that stopped the 7:08 PM scene was not
  present in the retained Core log. The change therefore hardens the scene
  against the observed failure shape rather than naming a single device fault.
- If a user manually changes individual lights very soon after Evening mode
  starts while the helper still says `Evening`, the short recent retry window
  could reassert the scene once. TV, Bedtime, and All Off remain protected.
