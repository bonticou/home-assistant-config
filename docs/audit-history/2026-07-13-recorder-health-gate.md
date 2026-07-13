# Recorder Health Gate After Cleanup

## Symptom And Purpose

After the first Recorder cleanup slices and the unused Climate tab removal, the
next question was whether Home Assistant is healthy enough to continue snappiness
and bloat work.

This health gate was read-only. No config changes, purge, repack, restart, or
reload was performed.

## Context Reviewed

- `docs/audit-history/README.md`
- `docs/audit-history/2026-07-13-recorder-pressure-follow-up.md`
- `docs/audit-history/2026-07-13-recorder-config-control-slice.md`
- `docs/home-assistant-remote-access-runbook.md`
- `docs/home-assistant-ui-hardening-runbook.md`
- `docs/recorder-inventory.md`

## Evidence Collected

Captured on 2026-07-13 around 2:06-2:08 PM America/New_York from the connected
Home Assistant frontend and bounded File Editor read-only shell commands.

Recorder websocket status:

- `recording`: `true`
- `thread_running`: `true`
- `backlog`: `0`
- `migration_in_progress`: `false`
- `migration_is_live`: `false`
- `db_in_default_location`: `true`
- long-term statistic IDs exposed: `206`

Remote/access status:

- frontend connected: `true`
- Core state: `RUNNING`
- `binary_sensor.remote_ui`: `on`
- `sensor.home_assistant_remote_access_status`: `online`
- last Remote UI degraded timestamp: `2026-07-11 05:20:03`
- last Remote UI recovery attempt: `2026-07-12 04:42:46`
- last Remote UI restored timestamp: `2026-07-12 04:45:35`
- `sensor.bonticou_gateway_state`: `connected`
- `binary_sensor.fios_router_wan_status`: `unavailable`

Database and disk status:

| Measurement | Value |
| --- | ---: |
| `home-assistant_v2.db` bytes | `20,462,624,768` |
| WAL bytes | `17,233,992` |
| SQLite free-list bytes | `7,867,670,528` |
| SQLite used bytes estimate | `12,594,954,240` |
| `/homeassistant` free bytes | `890,937,749,504` |
| `/homeassistant` total bytes | `984,434,429,952` |

Recent log tails:

- No Recorder/SQLite/database lines in the last filtered log tail.
- No cloud/Nabu/Remote UI/websocket/timeout lines in the last filtered log tail.

## Findings

1. **Recorder is currently healthy. Confidence: high.**
   Backlog is `0`, recording is active, the Recorder thread is running, and no
   migration is in progress. The system is not currently digesting the prior
   purge/repack work.

2. **The data disk is not capacity-constrained. Confidence: high.**
   `/homeassistant` has about `890.9 GB` free. Current incidents should not be
   treated as simple out-of-disk failures.

3. **The SQLite database still contains large reclaimable space. Confidence:
   high.** The DB file remains about `20.46 GB`, but the free-list is now about
   `7.87 GB`. This is higher than the prior post-cleanup `7.59 GB` reading,
   meaning HA-supported cleanup continued to show up inside SQLite even though
   the file did not shrink on disk.

4. **Remote UI is currently healthy, but WAN telemetry is imperfect.
   Confidence: medium-high.** Remote UI is online and the gateway reports
   connected, but the Fios WAN binary sensor is unavailable. Future outage
   reviews should not rely on that binary sensor alone.

5. **The next cleanup should be measurement, not another blind purge.
   Confidence: high.** Because Recorder is healthy and disk is ample, the next
   best step is to collect DB-backed top-writer row counts before deciding which
   entities to shorten, exclude, or purge.

## Decision

Proceed to DB-backed Recorder writer inventory/top-row-count measurement.

Do not run another purge, repack, restart, or direct SQLite vacuum as part of
this health gate.

## Recommended Follow-Up

1. Collect bounded DB row-count stats from the live HA host or from an
   off-device copy of `home-assistant_v2.db`.
2. Regenerate `docs/recorder-inventory.json` and
   `docs/recorder-inventory.md` using those DB stats.
3. Rank the largest actual writers before the next Recorder exclusion/purge
   slice.
4. Keep `sensor.house_notice_history` recorded until Notification Center memory
   is migrated to a durable sidecar ledger.
5. Treat SQLite file-size reclamation as a separate maintenance window with
   backup and quiet HA conditions.
