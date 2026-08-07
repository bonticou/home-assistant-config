# Ring Last-Activity Fallback Recovery

Date: 2026-08-07
Status: deployed after File Editor ingress recovery

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

Deployed after the initial access stall cleared.

Initial live deploy was blocked because the active Safari HA frontend reported
`hass.connected: false`, fresh local HTTP/API requests timed out, the Nabu route
failed fresh TLS probing from the Mac, and the File Editor panel would not
mount. No HA restart, reload, or config mutation was performed while HA was in
that state.

After local HA recovered:

- File Editor was confirmed started through Supervisor websocket info.
- File Editor direct ingress initially returned `401: Unauthorized`.
- A fresh ingress session was minted through the authenticated HA frontend and
  set for the local ingress path.
- The generated `.tmp-ha-utf8-browser-deploy.js` payload wrote and read back:
  - `/homeassistant/automations/10-lighting-security.yaml`;
  - `/homeassistant/scripts.yaml`;
  - `/homeassistant/automations/30-maintenance-environment.yaml`.
- HA config check returned `valid` with no errors or warnings.
- The helper's short reload calls timed out, then direct `script.reload` and
  `automation.reload` calls both returned HTTP 200.
- Live HA state confirmed
  `automation.security_entry_ring_last_activity_fallback_notifications` exists
  and is `on`.
- Live config read-back confirmed:
  - Ring fallback contains the `last_activity` source and `activity` event kind;
  - washer fallback contains `sensor.washer_current_status` and
    `status_end_fallback`;
  - dryer fallback contains `sensor.dryer_current_status` and
    `status_done_fallback`;
  - washer/dryer notification scripts contain rounded "Finished around" copy.

## Post-Deploy Ring Status

Reloading the Ring config entry did not fully recover the realtime event feed.
After reload, the Ring/Firebase push receiver still logged shutdown after
callback errors, and Ring `event.*_motion` / `event.*_ding` entities remained
`unknown`.

However, forcing an update of the Ring last-activity sensors repopulated
metadata timestamps while realtime events stayed `unknown`. That validates the
fallback source as useful for the current failure mode, though the normal Ring
event integration still needs follow-up.

## Residual Risk

The fallback still depends on Ring `last_activity` metadata. If Ring stops
updating both realtime events and last-activity metadata, native Ring app
notifications remain the only independent backup.
