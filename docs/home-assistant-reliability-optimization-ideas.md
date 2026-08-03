# Home Assistant Reliability Optimization Ideas

## Status

This is an **idea bank, not a to-do list, roadmap, backlog, or implementation
commitment**. Items here are hypotheses and possible optimization directions to
revisit when evidence, timing, and risk justify them. Their order does not imply
priority.

## Context

The 2026-08-02 Tesla setup interruption confirmed an unclean Home Assistant Core
restart. Earlier incidents also include Remote UI and client-session failures
without a proven Core restart. These ideas may improve stability or future
diagnosis, but none is established as the root-cause fix.

## Ideas

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
- Do not treat this document as an authorization to restart, purge, repack,
  vacuum, disable integrations, or change retention.

## Related Evidence

- `docs/audit-history/2026-08-02-unexpected-core-restart-during-tesla-setup.md`
- `docs/audit-history/2026-07-13-recorder-pressure-follow-up.md`
- `docs/audit-history/2026-07-13-recorder-health-gate.md`
- `docs/audit-history/2026-06-06-backend-availability-audit.md`
- `docs/home-assistant-remote-access-runbook.md`
- `docs/recorder-inventory.md`
