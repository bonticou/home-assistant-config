# Wine Trend Disclosure State

Date: 2026-07-20

## Symptom And User Impact

The Wine page's lazy 24-hour, 7-day, and 30-day charts could reopen after a
browser refresh. Their disclosure state lived in restored Home Assistant
`input_boolean` helpers, so an open helper caused the matching ApexChart to
mount and query history during the next page load. The expanded chart also
looked like a separate card rather than content belonging to its disclosure
row.

## Relevant Prior Context

- The July 13 Wine chart lazy-disclosure change correctly placed each chart
  behind a conditional card, but used durable HA helpers for UI-only state.
- The Wine page is intentionally mobile-first and should not perform long-range
  history work until the user explicitly requests it.

## Evidence And Ranked Findings

1. High confidence: restored `input_boolean.wine_chart_*_expanded` states made
   expansion survive refreshes.
2. High confidence: a chart whose helper restored to `on` could mount before
   the user interacted with the refreshed page, undermining the load guard.
3. High confidence: separate button and chart cards created unnecessary visual
   weight and made the open chart feel detached from its control.

## Changes Made

- Added `www/wine-trend-disclosure-card.js`, a purpose-built local disclosure
  component.
- Disclosure state now exists only inside the browser component and resets to
  collapsed whenever the component connects or the page reloads.
- The ApexCharts card element is created only after the user opens a disclosure.
- Closing or disconnecting the disclosure removes the chart element again.
- Replaced the six helper-backed summary/conditional dashboard cards with three
  concise disclosure-card declarations.
- Registered the new card as a cache-versioned Lovelace resource.
- Integrated the chart and header inside one calm surface with a quiet metric
  row, one border, and one disclosure affordance.

## Checks Run

- Ruby YAML parsing passed for `configuration.yaml` and
  `dashboards/calm_mobile.yaml`.
- `node --check www/wine-trend-disclosure-card.js` passed.
- `python3 tools/check_device_inventory_coverage.py` passed.
- `git diff --check` passed.
- File Editor write/read-back hashes matched for:
  - `/homeassistant/configuration.yaml`;
  - `/homeassistant/dashboards/calm_mobile.yaml`;
  - `/homeassistant/www/wine-trend-disclosure-card.js`.
- Home Assistant's live config check returned `valid`.
- The deployed JavaScript module was served successfully from `/local/`.
- The module was added to Home Assistant's live Lovelace resource registry.
- A full Safari/Nabu Wine-page refresh confirmed:
  - the custom element was registered;
  - all three disclosures rendered collapsed;
  - zero ApexCharts were mounted while collapsed;
  - zero configuration-error cards remained.
- A live interaction check confirmed opening one disclosure mounted exactly one
  ApexChart and closing it removed the chart again.

## Deployment Status

Deployed live on 2026-07-20 through the authenticated Nabu Casa File Editor
ingress. Home Assistant Core was restarted with user approval so the updated
configuration was loaded. Because this instance exposes no Lovelace reload
service and uses the live Lovelace resource registry, the custom module was
also added to that registry before the final browser validation.

## Residual Risks And Next Follow-Ups

- The former expansion helpers remain defined but unused for compatibility and
  can be removed in a later cleanup after live validation.
- Nabu Casa briefly returned TLS connection errors during the Core restart
  window, then the authenticated API and dashboard recovered.
