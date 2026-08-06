# Core Watchdog Restarts And Memory Pressure

Date: 2026-08-05

## Symptom And Impact

Home Assistant was again restarting too frequently. The operational impact was
availability: mobile/browser access could load the Home Assistant shell or
Remote UI route, but fresh state sometimes did not attach, and Core was being
restarted by Supervisor during the evening.

The audit goal was optimization, not rewriting. Existing household rules,
notification semantics, stateful alert memory, logbook meaning, and visible data
displays were treated as preserved unless later evidence justifies a tightly
scoped optimization.

## Relevant Prior Context

Reviewed before forming a fresh theory:

- `docs/audit-history/README.md`
- `docs/home-assistant-availability-investigation.md`
- `docs/audit-history/2026-08-02-unexpected-core-restart-during-tesla-setup.md`
- `docs/audit-history/2026-07-13-recorder-health-gate.md`
- `docs/audit-history/2026-07-13-recorder-pressure-follow-up.md`
- `docs/recorder-inventory.md`

Important inherited findings:

- The 2026-08-02 outage already confirmed an unclean Core termination.
- Prior Recorder cleanup deliberately avoided excluding
  `sensor.house_notice_history` because it still carries stateful notification
  history in template attributes.
- The previous health gate showed Recorder backlog `0`, ample disk, and a large
  SQLite database with significant free-list space. It recommended DB-backed
  top-writer measurement before another purge.

## Evidence Collected

Live checks were read-only. No config, Recorder, add-on, or dashboard changes
were made.

### Remote And Frontend Path

- Python and Node terminal probes both hit the known local certificate-chain
  validation failure against the Nabu Casa route from this Mac. This is treated
  as a local probe limitation, not proof that HA was down.
- With certificate verification bypassed for unauthenticated route testing only:
  - `/`, `/ha-safe/home`, and `/calm-mobile/home` returned HTTP `200`;
  - the Nabu fallback text was not detected;
  - `/api/websocket` returned the Home Assistant `auth_required` greeting;
  - the websocket greeting reported Core `2026.7.1`.
- The in-app browser loaded `/ha-safe/home`, completed the HA shell title, and
  loaded global Lovelace resources, but `hass.connected` stayed false for about
  30 seconds. Because this happened on the stock safe dashboard, the immediate
  symptom is not specific to `calm-mobile`.

### Live HA State

Authenticated Home Assistant API state at about 10:14 PM EDT:

- Core config state: `RUNNING`
- Core version: `2026.7.1`
- state count: `2100`
- `binary_sensor.remote_ui`: `on`
- `sensor.home_assistant_remote_access_status`: `online`
- Recorder websocket info:
  - `recording`: `true`
  - `thread_running`: `true`
  - `backlog`: `0`
  - `migration_in_progress`: `false`
  - `db_in_default_location`: `true`

Available update state at capture time:

- Core update available: installed `2026.7.1`, latest `2026.8.0`
- OS update available: installed `18.1`, latest `18.2`
- Matter Server update available: installed `9.0.4`, latest `9.1.1`
- File Editor update available: installed `6.0.0`, latest `6.1.0`
- Browser Mod update available: installed `3.0.2`, latest `3.2.0`
- Mushroom update available: installed `5.1.1`, latest `5.2.2`
- Sonos Card update available: installed `10.2.1`, latest `10.7.1`

Supervisor info/stats/add-on endpoints returned `401` from the available
session, so add-on memory/stats were not captured in this pass.

### Restart Timeline

Supervisor logs show three confirmed watchdog restarts in the available evening
log window:

| Watchdog Warning | Restart Ordered | Core Running Again | Approx Recovery |
| --- | --- | --- | ---: |
| 2026-08-05 20:33:11 EDT | 2026-08-05 20:35:42 EDT | 2026-08-05 20:42:22 EDT | ~6m 40s |
| 2026-08-05 21:10:53 EDT | 2026-08-05 21:13:24 EDT | 2026-08-05 21:20:02 EDT | ~6m 38s |
| 2026-08-05 21:58:49 EDT | 2026-08-05 22:01:20 EDT | 2026-08-05 22:08:00 EDT | ~6m 40s |

The repeated Supervisor message was:

```text
Watchdog missed 2 Home Assistant Core API responses in a row. Restarting Home Assistant Core!
```

This classifies the incident as Supervisor restarting Core because Core stopped
responding to the Supervisor API watchdog. It is not a normal manual restart and
not a pure Nabu Casa remote-access outage.

### Host And Core Logs

Host logs show repeated Home Assistant container terminations with memory peaks
around `1G` or `1000-1009M` before cleanup/restart. No explicit `OOM killed`
line was captured in the available filtered log output.

