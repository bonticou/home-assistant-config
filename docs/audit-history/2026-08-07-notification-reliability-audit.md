# Home Assistant Notification Reliability Audit

Date: 2026-08-07
Status: evidence-first audit, no live fixes deployed
Scope: Ring/security, irrigation, laundry, shared phone push path, recent optimization risk, and platform health as a confounder

## Symptom And User Impact

Trevor reported a major reliability problem: Ring motion and doorbell tests did
not produce notifications, and routine-but-essential notifications such as
laundry and irrigation have recently been missed or suspect.

The concern is not cosmetic. Notifications are part of the working home model:
security, water, laundry, irrigation, and maintenance depend on timely source
events, durable guards, push delivery, and action callbacks. The audit therefore
treated this as an end-to-end delivery problem, not as a one-off YAML bug.

No optimization, purge, reload, restart, or config change was performed during
this audit. The only live actions were controlled, labeled notification tests
and clears through the existing notification script.

## Relevant Prior Context

Reviewed before forming findings:

- [Ring realtime notifications stopped, 2026-08-05](2026-08-05-ring-realtime-notifications.md)
- [Irrigation start notification miss, 2026-08-06](2026-08-06-irrigation-start-notification-miss.md)
- [Laundry notification miss and ThinQ fallback, 2026-08-07](2026-08-07-laundry-notification-miss.md)
- [Core watchdog restarts and memory pressure, 2026-08-05](2026-08-05-core-watchdog-restarts.md)
- [Home Assistant Availability Investigation](../home-assistant-availability-investigation.md)
- [Notification reliability patterns](../notification-reliability-patterns.md)

Prior context matters because the latest symptoms rhyme with earlier incidents:

- Ring previously failed at the upstream realtime event-feed layer while the
  shared Trevor phone notification path still worked.
- Irrigation previously missed a start notification because stale durable helper
  state suppressed the current session.
- Laundry was recently hardened in Git with current-status fallbacks, but that
  repo change was not yet present in the live HA read-back during this audit.
- Core has recently restarted after watchdog missed-API windows, so platform
  availability remains a confounder for any missed notification.

## Notification Surface Inventory

Static repo inventory:

| Surface | Count | Interpretation |
| --- | ---: | --- |
| `script.notify_trevor_phone` callers | 160 | Almost all Trevor push paths intentionally funnel through the shared wrapper |
| Direct `notify.mobile_app_tk_iphone_16_pro` calls | 1 | The direct mobile notify service is contained inside the shared wrapper |
| `mobile_app_notification_action` handlers | 29 | There are many action callbacks that need receipt and callback observability |
| `house_notice_event_recorded` emitters | 10 | Notification Center history is centralized but not complete source-event truth |

Core delivery shape:

1. A source event or state changes.
2. An automation triggers.
3. A domain script prepares copy, tags, actions, and durable helper updates.
4. `script.notify_trevor_phone` records `house_notice_event_recorded`.
5. `script.notify_trevor_phone` calls `notify.mobile_app_tk_iphone_16_pro`.
6. The mobile app receives the push.
7. Optional action callbacks return as `mobile_app_notification_action`.

This audit found the most important gap is between steps 1 and 2 for Ring, and
a separate process gap between Git commits and live HA deployment for laundry.

## Live HA And Platform Evidence

Observed through the authenticated live HA API and browser session:

- HA frontend was connected locally during the audit.
- Home Assistant Core version reported by the live app: `2026.7.1`.
- `binary_sensor.remote_ui`: `on`.
- `sensor.home_assistant_remote_access_status`: `online`.
- Remote access status attributes showed recent recovery bookkeeping, including
  a last recovery attempt on 2026-08-07 and last restored time on 2026-08-07.
- System logs showed a recent Core startup window around 2026-08-07 19:05 UTC.
- Recorder logged an unclean previous database shutdown and ended an unfinished
  session from 2026-08-07 18:15 UTC.

Platform conclusion: HA was reachable during the audit, but recent Core restart
and unclean Recorder-session evidence remain a confounder. Platform instability
can explain some broad missed-notification windows, but it does not explain the
current Ring failure by itself because Ring had a specific integration-layer
push-receiver failure after startup.

## Controlled Notification Tests

Controlled tests run during this audit:

| Test | Result | Interpretation |
| --- | --- | --- |
| Basic `script.notify_trevor_phone` push with audit tag | Service call accepted; script trace finished | HA-side shared phone wrapper is callable |
| Actionable audit push with `CODEX_AUDIT_ACK` action | Service call accepted; no action callback observed in a 90 second listen window | Phone receipt/action path was not confirmed in-session |
| Direct `script.entry_camera_send_alert` test | Script trace finished and called shared notify wrapper | Ring alert downstream script path is callable when invoked directly |
| Clear audit notification tags | Service calls accepted | Tag clear path is callable from HA |

