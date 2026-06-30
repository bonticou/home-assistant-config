# Hunter Flow Irrigation Build

## Symptom And Goal

Hunter Flow was installed as a dedicated irrigation meter, so the irrigation
stack needed to stop treating household Flo usage as irrigation evidence and
start using Hunter-derived water data for notifications, history, baselines, and
the irrigation dashboard.

The target posture was:

- Hydrawise remains schedule and zone truth.
- Hunter Flow becomes the irrigation measurement layer.
- Moen Flo remains household water plus shared-well pressure context.
- Routine irrigation start/finish pushes remain enabled.
- Zone flow-baseline alerts launch in learning-first mode.

## Prior Context

- `2026-06-09-irrigation-flo-topology.md` corrected the architecture after
  Flo-derived irrigation memory proved unreliable for zone evidence.
- `2026-06-29-irrigation-hunter-flow-review.md` identified the Hunter Flow
  dashboard and notification build shape, including items to remove or demote
  from the irrigation tab.

## Evidence Collected

- Live Home Assistant discovery exported states, entity registry, device
  registry, areas, floors, and config entries through the authenticated
  frontend path.
- Candidate searches covered entity ids, names, device metadata, integrations,
  units, and attributes for Hunter, Hydrawise, flow, water-use, gallons,
  meters, and sensors.
- The Hydrawise entities exposed Hunter-metered water-use totals but not a
  separate live GPM entity:
  - `sensor.45_crr_daily_total_water_use`
  - `sensor.45_crr_daily_active_water_use`
  - `sensor.45_crr_daily_inactive_water_use`
  - `binary_sensor.45_chesnut_ridge_rd_armonk_connectivity`

## Findings

1. High confidence: `sensor.45_crr_daily_total_water_use` is the best canonical
   Hunter measurement source available in HA today.
2. High confidence: direct GPM is not exposed as a raw entity, so current flow
   must be derived from valid total-water-use deltas.
3. High confidence: new dashboard and automation logic should depend on stable
   normalized irrigation entities instead of raw Hydrawise/Hunter ids.
4. Medium confidence: live registry metadata is more accurate than local config
   alone for inventory, but normalized YAML template entities will only appear
   in the live registry after restart and the next registry refresh.

## Changes Made

- Added normalized irrigation measurement entities:
  - `sensor.irrigation_flow_rate`
  - `sensor.irrigation_session_gallons`
  - `binary_sensor.irrigation_flow_meter_available`
  - `sensor.irrigation_flow_baseline_status`
- Added Hunter-flow helper state for current flow, last total, session gallons,
  zone gallons, peak flow, and minimum shared-well pressure.
- Extended irrigation history recording with `flow_source: hunter`, session and
  zone gallons, average/peak flow, and minimum pressure.
- Preserved Hunter-derived history from legacy Flo-derived purge behavior.
- Renamed user-facing "fingerprint" language to "flow baseline" while keeping
  the existing Python tool compatible.
- Added flow-aware alerts through `script.water_send_alert`:
  `irrigation_no_flow`, `irrigation_high_flow`, `irrigation_low_flow`,
  `irrigation_flow_after_stop`, `irrigation_unscheduled_flow`, and
  `irrigation_flow_meter_stale`.
- Kept routine start/finish pushes and added flow, gallons, pressure, and
  baseline context.
- Rebuilt the irrigation tab around state, active zone, session gallons, next
  run, Hunter flow, and shared-well pressure; demoted raw status/debug surfaces.
- Refreshed device inventory from a live registry export and refreshed recorder
  inventory for the new high-churn/history assumptions.

## Checks

- `python3 -m unittest tests/test_irrigation_history.py tests/test_irrigation_fingerprints.py`
- `python3 -m py_compile tools/irrigation_history.py tools/irrigation_fingerprints.py`
- Ruby YAML parse for:
  - `configuration.yaml`
  - `automations/00-water-irrigation.yaml`
  - `scripts.yaml`
  - `dashboards/calm_mobile.yaml`
- `python3 tools/generate_device_inventory.py --config-dir .tmp/live-config-for-inventory --output-dir docs --salt-file .inventory_salt --token-file .inventory_token`
- `python3 tools/check_device_inventory_coverage.py`
- `python3 tools/generate_recorder_inventory.py --config configuration.yaml --device-inventory docs/device-inventory.json --output-json docs/recorder-inventory.json --output-md docs/recorder-inventory.md`
- `git diff --check`

## Deployment Status

- Deployed the six changed live files through the authenticated File Editor
  ingress path:
  - `configuration.yaml`
  - `automations/00-water-irrigation.yaml`
  - `scripts.yaml`
  - `dashboards/calm_mobile.yaml`
  - `tools/irrigation_history.py`
  - `tools/irrigation_fingerprints.py`
- Live read-back hash verification matched for all deployed files.
- Home Assistant config check returned valid with no warnings.
- `template.reload`, `script.reload`, and `automation.reload` succeeded.
- `lovelace.reload` returned a 400 from the service call, so a full restart was
  used for the dashboard and helper/template changes.
- Restart call succeeded. The Remote UI shell briefly served a failed page and
  local mDNS did not resolve from the workstation, but the REST API recovered.
- Post-restart API verification confirmed:
  - `sensor.irrigation_flow_rate` exists and reports `gal/min`.
  - `sensor.irrigation_session_gallons` exists and reports `gal`.
  - `binary_sensor.irrigation_flow_meter_available` is `on`.
  - `sensor.irrigation_flow_baseline_status` exists.
  - `sensor.45_crr_daily_total_water_use` is present as the Hunter source.
- A post-restart dashboard check exposed a restored stale-meter transient alert
  even though the Hunter meter was available. The clear automation was tightened
  to also wake on Home Assistant start, periodic checks, and meter-available
  recovery while preserving the same all-clear conditions.
- The flow-meter availability template was also corrected to use the sampler's
  `input_datetime.irrigation_flow_meter_last_seen_at` heartbeat instead of the
  cumulative total sensor's raw `last_updated`, which may not change while
  irrigation is idle.

## Residual Risks And Follow-Ups

- Observe or simulate one real irrigation zone run to verify the first
  Hunter-derived session and zone history records end to end.
- Verify one routine start/finish push on the next live run for final message
  tone and action routing.
- Baseline alerts intentionally require enough clean prior samples; learned
  high/low deviations should not notify during the initial learning window.
- Since direct GPM is derived from total-use deltas, long Hydrawise update
  intervals can make flow less granular than a native GPM entity would be.
- Refresh device inventory again after the normalized YAML entities are present
  in the live registry if exact metadata coverage for those new entities is
  needed.
