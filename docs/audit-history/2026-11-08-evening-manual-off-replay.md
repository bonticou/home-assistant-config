# Evening replay overrides manual Family Room off

## Result

Scoped fix deployed November 8 after Trevor approved preserving manual changes
until he explicitly chooses Evening again. See implementation evidence below.

Read-only diagnosis on November 8, 2026, Eastern time confirmed that the
Evening recovery rule reissued Family Room lighting commands after a configuration
reload and again on its five-minute refresh. No configuration, reload, scene,
light command or notification was issued during this investigation. The diagnostic findings below precede the subsequently authorized fix.

Trevor reported turning off the Family Room main lights to watch TV while
Evening was active, then finding them back at the Evening setting a few minutes
later. The August 3 catch-up audit documented a related manual-override risk;
the August 26 stale-helper correction retained that repair behavior.

## Live evidence

The existing Home Assistant administrative MCP read the current automation,
script and retained traces. The native context and diagnostic template supplied
current state. The documented CLI route could not resolve the local HA host;
this was a transport failure, not an access denial. Native admin MCP succeeded.

- At 8:25, 8:30 and 8:35 p.m., refresh traces failed the final eligibility
  condition and did not invoke Evening.
- At 8:36:47 p.m., an `automation_reloaded` trigger passed all conditions and
  invoked `script.lights_evening_scene`. That reload was from the earlier
  dehumidifier passive-monitor deployment, not this investigation.
- At 8:36:54 p.m., the Evening script issued `light.turn_on` to all three
  `light.family_room_main_lights_*` members at 10 percent with a one-second
  transition.
- At 8:40 p.m., the `refresh` trigger passed and issued the same Family Room
  command. Both script traces finished with no recorded Family Room action error.
- At 8:43:34 p.m., the active scene was Evening, TV hold was off, all three
  Family Room mains were off, and the other three expected lights were on.

Automation trace references: `736e61ce51be94f151431ca15b8e7250` (reload) and
`dd577dcda04bb413013151680db910d4` (refresh). Script references:
`01d3ba4c41d966ecad6138c39dc554c7` and
`a99726340fd710a394ab782cb504f490`. These are retained-trace identifiers, not
permanent archives. Physical history and the identity of whoever subsequently
switched off the lights were not retrieved. Commands are proven; every resulting
physical transition and earlier incidents outside retained traces are not.

## Cause

`interior_evening_mode_schedule_sync` treats an expected light being off,
unknown or unavailable as a scene failure. Startup and automation reload can
replay current-day Evening for this reason without a recent-run limit. The
five-minute refresh can replay it within 1,200 seconds of the script's latest
execution. Each replay renews that timestamp, so repeated manual offs or an
unavailable expected light can keep extending the retry window. The entire
scene is reasserted rather than only the presumed missing target.

Directly turning off Family Room mains does not select TV or enable
`input_boolean.tv_lighting_scene_hold`. Explicit `script.lights_tv_scene` does
both; mere television playback is not a scheduler guard. The Evening script
clears the TV hold.

## Recommended scoped fix

Remove missing-light repair eligibility from both the refresh and
startup/reload branches. Preserve catch-up when the scene is None or Evening
has not run since noon that day, existing dusk/arrival behavior and genuine
arrival filtering, schedule/presence/vacation/guest guards, and explicit
TV/Bedtime protection. This respects manual adjustments after current-day
Evening has run while preserving the normal scheduled entry behavior.

Tradeoff: periodic partial-scene repair is removed. If required later, design a
bounded retry tied to the original invocation rather than an eligibility window
renewed by each replay. The scene helper currently has `initial: None`; startup
catch-up after a full restart remains distinct from current-day manual override
protection and would need separate review if persistence across restarts is
requested.

No fix authorization or deployment was part of this diagnostic pass. Re-read
live files and hashes, test the relevant branches, review the minimum diff and
verify the next natural refresh after any future authorized change. Do not
replay a physical scene solely for testing.

## Authorized implementation - November 8, 2026

Trevor approved: "Yes. Unless I put it back into evening mode again in order to
resets everything". Removed only missing-light repair eligibility from the
scheduler's final condition. Startup/reload/refresh still catch up when the scene
is None or Evening has not run since noon today. Dusk/arrival conditions, genuine
first-arrival filtering, TV/Bedtime/guest/vacation and schedule guards are unchanged.
No script, dashboard, helper or other automation behavior was edited.

### Explicit Evening reset

Fresh live Home and Lights dashboard YAML each has an Evening button whose tap
calls script.turn_on targeting script.lights_evening_scene directly. The active
scene entity drives styling only; tapping an already-selected Evening does not
rely on a dropdown value changing. The live script has mode restart, no current-
scene eligibility gate, selects Evening and executes the full existing scene.
The House Modes bridge exposes that same script as Evening Lights. This verifies
configured entrypoints, not an Apple Home client interaction. No button, HomeKit
switch or scene was actuated solely for testing.

### Checks and deployment

Five targeted unittest methods pass: current-day protection for all triggers;
None/stale-day catch-up; TV/Bedtime and existing All off branch behavior;
genuine-arrival guard including tracker recovery; and both direct dashboard
script entrypoints. Semantic comparison proved exactly one condition changed
in live automations.yaml, with every other definition preserved. Repo/live
conditions parse identically. Prepared diff reviewed, YAML parsed, diff checks
passed. Prior live monolithic layout preserved.

Pre-reload state was Evening, TV hold off, expected lights on; corrected condition
was false for this current-day scene. Deployment/recovery ID:
2e7b85ccf3a44a3fb28f1c3d5104cb55. HA validation passed; automation reload completed;
no Core restart, script reload, test scene or direct light call. Live readback
SHA256 dbc9d8adf6f6e3790e3d1ea8171f55adf0f96048c7bb57cb7bd5e53451cfbca7 matched.
Reload trace 2faf7b7d4c3e54b1b645f857987d73cc at 8:48:03 PM Eastern contains the
new condition, fails condition/9 and has no action/0. Evening script's latest
execution remained 8:45 PM (the old repair rule before this deployment).

Limits: physical repeat-tap behavior is verified by direct action/script wiring,
not a disruptive runtime replay. The pre-existing helper initial None behavior
on full Core restart remains intact, so initial catch-up can still run then.
No claim of preserving manual overrides through a full restart. Periodic partial-
scene repair is intentionally removed; unrelated live and working-tree changes
were preserved.

Natural refresh verification at 8:50:00 PM Eastern: trace
c207690346733d791093183f18c57233 fails the new condition/9 and has no action/0.
Evening script still last executed at 8:45 PM, before deployment. Live Lights
page visually presents the existing Evening control; it was not pressed.
