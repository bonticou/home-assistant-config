# Recorder Inventory

A recording-focused inventory for Home Assistant Recorder. This sits next to the device inventory, but answers a different question: what state history Home Assistant is saving, how long it is retained, and which classes of entities should prove they need long-term stateful history.

## At A Glance

| Thing | Count |
| --- | --- |
| Configured retention | 30 days |
| Entities reviewed | 2356 |
| Recorder candidates | 1583 |
| Excluded by Recorder config | 424 |
| Disabled in registry | 349 |
| Low stateful-need candidates | 266 |
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
| excluded domains | button, camera, number, select, update |
| excluded entity globs | sensor.*_signal_strength, sensor.*_rssi, sensor.*_lqi, sensor.*_linkquality, switch.*_analytics_enabled, switch.*_animal_detection, switch.*_baby_cry_detection, switch.*_car_alarm_detection, switch.*_car_horn_detection, switch.*_co_alarm_detection, switch.*_crossfade, switch.*_glass_break_detection, switch.*_humidity_sensor, switch.*_insights_enabled, switch.*_license_plate_detection, switch.*_light_sensor, switch.*_loudness, switch.*_night_sound, switch.*_none, switch.*_overlay_show_*, switch.*_person_detection, switch.*_privacy_mode, switch.*_siren_detection, switch.*_smoke_detection, switch.*_speaking_detection, switch.*_speech_enhancement, switch.*_status_light*, switch.*_subwoofer_enabled, switch.*_surround_enabled, switch.*_surround_music_full_volume, switch.*_system_sounds, switch.*_temperature_sensor, switch.*_vehicle_detection |
| excluded entities | sun.sun, weather.forecast_home, switch.g6_instant_motion, switch.g6_instant_motion_2, switch.g6_instant_motion_3, switch.mechanical_room_motion, switch.mud_room_motion, switch.wynn_s_room_motion, sensor.device_inventory_pending_digest, sensor.device_inventory_status, sensor.garbage_recycling_schedule, sensor.house_notice_timeline, sensor.irrigation_7_day_ledger, sensor.irrigation_flow_baseline_status, sensor.irrigation_history_status, sensor.irrigation_schedule_summary, sensor.metro_north_nwp_to_grand_central, sensor.wine_collection_snapshot |

## Largest Low-Stateful-Need Review Sets

| Category | Entities | Low | Medium | High | DB rows | Live attr bytes |
| --- | --- | --- | --- | --- | --- | --- |
| derived_summary_or_dashboard_state | 167 | 167 | 0 | 0 |  |  |
| integration_config_or_update_state | 46 | 46 | 0 | 0 |  |  |
| infrastructure_health_diagnostic | 35 | 35 | 0 | 0 |  |  |
| camera_or_event_state | 15 | 15 | 0 | 0 |  |  |
| signal_quality_diagnostic | 3 | 3 | 0 | 0 |  |  |
| event_or_safety_history | 416 | 0 | 0 | 416 |  |  |
| operational_state_history | 412 | 0 | 412 | 0 |  |  |
| uncategorized | 346 | 0 | 0 | 0 |  |  |
| physical_timeseries | 72 | 0 | 0 | 72 |  |  |
| infrastructure_or_camera_misc | 71 | 0 | 71 | 0 |  |  |

## Domain Review

| Domain | Recorder candidates | Low | Medium | High | Unknown | DB rows |
| --- | --- | --- | --- | --- | --- | --- |
| sensor | 472 | 165 | 19 | 206 | 82 |  |
| binary_sensor | 282 | 5 | 49 | 144 | 84 |  |
| automation | 183 | 13 | 170 | 0 | 0 |  |
| script | 144 | 10 | 134 | 0 | 0 |  |
| switch | 115 | 47 | 0 | 63 | 5 |  |
| device_tracker | 84 | 0 | 84 | 0 | 0 |  |
| input_datetime | 82 | 5 | 0 | 13 | 64 |  |
| input_boolean | 42 | 2 | 0 | 8 | 32 |  |
| light | 36 | 0 | 3 | 2 | 31 |  |
| valve | 30 | 0 | 0 | 30 | 0 |  |
| media_player | 24 | 0 | 24 | 0 | 0 |  |
| input_text | 23 | 4 | 0 | 5 | 14 |  |
| input_number | 22 | 0 | 0 | 4 | 18 |  |
| event | 15 | 15 | 0 | 0 | 0 |  |
| lock | 4 | 0 | 0 | 4 | 0 |  |
| climate | 3 | 0 | 0 | 3 | 0 |  |
| input_select | 3 | 0 | 0 | 0 | 3 |  |
| remote | 3 | 0 | 0 | 0 | 3 |  |
| tts | 3 | 0 | 0 | 1 | 2 |  |
| ai_task | 2 | 0 | 0 | 0 | 2 |  |
| conversation | 2 | 0 | 0 | 0 | 2 |  |
| cover | 2 | 0 | 0 | 2 | 0 |  |
| person | 2 | 0 | 0 | 2 | 0 |  |
| siren | 2 | 0 | 0 | 0 | 2 |  |

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
| `event.back_patio_motion` | camera_or_event_state | ring | Camera/event entity state is often high churn; keep only if specific automations need history. |  |  |  |
| `event.back_stairs_motion` | camera_or_event_state | ring | Camera/event entity state is often high churn; keep only if specific automations need history. |  |  |  |
| `event.back_yard_vehicle` | camera_or_event_state | unifiprotect | Camera/event entity state is often high churn; keep only if specific automations need history. |  |  |  |
| `event.backup_automatic_backup` | camera_or_event_state | backup | Camera/event entity state is often high churn; keep only if specific automations need history. |  |  |  |
| `event.front_door_ding` | camera_or_event_state | ring | Camera/event entity state is often high churn; keep only if specific automations need history. |  |  |  |
| `event.front_door_motion` | camera_or_event_state | ring | Camera/event entity state is often high churn; keep only if specific automations need history. |  |  |  |
| `event.garage_vehicle` | camera_or_event_state | unifiprotect | Camera/event entity state is often high churn; keep only if specific automations need history. |  |  |  |
| `event.mechanical_room_vehicle` | camera_or_event_state | unifiprotect | Camera/event entity state is often high churn; keep only if specific automations need history. |  |  |  |
| `event.mud_room_vehicle` | camera_or_event_state | unifiprotect | Camera/event entity state is often high churn; keep only if specific automations need history. |  |  |  |
| `event.mudroom_door_ding` | camera_or_event_state | ring | Camera/event entity state is often high churn; keep only if specific automations need history. |  |  |  |
| `event.mudroom_door_motion` | camera_or_event_state | ring | Camera/event entity state is often high churn; keep only if specific automations need history. |  |  |  |
| `event.play_room_vehicle` | camera_or_event_state | unifiprotect | Camera/event entity state is often high churn; keep only if specific automations need history. |  |  |  |

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
