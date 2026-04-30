# Device Inventory

Generated from Home Assistant registries and UniFi-tracked network clients. Sensitive network identifiers are redacted.

## Summary

| Metric | Count |
| --- | --- |
| Devices | 114 |
| Entities | 962 |
| Orphan entities | 65 |
| Network clients | 95 |
| Areas | 27 |
| Integrations | 26 |

### Roles

| Role | Entities |
| --- | --- |
| control | 380 |
| network | 95 |
| other | 18 |
| telemetry | 469 |

### Top Integrations

| Integration | Entities |
| --- | --- |
| unifiprotect | 309 |
| unifi | 209 |
| sonos | 153 |
| sensorpush_cloud | 56 |
| flo | 43 |
| ring | 39 |
| hassio | 35 |
| hacs | 20 |
| mobile_app | 14 |
| automation | 12 |
| lutron_caseta | 12 |
| upnp | 12 |
| sun | 10 |
| matter | 7 |
| template | 6 |
| backup | 5 |
| airthings | 4 |
| apple_tv | 4 |
| cloud | 3 |
| cast | 2 |

## Devices By Area

### Attic

#### Attic

- Device ID: `device_0ccd0eba4181`
- Integration: sensorpush_cloud
- Model: SensorPush HT1
- Capability mix: 8 telemetry, 0 control, 0 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `sensor.attic_altitude` | telemetry | sensorpush_cloud | distance (ft) | disabled |
| `sensor.attic_atmospheric_pressure` | telemetry | sensorpush_cloud | atmospheric_pressure (inHg) | disabled |
| `sensor.attic_battery_voltage` | telemetry | sensorpush_cloud | voltage (V) | disabled |
| `sensor.attic_dew_point` | telemetry | sensorpush_cloud | temperature (°F) | disabled |
| `sensor.attic_humidity` | telemetry | sensorpush_cloud | humidity (%) | not_enriched |
| `sensor.attic_signal_strength` | telemetry | sensorpush_cloud | signal_strength (dBm) | disabled |
| `sensor.attic_temperature` | telemetry | sensorpush_cloud | temperature (°F) | not_enriched |
| `sensor.attic_vapor_pressure` | telemetry | sensorpush_cloud | pressure (psi) | disabled |

### Back Stairs

#### Back Stairs Back Stairs

- Device ID: `device_289d2bae593b`
- Integration: lutron_caseta
- Model: Lutron Electronics Co., Inc DVRF-6L (DivaSmartDimmer)
- Capability mix: 0 telemetry, 1 control, 0 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `light.back_stairs_back_stairs` | control | lutron_caseta |  | not_enriched |

### Back Yard

#### Back Patio

- Device ID: `device_fba4253633e3`
- Integration: ring
- Model: Ring Spotlight Cam Wired
- Capability mix: 6 telemetry, 4 control, 0 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `camera.back_patio_live_view` | telemetry | ring |  | not_enriched |
| `event.back_patio_motion` | telemetry | ring | motion | not_enriched |
| `light.back_patio_light` | control | ring |  | not_enriched |
| `number.back_patio_volume` | control | ring |  | not_enriched |
| `sensor.back_patio_battery` | telemetry | ring | battery (%) | not_enriched |
| `sensor.back_patio_last_activity` | telemetry | ring | timestamp | not_enriched |
| `sensor.back_patio_signal_strength` | telemetry | ring | signal_strength (dBm) | disabled |
| `sensor.back_patio_wi_fi_signal_category` | telemetry | ring | diagnostic | disabled |
| `siren.back_patio_siren` | control | ring |  | not_enriched |
| `switch.back_patio_motion_detection` | control | ring |  | not_enriched |

### Basement

#### Basement Air Quality

- Device ID: `device_6b447073c190`
- Integration: airthings
- Model: Airthings View Radon
- Capability mix: 4 telemetry, 0 control, 0 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `sensor.basement_air_quality_battery` | telemetry | airthings | battery (%) | not_enriched |
| `sensor.basement_air_quality_humidity` | telemetry | airthings | humidity (%) | not_enriched |
| `sensor.basement_air_quality_radon` | telemetry | airthings | Bq/m³ | not_enriched |
| `sensor.basement_air_quality_temperature` | telemetry | airthings | temperature (°F) | not_enriched |

#### Basement Ejector - Leak Detection

- Device ID: `device_42a5e06ebdf7`
- Integration: flo, unifi
- Model: Flo by Moen puck_v1
- Capability mix: 4 telemetry, 0 control, 1 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `binary_sensor.basement_ejector_leak_detection_water_detected` | telemetry | flo | problem | not_enriched |
| `device_tracker.basement_ejector_leak_detection_espressif` | network | unifi | diagnostic | not_enriched |
| `sensor.basement_ejector_leak_detection_battery` | telemetry | flo | battery (%) | not_enriched |
| `sensor.basement_ejector_leak_detection_humidity` | telemetry | flo | humidity (%) | not_enriched |
| `sensor.basement_ejector_leak_detection_temperature` | telemetry | flo | temperature (°F) | not_enriched |

### Electrical Room

#### Bonticou Gateway

- Device ID: `device_582d95951335`
- Integration: unifi, unifiprotect
- Model: Ubiquiti Networks UDMA6A8
- Capability mix: 28 telemetry, 12 control, 1 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `binary_sensor.bonticou_gateway_ssd_1` | telemetry | unifiprotect | problem | not_enriched |
| `button.bonticou_gateway_port_4_power_cycle` | control | unifi | restart | not_enriched |
| `button.bonticou_gateway_restart` | control | unifi | restart | not_enriched |
| `device_tracker.bonticou_gateway` | network | unifi | diagnostic | not_enriched |
| `sensor.bonticou_gateway_bonticou_gateway_cpu_temperature` | telemetry | unifi | temperature (°F) | disabled |
| `sensor.bonticou_gateway_bonticou_gateway_local_temperature` | telemetry | unifi | temperature (°F) | disabled |
| `sensor.bonticou_gateway_clients` | telemetry | unifi | diagnostic | disabled |
| `sensor.bonticou_gateway_cloudflare_wan2_latency` | telemetry | unifi | duration (ms) | disabled |
| `sensor.bonticou_gateway_cloudflare_wan_latency` | telemetry | unifi | duration (ms) | disabled |
| `sensor.bonticou_gateway_cpu_temperature` | telemetry | unifiprotect | temperature (°F) | disabled |
| `sensor.bonticou_gateway_cpu_utilization` | telemetry | unifiprotect | diagnostic (%) | disabled |
| `sensor.bonticou_gateway_cpu_utilization_2` | telemetry | unifi | diagnostic (%) | not_enriched |
| `sensor.bonticou_gateway_google_wan2_latency` | telemetry | unifi | duration (ms) | disabled |
| `sensor.bonticou_gateway_google_wan_latency` | telemetry | unifi | duration (ms) | disabled |
| `sensor.bonticou_gateway_memory_utilization` | telemetry | unifiprotect | diagnostic (%) | disabled |
| `sensor.bonticou_gateway_memory_utilization_2` | telemetry | unifi | diagnostic (%) | not_enriched |
| `sensor.bonticou_gateway_microsoft_wan2_latency` | telemetry | unifi | duration (ms) | disabled |
| `sensor.bonticou_gateway_microsoft_wan_latency` | telemetry | unifi | duration (ms) | disabled |
| `sensor.bonticou_gateway_port_4_poe_power` | telemetry | unifi | power (W) | disabled |
| `sensor.bonticou_gateway_recording_capacity` | telemetry | unifiprotect | diagnostic (s) | not_enriched |
| `sensor.bonticou_gateway_resolution_4k_video` | telemetry | unifiprotect | diagnostic (%) | not_enriched |
| `sensor.bonticou_gateway_resolution_free_space` | telemetry | unifiprotect | diagnostic (%) | not_enriched |
| `sensor.bonticou_gateway_resolution_hd_video` | telemetry | unifiprotect | diagnostic (%) | not_enriched |
| `sensor.bonticou_gateway_state` | telemetry | unifi | enum | not_enriched |
| `sensor.bonticou_gateway_storage_utilization` | telemetry | unifiprotect | diagnostic (%) | not_enriched |
| `sensor.bonticou_gateway_type_continuous_video` | telemetry | unifiprotect | diagnostic (%) | not_enriched |
| `sensor.bonticou_gateway_type_detections_video` | telemetry | unifiprotect | diagnostic (%) | not_enriched |
| `sensor.bonticou_gateway_type_timelapse_video` | telemetry | unifiprotect | diagnostic (%) | not_enriched |
| `sensor.bonticou_gateway_uptime` | telemetry | unifiprotect | timestamp | not_enriched |
| `sensor.bonticou_gateway_uptime_2` | telemetry | unifi | timestamp | not_enriched |
| `switch.bonticou_gateway_analytics_enabled` | control | unifiprotect | config | not_enriched |
| `switch.bonticou_gateway_insights_enabled` | control | unifiprotect | config | not_enriched |
| `switch.bonticou_gateway_port_1` | control | unifi | switch | disabled |
| `switch.bonticou_gateway_port_2` | control | unifi | switch | disabled |
| `switch.bonticou_gateway_port_3` | control | unifi | switch | disabled |
| `switch.bonticou_gateway_port_4` | control | unifi | switch | disabled |
| `switch.bonticou_gateway_port_4_poe` | control | unifi | outlet | disabled |
| `switch.bonticou_gateway_port_5` | control | unifi | switch | disabled |
| `switch.bonticou_gateway_sfp_1` | control | unifi | switch | disabled |
| `switch.bonticou_gateway_sfp_2` | control | unifi | switch | disabled |
| `update.bonticou_gateway` | telemetry | unifi | firmware | not_enriched |

#### Electrical Room - Leak Detection

- Device ID: `device_d82102de874c`
- Integration: flo, unifi
- Model: Flo by Moen puck_v1
- Capability mix: 4 telemetry, 0 control, 1 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `binary_sensor.electrical_room_leak_detection_water_detected` | telemetry | flo | problem | not_enriched |
| `device_tracker.electrical_room_leak_detection_espressif` | network | unifi | diagnostic | not_enriched |
| `sensor.electrical_room_leak_detection_battery` | telemetry | flo | battery (%) | not_enriched |
| `sensor.electrical_room_leak_detection_humidity` | telemetry | flo | humidity (%) | not_enriched |
| `sensor.electrical_room_leak_detection_temperature` | telemetry | flo | temperature (°F) | not_enriched |

#### Fios Router

- Device ID: `device_3995819518d9`
- Integration: upnp
- Model: Verizon G3100
- Capability mix: 12 telemetry, 0 control, 0 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `binary_sensor.fios_router_wan_status` | telemetry | upnp | connectivity | not_enriched |
| `sensor.fios_router_data_received` | telemetry | upnp | data_size (B) | disabled |
| `sensor.fios_router_data_sent` | telemetry | upnp | data_size (B) | disabled |
| `sensor.fios_router_external_ip` | telemetry | upnp | diagnostic | not_enriched |
| `sensor.fios_router_number_of_port_mapping_entries_ipv4` | telemetry | upnp | diagnostic | disabled |
| `sensor.fios_router_packet_download_speed` | telemetry | upnp | packets/s | disabled |
| `sensor.fios_router_packet_upload_speed` | telemetry | upnp | packets/s | disabled |
| `sensor.fios_router_packets_received` | telemetry | upnp | packets | disabled |
| `sensor.fios_router_packets_sent` | telemetry | upnp | packets | disabled |
| `sensor.fios_router_upload_speed` | telemetry | upnp | data_rate (KiB/s) | not_enriched |
| `sensor.fios_router_uptime` | telemetry | upnp | duration (s) | disabled |
| `sensor.fios_router_wan_status` | telemetry | upnp | diagnostic | disabled |

### Family Room

#### Family Room

- Device ID: `device_dc0447a8354b`
- Integration: sonos, unifi
- Model: Sonos Arc Ultra
- Capability mix: 2 telemetry, 18 control, 1 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `binary_sensor.family_room_microphone` | telemetry | sonos | diagnostic | not_enriched |
| `device_tracker.sonoszp_6` | network | unifi | diagnostic | not_enriched |
| `media_player.family_room` | control | sonos | speaker | not_enriched |
| `number.family_room_audio_delay` | control | sonos | config | not_enriched |
| `number.family_room_balance` | control | sonos | config | not_enriched |
| `number.family_room_bass` | control | sonos | config | not_enriched |
| `number.family_room_music_surround_level` | control | sonos | config | not_enriched |
| `number.family_room_sub_gain` | control | sonos | config | not_enriched |
| `number.family_room_surround_level` | control | sonos | config | not_enriched |
| `number.family_room_treble` | control | sonos | config | not_enriched |
| `select.family_room_speech_enhancement` | control | sonos |  | not_enriched |
| `sensor.family_room_audio_input_format` | telemetry | sonos | diagnostic | not_enriched |
| `switch.family_room_crossfade` | control | sonos | config | not_enriched |
| `switch.family_room_loudness` | control | sonos | config | not_enriched |
| `switch.family_room_night_sound` | control | sonos | config | not_enriched |
| `switch.family_room_speech_enhancement` | control | sonos | config | not_enriched |
| `switch.family_room_status_light` | control | sonos | config | disabled |
| `switch.family_room_subwoofer_enabled` | control | sonos | config | not_enriched |
| `switch.family_room_surround_enabled` | control | sonos | config | not_enriched |
| `switch.family_room_surround_music_full_volume` | control | sonos | config | not_enriched |
| `switch.family_room_touch_controls` | control | sonos | config | disabled |

#### Main Floor

- Device ID: `device_26607127a43f`
- Integration: sensorpush_cloud
- Model: SensorPush HT1
- Capability mix: 8 telemetry, 0 control, 0 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `sensor.main_floor_altitude` | telemetry | sensorpush_cloud | distance (ft) | disabled |
| `sensor.main_floor_atmospheric_pressure` | telemetry | sensorpush_cloud | atmospheric_pressure (inHg) | disabled |
| `sensor.main_floor_battery_voltage` | telemetry | sensorpush_cloud | voltage (V) | disabled |
| `sensor.main_floor_dew_point` | telemetry | sensorpush_cloud | temperature (°F) | disabled |
| `sensor.main_floor_humidity` | telemetry | sensorpush_cloud | humidity (%) | not_enriched |
| `sensor.main_floor_signal_strength` | telemetry | sensorpush_cloud | signal_strength (dBm) | disabled |
| `sensor.main_floor_temperature` | telemetry | sensorpush_cloud | temperature (°F) | not_enriched |
| `sensor.main_floor_vapor_pressure` | telemetry | sensorpush_cloud | pressure (psi) | disabled |

#### Smart Bridge 2

- Device ID: `device_aa3c678af681`
- Integration: lutron_caseta
- Model: Lutron Electronics Co., Inc L-BDG2-WH (SmartBridge)
- Capability mix: 0 telemetry, 1 control, 0 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `switch.unassigned_smart_away` | control | lutron_caseta |  | not_enriched |

### Family Room TV

#### Family Room TV

- Device ID: `device_f5a5522ed109`
- Integration: apple_tv
- Model: Apple Apple TV 4K
- Capability mix: 0 telemetry, 2 control, 0 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `media_player.family_room_tv_2` | control | apple_tv |  | not_enriched |
| `remote.family_room_tv` | control | apple_tv |  | not_enriched |

### Front Door

#### Front Door

- Device ID: `device_bd9feeb41bd1`
- Integration: ring
- Model: Ring Doorbell Pro 2
- Capability mix: 7 telemetry, 3 control, 0 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `camera.front_door_live_view` | telemetry | ring |  | not_enriched |
| `event.front_door_ding` | telemetry | ring | doorbell | not_enriched |
| `event.front_door_motion` | telemetry | ring | motion | not_enriched |
| `number.front_door_volume` | control | ring |  | not_enriched |
| `sensor.front_door_battery` | telemetry | ring | battery (%) | not_enriched |
| `sensor.front_door_last_activity` | telemetry | ring | timestamp | not_enriched |
| `sensor.front_door_signal_strength` | telemetry | ring | signal_strength (dBm) | disabled |
| `sensor.front_door_wi_fi_signal_category` | telemetry | ring | diagnostic | disabled |
| `switch.front_door_in_home_chime` | control | ring |  | not_enriched |
| `switch.front_door_motion_detection` | control | ring |  | not_enriched |

### Front Foyer

#### Front Foyer Ceiling Lights

