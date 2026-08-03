# Unexpected Core Restart During Tesla Setup

Date: 2026-08-02

## Symptom And Impact

Home Assistant disconnected while the Tesla Fleet integration was being added.
The Nabu Casa Remote UI lost its live connection and stalled at `Loading data`;
the local browser route also timed out briefly. Tesla developer application
setup remained intact, but Home Assistant credential entry could not continue.

## Relevant Prior Context

- `2026-06-04-home-assistant-transient-app-layer-stall.md`
- `2026-06-04-remote-ui-http-stall.md`
- `2026-06-16-remote-ui-overnight-flapping.md`
- `docs/home-assistant-remote-access-runbook.md`

Prior incidents established that custom dashboard content is not the lead
suspect when the root shell, stock dashboard, fresh HTTP, and websocket paths
fail together.

## Evidence Collected

- During the outage, the Remote UI frontend reported `Connection lost.
  Reconnecting…` and remained stuck loading the Application Credentials picker.
- Fresh Remote UI probes reached DNS and TCP but failed during TLS before HTTP
  or websocket establishment.
- The local browser route timed out during the bad window.
- Shortly afterward, a fresh local probe recovered fully:
  - `/`, `/calm-mobile/home`, and `/ha-safe/home` returned HTTP 200;
  - `/api/websocket` returned the Home Assistant `auth_required` greeting;
  - the reported Core version was 2026.7.1.
- The recovered Core log showed startup entries at about 9:13 PM Eastern:
  - Recorder ended an unfinished prior session;
  - Recorder could not validate that `home-assistant_v2.db` had shut down
    cleanly;
  - integration setup warnings followed during normal startup.
- The prior unfinished Recorder session began at approximately 8:35 PM
  Eastern.
- A repository search found no configured `homeassistant.restart`, host reboot,
  host shutdown, or update-install automation/script that explains the restart.
- Storage was healthy after recovery, with approximately 12% used and more than
  800 GB free.

## Ranked Findings

1. **High confidence:** the immediate cause of the visible disconnect was an
   unexpected Home Assistant Core restart or termination around 9:13 PM.

   The unclean Recorder shutdown and new startup sequence are direct evidence;
   this was not merely a stale Tesla form or dashboard rendering failure.

2. **High confidence:** the Tesla developer application did not cause or lose
   state because of the restart.

   The application was approved on Tesla's site before Home Assistant restarted,
   and Home Assistant had not yet completed credential storage.

3. **Medium confidence:** the underlying trigger was outside repo-owned YAML.

   No restart/update automation was found. Plausible remaining causes include a
   Supervisor watchdog restart, Core crash, host/container restart, or an
   external/manual restart action.

4. **Low confidence:** post-startup statistics warnings were causal.

   They appeared after the new startup began and are therefore treated as
   effects of startup unless earlier Supervisor or previous-Core logs show
   otherwise.

## Changes Made

- No Home Assistant configuration or live state was changed.
- No restart was initiated during diagnosis.
- Added this audit-history entry only.

## Checks Run

- Reviewed the related Remote UI and app-layer incident history.
- Probed Remote UI DNS, TCP, TLS, HTTP, and websocket paths.
- Probed local root, stock dashboard, custom dashboard, and websocket paths.
- Inspected the recovered Home Assistant Core log summary.
- Searched repo-owned configuration for intentional restart, reboot, shutdown,
  and update-install actions.

## Deployment Status

No deployment was required. Local Home Assistant HTTP and websocket service had
recovered by the end of the diagnostic window. Remote UI recovery was not
conclusively verified because the external Mac probe returned the previously
documented certificate-validation false positive after the earlier TLS EOFs.

## Residual Risks And Follow-Ups

- Capture Supervisor logs and the rotated previous Core log before they age out;
  these are the best remaining evidence for crash versus watchdog versus host
  restart.
- Record host boot time, Supervisor uptime, and Core container restart metadata
  during the next recurrence.
- Continue the Tesla Fleet setup through the healthy local route; do not treat
  Tesla configuration as the outage cause without contrary log evidence.
- The recurring external fresh-HTTP/websocket monitor remains the best way to
  timestamp future failures independently of Home Assistant itself.

Possible optimization directions are preserved separately in
`docs/home-assistant-reliability-optimization-ideas.md`. That document is an
idea bank, not an action list or authorization to make changes.
