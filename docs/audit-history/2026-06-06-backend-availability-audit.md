# Home Assistant Backend Availability Audit

Date: 2026-06-06

## Symptom And User Impact

Home Assistant has shown an intermittent backend availability problem that
predates the USB SSD migration. The visible pattern is that the frontend may
partially load or appear connected while fresh API, websocket, or service-call
paths are degraded. During affected windows, state can look stale, service
calls may hang or fail, and automations may not execute reliably.

The SSD migration appears to have improved general responsiveness, but it has
not fully resolved the underlying availability concern. This audit treats
room-specific automation misses as downstream evidence only; the primary
question is whether Home Assistant Core, Supervisor, storage, Recorder, add-ons,
network paths, or frontend sessions are degrading.

## Relevant Prior Context

- The 2026-06-04 availability and UI hardening audit found remote/mobile access
  failures that occurred before dashboard code was loaded, making a pure
  Lovelace failure unlikely.
- The 2026-06-04 transient app-layer stall and remote UI/fresh HTTP stall
  entries recorded a pattern where existing websocket sessions could remain
  usable while fresh HTTP, TLS, or remote UI requests failed.
- The 2026-06-06 SSD migration note recorded post-migration flapping in fresh
  local probes and documented the new data-disk storage breakdown.
- The remote-access runbook already separates Remote UI health from local Core
  health and uses the Remote UI watchdog helpers as durable breadcrumbs.

## Evidence Collected

### Current Local Baseline

Read-only probes were run against the local Home Assistant host, the safe
dashboard, the calm mobile dashboard, the storage page, and websocket.

- `tools/ha_remote_health_probe.py --url http://<local-ha-ip>:8123 ...`
  at `2026-06-06T21:19:41Z`: `status: ok`.
- The same probe confirmed HTTP 200 for `/`, `/manifest.json`,
  `/ha-safe/home`, `/calm-mobile/home`, and `/config/storage`.
- The probe's websocket check reached `auth_required` and reported Home
  Assistant `2026.3.4`.
- `tools/ha_remote_health_probe.py --url http://homeassistant.local:8123 ...`
  at `2026-06-06T21:24:35Z`: `status: ok`, including websocket
  `auth_required`.
- Direct local TCP checks to Home Assistant Core and Observer ports succeeded.

Safari was then used as an independent frontend/API comparison:

- `hass.connected`: `true`.
- `GET config`: Core state `RUNNING`, Home Assistant `2026.3.4`,
  `safe_mode: false`, `recovery_mode: false`.
- Websocket `get_states`: 1769 states returned.

### Storage And Data Disk

The Storage page showed the SSD as the active large data disk and did not show
rapid Home Assistant data growth during this pass:

- Used: 61.2 GB of 916.8 GB.
- System: 43.5 GB.
- Home Assistant: 13.9 GB.
- Backups: 3.9 GB.
- App data: 0 GB.
- Free space: 855.6 GB.

This matches the earlier post-migration value closely enough that the `60 GB
used` number is not evidence of day-one Home Assistant runaway growth by
itself. Most used space is attributed to the System bucket.

### Remote UI And Network Helpers

The local Remote UI status helper currently reported online status, but it also
captured a real earlier degraded/restored cycle:

- Remote UI helper state: online.
- `binary_sensor.remote_ui`: on.
- Last recovery attempt: 2026-06-06 16:26:36 local time.
- Last degraded at: 2026-06-06 02:44:12 local time.
- Last restored at: 2026-06-06 14:04:00 local time.
- Watchdog status: called `cloud.remote_connect` because Remote UI was off.
- Degraded notice active: off.
- Gateway state: connected.
- WAN status sensor: unavailable.

The remote/Nabu Casa probe was inconclusive in this pass. DNS/TCP succeeded in
one local Python probe, but the TLS verifier failed on the certificate chain.
A separate command-line remote request then showed DNS resolution variance.
Because the local frontend and local hostname probes were healthy at the same
time, this does not prove Core was down. It does show that remote-path
monitoring should be evaluated separately from local Core health.

