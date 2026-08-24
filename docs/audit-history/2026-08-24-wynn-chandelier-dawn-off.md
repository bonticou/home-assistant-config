# Wynn Chandelier Dawn Off

Date: 2026-08-24

## Symptom

Wynn's chandelier was intentionally settling to a 1 percent bedtime nightlight,
but that protected overnight state was still present in the morning.

## Relevant Prior Context

- `2026-06-12-front-stairs-cloudy-evening-threshold.md` recorded the policy
  that Wynn's chandelier is exempt from normal away and overnight cleanup
  because it may be used as a nightlight.
- `2026-07-31-wynn-daylight-light-timeout.md` covered daylight quiet-off rules
  for Wynn's room lights, but did not add a dawn release for the chandelier
  nightlight.
- The 1 AM whole-house sweep also deliberately exempts
  `light.wynn_s_room_chandelier`, so it should not be the place to solve a
  sunrise/nightlight cleanup problem.

## Evidence And Finding

High confidence: the missing piece was a morning handoff. The system had a
night policy that dims the chandelier to 1 percent after bedtime, and a whole
home overnight policy that preserves the chandelier, but no sun-aware rule that
turns off the stale 1 percent nightlight near dawn.

Medium confidence: this should target only the low nightlight brightness rather
than every chandelier-on state, so a brighter manual morning use is preserved.

## Changes Made

- Added `automation.lights_wynn_s_chandelier_dawn_nightlight_off`.
- The automation turns off `light.wynn_s_room_chandelier` only when:
  - vacation mode is off;
  - the chandelier is on;
  - the time is between 4:00 AM and 10:00 AM;
  - the sun is above the horizon or rising with elevation at least `-4`;
  - brightness is at or below `4` on the HA 0-255 scale.
- Added sunrise, sun-elevation, startup, reload, and 10-minute watchdog triggers
  so a missed transition does not leave the nightlight stuck on.
- Updated Wynn's camera quiet helper timestamp lookup to use the durable
  `input_datetime` timestamp attribute instead of parsing the display string.

## Checks And Deployment Status

- Local Ruby YAML parse passed for `automations/10-lighting-security.yaml`.
- Live File Editor write/read-back succeeded for
  `/homeassistant/automations/10-lighting-security.yaml`.
- Home Assistant config check returned `valid`.
- `automation.reload` returned HTTP 200.
- Live state confirmed
  `automation.lights_wynn_s_chandelier_dawn_nightlight_off` is `on`.

## Residual Risk

This intentionally does not turn off brighter chandelier use after dawn. If a
manual 1 percent daytime use becomes a real habit, the 10-minute watchdog could
turn that off during the morning window; that tradeoff is acceptable for now
because the current user-facing failure is the stale overnight 1 percent
nightlight.
