# Office vacation occupancy lighting

## Request and history

The user clarified that the externally visible office lights should simulate occupancy. They explicitly selected Vacation mode only, not ordinary evenings when both people are away. Reviewed the Office Uplights addition and June vacation-return incident, including the missed exterior cleanup regression.

## Findings and change

Both Office Main and Office Uplights were missing from vacation simulation. Added them to evening lived-in, late glow, and pre-sunrise phases. Main uses the existing family-room brightness curve and transitions; the plug follows the existing uplight on/off behavior. Added both to inactive-window and vacation-end cleanup to avoid leaving simulated lights on after return.

Away-light count, names, and entity IDs now consistently exempt both office controls only while vacation mode and an active evening/pre-sunrise window are present. Ordinary away behavior, normal Evening, Bedtime, and the existing vacation-return handoff remain unchanged. The existing overnight vacation guard still applies. No new notifications or automation triggers were needed.

## Checks and deployment

- Parsed repository and live-candidate YAML.
- Semantic checks verified both controls in all three on phases and both cleanup paths, with all unrelated scripts unchanged.
- Device inventory coverage: 178 active references passed. Updated inventory behavior notes and regenerated Recorder inventory.
- Fresh live hashes and focused patches preserved unrelated live/repo differences. Prepared diff reviewed.
- MCP applied successfully: HA validation OK, files verified, script and template reload completed, no Core restart.

## Limits and follow-up

Did not enable vacation or execute the whole-house simulation for testing. Natural vacation phase execution and physical transitions remain to be observed; configuration validation and reload success do not establish that a future device command will succeed. Existing unavailable-device and presence-lag risks remain. The prior vacation-return handoff handles arrival cleanup.