Important limitation: the audit did not receive an explicit user confirmation
that the phone displayed the controlled test pushes, and the action button was
not tapped during the listen window. Therefore this proves that HA can call the
mobile notify service, but it does not prove end-device receipt or action
round-trip reliability.

## Ring-Specific Evidence

Ring notification automation:

- Automation: `automation.security_entry_ring_notifications`
- Source entities:
  - `event.front_door_motion`
  - `event.front_door_ding`
  - `event.mudroom_door_motion`
  - `event.mudroom_door_ding`
- Downstream script: `script.entry_camera_send_alert`
- Shared push script: `script.notify_trevor_phone`

Live Ring state during audit:

| Entity | Observed state | Notes |
| --- | --- | --- |
| `event.front_door_ding` | `unknown` | State reset after current Core start; no current test event reflected in HA |
| `event.front_door_motion` | `unknown` | State reset after current Core start; no current test event reflected in HA |
| `event.mudroom_door_ding` | `unknown` | State reset after current Core start; no current test event reflected in HA |
| `event.mudroom_door_motion` | `unknown` | State reset after current Core start; no current test event reflected in HA |
| `sensor.front_door_last_activity` | recent activity timestamp present | Ring account polling/metadata path is not fully dead |
| `sensor.mudroom_door_last_activity` | recent activity timestamp present | Ring account polling/metadata path is not fully dead |
| `switch.front_door_motion_detection` | `on` | HA believes motion detection is enabled |
| `switch.mudroom_door_motion_detection` | `on` | HA believes motion detection is enabled |

Live trace evidence:

- `automation.security_entry_ring_notifications` had no traces after the current
  Core start.
- Its `last_triggered` remained at the prior Ring recovery/test window from
  2026-08-05.
- `script.entry_camera_send_alert` was callable directly during the audit, so
  the downstream alert script itself is not the first failure layer.

System log evidence:

- Logger: `firebase_messaging.fcmpushclient`
- Current startup log showed repeated notification callback failures inside the
  Ring event listener.
- The exception ended in the Ring event listener while reading an expected
  event id:
  - `ring_doorbell/listen/eventlistener.py`
  - `_get_ring_event`
  - `event_id = int(event["ding"]["id"])`
  - `KeyError: 'id'`
- After three sequential errors, the push receiver shut down.
- A nearby Firebase registration warning showed a timeout during GCM check-in.

Ring conclusion: the current Ring miss is upstream of our YAML automation. HA
did not receive a clean Ring realtime event from the integration, so the Ring
notification automation had nothing to trigger on. This is consistent with the
2026-08-05 Ring audit, but now there is fresh 2026-08-07 evidence that the Ring
push receiver shut itself down again.

Native Ring app behavior was not independently captured in this audit. That
comparison remains important: if the Ring native app fires while HA Ring event
entities stay `unknown`, the problem is specifically the HA Ring integration or
its Firebase push receiver. If the native Ring app also fails, the problem is
upstream of Home Assistant.

## Recent Optimization Risk Review

The audit explicitly checked whether recent Recorder or Notification Center
optimization appears to have broken critical notifications.

Findings:

- Ring event entities were not removed from Recorder and were not excluded by
  the recent low-stakes Recorder cleanup.
- Ring motion-detection switches were excluded from Recorder as config/control
  history, but their live states were still available and `on`. This does not
  explain missing Ring realtime events.
- Durable notification helpers for laundry, irrigation, and action handling were
  not broadly purged or removed.
- `sensor.house_notice_history` still updated during controlled notification
  tests, which means Notification Center event ingestion is still active.
- Some dashboard summary or diagnostic sensors are intentionally less recorded
  after recent optimization. That can reduce retrospective observability, but it
  did not remove the source event entities needed for the major automations
  checked here.

Optimization conclusion: the current Ring failure was not caused by the recent
Recorder optimization. However, optimization work has exposed the need for much
better delivery-chain observability before further slimming anything near
notifications.

## Live Deployment Drift

Live HA read-back did not match the newest Git state for the recently added
laundry fallback hardening.

Specifically, live HA did not show the current-status fallback logic from the
recent repo commits for:

- `automation.laundry_washer_cycle_complete_notification`
- `automation.laundry_dryer_cycle_complete_notification`
- washer/dryer completion scripts using rounded "finished around" copy

This is a process reliability problem. A repo commit and GitHub push are not
proof that the live HA instance is running the change. For notification-critical
fixes, live read-back must be part of the acceptance test.

## Recent Missed Notification Evidence

### Ring Motion And Doorbell

Evidence:

