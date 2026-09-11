# Irrigation notification precision and false connection warning

## Symptom and prior context

Trevor received a completion notice claiming 46 minutes, 3861.0 gallons and a
195.1 gal/min peak, followed two minutes later by “Hydrawise offline during
watering.” Earlier fixes were expected to have addressed unreliable alerts.

Reviewed the audit index and the July 4, August 6, and September 1 irrigation
incident entries, notification reliability patterns, and deployment runbook.
The prior rollback explicitly retained routine start/finish and connectivity
pushes. It also left a follow-up to audit session attribution and meter totals.
This was an incomplete coverage of the notification problem, not evidence that
the earlier changes had disappeared.

## Evidence and findings

1. **High confidence — the warning described the wrong period.** On September 11,
   watering activity went off at 11:18:54 Eastern; completion was recorded at
   11:23:54. Connectivity went off at 11:24:03, triggering the two-minute warning
   while only the post-watering grace helper remained active. Connectivity
   recovered at 11:29:11. Two earlier interruptions also lasted about five minutes.
2. **High confidence — the reported volume was not a verified session total.**
   The source reports `gal`, but updated only hourly: 17,786 at the start of the
   inspected window, 22,824 at 09:55, and 26,685 at 10:55. The reported 3861 was
   exactly the last hourly difference. A reconnect reset the session at 10:38:09,
   so that difference covered time before the purported session. Removing
   decimal places would not fix attribution.
3. **High confidence — peak flow was not measured peak flow.** It is calculated
   from delayed cumulative changes divided by an HA helper interval. Session
   resets and the 30-minute sample reset can shorten that denominator. The
   source does not provide the continuous measurements needed for a peak claim.
4. **High confidence — duration included the five-minute completion debounce.**
   The session also restarted when connectivity returned after its six-hour
   stale threshold, despite the watering grace window still being live.
5. **High confidence — connection loss is not proof the physical controller is
   offline.** The native integration combines cloud update success with the
   controller's online flag. An unsuccessful cloud refresh makes its connectivity
   sensor off too. See the [HA 2026.9.1 integration source](https://raw.githubusercontent.com/home-assistant/core/2026.9.1/homeassistant/components/hydrawise/binary_sensor.py).
6. Routine start/finish pushes were explicitly assigned Time Sensitive delivery,
   even though they were informational.

## Changes

- Completion push now says “Hydrawise reports watering has finished.” Removed
  unsupported session gallons, derived peak, elapsed runtime, and shared-well
  pressure claims from that push. Diagnostic history retains measurements with
  explicit attribution/estimate caveats; historical records were not rewritten.
- Require five continuous minutes of both connectivity and inactive watering
  before completion; recheck both before actions. A cloud failure cannot itself
  satisfy the finish trigger. Existing start/end timestamp guard prevents a
  second completion for the same session.
- Remove the six-hour-only session restart path. A reconnect inside the live
  grace period keeps the existing session instead of starting a false new one.
- During-session connectivity warning now requires 15 continuous minutes off,
  an unfinished session less than a day old, and a new durable session key.
  Completed-session grace windows do not qualify.
- Before-schedule warning also requires 15 minutes off, including its periodic
  recovery path. It only runs without an unfinished session, preventing the two
  warning paths from alternating and overwriting each other's duplicate keys.
- Both warnings describe missing HA connection confirmation and direct the user
  to check Hydrawise; neither claims a confirmed sprinkler fault.
- Add and load a durable input-text connectivity cycle key, stamped after send.
  Periodic checks allow the warning to recover after automation reload.
- Routine start and finish pushes are passive, without high-priority or sound
  presentation overrides. Warning delivery remains Time Sensitive.
- Reconcile the helper in the device inventory and regenerate Recorder inventory
  without a copied database. No device or integration was renamed.

## Checks and deployment

- All 11 existing irrigation history, ledger, and fingerprint tests passed.
- Ruby parsed each changed YAML file; `git diff --check` passed.
- HA's template engine passed eight cases against the served during-session
  condition: unfinished, screenshot's finished/grace period, already sent,
  restored same cycle, prior cycle key, stale session, future start, and missing
  session. The real current session correctly evaluated false.
- Served finish trigger includes connectivity plus inactivity for five minutes;
  served push text matches the shortened copy. Four HA-rendered finish cases
  passed: online/inactive true; offline/inactive, unavailable/inactive, and
  online/active false. Served script payload is passive with no high-priority
  or sound override. Served before-schedule guard has 15-minute persistence,
  mutually exclusive session scope, and durable cycle-key suppression.
- Full file SHA-256 read-back verified automation, script, and main config files.
  A missing YAML quote was caught and repaired before any reload. A transient
  frontend connection loss delayed read-back; it did not bypass validation.
- Final HA config check returned valid with no warnings or errors. Reloads of
  input_text, script, and automation completed. The new helper exists live.
- Device coverage still reports the pre-existing template-loop false positives
  `light.state` and `light.last_changed`; this change adds no missing physical
  device reference.

## Residual risks

The cloud-based zone model remains susceptible to stale activity and gaps. This
change makes notifications honest about available evidence; it does not certify
watering runtime, calibrate the Hunter meter, or repair historical ledger totals.
Do not reintroduce per-session volume or peak flow in push messages without
fresh samples aligned to reliable session boundaries. Physical controller loss
and cloud polling failure remain indistinguishable through this connectivity
entity alone. No sprinkler or water-valve commands were issued during testing.
