# Lights layout trial reverted

The user requested a trial of room cards with full-width dimmers. The resulting
room panels were too large and visually heavy; the user explicitly rejected them.
Restored the exact prior live dashboard using its saved pre-trial content and
hash, preserving the Master Bathroom controls and the separate Bedtime fix.

Restoration deployment `02d73f4a9c6f4c1db5b68a15104e6398` passed HA configuration
validation and file verification. MCP read-back matched the pre-trial hash.
No scripts, automation logic, entities, or physical light states were changed by
this layout trial. Repository dashboard restored to its committed version.

Design preference: retain compact room controls. Avoid large enclosing panels,
permanently visible sliders for every off light, and increased vertical spacing.
Any future improvement should be a small visual refinement of one room first.
