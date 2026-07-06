# Matter Server 9.0.4 Post-Update Validation

## Symptom And Impact

On July 6, 2026, after updating Matter Server to `9.0.4`, the release notes
flagged a migration-class change from the old Python Matter Server to the new
matter.js-based implementation introduced in `9.0.0`.

User impact: Matter-backed locks are operationally important, and the release
notes warned about first-start migration time, watchdog behavior, and higher
RAM needs.

## Relevant Prior Context

- The June 6 backend availability audit reviewed Matter Server logs and found
  stale websocket no-PONG warnings before reboot but no add-on restart loop.
- The July 6 update work also included Core/OS/add-on updates and exposed a
  separate File Editor ingress-session issue, so post-update add-on state needed
  to be interpreted carefully.

## Evidence Collected

- Supervisor reported Matter Server:
  - slug: `core_matter_server`;
  - version: `9.0.4`;
  - latest version: `9.0.4`;
  - state: `started`;
  - stage: `stable`;
  - update available: false;
  - watchdog: false;
  - beta option: false;
  - log level: `info`.
- `update.matter_server_update` reported:
  - state: `off`;
  - installed version: `9.0.4`;
  - latest version: `9.0.4`;
  - in progress: false.
- Active Matter entities refreshed after the update:
  - `lock.mudroom_door_lock`: `locked`;
  - `lock.garage_entry_lock`: `unlocked`;
  - mudroom lock battery: `96%`;
  - garage entry lock battery: `95%`;
  - both lock operating modes: `normal`.

## Ranked Findings

1. **No immediate Matter integration change is required. Confidence: high.**

   Evidence: the add-on is started on `9.0.4`, the update entity is clean, beta
   is off, watchdog is off, and the two active Matter locks are reporting fresh
   states.

2. **The first-start migration appears to have completed. Confidence: high.**

   Evidence: Matter Server reached `started` state on the new version and live
   Matter entities refreshed after the migration window.

3. **Resource monitoring remains worthwhile. Confidence: medium.**

   Evidence: Matter `9.0.0` release notes warned about higher RAM needs, while
   `9.0.4` specifically included RAM/CPU optimizations. No resource change was
   made during this validation.

## Changes Made

- No Home Assistant configuration changes.
- No Matter add-on option changes.
- No Matter entities, devices, or dashboards changed.

## Validation

- Read Supervisor Matter Server status through the authenticated HA frontend.
- Read the Matter Server update entity and key Matter device states.
- Confirmed the active Matter locks were not `unknown` or `unavailable`.

## Deployment Status

Matter Server is updated and running. No restart or remediation was required.

## Residual Risks And Follow-Ups

- Watch host CPU/RAM over the next day because Matter Server `9.x` changed the
  runtime architecture.
- If Matter devices become stale, first check Matter Server logs and lock states
  before changing add-on options.
- Do not enable beta or BLE proxy unless there is a specific commissioning need.