- Device ID: `device_bc242f727014`
- Integration: lutron_caseta
- Model: Lutron Electronics Co., Inc DVRF-6L (DivaSmartDimmer)
- Capability mix: 0 telemetry, 1 control, 0 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `light.front_foyer_ceiling_lights` | control | lutron_caseta |  | not_enriched |

#### Front Foyer Sconces

- Device ID: `device_b0bcbe9d9a0e`
- Integration: lutron_caseta
- Model: Lutron Electronics Co., Inc DVRF-5NS (DivaSmartSwitch)
- Capability mix: 0 telemetry, 1 control, 0 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `switch.front_foyer_sconces` | control | lutron_caseta |  | not_enriched |

### Front Yard

#### Front Yard

- Device ID: `device_ca0387716233`
- Integration: unifi, unifiprotect
- Model: Ubiquiti G6 Instant
- Capability mix: 27 telemetry, 32 control, 1 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `binary_sensor.wynn_s_room_animal_detected` | telemetry | unifiprotect |  | not_enriched |
| `binary_sensor.wynn_s_room_audio_object_detected` | telemetry | unifiprotect |  | disabled |
| `binary_sensor.wynn_s_room_baby_cry_detected` | telemetry | unifiprotect |  | not_enriched |
| `binary_sensor.wynn_s_room_barking_detected` | telemetry | unifiprotect |  | not_enriched |
| `binary_sensor.wynn_s_room_car_alarm_detected` | telemetry | unifiprotect |  | not_enriched |
| `binary_sensor.wynn_s_room_car_horn_detected` | telemetry | unifiprotect |  | not_enriched |
| `binary_sensor.wynn_s_room_co_alarm_detected` | telemetry | unifiprotect | carbon_monoxide | not_enriched |
| `binary_sensor.wynn_s_room_glass_break_detected` | telemetry | unifiprotect |  | not_enriched |
| `binary_sensor.wynn_s_room_is_dark` | telemetry | unifiprotect |  | not_enriched |
| `binary_sensor.wynn_s_room_motion` | telemetry | unifiprotect | motion | not_enriched |
| `binary_sensor.wynn_s_room_object_detected` | telemetry | unifiprotect |  | disabled |
| `binary_sensor.wynn_s_room_person_detected` | telemetry | unifiprotect |  | not_enriched |
| `binary_sensor.wynn_s_room_siren_detected` | telemetry | unifiprotect |  | not_enriched |
| `binary_sensor.wynn_s_room_smoke_alarm_detected` | telemetry | unifiprotect |  | not_enriched |
| `binary_sensor.wynn_s_room_speaking_detected` | telemetry | unifiprotect |  | not_enriched |
| `binary_sensor.wynn_s_room_vehicle_detected` | telemetry | unifiprotect |  | not_enriched |
| `button.wynn_s_room_restart` | control | unifiprotect | restart | disabled |
| `button.wynn_s_room_unadopt_device` | control | unifiprotect |  | disabled |
| `camera.wynn_s_room_high_resolution_channel` | telemetry | unifiprotect |  | not_enriched |
| `camera.wynn_s_room_high_resolution_channel_insecure` | telemetry | unifiprotect |  | disabled |
| `device_tracker.wynns_room` | network | unifi | diagnostic | not_enriched |
| `event.wynn_s_room_vehicle` | telemetry | unifiprotect |  | not_enriched |
| `media_player.wynn_s_room_speaker` | control | unifiprotect | speaker | not_enriched |
| `number.wynn_s_room_infrared_custom_lux_trigger` | control | unifiprotect | config | not_enriched |
| `number.wynn_s_room_microphone_level` | control | unifiprotect | config (%) | not_enriched |
| `number.wynn_s_room_system_sounds_volume` | control | unifiprotect | config (%) | not_enriched |
| `select.wynn_s_room_hdr_mode` | control | unifiprotect | config | not_enriched |
| `select.wynn_s_room_infrared_mode` | control | unifiprotect | config | not_enriched |
| `select.wynn_s_room_recording_mode` | control | unifiprotect | config | not_enriched |
| `sensor.wynn_s_room_disk_write_rate` | telemetry | unifiprotect | data_rate (MB/s) | not_enriched |
| `sensor.wynn_s_room_last_motion_detected` | telemetry | unifiprotect | timestamp | disabled |
| `sensor.wynn_s_room_oldest_recording` | telemetry | unifiprotect | timestamp | disabled |
| `sensor.wynn_s_room_received_data` | telemetry | unifiprotect | data_size (MB) | disabled |
| `sensor.wynn_s_room_storage_used` | telemetry | unifiprotect | data_size (MB) | not_enriched |
| `sensor.wynn_s_room_transferred_data` | telemetry | unifiprotect | data_size (MB) | disabled |
| `sensor.wynn_s_room_uptime` | telemetry | unifiprotect | timestamp | disabled |
| `sensor.wynn_s_room_wi_fi_signal_strength` | telemetry | unifiprotect | signal_strength (dBm) | disabled |
| `switch.wynn_s_room_animal_detection` | control | unifiprotect | config | not_enriched |
| `switch.wynn_s_room_baby_cry_detection` | control | unifiprotect | config | not_enriched |
| `switch.wynn_s_room_car_alarm_detection` | control | unifiprotect | config | not_enriched |
| `switch.wynn_s_room_car_horn_detection` | control | unifiprotect | config | not_enriched |
| `switch.wynn_s_room_co_alarm_detection` | control | unifiprotect | config | not_enriched |
| `switch.wynn_s_room_glass_break_detection` | control | unifiprotect | config | not_enriched |
| `switch.wynn_s_room_hdr_mode` | control | unifiprotect | config | disabled |
| `switch.wynn_s_room_license_plate_detection` | control | unifiprotect | config | not_enriched |
| `switch.wynn_s_room_motion` | control | unifiprotect | config | not_enriched |
| `switch.wynn_s_room_none` | control | unifiprotect | config | not_enriched |
| `switch.wynn_s_room_overlay_show_date` | control | unifiprotect | config | not_enriched |
| `switch.wynn_s_room_overlay_show_logo` | control | unifiprotect | config | not_enriched |
| `switch.wynn_s_room_overlay_show_name` | control | unifiprotect | config | not_enriched |
| `switch.wynn_s_room_overlay_show_nerd_mode` | control | unifiprotect | config | not_enriched |
| `switch.wynn_s_room_person_detection` | control | unifiprotect | config | not_enriched |
| `switch.wynn_s_room_privacy_mode` | control | unifiprotect | config | not_enriched |
| `switch.wynn_s_room_siren_detection` | control | unifiprotect | config | not_enriched |
| `switch.wynn_s_room_smoke_detection` | control | unifiprotect | config | not_enriched |
| `switch.wynn_s_room_speaking_detection` | control | unifiprotect | config | not_enriched |
| `switch.wynn_s_room_ssh_enabled` | control | unifiprotect | config | disabled |
| `switch.wynn_s_room_status_light_2` | control | unifiprotect | config | not_enriched |
| `switch.wynn_s_room_system_sounds` | control | unifiprotect | config | not_enriched |
| `switch.wynn_s_room_vehicle_detection` | control | unifiprotect | config | not_enriched |

### Garage

#### Garage

- Device ID: `device_cb1e19da3f33`
- Integration: sensorpush_cloud
- Model: SensorPush HT1
- Capability mix: 8 telemetry, 0 control, 0 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `sensor.garage_altitude` | telemetry | sensorpush_cloud | distance (ft) | disabled |
| `sensor.garage_atmospheric_pressure` | telemetry | sensorpush_cloud | atmospheric_pressure (inHg) | disabled |
| `sensor.garage_battery_voltage` | telemetry | sensorpush_cloud | voltage (V) | disabled |
| `sensor.garage_dew_point` | telemetry | sensorpush_cloud | temperature (°F) | disabled |
| `sensor.garage_humidity` | telemetry | sensorpush_cloud | humidity (%) | not_enriched |
| `sensor.garage_signal_strength` | telemetry | sensorpush_cloud | signal_strength (dBm) | disabled |
| `sensor.garage_temperature` | telemetry | sensorpush_cloud | temperature (°F) | not_enriched |
| `sensor.garage_vapor_pressure` | telemetry | sensorpush_cloud | pressure (psi) | disabled |

### Great Room Speakers

#### Great Room Sonos

- Device ID: `device_96c096ed4a91`
- Integration: sonos, unifi
- Model: Sonos Era 300
- Capability mix: 1 telemetry, 8 control, 1 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `binary_sensor.great_room_speakers_microphone` | telemetry | sonos | diagnostic | not_enriched |
| `device_tracker.sonoszp_7` | network | unifi | diagnostic | not_enriched |
| `media_player.great_room_speakers` | control | sonos | speaker | not_enriched |
| `number.great_room_speakers_balance` | control | sonos | config | not_enriched |
| `number.great_room_speakers_bass` | control | sonos | config | not_enriched |
| `number.great_room_speakers_treble` | control | sonos | config | not_enriched |
| `switch.great_room_speakers_crossfade` | control | sonos | config | not_enriched |
| `switch.great_room_speakers_loudness` | control | sonos | config | not_enriched |
| `switch.great_room_speakers_status_light` | control | sonos | config | disabled |
| `switch.great_room_speakers_touch_controls` | control | sonos | config | disabled |

### Kitchen

#### Dishwasher - Leak Detection

- Device ID: `device_3047d7172478`
- Integration: flo, unifi
- Model: Flo by Moen puck_v1
- Capability mix: 4 telemetry, 0 control, 1 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `binary_sensor.dishwasher_leak_detection_water_detected` | telemetry | flo | problem | not_enriched |
| `device_tracker.dishwasher_leak_detection_espressif` | network | unifi | diagnostic | not_enriched |
| `sensor.dishwasher_leak_detection_battery` | telemetry | flo | battery (%) | not_enriched |
| `sensor.dishwasher_leak_detection_humidity` | telemetry | flo | humidity (%) | not_enriched |
| `sensor.dishwasher_leak_detection_temperature` | telemetry | flo | temperature (°F) | not_enriched |

#### Island Sink - Leak Detection

- Device ID: `device_52ba6957f618`
- Integration: flo, unifi
- Model: Flo by Moen puck_v1
- Capability mix: 5 telemetry, 0 control, 1 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `binary_sensor.island_sink_leak_detection_water_detected` | telemetry | flo | problem | not_enriched |
| `device_tracker.island_sink_leak_detection_espressif` | network | unifi | diagnostic | not_enriched |
| `sensor.espressif_link_speed_3` | telemetry | unifi | data_rate (Mbit/s) | disabled |
| `sensor.island_sink_leak_detection_battery` | telemetry | flo | battery (%) | not_enriched |
| `sensor.island_sink_leak_detection_humidity` | telemetry | flo | humidity (%) | not_enriched |
| `sensor.island_sink_leak_detection_temperature` | telemetry | flo | temperature (°F) | not_enriched |

#### Kitchen Fridge - Leak Detection

- Device ID: `device_4fc75f38e213`
- Integration: flo, unifi
- Model: Flo by Moen puck_v1
- Capability mix: 5 telemetry, 0 control, 1 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `binary_sensor.kitchen_fridge_leak_detection_water_detected` | telemetry | flo | problem | not_enriched |
| `device_tracker.kitchen_fridge_leak_detection_espressif` | network | unifi | diagnostic | not_enriched |
| `sensor.espressif_link_speed_5` | telemetry | unifi | data_rate (Mbit/s) | disabled |
| `sensor.kitchen_fridge_leak_detection_battery` | telemetry | flo | battery (%) | not_enriched |
| `sensor.kitchen_fridge_leak_detection_humidity` | telemetry | flo | humidity (%) | not_enriched |
| `sensor.kitchen_fridge_leak_detection_temperature` | telemetry | flo | temperature (°F) | not_enriched |

#### Kitchen Sink - Leak Detection

- Device ID: `device_937c61cbde64`
- Integration: flo, unifi
- Model: Flo by Moen puck_v1
- Capability mix: 5 telemetry, 0 control, 1 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `binary_sensor.kitchen_sink_leak_detection_water_detected` | telemetry | flo | problem | not_enriched |
| `device_tracker.kitchen_sink_leak_detection_espressif` | network | unifi | diagnostic | not_enriched |
| `sensor.espressif_link_speed_2` | telemetry | unifi | data_rate (Mbit/s) | disabled |
| `sensor.kitchen_sink_leak_detection_battery` | telemetry | flo | battery (%) | not_enriched |
| `sensor.kitchen_sink_leak_detection_humidity` | telemetry | flo | humidity (%) | not_enriched |
| `sensor.kitchen_sink_leak_detection_temperature` | telemetry | flo | temperature (°F) | not_enriched |

### Kitchen Speakers

#### Kitchen Sonos

- Device ID: `device_df07ddeb668b`
- Integration: sonos, unifi
- Model: Sonos Era 100
- Capability mix: 1 telemetry, 8 control, 1 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `binary_sensor.kitchen_speakers_microphone` | telemetry | sonos | diagnostic | not_enriched |
| `device_tracker.sonoszp` | network | unifi | diagnostic | not_enriched |
| `media_player.kitchen_speakers` | control | sonos | speaker | not_enriched |
| `number.kitchen_speakers_balance` | control | sonos | config | not_enriched |
| `number.kitchen_speakers_bass` | control | sonos | config | not_enriched |
| `number.kitchen_speakers_treble` | control | sonos | config | not_enriched |
| `switch.kitchen_speakers_crossfade` | control | sonos | config | not_enriched |
| `switch.kitchen_speakers_loudness` | control | sonos | config | not_enriched |
| `switch.kitchen_speakers_status_light` | control | sonos | config | disabled |
| `switch.kitchen_speakers_touch_controls` | control | sonos | config | disabled |

### Master

#### Master Lantern

- Device ID: `device_de9e0458bd8b`
- Integration: lutron_caseta
- Model: Lutron Electronics Co., Inc PD-5WS-DV-XX (WallSwitch)
- Capability mix: 0 telemetry, 1 control, 0 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `switch.master_lantern` | control | lutron_caseta |  | not_enriched |

#### Master Wall Remote

- Device ID: `device_cdf225e33940`
- Integration: lutron_caseta
- Model: Lutron Electronics Co., Inc PJ2-2BRL-GXX-X01 (Pico2ButtonRaiseLower)
- Capability mix: 0 telemetry, 4 control, 0 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `button.unassigned_accent_lights_remote_1_lower` | control | lutron_caseta |  | disabled |
| `button.unassigned_accent_lights_remote_1_off` | control | lutron_caseta |  | disabled |
| `button.unassigned_accent_lights_remote_1_on` | control | lutron_caseta |  | disabled |
| `button.unassigned_accent_lights_remote_1_raise` | control | lutron_caseta |  | disabled |

### Mechanical Room

#### Flo shutoff

- Device ID: `device_6444bcfdb6d0`
- Integration: flo, unifi
- Model: Flo by Moen flo_device_075_v2
- Capability mix: 7 telemetry, 1 control, 1 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `binary_sensor.flo_shutoff_pending_system_alerts` | telemetry | flo | problem | not_enriched |
| `device_tracker.flo_d4e95ef8775b` | network | unifi | diagnostic | not_enriched |
| `sensor.flo_d4e95ef8775b_link_speed` | telemetry | unifi | data_rate (Mbit/s) | disabled |
| `sensor.flo_shutoff_current_system_mode` | telemetry | flo |  | not_enriched |
| `sensor.flo_shutoff_today_s_water_usage` | telemetry | flo | water (gal) | not_enriched |
| `sensor.flo_shutoff_water_flow_rate` | telemetry | flo | volume_flow_rate (gal/min) | not_enriched |
| `sensor.flo_shutoff_water_pressure` | telemetry | flo | pressure (psi) | not_enriched |
| `sensor.flo_shutoff_water_temperature` | telemetry | flo | temperature (°F) | not_enriched |
| `switch.flo_shutoff_shutoff_valve` | control | flo |  | not_enriched |

#### Mechanical Room

- Device ID: `device_e0835a8f890a`
- Integration: sensorpush_cloud
- Model: SensorPush HT1
- Capability mix: 8 telemetry, 0 control, 0 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `sensor.basement_altitude` | telemetry | sensorpush_cloud | distance (ft) | disabled |
| `sensor.basement_atmospheric_pressure` | telemetry | sensorpush_cloud | atmospheric_pressure (inHg) | disabled |
| `sensor.basement_battery_voltage` | telemetry | sensorpush_cloud | voltage (V) | disabled |
| `sensor.basement_dew_point` | telemetry | sensorpush_cloud | temperature (°F) | disabled |
| `sensor.basement_signal_strength` | telemetry | sensorpush_cloud | signal_strength (dBm) | disabled |
| `sensor.basement_vapor_pressure` | telemetry | sensorpush_cloud | pressure (psi) | disabled |
| `sensor.mechanical_room_humidity` | telemetry | sensorpush_cloud | humidity (%) | not_enriched |
| `sensor.mechanical_room_temperature` | telemetry | sensorpush_cloud | temperature (°F) | not_enriched |

