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

## Live write follow-up
Files were written through the mounted Nabu Casa File Editor ingress after
confirming `hass.connected`. Baseline and patched SHA-256 hashes matched the
repo, and live read-back matched each patched file. Config-check/reload commands
were attempted during intermittent disconnects, but completion was not confirmed.
The Mac then locked and the computer-use tool could not unlock it.
Do not treat activation or visual/physical verification as complete.

## Completed deployment after unlock
On September 10, resumed through the connected Safari/Nabu File Editor route.
Home Assistant configuration check returned `valid`, with no errors or warnings.
Template, script, and automation reloads completed for the banner and garage
changes. Flo was then written and read back with SHA-256
`e5f39039a77b37c4510060dcee270dce4b4a946793b0a9e5b9440733b0521e95`;
a second config check passed and automation reload completed.
Live automation config includes the passive Flo notice and excludes the garage
phone push. Served Lovelace config contains explicit left alignment for both
banner title and body. Home view was opened for visual checking.

Flo severity template scenarios returned the expected results: info-only and
clear alerts do not bypass the observation window; warning, critical, missing
counts, and unavailable alerts do. Recovery requires all four gates; each
individual failed gate rejected the informational notice. An initial synthetic
fixture used undefined attributes and returned 400; it was corrected to the
actual state_attr missing-value contract (`None`) before the passing run.

Flo entities still report unavailable, so real-device test completion remains
unverified. No water valve operation or test notification was triggered.
