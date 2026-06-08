# Late-Night Exterior Lighting And Remote UI Handoff

## Symptom And Impact

On Monday morning, June 8, 2026, the user reported a short mobile Home
Assistant hang where the Warm Up screen showed "loading data" and then briefly
went blank. The user also reported that Home Assistant seemed to have a weird
handoff between local and cloud access.

The user also reported missing overnight notifications on Sunday night, June 7
into Monday morning, June 8, 2026, for garage lights and the mudroom exterior
light, and expected the garage light to auto-off after five quiet minutes.

## Relevant Prior Context

- Prior 2026-06-04 audits found a recurring split between existing connected
  browser sessions and fresh local/Remote UI HTTP sessions.
- The deploy runbook warns not to deploy from a normal dashboard page and to
  require `hass.connected === true` plus a File Editor ingress iframe before
  writing through the browser deploy helper.
- Existing garage and entry-security notifications covered open garage doors
  and the mudroom lock at night, but did not provide a home/overnight exterior
  light reminder.

## Evidence Collected

- The local terminal path to `homeassistant.local:8123` was DNS-blind from this
  Mac during the check.
- Safari showed disconnected local Home Assistant tabs while a Remote UI File
  Editor tab was connected and had a mounted File Editor ingress iframe.
- Home Assistant history for the Sunday overnight window showed Remote UI
  availability flaps, including longer `remote_disconnected` windows around
  2:05-2:16am ET and 7:31-7:48am ET on Monday, June 8.
- `sensor.home_assistant_remote_access_status` also moved through
  disconnected/online states during the same overnight and morning window.
- Recorder history showed `switch.exterior_mud_room_stairs` on through the
  overnight schedule, off around 11:53pm ET, back on around midnight, and off
  again around 6:46am ET.
- Recorder history showed `switch.garage_garage_lights` briefly on around
  8:32pm ET and again briefly around 7:46am ET. It did not show the garage
  switch staying on all night.
- `automation.lights_garage_light_auto_off` was enabled, but its
  `last_triggered` timestamp was June 5, 2026, so it had not fired during the
  observed Sunday night window.
- `binary_sensor.g6_instant_motion_3` was unavailable during the inspected
  window. The garage person and vehicle sensors were available for most of the
  window and off except for a short morning person-detection event.

## Ranked Findings

1. High confidence: the mobile loading/blank symptom fits the prior access-layer
   pattern more than a dashboard YAML regression. Local tabs were disconnected,
   while one Remote UI File Editor session was connected.
2. High confidence: the mudroom exterior light was allowed back into the normal
   door-light schedule after All Off/overnight state. Bedtime had a sleep
   override path, but the exterior shutoff behavior needed to be made explicit
   for the door-light schedule and for all relevant exterior utility lights.
3. High confidence: there was no dedicated late-night exterior-light reminder
   for garage/mudroom/deck/yard lights while someone was home. Existing
   security reminders were mostly away-security, garage-door, or lock-focused.
4. Medium-high confidence: the garage auto-off automation needed a periodic
   watchdog trigger. The existing state triggers were correct for normal state
   flow, but a reload, missed state edge, or unavailable motion entity could
   leave no new trigger to evaluate the quiet-garage conditions.
5. Medium confidence: the user's observation of garage lights left on all night
   may have been a stale UI state, another garage/exterior light, or a recorder
   gap. The recorded `switch.garage_garage_lights` state did not show a
   sustained overnight on period.

## Changes Made

- Added a five-minute watchdog, Home Assistant start, and automation-reload
  triggers to `automation.lights_garage_light_auto_off`, preserving its existing
  "garage light on for at least five minutes and no recent garage activity"
  conditions.
- Added `input_datetime.late_night_exterior_lights_last_notified_at` as the
  durable timestamp guard for late-night exterior-light reminders.
- Added `automation.lights_late_night_exterior_lights_left_on`, which checks at
  10:30pm ET, on relevant light-on events, on restart/reload, and every 15
  minutes overnight, but sends at most hourly while watched exterior lights
  remain on.
- Added a mobile action handler for `Turn off exterior`, calling
  `script.lights_late_night_exterior_off`, and a clear automation to remove the
  notification once the watched lights are off.
- Added `script.lights_late_night_exterior_off`, which turns off garage and
  exterior utility lights while preserving front door lights.
- Updated Bedtime and All Off so the mudroom exterior stairs, deck lights,
  exterior deck lights, side/yard lights, back patio light, garage light, and
  uplight are part of the exterior sleep/off behavior, while front door sconces
  remain excluded.
- Updated All Off so the front-stairs sleep override also follows the
  door-light schedule, not only the front-stairs schedule.

## Checks And Live Validation

- Reviewed prior audit history and the remote-access/UI hardening runbooks.
- Parsed edited YAML with Ruby for `configuration.yaml`, `scripts.yaml`, and
  `automations/10-lighting-security.yaml`.
- Ran `git diff --check`.
- Ran `python3 tools/check_device_inventory_coverage.py`; coverage passed with
  79 active control entity references recorded.
- Deployed `configuration.yaml`, `scripts.yaml`, and
  `automations/10-lighting-security.yaml` through a connected Remote UI File
  Editor ingress tab.
- Browser deploy read back each written file byte-for-byte and Home Assistant
  returned `check_config` result `valid` with no errors or warnings.
- Reloaded `input_datetime` so the new timestamp helper appeared live.
- Reloaded automations and verified the live automation config contained the
  garage watchdog, the exterior deck light, and the durable timestamp helper.
- Verified the live script `script.lights_late_night_exterior_off` exists.

## Deployment Status

- Live deployment completed through File Editor read-back.
- Home Assistant config check was valid.
- The new script, helper, and automations were visible in live Home Assistant
  state after reload.

## Residual Risks And Follow-Ups

- The garage primary motion entity `binary_sensor.g6_instant_motion_3` was
  unavailable during the inspected window. If garage auto-off behavior still
  feels wrong, inspect why that Protect motion entity is unavailable.
- If the user sees garage lights on overnight again, compare the physical light,
  dashboard card, and recorder state at that moment to distinguish stale UI from
  a second entity or recorder gap.
- Continue treating local/cloud handoff failures as an access-layer incident
  unless both `/ha-safe/home` and `/calm-mobile/home` behave differently.