#### Mechanical Room - Leak Detection

- Device ID: `device_875d11919b1c`
- Integration: flo, unifi
- Model: Flo by Moen puck_v1
- Capability mix: 5 telemetry, 0 control, 1 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `binary_sensor.mechanical_room_leak_detection_water_detected` | telemetry | flo | problem | not_enriched |
| `device_tracker.mechanical_room_leak_detection_espressif` | network | unifi | diagnostic | not_enriched |
| `sensor.espressif_link_speed` | telemetry | unifi | data_rate (Mbit/s) | disabled |
| `sensor.mechanical_room_leak_detection_battery` | telemetry | flo | battery (%) | not_enriched |
| `sensor.mechanical_room_leak_detection_humidity` | telemetry | flo | humidity (%) | not_enriched |
| `sensor.mechanical_room_leak_detection_temperature` | telemetry | flo | temperature (°F) | not_enriched |

#### Mechanical room

- Device ID: `device_a21ac907c776`
- Integration: unifi, unifiprotect
- Model: Ubiquiti G6 Instant
- Capability mix: 27 telemetry, 32 control, 1 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `binary_sensor.mechanical_room_animal_detected` | telemetry | unifiprotect |  | not_enriched |
| `binary_sensor.mechanical_room_audio_object_detected` | telemetry | unifiprotect |  | disabled |
| `binary_sensor.mechanical_room_baby_cry_detected` | telemetry | unifiprotect |  | not_enriched |
| `binary_sensor.mechanical_room_barking_detected` | telemetry | unifiprotect |  | not_enriched |
| `binary_sensor.mechanical_room_car_alarm_detected` | telemetry | unifiprotect |  | not_enriched |
| `binary_sensor.mechanical_room_car_horn_detected` | telemetry | unifiprotect |  | not_enriched |
| `binary_sensor.mechanical_room_co_alarm_detected` | telemetry | unifiprotect | carbon_monoxide | not_enriched |
| `binary_sensor.mechanical_room_glass_break_detected` | telemetry | unifiprotect |  | not_enriched |
| `binary_sensor.mechanical_room_is_dark` | telemetry | unifiprotect |  | not_enriched |
| `binary_sensor.mechanical_room_motion` | telemetry | unifiprotect | motion | not_enriched |
| `binary_sensor.mechanical_room_object_detected` | telemetry | unifiprotect |  | disabled |
| `binary_sensor.mechanical_room_person_detected` | telemetry | unifiprotect |  | not_enriched |
| `binary_sensor.mechanical_room_siren_detected` | telemetry | unifiprotect |  | not_enriched |
| `binary_sensor.mechanical_room_smoke_alarm_detected` | telemetry | unifiprotect |  | not_enriched |
| `binary_sensor.mechanical_room_speaking_detected` | telemetry | unifiprotect |  | not_enriched |
| `binary_sensor.mechanical_room_vehicle_detected` | telemetry | unifiprotect |  | not_enriched |
| `button.mechanical_room_restart` | control | unifiprotect | restart | disabled |
| `button.mechanical_room_unadopt_device` | control | unifiprotect |  | disabled |
| `camera.mechanical_room_high_resolution_channel` | telemetry | unifiprotect |  | not_enriched |
| `camera.mechanical_room_high_resolution_channel_insecure` | telemetry | unifiprotect |  | disabled |
| `device_tracker.mechanical_room` | network | unifi | diagnostic | not_enriched |
| `event.mechanical_room_vehicle` | telemetry | unifiprotect |  | not_enriched |
| `media_player.mechanical_room_speaker` | control | unifiprotect | speaker | not_enriched |
| `number.mechanical_room_infrared_custom_lux_trigger` | control | unifiprotect | config | not_enriched |
| `number.mechanical_room_microphone_level` | control | unifiprotect | config (%) | not_enriched |
| `number.mechanical_room_system_sounds_volume` | control | unifiprotect | config (%) | not_enriched |
| `select.mechanical_room_hdr_mode` | control | unifiprotect | config | not_enriched |
| `select.mechanical_room_infrared_mode` | control | unifiprotect | config | not_enriched |
| `select.mechanical_room_recording_mode` | control | unifiprotect | config | not_enriched |
| `sensor.mechanical_room_disk_write_rate` | telemetry | unifiprotect | data_rate (MB/s) | not_enriched |
| `sensor.mechanical_room_last_motion_detected` | telemetry | unifiprotect | timestamp | disabled |
| `sensor.mechanical_room_oldest_recording` | telemetry | unifiprotect | timestamp | disabled |
| `sensor.mechanical_room_received_data` | telemetry | unifiprotect | data_size (MB) | disabled |
| `sensor.mechanical_room_storage_used` | telemetry | unifiprotect | data_size (MB) | not_enriched |
| `sensor.mechanical_room_transferred_data` | telemetry | unifiprotect | data_size (MB) | disabled |
| `sensor.mechanical_room_uptime` | telemetry | unifiprotect | timestamp | disabled |
| `sensor.mechanical_room_wi_fi_signal_strength` | telemetry | unifiprotect | signal_strength (dBm) | disabled |
| `switch.mechanical_room_animal_detection` | control | unifiprotect | config | not_enriched |
| `switch.mechanical_room_baby_cry_detection` | control | unifiprotect | config | not_enriched |
| `switch.mechanical_room_car_alarm_detection` | control | unifiprotect | config | not_enriched |
| `switch.mechanical_room_car_horn_detection` | control | unifiprotect | config | not_enriched |
| `switch.mechanical_room_co_alarm_detection` | control | unifiprotect | config | not_enriched |
| `switch.mechanical_room_glass_break_detection` | control | unifiprotect | config | not_enriched |
| `switch.mechanical_room_hdr_mode` | control | unifiprotect | config | disabled |
| `switch.mechanical_room_license_plate_detection` | control | unifiprotect | config | not_enriched |
| `switch.mechanical_room_motion` | control | unifiprotect | config | not_enriched |
| `switch.mechanical_room_none` | control | unifiprotect | config | not_enriched |
| `switch.mechanical_room_overlay_show_date` | control | unifiprotect | config | not_enriched |
| `switch.mechanical_room_overlay_show_logo` | control | unifiprotect | config | not_enriched |
| `switch.mechanical_room_overlay_show_name` | control | unifiprotect | config | not_enriched |
| `switch.mechanical_room_overlay_show_nerd_mode` | control | unifiprotect | config | not_enriched |
| `switch.mechanical_room_person_detection` | control | unifiprotect | config | not_enriched |
| `switch.mechanical_room_privacy_mode` | control | unifiprotect | config | not_enriched |
| `switch.mechanical_room_siren_detection` | control | unifiprotect | config | not_enriched |
| `switch.mechanical_room_smoke_detection` | control | unifiprotect | config | not_enriched |
| `switch.mechanical_room_speaking_detection` | control | unifiprotect | config | not_enriched |
| `switch.mechanical_room_ssh_enabled` | control | unifiprotect | config | disabled |
| `switch.mechanical_room_status_light` | control | unifiprotect | config | not_enriched |
| `switch.mechanical_room_system_sounds` | control | unifiprotect | config | not_enriched |
| `switch.mechanical_room_vehicle_detection` | control | unifiprotect | config | not_enriched |

### Mudroom

#### Back Stairs

- Device ID: `device_db65d45d11cd`
- Integration: ring
- Model: Ring Stick Up Cam (3rd Gen)
- Capability mix: 6 telemetry, 3 control, 0 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `camera.back_stairs_live_view` | telemetry | ring |  | not_enriched |
| `event.back_stairs_motion` | telemetry | ring | motion | not_enriched |
| `number.back_stairs_volume` | control | ring |  | not_enriched |
| `sensor.back_stairs_battery` | telemetry | ring | battery (%) | not_enriched |
| `sensor.back_stairs_last_activity` | telemetry | ring | timestamp | not_enriched |
| `sensor.back_stairs_signal_strength` | telemetry | ring | signal_strength (dBm) | disabled |
| `sensor.back_stairs_wi_fi_signal_category` | telemetry | ring | diagnostic | disabled |
| `siren.back_stairs_siren` | control | ring |  | not_enriched |
| `switch.back_stairs_motion_detection` | control | ring |  | not_enriched |

#### Laundry Sink - Leak Detection

- Device ID: `device_6f358bbfc961`
- Integration: flo, unifi
- Model: Flo by Moen puck_v1
- Capability mix: 5 telemetry, 0 control, 1 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `binary_sensor.laundry_sink_leak_detection_water_detected` | telemetry | flo | problem | not_enriched |
| `device_tracker.laundry_sink_leak_detection_espressif` | network | unifi | diagnostic | not_enriched |
| `sensor.espressif_link_speed_4` | telemetry | unifi | data_rate (Mbit/s) | disabled |
| `sensor.laundry_sink_leak_detection_battery` | telemetry | flo | battery (%) | not_enriched |
| `sensor.laundry_sink_leak_detection_humidity` | telemetry | flo | humidity (%) | not_enriched |
| `sensor.laundry_sink_leak_detection_temperature` | telemetry | flo | temperature (°F) | not_enriched |

#### Mud room

- Device ID: `device_e5236ec8767c`
- Integration: unifi, unifiprotect
- Model: Ubiquiti G6 Instant
- Capability mix: 27 telemetry, 32 control, 1 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `binary_sensor.mud_room_animal_detected` | telemetry | unifiprotect |  | not_enriched |
| `binary_sensor.mud_room_audio_object_detected` | telemetry | unifiprotect |  | disabled |
| `binary_sensor.mud_room_baby_cry_detected` | telemetry | unifiprotect |  | not_enriched |
| `binary_sensor.mud_room_barking_detected` | telemetry | unifiprotect |  | not_enriched |
| `binary_sensor.mud_room_car_alarm_detected` | telemetry | unifiprotect |  | not_enriched |
| `binary_sensor.mud_room_car_horn_detected` | telemetry | unifiprotect |  | not_enriched |
| `binary_sensor.mud_room_co_alarm_detected` | telemetry | unifiprotect | carbon_monoxide | not_enriched |
| `binary_sensor.mud_room_glass_break_detected` | telemetry | unifiprotect |  | not_enriched |
| `binary_sensor.mud_room_is_dark` | telemetry | unifiprotect |  | not_enriched |
| `binary_sensor.mud_room_motion` | telemetry | unifiprotect | motion | not_enriched |
| `binary_sensor.mud_room_object_detected` | telemetry | unifiprotect |  | disabled |
| `binary_sensor.mud_room_person_detected` | telemetry | unifiprotect |  | not_enriched |
| `binary_sensor.mud_room_siren_detected` | telemetry | unifiprotect |  | not_enriched |
| `binary_sensor.mud_room_smoke_alarm_detected` | telemetry | unifiprotect |  | not_enriched |
| `binary_sensor.mud_room_speaking_detected` | telemetry | unifiprotect |  | not_enriched |
| `binary_sensor.mud_room_vehicle_detected` | telemetry | unifiprotect |  | not_enriched |
| `button.mud_room_restart` | control | unifiprotect | restart | disabled |
| `button.mud_room_unadopt_device` | control | unifiprotect |  | disabled |
| `camera.mud_room_high_resolution_channel` | telemetry | unifiprotect |  | not_enriched |
| `camera.mud_room_high_resolution_channel_insecure` | telemetry | unifiprotect |  | disabled |
| `device_tracker.mud_room` | network | unifi | diagnostic | not_enriched |
| `event.mud_room_vehicle` | telemetry | unifiprotect |  | not_enriched |
| `media_player.mud_room_speaker` | control | unifiprotect | speaker | not_enriched |
| `number.mud_room_infrared_custom_lux_trigger` | control | unifiprotect | config | not_enriched |
| `number.mud_room_microphone_level` | control | unifiprotect | config (%) | not_enriched |
| `number.mud_room_system_sounds_volume` | control | unifiprotect | config (%) | not_enriched |
| `select.mud_room_hdr_mode` | control | unifiprotect | config | not_enriched |
| `select.mud_room_infrared_mode` | control | unifiprotect | config | not_enriched |
| `select.mud_room_recording_mode` | control | unifiprotect | config | not_enriched |
| `sensor.mud_room_disk_write_rate` | telemetry | unifiprotect | data_rate (MB/s) | not_enriched |
| `sensor.mud_room_last_motion_detected` | telemetry | unifiprotect | timestamp | disabled |
| `sensor.mud_room_oldest_recording` | telemetry | unifiprotect | timestamp | disabled |
| `sensor.mud_room_received_data` | telemetry | unifiprotect | data_size (MB) | disabled |
| `sensor.mud_room_storage_used` | telemetry | unifiprotect | data_size (MB) | not_enriched |
| `sensor.mud_room_transferred_data` | telemetry | unifiprotect | data_size (MB) | disabled |
| `sensor.mud_room_uptime` | telemetry | unifiprotect | timestamp | disabled |
| `sensor.mud_room_wi_fi_signal_strength` | telemetry | unifiprotect | signal_strength (dBm) | disabled |
| `switch.mud_room_animal_detection` | control | unifiprotect | config | not_enriched |
| `switch.mud_room_baby_cry_detection` | control | unifiprotect | config | not_enriched |
| `switch.mud_room_car_alarm_detection` | control | unifiprotect | config | not_enriched |
| `switch.mud_room_car_horn_detection` | control | unifiprotect | config | not_enriched |
| `switch.mud_room_co_alarm_detection` | control | unifiprotect | config | not_enriched |
| `switch.mud_room_glass_break_detection` | control | unifiprotect | config | not_enriched |
| `switch.mud_room_hdr_mode` | control | unifiprotect | config | disabled |
| `switch.mud_room_license_plate_detection` | control | unifiprotect | config | not_enriched |
| `switch.mud_room_motion` | control | unifiprotect | config | not_enriched |
| `switch.mud_room_none` | control | unifiprotect | config | not_enriched |
| `switch.mud_room_overlay_show_date` | control | unifiprotect | config | not_enriched |
| `switch.mud_room_overlay_show_logo` | control | unifiprotect | config | not_enriched |
| `switch.mud_room_overlay_show_name` | control | unifiprotect | config | not_enriched |
| `switch.mud_room_overlay_show_nerd_mode` | control | unifiprotect | config | not_enriched |
| `switch.mud_room_person_detection` | control | unifiprotect | config | not_enriched |
| `switch.mud_room_privacy_mode` | control | unifiprotect | config | not_enriched |
| `switch.mud_room_siren_detection` | control | unifiprotect | config | not_enriched |
| `switch.mud_room_smoke_detection` | control | unifiprotect | config | not_enriched |
| `switch.mud_room_speaking_detection` | control | unifiprotect | config | not_enriched |
| `switch.mud_room_ssh_enabled` | control | unifiprotect | config | disabled |
| `switch.mud_room_status_light` | control | unifiprotect | config | not_enriched |
| `switch.mud_room_system_sounds` | control | unifiprotect | config | not_enriched |
| `switch.mud_room_vehicle_detection` | control | unifiprotect | config | not_enriched |

#### Mudroom Door

- Device ID: `device_ece30c1a6455`
- Integration: ring
- Model: Ring Doorbell Pro 2
- Capability mix: 7 telemetry, 3 control, 0 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `camera.mudroom_door_live_view` | telemetry | ring |  | not_enriched |
| `event.mudroom_door_ding` | telemetry | ring | doorbell | not_enriched |
| `event.mudroom_door_motion` | telemetry | ring | motion | not_enriched |
| `number.mudroom_door_volume` | control | ring |  | not_enriched |
| `sensor.mudroom_door_battery` | telemetry | ring | battery (%) | not_enriched |
| `sensor.mudroom_door_last_activity` | telemetry | ring | timestamp | not_enriched |
| `sensor.mudroom_door_signal_strength` | telemetry | ring | signal_strength (dBm) | disabled |
| `sensor.mudroom_door_wi_fi_signal_category` | telemetry | ring | diagnostic | disabled |
| `switch.mudroom_door_in_home_chime` | control | ring |  | not_enriched |
| `switch.mudroom_door_motion_detection` | control | ring |  | not_enriched |

