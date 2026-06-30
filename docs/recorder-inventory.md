# Recorder Inventory

A recording-focused inventory for Home Assistant Recorder. This sits next to the device inventory, but answers a different question: what state history Home Assistant is saving, how long it is retained, and which classes of entities should prove they need long-term stateful history.

## At A Glance

| Thing | Count |
| --- | --- |
| Configured retention | 30 days |
| Entities reviewed | 2356 |
| Recorder candidates | 1942 |
| Excluded by Recorder config | 20 |
| Disabled in registry | 394 |
| Low stateful-need candidates | 625 |
| Medium stateful-need candidates | 483 |
| High stateful-need candidates | 488 |

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
| integration_config_or_update_state | 377 | 377 | 0 | 0 |  |  |
| derived_summary_or_dashboard_state | 185 | 185 | 0 | 0 |  |  |
| infrastructure_health_diagnostic | 35 | 35 | 0 | 0 |  |  |
| camera_or_event_state | 25 | 25 | 0 | 0 |  |  |
| signal_quality_diagnostic | 3 | 3 | 0 | 0 |  |  |
| event_or_safety_history | 416 | 0 | 0 | 416 |  |  |
| operational_state_history | 412 | 0 | 412 | 0 |  |  |
| uncategorized | 346 | 0 | 0 | 0 |  |  |
| physical_timeseries | 72 | 0 | 0 | 72 |  |  |
| infrastructure_or_camera_misc | 71 | 0 | 71 | 0 |  |  |

## Domain Review

| Domain | Recorder candidates | Low | Medium | High | Unknown | DB rows |
| --- | --- | --- | --- | --- | --- | --- |
| sensor | 481 | 174 | 19 | 206 | 82 |  |
| binary_sensor | 282 | 5 | 49 | 144 | 84 |  |
| switch | 271 | 203 | 0 | 63 | 5 |  |
| automation | 183 | 13 | 170 | 0 | 0 |  |
| script | 144 | 10 | 134 | 0 | 0 |  |
| number | 100 | 100 | 0 | 0 | 0 |  |
| device_tracker | 84 | 0 | 84 | 0 | 0 |  |
| input_datetime | 82 | 5 | 0 | 13 | 64 |  |
| input_boolean | 42 | 2 | 0 | 8 | 32 |  |
| light | 36 | 0 | 3 | 2 | 31 |  |
| select | 32 | 32 | 0 | 0 | 0 |  |
| button | 30 | 30 | 0 | 0 | 0 |  |
| valve | 30 | 0 | 0 | 30 | 0 |  |
| media_player | 24 | 0 | 24 | 0 | 0 |  |
| input_text | 23 | 4 | 0 | 5 | 14 |  |
| input_number | 22 | 0 | 0 | 4 | 18 |  |
| update | 22 | 22 | 0 | 0 | 0 |  |
| event | 15 | 15 | 0 | 0 | 0 |  |
| camera | 10 | 10 | 0 | 0 | 0 |  |
| lock | 4 | 0 | 0 | 4 | 0 |  |
| climate | 3 | 0 | 0 | 3 | 0 |  |
| input_select | 3 | 0 | 0 | 0 | 3 |  |
| remote | 3 | 0 | 0 | 0 | 3 |  |
| tts | 3 | 0 | 0 | 1 | 2 |  |

## High-Impact Entities To Review First

