# Wine Chart Lazy Disclosure

## Symptom And Purpose

The Wine tab rendered three ApexCharts on first load: 24-hour, 7-day, and
30-day temperature/humidity trends. Those charts are useful but history-heavy,
especially the longer windows. As part of the snappiness and connection
hardening work, the goal was to keep the Wine tab glanceable while avoiding
unnecessary history queries until the user asks for a chart.

## Context Reviewed

- `docs/home-assistant-ui-hardening-runbook.md`
- `docs/audit-history/2026-07-13-recorder-health-gate.md`
- current Wine tab in `dashboards/calm_mobile.yaml`

## Changes Made

- Changed the visible Wine page heading to `Wine cave`.
- Added three YAML helpers:
  - `input_boolean.wine_chart_24h_expanded`
  - `input_boolean.wine_chart_7d_expanded`
  - `input_boolean.wine_chart_30d_expanded`
- Replaced the three always-mounted Wine ApexCharts with full-width summary
  disclosure cards.
- Each summary card shows the relevant average temperature and humidity for its
  horizon.
- Moved each original Apex chart under a matching `conditional` card so it only
  mounts when the corresponding helper is `on`.
- Preserved the existing chart entities, colors, y-axis ranges, grouping
  windows, and dark glass visual language.

## Deployment And Validation

Deployed live on 2026-07-13 through the File Editor ingress deploy path.

Checks:

- Local Ruby YAML parse passed for `configuration.yaml` and
  `dashboards/calm_mobile.yaml`.
- `git diff --check` passed.
- File Editor write/read-back matched for deployed files.
- Home Assistant config check returned `valid` with no errors or warnings.
- `input_boolean.reload`, `template.reload`, `script.reload`, and
  `automation.reload` returned HTTP `200`.
- Live API verification confirmed all three new Wine chart helpers exist and are
  `off`.
- Live API verification confirmed the 24-hour, 7-day, and 30-day Wine average
  sensors returned current values.

## Residual Notes

The local Safari tab was stale-disconnected during visual verification, so the
server-side deploy and API verification were used as the validation source. The
change is designed so collapsed chart cards do not mount ApexCharts on initial
Wine tab load.

Follow-up: if the UI still feels heavy, apply the same disclosure pattern to
popup-level Wine detail charts or other first-load history charts.
