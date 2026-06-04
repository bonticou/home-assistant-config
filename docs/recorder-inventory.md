# Recorder Inventory

A recording-focused inventory for Home Assistant Recorder. This sits next to the device inventory, but answers a different question: what state history Home Assistant is saving, how long it is retained, and which classes of entities should prove they need long-term stateful history.

## At A Glance

| Thing | Count |
| --- | --- |
| Configured retention | 30 days |
| Entities reviewed | 2195 |
| Recorder candidates | 1794 |
| Excluded by Recorder config | 21 |
| Disabled in registry | 380 |
| Low stateful-need candidates | 594 |
| Medium stateful-need candidates | 472 |
| High stateful-need candidates | 429 |

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
| integration_config_or_update_state | 365 | 365 | 0 | 0 |  |  |
| derived_summary_or_dashboard_state | 168 | 168 | 0 | 0 |  |  |
| infrastructure_health_diagnostic | 35 | 35 | 0 | 0 |  |  |
| camera_or_event_state | 23 | 23 | 0 | 0 |  |  |
| signal_quality_diagnostic | 3 | 3 | 0 | 0 |  |  |
| operational_state_history | 402 | 0 | 402 | 0 |  |  |
| event_or_safety_history | 366 | 0 | 0 | 366 |  |  |
| uncategorized | 299 | 0 | 0 | 0 |  |  |
| infrastructure_or_camera_misc | 70 | 0 | 70 | 0 |  |  |
| physical_timeseries | 63 | 0 | 0 | 63 |  |  |

## Domain Review

| Domain | Recorder candidates | Low | Medium | High | Unknown | DB rows |
| --- | --- | --- | --- | --- | --- | --- |
| sensor | 413 | 163 | 19 | 162 | 69 |  |
| binary_sensor | 266 | 4 | 48 | 137 | 77 |  |
| switch | 259 | 199 | 0 | 57 | 3 |  |
| automation | 164 | 12 | 152 | 0 | 0 |  |
| script | 130 | 9 | 121 | 0 | 0 |  |
| device_tracker | 107 | 0 | 107 | 0 | 0 |  |
| number | 93 | 93 | 0 | 0 | 0 |  |
| input_datetime | 69 | 4 | 0 | 13 | 52 |  |
| input_boolean | 39 | 2 | 0 | 7 | 30 |  |
| light | 35 | 0 | 3 | 2 | 30 |  |
| select | 31 | 31 | 0 | 0 | 0 |  |
| button | 30 | 30 | 0 | 0 | 0 |  |
| valve | 27 | 0 | 0 | 27 | 0 |  |
| media_player | 22 | 0 | 22 | 0 | 0 |  |
| update | 22 | 22 | 0 | 0 | 0 |  |
| input_number | 18 | 0 | 0 | 4 | 14 |  |
| input_text | 15 | 2 | 0 | 5 | 8 |  |
| event | 13 | 13 | 0 | 0 | 0 |  |
| camera | 10 | 10 | 0 | 0 | 0 |  |
| lock | 4 | 0 | 0 | 4 | 0 |  |
| climate | 3 | 0 | 0 | 3 | 0 |  |
| conversation | 3 | 0 | 0 | 1 | 2 |  |
| input_select | 3 | 0 | 0 | 0 | 3 |  |
| remote | 3 | 0 | 0 | 0 | 3 |  |

## High-Impact Entities To Review First

| Entity | Category | Integration | Reason | DB rows | Rows/day | Live attr bytes |
| --- | --- | --- | --- | --- | --- | --- |
| `automation.climate_downstairs_schedule_change_notification` | derived_summary_or_dashboard_state | automation | Derived summary/status data is usually regenerated or shown as current state. |  |  |  |
| `automation.commute_metro_north_first_weekday_departure` | derived_summary_or_dashboard_state | automation | Derived summary/status data is usually regenerated or shown as current state. |  |  |  |
| `automation.commute_reset_metro_north_daily_reminder` | derived_summary_or_dashboard_state | automation | Derived summary/status data is usually regenerated or shown as current state. |  |  |  |
| `automation.inventory_daily_change_digest` | derived_summary_or_dashboard_state | automation | Derived summary/status data is usually regenerated or shown as current state. |  |  |  |
| `automation.irrigation_capture_advanced_schedule_candidate` | derived_summary_or_dashboard_state | automation | Derived summary/status data is usually regenerated or shown as current state. |  |  |  |
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
| `button.ratgdo32_4536e8_query_status` | derived_summary_or_dashboard_state | esphome | Derived summary/status data is usually regenerated or shown as current state. |  |  |  |
| `button.ratgdo32_4536e8_restart` | integration_config_or_update_state | esphome | Config/update controls rarely need 30-day Recorder history. |  |  |  |

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
