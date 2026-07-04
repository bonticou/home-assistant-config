# Irrigation No-Flow False Alerts

## Symptom And Impact

Trevor received critical irrigation "no flow" alerts during the morning
watering run on 2026-07-04 even though irrigation was actually running. The
alerts were noisy and over-confident: they used the critical push path and
repeated across zones.

## Prior Context

- `2026-06-30-hunter-flow-irrigation-build.md` installed Hunter as the direct
  irrigation measurement layer while keeping Hydrawise as zone truth and Moen
  Flo as shared-well pressure context.
- That build discovered that HA exposes Hunter water as cumulative Hydrawise
  water-use totals, not a native live GPM sensor. `sensor.irrigation_flow_rate`
  is therefore derived from changes in `sensor.45_crr_daily_total_water_use`.

## Evidence Collected

- Live HA history was queried through the authenticated frontend session for
  2026-07-04, including irrigation active state, active zone, derived flow,
  Hunter cumulative total, well pressure, alert helper state, and no-flow alert
  keys.
- `binary_sensor.irrigation_active` showed real watering windows on
  2026-07-04, including 08:13-08:18 UTC, 08:30-08:36 UTC, 08:56-10:31 UTC, and
  another active window beginning at 11:32 UTC.
- `input_text.irrigation_last_no_flow_alert_key` changed repeatedly during
  active irrigation, including Zone 2 at 08:17 UTC, Zone 5 at 08:57 UTC, Zone 6
  at 09:09 UTC, Zone 7 at 09:29 UTC, Zone 8 at 09:49 UTC, Zone 9 at 10:10 UTC,
  Zone 10 at 10:15 UTC, Zone 11 at 10:20 UTC, Zone 15 at 11:34 UTC, and Zone 16
  at 11:45 UTC.
- `sensor.45_crr_daily_total_water_use` did not move continuously. It was 0 or
  unavailable early in the run, then jumped to about 3352.5 gal at 08:56 UTC,
  7304.6 gal at 09:56 UTC, became unavailable around 10:56 UTC, and returned at
  about 13334.1 gal at 11:32 UTC.
- `sensor.irrigation_flow_rate` consequently spent long periods at 0.0 and only
  briefly jumped when the cumulative total changed, including a 138.73 gal/min
  derived spike at 09:56 UTC.
- Shared-well pressure showed irrigation-like load during active periods. In
  the final live verification, irrigation was active on Zone 16, derived flow
  was still 0.0, current pressure was about 47.7 psi, zone pressure had dropped
  about 2.0 psi, and session pressure had already dipped about 5.9 psi from the
  session start/minimum context.
- The pre-fix active irrigation alert helper remained set to
  `irrigation_no_flow` until it was explicitly cleared after deployment.

## Findings

1. High confidence: the no-flow automation was too brittle for the Hunter data
   source. It alerted after only 180 seconds of zero derived GPM, but derived
   GPM can be zero for much longer whenever Hydrawise has not published a new
   cumulative Hunter total.
2. High confidence: the alert severity was too strong. `irrigation_no_flow` was
   hardcoded into the critical severity and critical iOS push branches in
   `script.water_send_alert`.
3. High confidence: well-pressure behavior is useful corroborating evidence,
   but it must be evaluated at both zone and session scope. Late-session zones
   may start when pressure is already depressed, so a zone-only pressure drop
   check still false-warns.
4. Medium confidence: per-zone gallons remain the right Hunter-side check for a
   possible no-flow condition. Whole-session gallons would hide a later zone
   problem after earlier zones have already accumulated water.

## Changes Made

- Changed `irrigation_no_flow` to "Hunter Flow Not Confirmed" language.
- Increased the minimum active-zone age from 3 minutes to 10 minutes.
- Required the current zone to have under 1 gallon recorded before alerting.
- Suppressed the alert when any shared-well pressure evidence corroborates
  irrigation load:
  - zone pressure drop is at least 6 psi;
  - session pressure drop is at least 5 psi; or
  - current shared-well pressure is already below 50 psi.
- Downgraded the automation severity from `critical` to `warning`.
- Updated `script.water_send_alert` label/title to
  "Irrigation flow not confirmed."
- Removed `irrigation_no_flow` from the default critical severity list and from
  the hardcoded critical iOS push branch. Other truly critical irrigation
  faults remain critical.
- Cleared the stale pre-fix `irrigation_no_flow` helper state and phone
  notification tag after the corrected automation was live.

## Checks

- Ruby YAML parse for `automations/00-water-irrigation.yaml`.
- Ruby YAML parse for `scripts.yaml`.
- `git diff --check`.
- Live File Editor/direct-ingress deployment wrote and read back:
  - `/homeassistant/automations/00-water-irrigation.yaml`
  - `/homeassistant/scripts.yaml`
- Live Home Assistant config check returned `valid` with no errors or warnings.
- `script.reload` returned 200.
- `automation.reload` returned 200.
- Post-threshold live verification at 11:52 UTC confirmed:
  - `binary_sensor.irrigation_active` was still `on`;
  - `sensor.irrigation_active_zone` was `Zone 16`;
  - `sensor.irrigation_flow_rate` was still `0.0`;
  - `input_boolean.water_irrigation_alert_active` remained `off`;
  - `input_text.irrigation_active_alert_kind` remained empty.

## Deployment Status

- Deployed live on 2026-07-04 through the authenticated HA Remote UI/File
  Editor ingress path.
- Read-back hash verification matched for both changed live files.
- Config check and reloads succeeded.
- The stale critical no-flow notification/helper state was cleared.

## Residual Risks And Follow-Ups

- Hunter cumulative totals still arrive sparsely, so the dashboard's live GPM
  line should be read as a derived signal rather than native meter telemetry.
- The no-flow alert is now intentionally conservative. It should be much
  quieter, but a true low-flow/no-flow zone may be reported as a warning only
  after stronger corroboration.
- Observe the next full watering run to confirm that "flow not confirmed" stays
  quiet during normal shared-well pressure load and only appears when both
  Hunter gallons and pressure corroboration are absent.
- If Hunter exposes a native live GPM entity in a future integration update,
  replace the derived-flow no-flow logic with that direct entity.
