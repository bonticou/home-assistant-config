# Irrigation Flo Topology Correction

Date: 2026-06-09

## Symptom And User Impact

The irrigation system was confirmed to sit outside the Moen Flo measured and
shutoff branch, while still sharing the same well as the house. That means
Hydrawise remains the irrigation source of truth, and Flo pressure is useful
only as indirect shared-well pressure context.

The previous irrigation logic treated Flo flow, gallons, and valve state as
irrigation facts. That could create misleading alerts, learned baselines, and
dashboard copy about no-flow zones, flow after stop, blind watering, breaks,
clogs, or missing Flo telemetry during irrigation.

## Relevant Prior Context

- Irrigation history and fingerprint helpers were created to correlate
  Hydrawise zone activity with Flo telemetry.
- The regular Water tab and ordinary household water alerts also use Flo
  pressure, flow, gallons, and valve state. Those were intentionally outside
  the scope of this correction.
- Existing water-alert conditions continue to use
  `binary_sensor.irrigation_expected_water_use` so household water-alert
  behavior is not changed indirectly by this irrigation cleanup.

## Evidence Collected

Repository review found irrigation-specific dependencies on Flo flow or gallons
in these areas:

- Hydrawise irrigation automations that recorded session gallons, max flow,
  no-flow zones, flow after stop, blind watering, break/clog fingerprints, and
  Flo telemetry unavailable during watering.
- Irrigation dashboard surfaces showing Flo well truth, flow, gallons, average
  and maximum flow, learned zones, and fingerprint anomalies.
- Irrigation history and fingerprint tools that retained Flo-derived sessions,
  zone runs, active state, samples, anomalies, and learned profiles.

The same review found controller-only checks that remain valid and were
preserved:

- Hydrawise/controller offline while watering.
- Scheduled cycle missed.
- Zone ran too long.
- Valve/watering mismatch.
- Multiple zones active.
- Weather skip inference.
- Shared-well pressure collapse and recovery checks, rewritten without Flo
  flow or gallon claims.

## Ranked Findings

1. **Flo flow, gallons, daily usage, and valve state are not irrigation
   evidence. Confidence: high.** Irrigation is outside the Moen Flo measured
   branch.

2. **Flo pressure remains useful as indirect shared-well context. Confidence:
   high.** The house and irrigation share the same well, so pressure changes can
   still signal well-side stress during Hydrawise activity.

3. **Hydrawise/controller state is the correct irrigation source of truth.
   Confidence: high.** Controller schedule, zone state, run duration, and
   weather skip inference are still directly tied to irrigation.

4. **Historic Flo-derived irrigation memory is unreliable. Confidence: high.**
   Learned samples, session gallons, zone flow profiles, and fingerprint
   anomalies were built from telemetry that does not measure the irrigation
   branch.

## Changes Made

- Removed irrigation-only Flo flow/gallon alerts:
  - flow after stop;
  - no-flow zone detection;
  - blind watering;
  - break/clog fingerprint alerts;
  - Flo telemetry unavailable/restored during irrigation.
- Kept controller-based irrigation checks and rewrote their copy to Hydrawise
  status plus shared-well pressure context.
- Kept pressure-collapse and recovery checks, but renamed them as shared-well
  pressure alerts and removed Flo flow/gallon claims.
- Preserved regular Water tab cards, ordinary water alerts, and
  `binary_sensor.irrigation_expected_water_use` behavior.
- Reworked the irrigation dashboard to show Hydrawise schedule/status and
  shared-well pressure instead of Flo flow, gallons, zone learning, or
  fingerprint anomalies.
- Added `reset` support to `tools/irrigation_fingerprints.py`.
- Added `purge-flo-derived` support to `tools/irrigation_history.py`.
- Added unit tests for fingerprint reset and irrigation history purge behavior.

## Memory Cleanup Plan

After deployment, run the new live cleanup commands once against the live
`/config` files:

- `shell_command.irrigation_fingerprint_reset`
- `shell_command.irrigation_history_purge_flo_derived`

Then refresh the command-line status sensors so the dashboard and diagnostics
read the sanitized memory.

The history purge removes Flo-derived sessions, zone runs, active session and
zone state, fingerprint/anomaly events, and notes that depend on Flo flow,
gallons, learned profiles, clogs, breaks, or baselines. Clean controller-only
events are preserved when separable.

Live cleanup was completed during this pass. Because Home Assistant does not
hot-reload the `shell_command` domain, the one-shot cleanup was applied through
the File Editor route using the same purge rules, then Core was restarted so the
new reset/purge shell-command services replaced the old fingerprint/session
services.

## Checks

Local checks run before live deployment:

- `python3 -m unittest tests.test_irrigation_history tests.test_irrigation_fingerprints`
- Ruby YAML parse for:
  - `configuration.yaml`
  - `automations/00-water-irrigation.yaml`
  - `scripts.yaml`
  - `dashboards/calm_mobile.yaml`
- `python3 tools/check_device_inventory_coverage.py`

`python3 tools/generate_device_inventory.py --config-dir . --output-dir docs`
could not regenerate inventory from this checkout because live `.storage`
registry files are not present in the repo workspace. Coverage still passed
against the existing inventory.

Live checks run after deployment:

- File Editor deploy helper wrote and read back:
  - `configuration.yaml`
  - `automations/00-water-irrigation.yaml`
  - `scripts.yaml`
  - `dashboards/calm_mobile.yaml`
  - `tools/irrigation_fingerprints.py`
  - `tools/irrigation_history.py`
- HA config check returned `valid` with no warnings.
- Core restart completed and the frontend reconnected.
- Live `shell_command` services now expose only:
  - `irrigation_fingerprint_reset`
  - `irrigation_history_event`
  - `irrigation_history_purge_flo_derived`
- Removed helper entities for session gallons, max flow, zone gallons, and the
  latest fingerprint anomaly key were absent after restart.
- `binary_sensor.irrigation_well_pressure_proxy_available` was live and `on`.
- Fingerprint memory was empty:
  - learned zones: `0`
  - active zones: `0`
  - latest anomaly: empty
- Irrigation history was sanitized:
  - sessions: `0`
  - zone runs: `0`
  - events preserved: `18`
  - no preserved event mentioned Flo, flow, gallons, gpm, fingerprints, learned
    profiles, clogs, or breaks.

## Deployment Status

Deployment completed on 2026-06-09. The live config was written with read-back
hash verification, HA config check passed, Core was restarted, and live
irrigation fingerprint/history memory was reset and purged.

## Residual Risks And Follow-Ups

- There is still no direct irrigation flow sensor. Hydrawise can tell what the
  controller intended and what zones report active, but it cannot prove water
  actually moved through each irrigation branch.
- Shared-well pressure can show stress, but it cannot identify a specific
  irrigation-zone flow problem by itself.
- Regular Water tab and ordinary household water alerts were intentionally left
  unchanged, including their current conditions and use of irrigation expected
  water-use context.
- A live registry export confirmed the new pressure-proxy template entity is
  registered, but this local pass did not complete a full generated inventory
  refresh because redirecting the large Safari export payload into the repo was
  unreliable in the Codex app session. Regenerate the full device inventory from
  a current backup or live `.storage` export when available.
