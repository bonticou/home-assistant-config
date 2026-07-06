# File Editor Ingress 401 After Update

## Symptom And Impact

On July 6, 2026, immediately after Home Assistant update work, the File Editor
add-on update completed but the File Editor panel did not load through the Nabu
Casa Remote UI route.

User impact: the normal live deploy path was blocked even though Home Assistant
itself and the dashboard were reachable.

## Relevant Prior Context

- The repo deploy runbook depends on a mounted File Editor ingress iframe for
  safe browser-mediated live edits.
- Prior June remote-access incidents showed that Nabu Casa, browser session
  handoff, and ingress state can fail independently of Home Assistant Core.
- Earlier on July 6, the Remote UI route and local Mac DNS/TLS path were
  intermittently unstable during the Core/OS update window.

## Evidence Collected

- `update.file_editor_update` reported:
  - state: `off`;
  - installed version: `6.0.0`;
  - latest version: `6.0.0`;
  - update not in progress.
- Supervisor websocket add-on info for `core_configurator` reported:
  - add-on name: File editor;
  - version: `6.0.0`;
  - state: `started`;
  - ingress enabled;
  - ingress panel enabled;
  - update available: false.
- The File Editor HA panel route loaded and HA frontend was connected.
- The File Editor ingress iframe mounted full-size, but its body showed
  `401: Unauthorized`.
- The iframe path saw three `ingress_session` cookies, each 128 characters,
  indicating duplicate/stale browser-side ingress session state.

## Ranked Findings

1. **Stale/duplicate ingress session cookies blocked File Editor. Confidence:
   high.**

   Evidence: the add-on was started and current, but the iframe returned
   `401: Unauthorized`; after clearing duplicate ingress cookies and setting one
   fresh Supervisor ingress session, the iframe loaded File Editor normally.

2. **File Editor add-on update itself succeeded. Confidence: high.**

   Evidence: HA update entity and Supervisor add-on info both reported
   `6.0.0` installed/latest with no update pending.

3. **This was not a YAML/configuration failure. Confidence: high.**

   Evidence: failure was isolated to the browser-side ingress authorization
   layer; no HA configuration files were changed to restore access.

## Changes Made

- No Home Assistant configuration changes.
- No repository configuration changes.
- Browser-side recovery only:
  - cleared stale `ingress_session` cookies for likely HA ingress paths;
  - requested a fresh Supervisor ingress session through the authenticated HA
    frontend;
  - set one fresh `ingress_session` cookie on the File Editor ingress path;
  - reloaded the File Editor iframe.

Temporary uncommitted helpers were used under `.tmp/` to read and repair the
browser session. They intentionally remain scratch files.

## Validation

- Confirmed File Editor iframe changed from `401: Unauthorized` to the
  HASS Configurator UI.
- Confirmed the iframe title became `calm_mobile.yaml - HASS Configurator`.
- Confirmed only one `ingress_session` cookie was visible at the File Editor
  iframe path after repair.

## Deployment Status

File Editor is usable again through the authenticated Safari/Nabu Remote UI
session. No Home Assistant restart was required.

## Residual Risks And Follow-Ups

- If File Editor fails after future add-on or OS updates with `401:
  Unauthorized`, first suspect stale duplicate `ingress_session` cookies before
  restarting HA or changing config.
- If this becomes common, add a documented operator recovery snippet to
  `docs/home-assistant-deploy-runbook.md` under File Editor ingress recovery.
- Avoid broad HA restarts for this symptom unless the add-on is not `started` or
  Supervisor cannot mint an ingress session.
