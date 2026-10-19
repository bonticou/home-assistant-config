# Office Uplights — October 18, 2026

## Request and evidence

Add the new Kasa Office Uplights to Lights and the existing office lighting rules and notifications. Reviewed prior bathroom discovery, Bedtime exclusion, compact Lights layout history, and MCP deployment runbooks.

The first discovered EP25 was Family Room Uplight; the user confirmed it was a different device. Later discovery exposed Office Uplights EP25. Added it through the TP-Link integration and assigned it to Office. The device page reported On, power consumption, and healthy device diagnostics; native MCP independently confirmed On in Office.

## Findings and changes

1. Office Uplights was not yet configured in HA. Discovery/setup resolved that.
2. Plug switches do not participate in the existing light-domain enumeration automatically. Added `switch.office_uplights` consistently to away lighting count/names/entity IDs and overnight count/names/entity IDs.
3. Existing Office Main participates in All Off but not Evening or Bedtime. Matched that behavior, preserving scene intent and the bathroom Bedtime exclusion.
4. Added a compact on/off button beside Office Main using the existing switch styling. Existing notification and overnight sweep paths consume the updated sensors; no duplicate alert automation was added.

The separate Family Room Uplight was also integrated during identification. Its existing name was preserved and no new dashboard or lighting rules were assigned to it. Both targeted device registry additions are inventoried. Recorder reports were regenerated without a database snapshot; they contain no measured DB frequency evidence.

## Validation and deployment

- YAML parsed for all three repository files and three live candidates.
- Explicit semantic check confirmed Office Uplights and Great Room Uplights are separate All Off targets and no other script acquired the Office target.
- Device inventory coverage passed: 178 active control references.
- Prepared diff reviewed. Live/repo formatting and unrelated configuration differences preserved with focused live patches.
- MCP deployment applied successfully, verified file writes, HA validation OK, script and template reloads completed. No Core restart.
- Live Lights page visually rendered Office Main and Uplights with current On state.

## Limits and follow-ups

No physical toggle, All Off execution, or notification delivery was triggered for testing. The overnight sensor is not exposed to the native MCP context tool, so its live attributes were not independently read. A local Jinja rendering probe could not run because Jinja2 was unavailable in the YAML-check runtime; HA's own configuration validation and template reload succeeded. Monitor the next naturally occurring away/overnight cycle if behavior needs investigation.

The main configuration file remains above the decomposition threshold documented in AGENTS.md. This narrowly scoped addition preserves the current structure; a dedicated include split still warrants separate reliability work.
