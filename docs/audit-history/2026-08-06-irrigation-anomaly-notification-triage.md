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

- Not deployed yet.
- The Nabu Casa dashboard tab became disconnected and then loaded the Remote UI
  error page during deployment.
- Direct local checks to `homeassistant.local:8123` and `homeassistant:8123`
  timed out from the Mac, and the Nabu Casa URL timed out during TLS setup.
- Live deployment should be retried when HA is reachable, using the normal
  read-back/config-check/automation-reload path.

## Residual Risks And Follow-Ups

- Revisit baseline push notifications only if Hunter exposes native live GPM or
  a larger set of clean per-zone samples proves the derived signal is stable
  enough.
- Fix or replace stale irrigation history active-zone cleanup so diagnostic
  history is trustworthy.
- Watch Hydrawise-offline notification frequency; if it remains noisy, demote it
  to a dashboard notice unless it occurs immediately before or during a scheduled
  run.
