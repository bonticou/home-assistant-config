# Recorder Inventory

A recording-focused inventory for Home Assistant Recorder. This sits next to the device inventory, but answers a different question: what state history Home Assistant is saving, how long it is retained, and which classes of entities should prove they need long-term stateful history.

## At A Glance

| Thing | Count |
| --- | --- |
| Configured retention | 30 days |
| Entities reviewed | 2345 |
| Recorder candidates | 1944 |
| Excluded by Recorder config | 21 |
| Disabled in registry | 380 |
| Low stateful-need candidates | 627 |
| Medium stateful-need candidates | 507 |
| High stateful-need candidates | 449 |

## Data Quality

- Exact per-entity row counts are not included in this run.
- Frequency should be treated as pending until the tool is run against a `home-assistant_v2.db` copy.
- Live attr sizes and live recency are useful triage signals, not a substitute for SQLite row counts.

## Current Recorder Config

| Setting | Value |
| --- | --- |
| purge_keep_days | 30 |
| excluded domains | (none) |
| excluded entity globs | sensor.*_signal_strength, sensor.*_rssi, sensor.*_lqi, sensor.*_linkquality |
| excluded entities | sun.sun, weather.forecast_home |

## Largest Low-Stateful-Need Review Sets

| Category | Entities | Low | Medium | High | DB rows | Live attr bytes |
| --- | --- | --- | --- | --- | --- | --- |
| integration_config_or_update_state | 364 | 364 | 0 | 0 |  | 39554 |
| derived_summary_or_dashboard_state | 196 | 196 | 0 | 0 |  | 96742 |
| infrastructure_health_diagnostic | 41 | 41 | 0 | 0 |  | 7037 |
| camera_or_event_state | 23 | 23 | 0 | 0 |  | 7886 |
| signal_quality_diagnostic | 3 | 3 | 0 | 0 |  | 356 |
| operational_state_history | 439 | 0 | 439 | 0 |  | 68177 |
| event_or_safety_history | 390 | 0 | 0 | 390 |  | 48641 |
| uncategorized | 361 | 0 | 0 | 0 |  | 47771 |
| infrastructure_or_camera_misc | 68 | 0 | 68 | 0 |  | 7770 |
| physical_timeseries | 59 | 0 | 0 | 59 |  | 7587 |

## Domain Review

| Domain | Recorder candidates | Low | Medium | High | Unknown | DB rows |
| --- | --- | --- | --- | --- | --- | --- |
| sensor | 444 | 189 | 19 | 165 | 71 |  |
| binary_sensor | 281 | 4 | 46 | 149 | 82 |  |
| switch | 265 | 201 | 0 | 58 | 6 |  |
| automation | 176 | 13 | 163 | 0 | 0 |  |
| script | 156 | 9 | 147 | 0 | 0 |  |
| device_tracker | 107 | 0 | 107 | 0 | 0 |  |
| number | 94 | 94 | 0 | 0 | 0 |  |
| input_datetime | 92 | 4 | 0 | 15 | 73 |  |
| input_boolean | 58 | 2 | 0 | 9 | 47 |  |
| light | 35 | 0 | 3 | 2 | 30 |  |
| select | 33 | 33 | 0 | 0 | 0 |  |
| button | 31 | 31 | 0 | 0 | 0 |  |
| valve | 27 | 0 | 0 | 27 | 0 |  |
| media_player | 22 | 0 | 22 | 0 | 0 |  |
| update | 22 | 22 | 0 | 0 | 0 |  |
| input_number | 18 | 0 | 0 | 4 | 14 |  |
| input_select | 16 | 0 | 0 | 0 | 16 |  |
| input_text | 16 | 2 | 0 | 5 | 9 |  |
| event | 13 | 13 | 0 | 0 | 0 |  |
| camera | 10 | 10 | 0 | 0 | 0 |  |
| lock | 4 | 0 | 0 | 4 | 0 |  |
| climate | 3 | 0 | 0 | 3 | 0 |  |
| conversation | 3 | 0 | 0 | 1 | 2 |  |
| remote | 3 | 0 | 0 | 0 | 3 |  |

## High-Impact Entities To Review First

