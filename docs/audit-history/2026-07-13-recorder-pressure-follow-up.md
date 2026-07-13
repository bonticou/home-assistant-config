# Recorder Pressure Follow-Up

## Symptom And Impact

Intermittent Home Assistant connection problems continue after Core, OS, and
add-on updates, though less frequently. The user asked whether the next useful
investigation is to identify state changes that do not need long Recorder
history or can be forgotten sooner.

Impact is availability and responsiveness: a large or noisy Recorder database
can make startup, recovery, dashboard history queries, and storage pressure
worse. Prior incidents also prove that Remote UI/Nabu Casa path failures can
occur independently, so this is a load-reduction and hardening track, not the
sole explanation for every disconnect.

## Prior Context Reviewed

- `docs/audit-history/README.md`
- `docs/audit-history/2026-06-04-home-assistant-availability-ui-and-casey-closet.md`
- `docs/audit-history/2026-06-06-backend-availability-audit.md`
- `docs/audit-history/2026-06-16-remote-ui-overnight-flapping.md`
- `docs/audit-history/2026-06-22-mobile-disconnected-nabu-session.md`
- `docs/recorder-inventory.md`
- `docs/home-assistant-remote-access-runbook.md`
- `docs/home-assistant-ui-hardening-runbook.md`

Important inherited findings:

- Earlier audits observed a very large Recorder database and 30-day retention.
- Earlier Core logs warned that large attributes for
  `sensor.irrigation_history_status` and `sensor.house_notice_history` exceeded
  Home Assistant's Recorder attribute limit.
- The June 16 mobile app incident matched actual Remote UI state flapping,
  including a long overnight outage, so Remote UI reliability remains a
  separate track.
- The June 22 incident showed that browser/mobile session handoff can fail even
  when the Nabu shell and websocket are reachable.

## Evidence Collected

Live check from an authenticated Home Assistant frontend on 2026-07-13:

- Recorder was running.
- Recorder backlog was `0`.
- Recorder migration was not active.
- Recorder database was in the default location.
- Long-term statistics exposed `206` statistic IDs.

Current YAML Recorder config:

- `purge_keep_days: 30`
- before this pass, no domains were excluded;
- before this pass, only signal-strength/RSSI/LQI/link-quality globs plus
  `sun.sun` and `weather.forecast_home` were excluded.

File Editor read-only shell checks:

- Live `home-assistant_v2.db` size: `20,462,624,768` bytes, about `19.1 GiB`.
- Live WAL size at the time of the check: about `21.8 MB`.
- Full DB-backed entity/attribute scan was attempted through File Editor with a
  read-only SQLite connection and `nice -n 19`, but it did not complete in a
  useful window and the browser request dropped.
- A lighter rows-only grouping scan was also attempted and still did not return
  quickly enough through File Editor.
- Both scratch scan processes were stopped by exact PID after they proved too
  expensive for this path.

Interpretation: the database is large enough that precise live row-count
collection through File Editor is itself a risky diagnostic. Future DB-backed
audits should either use a copied DB, a purpose-built short HA-side task, or a
more selective query plan rather than a broad live scan.

Current live state surface:

- Total frontend states: `1976`
- Recorder candidates under current config: `1974`
- Largest live domains by candidate count:
  - `sensor`: `485`
  - `switch`: `289`
  - `binary_sensor`: `285`
  - `automation`: `183`
  - `script`: `144`
  - `number`: `100`
  - `device_tracker`: `85`
  - `input_datetime`: `82`
- Almost every large domain had reported within the last 15 minutes, so the
  state surface is broad and chatty even when Recorder backlog is currently
  healthy.

Largest live attribute payloads observed:

| Entity | Live Attribute Size | Notes |
| --- | ---: | --- |
| `sensor.irrigation_history_status` | ~104 KB | Generated from `.irrigation_history.json` and `.irrigation_history_status.json`; should not also need 30-day raw Recorder history. |
| `sensor.house_notice_history` | ~30 KB | Trigger-template sensor appears to use its own attributes as rolling state; do not exclude until replaced with durable sidecar storage. |
| `sensor.device_inventory_pending_digest` | ~24 KB | Generated inventory digest; current-only candidate. |
| `sensor.house_notice_timeline` | ~16 KB | Derived dashboard timeline; current-only candidate. |
| `sensor.irrigation_flow_baseline_status` | ~8 KB | Generated from irrigation baseline sidecar files; current-only candidate. |
| `sensor.garbage_recycling_schedule` | ~8 KB | Derived schedule summary; current-only candidate after dashboard use is confirmed. |
| `sensor.irrigation_schedule_summary` | ~7 KB | Derived dashboard summary; current-only candidate. |
| `sensor.irrigation_7_day_ledger` | ~6 KB | Generated ledger summary; current-only candidate. |
| `sensor.wine_collection_snapshot` | ~5 KB | Generated from sheet/cache; current-only candidate. |