#### Washing Machine - Leak Detection

- Device ID: `device_e9cb048d7124`
- Integration: flo, unifi
- Model: Flo by Moen puck_v1
- Capability mix: 5 telemetry, 0 control, 1 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `binary_sensor.washing_machine_leak_detection_water_detected` | telemetry | flo | problem | not_enriched |
| `device_tracker.washing_machine_leak_detection_espressif` | network | unifi | diagnostic | not_enriched |
| `sensor.espressif_link_speed_6` | telemetry | unifi | data_rate (Mbit/s) | disabled |
| `sensor.washing_machine_leak_detection_battery` | telemetry | flo | battery (%) | not_enriched |
| `sensor.washing_machine_leak_detection_humidity` | telemetry | flo | humidity (%) | not_enriched |
| `sensor.washing_machine_leak_detection_temperature` | telemetry | flo | temperature (°F) | not_enriched |

### Office

#### Office TV

- Device ID: `device_a76f54877bef`
- Integration: apple_tv
- Model: Apple Apple TV 4K
- Capability mix: 0 telemetry, 2 control, 0 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `media_player.office_tv` | control | apple_tv |  | not_enriched |
| `remote.office_tv` | control | apple_tv |  | not_enriched |

### Stairs

#### Stairs Front Stairs

- Device ID: `device_eb14b692d03a`
- Integration: lutron_caseta
- Model: Lutron Electronics Co., Inc DVRF-6L (DivaSmartDimmer)
- Capability mix: 0 telemetry, 1 control, 0 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `light.stairs_front_stairs` | control | lutron_caseta |  | not_enriched |

### Unassigned

#### Apple TV (Family Room)

- Device ID: `device_58f8e7ee4387`
- Integration: unifi
- Model: Apple, Inc.
- Capability mix: 1 telemetry, 0 control, 1 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `device_tracker.apple_tv_family_room` | network | unifi | diagnostic | not_enriched |
| `sensor.apple_tv_family_room_link_speed` | telemetry | unifi | data_rate (Mbit/s) | disabled |

#### Aqara Hub M100

- Device ID: `device_a735aed44232`
- Integration: matter
- Model: Aqara Aqara Hub M100
- Capability mix: 0 telemetry, 1 control, 0 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `button.aqara_hub_m100_identify` | control | matter | identify | not_enriched |

#### Aqara Smart Lock U100

- Device ID: `device_96ee54efd30b`
- Integration: matter
- Model: Aqara Aqara Smart Lock U100
- Capability mix: 3 telemetry, 3 control, 0 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `button.aqara_smart_lock_u100_identify` | control | matter | identify | not_enriched |
| `lock.aqara_smart_lock_u100` | control | matter |  | not_enriched |
| `select.aqara_smart_lock_u100_operating_mode` | control | matter |  | not_enriched |
| `sensor.aqara_smart_lock_u100_battery` | telemetry | matter | battery (%) | not_enriched |
| `sensor.aqara_smart_lock_u100_battery_type` | telemetry | matter | diagnostic | not_enriched |
| `sensor.aqara_smart_lock_u100_battery_voltage` | telemetry | matter | voltage (V) | not_enriched |

#### BRW849E567C91BC

- Device ID: `device_faba3c044d32`
- Integration: unifi
- Model: unknown model
- Capability mix: 1 telemetry, 0 control, 1 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `device_tracker.brw849e567c91bc` | network | unifi | diagnostic | not_enriched |
| `sensor.brw849e567c91bc_link_speed` | telemetry | unifi | data_rate (Mbit/s) | disabled |

#### Back Yard

- Device ID: `device_1557543cefbd`
- Integration: unifi, unifiprotect
- Model: Ubiquiti G6 Instant
- Capability mix: 26 telemetry, 33 control, 1 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `binary_sensor.back_yard_animal_detected` | telemetry | unifiprotect |  | not_enriched |
| `binary_sensor.back_yard_audio_object_detected` | telemetry | unifiprotect |  | disabled |
| `binary_sensor.back_yard_baby_cry_detected` | telemetry | unifiprotect |  | not_enriched |
| `binary_sensor.back_yard_barking_detected` | telemetry | unifiprotect |  | not_enriched |
| `binary_sensor.back_yard_car_alarm_detected` | telemetry | unifiprotect |  | not_enriched |
| `binary_sensor.back_yard_car_horn_detected` | telemetry | unifiprotect |  | not_enriched |
| `binary_sensor.back_yard_co_alarm_detected` | telemetry | unifiprotect | carbon_monoxide | not_enriched |
| `binary_sensor.back_yard_glass_break_detected` | telemetry | unifiprotect |  | not_enriched |
| `binary_sensor.back_yard_object_detected` | telemetry | unifiprotect |  | disabled |
| `binary_sensor.back_yard_person_detected` | telemetry | unifiprotect |  | not_enriched |
| `binary_sensor.back_yard_siren_detected` | telemetry | unifiprotect |  | not_enriched |
| `binary_sensor.back_yard_smoke_alarm_detected` | telemetry | unifiprotect |  | not_enriched |
| `binary_sensor.back_yard_speaking_detected` | telemetry | unifiprotect |  | not_enriched |
| `binary_sensor.back_yard_vehicle_detected` | telemetry | unifiprotect |  | not_enriched |
| `binary_sensor.g6_instant_is_dark_2` | telemetry | unifiprotect |  | not_enriched |
| `binary_sensor.g6_instant_motion_2` | telemetry | unifiprotect | motion | not_enriched |
| `button.g6_instant_restart_2` | control | unifiprotect | restart | disabled |
| `button.g6_instant_unadopt_device_2` | control | unifiprotect |  | disabled |
| `camera.g6_instant_high_resolution_channel_2` | telemetry | unifiprotect |  | not_enriched |
| `device_tracker.uvc_g6_instant_2` | network | unifi | diagnostic | not_enriched |
| `event.back_yard_vehicle` | telemetry | unifiprotect |  | not_enriched |
| `media_player.back_yard_speaker` | control | unifiprotect | speaker | not_enriched |
| `number.back_yard_infrared_custom_lux_trigger` | control | unifiprotect | config | not_enriched |
| `number.back_yard_microphone_level` | control | unifiprotect | config (%) | not_enriched |
| `number.back_yard_system_sounds_volume` | control | unifiprotect | config (%) | not_enriched |
| `number.g6_instant_wide_dynamic_range_2` | control | unifiprotect | config | not_enriched |
| `select.back_yard_hdr_mode` | control | unifiprotect | config | not_enriched |
| `select.back_yard_infrared_mode` | control | unifiprotect | config | not_enriched |
| `select.g6_instant_recording_mode_2` | control | unifiprotect | config | not_enriched |
| `sensor.g6_instant_disk_write_rate_2` | telemetry | unifiprotect | data_rate (MB/s) | not_enriched |
| `sensor.g6_instant_last_motion_detected_2` | telemetry | unifiprotect | timestamp | disabled |
| `sensor.g6_instant_link_speed` | telemetry | unifi | data_rate (Mbit/s) | disabled |
| `sensor.g6_instant_oldest_recording_2` | telemetry | unifiprotect | timestamp | disabled |
| `sensor.g6_instant_received_data_2` | telemetry | unifiprotect | data_size (MB) | disabled |
| `sensor.g6_instant_storage_used_2` | telemetry | unifiprotect | data_size (MB) | not_enriched |
| `sensor.g6_instant_transferred_data_2` | telemetry | unifiprotect | data_size (MB) | disabled |
| `sensor.g6_instant_uptime_2` | telemetry | unifiprotect | timestamp | disabled |
| `switch.back_yard_animal_detection` | control | unifiprotect | config | not_enriched |
| `switch.back_yard_baby_cry_detection` | control | unifiprotect | config | not_enriched |
| `switch.back_yard_car_alarm_detection` | control | unifiprotect | config | not_enriched |
| `switch.back_yard_car_horn_detection` | control | unifiprotect | config | not_enriched |
| `switch.back_yard_co_alarm_detection` | control | unifiprotect | config | not_enriched |
| `switch.back_yard_glass_break_detection` | control | unifiprotect | config | not_enriched |
| `switch.back_yard_hdr_mode` | control | unifiprotect | config | disabled |
| `switch.back_yard_license_plate_detection` | control | unifiprotect | config | not_enriched |
| `switch.back_yard_none` | control | unifiprotect | config | not_enriched |
| `switch.back_yard_person_detection` | control | unifiprotect | config | not_enriched |
| `switch.back_yard_privacy_mode` | control | unifiprotect | config | not_enriched |
| `switch.back_yard_siren_detection` | control | unifiprotect | config | not_enriched |
| `switch.back_yard_smoke_detection` | control | unifiprotect | config | not_enriched |
| `switch.back_yard_speaking_detection` | control | unifiprotect | config | not_enriched |
| `switch.back_yard_status_light` | control | unifiprotect | config | not_enriched |
| `switch.back_yard_system_sounds` | control | unifiprotect | config | not_enriched |
| `switch.back_yard_vehicle_detection` | control | unifiprotect | config | not_enriched |
| `switch.g6_instant_motion_2` | control | unifiprotect | config | not_enriched |
| `switch.g6_instant_overlay_show_date_2` | control | unifiprotect | config | not_enriched |
| `switch.g6_instant_overlay_show_logo_2` | control | unifiprotect | config | not_enriched |
| `switch.g6_instant_overlay_show_name_2` | control | unifiprotect | config | not_enriched |
| `switch.g6_instant_overlay_show_nerd_mode_2` | control | unifiprotect | config | not_enriched |
| `switch.g6_instant_ssh_enabled_2` | control | unifiprotect | config | disabled |

#### Backup

- Device ID: `device_aa77864d8f2c`
- Integration: backup
- Model: Home Assistant Home Assistant Backup
- Capability mix: 5 telemetry, 0 control, 0 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `event.backup_automatic_backup` | telemetry | backup |  | not_enriched |
| `sensor.backup_backup_manager_state` | telemetry | backup | enum | not_enriched |
| `sensor.backup_last_attempted_automatic_backup` | telemetry | backup | timestamp | not_enriched |
| `sensor.backup_last_successful_automatic_backup` | telemetry | backup | timestamp | not_enriched |
| `sensor.backup_next_scheduled_automatic_backup` | telemetry | backup | timestamp | not_enriched |

#### Basement TV

- Device ID: `device_726950982dc7`
- Integration: cast
- Model: Sony BRAVIA 4K VH21
- Capability mix: 0 telemetry, 1 control, 0 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `media_player.basement_tv` | control | cast |  | not_enriched |

#### Bonticou

- Device ID: `device_af91ab644a46`
- Integration: unifi
- Model: Ubiquiti Networks UniFi WLAN
- Capability mix: 2 telemetry, 2 control, 0 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `button.bonticou_regenerate_password` | control | unifi | update | disabled |
| `image.bonticou_qr_code` | telemetry | unifi | diagnostic | disabled |
| `sensor.bonticou` | telemetry | unifi | diagnostic | not_enriched |
| `switch.bonticou` | control | unifi | switch | not_enriched |

#### Bonticou Guest

- Device ID: `device_92a17863a365`
- Integration: unifi
- Model: Ubiquiti Networks UniFi WLAN
- Capability mix: 2 telemetry, 2 control, 0 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `button.bonticou_guest_regenerate_password` | control | unifi | update | disabled |
| `image.bonticou_guest_qr_code` | telemetry | unifi | diagnostic | disabled |
| `sensor.bonticou_guest` | telemetry | unifi | diagnostic | not_enriched |
| `switch.bonticou_guest` | control | unifi | switch | not_enriched |

#### DB15

- Device ID: `device_3d305b654446`
- Integration: unifi
- Model: Apple, Inc.
- Capability mix: 1 telemetry, 0 control, 1 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `device_tracker.db15` | network | unifi | diagnostic | not_enriched |
| `sensor.db15_link_speed` | telemetry | unifi | data_rate (Mbit/s) | disabled |

#### Family Room TV

- Device ID: `device_585364ba9de2`
- Integration: cast
- Model: VIZIO PQ65-F1
- Capability mix: 0 telemetry, 1 control, 0 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `media_player.family_room_tv` | control | cast |  | not_enriched |

#### File editor

- Device ID: `device_3245b94dd2f1`
- Integration: hassio
- Model: Official apps Home Assistant Add-on
- Capability mix: 6 telemetry, 1 control, 0 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `binary_sensor.file_editor_running` | telemetry | hassio | running | disabled |
| `sensor.file_editor_cpu_percent` | telemetry | hassio | % | disabled |
| `sensor.file_editor_memory_percent` | telemetry | hassio | % | disabled |
| `sensor.file_editor_newest_version` | telemetry | hassio |  | disabled |
| `sensor.file_editor_version` | telemetry | hassio |  | disabled |
| `switch.file_editor` | control | hassio |  | disabled |
| `update.file_editor_update` | telemetry | hassio | config | not_enriched |

#### Fios-VHTx3

- Device ID: `device_0a258d606684`
- Integration: unifi
- Model: Ubiquiti Networks UniFi WLAN
- Capability mix: 2 telemetry, 2 control, 0 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `button.fios_vhtx3_regenerate_password` | control | unifi | update | disabled |
| `image.fios_vhtx3_qr_code` | telemetry | unifi | diagnostic | disabled |
| `sensor.fios_vhtx3` | telemetry | unifi | diagnostic | not_enriched |
| `switch.fios_vhtx3` | control | unifi | switch | not_enriched |

#### Forecast

- Device ID: `device_9d764b6dff21`
- Integration: met
- Model: Met.no Forecast
- Capability mix: 1 telemetry, 0 control, 0 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `weather.forecast_home` | telemetry | met |  | not_enriched |

#### Galaxy-S24-Ultra

- Device ID: `device_66bf3c0457ee`
- Integration: unifi
- Model: unknown model
- Capability mix: 1 telemetry, 0 control, 1 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `device_tracker.galaxy_s24_ultra` | network | unifi | diagnostic | not_enriched |
| `sensor.galaxy_s24_ultra_link_speed` | telemetry | unifi | data_rate (Mbit/s) | disabled |

#### HACS

- Device ID: `device_c96e7314041e`
- Integration: hacs
- Model: hacs.xyz
- Capability mix: 1 telemetry, 1 control, 0 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `switch.hacs_pre_release` | control | hacs | diagnostic | disabled |
| `update.hacs_update` | telemetry | hacs | config | not_enriched |

#### Home Assistant

- Device ID: `device_32c099f4c862`
- Integration: unifi
- Model: Nabu Casa, Inc.
- Capability mix: 1 telemetry, 0 control, 1 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `device_tracker.home_assistant` | network | unifi | diagnostic | not_enriched |
| `sensor.home_assistant_link_speed` | telemetry | unifi | data_rate (Mbit/s) | disabled |

#### Home Assistant Core

- Device ID: `device_27a1401e8e43`
- Integration: hassio
- Model: Home Assistant Home Assistant Core
- Capability mix: 3 telemetry, 0 control, 0 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `sensor.home_assistant_core_cpu_percent` | telemetry | hassio | % | disabled |
| `sensor.home_assistant_core_memory_percent` | telemetry | hassio | % | disabled |
| `update.home_assistant_core_update` | telemetry | hassio | config | not_enriched |

#### Home Assistant Host

- Device ID: `device_d557496dfd6d`
- Integration: hassio
- Model: Home Assistant Home Assistant Host
- Capability mix: 5 telemetry, 0 control, 0 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `sensor.home_assistant_host_apparmor_version` | telemetry | hassio | diagnostic | disabled |
| `sensor.home_assistant_host_disk_free` | telemetry | hassio | data_size (GB) | disabled |
| `sensor.home_assistant_host_disk_total` | telemetry | hassio | data_size (GB) | disabled |
| `sensor.home_assistant_host_disk_used` | telemetry | hassio | data_size (GB) | disabled |
| `sensor.home_assistant_host_os_agent_version` | telemetry | hassio | diagnostic | disabled |

#### Home Assistant Operating System

- Device ID: `device_5998ed5c3bcd`
- Integration: hassio
- Model: Home Assistant Home Assistant Operating System
- Capability mix: 3 telemetry, 0 control, 0 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `sensor.home_assistant_operating_system_newest_version` | telemetry | hassio |  | disabled |
| `sensor.home_assistant_operating_system_version` | telemetry | hassio |  | disabled |
| `update.home_assistant_operating_system_update` | telemetry | hassio | config | not_enriched |

