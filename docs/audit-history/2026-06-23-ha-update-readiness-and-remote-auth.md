# HA Update Readiness And Remote Auth Bootstrap

Date: 2026-06-23

## Symptom And User Impact

Trevor reported another Home Assistant remote loading failure while preparing to
update Home Assistant. Safari showed the Home Assistant login shell with:

- `Unable to fetch auth providers`
- the remote Nabu Casa dashboard path with `auth_callback=1`

This blocks remote use before the `calm-mobile` dashboard can render.

## Relevant Prior Context

This matches the remote-access failure family already recorded in:

- `2026-06-16-remote-ui-overnight-flapping.md`
- `2026-06-22-mobile-disconnected-nabu-session.md`
- `2026-06-04-remote-ui-http-stall.md`

Those prior incidents separated several possible layers: Nabu Remote UI tunnel,
fresh HTTP/TLS/session bootstrap, HA Core availability, and custom dashboard
frontend payload.

## Evidence Collected

- A clean repo baseline was established before update prep:
  - local YAML parse passed for `configuration.yaml`, `scripts.yaml`,
    `scenes.yaml`, `lights.yaml`, `sensors.yaml`, automation includes, and
    dashboard YAML;
  - `python3 tools/check_device_inventory_coverage.py` passed;
  - `python3 -m unittest tests/test_ha_remote_health_probe.py` passed.
- The current repo baseline was committed and pushed:
  - `13003af Add Great Room uplights switch group`.
- A clean off-repo committed-state zip backup was created:
  - `/Users/trevor.kiviat/Desktop/house/backups/ha-config-pre-update-2026-06-23.zip`;
  - the archive was created with `git archive` from `HEAD`;
  - verified no `.git`, root scratch directories, or database files in the zip.
- The auth-provider failure is before dashboard boot:
  - failing to fetch auth providers happens during HA frontend authentication
    bootstrap;
  - this is not evidence that `calm-mobile` JavaScript or custom cards caused
    the blank/load failure.
- Remote unauthenticated checks were mixed:
  - `curl` reached `/`, `/auth/providers`, `/ha-safe/home`, and the
    `calm-mobile` shell path with HTTP 200 during one sample;
  - nearby system resolver checks intermittently returned no address for the
    redacted Nabu host;
  - repeated samples continued to show inconsistent behavior by client/tooling.
- The Mac/Zscaler path is material:
  - verbose `curl` showed a Zscaler-issued certificate for the redacted Nabu
    host;
  - Python/Node TLS checks rejected the same path because their trust stack did
    not accept the intercepted certificate chain;
  - this can explain Mac/Safari secure-connection/auth-provider failures, but
    does not by itself explain cellular iPhone failures when Zscaler is not in
    the path.
- The local `.inventory_token` used by older scratch helpers was expired, so it
  could not be relied on for authenticated live update/version checks.

## Ranked Findings

1. **Mac/Safari failures are at least partly network/TLS/auth-bootstrap path,
   not dashboard rendering. Confidence: high.**
   Evidence: the visible failure was `Unable to fetch auth providers`, which
   happens before the dashboard is loaded.

2. **Zscaler interception is a concrete Mac-side factor. Confidence: high.**
   Evidence: `curl` saw a certificate issued by Zscaler for the Nabu Casa host,
   while Python/Node rejected that TLS chain.

3. **Remote access still has a broader intermittent layer not fully explained
   by Zscaler. Confidence: medium-high.**
   Evidence: prior iPhone/mobile incidents happened away from the Mac path and
   matched Remote UI/session instability over time.

4. **The repo/config backup layer is ready for update prep, but live HA update
   execution is not ready until a real authenticated HA session is available.
   Confidence: high.**
   Evidence: GitHub and zip backups are complete; authenticated HA API checks
   were blocked by an expired local token.

## Changes Made

- Committed and pushed the current repo baseline:
  - `13003af Add Great Room uplights switch group`.
- Created an off-device repo zip backup from committed `HEAD`.
- Created scratch-only update-readiness probes under `.tmp/` for local use; they
  are untracked and should not be committed.

## Checks Run

- `ruby -e ... YAML.load_file(...)` for active YAML files: passed.
- `python3 tools/check_device_inventory_coverage.py`: passed.
- `python3 -m unittest tests/test_ha_remote_health_probe.py`: passed.
- `git diff --check`: passed before commit.
- `git push origin main`: succeeded.
- Unauthenticated `curl` checks to the redacted Nabu host: intermittently
  reached HTTP 200.
- Python/Node TLS probes: failed on the Zscaler-intercepted certificate chain.

## Deployment Status

No Home Assistant update was started during this entry.

## Residual Risks And Next Follow-Ups

- Before updating Core, open a fresh authenticated Home Assistant session and
  capture:
  - current Core, Supervisor, OS, and add-on versions;
  - current pending update list;
  - HA config-check result;
  - Backup manager state and latest successful HA backup.
- Create or confirm a real Home Assistant backup with the update flow, stored
  outside the HA device when possible.
- Review release notes and backward-incompatible changes for every monthly
  release between the installed Core version and the target version.
- Treat Zscaler as a Mac/Safari reliability factor, but continue monitoring
  Remote UI separately for iPhone/cellular failures.
