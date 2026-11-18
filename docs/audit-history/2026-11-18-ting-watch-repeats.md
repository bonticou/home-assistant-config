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
