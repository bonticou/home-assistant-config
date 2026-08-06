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

No optimization changes were made in this audit. Recommended next slices:

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
   use broad domain purges.

6. **Review add-on/integration memory after privileged stats are available.**
   Matter Server, Browser Mod, HACS resources, UniFi Protect/Ring camera event
   surfaces, Spotify, and File Editor should be reviewed from stats/logs, not by
   disabling them speculatively.

## Deployment Status

No Home Assistant deployment was performed. No restart, reload, purge, repack,
vacuum, update, or config write was initiated.

This audit entry is the only intended repo change from this pass.

## Residual Risks And Follow-Ups

- Add-on stats and Supervisor/Core metadata endpoints were not available from
  the current authenticated session.
- No exact DB row counts were captured because no current copied Recorder DB was
  available locally.
- The current Core log is post-restart; previous-Core causal logs may already
  have rotated. Future recurrence capture should prioritize Supervisor logs,
  host logs, previous Core logs, and DB/WAL status before they age out.
- Memory peak near `1G` may indicate a container limit, normal peak reporting,
  or true pressure. It should not be treated as OOM without OOM-kill evidence.