The current post-restart Core log showed:

- repeated `Already running` warnings for:
  - `Security - Clear Casey Left Lights Alert`
  - `Security - Clear Casey Left Combo Alert`
- repeated Recorder warnings that `sensor.house_notice_history` attributes
  exceed Home Assistant's `16384` byte Recorder attribute limit;
- one Spotify coordinator fetch error;
- several invalid-auth warnings from this audit's expired-token attempts after
  the system was already back online.

The invalid-auth warnings were generated after the restart window during this
audit and are not causal.

### Recorder Inventory

A temporary static Recorder inventory was generated outside the repo:

- entities reviewed: `2512`
- Recorder candidates: `1701`
- excluded by Recorder config: `443`
- disabled in registry: `368`
- low stateful-need candidates: `307`
- medium stateful-need candidates: `504`
- high stateful-need candidates: `506`

No current off-device `home-assistant_v2.db` copy was found under the checked
repo/backups/Downloads paths, so exact DB-backed row counts remain missing.

## Ranked Findings

1. **Confirmed: Supervisor watchdog is restarting Core. Confidence: high.**
   Three evening restarts were directly logged after missed Core API responses.
   This is the strongest current explanation for the user's recurring
   disconnects.

2. **Core is becoming unresponsive before restart. Confidence: high.**
   Supervisor waits for Core to recover for roughly six to seven minutes after
   each restart. That matches the user-facing pattern of HA being unavailable
   for minutes, then returning.

3. **Memory/load pressure is plausible but not proven as OOM. Confidence:
   medium.** Host logs show repeated Core container memory peaks around `1G`,
   but the available log slice did not contain an `OOM killed` marker. Treat
   this as load-pressure evidence, not a completed OOM diagnosis.

4. **Recorder is healthy after recovery but remains an optimization target.
   Confidence: medium-high.** Recorder backlog was `0` and no migration was
   running after recovery. However, the state surface is large, Recorder still
   retains 30 days, and exact top-writer row counts remain the key missing
   evidence before any purge.

5. **`sensor.house_notice_history` is still a known architectural hotspot.
   Confidence: high.** It is repeatedly too large for Recorder attributes.
   Because it preserves notification memory, it should not simply be excluded
   from Recorder; the safe optimization is to move that state to a durable
   sidecar ledger and keep the visible Notification Center behavior intact.

6. **The Casey-left clear-alert path is a possible post-restart load/noise
   contributor. Confidence: medium.** The repeated `Already running` warnings
   occur after restart and indicate duplicate clear attempts. The household
   behavior should not be changed, but the implementation can likely be made
   idempotent/quiet later so duplicate clear events do less work.

7. **Frontend/dashboard load is not the lead restart cause. Confidence:
   medium-high.** The safe dashboard also stalled at `hass.connected=false`, and
   Supervisor independently logged Core watchdog restarts. Frontend lazy-loading
   still helps snappiness, but it does not explain Supervisor restarting Core.

## Safe Optimization Plan

The initial audit made no live optimization changes. A follow-up DB-backed
slice was run later the same evening and identified one safe Recorder
optimization to prepare first. Recommended next slices:

1. **Capture DB-backed Recorder writer stats before purging.** Obtain an
   off-device DB copy or a small HA-host DB stats JSON and run
   `tools/generate_recorder_inventory.py --db` or `--db-stats-json`.

2. **Move notification history out of `sensor.house_notice_history`
   attributes.** Preserve the Notification Center and past-state behavior, but
   store the event ledger in a sidecar file or equivalent durable store so the
   template sensor no longer emits oversized attributes.

3. **Make duplicate notification clear paths idempotent without changing
   outcomes.** Focus on the Casey-left clear-alert warnings first. The intended
   behavior remains "clear the same notification tags"; the optimization is to
   avoid repeated overlapping service calls after a restart/state storm.

4. **Add restart breadcrumbs and preserve previous-Core evidence.** Enable a
   durable previous-Core log or lightweight breadcrumb sensors for Core start,
   Supervisor watchdog restart time, and host/container restart metadata during
   a maintenance window.

5. **Only after DB evidence, purge exact low-value entities.** Candidate classes
   remain generated dashboard summaries, config/update diagnostics, event
   entities that do not drive automations, and stale removed entities. Do not
   use broad domain purges. The first DB-backed exact candidates are recorded
   below.

6. **Review add-on/integration memory after privileged stats are available.**
   Matter Server, Browser Mod, HACS resources, UniFi Protect/Ring camera event
   surfaces, Spotify, and File Editor should be reviewed from stats/logs, not by
   disabling them speculatively.

