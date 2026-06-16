# Remote UI Overnight Flapping

Date: 2026-06-16

## Summary

Trevor reported that the Home Assistant mobile app failed to load for roughly
one hour on the night of 2026-06-15, showing network connection issues. Live HA
history confirmed repeated Nabu Casa Remote UI dropouts during that period and
into the morning of 2026-06-16.

This was not treated as a dashboard styling issue. The strongest evidence is
`binary_sensor.remote_ui` itself moving through `off` / `unavailable` while the
Remote UI watchdog recorded reconnect attempts.

## Prior Context

Related history reviewed before diagnosis:

- `docs/home-assistant-remote-access-runbook.md`
- `docs/home-assistant-mobile-disconnect-audit-2026-05-26.md`
- `docs/audit-history/2026-06-04-home-assistant-availability-ui-and-casey-closet.md`
- `docs/audit-history/2026-06-04-remote-ui-http-stall.md`
- `docs/audit-history/2026-06-06-backend-availability-audit.md`

Those prior audits established that mobile/Safari disconnects often correlate
with access-layer or Remote UI tunnel failures, not necessarily the
`calm-mobile` dashboard.

## Evidence Collected

Current live state at diagnosis time:

- `binary_sensor.remote_ui`: `on`
- `sensor.home_assistant_remote_access_status`: `online`
- Watchdog status: `Called cloud.remote_connect because Remote UI was off`
- Last recorded recovery attempt: 2026-06-16 09:39:49

Home Assistant history for `binary_sensor.remote_ui` from 2026-06-15 4:00 PM
through 2026-06-16 10:45 AM Eastern showed these significant Remote UI-off
windows:

| Start | End | Duration |
| --- | --- | ---: |
| Jun 15 4:43:14 PM | Jun 15 6:43:45 PM | 120.5 min |
| Jun 15 9:39:55 PM | Jun 15 10:13:59 PM | 34.1 min |
| Jun 15 10:22:15 PM | Jun 15 11:16:40 PM | 54.4 min |
| Jun 16 3:02:45 AM | Jun 16 3:08:29 AM | 5.7 min |
| Jun 16 3:45:18 AM | Jun 16 4:03:35 AM | 18.3 min |
| Jun 16 6:28:31 AM | Jun 16 6:33:55 AM | 5.4 min |
| Jun 16 7:29:43 AM | Jun 16 7:33:16 AM | 3.6 min |
| Jun 16 9:38:36 AM | Jun 16 9:47:19 AM | 8.7 min |

The reported one-hour app outage lines up best with the 10:22 PM to 11:16 PM
Remote UI-off window, with a separate 34-minute outage immediately before it.

The terminal remote health probe was run but still hit the known Mac-side
certificate-verification false positive documented in prior audits:

- DNS succeeded.
- TCP succeeded.
- TLS verification failed with the known certificate-chain error.

That probe result was therefore treated as secondary and not used as the outage
classification source. The authenticated Safari/HA frontend history was the
primary evidence.

The HA error-log REST route attempted from the authenticated frontend returned
404, so raw Core/cloud logs were not captured in this pass.

## Findings

1. High confidence: the mobile app symptom was caused by Remote UI/tunnel
   availability, not by the `calm-mobile` dashboard.

   Evidence: `binary_sensor.remote_ui` was `off` during the relevant evening
   window. A dashboard render bug would not normally make HA's own Remote UI
   cloud connectivity sensor turn off.

2. High confidence: the existing watchdog helped record and attempt recovery,
   but did not prevent long outages.

   Evidence: the watchdog recorded `cloud.remote_connect` attempts, yet Remote
   UI remained down for 34, 54, and 120 minute windows.

3. Medium confidence: this is a recurring Nabu Casa/cloud tunnel or home-side
   network stability issue.

   Evidence: the pattern matches earlier Remote UI disconnect audits. Some
   status snapshots also showed gateway/update entities unavailable during
   outage windows, but this pass did not capture enough raw logs to distinguish
   HA Cloud, Supervisor, host networking, router/WAN, or DNS/TLS as the root
   cause.

## No Config Changes In This Pass

No Home Assistant configuration was changed during this diagnostic note. The
only durable change is this audit-history entry and README index update.

## Recommended Next Fix

The next reliability slice should move beyond a simple HA-internal
`cloud.remote_connect` call:

- add an external monitor that runs outside HA and records Remote UI root,
  `/ha-safe/home`, `/calm-mobile/home`, and websocket reachability from a clean
  network path;
- add a stronger escalation when Remote UI stays down longer than 15-20 minutes,
  such as a persistent notification plus a mobile push once connectivity is
  restored;
- capture HA Core/Supervisor/cloud logs around the next outage window from a
  source that can access logs directly;
- fix or replace the current terminal remote probe certificate path so it can
  distinguish real TLS/Remote UI failure from the known Mac-side certificate
  validation false positive;
- add better WAN/gateway health evidence, because current helper attributes
  often report `wan_status: unavailable`.

## Residual Risk

Because the outage was already over by the time of diagnosis, the exact root
cause inside HA Cloud, the local host, Supervisor, or the network path remains
unproven. The incident is nevertheless confirmed as a real Remote UI
availability event.
