# Bedtime preserves master bathroom lighting

The user clarified that Bedtime glow must not affect the master bathroom.
The October 15 integration had added Main, Vanity and Shower to Bedtime's
explicit off list. Removed only those three targets from `lights_bedtime_scene`.
All off, the dashboard, and existing overnight/away rules retain their behavior.

Reviewed the October 15 audit and deployment runbook. Local and proposed live
YAML parsed successfully; semantic checks confirmed only Bedtime changed and
contains no bathroom targets. Preserved unrelated live/repository differences.

MCP deployment `3b2aec4ae2e546dda4e1a0aa6d98f6b0` passed configuration validation,
verified file writes, and completed script reload. Live read-back matched the
prepared hash. No Core restart or physical scene execution was performed;
verification covers configuration and reload, not a physical bedtime trial.
