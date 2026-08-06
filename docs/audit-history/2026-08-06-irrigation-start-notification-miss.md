# Irrigation Start Notification Miss

## Symptom And User Impact

Trevor did not receive the usual sprinkler-start notification for the morning
irrigation run on 2026-08-06. This is a reliability issue because sprinkler
start/finish pushes are the primary human-facing confirmation that watering
actually began.

## Prior Context

- `2026-06-30-hunter-flow-irrigation-build.md` established Hydrawise as the
  schedule/zone truth, Hunter as the irrigation water-use measurement layer, and
  preserved routine irrigation start/finish pushes.
- `2026-07-13-irrigation-ledger-zone-count.md` already found that custom
  irrigation history can retain stale active-zone entries after missed/offline
  transitions and should not be treated as perfect live truth.
- Notification reliability rules require durable timestamp/cycle helpers, but
  those helpers must not be allowed to suppress a genuinely new cycle after they
  become stale.

## Evidence Collected

- Live irrigation state showed `input_boolean.irrigation_notifications_enabled`
  was `on`.
- `sensor.irrigation_history_status` showed a same-day Hydrawise/Hunter event:
  the latest zone run was `Basil and forsythias` / `Zone 24`, starting around
  2026-08-06 04:21 local time.
- `input_datetime.irrigation_session_started_at` was still stamped
  `2026-08-02 04:00:24`, and `input_text.irrigation_session_id` was still the
  matching stale 2026-08-02 session id.
- `input_datetime.irrigation_expected_water_use_until` was extended into the
  2026-08-06 morning watering window.
- The `Irrigation — Session Started Notification` automation only allowed a new
  start notification when there was no prior start or the expected-water-use
  window had expired.
- Routine `irrigation_started` and `irrigation_finished` alert events are
  intentionally excluded from the warning/error irrigation history ledger, so a
  missed push is not automatically surfaced as a warning history item.

## Findings

1. High confidence: the start notification was suppressed by stale irrigation
   session helpers, not by Trevor notifications being disabled.
2. High confidence: the expected-water-use window is useful for watering context
   and related alerts, but it was too broad as the only duplicate guard for the
   start notification.
3. Medium confidence: the same stale session state could also suppress or distort
   the paired finish notification and session summary for that run.
4. Medium confidence: irrigation dashboard/history surfaces may still show stale
   active-zone context after missed transitions; this is a separate visibility
   follow-up, not the direct cause of the missed push.

## Changes Made

- Hardened the `Irrigation — Session Started Notification` condition so a prior
  session start older than six hours is treated as stale and cannot block a new
  real session start.
- Preserved the existing duplicate protection for normal short sessions:
  no prior start, a stale prior start, or an expired expected-water-use window
  can open the gate; otherwise the automation still avoids duplicate start
  pushes inside one active session.
- Did not change alert content, notification recipients, Hydrawise/Hunter logic,
  Recorder rules, or dashboard behavior.

## Checks

- Local YAML parse for `automations/00-water-irrigation.yaml`.
- Home Assistant config check through File Editor deploy path.
- File Editor byte-for-byte read-back of the deployed automation file.
- Automation reload after a valid config check.
- Live automation config API confirmed the loaded `irrigation_session_started`
  automation contains the `prior_start_stale` guard and six-hour threshold.

## Deployment Status

- Deployed to live Home Assistant on 2026-08-06.
- The normal File Editor tab was stale/disconnected and its read endpoint failed,
  so deployment used the repo's established direct browser pattern: a connected
  HA dashboard tab supplied auth, HA websocket requested a fresh File Editor
  ingress session, the automation file was written through that session, and the
  deployed file was read back byte-for-byte.
- Home Assistant config check returned `valid` with no warnings or errors.
- `automation.reload` returned 200.

## Residual Risks And Follow-Ups

- The next real irrigation run should confirm that `💦 Sprinklers started` and the
  paired finish notification both arrive.
- Review stale active-zone cleanup at session finish so the dashboard/history
  does not keep old active zones alive after missed/offline transitions.
- Consider a secondary low-noise dashboard status for the latest routine
  start/finish notification so a missed push has a visible fallback without
  turning routine receipts into warning history.
- After deployment, `sensor.irrigation_history_status` was observed as `unknown`
  even though `sensor.irrigation_flow_baseline_status` still refreshed. That
  command-line history status needs a separate follow-up before relying on the
  irrigation dashboard as a complete fallback surface.
