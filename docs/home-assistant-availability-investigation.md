# Home Assistant Availability Investigation

## Purpose And Status

This is the living inquiry for recurring Home Assistant stalls, unexpected
offline periods, Remote UI failures, and possible Core restarts. It integrates
the dated audit record into one current model so each recurrence builds on prior
evidence.

The optimization section is an **idea bank, not a to-do list, roadmap, priority
order, or implementation authorization**. Ideas remain hypotheses until logs,
measurements, timing, and risk justify a discrete change.

## Current Model

The visible symptom `Home Assistant is disconnected` does not identify one
root cause. Evidence to date supports at least three overlapping failure
families:

1. **Core/app-layer stall or unexpected termination.** Fresh HTTP and websocket
   sessions may stop responding even when the host still answers ping or TCP.
   The 2026-08-02 incident directly confirmed an unclean Core termination, and
   the 2026-08-05 incident confirmed repeated Supervisor watchdog restarts after
   missed Core API responses.
2. **Nabu Casa Remote UI/tunnel or TLS-path failure.** Remote access can fail
   while local Core remains healthy. The existing HA-internal watchdog can call
   `cloud.remote_connect`, but prior long outages prove that this is not a full
   recovery guarantee.
3. **Client session or route handoff failure.** A mobile or browser client can
   remain stuck in authentication or local/remote URL selection even while the
   Remote UI shell and websocket are reachable.

Do not classify another incident from the dashboard symptom alone. Compare the
root shell, stock `/ha-safe/home`, custom `/calm-mobile/home`, fresh websocket,
Remote UI state, local access, and restart evidence.

## Confirmed Evidence

- On 2026-08-02, Recorder found an unfinished session and reported that the
  SQLite database had not shut down cleanly. Core started around 8:35 PM and
  terminated around 9:13 PM, approximately 38 minutes later.
- On 2026-08-05, Supervisor logged three watchdog restarts after missing two
  Core API responses in a row. Each restart took roughly six to seven minutes to
  return Core to `RUNNING`, and host logs showed Core container memory peaks
  around `1G` without a captured OOM-kill marker.
- No repo-owned automation or script intentionally restarts Core, reboots the
  host, shuts it down, or installs updates.
- Prior incidents captured local ping/TCP success while fresh HTTP returned no
  bytes, including cases where an already-established websocket continued to
  receive state updates.
- Other incidents captured actual `binary_sensor.remote_ui` off/unavailable
  windows, including lengthy outages, without proving a Core restart.
- A separate incident showed the Remote UI shell and websocket reachable while
  the client remained stuck in authentication handoff.
- Recorder has historically been large: approximately 20.5 GB with 30-day raw
  retention. A July health gate showed backlog zero and ample SSD capacity, so
  database scope is a plausible load factor rather than a proven universal
  cause.
- `configuration.yaml` and the primary dashboard are both large, which raises
  deployment, recovery, and first-render risk. File size alone is not evidence
  that either is crashing Core.

## Active Hypotheses

These are ranked investigation hypotheses, not conclusions:

1. Core app-layer stalls leading to Supervisor watchdog restarts are now the
   leading explanation for the recurring restart-class outages.
2. Recorder/database pressure, integration retry load, template/state storms, or
   another app-layer stall may make Core unresponsive enough to trip the
   watchdog; OOM is plausible but not proven without an OOM-kill marker.
3. A host/container restart remains possible until host boot time, Supervisor
   uptime, and Core start time are compared for the same incident.
4. Remote UI instability is a real parallel problem and may occur independently
   of Core restarts.
5. Dashboard first-render load and client session state can worsen the visible
   experience, but they do not explain an unclean Recorder shutdown.

## Evidence Needed At The Next Recurrence

- Supervisor log and host log covering five minutes before through ten minutes
  after the outage.
- Rotated previous-Core log or duplicate Core log file.
- Core start time, Supervisor uptime, and host boot time from the same capture.
- Recorder backlog, WAL size, database status, Core CPU/memory, and Supervisor
  CPU/memory near the failure.
