# Compact Lights room layout

The user clarified that rejecting the oversized room-card trial meant improve
the design, not stop at restoration. Continued from the restored layout with a
lighter, compact revision. Read the earlier trial record and retained its lessons.

## Changes

- Keep each room title and its controls in a vertical stack so masonry cannot
  detach the heading from the lights. Retain two-column control grids.
- Use smaller room headings, quieter borders, subtle warm on-state backgrounds,
  and no additional enclosing room panels or decorative shadows.
- Put light names and state/brightness on one line; keep sliders collapsed for
  off lights. Preserve existing group controls and individual control actions.
- Keep Scenes, schedules, overrides, other dashboard views, and lighting logic
  unchanged, including the master bathroom Bedtime exemption.

## Validation and deployment

Both repository and proposed live YAML parsed. Semantic checks confirmed all
control targets, tap/hold/double-tap actions, dimmer visibility settings, and other
views were preserved. Inventory coverage passed (177 active control references).
Live/repository differences outside the room section were preserved.

MCP deployments `58097c65b8ad4764854a96c801fe55dd` and
`6a3930592f6145dbb4deb383100ff1d7` passed configuration checks and file verification.
No reload or Core restart required. Safari visual review confirmed compact
single-line labels, on-state dimmers, and coherent upper/lower room groups,
including Master Bathroom. No physical lights were operated to test the layout.
Phone-specific visual review remains unperformed.