#### Home Assistant Supervisor

- Device ID: `device_ee501121995a`
- Integration: hassio
- Model: Home Assistant Home Assistant Supervisor
- Capability mix: 3 telemetry, 0 control, 0 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `sensor.home_assistant_supervisor_cpu_percent` | telemetry | hassio | % | disabled |
| `sensor.home_assistant_supervisor_memory_percent` | telemetry | hassio | % | disabled |
| `update.home_assistant_supervisor_update` | telemetry | hassio | config | not_enriched |

#### Lutron-06926f09

- Device ID: `device_d047070a23cf`
- Integration: unifi
- Model: Lutron Electronics Co., Inc.
- Capability mix: 1 telemetry, 0 control, 1 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `device_tracker.lutron_06926f09` | network | unifi | diagnostic | not_enriched |
| `sensor.lutron_06926f09_link_speed` | telemetry | unifi | data_rate (Mbit/s) | disabled |

#### Master Bedroom

- Device ID: `device_92d8071e504b`
- Integration: sensorpush_cloud
- Model: SensorPush HT1
- Capability mix: 8 telemetry, 0 control, 0 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `sensor.master_altitude` | telemetry | sensorpush_cloud | distance (ft) | disabled |
| `sensor.master_atmospheric_pressure` | telemetry | sensorpush_cloud | atmospheric_pressure (inHg) | disabled |
| `sensor.master_battery_voltage` | telemetry | sensorpush_cloud | voltage (V) | disabled |
| `sensor.master_dew_point` | telemetry | sensorpush_cloud | temperature (°F) | disabled |
| `sensor.master_humidity` | telemetry | sensorpush_cloud | humidity (%) | not_enriched |
| `sensor.master_signal_strength` | telemetry | sensorpush_cloud | signal_strength (dBm) | disabled |
| `sensor.master_temperature` | telemetry | sensorpush_cloud | temperature (°F) | not_enriched |
| `sensor.master_vapor_pressure` | telemetry | sensorpush_cloud | pressure (psi) | disabled |

#### Matter Server

- Device ID: `device_c137b2ed9eba`
- Integration: hassio
- Model: Official apps Home Assistant Add-on
- Capability mix: 6 telemetry, 1 control, 0 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `binary_sensor.matter_server_running` | telemetry | hassio | running | disabled |
| `sensor.matter_server_cpu_percent` | telemetry | hassio | % | disabled |
| `sensor.matter_server_memory_percent` | telemetry | hassio | % | disabled |
| `sensor.matter_server_newest_version` | telemetry | hassio |  | disabled |
| `sensor.matter_server_version` | telemetry | hassio |  | disabled |
| `switch.matter_server` | control | hassio |  | disabled |
| `update.matter_server_update` | telemetry | hassio | config | not_enriched |

#### Mini Media Player

- Device ID: `device_ee47223930dd`
- Integration: hacs
- Model: kalkih plugin
- Capability mix: 1 telemetry, 1 control, 0 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `switch.mini_media_player_pre_release` | control | hacs | diagnostic | disabled |
| `update.mini_media_player_update` | telemetry | hacs | config | not_enriched |

#### Mushroom

- Device ID: `device_95e8ee1b21c9`
- Integration: hacs
- Model: piitaya plugin
- Capability mix: 1 telemetry, 1 control, 0 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `switch.mushroom_pre_release` | control | hacs | diagnostic | disabled |
| `update.mushroom_update` | telemetry | hacs | config | not_enriched |

#### Play Room

- Device ID: `device_5a7bbc9548a4`
- Integration: unifi, unifiprotect
- Model: Ubiquiti G6 Instant
- Capability mix: 26 telemetry, 33 control, 1 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `binary_sensor.g6_instant_is_dark` | telemetry | unifiprotect |  | not_enriched |
| `binary_sensor.g6_instant_motion` | telemetry | unifiprotect | motion | not_enriched |
| `binary_sensor.play_room_animal_detected` | telemetry | unifiprotect |  | not_enriched |
| `binary_sensor.play_room_audio_object_detected` | telemetry | unifiprotect |  | disabled |
| `binary_sensor.play_room_baby_cry_detected` | telemetry | unifiprotect |  | not_enriched |
| `binary_sensor.play_room_barking_detected` | telemetry | unifiprotect |  | not_enriched |
| `binary_sensor.play_room_car_alarm_detected` | telemetry | unifiprotect |  | not_enriched |
| `binary_sensor.play_room_car_horn_detected` | telemetry | unifiprotect |  | not_enriched |
| `binary_sensor.play_room_co_alarm_detected` | telemetry | unifiprotect | carbon_monoxide | not_enriched |
| `binary_sensor.play_room_glass_break_detected` | telemetry | unifiprotect |  | not_enriched |
| `binary_sensor.play_room_object_detected` | telemetry | unifiprotect |  | disabled |
| `binary_sensor.play_room_person_detected` | telemetry | unifiprotect |  | not_enriched |
| `binary_sensor.play_room_siren_detected` | telemetry | unifiprotect |  | not_enriched |
| `binary_sensor.play_room_smoke_alarm_detected` | telemetry | unifiprotect |  | not_enriched |
| `binary_sensor.play_room_speaking_detected` | telemetry | unifiprotect |  | not_enriched |
| `binary_sensor.play_room_vehicle_detected` | telemetry | unifiprotect |  | not_enriched |
| `button.g6_instant_restart` | control | unifiprotect | restart | disabled |
| `button.g6_instant_unadopt_device` | control | unifiprotect |  | disabled |
| `camera.g6_instant_high_resolution_channel` | telemetry | unifiprotect |  | not_enriched |
| `device_tracker.uvc_g6_instant` | network | unifi | diagnostic | not_enriched |
| `event.play_room_vehicle` | telemetry | unifiprotect |  | not_enriched |
| `media_player.play_room_speaker` | control | unifiprotect | speaker | not_enriched |
| `number.g6_instant_wide_dynamic_range` | control | unifiprotect | config | not_enriched |
| `number.play_room_infrared_custom_lux_trigger` | control | unifiprotect | config | not_enriched |
| `number.play_room_microphone_level` | control | unifiprotect | config (%) | not_enriched |
| `number.play_room_system_sounds_volume` | control | unifiprotect | config (%) | not_enriched |
| `select.g6_instant_recording_mode` | control | unifiprotect | config | not_enriched |
| `select.play_room_hdr_mode` | control | unifiprotect | config | not_enriched |
| `select.play_room_infrared_mode` | control | unifiprotect | config | not_enriched |
| `sensor.g6_instant_disk_write_rate` | telemetry | unifiprotect | data_rate (MB/s) | not_enriched |
| `sensor.g6_instant_last_motion_detected` | telemetry | unifiprotect | timestamp | disabled |
| `sensor.g6_instant_oldest_recording` | telemetry | unifiprotect | timestamp | disabled |
| `sensor.g6_instant_received_data` | telemetry | unifiprotect | data_size (MB) | disabled |
| `sensor.g6_instant_storage_used` | telemetry | unifiprotect | data_size (MB) | not_enriched |
| `sensor.g6_instant_transferred_data` | telemetry | unifiprotect | data_size (MB) | disabled |
| `sensor.g6_instant_uptime` | telemetry | unifiprotect | timestamp | disabled |
| `sensor.play_room_wi_fi_signal_strength` | telemetry | unifiprotect | signal_strength (dBm) | disabled |
| `switch.g6_instant_motion` | control | unifiprotect | config | not_enriched |
| `switch.g6_instant_overlay_show_date` | control | unifiprotect | config | not_enriched |
| `switch.g6_instant_overlay_show_logo` | control | unifiprotect | config | not_enriched |
| `switch.g6_instant_overlay_show_name` | control | unifiprotect | config | not_enriched |
| `switch.g6_instant_overlay_show_nerd_mode` | control | unifiprotect | config | not_enriched |
| `switch.g6_instant_ssh_enabled` | control | unifiprotect | config | disabled |
| `switch.play_room_animal_detection` | control | unifiprotect | config | not_enriched |
| `switch.play_room_baby_cry_detection` | control | unifiprotect | config | not_enriched |
| `switch.play_room_car_alarm_detection` | control | unifiprotect | config | not_enriched |
| `switch.play_room_car_horn_detection` | control | unifiprotect | config | not_enriched |
| `switch.play_room_co_alarm_detection` | control | unifiprotect | config | not_enriched |
| `switch.play_room_glass_break_detection` | control | unifiprotect | config | not_enriched |
| `switch.play_room_hdr_mode` | control | unifiprotect | config | disabled |
| `switch.play_room_license_plate_detection` | control | unifiprotect | config | not_enriched |
| `switch.play_room_none` | control | unifiprotect | config | not_enriched |
| `switch.play_room_person_detection` | control | unifiprotect | config | not_enriched |
| `switch.play_room_privacy_mode` | control | unifiprotect | config | not_enriched |
| `switch.play_room_siren_detection` | control | unifiprotect | config | not_enriched |
| `switch.play_room_smoke_detection` | control | unifiprotect | config | not_enriched |
| `switch.play_room_speaking_detection` | control | unifiprotect | config | not_enriched |
| `switch.play_room_status_light` | control | unifiprotect | config | not_enriched |
| `switch.play_room_system_sounds` | control | unifiprotect | config | not_enriched |
| `switch.play_room_vehicle_detection` | control | unifiprotect | config | not_enriched |

#### Serving Fridge

- Device ID: `device_1b1cd5daf7c5`
- Integration: sensorpush_cloud
- Model: SensorPush HT1
- Capability mix: 8 telemetry, 0 control, 0 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `sensor.sake_new_altitude` | telemetry | sensorpush_cloud | distance (ft) | disabled |
| `sensor.sake_new_atmospheric_pressure` | telemetry | sensorpush_cloud | atmospheric_pressure (inHg) | disabled |
| `sensor.sake_new_battery_voltage` | telemetry | sensorpush_cloud | voltage (V) | disabled |
| `sensor.sake_new_dew_point` | telemetry | sensorpush_cloud | temperature (°F) | disabled |
| `sensor.sake_new_humidity` | telemetry | sensorpush_cloud | humidity (%) | not_enriched |
| `sensor.sake_new_signal_strength` | telemetry | sensorpush_cloud | signal_strength (dBm) | disabled |
| `sensor.sake_new_temperature` | telemetry | sensorpush_cloud | temperature (°F) | not_enriched |
| `sensor.sake_new_vapor_pressure` | telemetry | sensorpush_cloud | pressure (psi) | disabled |

#### Sonos Card

- Device ID: `device_02ce76119161`
- Integration: hacs
- Model: punxaphil plugin
- Capability mix: 1 telemetry, 1 control, 0 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `switch.sonos_card_pre_release` | control | hacs | diagnostic | disabled |
| `update.sonos_card_update` | telemetry | hacs | config | not_enriched |

#### Spotify

- Device ID: `device_b09ca0ad1db1`
- Integration: spotify
- Model: Spotify AB Spotify premium
- Capability mix: 0 telemetry, 1 control, 0 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `media_player.spotify` | control | spotify |  | not_enriched |

#### Sun

- Device ID: `device_a33df9341ba8`
- Integration: sun
- Model: unknown model
- Capability mix: 10 telemetry, 0 control, 0 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `binary_sensor.sun_solar_rising` | telemetry | sun | diagnostic | disabled |
| `sensor.sun_next_dawn` | telemetry | sun | timestamp | not_enriched |
| `sensor.sun_next_dusk` | telemetry | sun | timestamp | not_enriched |
| `sensor.sun_next_midnight` | telemetry | sun | timestamp | not_enriched |
| `sensor.sun_next_noon` | telemetry | sun | timestamp | not_enriched |
| `sensor.sun_next_rising` | telemetry | sun | timestamp | not_enriched |
| `sensor.sun_next_setting` | telemetry | sun | timestamp | not_enriched |
| `sensor.sun_solar_azimuth` | telemetry | sun | diagnostic (°) | disabled |
| `sensor.sun_solar_elevation` | telemetry | sun | diagnostic (°) | disabled |
| `sensor.sun_solar_rising` | telemetry | sun | diagnostic | disabled |

#### TK iPhone 16 Pro

- Device ID: `device_784e00b00a1e`
- Integration: mobile_app
- Model: Apple iPhone17,1
- Capability mix: 14 telemetry, 0 control, 0 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `device_tracker.tk_iphone_16_pro` | telemetry | mobile_app | diagnostic | not_enriched |
| `sensor.tk_iphone_16_pro_app_version` | telemetry | mobile_app | diagnostic | not_enriched |
| `sensor.tk_iphone_16_pro_audio_output` | telemetry | mobile_app |  | not_enriched |
| `sensor.tk_iphone_16_pro_battery_level` | telemetry | mobile_app | battery (%) | not_enriched |
| `sensor.tk_iphone_16_pro_battery_state` | telemetry | mobile_app |  | not_enriched |
| `sensor.tk_iphone_16_pro_bssid` | telemetry | mobile_app |  | not_enriched |
| `sensor.tk_iphone_16_pro_connection_type` | telemetry | mobile_app |  | not_enriched |
| `sensor.tk_iphone_16_pro_geocoded_location` | telemetry | mobile_app |  | not_enriched |
| `sensor.tk_iphone_16_pro_last_update_trigger` | telemetry | mobile_app |  | not_enriched |
| `sensor.tk_iphone_16_pro_location_permission` | telemetry | mobile_app |  | not_enriched |
| `sensor.tk_iphone_16_pro_sim_1` | telemetry | mobile_app |  | not_enriched |
| `sensor.tk_iphone_16_pro_sim_2` | telemetry | mobile_app |  | not_enriched |
| `sensor.tk_iphone_16_pro_ssid` | telemetry | mobile_app |  | not_enriched |
| `sensor.tk_iphone_16_pro_storage` | telemetry | mobile_app | % available | not_enriched |

#### Terminal & SSH

- Device ID: `device_86ea87697a8c`
- Integration: hassio
- Model: Official apps Home Assistant Add-on
- Capability mix: 6 telemetry, 1 control, 0 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `binary_sensor.terminal_ssh_running` | telemetry | hassio | running | disabled |
| `sensor.terminal_ssh_cpu_percent` | telemetry | hassio | % | disabled |
| `sensor.terminal_ssh_memory_percent` | telemetry | hassio | % | disabled |
| `sensor.terminal_ssh_newest_version` | telemetry | hassio |  | disabled |
| `sensor.terminal_ssh_version` | telemetry | hassio |  | disabled |
| `switch.terminal_ssh` | control | hassio |  | disabled |
| `update.terminal_ssh_update` | telemetry | hassio | config | not_enriched |

#### Tesla

- Device ID: `device_ef443339991c`
- Integration: unifi
- Model: Tesla,Inc.
- Capability mix: 1 telemetry, 0 control, 1 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `device_tracker.tesla` | network | unifi | diagnostic | not_enriched |
| `sensor.tesla_link_speed` | telemetry | unifi | data_rate (Mbit/s) | disabled |

#### Texas Instruments CC2652

- Device ID: `device_c6f095238e88`
- Integration: zha
- Model: Texas Instruments CC2652
- Capability mix: 0 telemetry, 0 control, 0 network, 0 other

_No registered entities._

#### U7 Pro (Family Room)

- Device ID: `device_285a8f1e6261`
- Integration: unifi
- Model: Ubiquiti Networks U7PRO
- Capability mix: 7 telemetry, 2 control, 1 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `button.u7_pro_family_room_restart` | control | unifi | restart | not_enriched |
| `device_tracker.u7_pro_family_room` | network | unifi | diagnostic | not_enriched |
| `light.u7_pro_family_room_led` | control | unifi | config | not_enriched |
| `sensor.u7_pro_family_room_clients` | telemetry | unifi | diagnostic | disabled |
| `sensor.u7_pro_family_room_cpu_utilization` | telemetry | unifi | diagnostic (%) | not_enriched |
| `sensor.u7_pro_family_room_memory_utilization` | telemetry | unifi | diagnostic (%) | not_enriched |
| `sensor.u7_pro_family_room_state` | telemetry | unifi | enum | not_enriched |
| `sensor.u7_pro_family_room_uplink_mac` | telemetry | unifi | diagnostic | not_enriched |
| `sensor.u7_pro_family_room_uptime` | telemetry | unifi | timestamp | not_enriched |
| `update.u7_pro_family_room` | telemetry | unifi | firmware | not_enriched |

#### U7 Pro (Mesh)

