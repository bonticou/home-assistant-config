# Housekeeper Away-Security Suppression

Date: 2026-07-29

## Symptom And User Impact

The away-security reminder could notify Trevor that lights were on or entry
points were unsecured while the expected housekeeper visit was in progress.
Those routine away-state conditions are expected during the visit and are not
actionable from away.

## Relevant Prior Context

- `binary_sensor.away_motion_security_housekeeper_window` already represents the
  expected Tuesday visit window from 7:45 AM through 3:00 PM.
- Away-motion alerts already respect that window.
- The broader `Security — House Unsecured While Away` automation did not use
  the housekeeper window, so its away-security and Casey-left notification tags
  could still fire.
- Leak, fire, appliance-error, and other safety notification systems are
  separate and must remain active.

## Evidence And Findings

1. **High confidence:** `away_security_unsecured_reminder` evaluated entry
   points and active lights whenever both tracked residents were away, without
   checking the housekeeper window.
2. **High confidence:** the automation can emit four related notification tags:
   the general away-security alert plus Casey-left combo, entry, and lights
   alerts.
3. **High confidence:** the existing housekeeper binary sensor is the narrowest
   shared source of truth and avoids creating another schedule or helper.

## Changes Made

- Added housekeeper-window start and end triggers to
  `away_security_unsecured_reminder`.
- During the active window, the automation clears all four related notification
  tags and stops before sending a routine away-security reminder.
- When the window ends, the automation reevaluates immediately. If both
  residents remain away and an entry point or monitored light is still active,
  normal notification logic resumes.
- Preserved the existing away-security snooze behavior.
- Did not change Flo leak protection, fire alerts, appliance errors, camera
  alerts, or other safety-critical notification paths.

## Checks

- Ruby/Psych parsed `automations/10-lighting-security.yaml`.
- A targeted structural check confirmed:
  - housekeeper-window start and end triggers;
  - all four related notification-clear actions;
  - the stop action that prevents sends while the window is active.
- `python3 tools/check_device_inventory_coverage.py` passed with all 91 active
  control references covered.
- `git diff --check` passed.
- Live File Editor write/read-back matched the generated SHA-256 payloads for:
  - `/homeassistant/automations.yaml`;
  - `/homeassistant/automations/10-lighting-security.yaml`.
- Home Assistant configuration validation returned `valid` with no errors or
  warnings.
- The deploy helper's short reload calls timed out, but a follow-up targeted
  `automation.reload` completed successfully.
- The live automation config API confirmed both housekeeper triggers, the
  shared window entity, all four clear actions, and the suppression stop action.
- `automation.security_house_unsecured_while_away` was live and enabled.
- `binary_sensor.away_motion_security_housekeeper_window` was `off`, as expected
  outside the Tuesday visit window.

## Deployment Status

Deployed live on 2026-07-29 through the authenticated Nabu Casa File Editor
ingress route with byte-for-byte read-back, valid config check, targeted
automation reload, and live automation-config verification.

## Residual Risks And Follow-Up

- The suppression follows the existing scheduled window, not live
  person-detection. An unusual visit outside that window still requires the
  existing manual pause controls.
- The 3:00 PM end trigger intentionally sends a reminder immediately when an
  away-security issue remains.
- No synthetic live push was generated because the housekeeper window was not
  active; the active-window branch was verified structurally and through the
  live automation definition.