- External root, `/ha-safe/home`, `/calm-mobile/home`, and fresh websocket
  probes recorded independently of Home Assistant.
- Remote UI helper state and watchdog timestamps.

## Reliability Optimization Idea Bank

### Recorder And Database

- Consider shortening raw Recorder retention from 30 days to approximately
  10-14 days while preserving Home Assistant long-term statistics.
- Before changing retention or exclusions, obtain an off-device database copy
  and run `tools/generate_recorder_inventory.py --db` to identify actual top
  writers by rows and frequency.
- Use DB-backed evidence to exclude additional high-churn, low-history-value
  entities conservatively rather than applying broad domain exclusions.
- Treat purge, repack, and vacuum as separate maintenance work requiring a
  verified backup, quiet operating window, and post-operation health check.
- Avoid broad analytical queries against the live Recorder database through
  File Editor; prior attempts were expensive enough to disrupt the browser
  path.

### Crash And Restart Evidence

- Consider enabling Home Assistant's duplicate Core log file during a planned
  maintenance window so the previous Core process is easier to inspect after an
  unexpected restart.
- Add durable, low-noise breadcrumbs for Core start time, Supervisor uptime,
  host boot time, and restart classification.
- Maintain an external fresh-HTTP and websocket monitor so outages are recorded
  independently of Home Assistant itself.
- During a recurrence, compare Core start time, Supervisor uptime, and host boot
  time to distinguish a Core-only crash, Supervisor watchdog restart, and full
  host reboot.

### Configuration Structure

- Decompose the large `configuration.yaml` into coherent domain or purpose
  includes, especially its template sections and helper-heavy blocks.
- Treat this primarily as deployment and recovery blast-radius reduction; do
  not claim that file size alone is crashing Core without supporting evidence.

### Dashboard And History Load

- Make raw-history charts strictly disclosure-driven so closed detail surfaces
  do not initiate history queries.
- Prefer statistics sensors for recurring dashboard trends where they convey the
  same meaning with less Recorder/API work.
- Continue reducing first-render dashboard work while preserving the calm,
  glanceable Home experience.

### Integrations And Startup

- Review slow-start and retry-heavy integrations only when logs connect them to
  an outage, including Whisker Ting websocket startup, UniFi Protect retry
  noise, and statistics sensor setup time.
- Keep custom integrations and frontend dependencies current, but avoid broad
  disablement experiments without a controlled comparison and rollback plan.

## Guardrails

- Reliability evidence comes before optimization work.
- Take and verify an off-device backup before database maintenance or structural
  changes.
- Make one coherent change at a time and observe it before stacking another.
- Do not treat this document as authorization to restart, purge, repack, vacuum,
  disable integrations, or change retention.

## Investigation Record

- `docs/audit-history/2026-08-05-core-watchdog-restarts.md`
- `docs/audit-history/2026-08-02-unexpected-core-restart-during-tesla-setup.md`
- `docs/audit-history/2026-07-13-recorder-health-gate.md`
- `docs/audit-history/2026-07-13-recorder-pressure-follow-up.md`
- `docs/audit-history/2026-06-22-mobile-disconnected-nabu-session.md`
- `docs/audit-history/2026-06-16-remote-ui-overnight-flapping.md`
- `docs/audit-history/2026-06-06-backend-availability-audit.md`
- `docs/audit-history/2026-06-04-home-assistant-transient-app-layer-stall.md`
- `docs/audit-history/2026-06-04-remote-ui-http-stall.md`
- `docs/audit-history/2026-06-04-home-assistant-availability-ui-and-casey-closet.md`
- `docs/home-assistant-mobile-disconnect-audit-2026-05-26.md`

## Runbooks And Inventories

- `docs/home-assistant-remote-access-runbook.md`
- `docs/home-assistant-ui-hardening-runbook.md`
- `docs/home-assistant-deploy-runbook.md`
- `docs/recorder-inventory.md`
