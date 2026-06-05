# Remote UI And Fresh HTTP Stall

## Symptom And Impact

Home Assistant appeared to come back in some Safari/local views while other
routes still looked disconnected. File Editor Remote UI tabs lost their mounted
ingress iframe, and fresh browser or terminal loads could not reliably fetch
Home Assistant pages.

## Relevant Prior Context

- Earlier 2026-06-04 audits separated dashboard/frontend failures from
  Home Assistant app-layer and Nabu Casa Remote UI failures.
- The deploy runbook warns that a page can show stale state with
  `hass.connected === false` and that terminal HTTP to the LAN address can be
  less reliable than an already-connected browser session.
- The Remote UI watchdog exists and calls `cloud.remote_connect` when
  `binary_sensor.remote_ui` is off.

## Evidence Collected

- Safari showed local Home Assistant tabs with `hass.connected: true`.
- Safari showed Remote UI File Editor tabs with `hass.connected: false` and no
  `/api/hassio_ingress/` iframe.
- Local ping to the Home Assistant host succeeded with low latency.
- TCP port `8123` accepted connections locally.
- Fresh local HTTP GETs to `/` and `/ha-safe/home` connected quickly but
  returned zero bytes before the 8-second timeout.
- A direct-IP local HTTP GET behaved the same way, ruling out mDNS as the main
  explanation.
- A fresh in-browser `fetch()` from an existing connected local dashboard tab
  also remained queued.
- The existing local frontend websocket still received fresh state updates,
  including gateway CPU/memory, Ting voltage, and notice-history timestamps.
- External Remote UI probing reached DNS and TCP, then failed TLS with
  `UNEXPECTED_EOF_WHILE_READING` for `/`, `/calm-mobile/home`, `/ha-safe/home`,
  and websocket.
- Home Assistant state showed:
  - `binary_sensor.remote_ui`: `off`;
  - `sensor.home_assistant_remote_access_status`: `remote_disconnected`;
  - watchdog recovery attempt at about 9:40pm ET;
  - degraded status at about 9:44pm ET.
- A manual `cloud.remote_connect` call from an existing connected local tab
  returned successfully, but `binary_sensor.remote_ui` stayed `off` during the
  follow-up window.

## Ranked Findings

1. High confidence: this was not caused by the espresso popup styling change or
   the normal `calm-mobile` dashboard content. Both stock and custom fresh HTTP
   page loads were affected.
2. High confidence: the Home Assistant host and network path were not fully
   down. Ping and TCP worked, and an existing websocket continued to receive
   live state.
3. High confidence: Nabu Casa Remote UI was disconnected at the same time.
4. Medium-high confidence: the active failure mode was a split app-layer state:
   existing websocket sessions could keep receiving events while new HTTP/TLS
   sessions stalled or failed.
5. Medium confidence: this is related to the prior transient app-layer stall
   pattern, not simply frontend memory pressure. Memory cleanup helped one risk
   class but did not prevent HTTP/Remote UI tunnel stalls.

## Changes Made

- No configuration changes were made.
- Called `cloud.remote_connect` once from an existing connected local frontend
  session. The call returned successfully, but the Remote UI sensor did not
  recover during the observed follow-up window.

## Checks And Live Validation

- Ran local and Remote UI health probes with safe-dashboard comparison.
- Checked Safari tabs for `hass.connected` and mounted File Editor ingress
  iframes.
- Confirmed fresh local HTTP hangs using both hostname and direct IP.
- Confirmed existing websocket state was still fresh by checking recent entity
  timestamps in the connected local frontend.

## Deployment Status

- No deployment was performed.

## Residual Risks And Follow-Ups

- During the next recurrence, collect HA Core and Supervisor logs while fresh
  HTTP requests are hanging but existing websocket state remains live.
- Inspect whether Nabu Casa Remote UI disconnects before, after, or exactly
  alongside the local fresh-HTTP stall.
- Consider a lightweight local app-layer watchdog that checks fresh HTTP and
  websocket establishment, not only ping or existing frontend state.
- Keep using a connected local browser/websocket path for urgent live checks
  while Remote UI is off.
