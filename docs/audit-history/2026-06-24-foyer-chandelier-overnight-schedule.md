# Foyer Chandelier Overnight Schedule

Date: 2026-06-24

## Symptom

Trevor found the front foyer chandelier on in the morning. The intended policy is
that the foyer chandelier may participate in the evening glow, but it should not
stay on overnight.

## Relevant Prior Context

- `2026-06-22-overnight-evening-retrigger.md` fixed a separate issue where
  presence tracker recovery could re-run the Evening scene overnight.
- `2026-06-10-overnight-lights-sweep.md` added a whole-house overnight safety
  net that does not exempt the foyer chandelier.
- `2026-06-12-front-stairs-cloudy-evening-threshold.md` intentionally keeps the
  front stairs and front door lighting on a longer dusk-to-morning schedule.

## Evidence

- The repo-defined `binary_sensor.foyer_chandelier_schedule_active` was a direct
  alias of `binary_sensor.front_stairs_schedule_active`.
- `automation.lights_foyer_chandelier_schedule_sync` used the front-stairs
  schedule as its trigger and as its active condition.
- `script.foyer_chandelier_schedule_on` sets the chandelier to 10 percent.
- The front-stairs schedule is intentionally an overnight schedule; tying the
  chandelier to it meant the chandelier could be considered scheduled all night
  and into the morning.
- Vacation-mode cleanup paths also handed the chandelier back to the front-stairs
  schedule instead of a chandelier-specific evening window.

## Findings

1. High confidence: the chandelier schedule model was wrong. The chandelier was
   coupled to the overnight front-stairs schedule even though its intended
   behavior is evening-only.
2. Medium confidence: a reload, restart, or missed bedtime hold could re-apply
   the old schedule while the front-stairs schedule was still active in the
   morning.
3. High confidence: the right fix is a chandelier-specific evening schedule that
   ends before overnight, while leaving front stairs and front door lights on
   their existing overnight schedules.

## Changes Made

- Changed `binary_sensor.foyer_chandelier_schedule_active` so it is active only
  when:
  - the front-stairs schedule is active;
  - the sun is not in the rising/morning phase;
  - it is after noon;
  - it is before the evening tail end at 11:45 PM.
- Changed `sensor.foyer_chandelier_schedule_brightness` to use the new
  chandelier-specific schedule.
- Changed `automation.lights_foyer_chandelier_schedule_sync` to trigger from the
  chandelier schedule rather than the front-stairs schedule.
- Removed the old morning-only off condition so the chandelier turns off when
  its evening schedule ends.
- On startup, if the chandelier schedule is inactive, the automation now turns
  the chandelier off and clears the bedtime hold.
- Updated vacation handoff paths to use the chandelier schedule rather than the
  front-stairs schedule.
- Updated away-security exemptions so the chandelier is exempt only during its
  own evening schedule, not during the entire front-stairs overnight schedule.

## Checks And Deployment

- Local YAML parse passed for:
  - `configuration.yaml`;
  - `scripts.yaml`;
  - `automations/10-lighting-security.yaml`;
  - `dashboards/calm_mobile.yaml`.
- `git diff --check` passed.
- Live File Editor ingress write/read-back succeeded for:
  - `/homeassistant/configuration.yaml`;
  - `/homeassistant/scripts.yaml`;
  - `/homeassistant/automations/10-lighting-security.yaml`.
- Home Assistant config check returned `valid` with no warnings or errors.

## Residual Risks

- `template.reload`, `script.reload`, and `automation.reload` calls hung from the
  Remote UI session during the incident. The live files are deployed and config
  valid, but a successful reload or Core restart is still needed to guarantee the
  running automation/template model has switched to the new behavior immediately.
- Until the runtime reloads, the old in-memory automation could still be active.
  A Core restart would load the corrected files.

## Follow-Ups

- If the reload service path keeps hanging, audit HA service-call health
  separately from this lighting logic.