## Follow-Up Recorder Evidence And First Config Slice

After the initial watchdog audit, a bounded Recorder database investigation was
run from the live HA host.

Broad all-entity grouping against the full database was intentionally aborted
after roughly 211 seconds. That reinforced the existing rule: do not run broad
live SQLite scans through File Editor during an availability incident.

A narrower targeted scan of 313 low-stateful-need/current-only candidates
completed in roughly 52 seconds and found `14,113,858` rows. The largest
writers in that targeted set were:

| Entity | Existing rows | Last 24h rows | Last 7d rows | Approx rows/day | Assessment |
| --- | ---: | ---: | ---: | ---: | --- |
| `sensor.ting_notification_status` | 12,079,671 | 361,679 | 2,681,884 | 388,600 | Template-derived live alert context, not durable alert memory |
| `sensor.bonticou_gateway_cpu_utilization_2` | 330,013 | 10,817 | 74,722 | 10,617 | UniFi diagnostic telemetry; no repo automations/scripts/dashboards consume it |
| `sensor.bonticou_gateway_memory_utilization_2` | 298,850 | 9,733 | 67,339 | 9,614 | UniFi diagnostic telemetry; no repo automations/scripts/dashboards consume it |

`sensor.ting_notification_status` remains important live state. It feeds Ting
notification copy and Notification Center context. Its durable notification
memory, however, is stored in explicit `input_datetime` and `input_boolean`
helpers such as the Ting last-sent timestamps and active flags. Recording every
recomputed Ting status/attribute change for 30 days is therefore the wrong
storage shape. If short Ting history becomes useful later, it should be a
compact deliberate event ledger, not millions of raw Recorder rows.

Prepared and deployed config change:

- added exact Recorder exclusions for the three entities above;
- did not exclude `sensor.house_notice_history`, because it is still tied to
  stateful notification memory and needs a more careful sidecar-ledger
  redesign before Recorder history is changed;
- did not change global `purge_keep_days`;
- did not add broad domain or glob exclusions;
- regenerated `docs/recorder-inventory.json` and
  `docs/recorder-inventory.md`.

Expected future write reduction after the change is deployed and HA restarts:
roughly `408,800` rows/day based on the targeted seven-day rates above. Existing
database size will not materially shrink until an exact purge and any later
SQLite repack/vacuum are performed.

Additional DB size evidence captured before this slice:

| Item | Value |
| --- | ---: |
| Recorder DB file | 20,462,624,768 bytes |
| WAL file | 20,830,752 bytes |
| SQLite freelist | 2,426,698 pages |
| Estimated freelist bytes | 9,939,755,008 bytes |
| Estimated used bytes | 10,522,869,760 bytes |

The large freelist means prior purges already created reclaimable empty pages
inside the database file. Vacuum/repack may recover disk space, but it remains
separate maintenance work requiring a quiet window and a verified backup.

## Live Deployment And Purge Attempt

On 2026-08-05 at roughly 10:49 PM EDT, after the Remote UI recovered, the
prepared Recorder exclusion slice was deployed through the authenticated
Safari/Nabu Casa tab using a fresh Supervisor File Editor ingress session.

Deployment evidence:

- `/homeassistant/configuration.yaml` was written and read back with SHA-256
  `ca3619bf313c5e6aff2fcea990a8bdb1c41549d494ee00e8009d9756f46bd3df`.
- Home Assistant config check returned `valid` with no warnings or errors.
- Core restart was accepted at 10:50 PM EDT.
- Fresh local HTTP returned around 10:51:55 PM EDT.
- Post-restart authenticated HA check showed Core `RUNNING`, HA version
  `2026.7.1`, Recorder recording, and Recorder thread running.
- Live file verification showed the exact exclusions present at
  `/homeassistant/configuration.yaml` lines 1363, 1364, and 1374.

Exact pre-purge counts after restart:

| Entity | Rows |
| --- | ---: |
| `sensor.ting_notification_status` | 12,084,988 |
| `sensor.bonticou_gateway_cpu_utilization_2` | 330,091 |
| `sensor.bonticou_gateway_memory_utilization_2` | 298,921 |
| **Total** | **12,714,000** |

`recorder.purge_entities` was then called using only those exact entities and
`keep_days: 0`. Calls were accepted using both entity-list and target-style
service invocation. The safe service path did not clear the full history during
the observed window, but it did make partial progress.

Final observed counts at roughly 11:00 PM EDT:

