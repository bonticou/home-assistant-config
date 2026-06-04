# Home Assistant UI Hardening Runbook

Date: 2026-06-03

## Purpose

This runbook separates remote access failures from dashboard/frontend failures.
Use it when Safari, the companion app, or the Nabu Casa URL shows a blank page,
a navy Home Assistant shell, or a failed secure connection.

## Diagnostic Paths

- `/`: base Home Assistant shell.
- `/ha-safe/home`: stock-only diagnostic dashboard.
- `/calm-mobile/home`: normal mobile dashboard.
- `/api/websocket`: Home Assistant reachability marker; `auth_required` means
  the request reached HA before a token is needed.

## Probe Command

Keep the real Remote UI URL in your shell environment or local scheduler, not in
the repo:

```bash
HA_REMOTE_URL="https://example.ui.nabu.casa" \
  tools/ha_remote_health_probe.py --compare-safe-dashboard --pretty
```

Useful statuses:

- `tls_error`: DNS/TCP worked but the secure connection failed. This is not a
  dashboard problem.
- `remote_fallback`: Nabu Casa is reachable but cannot reach this HA instance.
- `shell_error`: HA did not return usable shell HTML for a requested path.
- `resource_error`: shell HTML loaded, but startup JS/resources failed.
- `websocket_error`: shell loaded, but the websocket did not reach
  `auth_required`.
- `ok`: shell resources loaded and websocket reached HA.

## Interpretation Matrix

| Result | Meaning | Next action |
| --- | --- | --- |
| TLS fails | Network, certificate, tunnel, or remote access path | Test another network and inspect VPN/filtering |
| `/` fails | HA shell is not reachable | Treat as backend/remote access |
| `/ha-safe/home` fails | Not a `calm-mobile` UI issue | Keep working access layer |
| `/ha-safe/home` works but `/calm-mobile/home` blanks | Main dashboard/custom resources are implicated | Harden `calm-mobile` |
| Both dashboards work but app blanks | Companion app cache/session/WebView issue | Reset app frontend cache/session |

## Current First-Paint Hardening

- Radon chart history now defers until after first render and starts on `24h`
  instead of `30d`.
- Casey presence timeline history now defers until after first render.
- The safe dashboard uses only stock Lovelace cards, so it should load even if
  custom frontend cards or Browser Mod are fragile.