| Entity | Category | Integration | Reason | DB rows | Rows/day | Live attr bytes |
| --- | --- | --- | --- | --- | --- | --- |
| `sensor.house_notice_timeline` | derived_summary_or_dashboard_state | template | Derived summary/status data is usually regenerated or shown as current state. |  |  | 16133 |
| `sensor.device_inventory_pending_digest` | derived_summary_or_dashboard_state | command_line | Derived summary/status data is usually regenerated or shown as current state. |  |  | 14828 |
| `sensor.garbage_recycling_schedule` | derived_summary_or_dashboard_state | template | Derived summary/status data is usually regenerated or shown as current state. |  |  | 7701 |
| `sensor.irrigation_schedule_summary` | derived_summary_or_dashboard_state | template | Derived summary/status data is usually regenerated or shown as current state. |  |  | 7077 |
| `sensor.house_notice_history` | derived_summary_or_dashboard_state | template | Derived summary/status data is usually regenerated or shown as current state. |  |  | 6547 |
| `sensor.wine_collection_snapshot` | derived_summary_or_dashboard_state | command_line | Derived summary/status data is usually regenerated or shown as current state. |  |  | 4789 |
| `sensor.irrigation_history_status` | derived_summary_or_dashboard_state | command_line | Derived summary/status data is usually regenerated or shown as current state. |  |  | 2977 |
| `sensor.metro_north_nwp_to_grand_central` | derived_summary_or_dashboard_state | command_line | Derived summary/status data is usually regenerated or shown as current state. |  |  | 1697 |
| `event.garage_vehicle` | camera_or_event_state | unifiprotect | Camera/event entity state is often high churn; keep only if specific automations need history. |  |  | 1070 |
| `sensor.environment_source_map` | derived_summary_or_dashboard_state | template | Derived summary/status data is usually regenerated or shown as current state. |  |  | 827 |
| `sensor.irrigation_zone_attention_summary` | derived_summary_or_dashboard_state | template | Derived summary/status data is usually regenerated or shown as current state. |  |  | 816 |
| `sensor.wine_cave_appliance_context` | derived_summary_or_dashboard_state | template | Derived summary/status data is usually regenerated or shown as current state. |  |  | 743 |
| `sensor.garden_weather_window` | derived_summary_or_dashboard_state | template | Derived summary/status data is usually regenerated or shown as current state. |  |  | 656 |
| `sensor.irrigation_weather_skip_context` | derived_summary_or_dashboard_state | template | Derived summary/status data is usually regenerated or shown as current state. |  |  | 620 |
| `sensor.environment_dining_room_status` | derived_summary_or_dashboard_state | template | Derived summary/status data is usually regenerated or shown as current state. |  |  | 615 |
| `sensor.ting_notification_status` | derived_summary_or_dashboard_state | template | Derived summary/status data is usually regenerated or shown as current state. |  |  | 613 |
| `sensor.device_inventory_status` | derived_summary_or_dashboard_state | command_line | Derived summary/status data is usually regenerated or shown as current state. |  |  | 591 |
| `sensor.home_assistant_remote_access_status` | derived_summary_or_dashboard_state | template | Derived summary/status data is usually regenerated or shown as current state. |  |  | 577 |
| `sensor.away_security_entry_point_issues` | derived_summary_or_dashboard_state | template | Template/command-line dashboard sensors should prove they need long raw Recorder history. |  |  | 568 |
| `sensor.irrigation_dashboard_status` | derived_summary_or_dashboard_state | template | Derived summary/status data is usually regenerated or shown as current state. |  |  | 567 |
| `sensor.house_low_battery_summary` | derived_summary_or_dashboard_state | template | Derived summary/status data is usually regenerated or shown as current state. |  |  | 557 |
| `sensor.espresso_maintenance_status` | derived_summary_or_dashboard_state | template | Derived summary/status data is usually regenerated or shown as current state. |  |  | 522 |
| `sensor.environment_basement_status` | derived_summary_or_dashboard_state | template | Derived summary/status data is usually regenerated or shown as current state. |  |  | 518 |
| `sensor.garden_workflow_status` | derived_summary_or_dashboard_state | template | Derived summary/status data is usually regenerated or shown as current state. |  |  | 510 |
| `update.home_assistant_operating_system_update` | integration_config_or_update_state | hassio | Config/update controls rarely need 30-day Recorder history. |  |  | 477 |
| `camera.mechanical_room_high_resolution_channel` | camera_or_event_state | unifiprotect | Camera/event entity state is often high churn; keep only if specific automations need history. |  |  | 469 |
| `sensor.garbage_recycling_next_pickup` | derived_summary_or_dashboard_state | template | Template/command-line dashboard sensors should prove they need long raw Recorder history. |  |  | 466 |
| `update.home_assistant_supervisor_update` | integration_config_or_update_state | hassio | Config/update controls rarely need 30-day Recorder history. |  |  | 465 |
| `camera.g6_instant_high_resolution_channel_2` | camera_or_event_state | unifiprotect | Camera/event entity state is often high churn; keep only if specific automations need history. |  |  | 461 |
| `camera.wynn_s_room_high_resolution_channel` | camera_or_event_state | unifiprotect | Camera/event entity state is often high churn; keep only if specific automations need history. |  |  | 461 |