| Entity | Category | Integration | Reason | DB rows | Rows/day | Live attr bytes |
| --- | --- | --- | --- | --- | --- | --- |
| `automation.climate_downstairs_schedule_change_notification` | derived_summary_or_dashboard_state | automation | Derived summary/status data is usually regenerated or shown as current state. |  |  |  |
| `automation.commute_metro_north_first_weekday_departure` | derived_summary_or_dashboard_state | automation | Derived summary/status data is usually regenerated or shown as current state. |  |  |  |
| `automation.commute_reset_metro_north_daily_reminder` | derived_summary_or_dashboard_state | automation | Derived summary/status data is usually regenerated or shown as current state. |  |  |  |
| `automation.inventory_daily_change_digest` | derived_summary_or_dashboard_state | automation | Derived summary/status data is usually regenerated or shown as current state. |  |  |  |
| `automation.irrigation_capture_advanced_schedule_candidate` | derived_summary_or_dashboard_state | automation | Derived summary/status data is usually regenerated or shown as current state. |  |  |  |
| `automation.irrigation_hunter_unscheduled_flow` | derived_summary_or_dashboard_state | automation | Derived summary/status data is usually regenerated or shown as current state. |  |  |  |
| `automation.irrigation_record_alert_history_events` | derived_summary_or_dashboard_state | automation | Derived summary/status data is usually regenerated or shown as current state. |  |  |  |
| `automation.irrigation_scheduled_cycle_did_not_start_watch` | derived_summary_or_dashboard_state | automation | Derived summary/status data is usually regenerated or shown as current state. |  |  |  |
| `automation.lights_door_lights_schedule_sync` | derived_summary_or_dashboard_state | automation | Derived summary/status data is usually regenerated or shown as current state. |  |  |  |
| `automation.lights_foyer_chandelier_schedule_sync` | derived_summary_or_dashboard_state | automation | Derived summary/status data is usually regenerated or shown as current state. |  |  |  |
| `automation.lights_front_stairs_schedule_sync` | derived_summary_or_dashboard_state | automation | Derived summary/status data is usually regenerated or shown as current state. |  |  |  |
| `automation.lights_interior_evening_mode_schedule_sync` | derived_summary_or_dashboard_state | automation | Derived summary/status data is usually regenerated or shown as current state. |  |  |  |
| `automation.notices_ai_notification_action_history` | derived_summary_or_dashboard_state | automation | Derived summary/status data is usually regenerated or shown as current state. |  |  |  |
| `binary_sensor.door_lights_schedule_active` | derived_summary_or_dashboard_state | template | Derived summary/status data is usually regenerated or shown as current state. |  |  |  |
| `binary_sensor.fios_router_wan_status` | derived_summary_or_dashboard_state | upnp | Derived summary/status data is usually regenerated or shown as current state. |  |  |  |
| `binary_sensor.foyer_chandelier_schedule_active` | derived_summary_or_dashboard_state | template | Derived summary/status data is usually regenerated or shown as current state. |  |  |  |
| `binary_sensor.front_stairs_schedule_active` | derived_summary_or_dashboard_state | template | Derived summary/status data is usually regenerated or shown as current state. |  |  |  |
| `binary_sensor.metro_north_commute_card_active` | derived_summary_or_dashboard_state | template | Derived summary/status data is usually regenerated or shown as current state. |  |  |  |
| `button.aqara_hub_m100_identify` | integration_config_or_update_state | matter | Config/update controls rarely need 30-day Recorder history. |  |  |  |
| `button.bonticou_gateway_port_4_power_cycle` | integration_config_or_update_state | unifi | Config/update controls rarely need 30-day Recorder history. |  |  |  |
| `button.bonticou_gateway_restart` | integration_config_or_update_state | unifi | Config/update controls rarely need 30-day Recorder history. |  |  |  |
| `button.casey_s_closet_clear_tamper` | integration_config_or_update_state | unifiprotect | Config/update controls rarely need 30-day Recorder history. |  |  |  |
| `button.dining_room_clear_hold` | integration_config_or_update_state | homekit_controller | Config/update controls rarely need 30-day Recorder history. |  |  |  |
| `button.dining_room_identify` | integration_config_or_update_state | homekit_controller | Config/update controls rarely need 30-day Recorder history. |  |  |  |
| `button.garage_entry_lock_identify` | integration_config_or_update_state | matter | Config/update controls rarely need 30-day Recorder history. |  |  |  |
| `button.master_clear_hold_2` | integration_config_or_update_state | homekit_controller | Config/update controls rarely need 30-day Recorder history. |  |  |  |
| `button.master_identify_2` | integration_config_or_update_state | homekit_controller | Config/update controls rarely need 30-day Recorder history. |  |  |  |
| `button.mudroom_door_lock_identify` | integration_config_or_update_state | matter | Config/update controls rarely need 30-day Recorder history. |  |  |  |
| `button.office_clear_hold` | integration_config_or_update_state | homekit_controller | Config/update controls rarely need 30-day Recorder history. |  |  |  |
| `button.office_identify` | integration_config_or_update_state | homekit_controller | Config/update controls rarely need 30-day Recorder history. |  |  |  |

## Largest Live Attribute Payloads

| Entity | Recommendation | Integration | Live attr bytes | Reason |
| --- | --- | --- | --- | --- |

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
