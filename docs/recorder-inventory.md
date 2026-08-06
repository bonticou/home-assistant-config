# Recorder Inventory

A recording-focused inventory for Home Assistant Recorder. This sits next to the device inventory, but answers a different question: what state history Home Assistant is saving, how long it is retained, and which classes of entities should prove they need long-term stateful history.

## At A Glance

| Thing | Count |
| --- | --- |
| Configured retention | 30 days |
| Entities reviewed | 2512 |
| Recorder candidates | 1698 |
| Excluded by Recorder config | 446 |
| Disabled in registry | 368 |
| Low stateful-need candidates | 304 |
| Medium stateful-need candidates | 504 |
| High stateful-need candidates | 506 |

## Data Quality

- Exact per-entity row counts are not included in this run.
- Frequency should be treated as pending until the tool is run against a `home-assistant_v2.db` copy.
- Live attr sizes and live recency are useful triage signals, not a substitute for SQLite row counts.

## Current Recorder Config

| Setting | Value |
| --- | --- |
| purge_keep_days | 30 |
| excluded domains | button, camera, number, select, update |
| excluded entity globs | sensor.*_signal_strength, sensor.*_rssi, sensor.*_lqi, sensor.*_linkquality, switch.*_analytics_enabled, switch.*_animal_detection, switch.*_baby_cry_detection, switch.*_car_alarm_detection, switch.*_car_horn_detection, switch.*_co_alarm_detection, switch.*_crossfade, switch.*_glass_break_detection, switch.*_humidity_sensor, switch.*_insights_enabled, switch.*_license_plate_detection, switch.*_light_sensor, switch.*_loudness, switch.*_night_sound, switch.*_none, switch.*_overlay_show_*, switch.*_person_detection, switch.*_privacy_mode, switch.*_siren_detection, switch.*_smoke_detection, switch.*_speaking_detection, switch.*_speech_enhancement, switch.*_status_light*, switch.*_subwoofer_enabled, switch.*_surround_enabled, switch.*_surround_music_full_volume, switch.*_system_sounds, switch.*_temperature_sensor, switch.*_vehicle_detection |
| excluded entities | sun.sun, weather.forecast_home, switch.g6_instant_motion, switch.g6_instant_motion_2, switch.g6_instant_motion_3, switch.mechanical_room_motion, switch.mud_room_motion, switch.wynn_s_room_motion, sensor.bonticou_gateway_cpu_utilization_2, sensor.bonticou_gateway_memory_utilization_2, sensor.device_inventory_pending_digest, sensor.device_inventory_status, sensor.garbage_recycling_schedule, sensor.house_notice_timeline, sensor.irrigation_7_day_ledger, sensor.irrigation_flow_baseline_status, sensor.irrigation_history_status, sensor.irrigation_schedule_summary, sensor.metro_north_nwp_to_grand_central, sensor.ting_notification_status, sensor.wine_collection_snapshot |

## Largest Low-Stateful-Need Review Sets

| Category | Entities | Low | Medium | High | DB rows | Live attr bytes |
| --- | --- | --- | --- | --- | --- | --- |
| derived_summary_or_dashboard_state | 168 | 168 | 0 | 0 |  |  |
| integration_config_or_update_state | 80 | 80 | 0 | 0 |  |  |
| infrastructure_health_diagnostic | 34 | 34 | 0 | 0 |  |  |
| camera_or_event_state | 17 | 17 | 0 | 0 |  |  |
| signal_quality_diagnostic | 5 | 5 | 0 | 0 |  |  |
| operational_state_history | 432 | 0 | 432 | 0 |  |  |
| event_or_safety_history | 417 | 0 | 0 | 417 |  |  |
| uncategorized | 384 | 0 | 0 | 0 |  |  |
| physical_timeseries | 89 | 0 | 0 | 89 |  |  |
| infrastructure_or_camera_misc | 72 | 0 | 72 | 0 |  |  |

## Domain Review

