# Evening scene on first return home

## Symptom and evidence

Trevor reported that Evening lights were not on when arriving home November 12.
Live trace at 4:04:19 p.m. Eastern detected Trevor's arrival and passed all
schedule, presence, vacation, guest, TV-hold and genuine-first-arrival gates.
The final eligibility guard failed: Evening was selected and its script had
already run since noon. Casey's 4:04:52 arrival then failed the existing
first-person-only filter because Trevor was home. This was not missed presence.

The November 8 manual-off protection removed missing-light repair and kept a
same-day guard shared by dusk and arrival. That guard also blocked a genuine
first return home. Preserve the November 8 protection against five-minute and
reload relighting while allowing this distinct arrival case.

## Authorization and change

Trevor approved the proposed narrow correction with “Yes def fix” on November 12:
allow first-person arrival to reapply Evening, retaining background suppression
and TV/Bedtime safeguards. Added only an arrival branch to the final condition.
Existing genuine-arrival filtering, other-person-home exclusion, both schedules,
TV hold, vacation/guest overrides and dusk behavior remain unchanged. Explicit
Evening controls remain unchanged. No direct light/scene action or simulated
presence event was issued for testing.

## Verification and deployment

- Six focused unittest methods pass, including current-day arrival reapplication,
  refresh/reload/startup/dusk suppression, None/stale-day catch-up, TV/Bedtime
  exclusions, both people's genuine-arrival and tracker-recovery filters, and
  direct Evening button wiring.
- YAML parsing and semantic comparison prove exactly one condition changed in
  the live monolithic automation file. Updated repository condition matches.
- Prepared two-line diff reviewed; unrelated live definitions and local work
  preserved. Active monolithic live layout retained.
- Deployment `ac777a8ca73a474b85ae727495480a61` applied successfully. Real HA
  configuration validation passed and automation-only reload completed. No
  Core restart or script reload.
- Live readback matches prepared bytes, SHA256
  `fd087419366cd7e081d6745f4e5dde14a9dc24f4d989673f1c74fd044f641a82`.
- Reload trace at 4:19:27 p.m. Eastern contains the new arrival branch and stops
  at condition 9, with no action steps: reload did not replay Evening.

- Natural five-minute refresh at 4:20 p.m. Eastern also contains the new branch,
  stops at condition 9 and has no actions. Background suppression verified live.
- Ten administrative bridge unit tests also pass.

## Limits

Arrival logic is tested without physically replaying the scene or spoofing
presence. The next genuine first return home is the end-to-end physical test.
Existing full-restart helper reset behavior remains outside this scope. Historical
trace references are retained-runtime evidence, not permanent archives.