- Device ID: `device_435c14fb97bb`
- Integration: unifi
- Model: Ubiquiti Networks U7PRO
- Capability mix: 7 telemetry, 2 control, 1 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `button.u7_pro_mesh_restart` | control | unifi | restart | not_enriched |
| `device_tracker.u7_pro_mesh` | network | unifi | diagnostic | not_enriched |
| `light.u7_pro_mesh_led` | control | unifi | config | not_enriched |
| `sensor.u7_pro_mesh_clients` | telemetry | unifi | diagnostic | disabled |
| `sensor.u7_pro_mesh_cpu_utilization` | telemetry | unifi | diagnostic (%) | not_enriched |
| `sensor.u7_pro_mesh_memory_utilization` | telemetry | unifi | diagnostic (%) | not_enriched |
| `sensor.u7_pro_mesh_state` | telemetry | unifi | enum | not_enriched |
| `sensor.u7_pro_mesh_uplink_mac` | telemetry | unifi | diagnostic | not_enriched |
| `sensor.u7_pro_mesh_uptime` | telemetry | unifi | timestamp | not_enriched |
| `update.u7_pro_mesh` | telemetry | unifi | firmware | not_enriched |

#### U7 Pro (Mud Room)

- Device ID: `device_776f62e721cd`
- Integration: unifi
- Model: Ubiquiti Networks U7PRO
- Capability mix: 7 telemetry, 2 control, 1 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `button.u7_pro_mud_room_restart` | control | unifi | restart | not_enriched |
| `device_tracker.u7_pro_mud_room` | network | unifi | diagnostic | not_enriched |
| `light.u7_pro_mud_room_led` | control | unifi | config | not_enriched |
| `sensor.u7_pro_mud_room_clients` | telemetry | unifi | diagnostic | disabled |
| `sensor.u7_pro_mud_room_cpu_utilization` | telemetry | unifi | diagnostic (%) | not_enriched |
| `sensor.u7_pro_mud_room_memory_utilization` | telemetry | unifi | diagnostic (%) | not_enriched |
| `sensor.u7_pro_mud_room_state` | telemetry | unifi | enum | not_enriched |
| `sensor.u7_pro_mud_room_uplink_mac` | telemetry | unifi | diagnostic | not_enriched |
| `sensor.u7_pro_mud_room_uptime` | telemetry | unifi | timestamp | not_enriched |
| `update.u7_pro_mud_room` | telemetry | unifi | firmware | not_enriched |

#### USW Flex 2.5G 5

- Device ID: `device_cb39eb41896c`
- Integration: unifi
- Model: Ubiquiti Networks USWED35
- Capability mix: 7 telemetry, 6 control, 1 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `button.usw_flex_2_5g_5_restart` | control | unifi | restart | not_enriched |
| `device_tracker.usw_flex_2_5g_5` | network | unifi | diagnostic | not_enriched |
| `sensor.usw_flex_2_5g_5_clients` | telemetry | unifi | diagnostic | disabled |
| `sensor.usw_flex_2_5g_5_cpu_utilization` | telemetry | unifi | diagnostic (%) | not_enriched |
| `sensor.usw_flex_2_5g_5_memory_utilization` | telemetry | unifi | diagnostic (%) | not_enriched |
| `sensor.usw_flex_2_5g_5_state` | telemetry | unifi | enum | not_enriched |
| `sensor.usw_flex_2_5g_5_uplink_mac` | telemetry | unifi | diagnostic | not_enriched |
| `sensor.usw_flex_2_5g_5_uptime` | telemetry | unifi | timestamp | not_enriched |
| `switch.usw_flex_2_5g_5_port_1` | control | unifi | switch | disabled |
| `switch.usw_flex_2_5g_5_port_2` | control | unifi | switch | disabled |
| `switch.usw_flex_2_5g_5_port_3` | control | unifi | switch | disabled |
| `switch.usw_flex_2_5g_5_port_4` | control | unifi | switch | disabled |
| `switch.usw_flex_2_5g_5_port_5` | control | unifi | switch | disabled |
| `update.usw_flex_2_5g_5` | telemetry | unifi | firmware | not_enriched |

#### UniFi Network

- Device ID: `device_bfecdd68ffca`
- Integration: unifi
- Model: Ubiquiti Networks UniFi Network Application
- Capability mix: 0 telemetry, 0 control, 0 network, 0 other

_No registered entities._

#### Unnamed Room

- Device ID: `device_70e6bc5cc91c`
- Integration: sonos, unifi
- Model: Sonos Era 100
- Capability mix: 2 telemetry, 8 control, 1 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `binary_sensor.unnamed_room_microphone_7` | telemetry | sonos | diagnostic | not_enriched |
| `device_tracker.sonoszp_10` | network | unifi | diagnostic | not_enriched |
| `media_player.unnamed_room_4` | control | sonos | speaker | not_enriched |
| `number.unnamed_room_balance_9` | control | sonos | config | not_enriched |
| `number.unnamed_room_bass_9` | control | sonos | config | not_enriched |
| `number.unnamed_room_treble_9` | control | sonos | config | not_enriched |
| `sensor.sonoszp_link_speed` | telemetry | unifi | data_rate (Mbit/s) | disabled |
| `switch.unnamed_room_crossfade_9` | control | sonos | config | not_enriched |
| `switch.unnamed_room_loudness_9` | control | sonos | config | not_enriched |
| `switch.unnamed_room_status_light_9` | control | sonos | config | disabled |
| `switch.unnamed_room_touch_controls_9` | control | sonos | config | disabled |

#### Unnamed Room

- Device ID: `device_958d2caf578a`
- Integration: sonos, unifi
- Model: Sonos Era 100
- Capability mix: 2 telemetry, 8 control, 1 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `binary_sensor.unnamed_room_microphone_6` | telemetry | sonos | diagnostic | not_enriched |
| `device_tracker.unifi_default_mac_e322eb2d1cf7` | network | unifi | diagnostic | not_enriched |
| `media_player.unnamed_room_3` | control | sonos | speaker | not_enriched |
| `number.unnamed_room_balance_8` | control | sonos | config | not_enriched |
| `number.unnamed_room_bass_8` | control | sonos | config | not_enriched |
| `number.unnamed_room_treble_8` | control | sonos | config | not_enriched |
| `sensor.link_speed_12` | telemetry | unifi | data_rate (Mbit/s) | disabled |
| `switch.unnamed_room_crossfade_8` | control | sonos | config | not_enriched |
| `switch.unnamed_room_loudness_8` | control | sonos | config | not_enriched |
| `switch.unnamed_room_status_light_8` | control | sonos | config | disabled |
| `switch.unnamed_room_touch_controls_8` | control | sonos | config | disabled |

#### Unnamed Room

- Device ID: `device_cc546a11400c`
- Integration: sonos, unifi
- Model: Sonos Arc Ultra
- Capability mix: 3 telemetry, 16 control, 1 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `binary_sensor.unnamed_room_microphone_5` | telemetry | sonos | diagnostic | not_enriched |
| `device_tracker.unifi_default_mac_0bbc683a0fb6` | network | unifi | diagnostic | not_enriched |
| `media_player.unnamed_room_2` | control | sonos | speaker | not_enriched |
| `number.unnamed_room_audio_delay_2` | control | sonos | config | not_enriched |
| `number.unnamed_room_balance_7` | control | sonos | config | not_enriched |
| `number.unnamed_room_bass_7` | control | sonos | config | not_enriched |
| `number.unnamed_room_music_surround_level_2` | control | sonos | config | not_enriched |
| `number.unnamed_room_surround_level_2` | control | sonos | config | not_enriched |
| `number.unnamed_room_treble_7` | control | sonos | config | not_enriched |
| `select.unnamed_room_speech_enhancement` | control | sonos |  | not_enriched |
| `sensor.link_speed_4` | telemetry | unifi | data_rate (Mbit/s) | disabled |
| `sensor.unnamed_room_audio_input_format_2` | telemetry | sonos | diagnostic | not_enriched |
| `switch.unnamed_room_crossfade_7` | control | sonos | config | not_enriched |
| `switch.unnamed_room_loudness_7` | control | sonos | config | not_enriched |
| `switch.unnamed_room_night_sound_2` | control | sonos | config | not_enriched |
| `switch.unnamed_room_speech_enhancement_2` | control | sonos | config | not_enriched |
| `switch.unnamed_room_status_light_7` | control | sonos | config | disabled |
| `switch.unnamed_room_surround_enabled_2` | control | sonos | config | not_enriched |
| `switch.unnamed_room_surround_music_full_volume_2` | control | sonos | config | not_enriched |
| `switch.unnamed_room_touch_controls_7` | control | sonos | config | disabled |

#### Wine Cave

- Device ID: `device_dfed0d9dd820`
- Integration: sensorpush_cloud
- Model: SensorPush HT.w
- Capability mix: 8 telemetry, 0 control, 0 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `sensor.wine_altitude` | telemetry | sensorpush_cloud | distance (ft) | disabled |
| `sensor.wine_atmospheric_pressure` | telemetry | sensorpush_cloud | atmospheric_pressure (inHg) | disabled |
| `sensor.wine_battery_voltage` | telemetry | sensorpush_cloud | voltage (V) | disabled |
| `sensor.wine_dew_point` | telemetry | sensorpush_cloud | temperature (°F) | disabled |
| `sensor.wine_humidity` | telemetry | sensorpush_cloud | humidity (%) | not_enriched |
| `sensor.wine_signal_strength` | telemetry | sensorpush_cloud | signal_strength (dBm) | disabled |
| `sensor.wine_temperature` | telemetry | sensorpush_cloud | temperature (°F) | not_enriched |
| `sensor.wine_vapor_pressure` | telemetry | sensorpush_cloud | pressure (psi) | disabled |

#### apexcharts-card

- Device ID: `device_c52d3866edb7`
- Integration: hacs
- Model: RomRider plugin
- Capability mix: 1 telemetry, 1 control, 0 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `switch.apexcharts_card_pre_release` | control | hacs | diagnostic | disabled |
| `update.apexcharts_card_update` | telemetry | hacs | config | not_enriched |

#### browser_mod

- Device ID: `device_9e59c4081483`
- Integration: hacs
- Model: thomasloven integration
- Capability mix: 1 telemetry, 1 control, 0 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `switch.browser_mod_pre_release` | control | hacs | diagnostic | disabled |
| `update.browser_mod_update` | telemetry | hacs | config | not_enriched |

#### button-card

- Device ID: `device_7023603357b8`
- Integration: hacs
- Model: custom-cards plugin
- Capability mix: 1 telemetry, 1 control, 0 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `switch.button_card_pre_release` | control | hacs | diagnostic | disabled |
| `update.button_card_update` | telemetry | hacs | config | not_enriched |

#### card-mod

- Device ID: `device_a8302d8a0e9a`
- Integration: hacs
- Model: thomasloven plugin
- Capability mix: 1 telemetry, 1 control, 0 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `switch.card_mod_pre_release` | control | hacs | diagnostic | disabled |
| `update.card_mod_update` | telemetry | hacs | config | not_enriched |

#### device_029571f3b27b

- Device ID: `device_029571f3b27b`
- Integration: unifi
- Model: unknown model
- Capability mix: 1 telemetry, 0 control, 1 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `device_tracker.unifi_default_mac_e52ad2d9d62a` | network | unifi | diagnostic | not_enriched |
| `sensor.link_speed_17` | telemetry | unifi | data_rate (Mbit/s) | disabled |

#### device_1aa897c2d0b4

- Device ID: `device_1aa897c2d0b4`
- Integration: unifi
- Model: unknown model
- Capability mix: 1 telemetry, 0 control, 1 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `device_tracker.unifi_default_mac_b019bd33cc89` | network | unifi | diagnostic | not_enriched |
| `sensor.link_speed_6` | telemetry | unifi | data_rate (Mbit/s) | disabled |

#### device_1c8c7be1ef1d

- Device ID: `device_1c8c7be1ef1d`
- Integration: unifi
- Model: unknown model
- Capability mix: 1 telemetry, 0 control, 1 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `device_tracker.unifi_default_mac_92902c5c8aa5` | network | unifi | diagnostic | not_enriched |
| `sensor.link_speed_18` | telemetry | unifi | data_rate (Mbit/s) | disabled |

#### device_1cc45f5d1971

- Device ID: `device_1cc45f5d1971`
- Integration: unifi
- Model: unknown model
- Capability mix: 1 telemetry, 0 control, 1 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `device_tracker.unifi_default_mac_de716b80d9a5` | network | unifi | diagnostic | not_enriched |
| `sensor.link_speed_3` | telemetry | unifi | data_rate (Mbit/s) | disabled |

#### device_2a3f688bcd08

- Device ID: `device_2a3f688bcd08`
- Integration: unifi
- Model: unknown model
- Capability mix: 1 telemetry, 0 control, 1 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `device_tracker.unifi_default_mac_5042130907ce` | network | unifi | diagnostic | not_enriched |
| `sensor.link_speed_7` | telemetry | unifi | data_rate (Mbit/s) | disabled |

#### device_2c405371e8c8

- Device ID: `device_2c405371e8c8`
- Integration: unifi
- Model: unknown model
- Capability mix: 1 telemetry, 0 control, 1 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `device_tracker.unifi_default_mac_b01ea2b181ff` | network | unifi | diagnostic | not_enriched |
| `sensor.link_speed_11` | telemetry | unifi | data_rate (Mbit/s) | disabled |

#### device_3ccbd9acaad8

- Device ID: `device_3ccbd9acaad8`
- Integration: unifi
- Model: Lumi United Technology Co., Ltd
- Capability mix: 1 telemetry, 0 control, 1 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `device_tracker.unifi_default_mac_754c3a1ea02a` | network | unifi | diagnostic | not_enriched |
| `sensor.link_speed_8` | telemetry | unifi | data_rate (Mbit/s) | disabled |

#### device_52184e4933c8

- Device ID: `device_52184e4933c8`
- Integration: unifi
- Model: unknown model
- Capability mix: 1 telemetry, 0 control, 1 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `device_tracker.unifi_default_mac_e29de8de1f70` | network | unifi | diagnostic | not_enriched |
| `sensor.link_speed_9` | telemetry | unifi | data_rate (Mbit/s) | disabled |

#### device_70d43284b9e8

- Device ID: `device_70d43284b9e8`
- Integration: unifi
- Model: unknown model
- Capability mix: 1 telemetry, 0 control, 1 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `device_tracker.unifi_default_mac_dd5079c60353` | network | unifi | diagnostic | not_enriched |
| `sensor.link_speed` | telemetry | unifi | data_rate (Mbit/s) | disabled |

#### device_7bb64bc09fcd

- Device ID: `device_7bb64bc09fcd`
- Integration: unifi
- Model: unknown model
- Capability mix: 1 telemetry, 0 control, 1 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `device_tracker.unifi_default_mac_d129d9e3d6b1` | network | unifi | diagnostic | not_enriched |
| `sensor.link_speed_20` | telemetry | unifi | data_rate (Mbit/s) | disabled |

#### device_7e76f4adbfbd

- Device ID: `device_7e76f4adbfbd`
- Integration: unifi
- Model: unknown model
- Capability mix: 1 telemetry, 0 control, 1 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `device_tracker.unifi_default_mac_7ed0c6182c02` | network | unifi | diagnostic | not_enriched |
| `sensor.link_speed_10` | telemetry | unifi | data_rate (Mbit/s) | disabled |

#### device_abb8fec33d8d

- Device ID: `device_abb8fec33d8d`
- Integration: unifi
- Model: unknown model
- Capability mix: 1 telemetry, 0 control, 1 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `device_tracker.unifi_default_mac_9878938b26f8` | network | unifi | diagnostic | not_enriched |
| `sensor.link_speed_13` | telemetry | unifi | data_rate (Mbit/s) | disabled |

#### device_bc00b8395464

- Device ID: `device_bc00b8395464`
- Integration: unifi
- Model: unknown model
- Capability mix: 1 telemetry, 0 control, 1 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `device_tracker.unifi_default_mac_a38f4e4b84a0` | network | unifi | diagnostic | not_enriched |
| `sensor.link_speed_5` | telemetry | unifi | data_rate (Mbit/s) | disabled |

#### device_c06583cbe783

- Device ID: `device_c06583cbe783`
- Integration: unifi
- Model: unknown model
- Capability mix: 1 telemetry, 0 control, 1 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `device_tracker.unifi_default_mac_29c96008c22e` | network | unifi | diagnostic | not_enriched |
| `sensor.link_speed_16` | telemetry | unifi | data_rate (Mbit/s) | disabled |

