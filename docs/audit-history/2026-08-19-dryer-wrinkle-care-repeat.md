# Dryer Wrinkle-Care Repeat Notifications

Date: 2026-08-19

## Symptom And User Impact

Trevor reported repeated dryer notifications even though no new dryer cycle had
finished. This occurred immediately after the Home Assistant migration to the
Beelink, making it important to separate restored helper state from a true
notification-logic defect.

## Relevant Prior Context

- The 2026-07-29 dryer notification build uses durable completion, notified,
  handled, snooze, follow-up, and event-key helpers.
- The 2026-08-07 laundry reliability fix added a status fallback for `end` and
  `wrinkle_care` so a missed ThinQ completion event would not suppress a useful
  notification.
- The fallback had a 15-minute duplicate window, but accepted any known prior
  status as a clean transition.

## Evidence Collected

- `dryer_cycle_complete_notification` triggers whenever
  `sensor.dryer_current_status` remains at `wrinkle_care` for two minutes.
- Its prior gate rejected only `unknown`, `unavailable`, `none`, and empty
  states. It therefore accepted later transitions back into `wrinkle_care`
  from non-drying states.
- LG wrinkle-care behavior can continue changing state after the load has
  already completed. Once the 15-minute duplicate window elapsed, the old gate
  could record that later transition as a new completion and reset the current
  cycle's notification timestamps.
- The official `event.dryer_notification` path already requires the exact
  `drying_is_complete` event type and is unaffected.

## Ranked Findings

1. **High confidence:** the status fallback was too permissive for recurring
   wrinkle-care transitions and could generate a false new completion.
2. **Medium confidence:** the migration made the symptom visible but was not
   itself the root cause; restored helpers can prolong an unresolved cycle, but
   they do not explain repeated new completion stamps as directly as the
   wrinkle-care transition gate.
3. **Low confidence:** the ThinQ cloud integration may emit additional unusual
   status sequences that still merit observation after this fix.

## Changes Made

- Restricted status-fallback completion detection to transitions whose prior
  state is an actual drying phase: `running`, `cooling`, or `detecting`.
- Preserved the official ThinQ event trigger, two-minute stability delay,
  15-minute event/fallback duplicate guard, presence policy, quiet hours,
  housekeeper behavior, follow-up timing, and all durable helpers.

## Checks

- Local YAML parsing and repository checks are recorded after the code change.
- Live read-back, configuration validation, automation reload, and next-cycle
  observation remain required before this incident is considered fully closed.

## Deployment Status

Prepared locally on 2026-08-19. Live deployment is pending completion of the
new Beelink's persistent SSH administration path.

## Residual Risks And Follow-Up

- Verify the next real dryer cycle produces one completion and at most the
  intended single unattended-load follow-up.
- Capture the observed `current_status` sequence so the accepted drying-phase
  list can be refined from evidence if LG reports a legitimate additional
  predecessor state.
- Clear or mark handled any already-active stale dryer notification after live
  deployment; the code change prevents future false completions but does not
  mutate restored helper history by itself.
