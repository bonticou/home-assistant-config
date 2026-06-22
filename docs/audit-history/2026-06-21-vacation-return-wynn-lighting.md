# Vacation Return Lighting And Wynn Protection

Date: 2026-06-21

## Symptom

Trevor and Casey returned home while vacation activity lighting was active and
Wynn was asleep. Vacation lighting had turned on Wynn's room lights, and the
home did not automatically hand back to the normal lived-in evening routine.

## Relevant Prior Context

- `2026-06-12-front-stairs-cloudy-evening-threshold.md` established that
  normal lived-in, away, and overnight cleanup behavior protects Wynn's room.
- The same entry documented vacation mode as the intentional exception that may
  use Wynn's room to simulate bedtime activity.
- `script.lights_evening_scene` already excludes Wynn's lights and Mudroom
  lights from the normal Evening scene.

## Evidence

- `automation.lights_interior_evening_mode_schedule_sync` triggered on
  Trevor/Casey arrival and applied `script.lights_evening_scene`, but it did
  not guard against vacation mode still being active.
- `script.vacation_activity_apply` intentionally controls
  `light.wynn_s_room_chandelier` and `light.wynn_s_room_ceiling_lights` while
  vacation mode is active.
- `script.vacation_mode_end` already turns off Wynn's room lights and clears
  the simulated vacation activity lights.

## Findings

1. High confidence: vacation mode needed an explicit household-return handoff.
2. High confidence: the generic Evening arrival automation should not race with
   vacation shutdown.
3. High confidence: the return handoff should call the existing normal Evening
   scene after vacation mode ends, because that scene already excludes Wynn's
   room.

## Changes Made

- Added `automation.vacation_mode_end_on_household_return`:
  - triggers when `person.bonticou` or `person.casey` becomes `home`;
  - runs only while `input_boolean.vacation_mode` is on;
  - calls `script.vacation_mode_end`;
  - then applies `script.lights_evening_scene` when the existing dark/evening
    schedule is active and guest override is off.
- Added a vacation-mode-off condition to
  `automation.lights_interior_evening_mode_schedule_sync` so the generic
  arrival path cannot race with vacation shutdown.

## Checks

- Ruby YAML parse passed for `automations/10-lighting-security.yaml`.
- Live File Editor write/read-back succeeded for
  `automations/10-lighting-security.yaml`.
- Home Assistant config check returned `valid` with no warnings or errors.
- `template.reload`, `script.reload`, and `automation.reload` returned HTTP
  200.
- Live read-back confirmed the deployed automation includes the vacation-return
  handoff, `script.vacation_mode_end`, and `script.lights_evening_scene`.

## Deployment Status

Deployed live on 2026-06-21 through the remote Home Assistant route.

## Residual Risks

The handoff relies on the `person.bonticou` and `person.casey` entities
transitioning to `home`. If presence lags or misses a return event, vacation
mode will remain active until manually ended or until a later presence update
fires.

## Follow-up: Mudroom Exterior Left On

Date: 2026-06-22

### Symptom

The mudroom exterior stairs light was still on after vacation mode had ended.

### Evidence

- Live logbook showed `automation.vacation_activity_lighting_sync` turned on
  `switch.exterior_mud_room_stairs` at 2026-06-21 19:26:36 EDT when
  `sensor.vacation_activity_window` changed.
- `input_boolean.vacation_mode` was later off, with `script.vacation_mode_end`
  last triggered at 2026-06-21 21:13:40 EDT.
- The newly added household-return automation had `last_triggered: null`
  because both household person entities were already `home` before the
  automation was loaded live.
- `script.vacation_mode_end` turned off the indoor vacation lights, Wynn's
  lights, yard/deck/patio lights, and `switch.uplight`, but did not include
  `switch.exterior_mud_room_stairs`.

### Finding

High confidence: the mudroom exterior light was correctly turned on by vacation
activity lighting, but vacation shutdown did not clear it.

### Change Made

Added `switch.exterior_mud_room_stairs` to the `switch.turn_off` cleanup in
`script.vacation_mode_end` so ending vacation mode clears the only remaining
mudroom exterior path.

### Checks And Deployment

- Ruby YAML parse passed for `scripts.yaml`.
- Live File Editor write/read-back succeeded for `scripts.yaml`.
- Home Assistant config check returned `valid` with no warnings or errors.
- `script.reload` returned HTTP 200.
- Live validation saw vacation mode `off`, turned
  `switch.exterior_mud_room_stairs` off, and confirmed the switch state was
  `off` afterward.
