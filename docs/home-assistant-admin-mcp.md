# Home Assistant administrative MCP

## Architecture

Codex stdio MCP → `tools/ha_admin_mcp.py` → pinned, key-authenticated SSH →
Terminal & SSH → local Unix socket → Codex HA Admin app → Core/Supervisor APIs
and allowlisted config files.

The original `homeassistant` MCP connection remains available for exposed device
states and actions. The separate `homeassistant_admin` connection handles traces,
logs, config checks, and reviewed file deployments. Browser access is still useful
for visual dashboard review and administrative features outside these tools.

The helper app source and operating details are in
[`addons/codex_ha_admin/README.md`](../addons/codex_ha_admin/README.md).

## Mac setup

Keep the SSH private key and host pin outside Git. The dedicated SSH configuration
uses host alias `ha-codex-admin`, `IdentitiesOnly yes`, `BatchMode yes`,
`StrictHostKeyChecking yes`, a dedicated `UserKnownHostsFile`, no agent forwarding,
and no port forwarding. Verify the host fingerprint through an already-trusted
HA session before saving the pin. Do not accept changed host keys automatically.

The stdio server uses Python 3.9+ standard library only. Configure Codex with:

```toml
[mcp_servers.homeassistant_admin]
command = "/usr/bin/python3"
args = ["/absolute/path/to/ha-config-repo/tools/ha_admin_mcp.py"]
startup_timeout_sec = 20
tool_timeout_sec = 660
```

Default SSH configuration: `~/.ssh/ha_codex_config`. Override with
`HA_ADMIN_SSH_CONFIG` if needed. Local deployment sources default to this repo;
set `HA_ADMIN_REPO` only when deliberately using another checkout. Local file
sources must resolve inside that repository.

New MCP registration may require a fresh Codex chat. The same bridge is usable
immediately from a terminal without browser access:

```bash
python3 tools/ha_admin_mcp.py --call health
python3 tools/ha_admin_mcp.py --call config_check
python3 tools/ha_admin_mcp.py --call traces_list --args-file /private/path/request.json
```

Do not commit argument files, logs, trace payloads, or deployment previews. For
`deploy_prepare`, supply `files` entries with `path`, repository-relative
`local_path`, and `expected_sha256` from the live file read. Use null only when
the destination does not exist. Prepare only the task's reviewed changes; do not
blindly replace live files with repository versions.

## Verification

Run focused failure/recovery tests with Python and PyYAML installed:

```bash
python3 -m unittest discover -s tests -p test_ha_admin_mcp.py -v
```

Live acceptance: health; automation discovery; retained trace list and detail;
Core/Supervisor/app logs; live file hash; config check; and a reversible, unused
frontend test file deployed then rolled back. Do not trigger a real automation
or restart Core merely to test connectivity.

## Recovery and removal

If `health` returns `recovery_required`, inspect the relevant plan and current
files before invoking `deploy_rollback`. The journal is stored in the helper
app's private data. If the socket is missing, check the helper app's state/logs
via the established SSH/HA CLI path. If SSH is unavailable, use the existing
browser runbook. No automatic Core restart is part of this bridge.

To retire the connection, remove its Codex MCP entry, stop the helper app, and
revoke its dedicated SSH authorized key. Preserve necessary deployment backups
before uninstalling the helper. Disable the SSH network port if no other client
needs it. Neither the bridge nor setup requires router port forwarding.
