# Irrigation Ledger Zone Count

## Symptom And User Impact

The irrigation dashboard showed recent high-water days as "Full cycle" with
only 13 or 14 zones. Trevor believed those were full runs, so the count looked
dubious and undermined trust in the irrigation ledger.

## Prior Context

- `2026-06-30-hunter-flow-irrigation-build.md` made Hydrawise the zone/schedule
  truth and Hunter the irrigation measurement layer.
- `2026-07-04-irrigation-no-flow-false-alerts.md` found that Hunter cumulative
  totals can update sparsely, so dashboard/history logic should avoid
  over-confident interpretations of partial telemetry.

## Evidence Collected

- Live `sensor.irrigation_7_day_ledger` showed:
  - 2026-07-10: 28,489.7 gallons, "Full cycle - 14 zones"
  - 2026-07-12: 28,324.2 gallons, "Full cycle - 13 zones"
- The same live Recorder history for Hydrawise
  `sensor.zone_*_daily_active_watering_time` showed 29 zones with positive
  runtime on both 2026-07-10 and 2026-07-12.
- Live Hydrawise inventory/config exposed zones 28, 29, and 30, while several
  repo templates and the ledger command still used a 27-zone universe.
- Zone 30 is present but automatic watering is off and has no next cycle, so
  29 zones appears to be the current full scheduled Hydrawise run.
- `.irrigation_history` had partial zone-transition records for those days.
  The ledger preferred that partial source wholesale, so it discarded the
  fuller Hydrawise daily runtime fallback whenever any custom history existed.

## Findings

1. High confidence: the dashboard was not proving that only 13 or 14 zones ran.
   It was showing an incomplete custom history count.
2. High confidence: "Full cycle" was over-confident wording because the label
   was based on gallons over 5,000 and more than six recorded zones, not on a
   complete Hydrawise zone set.
3. High confidence: the repo's 27-zone template/config references were stale
   relative to live Hydrawise's 30 exposed zones.
4. Medium confidence: `.irrigation_history` still has stale active-zone entries
   from missed or offline Hydrawise transitions, so it should enrich the ledger
   but not suppress Hydrawise's controller-reported daily runtime.

## Changes Made

- Changed `tools/irrigation_7day_ledger.py` so daily zone context merges
  custom irrigation history with Hydrawise daily active watering time instead
  of choosing the custom history source wholesale.
- Added name-based dedupe so named Hydrawise zones such as Vegetable garden do
  not duplicate their stable `Zone N` record.
- Replaced over-confident "Full cycle" labels with source-aware labels such as
  "Hydrawise logged 29 zones" or "7 zones recorded."
- Changed high-gallon day summaries from "Full irrigation run" to "Heavy
  irrigation."
- Updated the irrigation ledger command to use `--zone-count 30`.
- Expanded irrigation active-zone, schedule, focus-zone, and mismatch templates
  from zones 1-27 to zones 1-30.
- Added unit tests for Hydrawise/custom-history zone merging and non-overclaiming
  labels.

## Checks

- `python3 -m unittest tests/test_irrigation_7day_ledger.py`
- `python3 -m py_compile tools/irrigation_7day_ledger.py`
- Ruby YAML parse for `configuration.yaml`
- Ruby YAML parse for `dashboards/calm_mobile.yaml`
- `python3 tools/check_device_inventory_coverage.py`
- `git diff --check`

## Deployment Status

- Deployed `configuration.yaml` and `tools/irrigation_7day_ledger.py` through
  the authenticated Home Assistant File Editor ingress path.
- File Editor read-back matched both deployed files.
- Home Assistant config check returned valid with no warnings or errors.
- Redeployed the final cleaned `tools/irrigation_7day_ledger.py` after source
  attribution cleanup; read-back and config check were again valid.
- `input_select.reload` and `command_line.reload` returned 200 through raw
  authenticated service calls.
- `template.reload` through the frontend service path did not return promptly,
  but template-backed schedule verification showed `sensor.irrigation_schedule_summary`
  live with 30 zones, including zones 28, 29, and 30.
- `homeassistant.update_entity` restored command-line sensors after reload.
- Live ledger verification showed:
  - 2026-07-10: "Hydrawise logged 29 zones"
  - 2026-07-12: "Hydrawise logged 29 zones"
  - 2026-07-11: "Vegetable garden - 10 min"
  - 2026-07-13: "Vegetable garden + 1 more - 43 min"

## Residual Risks And Follow-Ups

- `.irrigation_history` still contains stale active-zone entries from earlier
  missed/offline transitions. A separate cleanup should close stale active
  zones at session finish and avoid leaving old active zones in status.
- Hunter gallons are still daily-total based and sparse; Hydrawise is now the
  better source for "which zones ran," while Hunter remains the better source
  for total irrigation volume.
- Zone 30 is exposed but automatic watering is off. If Zone 30 becomes part of
  normal watering, the ledger should naturally count 30 zones after Hydrawise
  reports runtime.
