# Irrigation History And August Commute Cleanup

## Symptom And User Impact

Two follow-ups came out of the irrigation notification triage:

- Old low-confidence irrigation flow notifications could still appear in the
  custom irrigation history after the rules were demoted.
- Trevor does not commute in August, so Metro-North notifications and the
  dashboard card should stay quiet for the month without generating suppressed
  notification history or extra Recorder churn.

## Relevant Prior Context

- `2026-08-06-irrigation-anomaly-notification-triage.md` demoted sparse
  derived-flow irrigation push alerts to diagnostic history and preserved
  higher-confidence pressure, Hydrawise, schedule, and start/finish notices.
- `docs/recorder-inventory.md` already excluded the Metro-North command-line
  sensor from Recorder, but the dashboard-only commute card sensor was still a
  Recorder candidate.

## Changes Made

- Added an exact `purge-demoted-flow-alerts` command to
  `tools/irrigation_history.py`.
  - Removes only the retired/demoted irrigation flow event kinds:
    no flow, high flow, low flow, flow after stop, unscheduled flow, and flow
    meter stale.
  - Preserves real irrigation history such as sprinkler start/finish,
    Hydrawise/controller offline, pressure collapse, zone ran too long, valve
    mismatch, and multiple-zone alerts.
- Added `shell_command.irrigation_history_purge_demoted_flow_alerts` so the
  exact cleanup can be run live after deployment.
- Made Metro-North commute quiet during August:
  - the departure automation exits before refreshing train data, sending a
    notification, or writing commute helper state;
  - the command-line sensor returns an `off_season` payload in August before
    fetching or parsing MTA schedule/realtime data;
  - the dashboard card binary sensor is forced off in August;
  - the dashboard-only binary sensor is excluded from Recorder.

## Recorder Awareness

The August commute behavior uses quiet absence, not a suppressed-event trail:

- no August push notification;
- no August helper write for card text or last-notified time;
- no August MTA network fetch from the command-line sensor;
- no Recorder history for the dashboard-only card sensor.

## Checks

- `python3 -m unittest tests/test_irrigation_history.py`
- Metro-North quiet-mode command returned `source: off_season` with no trains.
- Ruby YAML parse:
  - `configuration.yaml`
  - `automations/20-climate-commute.yaml`
  - `scripts.yaml`
- `python3 tools/generate_recorder_inventory.py`
  - Recorder candidates changed from 1567 to 1566.
  - Low-stateful-need candidates changed from 173 to 172.

## Deployment Status

- Deployed live on 2026-08-06 through the established Nabu Casa File Editor
  ingress path.
- Wrote and read back matching content for:
  - `/homeassistant/configuration.yaml`
  - `/homeassistant/automations/20-climate-commute.yaml`
  - `/homeassistant/tools/irrigation_history.py`
  - `/homeassistant/tools/mta_mnr_departures.py`
- Home Assistant config check returned `valid` with no warnings or errors.
- A controlled Home Assistant restart was required to activate the new
  `shell_command`, `command_line`, and Recorder configuration.
- The exact demoted-flow cleanup was run after restart.

## Live Verification

- `sensor.irrigation_history_status` reported 176 events after cleanup.
- Demoted irrigation flow alert/diagnostic event count was 0 after cleanup.
- `sensor.metro_north_nwp_to_grand_central` reported:
  - state: `Off-season`
  - source: `off_season`
  - trains: 0
- `binary_sensor.metro_north_commute_card_active` was `off` with
  `commute_season_active: false`.
- `shell_command.irrigation_history_purge_demoted_flow_alerts` was registered
  after restart.

## Residual Risks And Follow-Ups

- The custom irrigation history cleanup is expected to improve clarity, not
  materially reduce storage; the history ledger is compact and capped.
- The August commute quiet mode is calendar-based. If the non-commute window
  changes in future years, update the quiet month list or replace it with a
  small explicit commute-season helper.
