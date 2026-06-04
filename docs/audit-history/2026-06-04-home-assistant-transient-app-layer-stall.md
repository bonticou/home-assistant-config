# Home Assistant Transient App-Layer Stall

## Symptom And Impact

Home Assistant appeared to have loading issues again after earlier memory and
dashboard hardening work. The user reported that the UI later seemed to come
back without an obvious manual recovery step.

## Relevant Prior Context

- Earlier 2026-06-04 availability work separated dashboard/frontend failures
  from access-layer and backend availability failures.
- `/ha-safe/home` exists as a stock diagnostic dashboard. If both `/ha-safe/home`
  and `/calm-mobile/home` fail the same way, the main custom dashboard is not
  the lead suspect.
- Prior memory cleanup reduced one class of frontend/runtime risk, but does not
  prevent Home Assistant Core, the HTTP server, Supervisor, or the Remote UI
  path from stalling.

## Evidence Collected

- External Remote UI probe around 6:42pm ET:
  - DNS and TCP reached the Remote UI host;
  - TLS failed with an EOF before normal HTTP/dashboard loading;
  - `/`, `/ha-safe/home`, `/calm-mobile/home`, and websocket all failed before
    dashboard rendering.
- Local network checks around the same time:
  - `homeassistant.local` answered ping quickly;
  - TCP port `8123` accepted connections;
  - local HTTP returned no bytes within an 8-second timeout;
  - local probe to `/`, `/ha-safe/home`, `/calm-mobile/home`, and websocket
    timed out.
- Recovery check around 7:13pm ET:
  - local `/`, `/ha-safe/home`, `/calm-mobile/home`, startup resources, and
    websocket all returned OK;
  - Safari Remote UI `calm-mobile` had `hass.connected: true` and loaded live
    state;
  - a terminal Remote UI probe still showed a certificate-verification issue,
    but Safari and a curl check confirmed the remote server was responding.

## Ranked Findings

1. High confidence: this was not caused by the normal `calm-mobile` dashboard.
   The stock safe dashboard and the root shell failed the same way during the
   bad window.
2. High confidence: this was not explained by frontend memory alone. Local TCP
   worked, but HTTP and websocket did not answer promptly.
3. Medium-high confidence: the active failure was a transient Home Assistant
   Core/app-layer, Supervisor/proxy, host overload, or Remote UI path stall.
4. Medium confidence: because the system recovered without a config change, the
   next useful step is log and host-health capture during the next bad window,
   not another blind dashboard trim.

## Changes Made

- No configuration changes were made for this incident.
- No restart was performed during this check.

## Checks And Live Validation

- Ran the external Remote UI probe with safe-dashboard comparison.
- Ran the same probe against local `homeassistant.local:8123`.
- Confirmed local ping and TCP reachability during the bad window.
- Confirmed local HTTP/websocket recovery after the user reported it was back.
- Confirmed Safari had a connected Remote UI tab after recovery.

## Deployment Status

- No deployment was needed.

## Residual Risks And Follow-Ups

- During the next recurrence, capture HA Core/Supervisor logs and host resource
  health while local TCP works but HTTP/websocket stall.
- Compare Remote UI, local `/ha-safe/home`, and local `/calm-mobile/home`
  before changing dashboard code.
- Consider adding a lightweight local app-layer watchdog if this repeats: ping
  alone is insufficient because the host can answer ping while HA HTTP is stuck.
