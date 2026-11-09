# Evening replay overrides manual Family Room off

## Result

Read-only diagnosis on November 8, 2026, Eastern time confirmed that the
Evening recovery rule reissued Family Room lighting commands after a configuration
reload and again on its five-minute refresh. No configuration, reload, scene,
light command or notification was issued during this investigation. The fix
below is recommended, not implemented.

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
