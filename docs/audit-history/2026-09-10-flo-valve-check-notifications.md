# Flo valve check notifications — 2026-09-10

## Symptom and context
Trevor receives the same shutoff warning during routine Flo testing and unusual
closures; requests calm completion notices for normal checks and warnings for
unusual activity. Reviewed audit index, notification reliability guidance, and
existing water shutoff/native alert automations. Earlier inventory-only water
safety audit did not source-test these paths.

## Evidence and ranked findings
1. High confidence: existing immediate valve warning uses any pending Flo alert,
   including informational alerts. The upstream integration exposes separate
   info, warning, and critical counts; a pending alert is not necessarily a fault.
2. High confidence: the existing quiet-closure branch already waits six minutes,
   then records a presumed test without a phone notification.
3. High confidence: Home Assistant's integration exposes no confirmed test-pass
   result. Reopening alone cannot prove a successful test (it might be a manual
   operation or aborted test). Copy must describe an observed recovery and label
   routine-test attribution as inference.
4. Live Flo entities were unavailable. Exact cause of the photographed warning
   remains unverified; do not claim informational alerts were its proven cause.

## Local change — not yet deployed
- Only concerning Flo alerts (warning/critical counts, or unavailable/missing
  alert data) bypass the existing recovery window. Informational notices alone
  can enter the quiet-check path.
- Keep immediate warning for active leaks, flow above the existing threshold,
  and missing flow data. Preserve the six-minute window and failure warning.
- Require open valve, available quiet flow, cleared Flo alerts, and all nine
  watched leak sensors reporting dry before a passive “Water check complete”
  push. Wording says the recovery looks like a routine check, not that it passed.
- Preserve internal history and distinguish its label from a confirmed test.
- No valve commands, test initiation, schedules, or new entities added.

## Checks and limits
Ruby YAML parsing and diff whitespace checks passed. Structural checks confirm
the immediate critical branch and six-minute window remain. Jinja/runtime branch
validation and live deployment are pending: the Mac locked and computer-use
could not unlock it. No test was run against the physical water valve.
Recorder inventory generator ran without a copied DB; it also captures existing
inventory drift since its last refresh. Device coverage check reports pre-existing
false references `light.state` and `light.last_changed` from template iteration;
this change introduces no new entity IDs. System and bundled Python lacked
PyYAML/Jinja, so no local Jinja execution is claimed.

## Follow-up
After Mac unlock: finish config-check/reload verification for the first two fixes,
validate Flo templates with a scenario matrix (info-only, warnings, critical,
missing data, reopening, still closed, leak), deploy and read back the water file,
and verify config/reload. Confirm the next naturally occurring test; investigate
Flo availability before making any stronger test-result claims.

## Primary sources
- https://www.home-assistant.io/integrations/flo
- https://github.com/home-assistant/core/blob/dev/homeassistant/components/flo/binary_sensor.py
- https://solutions.moen.com/Moen_Flo_Shutoff/Alerts%2C_Notifications%2C_and_Settings/Get_to_Know_Your_Device%3A_MicroLeak_Test

## Completed deployment after unlock
On September 10, resumed through the connected Safari/Nabu File Editor route.
Home Assistant configuration check returned `valid`, with no errors or warnings.
Template, script, and automation reloads completed for the banner and garage
changes. Flo was then written and read back with SHA-256
`e5f39039a77b37c4510060dcee270dce4b4a946793b0a9e5b9440733b0521e95`;
a second config check passed and automation reload completed.
Live automation config includes the passive Flo notice and excludes the garage
phone push. Served Lovelace config contains explicit left alignment for both
banner title and body. Home view was opened for visual checking.

Flo severity template scenarios returned the expected results: info-only and
clear alerts do not bypass the observation window; warning, critical, missing
counts, and unavailable alerts do. Recovery requires all four gates; each
individual failed gate rejected the informational notice. An initial synthetic
fixture used undefined attributes and returned 400; it was corrected to the
actual state_attr missing-value contract (`None`) before the passing run.

Flo entities still report unavailable, so real-device test completion remains
unverified. No water valve operation or test notification was triggered.