## Largest Live Attribute Payloads

| Entity | Recommendation | Integration | Live attr bytes | Reason |
| --- | --- | --- | --- | --- |
| `sensor.house_notice_timeline` | review_current_only | template | 16133 | Derived summary/status data is usually regenerated or shown as current state. |
| `sensor.device_inventory_pending_digest` | review_current_only | command_line | 14828 | Derived summary/status data is usually regenerated or shown as current state. |
| `sensor.garbage_recycling_schedule` | review_current_only | template | 7701 | Derived summary/status data is usually regenerated or shown as current state. |
| `sensor.irrigation_schedule_summary` | review_current_only | template | 7077 | Derived summary/status data is usually regenerated or shown as current state. |
| `sensor.house_notice_history` | review_current_only | template | 6547 | Derived summary/status data is usually regenerated or shown as current state. |
| `sensor.wine_collection_snapshot` | review_current_only | command_line | 4789 | Derived summary/status data is usually regenerated or shown as current state. |
| `sensor.irrigation_history_status` | review_current_only | command_line | 2977 | Derived summary/status data is usually regenerated or shown as current state. |
| `sensor.metro_north_nwp_to_grand_central` | review_current_only | command_line | 1697 | Derived summary/status data is usually regenerated or shown as current state. |
| `event.garage_vehicle` | review_short_or_current_only | unifiprotect | 1070 | Camera/event entity state is often high churn; keep only if specific automations need history. |
| `binary_sensor.away_security_garage_door_open` | keep | template | 904 | Motion, presence, doors, valves, safety, and security history can support alerts and incident review. |
| `media_player.great_room_speakers` | review_selectively | sonos | 847 | Useful for diagnostics, but not every automation/script/device tracker needs long raw state history. |
| `media_player.wynn_s_room` | review_selectively | sonos | 833 | Useful for diagnostics, but not every automation/script/device tracker needs long raw state history. |
| `media_player.unnamed_room_2` | review_selectively | sonos | 832 | Useful for diagnostics, but not every automation/script/device tracker needs long raw state history. |
| `sensor.environment_source_map` | review_current_only | template | 827 | Derived summary/status data is usually regenerated or shown as current state. |
| `sensor.irrigation_zone_attention_summary` | review_current_only | template | 816 | Derived summary/status data is usually regenerated or shown as current state. |
| `sensor.wine_cave_appliance_context` | review_current_only | template | 743 | Derived summary/status data is usually regenerated or shown as current state. |
| `sensor.garden_weather_window` | review_current_only | template | 656 | Derived summary/status data is usually regenerated or shown as current state. |
| `sensor.irrigation_weather_skip_context` | review_current_only | template | 620 | Derived summary/status data is usually regenerated or shown as current state. |
| `sensor.environment_dining_room_status` | review_current_only | template | 615 | Derived summary/status data is usually regenerated or shown as current state. |
| `sensor.ting_notification_status` | review_current_only | template | 613 | Derived summary/status data is usually regenerated or shown as current state. |
| `sensor.device_inventory_status` | review_current_only | command_line | 591 | Derived summary/status data is usually regenerated or shown as current state. |
| `sensor.home_assistant_remote_access_status` | review_current_only | template | 577 | Derived summary/status data is usually regenerated or shown as current state. |
| `sensor.away_security_entry_point_issues` | review_current_only | template | 568 | Template/command-line dashboard sensors should prove they need long raw Recorder history. |
| `sensor.irrigation_dashboard_status` | review_current_only | template | 567 | Derived summary/status data is usually regenerated or shown as current state. |
| `media_player.family_room_tv_2` | review_selectively | apple_tv | 563 | Useful for diagnostics, but not every automation/script/device tracker needs long raw state history. |

## Use

Regenerate after Recorder config changes, major integration additions, or storage incidents:

```bash
python3 tools/generate_recorder_inventory.py
```

For exact frequency and largest historical writers, run against a copied Recorder DB:

```bash
python3 tools/generate_recorder_inventory.py --db /path/to/home-assistant_v2.db
```

Do not use this inventory as an automatic exclusion list. Treat it as the audit map for deciding what should be kept, shortened, or made current-only.
