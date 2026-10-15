# Codex HA Admin

A small local Home Assistant app that supplies administrative tools to the
Mac-side stdio MCP server in `tools/ha_admin_mcp.py`. It is separate from the
built-in Assist MCP integration, which continues handling device controls.

## Access

The app listens only on `/share/codex-ha-admin.sock` (mode 0600). It exposes no
TCP port, ingress page, or public endpoint. The Mac uses a dedicated SSH key,
pinned host identity, and `curl --unix-socket` through Terminal & SSH. The
Supervisor-managed token stays inside this app. SSH access itself is broader
than the limited MCP tools: protect the private key as an administrative key.
Other privileged apps with access to `/share` may also reach the socket.

The app needs `homeassistant_api` for live automation traces and reloads,
`hassio_api` with the manager role for logs and configuration checks, and write
access to Home Assistant config for deployment. It does not require Docker,
host networking, disabled protection mode, or an exposed listening port.

## Operations

- Health and live automation discovery.
- Retained automation/script trace list and trace detail via Core WebSocket.
- Bounded Core, Supervisor, and app logs.
- Allowlisted YAML/frontend file reads with exact source hashes.
- Home Assistant's actual configuration check.
- Prepare, apply, and rollback deployment plans.

There are no arbitrary shell commands, arbitrary API endpoints, device actions,
Core restarts, package management, or `.storage`/secrets file tools.

## Deployment protocol

1. Read the live file and its SHA-256. Compare it with the local repository;
   local layout is not necessarily the live layout.
2. Prepare 1–20 files with their expected live hashes. The helper parses YAML
   syntax and stores original/new bytes and file modes under its private
   `/data/deployments/<id>/manifest.json`. Review the returned diff.
3. Apply within one hour. The helper checks hashes and existing config validity,
   journals the operation, writes each file atomically, verifies read-back, and
   runs a full HA configuration check.
4. If validation fails, it restores the affected original files without reload.
   If concurrent edits prevent restoration, it reports `recovery_required`.
5. Reload only specified domains. A reload timeout is reported as **uncertain**;
   do not assume a timeout means the action did not occur. Core is never restarted.
6. Verify live behavior. A file-level deployment success does not establish that
   restart-only domains or YAML dashboards have loaded the new configuration.

Multiple requests are serialized. Multi-file deployments are not a filesystem
transaction; the durable journal detects interrupted writes and blocks further
deployments until recovery. Explicit rollback restores only files matching known
old/new hashes and refuses to overwrite later edits. Avoid concurrent HA UI/File
Editor edits while deploying. Backups remain in app data; no automatic deletion
is performed. Monitor its disk use over time.

Output redaction covers common token/password fields and JWTs but is best-effort.
Traces, logs, and configuration may still contain private household information;
do not commit their raw contents. Never deploy the redacted `file_read` response
verbatim. Use a known local source and inspect the diff.

## Install / update

Copy this directory to `/addons/codex_ha_admin` through SSH, reload the Supervisor
store, install `local_codex_ha_admin`, and start it. For subsequent source changes,
bump the version, copy files, reload the store, rebuild/update the local app, and
verify health. The Docker build uses official Python Alpine and pinned PyPI
versions for `websocket-client` and `PyYAML`.

See `docs/home-assistant-admin-mcp.md` for the Mac configuration and verification.
