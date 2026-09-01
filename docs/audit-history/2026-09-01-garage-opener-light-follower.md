# Garage Opener Light Follower, 2026-09-01

## Symptom And Impact

Trevor noticed that the garage door opener lights were still not shutting off
when the main garage light switch was turned off. The expected behavior is that
the opener lights should not remain on once the main garage lights are off.

## Relevant Prior Context

- On 2026-08-30, the garage opener follower rule was added to the repo in
  `automations/10-lighting-security.yaml`, but live deployment was blocked
  because File Editor did not mount in the available browser session.
- The same automation file already contains the garage five-minute auto-off
  rule, late-night exterior checks, and overnight light sweep logic.

## Evidence Collected

- The repo contains `automation.garage_opener_lights_follow_main_off` next to
  the garage auto-off rule.
- The follower rule listens for `switch.garage_garage_lights` turning off,
  opener lights turning on while the main switch is off, Home Assistant start,
  automation reload, and a one-minute watchdog.
- Because the one-minute watchdog would catch the condition even if the
  original switch-off transition was missed, the observed live failure strongly
  suggests the prior follower rule was not deployed or not reloaded live.
- Local `homeassistant.local` was not resolvable from the browser or terminal.
- The last known local HA IP accepted TCP on port 8123, but HTTP reset after
  the request was sent.
- The in-app browser loaded a Home Assistant shell on the Nabu route but did
  not attach a connected `hass` object or mount the File Editor iframe.
- Safari initially had no open tabs. After opening the Nabu File Editor route,
  the Safari deploy helper still could not find Home Assistant auth in local
  storage.
- After Trevor logged into Safari, the Home Assistant auth data was available
  through the live `home-assistant` element rather than `localStorage`, so the
  Safari deploy helper was adapted locally to use the current frontend auth
  object.

## Findings

1. High confidence: the repo rule is structurally correct but was not live.

   The automation has a one-minute state watchdog. If it had been loaded and
   enabled, opener lights that remained on while the main garage light was off
   should have been turned off without waiting for a new switch event.

2. Medium confidence: live deployment/auth path remains the active blocker.

   Both local and Nabu browser routes failed to provide a mounted File Editor
   surface during this investigation, and the local long-lived token available
   in scratch was no longer authorized.

3. High confidence: the rule should use visible failure handling.

   Even after deployment, opener lights are ESPHome/garage-controller devices
   and can fail to accept a command. The rule should retry once and notify
   Trevor if Home Assistant still sees the opener lights on.

## Changes Made

- Hardened `garage_opener_lights_follow_main_off` so it now:
  - turns both opener lights off when the main garage light is off;
  - waits three seconds for state convergence;
  - retries any opener light still reporting on;
  - waits five seconds;
  - sends a time-sensitive diagnostic notification if either opener light still
    reports on after both attempts.

## Checks

- Local Ruby YAML parse passed for `automations/10-lighting-security.yaml`.
- `git diff --check` passed for `automations/10-lighting-security.yaml`.

## Deployment Status

Deployed live on 2026-09-01 through the authenticated Safari/Nabu File Editor
ingress path after Trevor logged into Home Assistant.

Live deploy checks passed:

- `/homeassistant/automations/10-lighting-security.yaml` written and read back
  with SHA-256 `332a25cb97b9fe3f8975dcd97d71be21134b578da28d0b4d3c2feac8ad7822ef`.
- Home Assistant `check_config` returned `valid` with no errors or warnings.
- `automation.reload` returned HTTP 200.
- Live state check showed
  `automation.lights_garage_opener_lights_follow_main_off` was `on`.
- Live state check showed `switch.garage_garage_lights`,
  `light.ratgdo32_4536e8_light`, and
  `light.ratgdo32disco_c26634_light` were all `off`.

## Residual Risks And Follow-Ups

- During the next real garage use, verify that turning off
  `switch.garage_garage_lights` turns off both opener lights immediately.
- If either opener light still stays on, inspect whether the opener firmware is
  reasserting its own light state after HA turns it off.
