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