| Entity | Rows After | Rows Cleared |
| --- | ---: | ---: |
| `sensor.ting_notification_status` | 12,060,988 | 24,000 |
| `sensor.bonticou_gateway_cpu_utilization_2` | 226,091 | 104,000 |
| `sensor.bonticou_gateway_memory_utilization_2` | 298,921 | 0 |
| **Total** | **12,586,000** | **128,000** |

Storage impact from the observed purge window:

| Metric | Before Purge | After Observed Purge | Change |
| --- | ---: | ---: | ---: |
| DB file | 20,462,624,768 bytes | 20,462,624,768 bytes | 0 bytes |
| WAL file | 20,876,072 bytes | 76,516,672 bytes | +55,640,600 bytes |
| SQLite freelist | 9,932,804,096 bytes | 9,938,292,736 bytes | +5,488,640 bytes |
| Estimated used bytes | 10,529,820,672 bytes | 10,524,332,032 bytes | -5,488,640 bytes |

Interpretation: the important reliability win is future-write prevention,
expected at roughly `408,800` fewer state rows/day. Immediate disk capacity did
not improve because the database file was not repacked/vacuumed, and the purge
service only cleared a small fraction of historical rows during the safe
observation window. Manual SQLite deletion was deliberately not attempted.

## Second Prevention-Only Recorder Slice

A follow-up prevention-only slice added exact Recorder exclusions for additional
current-only summary sensors and unused UniFi diagnostics:

- `sensor.away_security_entry_point_issues`
- `sensor.downstairs_climate_insight`
- `sensor.environment_attic_status`
- `sensor.environment_basement_status`
- `sensor.environment_dining_room_status`
- `sensor.environment_garage_status`
- `sensor.environment_house_status`
- `sensor.environment_kitchen_status`
- `sensor.environment_main_floor_status`
- `sensor.environment_office_status`
- `sensor.environment_primary_bedroom_status`
- `sensor.environment_second_floor_status`
- `sensor.irrigation_dashboard_status`
- `sensor.irrigation_focus_zone_detail`
- `sensor.irrigation_running_context`
- `sensor.irrigation_zone_attention_summary`
- `sensor.u7_pro_family_room_cpu_utilization`
- `sensor.usw_flex_2_5g_5_cpu_utilization`

Rationale:

- The environment, irrigation, climate, and away-security entities are
  template-derived summary/current-context sensors used by dashboards,
  notification copy, startup refreshes, and live alert decisions.
- The durable state for notifications remains in the explicit
  `input_datetime`, `input_boolean`, and action-helper entities, not in the raw
  Recorder history of these summary sensors.
- The UniFi AP/switch CPU sensors are diagnostics with no repo automation,
  script, dashboard, or custom-card consumer found.
- Wine humidity/dew-point entities and `sensor.irrigation_flow_rate` were
  deliberately kept recorded because they represent physical/trend data used by
  wine or water/flow behavior.

The measured top-writer subset of this slice accounts for at least roughly
`16,600` additional rows/day avoided. The true future-write reduction is higher
because several related environment summary sensors were excluded even though
they were below the top-20 printout.

This slice is prevention-only. No historical purge was attempted for these
entities because the first exact purge had only partially progressed and the
safe maintenance rule is to avoid stacking heavy database work during an
availability recovery.

## Widened Low-Stakes No-Reference Recorder Slice

The scope was then widened using a stricter user-facing rule: exclude only data
that is not incorporated in rule sets, calculations, dashboards, custom cards,
or notice-building code. A repository reference scan was run across
`configuration.yaml`, `scripts.yaml`, `scenes.yaml`, `sensors.yaml`,
`lights.yaml`, `automations/`, `dashboards/`, and `www/`.

This identified `113` additional exact low-stakes Recorder candidates. They
fall into three classes:

- infrastructure diagnostics, such as UniFi CPU/memory/uptime, Protect camera
  disk-write/storage, gateway storage, and router/upload/client diagnostics;
- signal-quality diagnostics, such as Wi-Fi or lamp signal levels;
- integration configuration toggles, such as Sonos autoplay/loudness settings,
  Ring/Protect "motion detection enabled" settings, HomeKit audio settings, and
  device LED/auto-update toggles.

These are useful as live Home Assistant states, but the repo has no automation,
script, calculation, dashboard, custom-card, or notice consumer that needs their
30-day Recorder history.

Deliberately not excluded in this widened slice:

- automations, scripts, and helpers, because their history supports "when did
  this last fire" debugging and durable notification state;
- Ring/Protect motion, ding, person, vehicle, and camera event entities,
  because they can be meaningful security or incident history;
- water, irrigation flow, leak, valve, climate, radon, wine, and other physical
  time-series entities;
- notification ledgers and action-stamp history, including
  `sensor.house_notice_history` and `sensor.house_action_stamp_ledger`;
