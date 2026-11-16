# Ting hazard contradiction — November 16, 2026

**Update:** raw evidence later proved ReviewedSuspicious, not ReviewedNotFire.
The scoped classification correction and owner-requested notification snooze
are described below. Preserve the initial hypothesis as history, not the finding.

Read-only investigation at approximately 5:05–5:10 AM EST. Owner screenshot
reported via the parent shows Ting connected with no fire hazards; this worker
did not independently inspect that screenshot or the vendor account.

Live admin MCP works. At 5:05 AM, confirmed-hazard automation trace
`ffb585c17ec66fbb927581b4651c22fc` explicitly records
binary_sensor.ting_confirmed_hazard_active on, repeat due, and invocation of
ting_send_notification. Its prior timestamp is 4:55 AM. Retained sender runs
also cover 4:22:04, 4:35, 4:45 and 4:55 AM.

Sender trace `6fad7adf303047fbf54293d79d0c497c` at 5:05:00 records confirmed
devices Ting 1, vendor-message summary "No Hazards Detected", and both voltages
122.8 V. It sends the contradictory text "Ting is flagging a confirmed electrical
hazard on Ting 1. No Hazards Detected" with critical sound/volume, then stamps
last-sent after the call returns. This proves the HA alert path and conflicting
inputs, not vendor hazard confirmation or handset delivery.

Fresh live configuration confirms the aggregate hazard template ORs primary
fire_hazard and electrical_fire_hazard binaries from either device, with no
status interpretation. Repository custom integration electrical_fire_hazard
is simply efh level > 0, whereas its status sensor explicitly recognizes
ReviewedNotFire before treating positive EFH level as hazard_detected. This is
a concrete semantic inconsistency and a plausible source of this alert, but
the raw live Ting 1 primary flag, EFH flag, EFH level and status have not been
retrieved. Do not label ReviewedNotFire as today's proven raw payload.

Native MCP query for Ting returned no exposed matches; admin MCP does not
provide arbitrary state/template reads. No diagnostic deployment, browser login,
credentials, integration reload, access change or hazard disabling performed.

Proposed narrow correction, conditional on raw-status verification: preserve
the independent primary is_fire indication and valid active hazard statuses;
exclude explicitly reviewed-not-fire EFH status from level-only promotion.
Apply consistent semantics to the aggregate, device list and attention surfaces.
Do not suppress all hazards based solely on a free-text message or normal voltage.
Implementation/deployment awaits confirmed cause and scoped authorization.

## Authorized inspection, sleep request and verified cause

Trevor approved inspection/fix with "YA", then explicitly requested "Sleep alerts
3 hours". Existing MCP was used; no credential retries or access changes.
Diagnostic-only variables were temporarily added to the confirmed-hazard
automation (deployment `1014fa988e7d4811b99a8db29169b001`), leaving its triggers,
conditions/actions unchanged. The 5:15 run preceded reload; it did not contain
the diagnostics. No test notification or manual trigger was used.

Natural **5:20:00 AM EST** trace `9339f8592154b11b1304975b4e892a07` captured:

| Signal | Ting 1 | Ting 2 |
| --- | --- | --- |
| Primary fire flag | off | off |
| Electrical-fire binary | on | off |
| EFH status | ReviewedSuspicious | none |
| EFH level | 20 | unknown |
| Unverified-fire binary | off | off |
| Integration hazard status | hazard_detected | no_hazards |
| Vendor message | No Hazards Detected | No Hazards Detected |

This verifies the precise HA classification error: a positive-level EFH binary
was promoted to confirmed despite the primary fire flag being off and its
reviewed status being suspicious. It does not prove that the underlying pattern
is benign or establish undocumented vendor meanings for level 20. The candidate
ReviewedNotFire-only correction was not deployed because it would miss this case.

## Time-bounded notification snooze

Requested interval: November 16 **5:18:08–8:18:08 AM EST**. Script reload made
the gate effective at **5:18:58 AM** (about 50 seconds into that interval).
Deployment `5034bd03e68449b7b5d5e9153b1f695e` passed HA validation and script
reload. It gates only confirmed, unverified and confirmed-clear Ting notification
kinds before notification or last-sent stamping. Detection, automations and
voltage/offline/freeze/learning notifications remain active.

The absolute timezone-aware expiry restores eligibility without a timer,
restart or follow-up job. Normal delivery is next evaluated by each existing
trigger/repeat schedule, rather than promising a push at the exact second.
The date-specific gate remains harmless after expiry and survives restarts.
Actual wall-clock expiry has not yet occurred during this verification.
Final script SHA256:
`398b973b0f92a9d1023518dd1a01e4a50b9195023a740306497106bdf5a0cc5a`.

## Narrow classification correction

Deployment `9c79d497bea44d77986b2d906e0f9ace` changed only four template values:
confirmed aggregate, unverified/watch aggregate, and their two device lists.
Primary fire=true from either device always retains confirmed-hazard behavior.
An EFH-only ReviewedSuspicious indication is retained as a non-critical watch;
ReviewedNotFire is not promoted from EFH level alone. All other positive EFH
indications, including unknown status, retain prior confirmed behavior. Existing
UFH signals and confirmed-over-watch precedence remain intact. This is a
conservative HA notification policy, not a claim that undocumented vendor
ReviewedSuspicious metadata proves safety.

No custom integration or raw entity was altered; its level-only electrical
binary and derived hazard_status may still say on/hazard_detected. The HA notice
aggregation and device lists now distinguish those raw indications consistently.
Normal voltage and free-text messages are not suppression conditions. Dashboard
YAML has no direct references to those raw EFH/status entities.