### Probe-Path Finding

A key finding from this pass is that raw-IP websocket probes can produce false
availability signals in this environment.

During one follow-up check, a raw-IP probe received HTTP 200 responses but the
websocket portion timed out. At the same time:

- Direct raw-IP HTTP received a live Home Assistant response.
- Safari `GET config` and websocket `get_states` succeeded.
- A fresh browser websocket to `homeassistant.local` succeeded immediately.
- A fresh browser websocket to the raw IP timed out.
- A hostname-based probe to `homeassistant.local` succeeded end-to-end.

That means a raw-IP websocket timeout should not be treated as definitive proof
that Home Assistant Core is down unless the hostname/browser path also fails.
Future availability checks should prefer `homeassistant.local` for local
websocket reachability and record raw-IP behavior separately.

### Core, Supervisor, Host, And Add-On Logs

Core logs contained several noisy or potentially expensive signals:

- Repeated UniFi Protect snapshot 500 retry warnings against camera snapshot
  endpoints.
- Recorder warnings that attributes for these sensors exceeded the 16 KB
  Recorder attribute limit:
  - `sensor.irrigation_history_status`
  - `sensor.device_inventory_pending_digest`
  - `sensor.house_notice_history`
- A recurring command-line failure from the irrigation fingerprint status tool,
  including an empty reply where JSON was expected.
- Whisker/Ting websocket stale/disconnect messages followed by reconnects.

Supervisor logs showed a normal host/Core startup sequence after the approved
host reboot:

- Supervisor initiated Core start.
- Core transitioned through `NOT_RUNNING`, `STARTING`, and then `RUNNING`.
- Supervisor later reported itself up and running.

Supervisor also reported:

- No issue found for multiple data disks, disabled data disk, or disk lifetime.
- Only two backup files found.
- A `no_current_backup` system issue and suggestion to create a full backup.

Host logs reviewed in this pass did not show an obvious out-of-memory event,
kernel panic, or host crash signature in the retained excerpt.

Installed add-on logs reviewed:

- File Editor: regular ingress polling and normal restart around the host
  reboot; no restart loop found.
- Terminal & SSH: SSH service disabled by configuration and normal restart
  messages; no restart loop found.
- Matter Server: several pre-reboot websocket no-PONG warnings, then clean
  shutdown/restart and successful subscription initialization.

### Backup State

Backup state is a concrete reliability concern independent of the frontend
symptoms:

- Supervisor raised `no_current_backup`.
- Only two backup files were found.
- The last successful automatic backup sensor reported 2026-05-26.
- The last attempted automatic backup sensor reported 2026-06-05.
- The automatic backup event still showed `in_progress` at upload stage while
  the backup manager state was idle.

This should be corrected after the current availability audit window, because
changes such as Core upgrades, Recorder work, or add-on remediation should not
proceed without a current backup.

### Recorder And Database Risk

Static Recorder configuration review:

- `recorder:` keeps 30 days.
- Current exclusions are narrow and mostly cover signal/RSSI/link-quality
  style entities plus weather/sun.

A fresh static recorder inventory was generated into scratch output:

- Recorder candidates: 1765.
- Low stateful-need candidates: 594.
- Database row counts: unavailable because no copied `home-assistant_v2.db`
  was present in the repo workspace.

The static inventory and Core warnings make Recorder pressure plausible, but
not yet proven as the cause of backend stalls. The oversized attribute sensors
are the most concrete Recorder cleanup candidates because Home Assistant is
already warning that their attributes are too large to store.

## Ranked Findings

1. **Raw-IP websocket probes are not a reliable local health signal by
   themselves. Confidence: high.** Hostname/browser websocket checks succeeded
   while raw-IP websocket checks timed out, even though raw-IP HTTP returned a
   live Home Assistant response.

