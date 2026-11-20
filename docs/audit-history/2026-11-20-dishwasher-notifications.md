# Dishwasher completion notification

**One quiet completion notification is configured for the connected Bosch
SHV9PCM3N. Natural-cycle emission, reset behavior and phone delivery remain
unverified.** This implements Trevor's delegated November 20 request
`HA-DISHWASHER-NOTIFICATIONS-20261120`, following the
[verified connection](2026-11-19-dishwasher-connection-check.md).

The intended push is:

> **🍽️ Dishwasher finished**
>
> The dishwasher has finished its cycle.

It uses the existing `script.notify_trevor_phone` route, passive interruption level
and `sound: none`. No door, offline, start, generic stopped or fault alert was added.
No appliance control, settings change, cycle start or synthetic push was performed.
The separate Flo leak protection, Ring, dehumidifier and dashboard remain unchanged.

## Signal evidence and limits

The exact device UI identifies **Bosch SHV9PCM3N**. Its previously disabled
`sensor.dishwasher_program_finished` was the **only entity enabled** for this task.
Normal UI enablement loaded it as **off**. Read-only templates confirmed its model
association, enum device class and options **confirmed / off / present**. It is an
enum sensor carrying the Home Connect ProgramFinished event, not an event-domain
timestamp entity. The same model has `sensor.dishwasher_operation_state` and
`binary_sensor.dishwasher_connectivity`; all three are the automation inputs.

