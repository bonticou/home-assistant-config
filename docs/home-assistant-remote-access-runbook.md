# Home Assistant Remote Access Runbook

Date: 2026-05-27

## What This Watches

This runbook covers the intermittent state where the Home Assistant companion
app and Safari both show Nabu Casa/Home Assistant disconnect pages. That symptom
means the remote Nabu Casa page is reachable, but the cloud service cannot reach
this Home Assistant instance.

The repo now has two layers of protection:

- Home Assistant watchdog automation: watches `binary_sensor.remote_ui`, calls
  `cloud.remote_connect` at most once every 15 minutes when Remote UI is down,
  and records the last degraded/restored/recovery-attempt timestamps.
- External probe: `tools/ha_remote_health_probe.py` checks the Nabu Casa URL
  from outside HA, detects the Nabu Casa fallback page, and verifies whether the
  `/api/websocket` endpoint reaches Home Assistant by waiting for the
  `auth_required` greeting.
- UI diagnostic layer: `/ha-safe/home` is a stock-only dashboard used to compare
  against `/calm-mobile/home` when the HA logo appears and then the app goes
  blank. See `docs/home-assistant-ui-hardening-runbook.md`.

## Immediate Recovery

1. Open the Nabu Casa account page and use the Remote UI `Connect` action for
   this Home Assistant instance.
2. If it does not recover within 1-2 minutes, use local access or a home-side
   check to confirm the HA host is powered, online, and not restarting.
3. In Home Assistant, check Settings > Home Assistant Cloud:
   - account is logged in;
   - Remote Control / Remote UI is enabled;
   - `Allow external activation` is enabled;
   - status is connected rather than stuck on connecting.
4. If Cloud remains stuck on connecting, follow Nabu Casa's network guidance:
   check IPv6/firewall behavior and reboot the HA host if needed.

## External Probe

Run the probe from a Mac, server, or scheduler that is not part of Home
Assistant:

```bash
HA_REMOTE_URL="https://example.ui.nabu.casa" tools/ha_remote_health_probe.py
```

The output is one redacted JSON line. Useful statuses:

- `ok`: websocket reached Home Assistant and got `auth_required`.
- `remote_fallback`: Nabu Casa is reachable but cannot reach this HA instance.
- `dns_error`, `tcp_error`, `tls_error`: network path failed before HTTP.
- `http_error` or `websocket_error`: page or websocket failed without the
  known Nabu Casa fallback text.

Keep the real Remote UI URL in the environment or local scheduler config. Do
not commit it to the repo.

## Evidence To Capture During The Next Outage

- External probe JSON output at outage start and recovery.
- `sensor.home_assistant_remote_access_status` attributes.
- `input_datetime.home_assistant_remote_ui_last_recovery_attempt`.
- `input_datetime.home_assistant_remote_ui_last_degraded_at`.
- `input_datetime.home_assistant_remote_ui_last_restored_at`.
- HA Core/Supervisor logs from 5 minutes before through 10 minutes after the
  outage.
- WAN/gateway state, especially `binary_sensor.fios_router_wan_status`,
  `sensor.bonticou_gateway_state`, and gateway uptime.

## References

- Nabu Casa remote access setup:
  https://support.nabucasa.com/hc/en-us/articles/26474279202973-Enabling-remote-access-to-Home-Assistant
- Nabu Casa remote access flow:
  https://support.nabucasa.com/hc/en-us/articles/26469707849629-About-Home-Assistant-remote-access
- Nabu Casa cloud troubleshooting:
  https://support.nabucasa.com/hc/en-us/articles/25620486925085-Unable-to-reach-Home-Assistant-Cloud