2. **Current local Core health was good during the audit window. Confidence:
   high.** Fresh hostname probes, Safari API calls, and Safari websocket calls
   all confirmed Core `RUNNING`, 1769 live states, and no safe/recovery mode.

3. **The historical backend/remote instability remains real but was not fully
   reproduced during this pass. Confidence: medium-high.** Prior audits and the
   Remote UI helper timestamps show degraded windows, but current evidence did
   not show an active Core crash or Supervisor loop.

4. **Backup protection is stale or incomplete. Confidence: high.** Supervisor
   raised `no_current_backup`, only two backup files were found, and backup
   helper states disagree about the latest attempted/successful automatic
   backup.

5. **Recorder/log pressure is a plausible contributor but not proven. Confidence:
   medium.** There are 1765 recorder candidates, 594 low stateful-need
   candidates, 30-day retention, and live warnings for oversized attributes.
   A database copy is needed before ranking high-frequency row writers.

6. **UniFi Protect snapshot retry noise is a plausible integration pressure
   source. Confidence: medium.** Core logs show repeated snapshot 500 retries.
   This deserves follow-up if it continues, but it was not proven to block Core.

7. **Storage capacity is unlikely to be the immediate root cause. Confidence:
   medium-high.** Free space is ample, the SSD is active, and the used-space
   breakdown is stable across checks.

8. **Installed add-ons reviewed in this pass are unlikely to be the primary
   cause. Confidence: medium-high.** File Editor, Terminal & SSH, and Matter
   Server did not show restart loops. Matter had stale websocket warnings before
   reboot, but restarted cleanly.

## Changes Made

- Added this audit entry.
- Updated the audit-history index.
- No live Home Assistant configuration was changed.
- No add-ons were disabled or restarted during this audit pass.
- No Recorder purge or exclusion changes were made.
- No Home Assistant restart, reload, or reboot was performed during this audit
  pass.

## Checks And Live Validation

- Ran local HTTP, dashboard, storage-page, and websocket probes.
- Compared CLI probe results against fresh Safari frontend API and websocket
  calls.
- Checked local Remote UI helper states separately from local Core health.
- Pulled Core, Supervisor, host, and installed add-on logs through authenticated
  frontend APIs.
- Reviewed `recorder:` YAML and generated a static recorder inventory.
- Reviewed storage buckets on the live Storage page.

## Recommended Smallest Safe Next Step

Do not implement Recorder exclusions, add-on remediation, or Core upgrades as
the first response to this evidence. The smallest safe reliability change is to
fix the monitoring/probe path:

1. Prefer `homeassistant.local` for local websocket probes.
2. Keep raw-IP HTTP/websocket probes as a comparison path, but mark raw-IP
   websocket-only failures as probe-path suspect unless hostname/browser probes
   also fail.
3. Add a durable health snapshot that records local hostname HTTP, local
   hostname websocket, raw-IP HTTP, raw-IP websocket, Remote UI helper state,
   and Core state in one timestamped row.
4. Require several consecutive failing hostname/browser checks before treating
   an outage as a Core availability failure.

That monitoring change should be proposed and implemented separately so it can
be reviewed as a concrete config/tooling change.

## Residual Risks And Follow-Ups

- Create or repair a current full backup before any Core upgrade, Recorder
  cleanup, or add-on remediation.
- Re-run recorder inventory against a copied `home-assistant_v2.db` so row
  counts and high-frequency writers can be ranked from real data.
- Investigate the oversized attribute sensors and decide whether their large
  history payloads should be shortened, moved out of Recorder, or made
  current-only.
- Investigate the failing irrigation fingerprint command-line sensor so it
  stops generating recurring errors.
- Watch UniFi Protect snapshot 500 retries and reduce snapshot polling or fix
  the camera/API path if the volume remains high.
- Build a remote-path probe with a reliable certificate/DNS path so Remote UI
  degradation can be separated cleanly from local Core health.
- Plan the pending Home Assistant Core update only after backup health is
  restored and availability is stable.
