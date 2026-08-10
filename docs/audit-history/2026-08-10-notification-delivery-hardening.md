# Notification Delivery Hardening

Date: 2026-08-10
Status: deployed and live-read-back verified

## Symptom And User Impact

Trevor reported that Ring realtime notifications are still not reliably arriving
and that Hydrawise/sprinkler-start notifications are sometimes missed. This is
high-impact because entry-camera and irrigation notifications are routine
operational awareness, not dashboard polish.

Trevor also ordered a new, much stronger HA host. That should help Core,
Recorder, and frontend load pressure, but it does not by itself fix upstream
Ring/Hydrawise source-event problems or iOS push presentation/suppression.

## Relevant Prior Context

- [Notification reliability audit, 2026-08-07](2026-08-07-notification-reliability-audit.md)
- [Ring last-activity fallback recovery, 2026-08-07](2026-08-07-ring-last-activity-fallback.md)
- [Irrigation start notification miss, 2026-08-06](2026-08-06-irrigation-start-notification-miss.md)
- [Core watchdog restarts and memory pressure, 2026-08-05](2026-08-05-core-watchdog-restarts.md)

## Live Evidence Collected

Ring:

- `automation.security_entry_ring_notifications` was `on`, but still had not
  triggered since 2026-08-05.
- Ring realtime event entities remained `unknown` after startup:
  - `event.front_door_motion`;
  - `event.front_door_ding`;
  - `event.mudroom_door_motion`;
  - `event.mudroom_door_ding`.
- `automation.security_entry_ring_last_activity_fallback_notifications` was
  `on` and triggered multiple times on 2026-08-10.
- `script.entry_camera_send_alert` ran from the fallback path.
- `script.notify_trevor_phone` trace showed a concrete sent event:
  `👀 Mud room activity` at 8:39 AM local time.

Irrigation:

- `input_boolean.irrigation_notifications_enabled` was `on`.
- `automation.irrigation_session_started_notification` last triggered on
  2026-08-09 at 4:00 AM local time.
- `sensor.irrigation_history_status` showed `Weather skip likely` for the
  current morning.
- `automation.irrigation_scheduled_cycle_did_not_start_watch` triggered on
  2026-08-10 at 4:55 AM local time, consistent with a scheduled start that did
  not become a normal active irrigation session.

Shared phone path:

- A controlled `script.notify_trevor_phone` delivery test returned HTTP 200.
- The mobile notify entity updated.
- `sensor.house_notice_history` recorded the sent event.
- No action callback was observed from the phone during the short audit window.
- After the hardening deploy, a labeled Time Sensitive test notification was
  sent through the connected HA frontend at 8:58 AM local time. HA accepted the
  service call, but no action callback was observed during the next roughly 90
  seconds.
- Live mobile-app state showed the iPhone Companion integration present, current
  app version reporting, and the phone notify entity updated at the test-send
  time.

## Finding

The current failure pattern has two layers:

1. Ring realtime source events are still degraded before the YAML automation.
   The fallback path is firing from Ring metadata, but it is not truly realtime.
2. The HA-side mobile service call is succeeding, but phone receipt/action
   confirmation remains weak. Important Ring and irrigation operational alerts
   were still ordinary-priority notifications and could be muted, summarized, or
   hidden by iOS focus/presentation behavior.

## Change Made

Updated notification payloads only:

- Entry-camera alerts now include:
  - `ttl: 0`;
  - `priority: high`;
  - `push.interruption-level: time-sensitive`;
  - foreground `presentation_options` for alert and sound.
- Irrigation operational alerts now use the same Time Sensitive foreground
  presentation path for:
  - `irrigation_started`;
  - `irrigation_finished`;
  - `irrigation_scheduled_not_started`;
  - `irrigation_controller_offline`;
  - `irrigation_controller_offline_during_watering`.

This does not change when rules fire, source entities, durable gates, helpers,
Recorder behavior, or dashboard behavior.

## Checks

- Ruby YAML parse for `scripts.yaml`.
- `git diff --check`.
- File Editor byte-for-byte write/read-back for `/homeassistant/scripts.yaml`.
- HA config check returned `valid` with no errors or warnings.
- Direct `script.reload` returned HTTP 200 after the deploy helper's short
  reload calls timed out.
- Live script config API read-back confirmed `interruption-level:
  time-sensitive` and `presentation_options` are present in both
  `entry_camera_send_alert` and `water_send_alert`.
- Labeled Time Sensitive notification send accepted by HA frontend service call;
  no callback observed during the audit window.

## Deployment Notes

Deployed `scripts.yaml` through the File Editor/read-back/config-check path and
reloaded scripts. No HA restart was required.

## Residual Risks

- Ring realtime events remain an upstream integration problem. Time Sensitive
  delivery improves phone presentation for the fallback, but it does not make
  Ring realtime again.
- If HA/Core itself is down or stalled, no HA notification path can send. The new
  host should materially help with this class once migration is done.
- If the iPhone blocks Home Assistant notifications at the OS/app setting level,
  HA can still show successful service calls without visible phone receipt.
- The post-deploy test still needs human confirmation from the phone side: if it
  appeared but was not tapped, the callback result is inconclusive; if it did
  not appear, iOS/Home Assistant Companion notification settings are the next
  highest-priority check.
