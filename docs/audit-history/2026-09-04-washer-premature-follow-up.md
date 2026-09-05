# Washer Premature Follow-Up And New-Cycle Cleanup

Date: 2026-09-04

## Symptom And User Impact

Trevor reported that the washing-machine notification said finished laundry was
still sitting even though he had already moved it along. The false reminder
made the laundry state untrustworthy.

## Relevant Prior Context

- The durable washer notification system was added in July 2026.
- The 2026-08-22 dryer incident established that parsing the displayed state of
  an `input_datetime` can shift timestamp comparisons; the dryer rules were
  changed to use each helper's native `timestamp` attribute.
- A dryer start already acts as positive evidence that a recent washer load was
  moved, but a new washer cycle did not clear an unresolved prior washer load.

## Evidence Collected

Live Home Assistant state showed:

- washer completion at 9:02:29 PM;
- initial completion push at 9:02:39 PM;
- false follow-up at 9:27:00 PM, only about 25 minutes later despite the
  configured 45-minute interval;
- the handled action at 9:27:24 PM;
- the washer already in `running`, proving the previous load was no longer in
  the machine.

The washer automation and scripts still used
`as_timestamp(states('input_datetime...'))`, while the previously repaired
dryer path used `state_attr(..., 'timestamp')`.

## Ranked Findings

1. **High confidence:** local datetime-string parsing made the 45-minute washer
   follow-up gate evaluate too early. This matches the prior dryer failure
   class.
2. **High confidence:** starting another washer cycle is durable positive
   evidence that the prior completed load was handled, but no automation used
   that evidence.
3. **Low confidence:** a future ThinQ status sequence outside the currently
   observed transitions may need a small adjustment after a real trace.

## Changes Made

- Converted washer completion, handled, snooze, follow-up, duplicate, pending,
  and error comparisons to native `input_datetime` timestamp attributes.
- Reworked the washer follow-up guard to match the dryer pattern: one normal
  follow-up after 45 minutes and another only after an explicit snooze.
- Added a guarded new-cycle cleanup that marks the prior washer completion
  handled when status reaches `running` from a normal start-of-cycle state.
- Updated washer notification copy calculations to use the same native
  timestamp source.

## Checks And Deployment

- Parsed the changed automation chunk, `scripts.yaml`, and
  `configuration.yaml` successfully with Ruby YAML.
- Confirmed all 65 automation IDs in the changed chunk are unique and ran
  `git diff --check` successfully.
- Ran `tools/check_device_inventory_coverage.py`; it reported only the two
  pre-existing Jinja-loop false positives (`light.last_changed` and
  `light.state`) and no new missing references.
- Wrote both changed YAML files through the mounted File Editor ingress,
  verified the full editor tails against the local files, and saved them.
- Ran Home Assistant's configuration check, then reloaded automations and
  scripts without restarting Home Assistant.
- Verified the new `washer_cycle_started_laundry_cleanup` automation is present,
  enabled, and displaying its expected trigger, guards, and action in the live
  automation editor.

## Residual Risks And Follow-Up

- There is no washer-door entity, so hanging or moving a load without starting
  the dryer or another washer cycle still requires the notification's `Done`
  action.
- Observe the next normal load: no unattended follow-up should arrive before 45
  minutes, and starting a new washer load should clear any unresolved prior
  reminder.