The [vendor event definitions](https://api-docs.home-connect.com/events/)
distinguish successful completion from successful cancellation. The separately
inspected `sensor.dishwasher_program_blocked_salt_lack` remains disabled: its
vendor meaning is that a program cannot start, not proof of an interrupted wash.
ProgramAborted denotes cancellation. No positively verified model-specific fault
established an interrupted cycle, so no needs-attention alert was invented.
Registry rows are offered by appliance type; they do not prove actual emission
by this physical unit.

[Home Connect sensor implementation](https://github.com/home-assistant/core/blob/2026.9.2/homeassistant/components/home_connect/sensor.py)
and [entity implementation](https://github.com/home-assistant/core/blob/2026.9.2/homeassistant/components/home_connect/entity.py)
show enum values without provider event timestamps, force-update or an automatic
per-cycle reset. Therefore a repeated unchanged `present` cannot be treated as a
new completion, and a fresh HA receipt time is not provider freshness. Exact
Off/Confirmed timing and ordering remain natural-cycle checks.

## Implemented decision path

One queued automation, `automation.dishwasher_successful_cycle_notification`,
serializes decisions using the YAML-owned, max-255-character restored
`input_text.dishwasher_notification_cycle`. Its compact record holds the observed
cycle timestamp, reset baseline, attempted-cycle claim and successful-call stamp.
It has no initial value and does not depend on Recorder history.

- A genuinely observed ready/inactive/finished/delayed-start → run creates a
  provisional cycle. Pause or action-required → run preserves that cycle.
- The completion signal must be off/confirmed at run start, or reset to one of
  those values during the same observed active run. Reset alone cannot create a
  cycle. Both run-before-reset and reset-before-run are covered.
- Only an off/confirmed → present ProgramFinished edge can notify. Generic
  operation `finished` never triggers a push. Connectivity and current operation
  must remain usable; an old cycle or delayed queued event is rejected.
- Startup, automation reload, disconnected/unavailable telemetry and abort/error
  invalidate the active cycle. Loaded-automation time also rejects restored old
  cycles. Already-attempted and successful stamps are retained.
- Before dispatch, the automation writes an attempted-cycle claim and reads it
  back with the current signals. A silent failed helper write cannot dispatch.
  The successful-call stamp is written only after the phone wrapper returns.
  A failed/uncertain call or failed success-stamp write does not replay that cycle;
  a new genuine cycle remains eligible.

This favors silence over a false or repeated notice. A cycle spanning a restart,
reload/disconnect, lacking a signal reset, taking 24 hours, arriving after the
operation has already returned to ready, or missing its observed start may be
skipped. The 60-second queue-age check is local processing protection, not proof
of vendor-event freshness. The claim is durable HA helper state, not an atomic
transaction with a phone: an abrupt host/storage failure can still lose its most
recent persisted update. Exact-once handset delivery is not claimed.

The shared wrapper records local `sent` history before invoking the mobile
provider. Neither that history nor this automation's successful-call stamp proves
handset receipt. No wrapper changes were made.

## Validation and deployment

Fourteen focused tests execute the actual production YAML with simulated service
calls. They cover normal completion, both reset orders, next cycle, duplicate
edges, cancellation, pause/resume, startup/reload/disconnect, missing/corrupt/
unavailable ledger, stale cycles, delayed queue, failed/ignored claims, provider
failure/uncertain acceptance, success-stamp failure and subsequent eligibility.
An independent reviewer also checked adversarial cases and preservation of all
65 pre-existing maintenance rules. No real notification or appliance was used.

The live configuration is monolithic even though the repository is split. The
payload preserved the exact byte prefix and all **186 existing live automations**,
all **37 existing YAML input-text definitions**, and the existing global config.
Only one automation, one root include line and the dedicated helper file were
added. The existing helpers had no initial values. UI-managed helpers were not
changed. No administrative allowlist expansion or Core restart was used.

Initial admin deployment **e27c2a674aea4f54b30aed011752a193** passed configuration
validation, backup/write/readback and automation reload. The supported **Tools →
YAML → Input texts** control activated the helper. Before and after that reload,
the same 39 pre-existing input-text values had an identical SHA-256 fingerprint
(new helper excluded), confirming preservation without publishing their contents.
The new helper read back as YAML-owned, max 255 and initially unknown.

The initial reload trace performed invalidation only and did not enter the push
branch. It revealed that HA's absent state object is None rather than undefined,
so the guard was tightened and persisted-claim readback added before dispatch.
The correction was independently reviewed and prepared as an automation-only diff.
Corrective deployment **ac10afe0b01d47429ec45fd2bd6a62ae** passed validation,
write/readback and automation-only reload at **07:18:15 Eastern**. At 07:18:22,
the exact automation was on; the YAML-owned helper read
`{"cycle":0,"sent":0.0,"claimed":0.0,"baseline":false}`; completion was off,
connectivity on, operation ready and model SHV9PCM3N. The new retained trace
finished through invalidation with only `input_text.set_value`, no sender action.
Both deployments were independently reviewed; health reports no pending recovery.

Final live file hashes:

- `configuration.yaml`: `45ba21ece381a6eb90842a10ffb6994f436c6c0340b41f3a7aeeb6c591b8003c`
- `automations.yaml`: `f92ab3fee14f161631883db9b06340907487a9c318c96712233e846ef205a134`
- `helpers/dishwasher_notification_cycle.yaml`: `bb8cf09ec39ffef0b69bc70f2a5d9ca9ad589686ad64a3c55b5e09fae740f157`

The final missing-helper test models HA's None object; the test harness also
normalizes whitespace around boolean template results like HA. Fourteen final
tests passed locally and independently; a second reviewer passed seven additional
pre-dispatch disappearance/state-change checks. These simulated checks establish
logic behavior, not the appliance's natural event sequence or push delivery.

Device inventory now records 17 enabled entities on this exact device, including
four option entities discovered naturally after connection and the one newly
enabled completion sensor. Ten disabled IDs remain outside the targeted inventory.
The whole-house base totals remain dated. Inventory coverage passed for 181 active
control references. Recorder inventory was regenerated without database statistics;
Recorder policy was not changed.

## Remaining natural check and recovery

Observe the next ordinary cycle without starting one for testing: verify observed
run, ProgramFinished reset and present transition, a single attempted/success stamp,
and actual phone receipt. Absence of a push is not proof that the wash failed.
Inspect retained traces and current signal lifecycle before changing policy.

Administrative backups support guarded rollback in reverse deployment order.
Rolling back YAML requires reloading automation and Input texts through their
supported paths. Disabling the one completion sensor, if reverting the whole
feature, is a separate UI registry action; file rollback does not undo it.
