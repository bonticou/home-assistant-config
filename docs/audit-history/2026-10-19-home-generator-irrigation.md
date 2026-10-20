# Home generator and irrigation status

User requested a compact Generator pill beneath Wine Cave, with Irrigation to
its right, and reported that irrigation is winterized.

- Added both pills using the existing compact tile styling; removed the old
  icon-only irrigation chip.
- Generator details show reported status and battery voltage, with Mobile Link
  access. Connection failures are shown as monitoring unavailable.
- Added a restored irrigation season selector, initially Winterized, with a
  labeled control on the Irrigation page for spring startup. This records the
  user's seasonal status; it does not alter Hydrawise schedules or safety rules.
- Preserved unrelated live/repository differences using fresh live candidates.

Validation: local YAML parsing, inventory coverage, diff checks, and live HA
configuration validation passed. MCP deployment applied and verified both files;
Input selects were reloaded without restarting Core. Browser verification showed
Generator Ready beneath Wine Cave, Irrigation Winterized beside it, working
generator details with 14.1 V reported battery voltage, and the Winterized season
selector on the Irrigation page.

Limits: generator data reflects Mobile Link reporting, not independent transfer
or utility-power sensing. Seasonal status must be updated after spring startup.
