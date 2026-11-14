# Overnight lighting natural verification — November 14, 2026

**Result: PASS for the natural unprotected cleanup and overnight monitoring path.**
Read-only check HA-OVERNIGHT-VERIFY-20261114, completed approximately 8:44 AM EST
(13:44 UTC). No HA changes, device commands, replay, test alerts or access changes.
Reviewed the November 13 investigation and hardening before retrieving retained
traces through the existing admin MCP. Health: Core/API 2026.9.2, configuration
access available, no pending deployment recovery.

## Actual timeline (EST; UTC is five hours later)

| Time | Observed result | Retained run |
| --- | --- | --- |
| 12:00:00–12:00:05 AM | Midnight reminder completed for Upstairs Hallway Main Lights and Back Stairs Back Stairs; timestamp action followed notification call | `c321777211ee9bf7bfd387fb51c807c3` |
| 1:00:00 AM | Scheduler captured two watched lights, guard clear, Evening scene, TV paused, TV hold/guest lighting/House guests/vacation off, snooze expired | `01eec4570f1231bca12ef8707b7e2b1a` |
| 1:00:00.502 / .525 AM | Script rechecked protections successfully before each turn_off command: upstairs hallway, then back stairs | `8ed4a97878289be2dfe4d621118bd6a5` |
| By 1:00:08.587 AM | Script completed; second-pass remaining list empty. Scheduler remaining_count 0 and remaining_names empty; bounded wait completed successfully | Same script and scheduler runs |
| 1:00:08.587–1:00:09.372 AM | Separate reporter received cleanup result 0, chose clear-notification branch and completed; scheduler finished at 1:00:08.599, before reporter finished | `bf73b1484a5e79c1177ca688d680c599` |
| Every five minutes, 1:05–5:55 AM | All 59 further scheduled checks recorded watched_count 0 and stopped at the positive-count condition, without further device commands | Full retained scheduler interval inspected |
| 5:59:00 AM | Final check ran, watched_count 0, all watched lights off according to aggregate sensor | `e4647699bc5a4c00e53a781d2f4d0c84` |
| 6:00:00 AM | Morning review recorded count 0 and stopped before notification | `6ec536eb1cf9506db1682fc01b48b2fa` |
| 6:00 template tick and every five minutes through 6:55 AM | All morning recovery checks also recorded 0 and sent no morning notice | Last `0a975964f61ad6287bebb7eb01bfb5e8` |

All 61 scheduled overnight evaluations were present: 60 five-minute checkpoints
from 1:00 through 5:55 plus 5:59. Exact expected-minute comparison found no gap.
Detailed traces were read for all 61, all 13 morning runs (including the separate
6:00 time and template triggers), midnight reminder, script and reporter: 77
natural runs total. No top-level trace error was found. Later scheduler traces
labelled aborted stopped intentionally at the zero-light condition, not a failure.

## Protections, delivery and evidence limits

All sampled overnight/morning guard snapshots were clear: TV paused, TV hold off,
guest lighting off, vacation off and snooze expired. House guests was off and
remained separate from lighting protection. No blocking-to-clear transition,
failed device retry, service timeout, restart recovery or failure/morning notice
was exercised naturally this night. Those branches retain prior test/config
evidence, not a newly demonstrated real-world outcome.

Only the two named lights appeared in the actual script target list. The second
pass had no targets, so its per-command guard branch was not exercised. No exempt
light was commanded; the traces do not establish historical on/off states of
intentional exempt lights. Zero watched-light count and an empty remaining list
are HA aggregate convergence evidence, not independent visual confirmation or
complete individual entity history. Brief state changes between checkpoints, or
unavailable lights excluded by the watched sensor, cannot be ruled out here.

The midnight send and later clear call returned through their parent automations
without reported error. Reporter independence was observed: it completed about
0.77 seconds after the scheduler had already finished. Its notify child run
`b1e4474df541f8fc11fc3b13df10255d` was no longer retained when requested; exact
mobile-service details and handset receipt/clear were not independently verified.
No failure notice or morning review notice was sent by these observed runs.

Scheduler decision/result Logbook actions were represented in the traces; actual
Recorder database persistence was not queried. No general API/SSH/history
fallback, credential attempt, current-state inference of overnight history, or
additional schedule was used. The November 12–13 failure's original cause remains
unknown; this successful night does not retroactively identify it.

**Terminal status: verification complete; no repair performed or required by
this night's observed path.** Broader guarded/failure recovery and physical
confirmation remain bounded as above. Return evidence through the existing bridge.
