# Mudroom motion lighting

Trevor requested a two-minute exterior light assist for mudroom Ring motion
after dark. The rule must leave an already-on light alone and release its timer
if someone switches the light off and back on. This is the implementation record
for `HA-MUDROOM-RING-MOTION-20261120` (November 20 UTC; November 19 Eastern).

## Verified bindings and prior behavior

Read-only live checks on Core **2026.9.2** confirmed:

- `event.mudroom_door_motion`: **Mudroom Door Motion**, Ring Doorbell Pro 2,
  Ring integration, event types `motion`; motion detection enabled. This is not
  the separate doorbell-press event.
- `switch.exterior_mud_room_stairs`: **Exterior Mud Room Stairs**, Lutron
  Caseta DVRF-5NS Diva Smart Switch, confirmed off during inspection.
- The motion entity was available, with a November 17 event timestamp restored
  into state on November 19. Availability and an old timestamp do **not** prove
  the present realtime feed. No motion was manufactured to test it.

The [August Ring recovery](2026-08-10-ring-realtime-upstream-followup.md)
records the previous upstream realtime failure and later recovery; its retired
polling fallback remains retired. The [June exterior-light decision](2026-06-15-dehumidifier-done-and-mudroom-exterior.md)
removed normal door-schedule turn-on, while vacation lighting and house shutoff
coverage remained. The new rule does not change those paths.

## Change and ownership

One new automation, **Lights — Mudroom Ring Motion Exterior Assist**, uses
`sun.sun == below_horizon`. The existing door-light schedule can begin above the
horizon, so it is not an appropriate darkness gate for this request.

Only a changed, fresh motion timestamp newer than the previous state's change
and event time qualifies. Unavailable/restored recovery, stale timestamps,
attribute-only updates and doorbell presses do not start a cycle. A genuine
first motion after an unknown state can qualify. The target must be exactly off.

The single-mode run observes the first target transition in parallel with a
guarded on command. It accepts only the original off-to-on transition carrying
the current action context, then measures 120 seconds from that acknowledged
transition. Repeated motion cannot extend the run. The captured on timestamp
must remain unchanged; any off/unknown/unavailable transition or later on cycle
releases shutoff, even when Lutron reuses the service context. It never claims
whatever on state exists after an awaited service call returns.

The 100 ms command delay is a scheduling lead, **not a synchronization guarantee**.
Missing acknowledgement ends the observer after ten seconds without an off call;
HA records the timeout in the private retained trace. A rejected acknowledgement
is also visible as the failed ownership condition. Twenty traces are retained.
No user notification or new helper was added.

Source review used the deployed-version [HA script implementation](https://github.com/home-assistant/core/blob/2026.9.2/homeassistant/helpers/script.py)
and [Lutron switch implementation](https://github.com/home-assistant/core/blob/2026.9.2/homeassistant/components/lutron_caseta/switch.py).
The current run token is `context.id`, not `this.context.id`. The independent
review required the darkness and restoration corrections before deployment.

## Checks and deployment

- Nine non-actuating production-template tests cover fresh/restored motion,
  unknown/unavailable, darkness, confirmed-off, first acknowledgement, missed
  acknowledgement, inherited-context rapid off/on, cancellation and deadline.
- Seven Evening manual-override and seven shared-away-coverage tests pass.
- Inventory coverage: 181 active control references recorded; no device/entity
  was added or renamed, and the target already belongs to the shared inventory.
- Live baseline config check passed. Candidate preserves the exact original
  live byte prefix and all 185 existing automation definitions; local ownership
  remains the lighting/security file, live ownership remains monolithic YAML.
- Reload assessment: Evening already selected and run today, closet/garage
  lights off, Wynn's bedtime window guarded, both people home, maintenance due
  gates off. The only observed active automation was the inventory debounce;
  no competing deployment/reload or active lighting cycle was found. Existing
  reload listeners and their ordinary safeguards are preserved.
- Independent review approved the corrected candidate before apply. Deployment
  **`691dd5fe522c4d9ba05028cdecbc4409`** applied around **20:13 EST** with only
  `automation.reload`; validation passed and reload completed. No Core restart.
- Fresh live automation SHA-256 matched the reviewed candidate:
  `75c66cce794554a56e7ae02bff4dc814f83f3b038b7547068ac3a81f84e2eb0e`.
  Baseline was `6b127b2849297368d388e5470b44c130c7fb3fa24548fba6dfd5158eb7d1a620`.
  Post-deployment config check passed; administrative health had no recovery pending.
- Loaded entity **`automation.lights_mudroom_ring_motion_exterior_assist`** is
  **on**, with `last_triggered: null`. Fresh UI readback at 20:13 EST confirmed
  the target still off, its last state change hours before deployment, the same
  Ring event timestamp, and the unchanged Evening scene/last-run timestamp.
  This verifies deployment and guards against reload replay; it is not a real
  motion-cycle or physical two-minute acceptance test.

## Limits and recovery

No physical light command, test notification, motion simulation or routine replay
was used for verification. A later naturally occurring motion cycle is required
to establish realtime delivery, actual context propagation and physical timing.
If HA misses an acknowledgement or is restarted/reloaded during a cycle, the
light may remain on; the rule deliberately does not shut off an unowned cycle.
Physical transitions never reported to HA cannot be distinguished by YAML.
Existing vacation and house-off routines can still affect this light; those
independent policies remain unchanged.

Rollback uses the deployment journal with only an automation reload, subject to
the helper's unchanged-hash guard. Do not overwrite later unrelated changes.

## Owner-reported motion attempt, 20:16–20:17 EST

Trevor reported putting his hand in front of the motion detector. He did not
explicitly report the light's physical outcome. An immediate read-only check
at 20:16:39 EST found the new rule enabled, with no last trigger; retained traces
were empty, including no condition-rejection or ownership-failure trace.

Fresh HA template output at **20:17:00 EST** showed:

- Ring's mudroom `last_activity` sensor: **20:15:54 EST today**.
- Mudroom motion event: still **November 17, 08:52:32.175 EST**.
- Exterior target: **off**, with last state change **12:33:59 EST today**, well
  before deployment. No target state transition was evident during this attempt.
- Sun: below horizon; Ring motion detection: enabled.

The polling activity timestamp advanced within the reported attempt's window,
but the realtime motion event did not. The new rule therefore had no new motion
trigger to evaluate; this is not evidence of a darkness or ownership-code failure.
The specific Ring activity type is not established by `last_activity` alone.

A bounded 150-line recent Core log excerpt covering the attempt contained no
Ring/FCM/new-rule diagnostic explaining the missing event. The historical
polling-versus-realtime incident is relevant, but its old root cause is not
proven to have recurred. No full Recorder history was retrieved; current state,
last-changed timestamps and retained automation traces are the evidence limits.

Initial and follow-up facts were returned promptly through the originating relay.
No configuration correction, physical command, fake event, reconnect,
integration restart or authentication change was performed. Realtime Ring
delivery remains the unresolved dependency; do not substitute polling activity
for the explicitly requested motion signal.
