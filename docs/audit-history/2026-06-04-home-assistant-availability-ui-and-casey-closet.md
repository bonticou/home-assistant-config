# Home Assistant Availability, UI Hardening, And Casey Closet Recovery

Date: 2026-06-04

## Summary

This entry records the May 26 through June 4 Home Assistant reliability audit and
follow-up fixes. The work started as a critical remote/mobile availability
incident: Home Assistant often opened to a blank navy shell, the iOS companion
app showed "You're disconnected," and Safari sometimes showed the Nabu Casa
"Unable to connect to Home Assistant" fallback. The issue happened on both
mobile and Safari, sometimes while remote, and recovered later without a clear
single user action.

The audit treated this as an availability problem first and a dashboard problem
second. That was the right ordering. Live evidence repeatedly showed failures
before the custom dashboard could fully load, including Nabu Casa fallback and
TLS/connectivity failures. Because the main mobile dashboard is large and uses
several custom resources, the audit also added a stock diagnostic dashboard and
frontend boot probe so future incidents can separate "HA is unreachable" from
"HA reached the browser but the dashboard failed."

Separately, while validating the repaired system, Casey's closet automation
failed because the automation still referenced an old motion entity. That was
fixed and live-validated end to end. A later review found no separate old
"light has been on for 5 minutes, turn it off" automation remaining, but stale
repo wording still described that old behavior. The wording was cleaned up so
the repo and dashboard describe the current motion-based behavior.

## User Impact

- Remote and mobile access to Home Assistant was intermittently unavailable.
- Safari and the companion app failed together, which made the house UI feel
  unreliable rather than merely slow.
- During some incidents, the Nabu Casa remote UI host was reachable but could
  not connect through to the local HA instance.
- The primary `calm-mobile` dashboard sometimes appeared blank after the HA
  logo, which created concern that custom UI code might be involved.
- Casey's closet light did not turn on when motion occurred because the
  automation targeted a stale motion entity.

## Prior Context Reviewed

- `docs/home-assistant-mobile-disconnect-audit-2026-05-26.md`
- `docs/home-assistant-remote-access-runbook.md`
- `docs/home-assistant-ui-hardening-runbook.md`
- `docs/home-assistant-load-audit-2026-05-23.md` remains an untracked legacy
  scratch/report file and was intentionally preserved.
- Recent commits around Casey closet motion behavior and HA config structure.

## Evidence Collected

### Remote Access And Mobile Availability

- Screenshots showed the iOS app in two states:
  - blank dark/navy Home Assistant shell;
  - companion app "You're disconnected" screen.
- A later iPhone Safari screenshot showed the Nabu Casa fallback page:
  "Unable to connect to Home Assistant" with an automatic retry timer.
- Another Safari screenshot showed it could not establish a secure connection
  to the redacted Nabu Casa host.
- The issue occurred on both mobile app and Safari, so it was not only an iOS
  companion app WebView/cache problem.
- The issue occurred while remote and later recovered, matching an intermittent
  Remote UI/cloud tunnel or home-side availability failure.
- From the audit Mac, remote probing sometimes failed at TLS or before a normal
  HTTP/API response, which is not consistent with a Lovelace-only failure.
- The external probe design uses `/api/websocket` and treats `auth_required` as
  the strongest unauthenticated proof that the request reached HA.

### UI And Frontend Risk

- The normal dashboard route is `/calm-mobile/home`.
- The diagnostic route added for comparison is `/ha-safe/home`.
- The `calm-mobile` dashboard is large and custom-resource-heavy.
- Known frontend risk included custom cards, Browser Mod, ApexCharts, and
  history-loading custom cards.
- The radon and Casey timeline custom cards previously did history work early
  in their lifecycle, creating first-paint risk.
- The safe dashboard uses stock Lovelace cards so it can remain usable when
  custom resources are suspect.

### Configuration And Deployment Risk

- A live File Editor save truncated the tail of a very large
  `configuration.yaml` during one recovery attempt.
- The truncation was caught before a bad restart, and the configuration was
  repaired by splitting coherent tail domains into separate includes.
