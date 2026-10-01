# Parking Pass Morning Application Reminder

## Symptom And Prior Context

Trevor reported that the NWP parking-pass expired notice arrived after he could
already have left for his commute. He requested 7:30 AM delivery and an
application reminder five days before expiration because the replacement must
be requested in advance.

Reviewed the July 1 notification due-boundary and parking-cycle repair, the
August 22 native timestamp findings, notification reliability patterns, and the
deployment runbook. Preserve the exact handled-expiration cycle introduced in
July; applying alone must not mark a replacement as confirmed.

## Evidence And Findings

1. High confidence: the fixed trigger was 9:13 AM, while post-send and explicit
   snooze timestamps scheduled the next reminder at 9:00 AM. The live instance
   uses America/New_York. Tomorrow already had a 9:00 AM reminder saved.
2. High confidence: the application window opened only one day before expiry.
   Dashboard details also explicitly described that one-day lead time.
3. High confidence: aligning both old triggers at 7:30 would introduce competing
   triggers and dependence on a cached due sensor at the snooze boundary.
   Direct native timestamp checks avoid both that race and the previously
   documented plain-datetime timezone parsing error.

## Changes

- One daily 7:30 AM trigger; application reminders begin five calendar days
  before expiration and continue each morning until replaced or snoozed.
- Distinct application, expires-tomorrow, expires-today, and expired wording.
- The send script checks current enablement, expiration cycle, native snooze
  timestamp, and local clock before sending. Single execution plus the durable
  next-morning timestamp suppresses repeat calls; stamping remains after send.
- Both generated snoozes now end at 7:30 AM. Migrated the existing next-day
  9:00 AM helper to 7:30 AM on the same date.
- Reminder-open/status/due templates and dashboard details use five days.
  Needs Attention recognizes an open application window while Upcoming retains
  the actual expiration date. Existing shared send-throttle/snooze behavior is
  retained, so a push holds the next reminder until the following morning.
- Regenerated Recorder inventory; recording policy and reported counts remain
  unchanged. No database copy was used for this timing change.

## Checks And Deployment

- Six focused template checks passed: five-day boundaries and copy; disabled,
  missing-expiry and handled-cycle guards; exact 7:30 boundary and duplicate
  suppression with restored helpers; snooze and both DST transitions; one
  scheduled trigger; timeline action window with real expiration date.
- All three changed YAML files parsed; inventory coverage and diff checks passed.
- Deployed only parking sections in live automations, scripts and configuration.
  The live monolithic automation file and serialized script formatting differ
  from the repository; unrelated content was preserved. Existing script
  semantics were checked against the repository before replacement.
- Full live file read-back matched every write. Home Assistant configuration
  check returned valid with no errors or warnings. Script, template and
  automation reloads completed without a Core restart.
- Live automation config reports the single `07:30:00` trigger. Reminder-open
  state is five days before saved expiration. The pending helper reads
  `2026-10-02 07:30:00`.
- Invoked the guarded reminder script with that restored future timestamp:
  the phone notification script did not run and the timestamp stayed unchanged.

## Status And Residual Limits

Deployed and verified October 1, 2026. Actual scheduled phone delivery will occur
at the next eligible 7:30 AM; this verification did not generate another push.
As before, the daily clock trigger requires Home Assistant to be running then.
Confirmed replacement and snooze actions remain the existing controls.
