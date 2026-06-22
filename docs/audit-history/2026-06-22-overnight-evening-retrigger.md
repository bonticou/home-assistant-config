# Overnight Evening Retrigger

Date: 2026-06-22

## Symptom

Trevor received the overnight lights-left-on notification after the house had
already been wound down for bed. The bedroom sconces had been manually turned
off, so it was not obvious why any lights would have come back on.

## Relevant Prior Context

- `2026-06-10-overnight-lights-sweep.md` added the midnight whole-house
  physical-state safety net.
- `2026-06-12-front-stairs-cloudy-evening-threshold.md` and
  `2026-06-21-vacation-return-wynn-lighting.md` clarified that Evening and
  return-home lighting should not disturb late-night or sleeping-room behavior.

## Evidence

- Live history showed both master bedroom sconces were off by 2026-06-21
  22:49:55 EDT and did not turn back on before the alert.
- At 2026-06-22 00:08:19 EDT, `person.casey` briefly changed to `unknown`.
- At 2026-06-22 00:08:42 EDT, `person.casey` changed back to `home`.
- `automation.lights_interior_evening_mode_schedule_sync` interpreted that
  `unknown` to `home` transition as an arrival and ran
  `script.lights_evening_scene`.
- The Evening scene turned on non-exempt common lights, including family room,
  kitchen, and foyer chandelier lights.
- Home Assistant restarted or reloaded around 2026-06-22 00:26-00:28 EDT. The
  midnight reminder's startup path then saw the common lights still on and sent
  the notification at 2026-06-22 00:28 EDT.
- The 1:00 AM sweep subsequently turned the non-exempt lights off.

## Findings

1. High confidence: the notification was valid for the physical lights that were
   on at 00:28, but those lights were on because Evening was incorrectly
   re-applied.
2. High confidence: the retrigger was caused by a presence-state blip, not by
   the bedroom sconces.
3. High confidence: Evening return-home lighting should fire only for a real
   first return to an empty house, not for `unknown` to `home` tracker recovery
   while someone is already home.

## Change Made

Updated `automation.lights_interior_evening_mode_schedule_sync` so its arrival
branch only runs when the triggering person changes from `not_home` to `home`
and the other household person is not already `home`. The dusk branch is
unchanged.

## Checks

- Ruby YAML parse passed for `automations/10-lighting-security.yaml`.
- Live File Editor write/read-back succeeded for
  `automations/10-lighting-security.yaml`.
- Home Assistant config check returned `valid` with no warnings or errors.
- `automation.reload` returned HTTP 200.
- Live read-back confirmed the Evening arrival guard requires a `not_home` to
  `home` transition and another household person not already `home`.

## Residual Risks

If the house is genuinely empty but one person entity is stuck as `home`, the
arrival branch will intentionally stay quiet. That is safer than waking the
house from a tracker recovery while people are already inside.