- This produced an important repository principle: very large config files are
  not only harder to read; they can become live deployment reliability risks.

### Casey Closet Automation

- Live HA state showed:
  - `automation.lights_casey_s_closet_auto_off` existed and was enabled.
  - `light.master_casey_s_closet` worked.
  - the old `binary_sensor.usl_motion_motion` no longer existed.
  - the live motion entity was `binary_sensor.casey_s_closet_motion`.
- After the entity fix, the automation was observed working:
  - motion trigger fired;
  - closet light turned on roughly 40 ms later;
  - motion cleared;
  - the light turned off after the configured 3 quiet minutes.
- This proved the remaining perceived lag is probably sensor detection/reporting
  latency before HA sees motion, not YAML or light service latency.

## Ranked Findings

### 1. Remote outages were primarily availability/path failures, not dashboard rendering

Confidence: high.

Safari and the mobile app failed together. At least one live remote incident
reached Nabu Casa's fallback page, which means the browser could reach the
remote service but the remote service could not reach the local HA instance.
TLS/connect failures also occurred before Lovelace could be evaluated.

Smallest safe fix applied: add a watchdog and external probe so the next outage
is detected and classified with evidence.

### 2. The main dashboard still needed a diagnostic comparison path

Confidence: high.

Even if access-layer failures were the lead cause, `calm-mobile` has enough
frontend payload and custom-resource risk that a stock-only comparison dashboard
is valuable. Without it, a blank-after-logo symptom is ambiguous.

Smallest safe fix applied: add `/ha-safe/home` and extend the probe to compare
root, safe dashboard, normal dashboard, resources, and websocket reachability.

### 3. Large live-edited config files were a reliability hazard

Confidence: high.

The File Editor truncation event showed that the old monolithic
`configuration.yaml` shape increased operational risk. The fix was not a style
preference; it reduced deploy blast radius and made live read-back safer.

Smallest safe fix applied: split statistics sensors into `sensors.yaml` and
YAML light groups into `lights.yaml`, then document decomposition rules in
`AGENTS.md`.

### 4. Casey closet failure was caused by entity drift

Confidence: high.

The automation referenced an entity that no longer existed. Replacing it with
the live motion entity restored the automation, and live state confirmed the
motion-on and quiet-off branches worked.

Smallest safe fix applied: update the automation triggers to use
`binary_sensor.casey_s_closet_motion`.

### 5. Casey closet "snappiness" is limited by sensor reporting, not automation speed

Confidence: medium-high.

Once HA saw the motion event, the light turned on within roughly 40 ms. Any
human-noticeable delay is therefore likely before HA receives the motion state,
or in the sensor/device integration path.

Smallest safe next fix: identify a faster trigger source, such as a door/contact
sensor or dedicated local motion/occupancy sensor, and use it as an additional
turn-on trigger if available.

## Changes Made

### Remote Access Reliability

- Added a Home Assistant Remote UI watchdog.
- Added recovery attempt tracking and degraded/restored timestamps.
- Added `sensor.home_assistant_remote_access_status`.
- Added `tools/ha_remote_health_probe.py`.
- Added `docs/home-assistant-remote-access-runbook.md`.

Relevant commit:

- `763ae54 Add HA remote access reliability watchdog`

Backup tag:

- `backup-ha-remote-reliability-pre-fix-20260527`

### UI Hardening Diagnostics

- Added stock-only diagnostic dashboard `dashboards/ha_safe.yaml`.
- Registered `/ha-safe/home` in `configuration.yaml`.
- Extended the remote health probe to compare `/`, `/ha-safe/home`, and
  `/calm-mobile/home`.
- Added resource timing/resource extraction support.
- Deferred early history loading in repo-owned custom cards:
  - `www/radon-air-quality-card.js`
  - `www/casey-presence-timeline-card.js`
- Added `docs/home-assistant-ui-hardening-runbook.md`.

Relevant commit:

- `09b190e Add HA safe dashboard boot diagnostics`

Backup tag:

- `backup-ha-ui-hardening-pre-diagnostic-20260603`

### Config Recovery And Decomposition

- Repaired live `configuration.yaml` after a browser/File Editor truncation
  during deployment.
