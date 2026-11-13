# Overnight lights stayed on — November 13, 2026

**Current outcome:** focused retry/diagnostic hardening was subsequently authorized
and deployed. The original overnight cause remains unproven. See the implementation
and runtime evidence below; the first investigation itself was read-only.

Read-only investigation requested for the November 12–13 night. No HA files,
helpers, security/network settings or physical devices changed. Existing admin
MCP works in this project chat: Core/API 2026.9.2, configuration access true,
no pending deployment recovery. A different worker's DNS/access failure does
not establish that this established MCP connection is broken.

## Verified evidence (Eastern Standard Time)

- November 13, 12:00:00–12:00:10 AM: midnight reminder completed, reporting two
  watched lights: Upstairs Hallway Main Lights and Back Stairs Back Stairs.
  Trace `79284b51271a09c7136f1284fb143837` passed the light-count, snooze and
  guard tests. The guard was not guest_override or vacation at midnight;
  clear versus up_late_media cannot be distinguished from that boolean test.
  HA invoked the notification script; this is not phone-delivery proof.
- Overnight auto-off is enabled, but last_triggered remains November 12,
  1:00:00 AM. Its sweep script's latest retained run is also November 12,
  1:00:00–1:00:08 AM (`be07f8f2b21588d51fdb2d72bfbc4865`). No November 13
  sweep execution is evidenced.
- Auto-off retains only five traces. At inspection these covered November 13,
  7:00–8:00 AM, all correctly failing the 1:00–5:59 AM operating-window test.
  The 1–6 AM evaluations have rolled out of retention. Latest trace
  `b3a92cd045d03186ca8cc7181e9d5b88` confirms the live conditions and prior
  last_triggered; it does not explain the earlier overnight failure.
- November 12, 6:58:57–6:58:58 PM: House guests script completed, calling
  input_boolean.turn_on for away_motion_security_guest_stay and clearing the
  away-motion alert. Trace `894d6b3b483c8f6ad6cf27840a79f299` verifies the
  requested activation action. It does not prove the helper remained on later.
  This helper does not participate in the live overnight auto_off_guard.
- Guest Lighting Override is a different helper: interior_lights_guest_override.
  Its start script's latest retained run is October 24. Direct helper changes
  are not ruled out by script-trace absence. Midnight guard evidence rules out
  active Guest Lighting Override at that instant only.

## Findings and limits

Confirmed: the midnight detector saw the two reported lights; the overnight
shutdown action did not execute on November 13. The live guard can block for
Guest Lighting Override, TV scene, TV lighting hold, actively playing Family
Room TV, or vacation. A future snooze and zero/unavailable light-count sensor
also prevent execution. The native MCP does not expose the queried Overnight,
Guest or TV entities; admin MCP has no general Recorder/history reader.
Consequently neither the current private guard states nor their overnight
history were retrieved here. Root cause remains unproven. Do not infer that
House guests caused this failure, or that lack of retained traces proves an
outage or failed light command.

Prior August 22 timestamp and August 30 paused-TV guard incidents were reviewed.
The current live guard still correctly tests actively playing TV rather than
paused media. TV-related suppression is a candidate, not a verified recurrence.
Snooze notification-action last_triggered is August 14, with no retained trace;
that does not exclude direct/UI helper edits. No relevant Nov 12 TV-scene or
Bedtime script execution was retained.

Next useful evidence is Recorder/history for the watched-light sensor and its
guard attributes, snooze, scene, TV hold/player, guest-lighting and vacation
helpers between midnight and 6 AM. A future authorized reliability change could
increase sweep trace retention beyond a full day and capture guard values;
no such change was made during this read-only task.

## Authorized hardening and deployment

Trevor subsequently requested diagnosing and hardening the failure, emphasizing
that cleanup has all night to retry. Preserve intentional TV/up-late, guest
lighting, vacation and snooze protections; House guests remains a separate
away-motion feature. No access/security changes or physical replay authorized.

Implemented in the existing lighting automation chunk and sweep script:

- Five-minute evaluations during 1:00–5:59 AM, including a final 5:59 check,
  replace the 15-minute all-day watchdog. A ready-state template resumes after
  30 seconds when lights need cleanup and protection clears. Snooze expiry,
  HA startup and automation reload also reevaluate. Template triggers are false
  outside the overnight window, avoiding daytime TV churn consuming traces.
- Preserve the existing two-pass cleanup and per-device error isolation. Scheduled
  calls now recheck protection and operating hours before every device command
  in both passes. Explicit manual Turn off now retains its existing behavior.
- Launch the sweep asynchronously and wait at most one minute for completion.
  A stuck child does not occupy the scheduler indefinitely; its existing restart
  mode permits a subsequent overnight attempt. Physical services can still fail;
  retries are not a guarantee against HA/network/device outages.
- Capture the actual count, names/IDs, guard, scene, TV hold/player, guest
  lighting, motion-only House guests, vacation, snooze and last script start in
  each evaluation trace. Retain 200 scheduler and 40 script traces. Last_triggered
  on the scheduler now means an evaluation, not necessarily a light command.
- Log overnight decisions and outcomes to Logbook. Logging errors are explicitly
  nonfatal and cannot prevent cleanup. Existing 30-day Recorder policy has no
  exclusion for these automation/logbook records; database persistence was not
  directly measured. Regenerated Recorder inventories, with no database available;
  Markdown output was unchanged, JSON generation timestamp refreshed.
- Scheduled unsuccessful cleanup sends at most one failure notice after 1 AM
  per day, using the existing restored overnight last-notified timestamp. A
  separate 6 AM review (with recovery attempts until 7 AM) explains lights then
  reported on or unavailable and the current protection reason. It never turns
  lights off or claims that a current reading proves all-night persistence.
  Morning dedup uses the same timestamp with a separate 6 AM boundary, stamped
  only after the notification returns. A reload/restart with a saved stamp
  suppresses duplicates. As with other send-then-stamp flows, a crash precisely
  between successful delivery and stamping can still duplicate a notice.
- Existing notification action buttons provide Snooze tonight / Turn off now;
  morning review offers Turn off now and the Lights destination. Existing clear
  handling removes the tagged notices when the watched light count reaches zero.
  No new helper or Core restart was needed; no changes to Evening, exemptions,
  guard policy, House guests, or unrelated devices/configuration.

### Validation and live evidence

- Six focused tests passed: all 1,440 minute boundaries, protected/unprotected
  readiness, per-pass protection checks and manual bypass, snooze, unavailable
  count, durable notification windows, bounded waits, recovery triggers and
  nonfatal logging. Six existing Evening tests also passed.
- YAML parsed; semantic comparisons showed only the overnight scheduler, new
  morning review and sweep script differ from the fresh live baseline. Inventory
  coverage passed for 180 active control references. Focused diff checks passed.
- Reviewed MCP deployment `697bc246d19340a0a2684261a6d7c49b` applied November 13
  with HA configuration validation OK and script/automation reloads completed.
  No Core restart. Exact live hashes matched the reviewed plan:
  automations `d7f146168101787da1e87c6452795edd94f2c0599a5705ad46812e97851dac99`;
  scripts `b473329deb17899259eeef662903bf72a91bff83148923e0e3e06295d2a1085a`.
- Both automations loaded enabled. Natural reload traces at **8:14:56 AM EST**
  (`74795d8b0826de72398c8e85252e0cc5` scheduler,
  `6598ccc89a932f3cd6b0f182775b4050` morning) captured current variables and
  correctly stopped at their time-window condition, with no error, physical
  command or test notification.
- Current-only observation: guard clear; TV player paused; TV hold, guest
  lighting, House guests and vacation off; snooze expired. Ten daytime lights
  reported on, including Back Stairs but not Upstairs Hallway. Script last start
  remains November 12 at 1 AM. These current values do not reconstruct the
  November 13 overnight guard history or establish the original root cause.

Next-night verification remains: observe a natural unprotected sweep, any
protected deferral and subsequent retry, actual device convergence, persisted
decision records, and any real failure/morning notice. No scheduled follow-up
agent or physical replay was created. Runtime/config verification is complete;
the next-night physical outcome is not yet observed.