- User physically tested Ring motion or doorbell notifications and did not get
  expected notifications.
- HA Ring event entities remained `unknown` after the current Core start.
- Ring notification automation did not trace or trigger after current startup.
- System log showed Ring Firebase push callback failures and push receiver
  shutdown.
- Direct downstream alert script test was callable.

Finding: Ring failed at the source integration/realtime event-feed layer, before
our automation and before the shared phone notification wrapper.

### Irrigation Start

Evidence:

- Prior audit found a real stale-helper gate that could suppress a new irrigation
  start notification. That was fixed in Git and previously deployed.
- During this audit, live state showed a same-day irrigation start timestamp and
  recent irrigation status progression, including a zone-finished state.
- `automation.irrigation_session_started_notification` had triggered on
  2026-08-07.

Finding: current HA live state shows irrigation activity being detected. Phone
receipt for the latest irrigation push was not independently confirmed in this
audit. The previous stale-helper bug remains the best-supported explanation for
the earlier miss.

### Laundry Completion

Evidence:

- Live washer state showed a same-day washer completion event and matching
  completion helper timestamps.
- Live dryer state showed the older 2026-08-04 dryer completion event, but the
  dryer completion notification timestamp was not aligned in the same way.
- The newest repo fallback hardening for washer/dryer current-status sensors was
  not present in live HA during this audit.

Finding: laundry is not proven globally broken, but the newest hardening is not
live, and dryer completion/handled evidence remains ambiguous. The live system
still needs the fallback deploy and read-back verification before we can trust
it during ThinQ event misses.

## Notification Reliability Matrix

| Notification area | Tier | Source entity or event | Durable guard | Last source evidence | Last automation/script evidence | Audit status |
| --- | --- | --- | --- | --- | --- | --- |
| Shared Trevor phone wrapper | Foundational | `script.notify_trevor_phone` service call | Per-caller tags and helpers | Controlled test at 2026-08-07 15:24 ET | Script trace finished; mobile notify entity updated | HA-side callable; phone receipt unconfirmed |
| Ring entry cameras | Critical security | Four Ring `event.*_motion` and `event.*_ding` entities | None beyond source events and tags | Entities remained `unknown` after current Core start | Automation had no post-start trace; direct downstream script worked | Broken at Ring source/realtime layer |
| Front Door Ring doorbell/motion | Critical security | `event.front_door_ding`, `event.front_door_motion` | Ring automation tag path | No clean current Ring event in HA | Last automation trigger stayed at 2026-08-05 window | Broken or degraded; requires Ring-source repair |
| Mudroom Ring doorbell/motion | Critical security | `event.mudroom_door_ding`, `event.mudroom_door_motion` | Ring automation tag path | No clean current Ring event in HA | Last automation trigger stayed at 2026-08-05 window | Broken or degraded; requires Ring-source repair |
| Irrigation session start | Routine essential | Irrigation active/session helpers and Hydrawise-derived state | `irrigation_session_started_at`, session id helpers | Same-day start helper updated | Start automation triggered 2026-08-07 | Source path appears live; phone receipt unconfirmed |
| Irrigation finish/status | Routine essential | Irrigation history/status sensors and zone progress | Session/history helpers | Same-day zone-finished state observed | Not fully source-tested during audit | Partially verified; not enough receipt evidence |
| Washer completion | Routine essential | `event.washer_notification`, washer current status fallback in repo | washer event key and completion/notified helpers | Same-day washer completion observed | Live completion path triggered; fallback not live | Working for observed event, but hardening not live |
| Dryer completion | Routine essential | `event.dryer_notification`, dryer current status fallback in repo | dryer event key and completion/notified/handled helpers | Last observed dryer event 2026-08-04 | Current fallback not live; prior notification evidence ambiguous | Degraded confidence; needs deploy/read-back and next real cycle test |
| Water/leak safety | Safety critical | Flo/leak sensors and water safety automations | Water-specific helpers and alerts | Not source-tested in this audit | Inventory-only check | Untested in this audit; do not optimize blindly |
| Ting electrical safety | Safety critical | Ting sensors and Ting alert scripts | Ting-specific helpers | Ting websocket reconnect noise in logs | Not source-tested in this audit | Untested; live alerting should remain preserved |
| Late-night/away security | Security/routine | Presence, locks, garage, light state | Security-specific helpers and action handlers | Not source-tested in this audit | Action handlers present | Untested; keep out of optimization scope |
| Commute/train | Low August priority | Calendar/date/presence commute logic | Month/day gates | Intentionally quiet in August | Prior cleanup intentionally suppressed August output | Intentionally suppressed, not a failure |

## Ranked Findings