#### device_c47d5565d225

- Device ID: `device_c47d5565d225`
- Integration: unifi
- Model: unknown model
- Capability mix: 1 telemetry, 0 control, 1 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `device_tracker.unifi_default_mac_be3f4a9ec204` | network | unifi | diagnostic | not_enriched |
| `sensor.link_speed_15` | telemetry | unifi | data_rate (Mbit/s) | disabled |

#### device_c8b798d0e2b2

- Device ID: `device_c8b798d0e2b2`
- Integration: unifi
- Model: unknown model
- Capability mix: 1 telemetry, 0 control, 1 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `device_tracker.unifi_default_mac_2c894ada8b0b` | network | unifi | diagnostic | not_enriched |
| `sensor.link_speed_19` | telemetry | unifi | data_rate (Mbit/s) | disabled |

#### device_e90900658a90

- Device ID: `device_e90900658a90`
- Integration: unifi
- Model: unknown model
- Capability mix: 1 telemetry, 0 control, 1 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `device_tracker.unifi_default_mac_d8484ff5d8dc` | network | unifi | diagnostic | not_enriched |
| `sensor.link_speed_14` | telemetry | unifi | data_rate (Mbit/s) | disabled |

#### device_e9b166e8b6d8

- Device ID: `device_e9b166e8b6d8`
- Integration: unifi
- Model: unknown model
- Capability mix: 1 telemetry, 0 control, 1 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `device_tracker.unifi_default_mac_e75396edd3fe` | network | unifi | diagnostic | not_enriched |
| `sensor.link_speed_2` | telemetry | unifi | data_rate (Mbit/s) | disabled |

#### iPhone

- Device ID: `device_39dfc0b93cda`
- Integration: unifi
- Model: unknown model
- Capability mix: 1 telemetry, 0 control, 1 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `device_tracker.iphone` | network | unifi | diagnostic | not_enriched |
| `sensor.iphone_link_speed` | telemetry | unifi | data_rate (Mbit/s) | disabled |

#### mini-graph-card

- Device ID: `device_d6ad629b5b1b`
- Integration: hacs
- Model: kalkih plugin
- Capability mix: 1 telemetry, 1 control, 0 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `switch.mini_graph_card_pre_release` | control | hacs | diagnostic | disabled |
| `update.mini_graph_card_update` | telemetry | hacs | config | not_enriched |

#### visionOS & iOS 26 Liquid Glass Theme

- Device ID: `device_cbfb7f8b93cb`
- Integration: hacs
- Model: Nezz theme
- Capability mix: 1 telemetry, 1 control, 0 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `switch.visionos_ios_26_liquid_glass_theme_pre_release` | control | hacs | diagnostic | disabled |
| `update.visionos_ios_26_liquid_glass_theme_update` | telemetry | hacs | config | not_enriched |

### Unnamed Room

#### Master Sonos

- Device ID: `device_f1a2af0f711a`
- Integration: sonos, unifi
- Model: Sonos Beam
- Capability mix: 2 telemetry, 17 control, 1 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `binary_sensor.unnamed_room_microphone` | telemetry | sonos | diagnostic | not_enriched |
| `device_tracker.sonos_beam_master` | network | unifi | diagnostic | not_enriched |
| `media_player.unnamed_room` | control | sonos | speaker | not_enriched |
| `number.master_sonos_sub_gain` | control | sonos | config | not_enriched |
| `number.unnamed_room_audio_delay` | control | sonos | config | not_enriched |
| `number.unnamed_room_balance` | control | sonos | config | not_enriched |
| `number.unnamed_room_bass` | control | sonos | config | not_enriched |
| `number.unnamed_room_music_surround_level` | control | sonos | config | not_enriched |
| `number.unnamed_room_surround_level` | control | sonos | config | not_enriched |
| `number.unnamed_room_treble` | control | sonos | config | not_enriched |
| `sensor.unnamed_room_audio_input_format` | telemetry | sonos | diagnostic | not_enriched |
| `switch.master_sonos_subwoofer_enabled` | control | sonos | config | not_enriched |
| `switch.unnamed_room_crossfade` | control | sonos | config | not_enriched |
| `switch.unnamed_room_loudness` | control | sonos | config | not_enriched |
| `switch.unnamed_room_night_sound` | control | sonos | config | not_enriched |
| `switch.unnamed_room_speech_enhancement` | control | sonos | config | not_enriched |
| `switch.unnamed_room_status_light` | control | sonos | config | disabled |
| `switch.unnamed_room_surround_enabled` | control | sonos | config | not_enriched |
| `switch.unnamed_room_surround_music_full_volume` | control | sonos | config | not_enriched |
| `switch.unnamed_room_touch_controls` | control | sonos | config | disabled |

#### Office

- Device ID: `device_f5cc48a3b632`
- Integration: sonos, unifi
- Model: Sonos Arc Ultra
- Capability mix: 2 telemetry, 18 control, 1 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `binary_sensor.unnamed_room_microphone_4` | telemetry | sonos | diagnostic | not_enriched |
| `device_tracker.sonoszp_4` | network | unifi | diagnostic | not_enriched |
| `media_player.unnamed_room_6` | control | sonos | speaker | not_enriched |
| `number.office_audio_delay` | control | sonos | config | not_enriched |
| `number.office_music_surround_level` | control | sonos | config | not_enriched |
| `number.office_sub_gain` | control | sonos | config | not_enriched |
| `number.office_surround_level` | control | sonos | config | not_enriched |
| `number.unnamed_room_balance_6` | control | sonos | config | not_enriched |
| `number.unnamed_room_bass_6` | control | sonos | config | not_enriched |
| `number.unnamed_room_treble_6` | control | sonos | config | not_enriched |
| `select.office_speech_enhancement` | control | sonos |  | not_enriched |
| `sensor.office_audio_input_format` | telemetry | sonos | diagnostic | not_enriched |
| `switch.office_night_sound` | control | sonos | config | not_enriched |
| `switch.office_speech_enhancement` | control | sonos | config | not_enriched |
| `switch.office_subwoofer_enabled` | control | sonos | config | not_enriched |
| `switch.office_surround_enabled` | control | sonos | config | not_enriched |
| `switch.office_surround_music_full_volume` | control | sonos | config | not_enriched |
| `switch.unnamed_room_crossfade_6` | control | sonos | config | not_enriched |
| `switch.unnamed_room_loudness_6` | control | sonos | config | not_enriched |
| `switch.unnamed_room_status_light_6` | control | sonos | config | disabled |
| `switch.unnamed_room_touch_controls_6` | control | sonos | config | disabled |

#### Unnamed Room

- Device ID: `device_03b5c329a9f3`
- Integration: sonos
- Model: Sonos One SL
- Capability mix: 0 telemetry, 7 control, 0 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `number.unnamed_room_balance_3` | control | sonos | config | not_enriched |
| `number.unnamed_room_bass_3` | control | sonos | config | not_enriched |
| `number.unnamed_room_treble_3` | control | sonos | config | not_enriched |
| `switch.unnamed_room_crossfade_3` | control | sonos | config | not_enriched |
| `switch.unnamed_room_loudness_3` | control | sonos | config | not_enriched |
| `switch.unnamed_room_status_light_3` | control | sonos | config | disabled |
| `switch.unnamed_room_touch_controls_3` | control | sonos | config | disabled |

#### Unnamed Room

- Device ID: `device_41760008fad9`
- Integration: sonos, unifi
- Model: Sonos Era 300
- Capability mix: 1 telemetry, 7 control, 1 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `binary_sensor.unnamed_room_microphone_3` | telemetry | sonos | diagnostic | not_enriched |
| `device_tracker.sonoszp_11` | network | unifi | diagnostic | not_enriched |
| `number.unnamed_room_balance_5` | control | sonos | config | not_enriched |
| `number.unnamed_room_bass_5` | control | sonos | config | not_enriched |
| `number.unnamed_room_treble_5` | control | sonos | config | not_enriched |
| `switch.unnamed_room_crossfade_5` | control | sonos | config | not_enriched |
| `switch.unnamed_room_loudness_5` | control | sonos | config | not_enriched |
| `switch.unnamed_room_status_light_5` | control | sonos | config | disabled |
| `switch.unnamed_room_touch_controls_5` | control | sonos | config | disabled |

#### Unnamed Room

- Device ID: `device_59c87770e78a`
- Integration: sonos, unifi
- Model: Sonos Era 300
- Capability mix: 1 telemetry, 7 control, 1 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `binary_sensor.unnamed_room_microphone_2` | telemetry | sonos | diagnostic | not_enriched |
| `device_tracker.sonoszp_12` | network | unifi | diagnostic | not_enriched |
| `number.unnamed_room_balance_4` | control | sonos | config | not_enriched |
| `number.unnamed_room_bass_4` | control | sonos | config | not_enriched |
| `number.unnamed_room_treble_4` | control | sonos | config | not_enriched |
| `switch.unnamed_room_crossfade_4` | control | sonos | config | not_enriched |
| `switch.unnamed_room_loudness_4` | control | sonos | config | not_enriched |
| `switch.unnamed_room_status_light_4` | control | sonos | config | disabled |
| `switch.unnamed_room_touch_controls_4` | control | sonos | config | disabled |

#### Unnamed Room

- Device ID: `device_73cd04bd08c1`
- Integration: sonos
- Model: Sonos One SL
- Capability mix: 0 telemetry, 7 control, 0 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `number.unnamed_room_balance_2` | control | sonos | config | not_enriched |
| `number.unnamed_room_bass_2` | control | sonos | config | not_enriched |
| `number.unnamed_room_treble_2` | control | sonos | config | not_enriched |
| `switch.unnamed_room_crossfade_2` | control | sonos | config | not_enriched |
| `switch.unnamed_room_loudness_2` | control | sonos | config | not_enriched |
| `switch.unnamed_room_status_light_2` | control | sonos | config | disabled |
| `switch.unnamed_room_touch_controls_2` | control | sonos | config | disabled |

### Upstairs Hallway

#### Upstairs Hallway Main Lights

- Device ID: `device_50d071801b14`
- Integration: lutron_caseta
- Model: Lutron Electronics Co., Inc DVRF-6L (DivaSmartDimmer)
- Capability mix: 0 telemetry, 1 control, 0 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `light.upstairs_hallway_main_lights` | control | lutron_caseta |  | not_enriched |

### Vestibule

#### Vestibule Main Lights

- Device ID: `device_bdc194038091`
- Integration: lutron_caseta
- Model: Lutron Electronics Co., Inc DVRF-6L (DivaSmartDimmer)
- Capability mix: 0 telemetry, 1 control, 0 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `light.vestibule_main_lights` | control | lutron_caseta |  | not_enriched |

### Wynn's Room

#### Wynn Sonos

- Device ID: `device_d2716c1c55b9`
- Integration: sonos, unifi
- Model: Sonos Era 100
- Capability mix: 1 telemetry, 8 control, 1 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `binary_sensor.wynn_s_room_microphone` | telemetry | sonos | diagnostic | not_enriched |
| `device_tracker.sonoszp_3` | network | unifi | diagnostic | not_enriched |
| `media_player.wynn_s_room` | control | sonos | speaker | not_enriched |
| `number.wynn_s_room_balance` | control | sonos | config | not_enriched |
| `number.wynn_s_room_bass` | control | sonos | config | not_enriched |
| `number.wynn_s_room_treble` | control | sonos | config | not_enriched |
| `switch.wynn_s_room_crossfade` | control | sonos | config | not_enriched |
| `switch.wynn_s_room_loudness` | control | sonos | config | not_enriched |
| `switch.wynn_s_room_status_light` | control | sonos | config | disabled |
| `switch.wynn_s_room_touch_controls` | control | sonos | config | disabled |

## Orphan Entities

| Entity | Name | Role | Integration | Availability |
| --- | --- | --- | --- | --- |
| `automation.new_automation` | Noise Detection - Wynn's Room | other | automation | not_enriched |
| `automation.security_alert_garage_door_unlocked` | Security Alert - Garage door unlocked | other | automation | not_enriched |
| `automation.water_daytime_sustained_low_flow` | Water — Daytime Sustained Low Flow | other | automation | not_enriched |
| `automation.water_flo_system_alert` | Water — Flo System Alert | other | automation | not_enriched |
| `automation.water_high_daily_usage` | Water — High Daily Usage | other | automation | not_enriched |
| `automation.water_high_flow_burst_daytime` | Water — High Flow Burst (Daytime) | other | automation | not_enriched |
| `automation.water_high_flow_burst_overnight` | Water — High Flow Burst (Overnight) | other | automation | not_enriched |
| `automation.water_high_pressure` | Water — High Pressure | other | automation | not_enriched |
| `automation.water_leak_sensor_triggered` | Water — Leak Sensor Triggered | other | automation | not_enriched |
| `automation.water_low_pressure` | Water — Low Pressure | other | automation | not_enriched |
| `automation.water_overnight_continuous_flow_running_toilet` | Water — Overnight Continuous Flow (Running Toilet) | other | automation | not_enriched |
| `automation.water_shutoff_valve_closed` | Water — Shutoff Valve Closed | other | automation | not_enriched |
| `binary_sensor.remote_ui` | Remote UI | telemetry | cloud | not_enriched |
| `device_tracker.airthings_view` | airthings-view | network | unifi | disabled |
| `device_tracker.apple_tv_basement` | Apple TV (Basement) | network | unifi | disabled |
| `device_tracker.apple_tv_family_room_2` | Apple TV (Family Room) | network | unifi | disabled |
| `device_tracker.apple_tv_master` | Apple TV (Master) | network | unifi | disabled |
| `device_tracker.casey_s_iphone_16_pro` | Casey's iPhone 16 Pro | network | unifi | disabled |
| `device_tracker.db15_2` | DB15 | network | unifi | disabled |
| `device_tracker.dining_room` | Dining-Room | network | unifi | disabled |
| `device_tracker.ecobee_master` | Ecobee (Master) | network | unifi | disabled |
| `device_tracker.ecobee_office` | Ecobee (Office) | network | unifi | disabled |
| `device_tracker.galaxy_tab_a_80_2019` | Google Tablet (Monitor) | network | unifi | disabled |
| `device_tracker.google_tablet` | device_tracker.google_tablet | network | unifi | disabled |
| `device_tracker.hs103` | HS103 | network | unifi | disabled |
| `device_tracker.hs103_2` | HS103 | network | unifi | disabled |
| `device_tracker.ipad` | iPad | network | unifi | disabled |
| `device_tracker.iphone_2` | iPhone | network | unifi | disabled |
| `device_tracker.iphone_3` | iPhone | network | unifi | disabled |
| `device_tracker.iphone_4` | iPhone | network | unifi | disabled |
| `device_tracker.iphone_5` | iPhone | network | unifi | disabled |
| `device_tracker.jose_s_s23_fe` | Jose-s-S23-FE | network | unifi | disabled |
| `device_tracker.lg_tv_master` | LG TV (Master) | network | unifi | disabled |
| `device_tracker.mac` | Mac | network | unifi | disabled |
| `device_tracker.macbook_air_casey` | Macbook Air (Casey) | network | unifi | disabled |
| `device_tracker.macbook_air_trevor` | Macbook Air (Trevor) | network | unifi | disabled |
| `device_tracker.office_tv` | Apple TV (Office) | network | unifi | disabled |
| `device_tracker.security_camera_backyard` | Security Camera (Backyard) | network | unifi | disabled |
| `device_tracker.security_camera_doorbell` | Security Camera (Doorbell) | network | unifi | disabled |
| `device_tracker.security_camera_side_entry` | Security Camera (Side Entry) | network | unifi | disabled |
| `device_tracker.sonoszp_13` | SonosZP | network | unifi | disabled |
| `device_tracker.sonoszp_2` | SonosZP | network | unifi | disabled |
| `device_tracker.sonoszp_5` | SonosZP | network | unifi | disabled |
| `device_tracker.sonoszp_8` | SonosZP | network | unifi | disabled |
| `device_tracker.sonoszp_9` | SonosZP | network | unifi | disabled |
| `device_tracker.trevor_s_iphone_16_pro` | Trevor's iPhone 16 Pro | network | unifi | disabled |
| `device_tracker.unifi_default_mac_5395b13a8a3d` | iPhone | network | unifi | disabled |
| `device_tracker.unifi_default_mac_c8c81f1a78e1` | device_tracker.unifi_default_mac_c8c81f1a78e1 | network | unifi | disabled |
| `device_tracker.unifi_default_mac_fd58284dab4a` | device_tracker.unifi_default_mac_fd58284dab4a | network | unifi | disabled |
| `device_tracker.vizio_tv_family_room` | Vizio TV (Family Room) | network | unifi | disabled |
| `device_tracker.watch` | Watch | network | unifi | disabled |
| `light.interior_test` | Interior (Test) | control | group | not_enriched |
| `person.bonticou` | Trevor | other | person | not_enriched |
| `person.casey` | Casey | other | person | not_enriched |
| `sensor.radon_level_status` | Radon Level Status | telemetry | template | not_enriched |
| `sensor.sonos_favorites` | Sonos favorites | telemetry | sonos | disabled |
| `sensor.wine_cave_absolute_humidity` | wine_cave_absolute_humidity | telemetry | template | not_enriched |
| `sensor.wine_cave_dew_point` | wine_cave_dew_point | telemetry | template | not_enriched |
| `sensor.wine_cave_rh_excursion` | wine_cave_rh_excursion | telemetry | template | not_enriched |
| `sensor.wine_cave_status` | wine_cave_status | telemetry | template | not_enriched |
| `sensor.wine_cave_temp_excursion` | wine_cave_temp_excursion | telemetry | template | not_enriched |
| `stt.home_assistant_cloud` | Home Assistant Cloud | other | cloud | not_enriched |
| `todo.shopping_list` | Shopping List | other | shopping_list | not_enriched |
| `tts.google_translate_en_com` | Google Translate en com | other | google_translate | not_enriched |
| `tts.home_assistant_cloud` | Home Assistant Cloud | other | cloud | not_enriched |

