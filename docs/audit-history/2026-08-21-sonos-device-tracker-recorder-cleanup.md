# Sonos Device-Tracker Recorder Cleanup

## Symptom And Impact

Fixed Sonos speakers were being retained as `device_tracker` history even
though their network presence is not meaningful historical data. A historical
Recorder sample identified `device_tracker.sonos_beam_master` as one of the
highest-write fixed-device trackers.

## Evidence And Scope

- Reviewed the Recorder audit history, current Recorder exclusions, device
  inventory, and the available historical Recorder sample.
- The historical sample recorded 42,050 total Sonos tracker rows over 12.491
  days. Of those, 42,003 belonged to `device_tracker.sonos_beam_master`.
- At the measured rate, the Sonos tracker family projects to approximately
  101,000 rows per 30-day Recorder window.
- Current repo references do not use Sonos `device_tracker` history for
  automations or dashboards.
- Camera trackers and camera detection/event entities are explicitly outside
  this change.

## Change Made

Added the targeted Recorder exclusion:

```yaml
- device_tracker.sonos*
```

This excludes only Sonos `device_tracker` entities. It does not exclude Sonos
`media_player` entities, their controls, or their current live state.

## Checks And Deployment

- Local YAML syntax parsing passed with Ruby/Psych.
- Recorder inventory regeneration passed and classified all 20 inventoried
  Sonos trackers as excluded by `glob:device_tracker.sonos*`.
- Device inventory coverage reached the existing concurrent lighting-edit
  boundary: `light.last_changed` and `light.state` are unresolved references
  in the separately modified lighting automation. That file was not changed or
  staged as part of this Recorder slice.
- Live `configuration.yaml` was written through File Editor and read back in a
  fresh page with exactly one matching Sonos tracker glob and its adjacent
  guardrail comments.
- Home Assistant restarted and returned with the main dashboard populated.
- Targeted `recorder.purge_entities` for the explicit 20-entity Sonos tracker
  manifest remains pending because the Codex-controlled Developer Tools action
  picker did not receive the connected Home Assistant action context. No broad
  purge or database operation was substituted.

## Residual Risk

Home Assistant will no longer retain historical connectivity/presence changes
for fixed Sonos speakers. Their current connectivity and media-player state
remain available. Home Assistant's purge action does not report a deleted-row
count; the approximately 101,000-row 30-day reduction is a projection from the
measured historical sample, not a claimed live deletion count.
