# Fertilizer notification removal

Trevor explicitly requested removal of the no-longer-needed Fertilizer time
notification after harvest. Earlier native helper and automation action paths
could not match unexposed entities; no mutation occurred through those paths.

Removed only the fertilizer item construction from the house notice timeline
and its dedicated biweekly reminder sender. Preserved action handlers, historical
helpers/scripts, irrigation, all other notices, and the separately managed April
2027 planning reminder. This is permanent until deliberately restored, not a
snooze or a helper toggle that resets at startup.

Direct administrative MCP deployment: `4b1dfc08dfbd49d3a72fba867a046d09`.
Existing deployment backups preserve exact originals and support guarded rollback.
Reviewed complete diff; live/repo differences were preserved. HA config validation
passed; automation and template reloads completed without Core restart.
Live file readback confirmed the timeline item and exclusive sender absent, with
no remaining sender calls in the live automation file. Automation discovery shows
the removed sender unavailable (unloaded registry remnant), and the fertilizer
notification action handler still on. Device inventory coverage passed.

Native timeline state is not exposed. The originating agent reported completed
desktop verification through native CUA Safari after refreshing
`/calm-mobile/notices`: Needs Attention decreased from 2 to 1, leaving only the
existing Water guardrail; Upcoming decreased from 18 to 17. The screenshot
confirmed Fertilizer time absent and unrelated Recent laundry notices preserved.
The full accessibility tree contained no fertilizer text. This UI evidence is
attributed to the originating agent's final verification handoff, not a second
desktop inspection by this worker. No further live changes were made.
Dormant historical helpers/scripts remain intentionally preserved; no automatic
reactivation was created. Prior Recent history may remain as historical evidence.
