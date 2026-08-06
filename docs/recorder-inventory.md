# Recorder Inventory

A recording-focused inventory for Home Assistant Recorder. This sits next to the device inventory, but answers a different question: what state history Home Assistant is saving, how long it is retained, and which classes of entities should prove they need long-term stateful history.

## At A Glance

| Thing | Count |
| --- | --- |
| Configured retention | 30 days |
| Entities reviewed | 2512 |
| Recorder candidates | 1566 |
| Excluded by Recorder config | 578 |
| Disabled in registry | 368 |
| Low stateful-need candidates | 172 |
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
| excluded entities | sun.sun, weather.forecast_home, switch.g6_instant_motion, switch.g6_instant_motion_2, switch.g6_instant_motion_3, switch.mechanical_room_motion, switch.mud_room_motion, switch.wynn_s_room_motion, sensor.away_security_entry_point_issues, sensor.bonticou_gateway_cpu_utilization_2, sensor.bonticou_gateway_memory_utilization_2, sensor.bonticou_gateway_storage_utilization, sensor.device_inventory_pending_digest, sensor.device_inventory_status, sensor.downstairs_climate_insight, sensor.environment_attic_status, sensor.environment_basement_status, sensor.environment_dining_room_status, sensor.environment_garage_status, sensor.environment_house_status, sensor.environment_kitchen_status, sensor.environment_main_floor_status, sensor.environment_office_status, sensor.environment_primary_bedroom_status, sensor.environment_second_floor_status, sensor.fios_router_upload_speed, sensor.fios_vhtx3, sensor.flower_lamp_signal_level, sensor.g6_instant_disk_write_rate, sensor.g6_instant_disk_write_rate_2, sensor.g6_instant_disk_write_rate_3, sensor.g6_instant_storage_used, sensor.g6_instant_storage_used_2, sensor.g6_instant_storage_used_3, sensor.garbage_recycling_schedule, sensor.house_notice_timeline, sensor.irrigation_7_day_ledger, sensor.irrigation_dashboard_status, sensor.irrigation_flow_baseline_status, sensor.irrigation_focus_zone_detail, sensor.irrigation_history_status, sensor.irrigation_running_context, sensor.irrigation_schedule_summary, sensor.irrigation_zone_attention_summary, sensor.mechanical_room_disk_write_rate, sensor.mechanical_room_storage_used, binary_sensor.metro_north_commute_card_active, sensor.metro_north_nwp_to_grand_central, sensor.mud_room_disk_write_rate, sensor.mud_room_storage_used, sensor.ratgdo32_4536e8_wifi_signal, sensor.ratgdo32disco_c26634_wifi_signal, sensor.ting_notification_status, sensor.u7_pro_family_room_cpu_utilization, sensor.u7_pro_family_room_memory_utilization, sensor.u7_pro_family_room_uptime, sensor.u7_pro_mesh_cpu_utilization, sensor.u7_pro_mesh_memory_utilization, sensor.u7_pro_mesh_uptime, sensor.u7_pro_mud_room_cpu_utilization, sensor.u7_pro_mud_room_memory_utilization, sensor.u7_pro_mud_room_uptime, sensor.u7_pro_outdoor_cpu_utilization, sensor.u7_pro_outdoor_memory_utilization, sensor.u7_pro_outdoor_uptime, sensor.uplight_2_signal_level, sensor.uplight_signal_level, sensor.usw_flex_2_5g_5_cpu_utilization, sensor.usw_flex_2_5g_5_memory_utilization, sensor.usw_flex_2_5g_5_uptime, sensor.usw_lite_8_poe_uptime, sensor.wine_collection_snapshot, sensor.wynn_s_room_disk_write_rate, sensor.wynn_s_room_storage_used, switch.back_patio_motion_detection, switch.back_stairs_motion_detection, switch.bonticou, switch.bonticou_guest, switch.casey_s_closet_alarm_sound_detection, switch.casey_s_closet_motion_detection, switch.dining_room_dining_room_thermostat_dining_room_airplay_enable, switch.dining_room_mute, switch.dining_room_tv_autoplay, switch.dining_room_ungroup_on_autoplay, switch.family_room_family_room_tv_autoplay, switch.family_room_family_room_ungroup_on_autoplay, switch.fios_vhtx3, switch.flower_lamp_auto_off_enabled, switch.flower_lamp_auto_update_enabled, switch.flower_lamp_led, switch.front_door_in_home_chime, switch.front_door_motion_detection, switch.great_room_speakers_great_room_sonos_tv_autoplay, switch.great_room_speakers_great_room_sonos_ungroup_on_autoplay, switch.kitchen_speakers_kitchen_sonos_tv_autoplay, switch.kitchen_speakers_kitchen_sonos_ungroup_on_autoplay, switch.master_master_thermostat_master_airplay_enable, switch.master_mute_2, switch.move_2_a_tv_autoplay, switch.move_2_a_ungroup_on_autoplay, switch.move_2_b_tv_autoplay, switch.move_2_b_ungroup_on_autoplay, switch.mudroom_door_in_home_chime, switch.mudroom_door_motion_detection, switch.office_subwoofer_enabled_2, switch.office_tv_autoplay, switch.office_ungroup_on_autoplay, switch.ratgdo32_4536e8_led, switch.ratgdo32disco_c26634_laser, switch.ratgdo32disco_c26634_learn, switch.ratgdo32disco_c26634_led, switch.unnamed_room_crossfade_10, switch.unnamed_room_crossfade_11, switch.unnamed_room_crossfade_2, switch.unnamed_room_crossfade_3, switch.unnamed_room_crossfade_4, switch.unnamed_room_crossfade_5, switch.unnamed_room_crossfade_6, switch.unnamed_room_crossfade_7, switch.unnamed_room_crossfade_8, switch.unnamed_room_crossfade_9, switch.unnamed_room_loudness_10, switch.unnamed_room_loudness_11, switch.unnamed_room_loudness_2, switch.unnamed_room_loudness_3, switch.unnamed_room_loudness_4, switch.unnamed_room_loudness_5, switch.unnamed_room_loudness_6, switch.unnamed_room_loudness_7, switch.unnamed_room_loudness_8, switch.unnamed_room_loudness_9, switch.unnamed_room_master_sonos_tv_autoplay, switch.unnamed_room_master_sonos_ungroup_on_autoplay, switch.unnamed_room_master_tv_autoplay, switch.unnamed_room_master_ungroup_on_autoplay, switch.unnamed_room_night_sound_2, switch.unnamed_room_speech_enhancement_2, switch.unnamed_room_surround_enabled_2, switch.unnamed_room_surround_music_full_volume_2, switch.unnamed_room_unnamed_room_crossfade_2, switch.unnamed_room_unnamed_room_loudness_2, switch.unnamed_room_unnamed_room_tv_autoplay, switch.unnamed_room_unnamed_room_tv_autoplay_2, switch.unnamed_room_unnamed_room_ungroup_on_autoplay, switch.unnamed_room_unnamed_room_ungroup_on_autoplay_2, switch.uplight_2_auto_off_enabled, switch.uplight_2_auto_update_enabled, switch.uplight_2_led, switch.uplight_auto_off_enabled, switch.uplight_auto_update_enabled, switch.uplight_led, switch.wynn_s_room_wynn_sonos_tv_autoplay, switch.wynn_s_room_wynn_sonos_ungroup_on_autoplay |

