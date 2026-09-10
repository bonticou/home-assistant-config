# Pickup banner formatting — 2026-09-10

The mobile holiday pickup banner had a left-positioned title but centered
wrapped body text. The shared button-card styles positioned the text containers
without overriding text alignment. Both title and body now explicitly use
`text-align: left`, covering holiday and normal pickup banners.

Removed the redundant instruction not to put bins out from the banner template
and matching holiday push copy. Pickup dates, conditions, and actions are unchanged.

Context: reviewed the June 11 sticky-bar history and deployment runbook.
Ruby YAML parsing passed for configuration.yaml, scripts.yaml, and the dashboard;
`git diff --check` passed. Python system runtime lacked PyYAML, so Ruby was used.
Live deployment and visual verification remain pending; File Editor mounted after
an initial disconnected dashboard. No live behavior claims are made yet.

## Live write follow-up
Files were written through the mounted Nabu Casa File Editor ingress after
confirming `hass.connected`. Baseline and patched SHA-256 hashes matched the
repo, and live read-back matched each patched file. Config-check/reload commands
were attempted during intermittent disconnects, but completion was not confirmed.
The Mac then locked and the computer-use tool could not unlock it.
Do not treat activation or visual/physical verification as complete.