- Split tail sections:
  - `sensor: !include sensors.yaml`
  - `light: !include lights.yaml`
- Added:
  - `sensors.yaml`
  - `lights.yaml`
- Documented when and why to split HA config in `AGENTS.md`.

Relevant commits:

- `71a25be Split HA config tail includes`
- `66d8369 Document HA config decomposition rules`

### Casey Closet Motion Repair

- Replaced stale `binary_sensor.usl_motion_motion` references with
  `binary_sensor.casey_s_closet_motion`.
- Reloaded automations live after config check.
- Confirmed the automation fired, turned the light on, waited for quiet, and
  turned it off.

Relevant commit:

- `86d89df Fix Casey closet motion trigger entity`

### Casey Closet Old Rule Cleanup

- Reviewed repo automation and script references for Casey closet shutoff logic.
- Found no separate remaining crude "on for 5 minutes, turn it off" rule.
- Found stale dashboard/helper wording that still described a 5 minute fallback.
- Updated wording to describe the current motion helper:
  - motion turns the closet light on;
  - 3 quiet minutes turn it off.

Relevant commit:

- `11588e4 Clarify Casey closet motion helper wording`

### Casey Closet Stale-On Safety Net

- Added the deliberate crude-but-safe fallback Trevor requested:
  if Casey's closet light is on and the closet motion sensor has not been `on`
  for 3 continuous minutes, turn the light off.
- Implemented this inside the existing Casey closet helper rather than as a
  second competing rule.
- Replaced the old motion-off trigger with a template trigger that watches both
  the light and motion state, so manual-on and already-on cases are covered.
- Kept the motion-on branch unchanged.

Relevant commit:

- `01b4788 Add Casey closet stale-on safety net`

Deployment note: the reliable live deploy path was Nabu Casa Remote UI File
Editor at `/core_configurator`, after verifying the frontend was connected and
the File Editor iframe had mounted through `/api/hassio_ingress/`. The helper
wrote and read back `automations.yaml` and `dashboards/calm_mobile.yaml`, HA
config check returned valid with no warnings, and a targeted `automation.reload`
completed successfully after the helper's short reload calls timed out.

## Checks And Validation

### Local Checks

- YAML parse checks were run for affected files when Python/Ruby tooling was
  available.
- `python3 tools/check_device_inventory_coverage.py` passed after the Casey
  closet entity fix:
  - `Inventory coverage ok: 72 active control entity references are recorded.`
- `git diff --check` passed for committed slices.

### HA Live Checks

- HA config check passed during the major remote/UI/config recovery deploys.
- HA restarted normally after the config split recovery.
- Local post-restart probe confirmed:
  - `/`
  - `/ha-safe/home`
  - `/calm-mobile/home`
  - `/api/websocket`
- Casey closet automation was live-tested successfully after reload.

### Known Validation Gaps

- A fresh live `.storage` registry export is still needed before regenerating
  device inventory docs that reflect the new Casey closet entity. The repo's
  current generator needs live registries that are not committed.
- Remote probe results from the Mac can be distorted by local network/VPN/filter
  path behavior, so they should be interpreted alongside iPhone/Safari evidence.

## June 4 Storage, Recorder, Motion, And Wine Follow-Up

### Triggering Symptoms

After the remote/UI recovery, HA still showed signs of state/history strain:

- File Editor had previously failed to create `/homeassistant/automations`
  with `No space left on device`.
- Live `home-assistant_v2.db` was observed around 14 GB.
- The Home header's latest motion line showed Wynn's Room from June 1 even
  though motion had occurred elsewhere since then.
- The wine dashboard showed current temperature/humidity but the 24-hour trend
  chart had little or no data.

### Backup Space Recovery

Trevor selected three old local-only backups for deletion. Deleted backups:

- May 25, 2026 4:46 AM, slug `bfaa086a`, about 1.22 GB, local only.
- May 24, 2026 5:04 AM, slug `214444ad`, about 1.01 GB, local only.
- March 25, 2026 9:35 PM, slug `459efa58`, about 0.25 GB, local only.

Remaining backup coverage after deletion:

- May 29, 2026 5:02 AM, about 1.97 GB, local only.
- May 28, 2026 5:32 AM, about 1.78 GB, local only.
- May 27, 2026 5:29 AM, about 1.63 GB, local only.
- May 26, 2026 5:04 AM, about 1.43 GB local and about 1.43 GB cloud.

Important: the Recorder/logbook database was not deleted. A live helper-state
snapshot was saved under `.tmp/` before further diagnosis.

### Recorder Evidence

Current recorder config retained 30 days and excluded only a few signal-strength
patterns plus `sun.sun` and `weather.forecast_home`.

Live state surface showed:

- 1,899 total live states.
- 1,897 states were recorder candidates under the current include/exclude rules.
- Largest candidate domains by entity count:
  - `sensor`: 439 entities.
  - `binary_sensor`: 276 entities.
  - `switch`: 259 entities.
  - `automation`: 176 entities.
  - `script`: 156 entities.
  - `number`: 93 entities.
  - `input_datetime`: 92 entities.
  - `device_tracker`: 80 entities.
- Most active domains during the snapshot:
  - `sensor`: 104 recently reported in 15 minutes.
  - `automation`: 16 recently reported in 15 minutes.
  - `binary_sensor`: 10 recently reported in 15 minutes.
  - `camera`: 9 recently reported in 15 minutes.

Largest live attribute payloads included:

- `sensor.house_notice_timeline`
- `sensor.device_inventory_pending_digest`
- `sensor.garbage_recycling_schedule`
- `sensor.irrigation_schedule_summary`
- `sensor.wine_collection_snapshot`
- `sensor.house_notice_history`
- `sensor.irrigation_history_status`
- `sensor.metro_north_nwp_to_grand_central`

Interpretation: the 14 GB DB is likely caused by recording nearly everything
for 30 days across a large HA install, plus high-frequency telemetry and large
derived/template attributes. The live evidence does not yet prove exact
per-entity row counts; that requires a direct SQLite analysis of
`home-assistant_v2.db` from a shell or backup copy.

Recorder metadata over HA websocket reported:

- recording: true
- thread running: true
- backlog: 0
- migration in progress: false
- statistic IDs: 194

So Recorder was running at the moment of the check, but the database size and
recent history gaps still justify a targeted Recorder policy review.

### Latest Motion Evidence And Fix

The stale latest motion bar was not a Recorder-history issue. It was a source
coverage issue.

Live state showed the tracker still stored:

- label: Wynn's Room
- entity: `binary_sensor.wynn_s_room_person_detected`
- timestamp: June 1, 2026 11:36:51 PM

The automation only listened to this older set:

- `binary_sensor.g6_instant_motion`
- `binary_sensor.wynn_s_room_motion`
- `binary_sensor.wynn_s_room_person_detected`
- `binary_sensor.mud_room_motion`
- `binary_sensor.mud_room_person_detected`

Live HA had newer relevant camera/motion entities not covered by that map,
including:

- `binary_sensor.g6_instant_motion_2` / Front Yard Motion
- `binary_sensor.back_yard_person_detected` / Front Yard Person detected
- `binary_sensor.g6_instant_motion_3` / Garage Motion
- `binary_sensor.garage_person_detected` / Garage Person detected
- `binary_sensor.play_room_person_detected`
- `binary_sensor.mechanical_room_motion`
- `binary_sensor.mechanical_room_person_detected`

Fix applied:

- Expanded `automation.cameras_latest_motion_tracker` source map.
- Expanded the matching `calm-mobile` Latest Motion dashboard card source map
  and active icon list.
- Deployed only `automations/00-water-irrigation.yaml` and
  `dashboards/calm_mobile.yaml` through File Editor.
- Read-back hashes matched and HA config check returned valid.
- `automation.reload` succeeded.

### Wine Chart Evidence

The wine sensor was not dead.

Live state showed:

- `sensor.wine_temperature`: about 54.8°F and actively updating.
- `sensor.wine_humidity`: about 53-54% and actively updating.
- `sensor.wine_temperature_24h_stats`: available.
- `sensor.wine_humidity_24h_stats`: available.
- `sensor.wine_temp_24h_mean`: available.
- `sensor.wine_humidity_24h_mean`: available.