| Domain | Recorder candidates | Low | Medium | High | Unknown | DB rows |
| --- | --- | --- | --- | --- | --- | --- |
| sensor | 495 | 166 | 20 | 220 | 89 |  |
| binary_sensor | 294 | 5 | 49 | 147 | 93 |  |
| automation | 189 | 14 | 175 | 0 | 0 |  |
| switch | 152 | 81 | 0 | 63 | 8 |  |
| script | 151 | 10 | 141 | 0 | 0 |  |
| input_datetime | 90 | 5 | 0 | 13 | 72 |  |
| device_tracker | 89 | 0 | 89 | 0 | 0 |  |
| input_boolean | 46 | 2 | 0 | 8 | 36 |  |
| light | 36 | 0 | 3 | 2 | 31 |  |
| valve | 30 | 0 | 0 | 30 | 0 |  |
| input_text | 28 | 4 | 0 | 5 | 19 |  |
| media_player | 27 | 0 | 27 | 0 | 0 |  |
| input_number | 22 | 0 | 0 | 4 | 18 |  |
| event | 17 | 17 | 0 | 0 | 0 |  |
| lock | 4 | 0 | 0 | 4 | 0 |  |
| climate | 3 | 0 | 0 | 3 | 0 |  |
| input_select | 3 | 0 | 0 | 0 | 3 |  |
| remote | 3 | 0 | 0 | 0 | 3 |  |
| tts | 3 | 0 | 0 | 1 | 2 |  |
| ai_task | 2 | 0 | 0 | 0 | 2 |  |
| conversation | 2 | 0 | 0 | 0 | 2 |  |
| cover | 2 | 0 | 0 | 2 | 0 |  |
| notify | 2 | 0 | 0 | 0 | 2 |  |
| person | 2 | 0 | 0 | 2 | 0 |  |

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
| `automation.laundry_washer_pending_notice_when_trevor_is_home` | derived_summary_or_dashboard_state | automation | Derived summary/status data is usually regenerated or shown as current state. |  |  |  |
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
| `event.back_patio_motion` | camera_or_event_state | ring | Camera/event entity state is often high churn; keep only if specific automations need history. |  |  |  |
| `event.back_stairs_motion` | camera_or_event_state | ring | Camera/event entity state is often high churn; keep only if specific automations need history. |  |  |  |
| `event.back_yard_vehicle` | camera_or_event_state | unifiprotect | Camera/event entity state is often high churn; keep only if specific automations need history. |  |  |  |
| `event.backup_automatic_backup` | camera_or_event_state | backup | Camera/event entity state is often high churn; keep only if specific automations need history. |  |  |  |
| `event.dryer_error` | camera_or_event_state | lg_thinq | Camera/event entity state is often high churn; keep only if specific automations need history. |  |  |  |
| `event.dryer_notification` | camera_or_event_state | lg_thinq | Camera/event entity state is often high churn; keep only if specific automations need history. |  |  |  |
| `event.front_door_ding` | camera_or_event_state | ring | Camera/event entity state is often high churn; keep only if specific automations need history. |  |  |  |
| `event.front_door_motion` | camera_or_event_state | ring | Camera/event entity state is often high churn; keep only if specific automations need history. |  |  |  |
| `event.garage_vehicle` | camera_or_event_state | unifiprotect | Camera/event entity state is often high churn; keep only if specific automations need history. |  |  |  |
| `event.mechanical_room_vehicle` | camera_or_event_state | unifiprotect | Camera/event entity state is often high churn; keep only if specific automations need history. |  |  |  |
| `event.mud_room_vehicle` | camera_or_event_state | unifiprotect | Camera/event entity state is often high churn; keep only if specific automations need history. |  |  |  |

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

For remote systems where copying the full DB is impractical, first collect a small DB stats JSON on the HA host, then run:

```bash
python3 tools/generate_recorder_inventory.py --db-stats-json .tmp/recorder-db-row-stats.json
```

Do not use this inventory as an automatic exclusion list. Treat it as the audit map for deciding what should be kept, shortened, or made current-only.