## UniFi Network Clients

| Client ID | Sources | Connection | Scope | Tracked Entities | Names |
| --- | --- | --- | --- | --- | --- |
| `network_01a7ffa721b6` | entity_registry, unifi_data.wireless_clients |  |  | `device_tracker.hs103_2` | HS103 |
| `network_0349e3cbc41e` | entity_registry, unifi_data.wireless_clients |  |  | `device_tracker.wynns_room` | front-yard |
| `network_063dcd69dabd` | entity_registry, unifi_data.wireless_clients |  |  | `device_tracker.sonoszp_13` | SonosZP |
| `network_0701248004f4` | entity_registry, unifi_data.wireless_clients |  |  | `device_tracker.sonoszp_7` | SonosZP |
| `network_077f803201db` | entity_registry, unifi_data.wireless_clients |  |  | `device_tracker.mechanical_room_leak_detection_espressif` | espressif |
| `network_0bb5a2bc3a59` | entity_registry |  |  | `device_tracker.apple_tv_family_room` | Apple TV (Family Room) |
| `network_1134d72f2862` | entity_registry |  |  | `device_tracker.u7_pro_mesh` | U7 Pro (Mesh) |
| `network_138dd978fd39` | entity_registry, unifi_data.wireless_clients |  |  | `device_tracker.tesla` | Tesla |
| `network_162861e9f8a0` | entity_registry, unifi_data.wireless_clients |  |  | `device_tracker.macbook_air_trevor` | Macbook Air (Trevor) |
| `network_1becf4615ae2` | entity_registry, unifi_data.wireless_clients |  |  | `device_tracker.unifi_default_mac_b01ea2b181ff` |  |
| `network_1c390e0e7586` | entity_registry, unifi_data.wireless_clients |  |  | `device_tracker.office_tv` | Apple TV (Office) |
| `network_24f2b3079862` | entity_registry, unifi_data.wireless_clients |  |  | `device_tracker.unifi_default_mac_5395b13a8a3d` | iPhone |
| `network_2cad38dabb52` | entity_registry, unifi_data.wireless_clients |  |  | `device_tracker.galaxy_tab_a_80_2019` | Google Tablet (Monitor) |
| `network_2dbcba4c5e25` | entity_registry, unifi_data.wireless_clients |  |  | `device_tracker.unifi_default_mac_c8c81f1a78e1` |  |
| `network_31c6e9accc86` | entity_registry |  |  | `device_tracker.bonticou_gateway` | Bonticou Gateway |
| `network_381b44eab343` | entity_registry, unifi_data.wireless_clients |  |  | `device_tracker.apple_tv_master` | Apple TV (Master) |
| `network_3ad07386bd1b` | entity_registry, unifi_data.wireless_clients |  |  | `device_tracker.unifi_default_mac_0bbc683a0fb6` | SonosZP |
| `network_3dcc9e36ff54` | entity_registry, unifi_data.wireless_clients |  |  | `device_tracker.sonoszp_2` | SonosZP |
| `network_40b057178bcb` | entity_registry, unifi_data.wireless_clients |  |  | `device_tracker.uvc_g6_instant` | play-room |
| `network_46e900e653b2` | entity_registry, unifi_data.wireless_clients |  |  | `device_tracker.sonoszp_9` | SonosZP |
| `network_4c75cbea40e0` | entity_registry, unifi_data.wireless_clients |  |  | `device_tracker.unifi_default_mac_e75396edd3fe` | iPhone |
| `network_4dce3587a71b` | entity_registry, unifi_data.wireless_clients |  |  | `device_tracker.dining_room` | Dining-Room |
| `network_4eb1785061b8` | entity_registry, unifi_data.wireless_clients |  |  | `device_tracker.macbook_air_casey` | Macbook Air (Casey) |
| `network_50358c472a72` | entity_registry, unifi_data.wireless_clients |  |  | `device_tracker.island_sink_leak_detection_espressif` | espressif |
| `network_50c937441dd5` | entity_registry, unifi_data.wireless_clients |  |  | `device_tracker.hs103` | HS103 |
| `network_5200a5ded176` | entity_registry |  |  | `device_tracker.home_assistant` | Home Assistant |
| `network_52793b9da44a` | entity_registry, unifi_data.wireless_clients |  |  | `device_tracker.laundry_sink_leak_detection_espressif` | espressif |
| `network_56124397cc01` | entity_registry, unifi_data.wireless_clients |  |  | `device_tracker.flo_d4e95ef8775b` | flo-d4e95ef8775b |
| `network_5d120dfc3950` | entity_registry, unifi_data.wireless_clients |  |  | `device_tracker.unifi_default_mac_de716b80d9a5` | Watch |
| `network_5d21a958dc6c` | entity_registry, unifi_data.wireless_clients |  |  | `device_tracker.washing_machine_leak_detection_espressif` | espressif |
| `network_5db1c1849ddb` | entity_registry, unifi_data.wireless_clients |  |  | `device_tracker.basement_ejector_leak_detection_espressif` | espressif |
| `network_5dca10f15aa3` | entity_registry, unifi_data.wireless_clients |  |  | `device_tracker.lg_tv_master` | LG TV (Master) |
| `network_5f232cbd21d5` | entity_registry, unifi_data.wireless_clients |  |  | `device_tracker.ecobee_office` | Ecobee (Office) |
| `network_60e35b633815` | entity_registry, unifi_data.wireless_clients |  |  | `device_tracker.google_tablet` |  |
| `network_62b3b60215cc` | entity_registry, unifi_data.wireless_clients |  |  | `device_tracker.unifi_default_mac_9878938b26f8` | Watch |
| `network_68a3d3ec0b4d` | entity_registry, unifi_data.wireless_clients |  |  | `device_tracker.apple_tv_family_room_2` | Apple TV (Family Room) |
| `network_6b848b8b0f65` | entity_registry, unifi_data.wireless_clients |  |  | `device_tracker.unifi_default_mac_d8484ff5d8dc` | iPad |
| `network_6cfb76146798` | entity_registry |  |  | `device_tracker.unifi_default_mac_29c96008c22e` |  |
| `network_6fbe104ea2f3` | entity_registry, unifi_data.wireless_clients |  |  | `device_tracker.uvc_g6_instant_2` | back-yard |
| `network_6fbf9451dc87` | entity_registry, unifi_data.wireless_clients |  |  | `device_tracker.security_camera_side_entry` | Security Camera (Side Entry) |
| `network_75555cf80976` | entity_registry, unifi_data.wireless_clients |  |  | `device_tracker.unifi_default_mac_e29de8de1f70` | Watch |
| `network_7603f3886332` | entity_registry, unifi_data.wireless_clients |  |  | `device_tracker.ecobee_master` | Ecobee (Master) |
| `network_78cf9ce5485a` | entity_registry, unifi_data.wireless_clients |  |  | `device_tracker.iphone_5` | iPhone |
| `network_78ef6386293f` | entity_registry, unifi_data.wireless_clients |  |  | `device_tracker.iphone_4` | iPhone |
| `network_7936b0ab270d` | entity_registry, unifi_data.wireless_clients |  |  | `device_tracker.sonoszp_8` | SonosZP |
| `network_7a3ecf75712d` | entity_registry, unifi_data.wireless_clients |  |  | `device_tracker.vizio_tv_family_room` | Vizio TV (Family Room) |
| `network_7c5c974675ea` | entity_registry, unifi_data.wireless_clients |  |  | `device_tracker.sonoszp_10` | SonosZP |
| `network_7c8af86dfe2f` | entity_registry |  |  | `device_tracker.unifi_default_mac_2c894ada8b0b` |  |
| `network_7cbdb6e2ee7c` | entity_registry, unifi_data.wireless_clients |  |  | `device_tracker.iphone_3` | iPhone |
| `network_7d82b3372ee2` | entity_registry, unifi_data.wireless_clients |  |  | `device_tracker.kitchen_fridge_leak_detection_espressif` | espressif |
| `network_7e17b1e5ef19` | entity_registry, unifi_data.wireless_clients |  |  | `device_tracker.jose_s_s23_fe` | Jose-s-S23-FE |
| `network_835ec58c4a7c` | entity_registry, unifi_data.wireless_clients |  |  | `device_tracker.unifi_default_mac_dd5079c60353` | iPhone |
| `network_853689a7af66` | entity_registry, unifi_data.wireless_clients |  |  | `device_tracker.unifi_default_mac_b019bd33cc89` | iPhone |
| `network_88fdba8f6b4d` | entity_registry |  |  | `device_tracker.usw_flex_2_5g_5` | USW Flex 2.5G 5 |
| `network_89e7f0fa3fd2` | entity_registry, unifi_data.wireless_clients |  |  | `device_tracker.db15_2` | DB15 |
| `network_8a7a9f3fb2a8` | entity_registry, unifi_data.wireless_clients |  |  | `device_tracker.brw849e567c91bc` | BRW849E567C91BC |
| `network_8b065ef7c1a0` | entity_registry |  |  | `device_tracker.lutron_06926f09` | Lutron-06926f09 |
| `network_90db9d129b74` | entity_registry, unifi_data.wireless_clients |  |  | `device_tracker.mud_room` | mud-room |
| `network_968a6d9f0306` | entity_registry, unifi_data.wireless_clients |  |  | `device_tracker.sonoszp_6` | SonosZP |
| `network_9a89c65234c8` | entity_registry, unifi_data.wireless_clients |  |  | `device_tracker.unifi_default_mac_a38f4e4b84a0` | iPhone |
| `network_9f52e1e5c4b5` | entity_registry, unifi_data.wireless_clients |  |  | `device_tracker.trevor_s_iphone_16_pro` | Trevor's iPhone 16 Pro |
| `network_a3399227e493` | entity_registry, unifi_data.wireless_clients |  |  | `device_tracker.dishwasher_leak_detection_espressif` | espressif |
| `network_ab5c96352376` | entity_registry, unifi_data.wireless_clients |  |  | `device_tracker.unifi_default_mac_754c3a1ea02a` | Aqara-Hub-M100-6617 |
| `network_ac89c89ac6b9` | entity_registry, unifi_data.wireless_clients |  |  | `device_tracker.watch` | Watch |
| `network_acba2652c74d` | entity_registry, unifi_data.wireless_clients |  |  | `device_tracker.electrical_room_leak_detection_espressif` | espressif |
| `network_ad87894f3188` | entity_registry, unifi_data.wireless_clients |  |  | `device_tracker.ipad` | iPad |
| `network_addb6fd64468` | entity_registry, unifi_data.wireless_clients |  |  | `device_tracker.sonoszp` | SonosZP |
| `network_afc2c317cfe4` | entity_registry, unifi_data.wireless_clients |  |  | `device_tracker.unifi_default_mac_7ed0c6182c02` | Watch |
| `network_b39ec9ba6c3e` | entity_registry |  |  | `device_tracker.unifi_default_mac_d129d9e3d6b1` |  |
| `network_b5f62e7218fc` | entity_registry, unifi_data.wireless_clients |  |  | `device_tracker.unifi_default_mac_fd58284dab4a` |  |
| `network_b626f9bdd329` | entity_registry, unifi_data.wireless_clients |  |  | `device_tracker.kitchen_sink_leak_detection_espressif` | espressif |
| `network_b65459b7ebe9` | entity_registry |  |  | `device_tracker.u7_pro_family_room` | U7 Pro (Family Room) |
| `network_bef51c8b3c76` | entity_registry, unifi_data.wireless_clients |  |  | `device_tracker.unifi_default_mac_e52ad2d9d62a` | Watch |
| `network_c1e39619d733` | entity_registry, unifi_data.wireless_clients |  |  | `device_tracker.airthings_view` | airthings-view |
| `network_c1face513856` | entity_registry, unifi_data.wireless_clients |  |  | `device_tracker.mac` | Mac |
| `network_c2dfbbd33698` | entity_registry, unifi_data.wireless_clients |  |  | `device_tracker.security_camera_doorbell` | Security Camera (Doorbell) |
| `network_cbae0aa1353c` | entity_registry, unifi_data.wireless_clients |  |  | `device_tracker.sonoszp_3` | SonosZP |
| `network_cc8a57ab7094` | entity_registry, unifi_data.wireless_clients |  |  | `device_tracker.unifi_default_mac_e322eb2d1cf7` | SonosZP |
| `network_d24c85bd5443` | entity_registry, unifi_data.wireless_clients |  |  | `device_tracker.iphone` | Steve's iPhone |
| `network_d6c8b6df39de` | entity_registry, unifi_data.wireless_clients |  |  | `device_tracker.mechanical_room` | mechanical-room |
| `network_d8833f9e6da5` | entity_registry, unifi_data.wireless_clients |  |  | `device_tracker.sonoszp_4` | SonosZP |
| `network_daaa0c318301` | entity_registry, unifi_data.wireless_clients |  |  | `device_tracker.casey_s_iphone_16_pro` | Casey's iPhone 16 Pro |
| `network_db9f019d8988` | entity_registry, unifi_data.wireless_clients |  |  | `device_tracker.security_camera_backyard` | Security Camera (Backyard) |
| `network_dfabd39e61a1` | entity_registry, unifi_data.wireless_clients |  |  | `device_tracker.iphone_2` | iPhone |
| `network_e135643655fd` | entity_registry, unifi_data.wireless_clients |  |  | `device_tracker.galaxy_s24_ultra` | Galaxy-S24-Ultra |
| `network_e1854c2ce2bc` | entity_registry, unifi_data.wireless_clients |  |  | `device_tracker.unifi_default_mac_be3f4a9ec204` | iPhone |
| `network_e238f98d2452` | entity_registry, unifi_data.wireless_clients |  |  | `device_tracker.sonos_beam_master` | Sonos Beam (Master) |
| `network_ece0fee4cc8a` | entity_registry |  |  | `device_tracker.u7_pro_mud_room` | U7 Pro (Mud Room) |
| `network_f17d59d143c7` | entity_registry, unifi_data.wireless_clients |  |  | `device_tracker.db15` | DB15 |
| `network_f24001ded53e` | entity_registry, unifi_data.wireless_clients |  |  | `device_tracker.sonoszp_5` | SonosZP |
| `network_f4b709ebd714` | entity_registry |  |  | `device_tracker.unifi_default_mac_92902c5c8aa5` |  |
| `network_f9edbe1f2387` | entity_registry, unifi_data.wireless_clients |  |  | `device_tracker.sonoszp_12` | SonosZP |
| `network_fb15e20f5084` | entity_registry, unifi_data.wireless_clients |  |  | `device_tracker.apple_tv_basement` | Apple TV (Basement) |
| `network_fb3eecf6e92b` | entity_registry, unifi_data.wireless_clients |  |  | `device_tracker.unifi_default_mac_5042130907ce` | Casey's iPhone 17 Pro |
| `network_fce37b630e1f` | entity_registry, unifi_data.wireless_clients |  |  | `device_tracker.sonoszp_11` | SonosZP |
