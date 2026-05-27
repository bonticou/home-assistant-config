# Home Assistant Mobile Disconnect Audit

Date: 2026-05-26

## Summary

This audit treats the iOS Home Assistant open failure as an availability issue.
The screenshots show two related failure modes: a blank Home Assistant app shell
and the companion app's "You're disconnected" screen. Trevor confirmed the
issue occurs on both home Wi-Fi and away/cellular paths and usually clears only
after waiting minutes.

The strongest current finding is not a dashboard YAML error. From this Mac,
both the cached LAN path to Home Assistant and the known Nabu Casa Remote UI
path are routed through a `utun6` tunnel at `100.64.0.1`. TCP connects, but HTTP
or TLS is reset before Home Assistant can respond. That gives a reproducible
connection-class failure from the audit environment, but it is not enough by
itself to prove the iPhone's same failure, because the Mac is not on the same
network path as the phone.

No configuration or dashboard files were changed as part of this audit. This
report is evidence-first and supersedes the May 23 load audit for the mobile
disconnect incident, while preserving its frontend-load findings as secondary
risk.

## Evidence Collected

### Live incident update: 2026-05-27 08:53 EDT

Trevor reproduced the failure while remote and then opened the same remote path
in iPhone Safari. Safari showed the Nabu Casa/Home Assistant fallback page:

- "Unable to connect to Home Assistant."
- "Retrying in 54 seconds..."
- "It is possible that you are seeing this screen because your Home Assistant is
  not currently connected."

This is decisive new evidence: the incident is not limited to the Home
Assistant iOS app, a stale app WebView, or the custom dashboard. The remote
Nabu Casa page is reachable, but Nabu Casa cannot connect through to Trevor's
Home Assistant instance.

At roughly the same window, public status pages showed no broad cloud outage:

- [Nabu Casa status](https://status.nabucasa.com/) showed America Remote Access
  operational and no May 27 incident.
- [Home Assistant status](https://status.home-assistant.io/) showed Home
  Assistant Cloud and Remote UI operational and no May 27 incident.

Current lead: Trevor's HA instance, home internet path, or HA Cloud connection
is offline or disconnected from Nabu Casa during the incident window.

### Reliability fix added: 2026-05-27

Follow-up implementation now adds a first safety layer for this failure mode:

- `Home Assistant — Remote UI Watchdog` watches `binary_sensor.remote_ui`, calls
  `cloud.remote_connect` at most once every 15 minutes while Remote UI is down,
  and records degraded/restored/recovery-attempt timestamps.
- `sensor.home_assistant_remote_access_status` summarizes Remote UI state and
  nearby HA/WAN context for the next incident.
- `tools/ha_remote_health_probe.py` provides an outside-HA probe that detects
  the Nabu Casa fallback page and treats a websocket `auth_required` greeting as
  proof that the request reached HA.
- `docs/home-assistant-remote-access-runbook.md` documents the manual recovery
  path and evidence to capture next time.

### User-visible symptom

- Screenshot at 10:05 AM on 2026-05-26 shows a blank dark Home Assistant app
  shell with only the iOS status bar visible.
- Second screenshot at 10:05 AM on 2026-05-26 shows the Home Assistant iOS
  companion app "You're disconnected" state.
- Trevor confirmed the issue happens on both local and remote use and usually
  clears only after waiting minutes.

### Repo and config surface

- `configuration.yaml` does not define `http:`, `external_url`,
  `internal_url`, `trusted_proxies`, `use_x_forwarded_for`, SSL settings, or a
  reverse proxy. Therefore URL selection and remote access truth are live/UI
  managed, companion-app managed, or network managed rather than visible in this
  repo.
- YAML dashboard mode is configured for `calm-mobile` in
  `configuration.yaml`; repo-owned frontend resources are limited to the local
  custom cards listed there.
- HACS resources, Browser Mod injection, and any `.storage` Lovelace resource
  truth are not fully represented in repo YAML.

### Live reachability from this Mac

The current Mac network is not a clean home-LAN vantage point:

- Default route is via Wi-Fi gateway `10.60.172.1`.
- Route to the cached HA LAN address goes through `utun6` via `100.64.0.1`.
- Route to the known Nabu Casa Remote UI IP also goes through `utun6` via
  `100.64.0.1`.
- `ps aux` showed a Zscaler tunnel process running.

Endpoint probes from this Mac:

| Target | Result |
| --- | --- |
| `127.0.0.1:8123` | Refused connection |
| `homeassistant:8123` | DNS lookup failed |
| `homeassistant.local:8123` | Timed out / no mDNS result |
| Cached HA LAN address, port `8123` | TCP connect succeeded, HTTP request reset by peer after request was sent |
| Cached HA LAN address, port `443` | TCP connect succeeded, TLS reset after ClientHello |
| Known Nabu Casa Remote UI host, port `443` | TCP connect succeeded, TLS failed immediately after ClientHello with `SSL_ERROR_SYSCALL` |
| Remote UI websocket probe with local token | Failed with websocket `error` before authenticated API results |
| In-app browser remote UI navigation | Browser automation hung during navigation and reset; no usable DOM/console evidence captured |

The reset-after-connect pattern is important. It means the audit machine can
reach something at the target IP/port, but the path does not deliver a normal HA
HTTP or TLS session.

### Cached live HA state

Cached live exports are stale but useful for baseline risk:

- Latest parsed live API export is from 2026-05-20.
- Remote UI was `on` in the cached export.
- Home Assistant Core was `2026.3.4`; `2026.5.3` was available.
- Supervisor was `2026.05.0`; OS was `17.3`.
- Trevor's iPhone companion app version was `2026.4.1`.
- Cached iPhone connection state showed Wi-Fi, but the cached export is not
  from the 2026-05-26 failure window.
- Cached router state identified Home Assistant at a private LAN address and
  host name `homeassistant`.

No current HA logs or current `/api/config` response could be fetched from this
Mac because both local and remote paths failed before a normal HTTP/API
response.

### Frontend and dashboard shape

Current dashboard facts:

- `dashboards/calm_mobile.yaml` has 12,834 lines.
- It contains 7 views.
- The Home view currently has 28 top-level cards.
- The full dashboard contains:
  - 102 `custom:mushroom-template-card`
  - 91 `custom:button-card`
  - 57 `vertical-stack`
  - 47 `custom:popup-card`
  - 37 `conditional`
  - 35 `custom:mushroom-chips-card`
  - 15 `custom:apexcharts-card`

Current frontend resource sizes:

| Resource | Size |
| --- | ---: |
| `www/community/apexcharts-card/apexcharts-card.js` | 1,627,706 bytes |
| `www/community/lovelace-mushroom/mushroom.js` | 712,046 bytes |
| `www/community/custom-sonos-card/custom-sonos-card.js` | 559,517 bytes |
| `www/community/button-card/button-card.js` | 162,135 bytes |
| `custom_components/browser_mod/browser_mod.js` | 150,297 bytes |
| `www/house-notices-card.js` | 54,177 bytes |
| `www/radon-air-quality-card.js` | 23,411 bytes |

`node --check` passed for the repo-owned custom frontend cards and Browser Mod
script checked in this repo.

### Known frontend risk from cached live state

- Browser Mod is checked in at `2.7.3`; cached live HACS state showed `2.13.3`
  available.
- Browser Mod is directly in the dashboard load path: it injects
  `/browser_mod.js`, auto-adds a Lovelace resource, registers a panel, and powers
  many `custom:popup-card` interactions.
- `card-mod` was cached at `v4.1.0` with `v4.2.1` available.
- The radon card still loads 30 days of history on mount through
  `history/period/...` from both `set hass` and `connectedCallback()`.
- The Casey presence timeline also loads history on mount, though with a
  smaller default horizon.

### Backend startup risk

The custom Whisker Ting coordinator still performs first-refresh external work:

- API state fetch runs during coordinator refresh.
- On first successful fetch, it connects to the SignalR websocket.
- Websocket handshake waits up to 10 seconds.
- First voltage data waits up to 5 seconds.

This can add startup noise or delayed integration readiness, but the code path
does not yet explain a multi-minute app disconnect by itself.

## Ranked Findings

### 1. Highest-confidence incident finding: Nabu Casa can be reached, but Trevor's instance is not connected

Confidence: high.

The 2026-05-27 Safari reproduction reaches the remote Home Assistant/Nabu Casa
fallback page and reports that Home Assistant is not connected. That moves the
incident away from "mobile app cache" and "dashboard render" and toward one of:

- Home Assistant Core/host is down or restarting.
- The home internet path is down or blocking the cloud tunnel.
- HA Cloud inside the instance is disconnected, stuck, or unable to maintain
  its websocket/tunnel to Nabu Casa.
- Account/server-side Remote UI state for this instance needs to be nudged from
  the Nabu Casa account page.

Why it matters: the fastest useful fix is to restore the instance's connection
to Nabu Casa or bring HA back online, not to edit dashboard YAML.

Smallest safe next fix: from the Nabu Casa account page, use the offered action
to ask the instance to come online; if that does not recover within a minute or
two, get a home-side check of HA host power/network or restart Home Assistant
Core/host when safe.

### 2. Highest-confidence environment finding: the audit Mac's HA traffic is being reset through a tunnel

Confidence: high for the Mac, medium for the iPhone incident.

The audit Mac routes both the cached private HA LAN address and the Nabu Casa
Remote UI address through `utun6` / `100.64.0.1`. TCP connects, then HTTP/TLS
resets. This can produce exactly the kind of "disconnected" result seen by a HA
client, but the Mac's route is not the same as a phone on home Wi-Fi or pure
cellular.

Why it matters: any live test from this Mac can falsely look like Home
Assistant is broken when a tunnel/security layer is actually terminating the
connection.

Smallest safe next fix: retest from a clean path before changing HA config:

- iPhone on home Wi-Fi with any VPN/security profile disabled.
- iPhone on cellular with Wi-Fi disabled.
- Mac on home LAN with tunnel disabled or bypassed.
- Another device on the same home Wi-Fi, using Safari against the HA local URL
  and the Nabu Casa URL.

### 3. Still important: HA/backend unavailable during the failure window

Confidence: medium-high after the Safari reproduction.

The "wait minutes" recovery pattern fits HA restart, host overload, recorder
startup, supervisor/container instability, or network path recovery better than
a simple dashboard rendering bug. But current logs from 2026-05-26 around
10:05 AM were not available from this environment.

Why it matters: if HA is actually restarting or wedged, frontend tuning will not
fix the incident.

Smallest safe next fix: collect live logs and uptime around the next failure:

- `home-assistant.log` lines from 5 minutes before through 10 minutes after the
  failed open.
- Supervisor/Core uptime and restart timestamps.
- Any recorder/database startup warnings.
- Any `homeassistant_started`, websocket disconnect, auth, cloud, or mobile_app
  errors.

### 4. Companion-app URL/session selection is no longer the primary suspect

Confidence: low to medium.

The repo does not define internal or external URLs. If the iOS companion app has
a stale internal URL, stale external URL, bad SSID match, or cached WebView
session, it can land on the blank shell or disconnected screen even when HA is
otherwise healthy.

Why it matters: this can still make recovery flaky, but the 2026-05-27 Safari
test proves the remote browser path fails too.

Smallest safe next fix: inspect the iOS companion app settings directly:

- Confirm internal URL, external URL, and "use Home Assistant Cloud" behavior.
- Confirm whether the app is switching between LAN and Remote UI as expected.
- Confirm whether the phone has any VPN, private relay, DNS filter, or security
  profile active during failures.
- If HA is reachable in iPhone Safari while the app is disconnected, clear the
  companion-app frontend cache or re-add the server.

### 5. Frontend first-render fragility is real, but currently secondary

Confidence: medium.

The `calm-mobile` dashboard is large and Browser Mod is stale and deeply
involved in first load. The radon and Casey custom cards make history API calls
on mount. These facts can explain blank or fragile first render after HA is
reachable, especially on cold cache. They do not explain connection resets or a
multi-minute wait by themselves.

Why it matters: once reachability is stable, this dashboard can still make the
app feel unreliable.

Smallest safe next fix after reachability is proven:

- Update Browser Mod and card-mod through HACS.
- Hard-reload iOS app/frontend caches.
- Retest first render before editing dashboard YAML.
- Lazy-load radon history and move heavy popup detail surfaces off first render.

### 6. Whisker Ting can add startup delay, but is not yet the main suspect

Confidence: low to medium.

The integration waits on external API/websocket work during the first
coordinator refresh. This can contribute to noisy startup and delayed entity
readiness, but there is not yet evidence that it blocks HA's HTTP server or
creates the observed disconnected screen.

Why it matters: if logs show Ting delays during the failure window, this becomes
a clear low-risk optimization.

Smallest safe next fix if logs implicate it: decouple initial entity setup from
first websocket voltage data and let voltage arrive asynchronously after setup.

## Recommended Next Incident Drill

Run this during the next phone failure before making any HA changes:

1. On the iPhone, note the exact time, network mode, and whether VPN/security
   filtering is active.
2. From the same iPhone, open HA in Safari using the local URL if on home Wi-Fi,
   then the Nabu Casa URL.
3. From a second home-LAN device, open the same local URL.
4. In HA, collect logs for the exact window if the UI becomes available.
5. Record whether all clients fail, only the app fails, or only one network path
   fails.

Interpretation:

- All clients fail: investigate HA host/Core/Supervisor/network availability.
- Browser works but iOS app fails: investigate companion-app URL selection,
  cached session, WebView cache, or app version.
- Local works but remote fails: investigate Nabu Casa/cloud path.
- Remote works but local fails: investigate LAN DNS, SSID detection, VLAN/guest
  Wi-Fi, or local URL.
- Only heavy dashboard path fails: investigate frontend resource order,
  Browser Mod, popup payload, and eager history calls.

## Retest Matrix After Each Fix

- 5 iPhone app opens on home Wi-Fi after the app has been idle.
- 5 iPhone app opens on cellular with Wi-Fi off.
- 3 iPhone Safari opens to the local URL when on home Wi-Fi.
- 3 iPhone Safari opens to the Nabu Casa URL.
- 3 desktop browser opens from a clean, non-tunneled home-LAN path.
- One open immediately after HA restart, with logs captured until the dashboard
  is stable.

Record:

- time to first visible app shell
- time to first rendered dashboard content
- whether websocket connects
- whether `/api/config` responds
- whether `/api/websocket` authenticates
- console errors or failed frontend resources
- HA log errors in the same window

## What Was Not Proven

- Not proven that Home Assistant restarted at 10:05 AM on 2026-05-26.
- Not proven that Nabu Casa itself was down.
- Not proven that dashboard YAML or custom-card syntax caused the disconnect.
- Not proven that Browser Mod caused the iOS disconnected screen.
- Not proven that Whisker Ting blocked HA startup.

The next decisive evidence is same-window HA logs plus a clean-path phone or
home-LAN browser test.
