# Dashboard Chart Audit

Use this playbook when editing Home Assistant dashboard charts, especially
`custom:apexcharts-card` charts in `dashboards/calm_mobile.yaml`.

The main lesson: do not assume a repo YAML edit reached the phone. If the UI
looks unchanged, first prove whether Home Assistant is serving the updated
dashboard config before debugging chart math.

## Fast Checklist

1. Identify the chart block in `dashboards/calm_mobile.yaml`.
2. Confirm the dashboard source in `configuration.yaml`.
3. Validate YAML after any edit.
4. Static-scan the edited chart for old bounds, old grouping, or stale options.
5. If the live UI still looks unchanged, compare the live Lovelace config with
   the repo YAML before changing chart values again.
6. Pull real sensor history for the chart window and compare raw min/max against
   grouped min/max.
7. Render-test the dashboard when possible. If rendering is blocked, record that
   limitation in the audit result.
8. Document the final reload, deploy, or cache action that made the UI change.

## Source Verification

For YAML dashboards, start with `configuration.yaml` and confirm the dashboard
entry points at the expected file. For the calm mobile dashboard, the expected
source is:

- dashboard URL path: `/calm-mobile`
- dashboard file: `dashboards/calm_mobile.yaml`

If the phone still shows old labels, old axis ranges, or old chart behavior
after a repo edit, classify the issue as one of these before making another
chart patch:

- **Source/deploy issue:** Home Assistant is serving an older copy than the repo.
- **Frontend cache issue:** Home Assistant serves the new config, but the app or
  browser is still displaying an old frontend payload.
- **Chart/data issue:** The live config is current, but the real data or chart
  options still render poorly.

Only debug chart ranges after the live config is confirmed current.

## ApexCharts Guidance

Prefer soft bounds for calm guardrails that may expand to include real data:

```yaml
yaxis:
  - id: temp
    min: "~50"
    max: "~62"
```

Use fixed numeric bounds only when clipping outside that range is intentional.
For operational telemetry, clipped lines usually hide the fact the user needs to
see.

For grouped time-series charts:

```yaml
group_by:
  func: avg
  duration: 2h
  fill: last
```

Use `fill: last` when recorder gaps create dropouts or zero-like vertical dives.
Document the bucket duration next to the chart window in the audit notes.

Use straight interpolation when smooth curves visually overshoot the data:

```yaml
apex_config:
  stroke:
    curve: straight
```

This is especially useful for small mobile charts where sharp sensor changes can
look like they leave the plot area.

## History Audit

For each chart, compare both raw and grouped data:

- raw min/max for the chart window
- non-numeric, `unknown`, and `unavailable` counts
- zero-like values
- clearly impossible extremes for the sensor domain
- grouped min/max using the chart's configured bucket duration
- configured y-axis bounds after soft-bound expansion is considered

The grouped min/max should fit inside the rendered axis domain. If raw data has
meaningful excursions, show them with more axis room instead of hiding them. If
raw data has bad dropouts, filter or fill only the invalid points and document
why they are invalid.

## Render Audit

When possible, open the live dashboard at a mobile-sized viewport and inspect:

- rendered y-axis labels
- chart SVG path bounds versus the plot area
- visible line clipping at the top, bottom, or card edge
- whether the rendered axis labels match the current repo/live config

If browser rendering cannot be completed because the authenticated frontend is
blocked, redirected, or unavailable, say that directly in the final audit. Do
not claim a rendered pass from config-only evidence.

## Audit Report Template

```text
Chart:
Dashboard path:
Repo config bounds:
Live config bounds:
Window and group bucket:
Raw min/max:
Grouped min/max:
Bad data counts:
Rendered axis labels:
SVG/render pass:
Reload or deploy action:
Result:
```

## Safe Defaults

- Keep chart changes scoped to the affected dashboard section.
- Prefer readable YAML over clever dynamic behavior.
- Do not edit `.storage` unless the dashboard is proven to be UI-managed.
- Do not record secrets, hostnames, auth tokens, or temporary one-off scripts in
  audit notes or committed docs.
