# Main-floor sensor spread retired

Trevor explicitly requested no further monitoring or notifications comparing the
two main-floor sensors. The running system already had that feature unloaded.
This change removes the stale repository implementation so a later deployment
cannot restore it accidentally. No live configuration mutation was needed.

## Exact feature and evidence

The dedicated rule was **Environment — Main Floor Sensor Spread Watch**, YAML ID
`downstairs_climate_sensor_spread_watch`, registered as
`automation.climate_downstairs_sensor_spread_watch`. It compared Kitchen
`sensor.main_floor_temperature` with Dining Room
`sensor.main_floor_2_temperature` through `sensor.downstairs_temp_spread` and
`binary_sensor.downstairs_temp_spread_high`, above 3°F for 30 minutes. Its message
was “Kitchen and Dining Room are still …°F apart”; the shared
`script.environment_send_alert` delivered it as Main Floor/source_disagreement.

Read live configuration, automations, scripts and primary dashboard through the
established authenticated administrative MCP bridge CLI before editing. Live
files contained no dedicated spread sensor, binary sensor, sender or dashboard
spread reference. The exact complete configuration.yaml diff consisted only of
this retired feature; the repository file now matches the live bytes. Preserved
live monolithic automation layout and unrelated repo/live divergence.

The live Notification Center owner is `sensor.house_notice_timeline`; its
items_json contains no spread/apart comparison item. No active Notification Center
rule for this comparison was found, so none was invented or indiscriminately
disabled. Safari showed Needs Attention: 1 (Water guardrail), Upcoming: 18, and
quiet Recent. No stale comparison item needed clearing. Read-only template output reported
22 timeline items, comparison text absent, and no persistent spread/apart notices.

Developer Tools read-only template evaluation verified the three dedicated
entities unavailable (historical registry remnants), Kitchen 71.74°F / 35.87%,
Dining Room 68.12°F / 39.14%, average 69.9°F, climate status too_warm and
Dining Room thermostat in heat mode. These are observation-time values.

## Changes and preservation

Removed the repository-only sender and dedicated comparison entities, their
startup-refresh and alert-clear branches, the uneven climate status and spread
text in climate insight and dashboard. Shared scripts, helpers, both underlying
sensors, averages, HVAC logic, ordinary room alerts and separate Dining Room
SensorPush-versus-Ecobee checks remain. Recorded the do-not-recreate decision in
climate notes, annotated historical inventory entries and regenerated Recorder
inventory. No historical data or registry entries were deleted.

## Validation and recovery

Live admin health: Core/API 2026.9.2, config access available, no recovery required.
Live HA config_check returned result ok. Local Psych YAML parsing passed for all
three changed YAML files. Inventory coverage passed (178 control references).
Semantic automation comparison found only the dedicated sender removed; the two
shared changes are its startup refresh and clear-notification dependencies.
Diff whitespace check passed. Recorder generation passed; no database supplied,
so no database frequency/row-count claims are made. The system Python requires a
runtime datetime.UTC alias for this generator; source code was not changed.

No deployment ID, reload or restart: live configuration already implements the
requested retirement and loaded-state evidence confirms it. The focused Git
commit preserves recovery; do not restore the retired feature without a new
explicit request. Existing unrelated untracked files were preserved. No physical
routines, real notifications, credentials, network or security settings changed.

Residual limit: the time/source of the earlier live removal and the historical
notification Trevor saw are not established by current evidence. Separate Ecobee
disagreement rules remain intentionally outside this Kitchen–Dining Room scope.

## October 31 correction

Trevor's new screenshot established that the separate Dining Room SensorPush–
Ecobee alert was also unwanted. The earlier scope interpretation was incomplete.
Both disagreement branches are now retired in live HA; see
[corrective deployment](2026-10-31-dining-disagreement-retirement.md).
