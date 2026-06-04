# Garden Decommission

Date: 2026-06-04

## Symptom And Goal

The crop-garden workflow was no longer used and had become unnecessary Home
Assistant surface area. The goal was to remove the whole Garden concept from
the active home model while preserving irrigation, Hydrawise, watering zones,
water safety alerts, and non-Garden notifications.

## Backup

Created an off-device Mac zip backup before deletion:

- `/Users/trevor.kiviat/Desktop/house/backups/ha-config-garden-removal-2026-06-04.zip`
- Size: 24 MB
- Integrity: `zip -T` passed
- Excluded `.git`, `.tmp`, caches, logs, databases, tarballs, and generated
  scratch files

No HA Supervisor backup was created for this work, per the requested approach.

## Changes Made

- Removed the Garden dashboard view from `dashboards/calm_mobile.yaml`.
- Removed Garden helpers, template sensors, binary sensors, notices, and AI
  Garden brief state from `configuration.yaml`.
- Removed Garden scripts from `scripts.yaml`.
- Removed Garden automations from the climate/commute automation file.
- Renamed `automations/20-climate-garden-commute.yaml` to
  `automations/20-climate-commute.yaml`.
- Neutralized the old live HA automation include path
  `/homeassistant/automations/20-climate-garden-commute.yaml` to `[]` so HA's
  include-dir loader could not keep running stale Garden automations.
- Deleted `docs/garden-workflow.md`.
- Updated deploy/documentation references to the new automation filename.
- Updated `tools/prepare_ha_utf8_browser_deploy.js` default deploy file list.

Primary config-removal commit:

- `cdc7fc7 Remove unused Garden workflow`

## Live Cleanup

The first config deploy and restart proved that YAML removal alone was not the
whole cleanup. HA still showed 130 Garden entities as unavailable restored
states. The follow-up cleanup was:

- Explicit `recorder.purge_entities` for 130 Garden/AI Garden entity IDs.
- The purge manifest was checked to exclude irrigation, Hydrawise, watering
  zone, and sprinkler-like entity IDs.
- Sample post-purge history checks returned zero rows for:
  - `automation.garden_afternoon_weather_protection_notification`
  - `input_boolean.garden_tracking_enabled`
  - `sensor.garden_workflow_status`
- Removed the same 130 Garden entity registry entries through HA's entity
  registry websocket API.

Final live verification:

- Live state Garden/AI Garden count: `0`
- Live entity registry Garden/AI Garden count: `0`
- Fresh registry export Garden/AI Garden count: `0`
- Fresh live state export Garden/AI Garden count: `0`

## Recorder And Storage Impact

Logical Recorder inventory impact:

- Before cleanup, Recorder inventory entity count: `2345`
- After cleanup, Recorder inventory entity count: `2195`
- Before cleanup, recorded candidates: `1944`
- After cleanup, recorded candidates: `1794`
- Garden purge manifest size: `130` entities

Physical HA disk-space impact could not be measured from the available route:

- Supervisor host storage APIs returned `401` from the frontend route.
- The visible storage-like sensors were camera/NVR, phone, gateway, or network
  device storage metrics, not HA host Recorder DB size.
- The Recorder inventory generator did not have a copied DB available, so
  `db.available` remained `false`.

Important interpretation: `recorder.purge_entities` removes matching history
rows, but SQLite files often do not physically shrink until a repack/vacuum
operation. No database repack/vacuum was performed in this slice.

## Checks

Local checks passed:

- YAML parse for:
  - `configuration.yaml`
  - `scripts.yaml`
  - `automations.yaml`
  - `automations/00-water-irrigation.yaml`
  - `automations/10-lighting-security.yaml`
  - `automations/20-climate-commute.yaml`
  - `automations/30-maintenance-environment.yaml`
  - `dashboards/calm_mobile.yaml`
- `python3 tools/check_device_inventory_coverage.py`
- `git diff --check`
- Active config and regenerated inventories contain no Garden, AI Garden, crop,
  or seedling references.

Live checks passed:

- File Editor read-back confirmed live YAML files contained no Garden text.
- HA config check passed before restart.
- Nabu Casa route reconnected after the usual post-restart delay.
- Final live state and registry exports contained no Garden entries.

## Residual Notes

- Remote UI flapped after restarts, matching the previously documented Nabu
  Casa reconnect behavior.
- The exact physical disk-space recovery remains unknown until HA host disk/DB
  size is measured directly or a safe DB copy/repack audit is run.
- Irrigation, Hydrawise, watering zones, pressure/flow alerts, and water-safety
  entities were explicitly excluded from the purge and were not removed.
