# Casey closet delayed Protect feed — 2026-09-10

## Symptom and historical context
Trevor reported another missed closet auto-on late afternoon/early evening on
September 9. Reviewed the audit-history index, June 25 Lutron disconnect,
August 24 stale motion incident, and August 30 motion timestamp fallback.
Earlier incidents included both missing Protect motion and failed Lutron commands.
The successful August 30 walk test demonstrated temporary recovery, not a
permanent integration fix.

## Evidence
Read-only live Recorder query covered September 9, 2 PM–10 PM Eastern:

| Protect event time | HA timestamp entity update | Arrival delay |
| --- | --- | --- |
| 6:00:56 PM | 6:09:39 PM | 8 minutes 43 seconds |
| 6:32:29 PM | 6:39:39 PM | 7 minutes 10 seconds |

The binary motion sensor stayed off, the processed-motion helper did not advance,
and the closet light stayed off across that window. Today's timestamp also
arrived roughly eight minutes late. Both closet automations were enabled;
motion detection was enabled and battery read 92 percent.

The live helper held 12:21:47 local from an event at 12:21:47 UTC, written at
12:24:36 UTC on September 9. Live template evaluation confirmed bare
`.astimezone()` uses the HA host's UTC timezone, whereas `as_local` uses the
configured Eastern timezone. The processed-motion stamp was four hours ahead.

Live diagnostics report Home Assistant 2026.7.1 and UniFi Protect 7.2.105.
Historical registry evidence identifies Casey's device as USL Motion. Official
2026.8 release notes add USL sensor support; the corresponding merged change
moves sensor handling to the public API and sensor capability map.

Protect and Lutron entries report loaded. Retained system logs include 53
aggregated Lutron reconnect/ping/network errors, but no retained Protect-specific
log entry was found. Those Lutron errors remain relevant historical evidence;
they do not explain this window's absent motion trigger by themselves.

## Ranked findings
1. Confirmed: HA did not receive a timely closet motion trigger. Both delayed
   timestamps were older than the fallback's five-minute limit when received.
   Widening that limit would switch lights on long after someone walked in.
2. Strong hypothesis: old integration support for the USL sensor family is
   behind recurring realtime feed failures. The delayed timestamp updates are
   consistent with periodic refresh replacing missing push delivery. No packet
   capture proves exactly where the realtime connection fails.
3. Confirmed additional bug: UTC text was saved as local helper time, creating
   four hours of erroneous deduplication and misleading stale-recovery labels.
4. Lutron command reliability remains a separate concern; no light command was
   necessary to explain these missed triggers. No physical light test was run.

## Minimal fix
- Save processed motion with input_datetime `timestamp` (epoch seconds).
- Reject future-dated events as well as stale/duplicate events.
- Format stale-motion labels with `as_local`.
- Preserve the five-minute freshness boundary, light retries and hard cap.
- Correct the known erroneous live helper only if its timestamp still matches
  the exact pre-fix value; do not overwrite a newer event.

## Checks and deployment
Ruby YAML parse and whitespace checks passed. Recorder inventory generator ran
without a copied DB; only generated_at changed, with Markdown output unchanged.
No new entities were introduced.
The lighting file was written through mounted File Editor ingress and read back
with SHA-256 `504fb5edb6baf1a7eadf8e0a6397c2e2e5a88f2b482b389c59e0697a95efbaa8`.
Home Assistant config check returned valid with no errors/warnings, and automation
reload completed. Runtime freshness/timezone tests and helper repair were run;
final results are recorded below.

## Remaining work
A supported Home Assistant Core upgrade is the substantive next recovery path;
review target-version compatibility and backup/restart readiness before upgrading
the whole home. Then verify actual USL motion delivery and a physical walk test.
No Core upgrade, firmware change, sensor replacement, or recurring reset loop
was performed in this investigation. The timezone fix alone does not repair the
missing realtime feed and should not be reported as a complete closet fix.

## Primary sources
- https://www.home-assistant.io/blog/2026/08/05/release-20268/#noteworthy-improvements-to-existing-integrations
- https://github.com/home-assistant/core/pull/175592
- https://github.com/home-assistant/core/issues/172164

Final runtime results: fresh event accepted; duplicate, ten-minute-old, and
future events rejected. Local/epoch round-trip passed. The guarded helper repair
completed and loaded automation config confirms the epoch `timestamp` field.