Static Recorder inventory:

- Recorder candidates: `1942`
- Low stateful-need candidates: `625`
- Largest low-value categories:
  - integration/config/update state: `377`
  - derived summary/dashboard state: `185`
  - infrastructure diagnostics: `35`
  - camera/event state: `25`
- Low-value domains include `number`, `select`, `button`, `update`, `camera`,
  and many UniFi Protect/Sonos configuration entities.

## Ranked Findings

1. **Recorder scope is broader than it needs to be. Confidence: high.**
   Recorder is healthy at the instant checked, but the system is recording
   nearly the entire live state graph for 30 days, including many generated
   summaries and configuration controls.

2. **Large generated sensors are concrete cleanup candidates. Confidence:
   high.** Several large entities are regenerated from scripts or sidecar files
   and are used as current dashboard state. Keeping 30 days of their raw state
   attributes adds weight without much operational value.

3. **`sensor.house_notice_history` needs special handling. Confidence: high.**
   It appears to preserve rolling notice history in its own template attributes.
   Excluding it from Recorder before moving that state to a sidecar file could
   lose restored notice history after restart.

4. **Config/update controls are likely safe Recorder exclusions, but should be
   cut conservatively. Confidence: medium-high.** Domains like `button` and
   `update` rarely need history. `number`, `select`, and `switch` need more
   careful pattern selection because some are real controls.

5. **Recorder pressure is not proven to be the full connection problem.
   Confidence: high.** Prior audits documented Remote UI flapping and browser
   session failures. Reducing Recorder load may improve stability and recovery,
   but it does not replace remote-access monitoring.

## Recommended Next Slice

Implemented first conservative slice on 2026-07-13:

- Excluded current-only domains:
  - `button`
  - `camera`
  - `update`
- Excluded explicit generated/current-only sensors:
  - `sensor.device_inventory_pending_digest`
  - `sensor.device_inventory_status`
  - `sensor.garbage_recycling_schedule`
  - `sensor.house_notice_timeline`
  - `sensor.irrigation_7_day_ledger`
  - `sensor.irrigation_flow_baseline_status`
  - `sensor.irrigation_history_status`
  - `sensor.irrigation_schedule_summary`
  - `sensor.metro_north_nwp_to_grand_central`
  - `sensor.wine_collection_snapshot`

This deliberately did not exclude motion, doors, locks, leaks, water, security,
presence, meaningful physical trend sensors, `sensor.house_notice_history`, or
broad `switch`/`number`/`select` domains.

Inventory effect after regenerating `docs/recorder-inventory.*`:

- Recorder candidates: `1942` -> `1871`
- Excluded by Recorder config: `20` -> `120`
- Low stateful-need candidates: `625` -> `554`
- Integration/config/update low-value candidates: `377` -> `327`
- Derived summary/dashboard low-value candidates: `185` -> `174`

Recommended next DB-backed step:

1. Obtain an off-device copy of `home-assistant_v2.db` from a current backup or
   safe HA shell path, or collect a small DB stats JSON with a bounded HA-side
   task that avoids broad live scans through File Editor.
2. Run one of:

   ```bash
   python3 tools/generate_recorder_inventory.py --db /path/to/home-assistant_v2.db
   ```

   ```bash
   python3 tools/generate_recorder_inventory.py --db-stats-json .tmp/recorder-db-row-stats.json
   ```

3. Use DB row counts to rank the biggest actual writers by rows/day and
   repeated attribute bytes.
4. Review `event`, `number`, `select`, UniFi Protect config switches, Sonos
   tuning controls, and additional generated dashboard sensors as a second
   conservative slice.
5. Do not exclude `sensor.house_notice_history` until it has sidecar storage.
6. Only then consider targeted purge/repack, with backup and free-space checks.

## Deployment Status

Configuration was changed in the repo but not yet deployed to the live HA
instance in this pass. A deploy/restart is required for Recorder config changes
to affect future recording scope.

Checks run:

- `python3 -m py_compile tools/generate_recorder_inventory.py`
- local Ruby YAML parse for `configuration.yaml`, `automations.yaml`, and
  `scripts.yaml`
- `python3 tools/generate_recorder_inventory.py`
- `python3 tools/generate_recorder_inventory.py --db-stats-json /tmp/does-not-exist --output-json /tmp/recorder-test.json --output-md /tmp/recorder-test.md`

## Residual Risks

- DB row counts are still missing; live state size and static inventory identify
  candidates but cannot prove the largest historical writers.
- Reducing Recorder scope may improve load and recovery but may not eliminate
  Remote UI or mobile session failures.
- Some generated sensors double as state stores. Those need a durable sidecar
  migration before Recorder exclusion.
- The current change only reduces future recording. It does not shrink the
  existing 19 GiB database until Recorder purge and possible repack/vacuum are
  handled separately with a backup and free-space check.
