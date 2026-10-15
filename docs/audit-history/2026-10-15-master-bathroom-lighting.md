# Master bathroom lighting — October 15, 2026

## Request and evidence

Add bathroom lighting to Lights and existing house lighting rules. Reviewed the
August 26 evening-scene and August 30 lighting reliability incidents, notification
patterns, and MCP deployment runbook before changing configuration.

High-confidence finding: three Lutron Diva dimmers were already discovered but
were disabled under retired replacement entity IDs and assigned to former rooms.
Enabled them through HA device settings, assigned Master Bathroom, and renamed
them to `light.master_bathroom_main_lights`, `light.master_bathroom_vanity_lights`,
and `light.master_bathroom_shower_lights`. Native MCP confirmed all three available.
The chandelier device is a Pico remote, not a controllable light output. Enabling
the dimmers was sufficient; no separate integration reload or Core restart needed.

## Changes

- Added a grouped Master Bathroom section with Main, Vanity, Shower dimming cards.
  A vertical stack keeps the heading with its controls in desktop masonry.
- Added all three dimmers to All off and Bedtime, preserving transition durations.
- Live away and overnight sensors dynamically enumerate individual lights, so
  these dimmers already participate in existing alerts and overnight sweep rules.
  No new notification automations, durable guards, or Recorder assumptions added.
- Evening/TV retain their common-room scope; bathroom task lights stay manual-on.
- Reconciled only these three devices in the inventory, preserving older snapshot
  context. Targeted pseudonyms use entity names and contain no raw registry IDs.

## Validation and deployment

Local YAML parsing passed. Semantic comparisons confirmed only the two intended
scripts and Lights view changed, and affected live/repository content agrees.
Inventory coverage passed for 177 active control references. Live formatting and
unrelated repository/live drift were preserved with focused patches.

MCP deployment `74e337496d504ef097eef53d40eac529` applied scripts and dashboard;
config validation passed and script reload completed. Dashboard grouping refinement
`47e9e8a16605468d83b3735e623a7c9e` passed config validation without another reload.
File hashes were verified by the deployment helper, with initial deployment also
read back through MCP. Browser rendered all three controls with live state.

## Residual limits

No physical lights or whole-house scenes were triggered for testing. Vanity was
already on at full brightness; Main and Shower were off. Natural overnight/away
notification delivery remains to be observed. Pico buttons remain unchanged.
