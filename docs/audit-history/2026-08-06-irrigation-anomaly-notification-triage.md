# Irrigation Anomaly Notification Triage

## Symptom And User Impact

Trevor reported that several irrigation anomaly notifications did not feel
reliable, especially messages about irregular zones, pressure, or flow. The
concern was that some alerts may be based on weak inferences rather than solid
measurements and should either be improved with Hunter Flow data or stopped.

## Prior Context

- `2026-06-30-hunter-flow-irrigation-build.md` made Hydrawise the schedule/zone
  truth, Hunter the irrigation water-use layer, and Flo shared-well pressure
  context.
- `2026-07-04-irrigation-no-flow-false-alerts.md` confirmed that HA does not
  expose native live Hunter GPM. `sensor.irrigation_flow_rate` is derived from
  sparse cumulative-total changes, so it can sit at zero and then spike even
  during normal watering.
- `2026-08-06-irrigation-start-notification-miss.md` found stale irrigation
  session helpers and stale history surfaces, so irrigation visibility still
  needed skepticism.

## Evidence Collected

- Live `sensor.irrigation_flow_baseline_status` had only one learned zone:
  `Zone 8`, with three clean samples.
- Recent irrigation history was dominated by:
  - `alert_irrigation_flow_meter_stale`;
  - `alert_irrigation_controller_offline_during_watering`;
  - older repeated `alert_irrigation_no_flow` entries;
  - one `alert_irrigation_recovery_slow` entry reporting `0.0 psi`, which is more
    consistent with bad/unavailable pressure telemetry than a meaningful
    recovery judgment.
- The high/low baseline alert template compared live derived GPM to learned
  medians, even though derived GPM is already known to be sparse and laggy.
- `script.water_send_alert` treated all irrigation anomaly kinds as active
  water alerts, and `irrigation_high_flow` was in the critical push path.

## Findings

1. High confidence: live derived Hunter GPM should not page Trevor by itself.
   It is useful dashboard/diagnostic context, but too sparse for precise push
   alerts.
2. High confidence: baseline high/low alerts are not mature enough for push
   notifications yet. Only one zone is learned, and even a learned zone still
   uses sparse derived GPM during the run.
3. High confidence: pressure recovery alerts need sanity checks so an invalid
   or `0.0 psi` pressure reading does not create a misleading recovery alert.
4. Medium confidence: Hydrawise offline alerts remain useful because they explain
   HA blindness during watering, but they should be watched for frequency.
5. Medium confidence: true low shared-well pressure during active irrigation
   remains push-worthy because it is based on a direct pressure entity and has a
   clear household/system meaning.

## Changes Made

- Converted the low-confidence derived-flow notification automations to
  diagnostic irrigation history events instead of phone pushes:
  - `irrigation_no_flow`;
  - `irrigation_high_flow`;
  - `irrigation_low_flow`;
  - `irrigation_flow_after_stop`;
  - `irrigation_unscheduled_flow`;
  - `irrigation_flow_meter_stale`.
- Preserved their duplicate keys and history evidence so the system can still
  learn from them without waking Trevor.
- Hardened `irrigation_recovery_slow` and `irrigation_recovery_failed` with a
  pressure sanity condition requiring a numeric pressure greater than 5 psi
  before judging recovery.
- Left these push-worthy alerts intact:
  - routine start/finish;
  - active shared-well pressure collapse;
  - zone running too long;
  - Hydrawise valve state mismatch;
  - multiple active zones;
  - Hydrawise offline before/during watering;
  - scheduled watering did not start when not plausibly explained by weather.

## Checks

- Local YAML parse for `automations/00-water-irrigation.yaml`.
- `git diff --check`.
- Repo grep confirmed the low-confidence derived-flow automations now write
  `diagnostic_irrigation_*` history events instead of calling
  `script.water_send_alert`.

## Deployment Status

- Deployed to live Home Assistant on 2026-08-06 after the Nabu route recovered.
- The normal File Editor tab was stale/disconnected, so deployment used the
  established direct browser pattern from a connected Nabu dashboard tab:
  authenticated HA websocket, fresh File Editor ingress session, file write,
  byte-for-byte read-back, config check, and automation reload.
- Live deployment wrote `/homeassistant/automations/00-water-irrigation.yaml`;
  read-back hash matched the repo file.
- Home Assistant config check returned `valid` with no warnings or errors.
- `automation.reload` returned 200.
- Live automation config verification confirmed:
  - `irrigation_no_flow`, `irrigation_high_flow`, `irrigation_low_flow`,
    `irrigation_flow_after_stop`, `irrigation_unscheduled_flow`, and
    `irrigation_flow_meter_stale` no longer call `script.water_send_alert`;
  - those six automations now write `diagnostic_irrigation_*` history events;
  - `irrigation_recovery_slow_followup` and
    `irrigation_recovery_failed_followup` still use the push path but include
    the pressure sanity guard.

## Residual Risks And Follow-Ups

- Revisit baseline push notifications only if Hunter exposes native live GPM or
  a larger set of clean per-zone samples proves the derived signal is stable
  enough.
- Fix or replace stale irrigation history active-zone cleanup so diagnostic
  history is trustworthy.
- Watch Hydrawise-offline notification frequency; if it remains noisy, demote it
  to a dashboard notice unless it occurs immediately before or during a scheduled
  run.
