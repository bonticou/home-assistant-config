# Garage opener alert noise — 2026-09-10

## Symptom and history
Trevor reports frequent, unhelpful Time Sensitive opener-light failure pushes.
Reviewed the August 30 lighting regression and September 1 follower investigation.
The September 1 retry/alert change was deployed, but its alert had no cooldown.

## Evidence and findings
High confidence from configuration: the follower ran every minute, on startup
and reload, and after any opener light stayed on 15 seconds while the main
switch was off. Every failed pair of commands could push again after eight
seconds. This allowed recurring notifications and interference with independent
opener-light use. Actual physical failure versus device reassertion remains
unverified; the previous device-control concern is not dismissed.

## Change
Limit the follower to a real main-switch on-to-off transition. Preserve one
retry, rechecking that the main switch remains off. Remove the routine failure
push. The separate five-minute quiet automation continues to clean up all three
garage lights, with its existing activity protections. No new entities.

## Validation and deployment
Ruby YAML parsing and diff whitespace checks passed. Verified the follower has
only the main-switch transition trigger, no notify call, and the retry guard.
Live deployment pending. Physical follow-up: main-switch-off should still turn
off opener lights; normal later opener activity should not invoke this follower.
