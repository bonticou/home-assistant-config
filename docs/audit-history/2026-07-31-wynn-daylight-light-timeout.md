# Wynn Daylight Light Timeout

Date: 2026-07-31

## Symptom

One of Wynn's room lights remained on during daylight after the room camera had
not apparently detected activity for roughly 20 to 30 minutes.

## Relevant Prior Context

- `automation.wynn_room_daylight_camera_quiet_auto_off` turns Wynn's room lights
  off only during daylight and while vacation mode is off.
- The automation considers both the camera motion and person-detected entities.
- A five-minute watchdog covers missed state triggers and restart/reload cases.

## Evidence And Finding

The committed rule required 30 full minutes without camera activity. Because
the watchdog runs every five minutes, its practical watchdog shutoff window was
approximately 30 to 35 minutes. A light still being on after roughly 20 to 30
minutes therefore did not necessarily indicate an automation failure.

High confidence: a 20-minute quiet threshold better matches the desired daytime
behavior while retaining the existing motion, daylight, and vacation safeguards.

Live trace evidence was not available during this change because the local Home
Assistant route was unreachable from the browser session and no signed-in
remote session was open.

## Changes Made

- Reduced the camera-off trigger from 30 minutes to 20 minutes.
- Reduced the light-on fallback trigger from 30 minutes to 20 minutes.
- Reduced the watchdog's last-activity threshold from 30 minutes to 20 minutes.
- Updated the automation description to match the new policy.

The five-minute watchdog remains unchanged, so the practical watchdog shutoff
window is approximately 20 to 25 minutes after the latest camera activity.

## Checks And Deployment Status

- Local YAML parsing passed for `automations/10-lighting-security.yaml`.
- Git whitespace validation passed.
- Not deployed live during this change.

## Residual Risks And Follow-Up

- A camera motion or person-detected entity stuck in `on` will continue to block
  shutoff, intentionally avoiding turning the room dark while occupancy is still
  reported.
- Confirm the live automation reload after deployment, then verify a daylight
  shutoff within approximately 20 to 25 minutes of the latest camera activity.