- derived calculation outputs where the state itself is part of a household
  decision model rather than pure infrastructure/config noise.

After regenerating the inventory, Recorder candidates fell from `1680` to
`1567`, excluded-by-config entities rose from `464` to `577`, and low
stateful-need candidates fell from `286` to `173`.

## Deployment Status

Initial audit: no Home Assistant deployment was performed. No restart, reload,
purge, repack, vacuum, update, or config write was initiated.

Follow-up Recorder slice, first attempt: repo files were updated, but live
deployment was deferred because the deploy surface was unhealthy:

- Nabu Casa Remote UI probe reached TCP, but TLS handshakes timed out for `/`,
  `/ha-safe/home`, `/calm-mobile/home`, and `/api/websocket`.
- Local `homeassistant.local:8123` probe reached TCP, but fresh HTTP and
  websocket requests timed out.
- The browser/File Editor route showed the HA shell but did not reach a
  connected File Editor ingress surface suitable for write/read-back.

No live config write, restart, purge, repack, or vacuum was performed during
that bad connectivity window.

Follow-up Recorder slice, second attempt: live deployment completed after the
Remote UI recovered. Core was restarted after a valid config check. Exact
purge was attempted through HA's Recorder service and partially progressed. No
manual SQLite deletes, repack, vacuum, broad purge, or retention change was
performed.

Widened low-stakes no-reference slice: live deployment completed through the
authenticated Nabu Casa/File Editor route. `/homeassistant/configuration.yaml`
was written and read back successfully, Home Assistant reported a valid config,
and Core was restarted so Recorder would load the new exclusions. Post-restart
health showed:

- Core state: `RUNNING`
- Core version: `2026.7.1`
- Remote UI: `on`
- remote access status: `online`
- Recorder: recording `true`, thread running `true`, backlog `0`, migration
  not in progress

No historical purge, SQLite repack, vacuum, broad purge, retention change, or
manual database edit was performed for this widened slice. The immediate
storage freed by this specific slice is therefore expected to be essentially
zero; the benefit is reduced future Recorder write volume and lower ongoing DB
churn.


## Exact Recorder Purge And Supported Repack Attempt

Annotation-driven maintenance was run after the widened Recorder exclusions were
live. The goal was to reclaim safe low-stakes history without changing rules,
notifications, dashboards, helpers, or physical trend data.

Actions performed through the authenticated Home Assistant frontend:

- called `recorder.purge_entities` with the exact `152` entity IDs currently in
  `recorder.exclude.entities`;
- called HA-supported `recorder.purge` with `keep_days: 30`, `apply_filter:
  true`, and `repack: true`;
- did not call a broad domain purge;
- did not reduce global retention;
- did not manually delete SQLite rows;
- did not run direct SQLite `VACUUM` against the live database.

Health after the service calls:

- HA frontend connected: `true`
- Remote UI: `on`
- remote access status: `online`
- Recorder: recording `true`, thread running `true`, migration not in progress
- Recorder backlog: `200` against a `65,000` max backlog
- Core memory: about `989 MB` of a `4.11 GB` limit (`24.06%`)
- Host disk: about `808.2 GB` free, `71.4 GB` used, `916.8 GB` total

Storage result: the supported purge/repack path did not visibly reduce host disk
usage during the observation window. This is consistent with earlier Recorder
maintenance: HA can remove rows and create reclaimable SQLite free pages without
immediately shrinking the physical DB file. A direct SQLite vacuum may reclaim
more space, but it is a separate higher-risk maintenance operation because it
can lock or rewrite the live database. It should only be considered with a fresh
off-device backup, a quiet window, and a plan to stop HA or otherwise guarantee
Recorder is not writing.

## Residual Risks And Follow-Ups

- Add-on stats and Supervisor/Core metadata endpoints were not available from
  the current authenticated session.
- Exact row counts were captured only for the targeted low-stateful-need
  candidate set, not for every entity in the full database.
- The current Core log is post-restart; previous-Core causal logs may already
  have rotated. Future recurrence capture should prioritize Supervisor logs,
  host logs, previous Core logs, and DB/WAL status before they age out.
- Memory peak near `1G` may indicate a container limit, normal peak reporting,
  or true pressure. It should not be treated as OOM without OOM-kill evidence.
- The Recorder exclusions are now live, but historical rows for the three target
  entities mostly remain. Future cleanup should use HA service behavior,
  backups, and a quiet maintenance window; do not hand-edit SQLite rows.
- Final Recorder health showed HA connected and `RUNNING`; Recorder was
  recording with thread running, migration not in progress, and backlog `167`.
