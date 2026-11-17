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

## Scheduled read-only verification — November 16, 8:59–9:00 AM EST

**Result: no qualifying evening arrival identified; insufficient retained evidence
to certify the first-arrival fix.** This is not a verified arrival success or
failure. No runtime changes, test triggers, access changes or outbound message.
Existing scheduled verification/delivery remains owned by Eames. The preceding
automatic-review rejection is not treated as a completed check; these are fresh
supported MCP reads under the supplied standing read-only instruction.

- Health succeeds (Core/API 2026.9.2, config access true, recovery empty).
  Scheduler still contains the November 14 All off hold exception. Its retained
  five traces cover November 16 8:35–8:55 AM, all background refreshes stopped
  by the daytime schedule. Latest `bb87f68512397f113b61aec8cffe255d` confirms this.
- There is a **post-deployment Evening execution on November 15 at 3:25:00 PM
  EST** (20:25 UTC), script trace `cc2742a81a5cf9ce15cd5c399b8ee7be`.
  It selected Evening, cleared the three lighting holds, issued normal scene
  commands and finished at 3:25:00.685 without a recorded error. Scheduler
  last_triggered is 3:25:00.094 and shares context
  `01M7GE4XDW670P6CTVAZ7ZM9TK`, establishing the scheduler/script relationship.
  The original scheduler run/trigger is no longer retained. Timing alone does
  not prove arrival; completed service calls are not physical state verification.
- Independent person-home traces retain November 15 known-away returns:
  Trevor **11:39:53 AM** (`89a868768101d4750b94d46bc7db9b03`), Trevor
  **1:33:35 PM** (`7e5e8e5ecc9c28fd73c621d36ac3e135`) and Casey
  **1:33:47 PM** (`1dd242a4400c8ea0b30ee96967ee1e2d`). Each payload is
  not_home → home. These are earlier than the 3:25 Evening run, not a matched
  evening-arrival activation. That separate automation stops at vacation off;
  it does not record the other person's state or scene/schedule/hold/guest
  conditions needed to qualify the corrected path. No later person-home event
  is in that retained list, which also still contains two earlier recovery runs.
- Do not count the 3:25 Evening run as validation of the arrival exception. No
  matched first-person evening arrival + eligibility + Evening execution chain
  is available. The original November 14 7:23:43 PM EST deployment boundary
  remains controlling; November 14 pre-deployment events remain excluded.

No general API/history or credential fallback was attempted. Retention prevents
complete historical reconstruction. Continue the existing bounded verification
under its original seven-day limit; no duplicate schedule created here.

## HA-ARRIVAL-VERIFY-20261117 — November 17, 9:05–9:06 AM EST

**Result: insufficient retained evidence; an evening return is observed, but
qualification and activation/failure cannot be established.** This is neither
"no arrival occurred" nor verified success/failure. Reviewed the existing audit
and prior check before fresh supported MCP reads; no matching completed November
17 check was present in the owning record. No runtime changes or outbound sends.

- Deployment boundary remains November 14 7:23:43 PM EST, fix ab01da3.
- Evening script has one retained run: **November 16 6:40:02–6:40:03 PM EST**
  (23:40:02 UTC), `4f570a997e005a6b3b0d028fdd0ba8dd`, context
  `01M7KBPRDYHZPDRQHWBC1H2T1X`. It selected Evening, cleared the three holds,
  issued the normal light commands and finished without a recorded error.
  Scheduler last_triggered matches 6:40:02.366748. The original scheduler
  trigger/eligibility trace is absent; completion of commands alone is not
  physical convergence or evidence of a first-person arrival.
- **Trevor returned not_home → home at 6:58:20 PM EST November 16**, verified
  by independent person-triggered trace `69eec3ff8ce730508bf3ec74c771d140`.
  Vacation was off. This is about 18 minutes AFTER the retained Evening run,
  so that run cannot be attributed to this return. The trace lacks Casey's
  contemporaneous state and the scene, hold, schedule and guest-lighting guards.
  It therefore does not establish that this was a qualifying first arrival.
  No subsequent Evening invocation is retained; without those prerequisites,
  do not call this an arrival failure.
- Casey's retained **5:57:33 AM EST November 17** transition is unknown → home,
  trace `667c863e2c2a08427b90c8715b61f5d9`; it is tracker recovery, not a
  qualifying known-away return.
- Scheduler's five retained traces cover **8:45:11–9:05 AM EST November 17**,
  including a natural HA-start trace at 8:52:38. Latest
  `842a668d5e42b8d0f4cb50673e8e036c` passes scene/hold guards and stops because
  the front-stairs schedule is off. These morning checks cannot reconstruct
  November 16 arrival conditions. The changed retention population and startup
  further limit historical coverage; this task did not restart HA or investigate
  that independent startup.

Admin health/read access succeeded (Core/API 2026.9.2, recovery empty). The
blocking issue is missing contemporaneous historical eligibility evidence,
not authentication. No general API/history fallback, simulated arrival, scene
call, diagnostic deployment, retention change or new schedule used. No resulting
historical light-state evidence qualified for the arrival was available.
Existing bounded verification remains inconclusive; caller owns quiet follow-up
and the original seven-day deadline. Do not deliver a success/failure notice on
this evidence alone.
