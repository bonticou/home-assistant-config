# Administrative MCP connection

## Request and prior context

The user requested browser-free automation trace inspection, log reads, and
configuration deployment alongside the newly working native Assist MCP server.
Reviewed the audit index, remote-access and deploy runbooks, and October 1
parking-reminder deployment report. That report documented live/repository file
layout differences; earlier deployment guidance documented File Editor tail
truncation and wrong-ingress endpoint failures.

## Evidence and ranked findings

1. Confirmed: official Terminal & SSH was installed and running, but its network
   port was disabled. The user entered and saved a dedicated public key, cleared
   the mistakenly populated password, and explicitly authorized enabling port
   22 and restarting only that app. Pinned its SSH host identity against the
   trusted web terminal before connecting. No router forwarding was configured.
2. Confirmed: SSH provides working HA CLI, Supervisor, and filesystem access.
   The stock app lacks Core API permission, so its Supervisor token alone cannot
   retrieve live traces. A dedicated helper app with supported Core API access
   avoids copying personal OAuth or long-lived tokens into the bridge.
3. Confirmed: live automation layout still differs from this repo: the live root
   automation file is approximately 339 KB. Deployment requires live hashes and
   review of the actual diff, not blind synchronization.
4. Confirmed: the repository was owned by the previous macOS user. The user
   corrected ownership through an administrator account. All final source edits
   are in the original repository; existing unrelated untracked files remain.

## Changes

- Added repository-owned `addons/codex_ha_admin`: a small Python app with Core
  and Supervisor API access, config/share mounts, and no TCP listener or ingress.
  It retains normal protection mode and exposes only a mode-0600 Unix socket.
- Added dependency-free `tools/ha_admin_mcp.py` as a local stdio MCP server.
  Tools cover health, automation discovery, trace list/detail, bounded logs,
  allowlisted file reads, config validation, deployment preparation/application,
  and rollback. No arbitrary shell, arbitrary API, device-control, or Core
  restart tool is exposed.
- Deployment plans contain original/new bytes and hashes in app-private data;
  writes have precondition checks, per-file atomic replacement, read-back,
  full configuration validation, and failure restoration. Interrupted operations
  are journaled and block new deployments pending recovery.
- Added focused failure/recovery tests and operating documentation; updated the
  deployment runbook with the direct path and retained browser fallback.
- Registered the separate `homeassistant_admin` server in local Codex settings,
  preserving native MCP and other entries and saving a private local backup.
  SSH key material, host pin, and connection settings remain outside Git.

## Checks and deployment

- Ten focused tests passed: path/symlink boundaries, YAML rejection, stale hashes,
  unsupported reloads, validation rollback, external-change preservation,
  interrupted-batch recovery, new-file rollback, plan expiry/duplicates,
  protocol initialization/tool discovery, and common credential redaction.
- Python compilation, add-on YAML parse, and Codex TOML parse passed.
- Installed and started helper version 0.1.0; source file SHA-256 read-back
  matched local config, Dockerfile, and server source.
- Real Core and Core API health passed; both report version 2026.9.2.
- Live Evening automation discovery, retained trace listing, and full trace
  detail succeeded. This was connectivity verification, not a fresh diagnosis
  of the earlier evening-lighting incident.
- Core, Supervisor, and SSH-app log reads succeeded with bounded output.
- Live automation-file read and SHA-256 retrieval succeeded.
- Tested the actual stdio MCP wire protocol: initialize, notification, tools/list
  (10 tools), and a live health tools/call.
- Prepared, applied, read back, and rolled back a single unused CSS comment file.
  Real HA configuration checks passed before writing, after writing, and after
  rollback. Verified the temporary file was absent afterward. No home behavior,
  automation, or dashboard was changed; no Core restart or domain reload occurred.

## Status, residual risks, and follow-up

Installed, connected, and verified. A fresh Codex chat may be needed to load the
new tool registration; the same bridge CLI works immediately without a browser.
Only Terminal & SSH was restarted during access setup.

The dedicated SSH key grants broader administrative access than the scoped MCP
surface. Keep it private. Privileged apps sharing `/share` can potentially reach
the Unix socket. Redaction is best-effort: treat logs, traces, and configuration
as private and do not commit raw output. No private endpoint, credential, raw
log, or device identifier is included here.

Multi-file replacement is not a filesystem transaction. The journal and recovery
checks mitigate interruption, but avoid simultaneous File Editor/UI changes.
Reload timeouts remain uncertain and require live verification; restart-only
changes require separate handling. The connection test deliberately did not
reload production domains, so their HTTP handling is implemented but not
exercise-tested against a production reload in this setup session.

Backups remain in the helper app's data and are not automatically pruned. Monitor
storage and preserve required journals before uninstall. The base image follows
the Python 3.13 Alpine tag; PyPI library versions are pinned. Continue normal
review and maintenance of this repository-owned helper.

No existing oversized configuration or live/repository drift was changed as
part of this connection setup. Visual dashboard QA still requires the browser.

## Primary interface references

- https://developers.home-assistant.io/docs/apps/communication/
- https://developers.home-assistant.io/docs/apps/configuration/
- https://developers.home-assistant.io/docs/api/supervisor/endpoints/
- https://github.com/home-assistant/core/blob/dev/homeassistant/components/trace/websocket_api.py
- https://learn.chatgpt.com/docs/extend/mcp?surface=cli
