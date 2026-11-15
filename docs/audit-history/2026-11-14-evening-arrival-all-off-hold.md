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

## Read-only morning verification — November 15, 2026

HA-ARRIVAL-VERIFY-20261115 checked approximately **9:26–9:28 AM EST**
(14:26–14:28 UTC). **Terminal result: INCONCLUSIVE for natural first-arrival
activation; no post-deployment Evening invocation was evidenced.** This is not
proof that no genuine arrival occurred. No runtime changes or test triggers.

Deployment boundary remains November 14 **7:23:43 PM EST** (November 15
00:23:43 UTC). The previously observed 7:17 arrivals and 7:20:55 Evening
invocation are before this boundary and cannot qualify the fix.

- Admin MCP health succeeded: Core/API 2026.9.2, config access available and no
  pending recovery. No access/security or credential changes were needed.
- Arrival scheduler retains only five traces; these now cover November 15
  **9:05–9:25 AM EST**, all background refreshes. The 9:25 trace
  `2e0e4f3404860a5ac1787c635912d44b` contains the corrected All off arrival
  exception. Scene and hold conditions pass; front-stairs schedule is off, so
  execution stops before any action. This is morning behavior, not arrival proof.
  Its loaded-state timestamp matches the deployment boundary; last_triggered is
  November 14 **2:20 PM EST**, before the fix.
- Evening script's five retained runs span November 12–14. Latest is
  `e836feed9c6ec04057186040f17207a6`, November 14 **7:20:55–7:20:56 PM EST**,
  also before deployment. No retained post-deployment invocation or resulting
  Evening light-action/state evidence exists in this bounded source.
- A separate person-home-triggered vacation-return automation retains five
  Casey transitions at **4:03:56, 4:04:11, 4:04:26, 4:04:42 and 4:04:57 AM EST**
  on November 15. All five actual trigger payloads are **unknown → home**,
  not known-away → home; these do not qualify under the genuine-arrival rule.
  Vacation was off at each. Representative first/last runs:
  `201c3aec51a833669498cfdf3efba8d2`,
  `c6167b763cb8ad81aa56b5a2cb9d2480`.
  Companion away-motion-clear traces show corresponding phone-home triggers.
  Neither source preserves the other person's state or full scene/schedule/
  guest conditions at those times. No tracker repair attempted.
- Native MCP's person-domain query returned no exposed entities. Admin MCP
  provides retained traces, not general person/Recorder history. No undocumented
  API/SSH/history fallback was used. Current states would not reconstruct the
  missing evening window in any case.

Coverage gap: evening arrival scheduler traces since deployment were evicted by
five-minute refreshes, and the independent person-event traces have also rolled
to the later recovery transitions. Therefore no qualifying first-person evening
arrival can be established or ruled out for the full post-deployment interval.
The corrected configuration is still loaded, but natural end-to-end success
remains unverified. Additional verification needs an actual known-away first
arrival with its contemporaneous trace retained; this check created no schedule,
increased retention, reload, simulated arrival, notification or light action.