## Largest Low-Stateful-Need Review Sets

| Category | Entities | Low | Medium | High | DB rows | Live attr bytes |
| --- | --- | --- | --- | --- | --- | --- |
| derived_summary_or_dashboard_state | 151 | 151 | 0 | 0 |  |  |
| camera_or_event_state | 17 | 17 | 0 | 0 |  |  |
| integration_config_or_update_state | 2 | 2 | 0 | 0 |  |  |
| infrastructure_health_diagnostic | 2 | 2 | 0 | 0 |  |  |
| operational_state_history | 432 | 0 | 432 | 0 |  |  |
| event_or_safety_history | 417 | 0 | 0 | 417 |  |  |
| uncategorized | 384 | 0 | 0 | 0 |  |  |
| physical_timeseries | 89 | 0 | 0 | 89 |  |  |
| infrastructure_or_camera_misc | 72 | 0 | 72 | 0 |  |  |
| signal_quality_diagnostic | 0 | 0 | 0 | 0 |  |  |

## Domain Review

| Domain | Recorder candidates | Low | Medium | High | Unknown | DB rows |
| --- | --- | --- | --- | --- | --- | --- |
| sensor | 443 | 114 | 20 | 220 | 89 |  |
| binary_sensor | 293 | 4 | 49 | 147 | 93 |  |
| automation | 189 | 14 | 175 | 0 | 0 |  |
| script | 151 | 10 | 141 | 0 | 0 |  |
| input_datetime | 90 | 5 | 0 | 13 | 72 |  |
| device_tracker | 89 | 0 | 89 | 0 | 0 |  |
| switch | 73 | 2 | 0 | 63 | 8 |  |
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
| `event.mudroom_door_ding` | camera_or_event_state | ring | Camera/event entity state is often high churn; keep only if specific automations need history. |  |  |  |

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