HA validation passed, template reload completed, exact config readback matched
`4498030b5466acc44b03fac425c50eb50362b4ed26fa597c05e175f57e89611e`.
The natural watch activation at **5:21:43 AM** was recorded in automation trace
`f0a27da40c00d298b0739397379118d7`; sender
`aa97c3d82d51aea78ba9f0ead4293e21` stopped at the snooze condition before sending.
Its summary attributes were briefly unavailable during template reload, so they
are not used as settled-state proof. No test push or Core restart occurred.

Tests: three unittest methods cover 112 primary/EFH/UFH/status/device combinations,
cross-device hazard precedence and 24 snooze-expiry/unrelated-alert cases.
Inventory coverage passed (180 active controls). Semantic comparison confirmed
exactly the four template values above changed; unrelated live differences were
preserved. Recorder inventory was regenerated; Markdown was unchanged, JSON date
refreshed, no database-frequency evidence available. Existing AGENTS.md edits
remain outside this task's commits.

### Settled-state verification and diagnostic removal

At **5:25:00 AM EST**, natural trace `93fde2946aa97616e855b5aae0c3fafc`
captured the same raw Ting 1 primary off / EFH on / ReviewedSuspicious / level 20
and both No Hazards Detected messages. Its confirmed-hazard condition explicitly
read **off**, so no critical sender action ran. This verifies the new loaded
classification, rather than relying on file contents or the snooze alone.

Temporary variables were removed with deployment
`5cb00ab04e8b44c6977f286974e57253`; HA validation passed and automation reload
completed. Readback has no diagnostic variables and hash
`3b3cc08f7899fb572d46d5749a313d6a7d11c910e5cafe06d01cbb1541e23a86`.
No temporary diagnostics remain in the committed automation configuration.
The candidate-only preparation scripts and raw live-file snapshots stay outside
Git. No vendor-side alert was dismissed and no detection entity was disabled.
Remaining limits: exact vendor semantics/age of ReviewedSuspicious are not
documented here; no claim that the electrical pattern is harmless. The snooze's
expiry boundary is tested but its future wall-clock execution is not yet observed.


## Message provenance and freshness review — later November 16

The labels "vendor-message summary" / "Vendor message" above identify the
HA integration's rendered text, **not proof that the current vendor payload
explicitly supplied that text**. The repository parser in
`custom_components/whisker_ting/api.py` defaults missing overall, EFH and UFH
`message` keys to `No Hazards Detected`; its dataclasses have the same defaults.
Therefore that HA message can be synthetic. The owner's separate Ting-app
screenshot is independent evidence of the app presentation at screenshot time,
not a captured API response or proof of electrical safety.

This provenance correction does not change the deployed predicate: neither
message text nor voltage suppresses any hazard. Primary-fire on always takes
precedence. Active EFH with unknown, unavailable, empty or unrecognized status
retains prior critical behavior; it is not interpreted as reviewed-clear.
ReviewedSuspicious stays visible as a watch rather than being discarded.
The four template changes are HA notification policy, not vendor confirmation
that the electrical pattern is harmless.

Forty additional message/status/primary combinations verify that clear-looking,
missing/unknown and warning message strings cannot change classification.
All four test methods pass. No additional runtime changes were made.

Raw payload key presence and the vendor's EFH `timestampUtc` are not exposed
by these sensor definitions. The current admin tool file allowlist excludes
custom-integration Python, so repository parser content is not a fresh hash
comparison with installed code. Authenticated raw-state/API inspection was
blocked by the saved HA login being rejected. No new credential attempts,
access expansion or unsupported internal-memory reads were made for this review.
The trace's 5:20/5:25 capture times prove when HA evaluated its state, not when
Ting refreshed the hazard metadata. Live voltage also does not prove hazard
metadata freshness: repository coordinator code obtains voltage from a separate
WebSocket path and updates hazard data through its API polling path. Current
vendor payload presence, hazard timestamp and last successful hazard-data fetch
remain unknown. Do not describe the incident as a verified vendor false alarm.

## Reported unusual-pattern notification — 8:35 AM EST follow-up

Read-only check at November 16 8:35 AM EST (13:35 UTC) found no snooze bypass.
Live script hash remains `398b973b0f92a9d1023518dd1a01e4a50b9195023a740306497106bdf5a0cc5a`,
with the same 8:18:08 AM expiry. Natural unverified sender runs at 7:30, 7:45,
8:00 and 8:15 stopped at the snooze gate. The 8:15 trace
`56f910996c6b3e116e6940650677ed65` explicitly shows kind unverified and gate false.

The next scheduled check, **8:30:00 AM EST**, passed the expired gate and sent
the non-critical watch, then stamped its last-sent timestamp. Sender trace
`57518429f4b318ec3ab1e0d05917bd76` records title **⚡ Ting sees something odd**
and body: "Ting flagged an unverified electrical pattern on Ting 1. No Hazards
Detected No confirmed hazard yet. I’m watching for escalation." It used tag
ting-unverified-hazard, sticky/high-priority data, without the confirmed alert's
critical sound override. The wording is confusing because it concatenates the
possibly parser-default message; it is not proof of vendor clearance or a new
confirmed hazard. Handset presentation timing was not independently retrieved.

Confirmed sender's 8:35 trace `0408f4be89bf0b07d97cc5b327dc363f` explicitly reads
confirmed-hazard off and stops before actions. Thus the critical-classification
fix remains effective, and the watch intentionally retained by the fix resumed
after the requested snooze. No timing/kind/gate defect was established. No
snooze extension, configuration edit, credential attempt or test push was made.
