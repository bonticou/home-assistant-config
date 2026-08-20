# Beelink Restart And WebSocket Pressure

Date: 2026-08-20

## Symptom And Impact

After migrating Home Assistant OS and the restored Recorder database to the
Beelink, the user observed lost connections and apparent restarts. The migration
was intended to eliminate the recurring availability failures seen on the old
host, so the immediate question was whether the new hardware was failing or the
restored software workload remained unhealthy.

## Relevant Prior Context

Reviewed before forming a new theory:

- `docs/audit-history/README.md`
- `docs/home-assistant-availability-investigation.md`
- `docs/audit-history/2026-08-02-unexpected-core-restart-during-tesla-setup.md`
- `docs/audit-history/2026-08-05-core-watchdog-restarts.md`
- `docs/home-assistant-remote-access-runbook.md`

The old host had at least three distinct availability failure families: unclean
Core termination, Supervisor watchdog restarts after missed Core API responses,
and remote/client connection failures that did not necessarily mean Core had
restarted. The restored system also brought forward the existing configuration,
integrations, and large Recorder history.

## Evidence Collected

All live checks were read-only. No restart, reload, integration change, or
configuration deployment was performed.

### Confirmed Restart Evidence

The current Core log shows Recorder ending an unfinished session from
2026-08-19 23:24 and reporting that the SQLite database did not shut down
cleanly when Core started at about 05:30 on 2026-08-20. This confirms at least
one real unclean Core stop/restart; it was not merely a browser refresh.

The available Core log does not identify whether Supervisor's watchdog,
another Core failure, or a host/container event forced that stop. Supervisor
and previous-host logs remain the missing evidence needed to classify it.

### Connection-Loss Evidence

The Core log separately records:

- an iPhone websocket disconnect after no PONG was received for 27.5 seconds;
- nine browser websocket failures where the client reached Home Assistant's
  4,096-pending-message limit;
- Home Assistant's own diagnosis on those failures that system load was too
  high or an integration was misbehaving;
- a Ting voltage state event as the last message in the saturated client queue.

These later connection failures are not accompanied by startup evidence in the
available Core log and therefore must not all be described as restarts.

### Integration And Event Pressure

The custom Whisker Ting integration is in a sustained reconnect loop:

- approximately 1,976 websocket disconnect/reconnect warnings;
- approximately 1,966 stale-data reconnect errors;
- both families began at about 05:38 and were still recurring near noon;
- one Ting entity state update took about 0.6 seconds;
- Ting voltage events were present when the browser websocket queue saturated.

The same log window also contains repeated timeouts or slow updates from Ring,
Spotify, Sonos, Hydrawise, Airthings, TP-Link, UniFi Protect, Brother, ESPHome,
and mobile notification delivery. These may amplify load, but none has evidence
as direct as the Ting reconnect/event storm for the observed websocket backlog.

Recorder still retains 30 days. The two raw Ting current-voltage entities and
most other Whisker Ting entities remain Recorder candidates; only the derived
`sensor.ting_notification_status` is explicitly excluded. The migration
restored the prior Recorder database and therefore did not erase historical DB
size or fragmentation by itself.

### Current Host Health

At the time of inspection:

- Processor use was about 12%.
- Memory use was about 1.7 GB of 15 GB.
- Storage showed about 412 GB free.
- Home Assistant Observer reported Supervisor connected, supported, and
  healthy.
- Core and Observer interfaces were reachable.

The Beelink therefore had ample current capacity. This argues against a simple
hardware-resource shortage, while not ruling out short-lived event-loop stalls.

### Other Errors

Startup/runtime logs also show invalid JSON handling in water/irrigation
templates, a duplicate `grid` key in the calm mobile dashboard, push-client
credential decoding failure, and HomeKit limit/value errors. These should be
cleaned up, but the current evidence does not make them the leading cause of
the lost connections or the confirmed restart.

## Ranked Findings

1. **Confirmed: at least one unclean Core restart occurred. Confidence: high.**
   Recorder's unfinished-session warning is direct evidence.

2. **Confirmed: some reported losses were websocket overload/disconnects, not
   proven restarts. Confidence: high.** Home Assistant logged the 4,096-message
   client backlog and a separate no-PONG disconnect.

3. **The Whisker Ting reconnect/event storm is the leading explanation for the
   connection losses. Confidence: high.** It is continuous, extremely noisy,
   produces slow entity updates, and is named in the final event when the
   websocket queue saturates.

4. **The migration removed the old hardware bottleneck but preserved the
   software workload. Confidence: high.** The new host is currently healthy and
   lightly loaded, while the restored integrations, configuration, and Recorder
   history remain in place.

5. **The exact cause of the 05:30 restart is still unclassified. Confidence:
   high.** The Ting storm starts after Core comes back, so it cannot yet be
   claimed as the trigger for that specific restart. Supervisor watchdog and
   host/container evidence are still required.

## Changes Made

None. This pass was diagnostic only.

## Recommended Next Actions

1. Capture Supervisor, host, and previous-Core logs around 05:30 before any
   restart rotates the evidence.
2. Temporarily stop or reload the Whisker Ting integration during an authorized
   maintenance window and verify that reconnect counts, pending websocket
   messages, and client disconnects cease.
3. Review or update the custom Whisker Ting integration before re-enabling it;
   report the reconnect loop upstream if the current release reproduces it.
4. Preserve useful Ting safety state, but reduce unnecessary Recorder writes
   from high-frequency raw/derived entities using exact entity exclusions or
   lower-frequency statistics rather than a broad domain exclusion.
5. Fix the water/irrigation JSON templates and duplicate dashboard key as
   separate, minimal reliability slices.
6. Add durable restart breadcrumbs or external uptime monitoring so future
   client disconnects can immediately be distinguished from Core restarts.

## Residual Risk

Until the Ting reconnect loop is stopped, Home Assistant may continue to shed
websocket clients even when average CPU and memory look normal. Until
Supervisor/host evidence is captured, another unclean restart could recur
without a definitive classification.
