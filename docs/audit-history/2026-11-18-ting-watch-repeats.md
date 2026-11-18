# Ting watch repeats — November 18, 2026

The repeated “Ting pattern watch” pushes came from the unchanged unconfirmed
watch's periodic reminder, not a newly confirmed hazard. The November 16
classification correction deliberately retained that old cadence.

## Evidence

The live 7:15 AM EST run used the time-pattern trigger, found watch enabled/on
and confirmed hazard off, and sent because its prior send stamp was 6:00:03 AM.
The 7:30 and 7:45 runs skipped the hourly throttle. This design can produce
roughly 60–75-minute repeats because successful-send timestamps occur seconds
after the quarter-hour scheduler. The screenshot is consistent with that send.
The latest inspected confirmed trace, 7:50 AM, again read confirmed hazard off.
This is HA evidence, not a fresh vendor diagnosis or proof the pattern is benign.

## Change and deployment

Changed only `ting_unverified_hazard_notification`:
- Removed periodic repeat trigger and elapsed-hour send eligibility.
- Notify for an actual off-to-on watch transition, or an additional watched
  device while a watch is already active. Device removals, unchanged sets,
  missing prior state, and initial empty-to-populated attributes do not send.
- Kept watch-enabled, watch-active and confirmed-hazard-off gates and the same
  notification sender. A new watch need not wait out the old hourly throttle.
- Kept confirmed-hazard detection, critical notification/repeat path, clearing,
  voltage, offline, freeze, sender timestamp recording and classification intact.

Reconciled against fresh live monolithic automations; preserved every other
live automation rather than replacing it with repository chunks. Semantic
comparison proved exactly one automation changed. No test push, synthetic hazard,
Core restart, credentials change, network/security setting change or vendor
account mutation was performed.

Deployment `8b5cd5256f3745f5b574fb10501a8e0d` passed HA configuration validation
and completed automation reload. Exact live readback matched candidate SHA256
`1296a21203d78b380aa75ab66ada6710923ec0b7b351ef500ac7e2ac4bdba3bb`.
Both watch and confirmed-hazard automations remained enabled.

## Verification and limits

Eight focused tests passed: prior hazard classification/message/snooze tests
plus event-only triggers, new/unchanged/removed/missing device cases, and safety
gates/sender preservation. No timed watch trigger remains in deployed YAML.
A future natural quarter-hour and handset behavior have not yet been observed;
no claim of a full end-to-end phone test. The watch can notify again for a real
new episode or added device; this is not a snooze or a safety-clearance claim.

Access note: ordinary sandbox DNS/SSH failed; the already-authorized admin
bridge worked with the normal host/key configuration under approved execution.
An old known-IP probe timed out. No host pin bypass or permanent access change.

## Natural follow-up at 8:18 AM EST

Read-only checks after the 8:00 and 8:15 quarter-hours found no new watch
execution: its latest retained run and last-triggered stamp remain 7:45 AM.
The Ting sender's latest retained execution remains 7:15 AM; no subsequent
sender run appears. The next old hourly eligibility would have been 8:30 AM
because the 7:15 successful send stamped seconds after the minute boundary;
this check verifies removed scheduler activity, not that later boundary yet.
Both watch and confirmed-hazard automations remain enabled. Critical evaluation
continues naturally every five minutes, including 8:15 AM, whose trace explicitly
reads confirmed-hazard off and stops at that condition. Live automation file hash
still matches the deployed candidate. No safety setting was changed, no test
notification was sent, and no synthetic hazard or trigger was used. Phone display
and vendor diagnosis were not independently checked.

## Utility semantics correction and scoped safety restoration

Subsequent investigation found the local third-party integration uses the name
`unverified_fire_hazard` for `ufhStatus.level > 0`. That expansion is wrong:
[Ting defines UFH as Utility Fire Hazard](https://help.tingfire.com/hc/en-us/articles/43729080235411-Power-Quality),
as does the [upstream integration README](https://github.com/aidenmitchell/ha-whisker-ting).
The shared watch branch therefore includes utility indications as well as our
locally inferred ReviewedSuspicious EFH watch. Removing all periodic watch
reminders was broader than necessary. No observed current utility event was
established; the proven November 16 raw case had both UFH binaries off.

Restored the **preexisting** 15-minute evaluation / 3600-second repeat eligibility
only when at least one actual UFH-derived binary is on. ReviewedSuspicious-only
EFH remains event-only. Kept the existing critical path, severity, classification,
sender, enable gate, and successful-send timestamp unchanged. This is not a new
claim that every positive UFH level is confirmed hazardous, nor a claim that
legacy UFH notification severity was already critical. Names/copy remain legacy;
a broader semantic correction needs verified vendor mappings.

Deployment `e9c54f000e214f2b8ff432b0b163ca0a` passed HA validation and automation
reload; exact readback matched SHA256
`cced3eab9cdbb871bb609968812331932de90f5eeab78cbd999b71f7c71d9c9a`.
Both relevant automations remain enabled. Nine focused tests pass, including
both devices' actual UFH on/off and old/recent/missing timestamps, showing that
EFH-only watch cannot pass the periodic repeat gate. No simulated event or push.

No authoritative public meaning or actionable threshold for ReviewedSuspicious
or level 20 was found. These values are not a percentage, severity score or
confirmed vendor instruction. The integration's “No Hazards Detected” can be a
parser default, not proof of actual vendor clearance. Latest available sender
snapshot at 7:15 AM showed Ting 1 watch, no confirmed devices, no useful message.
Latest inspected confirmed trace at 9:00 AM reads off. Attempted read-only live
raw-state request returned 401; no credential/access change or diagnostic
configuration was added. Trevor reports the Ting app looks normal. Treat that
as owner observation, not an independently verified all-clear.

Recommendation, not implemented: keep undocumented ReviewedSuspicious-only EFH
indications in diagnostic context rather than actionable push alerts until a
vendor-supported meaning/action is available. Do not blanket-disable the legacy
unverified branch because it also carries UFH. Ting's own actual hazard
notifications and Fire Safety Team guidance remain the practical action source.

## Owner-approved diagnostic-only ReviewedSuspicious EFH

Trevor agreed that undocumented Home Assistant interpretation should not generate
an alert without a documented actionable meaning. The push automation is now
triggered by the actual UFH-derived device entities, with an explicit UFH-active
gate on every path. ReviewedSuspicious-only EFH cannot push on activation,
additional-device changes, restart, or periodic evaluation. Its sensor/status
and dashboard diagnostic context remain intact; no data was discarded and no
safety-clearance claim was made. Utility activation can notify immediately even
if an EFH diagnostic was already active; existing periodic utility reminder
throttling and independent confirmed-critical behavior remain intact.

Only the selected watch automation changed. Legacy internal names and sender
copy remain unchanged in this narrow deployment; no integration entity migration,
new vendor threshold, or critical-path change was introduced. Nine focused tests
passed, including no-UFH gating and both utility devices, activation and repeat
throttle cases, plus the existing confirmed classification suite.

Deployment `9b08b57ad44a4405986c279a61d22134` passed HA validation and completed
automation reload without restart. Exact live readback SHA256:
`7e77bd0531e933541be6bd999833465a44ebf23c5cf30bc0e9c6348aa1d39684`.
Utility/watch and confirmed-critical automations both remain enabled. No test
push or synthetic hazard; next natural scheduled run is not yet inspected.
