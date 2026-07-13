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

Deployed live on 2026-07-13 through File Editor ingress.

Live validation:

- Local YAML parse passed before deploy.
- `homeassistant.check_config` service accepted the pre-restart check request.
- `/homeassistant/configuration.yaml` write/read-back matched the repo payload.
- HA restarted and returned through Remote UI.
- Remote UI root and `/calm-mobile/home` returned HTTP `200`.
- Fresh Safari frontend reconnected after reload with Core `RUNNING` and Remote
  UI `online`.
- Recorder block read-back confirmed:
  - `number` and `select` are excluded domains;
  - Sonos and UniFi Protect config-control switch globs are present;
  - the full `switch` domain is not excluded;
  - `sensor.house_notice_history` is not excluded.

Recorder cleanup:

- Ran `recorder.purge_entities` against the explicit 288-entity manifest from
  this slice with `keep_days: 0`.
- Ran HA-supported `recorder.purge` with `repack: true`.
- Ran HA-supported `recorder.purge` with `apply_filter: true` and `repack: true`.
- No raw SQLite `VACUUM` or direct database surgery was attempted.

Storage result:

| Measurement | Before | After | Change |
| --- | ---: | ---: | ---: |
| DB file bytes | `20,462,624,768` | `20,462,624,768` | `0` |
| WAL bytes | `21,494,072` | `51,298,152` | `+29,804,080` |
| SQLite freelist bytes | `7,258,091,520` | `7,586,054,144` | `+327,962,624` |
| Estimated used DB bytes | `13,204,533,248` | `12,876,570,624` | `-327,962,624` |

Plain-English result: this slice freed about `328 MB` inside SQLite and reduced
future Recorder writes by excluding 288 current-only controls. It did not return
filesystem disk space immediately: the DB file remained the same size. Total
SQLite freelist/reclaimable space after the cleanup is about `7.59 GB`.

Residual live status:

- Recorder remained recording and its thread was running.
- Recorder migration was inactive.
- Recorder backlog rose during cleanup and was still non-zero in the final
  checks, last observed at `782`. No additional DB operations should be stacked
  until it drains.

## Residual Risks

- Exact per-entity row counts are still pending because broad live DB scans
  through File Editor were too expensive.
- Excluding current-only controls should be low risk, but it removes their HA
  history from future Recorder queries.
- HA-supported repack did not shrink the DB file during the observed window.
  Direct SQLite vacuum may reclaim the `7.59 GB` freelist, but should only be
  considered as a separately planned maintenance action after backup and a quiet
  HA window.
