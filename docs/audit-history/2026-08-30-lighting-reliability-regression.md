# Lighting Reliability Regression, 2026-08-30

## Symptom And Impact

Trevor reported two major lighting reliability failures:

- Casey's closet light has not been reliably turning on from closet motion.
- A non-exempt light, including the office light, was left on overnight despite the midnight reminder and 1 AM shutoff design.

The impact is trust erosion in the lighting layer: motion lights can miss, and lights that should never be found on in the morning can remain on.

## Relevant Prior Context

- [2026-08-24 Casey closet motion stale](2026-08-24-casey-closet-motion-stale.md) already identified stale UniFi motion as one failure mode and a nonresponsive Lutron command path as a separate risk.
- [2026-08-22 Overnight lights timestamp guard](2026-08-22-overnight-lights-timestamp-guard.md) fixed an earlier false guard where the reminder fired but the 1 AM auto-off did not run.
- [2026-06-25 Casey closet Lutron bridge disconnect](2026-06-25-casey-closet-lutron-bridge-disconnect.md) found an older case where motion reached HA but Lutron service calls failed.
- [2026-06-10 Overnight lights sweep](2026-06-10-overnight-lights-sweep.md) created the midnight reminder, snooze, and guarded 1 AM shutoff.

## Evidence Collected

- `automation.lights_overnight_left_on_auto_off` was enabled, but its live `last_triggered` remained `2026-08-25T05:00:00Z`, so it had not been running on later nights.
- `sensor.overnight_lights_left_on` reported active non-exempt lights while its `auto_off_guard` was `up_late_media`.
- `media_player.family_room_tv_2` was merely `paused`, not actively playing. The old template treated any non-off/non-idle media state as up-late media, so a stale paused TV could block the 1 AM shutoff indefinitely.
- Live verification after the fix showed the same paused media player with `sensor.overnight_lights_left_on.attributes.auto_off_guard` now `clear`.
- `automation.lights_casey_s_closet_auto_off` and `automation.lights_casey_s_closet_motion_stale_recovery` were enabled.
- `binary_sensor.casey_s_closet_motion` had not reported motion since `2026-08-29T15:43:14Z`, while motion detection was enabled and battery was healthy.
- Direct HA `light.turn_on` tests against `light.master_casey_s_closet` did not change the light state, even after reloading the light's config entry. This indicates that the closet miss is not only an automation trigger problem; the Lutron device/control path is also failing to respond.

## Findings

1. High confidence: the overnight auto-off was blocked by an overbroad media guard.

   A stale or paused Family Room TV state counted as `up_late_media`. That protected against interrupting someone watching TV, but it also prevented the 1 AM sweep when the TV was not actually playing.

2. High confidence: the overnight sweep needed a second-pass and failure alert.

   Even with the guard corrected, the script previously sent one `turn_off` per entity and had no explicit failure notification if lights were still on afterward.

3. High confidence: Casey's closet still has a real device/control-path problem.

   Motion stale recovery is necessary but not sufficient. HA currently accepts the light service call, but the Lutron light state does not move. The automation must verify success and escalate instead of silently pretending it worked.

4. Medium confidence: the Casey motion feed may still be stale.

   The motion sensor's last state change is old enough to justify recovery checks, but without a live walk test during the incident, the command-path failure is the stronger direct evidence.

## Changes Made

- Narrowed `sensor.overnight_lights_left_on.attributes.auto_off_guard` so only explicit guest override, vacation mode, TV scene/hold, or actively `playing` Family Room TV blocks the 1 AM shutoff. A paused/stale media state no longer blocks.
- Hardened `script.lights_overnight_sweep_off` to:
  - run a first fault-tolerant off pass;
  - wait for state convergence;
  - run a second fault-tolerant off pass for anything still on;
  - notify Trevor if lights remain on after both attempts.
- Updated `automation.lights_clear_overnight_left_on_reminder` to clear the new sweep-failed notification once watched lights reach zero.
- Hardened `automation.lights_casey_s_closet_auto_off` so the motion-on branch:
  - retries the light turn-on;
  - reloads the Lutron config entry once if the light still does not report on;
  - retries after reload;
  - sends a time-sensitive diagnostic push if HA still cannot get the Lutron light to turn on.
- Added automatic clearing for the Casey closet command-failed notification once the light reports on.
- Follow-up everyday-lighting audit found that the passive `overnight_lights_clear_when_off` path cleared the original reminder but not the newer sweep-failed notification. The clear path now clears both tags once the watched light count reaches zero.

## Checks And Live Validation

- Local YAML parsing passed for:
  - `configuration.yaml`
  - `automations/10-lighting-security.yaml`
  - `scripts.yaml`
- `git diff --check` passed.
- Live File Editor deploy completed with read-back hash verification for:
  - `/homeassistant/configuration.yaml`
  - `/homeassistant/automations/10-lighting-security.yaml`
  - `/homeassistant/scripts.yaml`
- Home Assistant `check_config` returned valid.
- Reloads succeeded:
  - `template.reload`
  - `automation.reload`
  - `script.reload`
- Live post-reload verification showed:
  - `sensor.overnight_lights_left_on.attributes.auto_off_guard: clear`
  - `automation.lights_overnight_left_on_auto_off: on`
  - `script.lights_overnight_sweep_off: off`
  - `automation.lights_casey_s_closet_auto_off: on`
  - `automation.lights_casey_s_closet_motion_stale_recovery: on`

## Deployment Status

Deployed live through the authenticated local Home Assistant route and reloaded in memory.

## Residual Risks And Follow-Ups

- Casey's closet may still require physical Lutron troubleshooting or re-pairing because direct HA light commands did not change the light state after a config-entry reload.
- The next real 1 AM window should be checked to confirm the auto-off automation now triggers with `auto_off_guard: clear`.
- If another non-exempt light is found on overnight, inspect whether the failure is guard suppression, service-call failure, entity omission from `sensor.overnight_lights_left_on`, or HA availability during the 1 AM to 6 AM watchdog window.
- The next best hardening slice is to bring garage auto-off, late-night exterior off, Bedtime, and All Off closer to the overnight sweep pattern: fault-tolerant first pass, short convergence delay, second pass, and explicit failure visibility for lights that still report on.