However, the 24-hour history API returned only a small recent slice:

- `sensor.wine_temperature`: 9 samples, beginning around 10:42 AM EDT.
- `sensor.wine_humidity`: 11 samples, beginning around 10:42 AM EDT.

The 24-hour statistics sensors also showed very low age coverage:

- age coverage ratio about 0.03.
- buffer usage ratio about 0.04.

Interpretation: current wine telemetry is healthy, but the 24-hour chart lacked
data because HA/Recorder only had a short recent history window available after
the recovery/storage pressure. This matches a Recorder/history continuity
problem more than a wine sensor or dashboard typo problem.

### Recorder Policy Guidance From This Follow-Up

Do not solve the 14 GB database by excluding broad domains blindly. History and
logbook records support stateful alerts, incident review, and safety logic.

Follow-up implemented: added `docs/recorder-inventory.md`,
`docs/recorder-inventory.json`, and `tools/generate_recorder_inventory.py` so
Recorder scope can be audited beside the device inventory. The first generated
inventory identified 1,944 Recorder candidates under the current config and 627
low stateful-need candidates for review. The first run used live-state recency
and attribute size; exact per-entity frequency remains pending until the tool is
run against a copied `home-assistant_v2.db`.

Recommended next Recorder slice:

- Keep event/security/motion history that supports alerts and postmortems.
- Reduce retention from 30 days only after confirming which dashboards and
  automations depend on 30-day raw history.
- Exclude derived summary sensors with large attributes when they are
  regenerated elsewhere or only used for current dashboard display.
- Exclude noisy infrastructure telemetry that is not operationally important
  as raw state history.
- Add direct SQLite row-count evidence before making aggressive exclusions.
- After policy changes, purge/repack only with a fresh backup and enough free
  disk space for the operation.

## Current Operational Guidance

### When HA Remote/Mobile Fails Again

1. Run the external probe from outside HA with the real Remote UI URL supplied
   through local environment, not committed config.
2. Compare these paths:
   - `/`
   - `/api/websocket`
   - `/ha-safe/home`
   - `/calm-mobile/home`
3. Interpret results using the UI hardening runbook:
   - TLS/connect fails: not a dashboard problem.
   - Nabu Casa fallback: remote service cannot reach local HA.
   - safe dashboard works but calm dashboard blanks: harden `calm-mobile`.
   - both dashboards work but app blanks: companion app cache/session issue.
4. Check Remote UI state and watchdog timestamps in HA.
5. Capture HA Core/Supervisor logs around the failure window before restarting.

### When Working On Casey Closet

- The controlling automation is `automation.lights_casey_s_closet_auto_off`.
- The light is `light.master_casey_s_closet`.
- The motion trigger is `binary_sensor.casey_s_closet_motion`.
- Current behavior is motion-on, then off after 3 quiet minutes.
- If snappiness is still not good enough, look for a faster physical trigger
  source rather than optimizing the automation YAML.

## Residual Risks And Follow-Ups

- Confirm Remote UI watchdog behavior during the next real outage.
- Run the external probe from a clean non-VPN/non-filtered path if possible.
- Refresh live HA registries and regenerate device inventory so docs stop
  carrying stale Casey closet entity names.
- If `/ha-safe/home` works while `/calm-mobile/home` fails, continue hardening:
  - Browser Mod/resource loading;
  - heavy dashboard first render;
  - custom card history fetch behavior;
  - cache-busting and stale resource versions.
- For Casey closet response time, test a door/contact sensor or faster local
  occupancy sensor as an additional early trigger.

## Decision Record

- Do not treat the mobile blank screen as "dashboard polish" until access-layer
  probes prove HA shell and websocket are reachable.
- Keep `/ha-safe/home` until the remote/mobile issue has been quiet for a
  sustained period.
- Keep config decomposition rules in `AGENTS.md`; do not recombine
  `sensors.yaml` or `lights.yaml` without a deliberate reason.
- Record future audits in `docs/audit-history/` and consult that history before
  forming a new incident theory.
