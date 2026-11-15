# Evening arrival blocked by All Off hold

## Evidence and cause

Trevor reported another failed homecoming after the November 12 arrival fix.
Live traces prove that correction remained loaded. On November 14 at 3:01:21
p.m. Eastern, All Off ran and set `tv_lighting_scene_hold` on, along with stair
and foyer holds. At 3:46 p.m. the metadata reset saw All off and an active dark
schedule, so intentionally retained the scene and holds. At 7:17:23 Trevor's
arrival and 7:17:44 Casey's arrival both stopped at condition 1 because the TV
hold was on, although the first guard passed (scene was not TV or Bedtime).
The previous correction addressed final eligibility but missed this earlier
shared hold gate. An Evening invocation at 7:20:55 preceded this deployment;
this worker did not initiate it.

## Scoped correction

Under Trevor's request to fix the recurrent failure, replace only the blanket
hold-off requirement with: hold off OR arrival while scene is All off. The
existing genuine-first-arrival gate still rejects tracker recovery, repeated
home state and second-person arrivals. TV and Bedtime scene protection, schedules,
vacation/guest guards and background/manual-light-change protection stay intact.
Do not clear the shared hold on departure or change All Off itself. The existing
Evening script clears holds when the eligible arrival actually runs it.

## Verification

- Seven targeted unittest methods pass, including a 100-case hold/scene/trigger
  matrix, both people's arrival guard, current-day Evening replay, background
  suppression, TV/Bedtime exclusion and explicit Evening wiring.
- Ten administrative bridge tests pass; YAML parses and semantic comparison
  proves exactly one condition changed in live automations. Local/live condition
  matches. Unrelated local and live edits preserved.
- Reviewed deployment `45448c7217114ad89f5385462804a8c4` applied successfully;
  real HA configuration validation passed, automation-only reload completed,
  and no Core restart occurred.
- Exact live readback SHA256:
  `d841f7ebfc607beea8681020e6cb81b1af41a13e6353a5954fa02c39c5cb2ed4`.
- Reload at 7:23:43 p.m. contains the corrected guard and stops at final
  eligibility with no actions. No light actions or simulated arrivals used.

## Remaining verification limit

The next genuine first-person return from All Off is the physical end-to-end
check. This change does not bypass a real TV or Bedtime scene, or reinterpret
unknown scene metadata as an arrival permission. Retained traces are ephemeral.

## Record reconciliation — November 15 UTC

Implementation commit: `ab01da3`. Live deployment and test evidence above remain
the verified result; next real arrival is still unverified. Parent has already
scheduled the trace check. No additional automation created during reconciliation.
