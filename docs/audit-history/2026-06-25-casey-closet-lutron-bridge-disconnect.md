# Casey Closet Lutron Bridge Disconnect

## Symptom And Impact

Trevor walked into Casey's closet and the closet light did not automatically
turn on. The expected behavior is immediate motion-on lighting followed by
quiet auto-off.

## Relevant Prior Context

- `2026-06-04-home-assistant-availability-ui-and-casey-closet.md` fixed the
  original stale motion entity for this automation.
- `2026-06-05-casey-closet-missed-motion.md` and
  `2026-06-06-ssd-data-disk-and-casey-closet.md` found earlier failures where
  Home Assistant did not receive a closet motion event or Core was unstable.
- `2026-06-11-casey-closet-stale-on.md` added the twelve-minute hard cap and
  watchdog so the closet light cannot remain on indefinitely.

## Evidence Collected

- Live API state showed `automation.lights_casey_s_closet_auto_off` was enabled
  and the loaded automation config still referenced:
  - `binary_sensor.casey_s_closet_motion`;
  - `light.master_casey_s_closet`;
  - the `watchdog` and `hard_cap` triggers.
- Within the two-hour incident window on June 25, 2026:
  - `binary_sensor.casey_s_closet_motion` reported `on` at 8:17:24 AM;
  - the automation triggered from that motion at 8:17:26 AM;
  - `light.master_casey_s_closet` remained `off`.
- The retained automation trace for the 8:17:26 AM run showed:
  - the motion trigger branch matched;
  - the light state condition was true (`off`);
  - the `light.turn_on` call failed with `BridgeDisconnectedError`.
- The prior quiet-off run at 8:12:32 AM also showed a service-level failure
  (`TimeoutError`) while calling `light.turn_off`, which is consistent with a
  flaky Lutron bridge/integration path rather than bad motion logic.
- The Safari Home Assistant shell was stale/disconnected during the
  investigation, so live API/history/websocket reads were treated as the source
  of truth instead of frontend state.

## Ranked Findings

1. High confidence: the closet motion sensor did report the walk-in, and the
   automation did take the correct turn-on branch.
2. High confidence: the immediate failure was the Lutron/Caseta light service
   path. Home Assistant raised `BridgeDisconnectedError` when the automation
   called `light.turn_on`.
3. Medium-high confidence: this was not caused by the YAML conditions, disabled
   automation, motion sensitivity, or a stale entity reference.
4. Medium confidence: short service retries are an appropriate minimal
   hardening step for momentary bridge disconnects, but they cannot fix a
   bridge that remains disconnected for an extended period.

## Changes Made

- Updated `automations/10-lighting-security.yaml`.
- Wrapped the Casey closet motion-on `light.turn_on` action in a short retry
  loop with `continue_on_error` so a brief bridge disconnect gets several
  chances to recover before leaving the closet dark.
- Added `continue_on_error` to the existing quiet-off and hard-cap off calls so
  transient service failures do not stop the automation run abruptly.

## Checks And Live Validation

- Local Ruby/Psych YAML parse passed for
  `automations/10-lighting-security.yaml`.
- `python3 tools/check_device_inventory_coverage.py` passed.
- `git diff --check` passed.
- Python/PyYAML parsing was not available in the local environment because the
  `yaml` module was not installed.
- Live config deployment was attempted but did not complete:
  - the File Editor page initially mounted with `hass.connected: true`;
  - the standard browser deploy helper reached the File Editor ingress path but
    received `401 Unauthorized` from `api/save`;
  - a browser-contained ingress deploy helper was queued, then stopped before
    write/read-back after the HA API path stopped responding;
  - no successful live file write/read-back was recorded during this pass.
- Remote UI probe at 8:34 AM showed DNS and TCP success but TLS handshake
  timeout to the Remote UI host.
- Local `homeassistant.local:8123` probe at 8:34 AM showed DNS and TCP success
  but HTTP and websocket timeout.

## Deployment Status

Not deployed as of this entry. Local repo fix is ready, but live Home Assistant
was unreachable/unreliable over both the Remote UI and local HTTP/websocket
paths during deployment.

## Residual Risks And Next Follow-Ups

- Deploy `automations/10-lighting-security.yaml` when Home Assistant access
  recovers, then run HA config check, `automation.reload`, and live config
  verification for `casey_closet_auto_off`.
- If another walk-in fails after this retry hardening is live, inspect Lutron
  bridge connectivity and Home Assistant system logs around the failure window.
- Consider adding a direct physical closet door/contact trigger or another
  local control path if the Lutron bridge continues to disconnect during
  high-trust lighting paths.
