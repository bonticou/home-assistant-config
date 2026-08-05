# Ring Realtime Notifications Stopped

Date: 2026-08-05

## Symptom And Impact

Trevor reported that Home Assistant was no longer delivering motion or
doorbell notifications from the Front Door and Mudroom Door Ring doorbells.
Both event types share one automation and alert script, so the loss removed the
normal HA-powered entry awareness for both doors.

Trevor then confirmed that a visitor physically rang the Front Door doorbell on
the morning of August 5 without an HA notification and that many motion events
had also been missed. This establishes repeated real-world misses across both
event types rather than an absence of expected activity.

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
- A connected local HA check on August 5 showed new polled activity while the
  realtime entities remained silent:
  - Front Door `Last activity`: 10:05 AM Eastern;
  - Mudroom Door `Last activity`: 10:24 AM Eastern;
  - Front Door and Mudroom Door `Ding`: `unknown`;
  - Front Door and Mudroom Door `Motion`: `unknown`;
  - both motion-detection switches: `on`;
  - `automation.security_entry_ring_notifications`: `on`.
- The current Core startup log captured the specific realtime-client failure at
  10:32:04 AM Eastern: `Incorrect padding, shutting down FcmPushClient`. The
  traceback ends in `firebase_messaging/fcmpushclient.py` while decoding a
  message encryption key. The client's own error path then terminates the push
  receiver.
- The same startup log showed Ring among integrations still completing setup
  shortly before the FCM failure. A fresh Core startup therefore did not restore
  durable Ring realtime delivery; the push receiver failed again immediately.
- Ring Control Center showed exactly one active Home Assistant client,
  `ring-doorbell:HomeAssistant/ring-integration`, last accessed at 2:25 PM
  Eastern on August 5. There was no accumulation of obsolete Home Assistant or
  Python clients to clean up. The fresh access time further confirms that the
  ordinary Ring account/API session remained active while realtime delivery was
  broken.
- HA reported that Ring reconfiguration completed successfully during the
  afternoon recovery attempt, but the Core log recorded the identical
  `Incorrect padding, shutting down FcmPushClient` failure at 2:25:54 PM
  Eastern. The Front Door `Ding` and `Motion` entities remained `unknown`
  afterward. Reconfiguration without first revoking the existing authorized
  client therefore did not rotate enough realtime state to restore service.
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

2. **High confidence: Ring's Firebase realtime push client is terminating on a
   malformed or incompatible encoded message/key while ordinary polling still
   works.**

   The `FcmPushClient` traceback is direct failure evidence. It explains the
   exact split between fresh `last_activity` polling and silent motion/ding
   entities, and it affects the whole Ring account rather than one automation
   or doorbell.

3. **High confidence: regenerating the Ring integration's realtime client
   identity/credentials is more promising than client cleanup, a simple reload,
   or a Core restart.**

   The push client failed again immediately after startup, so a plain restart is
   not a durable fix. Home Assistant's current troubleshooting guidance directs
   users to clean obsolete Ring Authorized Client Devices before reconfiguring
   the integration to generate a new unique ID. The account has only one current
   Home Assistant client, so excess-client cleanup is not applicable here. The
   current client should not be removed unless HA reconfiguration is performed
   immediately afterward.

   The first reconfiguration attempt completed in HA but the realtime client
   crashed immediately. The next bounded recovery attempt should therefore
   revoke the sole Ring-authorized Home Assistant client first and then
   immediately reconfigure HA Ring again, forcing a genuinely fresh client
   registration.

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
- Inspected connected local HA entity state for both Ring doorbells and the Ring
  automation after Trevor confirmed physical misses.
- Inspected and filtered the live Home Assistant Core log to the terminating
  `FcmPushClient` traceback.
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

1. Download the Ring diagnostics and preserve the 10:32:04 AM Core traceback
   before changing the integration.
2. Reconfigure the Ring integration to generate a new unique ID and realtime
   client identity. A simple reload or Core restart is unlikely to be durable
   because the client already failed again after startup.
3. If reconfiguration does not replace the Ring Authorized Client Devices
   entry, remove the single `ring-doorbell:HomeAssistant/ring-integration`
   client and immediately complete HA Ring reconfiguration and 2FA. Do not
   remove phone or ordinary Ring-app clients.
4. Verify outbound TCP 5228 from the HA host/network is allowed, although the
   decoded-message traceback proves the client connected far enough to receive
   a realtime message.
5. If alerts remain absent, toggle the Ring Motion Warning setting off, wait 30
   seconds, and turn it back on as documented by Home Assistant.
6. Verify all four paths with real tests: Front Door motion and ring, then
   Mudroom Door motion and ring. Confirm event timestamps, automation traces,
   alert-script runs, and receipt on Trevor's phone.

## Residual Risks And Follow-Ups

- A Ring integration reload may restore service only until the next incompatible
  message; capture diagnostics first and prefer the documented client-identity
  reset sequence.
- If a revoke-then-reconfigure cycle produces the same traceback, stop repeating
  account resets. Treat the failure as an upstream `firebase-messaging` / Ring
  integration defect, preserve native Ring-app alerts as the temporary safety
  path, and escalate with sanitized diagnostics and the exact traceback.
- Reconfiguring Ring can invalidate the current integration identity and should
  follow Authorized Client Devices cleanup in the documented order.
- The concurrent Remote UI tunnel outage needs separate follow-up if it persists,
  because it affects remote dashboard access even though it does not explain the
  Ring-only cutoff.
- The existing Ring automation has no durable health signal for a silent
  realtime-feed stall. After recovery, consider a low-noise monitor comparing
  recent Ring `last_activity` against event-entity updates so the next failure
  becomes visible quickly.
