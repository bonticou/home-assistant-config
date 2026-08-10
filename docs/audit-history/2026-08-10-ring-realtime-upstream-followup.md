# Ring Realtime Upstream Follow-Up

Date: 2026-08-10
Status: HA-side reload attempted; upstream Ring realtime path still not proven healthy

## Symptom And User Impact

Trevor asked what "broken upstream" means and asked to fix the source of missed
Ring realtime notifications. This is security-critical: Ring motion and doorbell
events should not silently fail before the notification automation can run.

## Relevant Prior Context

- [Ring realtime notifications stopped, 2026-08-05](2026-08-05-ring-realtime-notifications.md)
- [Notification reliability audit, 2026-08-07](2026-08-07-notification-reliability-audit.md)
- [Ring last-activity fallback recovery, 2026-08-07](2026-08-07-ring-last-activity-fallback.md)
- [Notification delivery hardening, 2026-08-10](2026-08-10-notification-delivery-hardening.md)

## What "Broken Upstream" Means

The repo-owned YAML path is:

1. Ring source event entity changes.
2. `automation.security_entry_ring_notifications` triggers.
3. `script.entry_camera_send_alert` sends the message.
4. `script.notify_trevor_phone` calls the iPhone notify service.

"Broken upstream" means the failure is before step 2. HA is not receiving a
clean realtime Ring motion or ding event from the Ring integration, so the
normal automation has nothing to react to.

## Live Evidence

- The Ring config entry was loaded and supported unload/reconfigure.
- Ring cameras, switches, and last-activity sensors existed under the Ring
  config entry.
- Motion detection switches were `on`.
- `automation.security_entry_ring_notifications` was `on`, but its
  `last_triggered` remained 2026-08-05.
- Ring realtime event entities were still `unknown`:
  - `event.front_door_motion`;
  - `event.front_door_ding`;
  - `event.mudroom_door_motion`;
  - `event.mudroom_door_ding`.
- The fallback automation based on Ring `last_activity` had triggered on
  2026-08-10, proving Ring metadata polling is not completely dead.

## HA-Side Recovery Attempt

Called `homeassistant.reload_config_entry` for the loaded Ring integration
entry.

Result:

- The reload call returned successfully.
- Ring metadata polling recovered on the next polling interval.
- Ring `last_activity` sensors repopulated with the prior Ring activity
  timestamps.
- Ring realtime event entities remained `unknown`.
- The primary Ring realtime automation still had not triggered.

Conclusion: a plain HA-side Ring reload is not enough evidence of recovery. It
refreshes the account/polling path, but it does not prove the realtime event
listener is healthy.

## External Reference Checked

The official Home Assistant Ring integration documentation says:

- Ring event entities are the supported entities for doorbell rings and motion
  alerts.
- Ring cloud polling runs every 60 seconds and all communication goes through
  the cloud.
- Realtime events require outbound TCP access to port `5228`.
- If realtime events are not working, first clean old Ring authorized clients
  that start with `ring-doorbell:HomeAssistant` or `Python`, then use the Ring
  integration `Reconfigure` option to generate a new unique ID.

The live evidence matches that model: the 60-second polling path works, while
the realtime event path remains degraded.

## Network Check

From the Mac on the same LAN, outbound TCP to `mtalk.google.com:5228` succeeded.
That does not prove the HA host itself has the same path, but it makes a simple
house-wide firewall/DNS block less likely.

## Ranked Findings

1. High confidence: the normal Ring automation is not broken; it is starved of
   Ring realtime events.
2. High confidence: Ring account/API metadata polling is alive enough for the
   `last_activity` fallback, but that fallback is not true realtime.
3. Medium-high confidence: the next root-cause fix is the official Ring cleanup
   and reconfigure sequence, not another YAML notification change.
4. Medium confidence: updating Core may still be sensible maintenance, but the
   current 2026.8.1 changelog did not show a direct Ring realtime-event fix.

## Recommended Next Fix

Do the official Ring realtime recovery sequence:

1. In the Ring account Control Center, remove only stale authorized clients that
   begin with `ring-doorbell:HomeAssistant` or `Python`.
2. In Home Assistant, open the Ring integration entry and run `Reconfigure` to
   generate a new unique ID.
3. Trigger a real motion and a real doorbell test at each monitored entry.
4. Confirm both layers:
   - Ring event entity changes in HA;
   - Trevor receives the Time Sensitive HA notification.

Do not delete Ring phone/app authorized clients. Do not remove and re-add the HA
Ring integration unless reconfigure fails, because that has higher entity-ID and
automation-blast-radius risk.

## Current Blocker

Attempted to open the Ring authorized-client page from Safari. The page landed
on the Ring login screen, so the account-client cleanup and any 2FA-backed
reconfigure cannot be completed by the repo agent alone without Trevor's Ring
account session.