1. **Ring notifications are currently failing before the automation layer.**
   Confidence: high. The Ring event entities did not update, the Ring automation
   did not trace, and the system log shows the Ring Firebase push receiver
   shutting down after repeated callback failures.

2. **The shared HA-side phone notify wrapper is callable, but end-device receipt
   remains unconfirmed.**
   Confidence: medium-high for HA-side service execution, low for phone receipt
   because the audit did not receive user confirmation or an action callback.

3. **Recent Recorder optimization did not cause the Ring outage.**
   Confidence: high. The failed layer is the Ring realtime event feed, not a
   removed notification helper or excluded Recorder entity.

4. **Live HA is not necessarily running the latest repo notification fixes.**
   Confidence: high. The newest laundry fallback logic was present in Git but
   absent from live read-back. This must be treated as a notification reliability
   defect in the deploy process.

5. **Core availability remains a notification confounder.**
   Confidence: medium. The audit saw recent startup, unclean Recorder session
   evidence, and the known Core watchdog history. A Core stall can cause broad
   misses, but the current Ring evidence is more specific than a generic stall.

6. **Current observability is not strong enough for the importance of these
   alerts.**
   Confidence: high. We can infer many layers from traces and helpers, but there
   is no compact always-on matrix showing source event, automation trigger,
   script send, mobile service call, and action callback per critical alert.

## Confirmed, Degraded, Untested, Broken

Confirmed HA-side:

- `script.notify_trevor_phone` can be called.
- `script.entry_camera_send_alert` can be called directly.
- `house_notice_event_recorded` still updates Notification Center history.
- Clear-notification tag path can be called.

Broken or degraded:

- Ring event source path is broken or degraded right now.
- Dryer completion confidence is degraded because live fallback hardening is not
  deployed and recent evidence is ambiguous.
- Notification action callback was not confirmed during the 90 second audit
  listen window.

Untested in this audit:

- Native Ring app side-by-side result.
- Ring front door and mudroom physical tests with timestamped native-app,
  HA-entity, automation-trace, and phone-receipt comparison.
- Water/leak and Ting source-trigger tests.
- Next real dryer cycle after live fallback deployment.
- End-device receipt confirmation for controlled audit pushes.

## Do Not Change Yet

- Do not remove more notification-related history, helpers, source entities, or
  action metadata until source/send/action observability is stronger.
- Do not treat Ring as a YAML notification-copy problem. The evidence points
  upstream of the YAML automation.
- Do not count a Git commit as a live notification fix. Notification-critical
  changes need live read-back of the relevant automation/script and at least one
  source or controlled trigger test.
- Do not assume all misses have one cause. Current evidence shows at least three
  different layers: Ring source feed failure, stale-helper gate bug for a prior
  irrigation miss, and deploy drift for laundry hardening.

## Recommended Fix Plan To Draft Next

1. **Ring recovery and fallback plan**
   - Preserve the current Ring/Firebase error evidence.
   - Compare native Ring app behavior against HA Ring entities during a physical
     front door and mudroom test.
   - Reconfigure or reload the Ring integration only after capturing current
     traces/logs.
   - If this exact `KeyError: 'id'` push-receiver shutdown recurs, treat it as a
     Ring integration/upstream event-format defect and consider a temporary
     fallback based on `last_activity` polling for "something happened" alerts.

2. **Deploy drift repair**
   - Deploy the pending laundry fallback changes through the normal HA deploy
     path.
   - Read back the live automation/script definitions before declaring it done.
   - Run the next real washer/dryer cycle as the acceptance test.

3. **Critical notification observability**
   - Add a compact reliability matrix or sidecar ledger that records, for each
     critical alert, the last source event, last automation trigger, last script
     call, last mobile service call, and last action callback.
   - Keep it small and Recorder-aware. This is operational state, not a giant
     notification transcript.

4. **Source-feed health monitors**
   - Add stale-source monitors for Ring, ThinQ laundry, Hydrawise/irrigation, and
     Ting only after the audit/fix plan decides exact thresholds.
   - These should detect "the integration stopped producing useful events,"
     which is different from "a notification failed to send."

5. **Platform availability follow-through**
   - Continue the Core watchdog/memory-pressure audit because a Core stall can
     make all notification categories look broken at once.
   - Keep this separate from the Ring fix, because the Ring push-receiver error
     is already specific enough to act on.

## Deployment Status

No HA config was changed, reloaded, restarted, or deployed during this audit.

Repo deliverable only:

- This audit history entry.
- Audit-history index update.

## Residual Risk

The most urgent residual risk is that Ring security alerts can fail silently
when the HA Ring realtime push receiver shuts down. The second risk is process:
notification fixes can exist in Git but not in live HA unless live read-back is
made mandatory for notification-critical work.
