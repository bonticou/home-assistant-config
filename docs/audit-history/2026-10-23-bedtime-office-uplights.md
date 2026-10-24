# Bedtime office uplights omission

Trevor reported Office Uplights remained on after Bedtime on October 23 around
22:35 America/New_York and explicitly requested a fix. Reviewed the operations
map, October 18 Office Uplights audit, and October 16 bathroom exclusion.

## Evidence and finding

Live Home dashboard and Lights Bedtime buttons target script.lights_bedtime_scene;
the House Modes HomeKit bridge exposes that same script as Bedtime Lights.
Retained run `77a07bbac504f9b6a4542fba0111811a` started October 23 at
22:34:40.836 and finished at 22:34:42.916 local time. Its switch.turn_off step
completed with Great Room uplights, flower lamp, garage and exterior mudroom
switches, but no switch.office_uplights. The live script matched this omission.
This establishes no office command was attempted by that run, rather than an
office command failure. It supersedes the October 18 decision to match Office
Main's Bedtime omission for the new plug. The broader office state history was
not retrieved; no claim is made about who subsequently switched it off.

Native state readback found Office Uplights already off before this fix and off
again afterward. No physical action or full Bedtime replay was performed.

## Minimal correction and verification

Added only switch.office_uplights to Bedtime's existing switch.turn_off target
list. Office Main, master bathroom exclusion, security/locks and all other actions
remain unchanged. Semantic comparison confirmed exactly this one target addition;
live and repo Bedtime objects match. YAML parsing, diff checks and device inventory
coverage passed. Unrelated live/repo drift was preserved.

MCP deployment/backup `966c1effa3374308b6d18566e75ca1ad` applied successfully:
HA config validation OK, script reload completed, no Core restart. Exact live
readback hash matched `61ced2c546d021c68f14707310cc3f854d01d7444fd1eb560c4509b0199cfc9f`.
The same dashboard/HomeKit entrypoints now use the reloaded script. Verification
covers deployed configuration, reload success and current off state, not a new
physical scene trial; inspect the next naturally occurring Bedtime trace if needed.
