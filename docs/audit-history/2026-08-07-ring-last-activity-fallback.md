# Ring Last-Activity Fallback Recovery

Date: 2026-08-07
Status: repo fix prepared; live HA deploy blocked by active access stall

## Symptom And User Impact

Trevor asked to fix the notification reliability issue immediately after the
full notification audit found Ring motion and doorbell pushes failing. This is
security-critical because entry-camera activity should not silently disappear
when the Ring realtime event feed breaks.

## Evidence Used

- The full notification audit on 2026-08-07 found fresh Ring/Firebase callback
  failures in HA logs.
- Ring `event.*_motion` and `event.*_ding` entities remained `unknown` after the
  current Core start.
- The primary Ring notification automation had not traced after the current Core
  start.
- Ring `sensor.*_last_activity` entities had recent timestamps, so Ring account
  metadata was not completely dead even though realtime event classification was
  degraded.
- The shared `script.entry_camera_send_alert` and `script.notify_trevor_phone`
  paths were callable when invoked directly during the audit.

## Change Made

Added a conservative fallback automation:

- primary path remains unchanged:
  `automation.security_entry_ring_notifications` still listens to the Ring
  `event.*_motion` and `event.*_ding` entities;
- fallback path listens to:
  - `sensor.front_door_last_activity`;
  - `sensor.mudroom_door_last_activity`;
- fallback only considers fresh activity timestamps from the last three minutes;
- fallback waits eight seconds after the `last_activity` update;
- fallback skips itself if the primary Ring event automation triggered at the
  same time;
- fallback sends an "activity" alert rather than pretending to know whether the
  event was motion or a doorbell ring.

Also extended `script.entry_camera_send_alert` to support `event_kind:
activity`, with copy that makes the uncertainty explicit.

## Files Changed

- `automations/10-lighting-security.yaml`
- `scripts.yaml`

## Checks Run

- Ruby YAML parse check for:
  - `automations/10-lighting-security.yaml`;
  - `scripts.yaml`;
  - `automations/30-maintenance-environment.yaml`.
- `git diff --check`.
- Generated browser deploy payload for:
  - `automations/10-lighting-security.yaml`;
  - `scripts.yaml`;
  - `automations/30-maintenance-environment.yaml`.

## Deployment Status

Not deployed at the time of this entry.

Live deploy was blocked because the active Safari HA frontend reported
`hass.connected: false`, fresh local HTTP/API requests timed out, the Nabu route
failed fresh TLS probing from the Mac, and the File Editor panel would not
mount. No HA restart, reload, or config mutation was performed while HA was in
that state.

The generated deploy payload is `.tmp-ha-utf8-browser-deploy.js`, but it must be
run only from a mounted File Editor ingress page with read-back and config-check
success.

## Residual Risk

Until this is deployed and read back from live HA, it is only a repo-backed fix.
After deployment, the fallback still depends on Ring `last_activity` metadata;
if Ring stops updating both realtime events and last-activity metadata, native
Ring app notifications remain the only independent backup.
