# Irrigation False Critical Alerts

## Symptom And User Impact

Trevor reported repeated sprinkler alerts that did not match real conditions,
including zones said to be running too long and critical pressure alerts when
there was no actual problem. These false critical pushes reduce confidence in
the water safety system and can hide alerts that genuinely require action.

## Relevant Prior Context

- `2026-07-04-irrigation-no-flow-false-alerts.md` established that Hunter flow
  is derived from sparse cumulative data and cannot reliably prove live flow.
- `2026-08-06-irrigation-anomaly-notification-triage.md` demoted weak
  flow-derived anomaly pushes but retained zone-too-long and shared-well
  pressure alerts.
- `2026-08-06-irrigation-start-notification-miss.md` confirmed stale irrigation
  session helpers and active-zone context can survive missed Hydrawise
  transitions.

## Evidence Collected

- The live Irrigation dashboard showed `North back lawn lower` as a live run,
  `Meter stale`, and `irrigation_zone_ran_too_long` at the same time.
- The live seven-day ledger contained impossible reported runs of approximately
  751 minutes and 520 minutes. These are consistent with stale Hydrawise zone
  state, not credible single-zone watering durations.
- The Water dashboard showed both the Valve/Flo and Irrigation guardrails still
  active, with `Irrigation zone ran too long` as the latest alert.
- Live shared-well pressure moved through the high-40s while the stale
  irrigation alert remained active. The pressure entity measures the shared
  house/well system, not a dedicated irrigation fault condition.
- The current `irrigation_pressure_collapse` automation treated pressure below
  25 psi for three minutes, or below 20 psi for one minute, as a critical
  irrigation failure whenever Hydrawise reported any active zone. It required
  no independent evidence of a stuck valve, failed zone, leak, or pump fault.
- The current zone-too-long alert depended on the same Hydrawise active-zone
  state and a helper timestamp, so a missed zone transition could satisfy the
  45-minute threshold even when no zone had actually run that long.

## Findings

1. High confidence: zone-running-too-long is not push-worthy while Hydrawise
   zone transitions can remain stale for hours.
2. High confidence: shared-well pressure alone is not sufficient evidence for
   a critical irrigation alert. Normal well cycling and household demand can
   lower it, and the irrigation-active gate itself can be stale.
3. High confidence: both signals remain useful as diagnostic evidence for
   improving integration health and future corroborated alert design.
4. Medium confidence: the same stale-state failure can distort irrigation
   duration and water-use dashboard summaries. That broader data-quality issue
   remains separate from stopping false critical pushes.

## Changes Made

- Converted `irrigation_pressure_collapse` from a critical phone alert to a
  warning-severity diagnostic irrigation-history event.
- Converted `irrigation_zone_ran_too_long` from a critical phone alert to a
  warning-severity diagnostic irrigation-history event.
- Preserved the trigger thresholds, timestamps, zone names, pressure readings,
  and session context so the anomalies remain auditable.
- Removed both alert kinds from the shared notification script's default
  critical classification and hardcoded critical iOS push branch.
- Did not change leak, burst-flow, valve-closed, routine sprinkler start/finish,
  controller-offline, or other water safety behavior.

## Checks

- Ruby YAML parsing passed for the changed automation and script files, plus
  `configuration.yaml` and the calm mobile dashboard.
- All 11 irrigation unit tests passed.
- `git diff --check` passed.
- Live deployment, read-back, Home Assistant config validation, automation
  reload, and stale-notification cleanup are not yet performed.

## Deployment Status

- Repository change only; not yet deployed to live Home Assistant.

## Residual Risks And Follow-Ups

- The currently active stale irrigation guardrail and old phone notification
  will remain until live deployment and explicit cleanup.
- Audit the Hydrawise zone-transition source and reconcile stale zone/session
  helpers before relying on durations for push alerts again.
- Review the irrigation ledger's unit handling and impossible multi-hour runs;
  current displayed gallons and durations should not be treated as accurate
  until that data-quality review is complete.
- Reintroduce anomaly pushes only when a condition is corroborated by an
  independent, timely signal and cannot be explained by stale integration state
  or normal shared-well behavior.
