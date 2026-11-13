# Overnight lights stayed on — November 13, 2026

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
