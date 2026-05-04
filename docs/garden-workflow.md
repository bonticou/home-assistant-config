# Garden workflow

This garden setup is intentionally rule-driven. The dashboard should mostly
display the workflow state; the durable logic lives in Home Assistant template
entities, automations, and scripts.

## Source of truth

- Live forecast source: `weather.forecast_home`
- Forecast rollup: `sensor.garden_weather_window`
- Main action: `sensor.garden_next_action`
- Workflow summary: `sensor.garden_workflow_status`
- Attention binary: `binary_sensor.garden_needs_attention`
- Compatibility binary: `binary_sensor.garden_actionable_alert`

Climate normals are context only. They should explain seasonal pressure, not
override the live forecast.

## Attention model

`binary_sensor.garden_needs_attention` turns on when any of these are true:

- A crop is ready to plant under the live weather rules.
- Outdoor starts need weather protection.
- A crop observation is marked `stressed`.

Planting readiness is intentionally treated as "needs attention", not passive
dashboard information. If a crop is ready to plant, it should appear in House
Notices and be eligible for a push notification.

`sensor.garden_workflow_status` explains why attention is needed through:

- `attention_type`
- `attention_reason`
- `ready_to_plant`
- `notification_policy`

Dashboards and notices should read these attributes instead of re-creating
their own attention logic.

## Dashboard action design

Garden controls should be explicit and local to the crop or notice they affect.
Avoid loose action chips at the bottom of the page. If a durable helper already
models a manual state, prefer a clean select/dropdown card over a cryptic chip.

Forecast chips are useful only when they are readable at a glance. Spell out
crop groups such as "Tomatoes & cape" and "Peppers & squash"; avoid shorthand
labels like "Tom/Cape" or "Pep/Squash". Notification controls such as snooze
and push toggles should live in the notification center or a clearly labeled
settings surface, not beside crop-care status chips.

Garden notification details should be calm workflow explainers, not stock HA
entity popups. A planting or protection reminder detail should state what the
garden is asking for, why the live forecast or crop state triggered it, what the
primary action will record, and what notifications/rules change afterward. For
forecast-driven details, include the relevant lows, threshold, and crop group;
for care history, use a short designed timeline instead of the raw HA activity
view. Project-wide rules live in `docs/notification-detail-surfaces.md`.

## Weather rules

`sensor.garden_weather_window` looks at the next 4 daily forecast lows.

- If fewer than 4 lows are available, planting-window notifications stay quiet.
- Bok choy can be planted unless a hard frost is forecast.
- Tomatoes and cape gooseberry need 4 forecast lows at or above 50 deg F.
- Peppers need 4 forecast lows at or above 55 deg F.
- Honeynut squash needs 4 forecast lows at or above 55 deg F and no cold/wet
  pattern.

Protection alerts use the same thresholds after crops are outdoors or planted.

## Notification rules

Garden pushes should stay quiet and actionable:

- Planting windows notify when the window opens or at the morning check, at most
  once per day.
- Weather protection notifies in late afternoon, at most once per day.
- Stressed crops notify immediately or at the daily issue check.
- `dry` is dashboard-only. Only `stressed` creates an issue push.
- Snooze suppresses garden pushes until
  `input_datetime.garden_notifications_snooze_until`.

## Current crop groups

- Spinach: planted group; dashboard care only unless marked `stressed`.
- Bok choy: cool-season start group; ready unless hard frost is forecast.
- Tomatoes: warm start group; 50 deg F threshold after hardening.
- Cape gooseberry: warm container crop; follows tomato threshold.
- Peppers: warm start group; 55 deg F threshold after hardening.
- Honeynut squash: warm, weather-sensitive start group; 55 deg F threshold and
  no wet pattern.

## Adding a new crop group

For each new garden item, add or update the workflow in this order:

1. Add helper state if the item needs durable manual state.
   Typical helpers are an `input_select` for stage, an `input_select` for
   observation, and optional planted/hardening timestamps.
2. Add a crop status sensor with count, varieties, target location, threshold,
   and `stage_note`.
3. Add forecast-window logic if the crop has a distinct threshold or weather
   sensitivity.
4. Add the crop to `sensor.garden_next_action` and its `action_id` attribute if
   it can become ready to plant or needs issue resolution.
5. Add it to `binary_sensor.garden_stage_action_due`,
   `binary_sensor.garden_weather_protection_due`, and
   `binary_sensor.garden_issue_attention_due` as applicable.
6. Add scripts for safe one-tap actions, such as mark planted, mark hardened, or
   issue resolved.
7. Add notification action handling in the mobile action automation.
8. Add a calm dashboard card that displays the rule outcome, not raw helper
   controls.
9. Run YAML checks, `git diff --check`, and Home Assistant config validation
   before restart.

Avoid adding one card per plant. Group by meaningful care rules: cool-season
greens, warm fruiting crops, containers, vines, herbs, or whatever rule boundary
actually changes the care.
