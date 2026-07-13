# Recorder Config-Control Slice

## Symptom And Impact

Home Assistant still has intermittent mobile/remote availability problems and a
large Recorder database. After the first conservative Recorder cut, the next
approved slice was to remove 30-day history for current-only configuration
controls:

1. `number` device tuning entities.
2. `select` mode/config entities.
3. UniFi Protect camera configuration switches.
4. Sonos configuration switches.

The goal is to reduce future Recorder writes and prepare a targeted purge for
old low-value rows without touching durable helpers, reminders, security, water,
or physical telemetry.

## Context Reviewed

- `docs/audit-history/README.md`
- `docs/audit-history/2026-07-13-recorder-pressure-follow-up.md`
- `docs/recorder-inventory.md`
- current `recorder:` block in `configuration.yaml`

## Evidence

Before this slice:

- Recorder candidates: `1871`
- Excluded by Recorder config: `120`
- Low stateful-need candidates: `554`

The remaining low-value candidates were concentrated in:

- `number`: Sonos EQ/balance/sub levels, Ring volume, UniFi Protect camera
  thresholds, ESPHome/RATGDO tuning values, TP-Link/LG controls.
- `select`: UniFi Protect HDR/IR/recording modes, Sonos speech settings,
  thermostat display modes, Matter lock operating modes, LG operation mode.
- `switch`: Sonos listening-preference toggles and UniFi Protect detection,
  overlay, status-light, sensor, privacy, and system-sound configuration.

These are useful as current controls, but their 30-day HA state history has low
operational value. Current values remain available from the integrations.

## Changes Made

Updated `configuration.yaml` Recorder exclusions:

- Added excluded domains:
  - `number`
  - `select`
- Added targeted `switch` entity globs for:
  - UniFi Protect analytics, detection, overlay, privacy, sensor, status-light,
    and system-sound configuration controls.
  - Sonos crossfade, loudness, night sound, speech enhancement, subwoofer, and
    surround configuration controls.
- Added explicit UniFi Protect motion-config switch entities that do not match
  a safe shared glob.

Regenerated `docs/recorder-inventory.json` and
`docs/recorder-inventory.md`.

## Inventory Effect

After this slice:

- Recorder candidates: `1871` -> `1583`
- Excluded by Recorder config: `120` -> `424`
- Low stateful-need candidates: `554` -> `266`

Net newly excluded from Recorder:

- `288` entities total
- `100` `number` entities
- `32` `select` entities
- `156` targeted `switch` entities

## Guardrails

Not excluded:

- durable reminder/helper state;
- espresso last-clean, snooze, last-notified, weekend-gate helpers;
- `sensor.house_notice_history`;
- doors, locks, leaks, motion, occupancy, garage doors;
- irrigation/water safety state;
- raw physical trend sensors used for charts.

This slice changes future recording only. Disk space is not reclaimed until old
rows are purged and, if safe, the database is repacked.

## Deployment Status

Repo changes prepared locally. Live deployment, targeted purge, and post-purge
storage measurement are the next steps.

## Residual Risks

- Exact per-entity row counts are still pending because broad live DB scans
  through File Editor were too expensive.
- Excluding current-only controls should be low risk, but it removes their HA
  history from future Recorder queries.
- Purge/repack should be handled separately with explicit entity/domain scope
  and before/after storage measurement.
