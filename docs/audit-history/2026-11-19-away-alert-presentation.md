# Keep unavailable-device diagnostics out of routine away alerts

**Deployed November 19 at approximately 10:34 AM EST.** Routine away alerts now
show only their existing confirmed entry/light information. The appended
“Couldn't check” device list is removed from all eight general-away variants,
Casey lights-only and Casey combined alerts. Buttons, recipients and gates are
unchanged. All 42 lighting targets and truthful explicit-action failure reporting
remain intact. No test notification or household control was executed.

## Decision and narrow scope

Trevor's direct November 19 instruction, relayed by Eames under
`HA-AWAY-ALERT-PRESENTATION-20261119`, was to keep unavailable diagnostics out of
these routine notifications while allowing separate troubleshooting. This
supersedes the routine diagnostic-disclosure presentation added November 18;
the inventory and action verification remain as documented in the
[coverage audit](2026-11-18-away-lighting-coverage.md).

Exactly ten `message` scalar values changed in `scripts.yaml`, removing only
the appended diagnostic suffix. Parsed comparisons of both repository and fresh
live candidates prove every other value unchanged: titles, confirmed-count
templates, buttons/tokens, metadata, tags, recipients, action steps and conditions.
The live-only Ting sender difference was preserved. Search found no additional
routine diagnostic suffix in active dashboard/frontend/automation sources.

Private unavailable attributes remain in `sensor.away_security_active_lights`,
and `away_lights_turn_off_verified` retains its target/result traces.
`away_lights_report_result` is identical: explicitly requested incomplete actions
still name the unresolved devices and never claim all lights are off. No new
routine diagnostic notification or logger was introduced.

## Verification and deployment

- Three presentation tests pass using
  `/Users/ames/.codex/ha-admin-venv/bin/python -m unittest discover -s tests -p test_away_alert_presentation.py -v`.
  They cover all ten messages with missing/empty/three unavailable diagnostics,
  the two-entry/three-light example, singular/pair/multiple Casey text, retained
  buttons and explicit incomplete/missing-inventory result wording.
- Independent review confirmed exact message-only semantics and rendered
  0/1/2/3-light variants. The independent root also passed seven lighting-coverage
  and seven Evening regression tests. YAML parses and diff whitespace check passes.
- Fresh live automation readback has no script-reload event listener or direct
  script-state trigger. Only `script.reload` was used: no automation/template
  reload or Core restart. A fresh connected read-only template at **10:33:38 EST**
  showed no running scripts; disconnected cached UI was not accepted as evidence.
- Deployment **`04c31a1b86e44b28885e6ada95aa0fe9`** prepared a complete, untruncated
  ten-message diff. The helper backed up/journaled the original, validated config,
  applied/verified the file, validated again and completed script-only reload.
- Before hash: `291367be94d243ac565d1462b6f2c237f284b2ec27db63a87e9282bf73945ac8`.
  Fresh readback matches reviewed after hash:
  `4c0773c649ec22e22cfabfd04c0ddfa60f1630b4671121f8f7766a4d2b9f8a13`.
- Post-reload connected template at **10:34:13 EST** shows no running scripts and
  unchanged execution timestamps: general sender November 19 **10:30:06 EST**,
  Casey combined **8:56:17 AM EST**, Casey lights November 16 **12:56:51 PM EST**,
  Evening November 18 **5:42:19 PM EST**. Both new verified-action/result scripts
  still have no last execution. No sender or lighting script was invoked to test.

Rollback is the supported `deploy_rollback` operation for this deployment ID,
script reload only, after checking drift. No rollback needed. Delivery of the
next natural push was not tested, and an already delivered notification on a
phone is not rewritten by a configuration reload.

## Separate bounded device finding

Fresh read-only state at **10:33:23 EST** still reports `switch.flower_lamp`,
`switch.master_lantern` and `switch.uplight` as **unavailable**, not unknown;
the shared inventory still contains **42** members. Saved inventory classifies
the first/third as TP-Link physical devices and the door lantern as a distinct
Lutron switch. Prior reconciliation explicitly distinguishes that lantern from
the bedroom lantern and Uplight 1 from the other uplight devices. These historical
device records do not prove present physical installation, power or connectivity.
There is no evidence here sufficient to retire or call them stale aliases. No
repair, rename, removal, network change or control was attempted.

The [onboarding checklist](../lighting-onboarding.md) now retains the November 19
presentation decision alongside the unchanged dual-path coverage requirement.
Unrelated AGENTS edits and scratch/earlier audit files were preserved.
