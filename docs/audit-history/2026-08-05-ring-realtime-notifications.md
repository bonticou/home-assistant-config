# Ring Realtime Notifications Stopped

Date: 2026-08-05

## Symptom And Impact

Trevor reported that Home Assistant was no longer delivering motion or
doorbell notifications from the Front Door and Mudroom Door Ring doorbells.
Both event types share one automation and alert script, so the loss removed the
normal HA-powered entry awareness for both doors.

## Relevant Prior Context

- `docs/home-assistant-availability-investigation.md`
- `docs/audit-history/2026-08-02-unexpected-core-restart-during-tesla-setup.md`
- `docs/audit-history/2026-06-16-remote-ui-overnight-flapping.md`
- `docs/home-assistant-remote-access-runbook.md`

Prior incidents distinguish Core/app-layer failures, Remote UI tunnel outages,
and client-session failures. This investigation therefore checked the Ring
event source, automation, shared notification path, and current access paths
separately.

## Evidence Collected

- The repo owns one enabled automation,
  `automation.security_entry_ring_notifications`, triggered by:
  - `event.front_door_motion`;
  - `event.front_door_ding`;
  - `event.mudroom_door_motion`;
  - `event.mudroom_door_ding`.
- The trigger form matches Home Assistant's documented Ring event-entity
  pattern: a state trigger with any prior state.
- The automation and `script.entry_camera_send_alert` last triggered together
  on 2026-08-01 at about 7:15 PM Eastern.
- The shared `script.notify_trevor_phone` triggered successfully again on
  2026-08-03 at about 9:31 PM Eastern. This proves the general Trevor phone
  notification path continued operating after the last Ring alert.
- Both Ring motion-detection switches were `on` in the most recent frontend
  state snapshot.
- Both doorbells had later `last_activity` values on 2026-08-03 around 8:00 PM
  Eastern, but all four Ring event entities were still `unknown` after the
  subsequent HA startup and had not produced a new automation trigger. This is
  consistent with ordinary Ring polling returning device activity while the
  separate realtime event connection is not delivering events.
- The event entities still existed with the expected Ring event metadata, so an
  entity rename or deleted entity is not the leading explanation.
- Home Assistant's current Ring documentation states that realtime events
  require outbound TCP port 5228. It also documents excess Ring Authorized
  Client Devices, integration reconfiguration, and toggling Ring Motion Warning
  as recovery steps when realtime alerts fail.
- During the live check, local HA recovered and answered ping, TCP 8123, and an
  HTTP root request, while the Nabu Casa Remote UI showed its instance-not-
  connected fallback. Home Assistant's public Cloud, Remote UI, and push-
  notification status were operational. This is a concurrent instance-specific
  Remote UI/tunnel problem, but it does not explain why the Ring automation
  stopped on August 1 while other HA phone notifications continued later.

## Ranked Findings

1. **High confidence: the primary Ring notification failure is upstream of the
   automation, in Ring realtime event delivery to Home Assistant.**

   The automation, alert script, and general Trevor phone notification path are
   present and enabled. The shared phone script worked after the Ring automation
   stopped, while all four Ring event sources stopped producing triggers
   together.

2. **Medium-high confidence: the Ring integration's realtime connection is
   stale or disconnected while ordinary polling still works.**

   Later `last_activity` readings coexist with no new event-entity activity.
   Home Assistant documents a separate realtime connection requiring outbound
   TCP 5228, which fits this split behavior.

3. **Medium confidence: account-session accumulation or a stale Ring integration
   identity may be the immediate cause.**

   These are the first two recovery areas in Home Assistant's current Ring
   troubleshooting guidance. Live Ring diagnostics and the Ring Authorized
   Client Devices list were not available in this read-only pass, so neither is
   yet proven.

4. **High confidence: the current Nabu Casa Remote UI outage is real but is not
   the primary August 1 Ring cutoff.**

   Local Core answered during the check and general mobile notification calls
   continued after Ring stopped. The Remote UI outage should still be followed
   under the existing longitudinal availability investigation.

## Changes Made

- No Home Assistant configuration or live state was changed.
- No integration reload, Core restart, test notification, or Ring account
  change was performed.
- Added this diagnostic record and linked it from the audit-history index.

## Checks Run

- Reviewed the audit-history index, availability investigation, related outage
  entries, and remote-access runbook.
- Inspected the Ring automation, shared alert script, device inventory, Recorder
  inventory, and relevant git history.
- Compared cached live entity state and last-triggered timestamps across the
  Ring source, automation, alert script, and shared notification script.
- Probed local HA DNS, ICMP, TCP 8123, and HTTP.
- Probed the Nabu Casa root, stock dashboard, calm dashboard, and websocket
  paths without authentication.
- Checked the official Home Assistant Ring documentation and public service
  status.

## Deployment Status

No deployment was performed. The Ring notification failure remains active
until realtime event delivery is restored and verified with a physical motion
and doorbell test at each entry.

## Recommended Recovery Order

1. Capture the live Ring integration status and diagnostics, plus relevant Core
   log lines, before changing it.
2. Verify outbound TCP 5228 from the HA host/network is allowed.
3. Review Ring `Authorized Client Devices` and remove only obsolete entries
   beginning with `ring-doorbell:HomeAssistant` or `Python`, following the
   official warning not to remove phone/app clients.
4. Reload or reconfigure only the Ring integration, avoiding a full Core restart
   unless integration-level recovery fails.
5. If alerts remain absent, toggle the Ring Motion Warning setting off, wait 30
   seconds, and turn it back on as documented by Home Assistant.
6. Verify all four paths with real tests: Front Door motion and ring, then
   Mudroom Door motion and ring. Confirm event timestamps, automation traces,
   alert-script runs, and receipt on Trevor's phone.

## Residual Risks And Follow-Ups

- A Ring integration reload may restore service without revealing the underlying
  cause; capture logs and diagnostics first.
- Reconfiguring Ring can invalidate the current integration identity and should
  follow Authorized Client Devices cleanup in the documented order.
- The concurrent Remote UI tunnel outage needs separate follow-up if it persists,
  because it affects remote dashboard access even though it does not explain the
  Ring-only cutoff.
- The existing Ring automation has no durable health signal for a silent
  realtime-feed stall. After recovery, consider a low-noise monitor comparing
  recent Ring `last_activity` against event-entity updates so the next failure
  becomes visible quickly.
