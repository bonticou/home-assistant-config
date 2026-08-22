# Dryer Follow-Up Timestamp Loop

Date: 2026-08-22

## Symptom And Impact

Trevor reported a burst of erroneous dryer signals shortly after a dryer cycle
finished. The dryer reminder system is supposed to send one completion notice
and, if still unresolved, one follow-up after 90 minutes or one additional
follow-up after an explicit snooze.

User impact: the dryer notification became noisy and untrustworthy.

## Relevant Prior Context

- `2026-07-29-dryer-cycle-notifications.md` added dryer completion,
  follow-up, housekeeper-window handling, and dryer-start handoff behavior.
- `2026-08-07-laundry-notification-miss.md` added status fallbacks for missed
  ThinQ events.
- `2026-08-19-dryer-wrinkle-care-repeat.md` narrowed status fallback detection
  after repeated wrinkle-care completions.
- Earlier on 2026-08-22, `2026-08-22-overnight-lights-timestamp-guard.md`
  identified a separate failure caused by parsing plain `input_datetime` state
  strings instead of using their native timestamp attributes.

## Evidence Collected

- Live history showed two dryer completion events on 2026-08-22:
  - 9:14 AM;
  - 9:26 AM.
- The dryer follow-up script fired repeatedly every minute from 9:27 AM through
  9:32 AM.
- The trace for `automation.laundry_dryer_cycle_unhandled_follow_up` showed
  `should_notify: true` at 9:30 AM even though:
  - the completion notification was stamped at 9:26 AM;
  - the normal 90-minute follow-up should not have been due until 10:56 AM;
  - a follow-up had already been sent at 9:27 AM.
- Trace variables showed parsed helper timestamps were four hours behind the
  helpers' actual local times, matching the plain-string timestamp parsing
  class found in the overnight-light incident.
- The existing follow-up guard compared `follow_up_ts` with the due timestamp,
  which allowed repeated sends after the first follow-up instead of blocking
  normal repeats until an explicit snooze.

## Ranked Findings

1. **Plain `input_datetime` state parsing caused premature due detection.
   Confidence: high.**

   The automation used `as_timestamp(states('input_datetime...'))` on helpers
   whose visible states are local datetime strings. The resulting timestamps
   were offset enough that the 90-minute follow-up appeared due immediately.

2. **The follow-up idempotency condition allowed repeats. Confidence: high.**

   The rule checked whether the last follow-up was before the next due time.
   Once the computed due time was wrong, every minute still satisfied that
   comparison. The correct normal-follow-up guard is whether no follow-up has
   been sent since the current completion notification.

3. **Completion detection was not the primary noisy path in this incident.
   Confidence: medium-high.**

   Live history did show two completion events, but the burst of erroneous
   signals came from the follow-up script firing every minute.

## Changes Made

- Updated dryer notification action conditions, completion duplicate guards,
  pending-delivery checks, follow-up checks, error throttles, dryer-start
  handoff, and housekeeper-window dryer handling to use
  `state_attr(..., 'timestamp')` for durable `input_datetime` helpers.
- Updated dryer completion and follow-up notification scripts so user-facing
  "finished around" and "sitting for X min" copy uses helper timestamp
  attributes.
- Rewrote the dryer follow-up due logic:
  - normal follow-up sends only if no follow-up has been sent since the current
    completion notification and 90 minutes have elapsed;
  - snooze follow-up sends only if the snooze timestamp is newer than both the
    original notification and the last follow-up.
- Cleared the visible dryer-cycle notification after deployment.

## Checks And Validation

- Ruby YAML parse passed for:
  - `automations/30-maintenance-environment.yaml`;
  - `scripts.yaml`;
  - `configuration.yaml`.
- Live File Editor/direct-ingress deployment wrote and read back:
  - `/homeassistant/automations/30-maintenance-environment.yaml`;
  - `/homeassistant/scripts.yaml`.
- Home Assistant config check returned `valid`.
- `script.reload` and `automation.reload` returned HTTP 200.
- Live post-deploy computation for the current dryer helpers returned
  `shouldNotify: false`.
- Waited through the next minute-boundary automation tick:
  - the follow-up automation evaluated;
  - `script.dryer_send_follow_up_notification` did not run again;
  - `input_datetime.dryer_last_follow_up_at` did not change.

## Deployment Status

Deployed live on 2026-08-22. No Core restart was required.

## Residual Risks And Follow-Ups

- Observe the next normal dryer cycle. Expected behavior is one completion
  notification and no follow-up until 90 minutes after the completion notice
  unless Trevor snoozes.
- The official ThinQ completion event path remains active. If LG emits genuinely
  duplicate official completion events for the same load, that should be
  handled separately from the follow-up-loop bug fixed here.
