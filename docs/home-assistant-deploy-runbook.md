# Home Assistant Deploy Runbook

Date: 2026-06-04

## Purpose

Use this when deploying repo-owned Home Assistant YAML or local frontend files
to the live HA instance. The goal is a repeatable path with write/read-back,
config check, reload, and verification.

## Preferred Browser Deploy Path

Keep deployed files small enough for reliable browser-mediated write/read-back.
`automations.yaml` is intentionally a tiny include pointer; deploy it together
with the files under `automations/` when automation behavior changes.

1. Open Home Assistant in Safari through a connected route.
   - Local may work when `homeassistant.local` is healthy.
   - If local shows stale state or `hass.connected === false`, use the Nabu Casa
     Remote UI route instead.
2. Open the File Editor panel at `/core_configurator` on that same host.
3. Verify the File Editor add-on actually mounted:
   - `document.querySelector("home-assistant")?.hass?.connected` is `true`.
   - the page contains an iframe with `src` including `/api/hassio_ingress/`.
4. Generate the browser deploy payload from the repo:

```bash
node tools/prepare_ha_utf8_browser_deploy.js automations.yaml automations/20-climate-commute.yaml
```

5. Execute the generated `.tmp-ha-utf8-browser-deploy.js` in the File Editor
   browser tab.
6. Poll `window.__haUtf8DeployResult`.

Successful deploy evidence should include:

- each file written;
- each file read back with matching content/hash;
- Home Assistant config check result `valid`;
- no config-check warnings or errors.

## Reload Handling

The deploy helper calls `template.reload`, `script.reload`, and
`automation.reload` with bounded waits. Those calls may time out even after the
file write and config check succeeded.

When the helper reports reload timeouts:

1. Call the smallest relevant reload again from the connected frontend. For an
   automation-only behavior change, use `automation.reload`.
2. Wait longer than the helper's short timeout.
3. Verify the live config through HA's config API or by live behavior.

For the Casey closet stale-on fix, `automation.reload` completed successfully
after the helper timeout, and HA's automation config API returned the live
template trigger.

## Known Bad Paths

- Running the deploy helper from a normal dashboard page writes to the wrong
  relative `api/save` endpoint and returns `405 Method Not Allowed`.
- Saving one large YAML file through File Editor can fail near the tail and
  leave the live file partially written. Prefer Home Assistant include files
  with coherent chunks, and require byte-for-byte read-back before reload.
- A local dashboard can show cached/stale HA state while
  `hass.connected === false`; do not deploy from that state.
- From this Mac, terminal HTTP/curl to the HA LAN address may connect at TCP
  level but reset during HTTP. Prefer the connected browser/File Editor ingress
  path unless SSH or another direct host path is proven healthy.

## Post-Deploy Checklist

- Run local YAML checks before writing.
- Run `python3 tools/check_device_inventory_coverage.py` when entity references
  changed.
- Confirm File Editor read-back succeeded.
- Confirm HA config check is valid.
- Reload only the needed domains when possible.
- Verify live state/config, not only repo diff.
- Commit and push the repo change if that has not already happened.
