# Garage Transient-Open Notification Grace

## Symptom And Impact

When exactly one household member was away, opening either garage door caused
an immediate push. A brief open-and-close while the person at home was working
outside therefore produced a false "left open" alert before there was evidence
that the door had actually been left open.

## Relevant Context

- `Garage — Open While Person Away` owns the one-person-away reminder.
- Both-away garage openings are handled separately by the away-security
  automation.
- Overnight openings without a recent arrival have a separate immediate
  security alert.
- Garage notifications use stable tags and are cleared when the condition
  resolves.

## Evidence And Findings

1. High confidence: the one-person-away automation triggered as soon as
   `binary_sensor.away_security_garage_door_open` changed to `on`; it had no
   duration guard.
2. High confidence: a Home Assistant state trigger with a `for` duration is
   canceled naturally when the sensor returns to `off`, which matches the
   desired transient-open behavior.
3. High confidence: the Casey-away title said Casey "left" the door open even
   when the garage could have been opened later by the person still home.
4. High confidence: the separate both-away and overnight automations can remain
   immediate because those are security events rather than routine
   left-open reminders.

## Changes

- Added a five-minute `for` duration to the one-person-away garage-open trigger.
- Changed the Casey-away notification title to report that the relevant door is
  still open without attributing who opened it.
- Left departure-triggered, both-away, overnight, obstruction, and 30-minute
  all-home behavior unchanged.

## Checks

- Local YAML parsing passed for `automations/10-lighting-security.yaml` and
  `scripts.yaml`.
- Targeted policy checks confirmed the five-minute duration, the neutral title,
  and removal of the old blame wording.
- Device-inventory coverage passed for all 91 active control references.
- `git diff --check` passed.
- Live File Editor write/read-back matched the generated SHA-256 payloads for
  `automations.yaml`, `automations/10-lighting-security.yaml`, and
  `scripts.yaml`.
- Home Assistant configuration validation returned `valid` with no errors or
  warnings.
- Direct follow-up `script.reload` and `automation.reload` requests both
  completed with HTTP 200 after the deploy helper's shorter reload waits timed
  out.
- The live automation config API confirmed the five-minute `garage_opened`
  duration. The live script config confirmed the neutral title, and the
  automation entity was enabled.

## Deployment Status

Deployed live on 2026-07-29 through the authenticated File Editor ingress
route, with matching read-back hashes, valid config, successful targeted
reloads, and live config verification.

## Residual Risks And Follow-Up

- Presence transitions can still trigger the one-person-away check immediately
  when someone actually departs and a garage door is already open. That is
  intentional because it is direct departure evidence rather than a brief door
  opening by someone known to be home.
- The shared open sensor cannot identify who physically operated the door, so
  reminder language should continue to describe state rather than assign blame.
