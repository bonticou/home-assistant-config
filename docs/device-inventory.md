# Device Inventory

Generated from Home Assistant registries and UniFi-tracked network clients. Sensitive network identifiers are redacted.

## Summary

| Metric | Count |
| --- | --- |
| Devices | 166 |
| Entities | 1788 |
| Orphan entities | 638 |
| Network clients | 114 |
| Areas | 32 |
| Integrations | 40 |

### Roles

| Role | Entities |
| --- | --- |
| control | 626 |
| network | 114 |
| other | 248 |
| telemetry | 800 |

### Top Integrations

| Integration | Entities |
| --- | --- |
| unifiprotect | 371 |
| unifi | 261 |
| template | 192 |
| sonos | 153 |
| script | 124 |
| automation | 112 |
| input_datetime | 65 |
| sensorpush_cloud | 56 |
| input_boolean | 48 |
| flo | 43 |
| homekit_controller | 39 |
| ring | 39 |
| hassio | 35 |
| esphome | 34 |
| mobile_app | 26 |
| lutron_caseta | 22 |
| matter | 22 |
| tplink | 21 |
| hacs | 20 |
| input_select | 14 |

## Devices By Area

### Attic

#### Attic

- Device ID: `device_0ccd0eba4181`
- Integration: sensorpush_cloud
- Model: SensorPush HT1
- Capability mix: 8 telemetry, 0 control, 0 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `sensor.attic_altitude` | telemetry | sensorpush_cloud |  | disabled |
| `sensor.attic_atmospheric_pressure` | telemetry | sensorpush_cloud |  | disabled |
| `sensor.attic_battery_voltage` | telemetry | sensorpush_cloud |  | disabled |
| `sensor.attic_dew_point` | telemetry | sensorpush_cloud |  | disabled |
| `sensor.attic_humidity` | telemetry | sensorpush_cloud |  | available |
| `sensor.attic_signal_strength` | telemetry | sensorpush_cloud |  | disabled |
| `sensor.attic_temperature` | telemetry | sensorpush_cloud |  | available |
| `sensor.attic_vapor_pressure` | telemetry | sensorpush_cloud |  | disabled |

### Back Stairs

#### Back Stairs Back Stairs

- Device ID: `device_289d2bae593b`
- Integration: lutron_caseta
- Model: Lutron Electronics Co., Inc DVRF-6L (DivaSmartDimmer)
- Capability mix: 0 telemetry, 1 control, 0 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `light.back_stairs_back_stairs` | control | lutron_caseta |  | available |

### Back Yard

#### Back Patio

- Device ID: `device_fba4253633e3`
- Integration: ring
- Model: Ring Spotlight Cam Wired
- Capability mix: 6 telemetry, 4 control, 0 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `camera.back_patio_live_view` | telemetry | ring |  | available |
| `event.back_patio_motion` | telemetry | ring |  | available |
| `light.back_patio_light` | control | ring |  | available |
| `number.back_patio_volume` | control | ring |  | available |
| `sensor.back_patio_battery` | telemetry | ring | diagnostic | available |
| `sensor.back_patio_last_activity` | telemetry | ring |  | available |
| `sensor.back_patio_signal_strength` | telemetry | ring | diagnostic | disabled |
| `sensor.back_patio_wi_fi_signal_category` | telemetry | ring | diagnostic | disabled |
| `siren.back_patio_siren` | control | ring |  | available |
| `switch.back_patio_motion_detection` | control | ring |  | available |

### Basement

#### Basement Air Quality

- Device ID: `device_6b447073c190`
- Integration: airthings
- Model: Airthings View Radon
- Capability mix: 4 telemetry, 0 control, 0 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `sensor.basement_air_quality_battery` | telemetry | airthings | diagnostic | available |
| `sensor.basement_air_quality_humidity` | telemetry | airthings |  | available |
| `sensor.basement_air_quality_radon` | telemetry | airthings |  | available |
| `sensor.basement_air_quality_temperature` | telemetry | airthings |  | available |

#### Basement Ejector - Leak Detection

- Device ID: `device_42a5e06ebdf7`
- Integration: flo, unifi
- Model: Flo by Moen puck_v1
- Capability mix: 4 telemetry, 0 control, 1 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `binary_sensor.basement_ejector_leak_detection_water_detected` | telemetry | flo |  | available |
| `device_tracker.basement_ejector_leak_detection_espressif` | network | unifi | diagnostic | available |
| `sensor.basement_ejector_leak_detection_battery` | telemetry | flo |  | available |
| `sensor.basement_ejector_leak_detection_humidity` | telemetry | flo |  | available |
| `sensor.basement_ejector_leak_detection_temperature` | telemetry | flo |  | available |

#### Wine Cave

- Device ID: `device_dfed0d9dd820`
- Integration: sensorpush_cloud
- Model: SensorPush HT.w
- Capability mix: 8 telemetry, 0 control, 0 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `sensor.wine_altitude` | telemetry | sensorpush_cloud |  | disabled |
| `sensor.wine_atmospheric_pressure` | telemetry | sensorpush_cloud |  | disabled |
| `sensor.wine_battery_voltage` | telemetry | sensorpush_cloud |  | disabled |
| `sensor.wine_dew_point` | telemetry | sensorpush_cloud |  | disabled |
| `sensor.wine_humidity` | telemetry | sensorpush_cloud |  | available |
| `sensor.wine_signal_strength` | telemetry | sensorpush_cloud |  | disabled |
| `sensor.wine_temperature` | telemetry | sensorpush_cloud |  | available |
| `sensor.wine_vapor_pressure` | telemetry | sensorpush_cloud |  | disabled |

### Deck

#### Deck Deck Lights

- Device ID: `device_e39749ff5aa3`
- Integration: lutron_caseta
- Model: Lutron Electronics Co., Inc DVRF-6L (DivaSmartDimmer)
- Capability mix: 0 telemetry, 1 control, 0 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `light.deck_deck_lights` | control | lutron_caseta |  | available |

### Dining Room

#### Dining Room Thermostat

- Device ID: `device_fe017352418f`
- Integration: homekit_controller
- Model: ecobee Inc. ECB601
- Capability mix: 4 telemetry, 6 control, 0 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `binary_sensor.dining_room_motion` | telemetry | homekit_controller |  | available |
| `binary_sensor.dining_room_occupancy` | telemetry | homekit_controller |  | available |
| `button.dining_room_clear_hold` | control | homekit_controller |  | unknown |
| `button.dining_room_identify` | control | homekit_controller | diagnostic | unknown |
| `climate.dining_room` | control | homekit_controller |  | available |
| `select.dining_room_current_mode` | control | homekit_controller |  | unknown |
| `select.dining_room_temperature_display_units` | control | homekit_controller | config | available |
| `sensor.dining_room_current_humidity` | telemetry | homekit_controller |  | available |
| `sensor.dining_room_current_temperature` | telemetry | homekit_controller |  | available |
| `switch.dining_room_mute` | control | homekit_controller | config | available |

#### Main Floor 2

- Device ID: `device_1b1cd5daf7c5`
- Integration: sensorpush_cloud
- Model: SensorPush HT1
- Capability mix: 8 telemetry, 0 control, 0 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `sensor.main_floor_2_humidity` | telemetry | sensorpush_cloud |  | available |
| `sensor.main_floor_2_temperature` | telemetry | sensorpush_cloud |  | available |
| `sensor.sake_new_altitude` | telemetry | sensorpush_cloud |  | disabled |
| `sensor.sake_new_atmospheric_pressure` | telemetry | sensorpush_cloud |  | disabled |
| `sensor.sake_new_battery_voltage` | telemetry | sensorpush_cloud |  | disabled |
| `sensor.sake_new_dew_point` | telemetry | sensorpush_cloud |  | disabled |
| `sensor.sake_new_signal_strength` | telemetry | sensorpush_cloud |  | disabled |
| `sensor.sake_new_vapor_pressure` | telemetry | sensorpush_cloud |  | disabled |

### Electrical Room

#### Bonticou Gateway

- Device ID: `device_582d95951335`
- Integration: unifi, unifiprotect
- Model: Ubiquiti Networks UDMA6A8
- Capability mix: 35 telemetry, 12 control, 1 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `binary_sensor.bonticou_gateway_ssd_1` | telemetry | unifiprotect | diagnostic | available |
| `button.bonticou_gateway_port_4_power_cycle` | control | unifi | config | unknown |
| `button.bonticou_gateway_restart` | control | unifi | config | unknown |
| `device_tracker.bonticou_gateway` | network | unifi | diagnostic | available |
| `sensor.bonticou_gateway_bonticou_gateway_cpu_temperature` | telemetry | unifi | diagnostic | disabled |
| `sensor.bonticou_gateway_bonticou_gateway_local_temperature` | telemetry | unifi | diagnostic | disabled |
| `sensor.bonticou_gateway_clients` | telemetry | unifi | diagnostic | disabled |
| `sensor.bonticou_gateway_cloudflare_wan2_latency` | telemetry | unifi | diagnostic | disabled |
| `sensor.bonticou_gateway_cloudflare_wan_latency` | telemetry | unifi | diagnostic | disabled |
| `sensor.bonticou_gateway_cpu_temperature` | telemetry | unifiprotect | diagnostic | disabled |
| `sensor.bonticou_gateway_cpu_utilization` | telemetry | unifiprotect | diagnostic | disabled |
| `sensor.bonticou_gateway_cpu_utilization_2` | telemetry | unifi | diagnostic | available |
| `sensor.bonticou_gateway_google_wan2_latency` | telemetry | unifi | diagnostic | disabled |
| `sensor.bonticou_gateway_google_wan_latency` | telemetry | unifi | diagnostic | disabled |
| `sensor.bonticou_gateway_memory_utilization` | telemetry | unifiprotect | diagnostic | disabled |
| `sensor.bonticou_gateway_memory_utilization_2` | telemetry | unifi | diagnostic | available |
| `sensor.bonticou_gateway_microsoft_wan2_latency` | telemetry | unifi | diagnostic | disabled |
| `sensor.bonticou_gateway_microsoft_wan_latency` | telemetry | unifi | diagnostic | disabled |
| `sensor.bonticou_gateway_port_1_link_speed` | telemetry | unifi | diagnostic | disabled |
| `sensor.bonticou_gateway_port_2_link_speed` | telemetry | unifi | diagnostic | disabled |
| `sensor.bonticou_gateway_port_3_link_speed` | telemetry | unifi | diagnostic | disabled |
| `sensor.bonticou_gateway_port_4_link_speed` | telemetry | unifi | diagnostic | disabled |
| `sensor.bonticou_gateway_port_4_poe_power` | telemetry | unifi | diagnostic | disabled |
| `sensor.bonticou_gateway_port_5_link_speed` | telemetry | unifi | diagnostic | disabled |
| `sensor.bonticou_gateway_recording_capacity` | telemetry | unifiprotect | diagnostic | available |
| `sensor.bonticou_gateway_resolution_4k_video` | telemetry | unifiprotect | diagnostic | unknown |
| `sensor.bonticou_gateway_resolution_free_space` | telemetry | unifiprotect | diagnostic | unknown |
| `sensor.bonticou_gateway_resolution_hd_video` | telemetry | unifiprotect | diagnostic | unknown |
| `sensor.bonticou_gateway_sfp_1_link_speed` | telemetry | unifi | diagnostic | disabled |
| `sensor.bonticou_gateway_sfp_2_link_speed` | telemetry | unifi | diagnostic | disabled |
| `sensor.bonticou_gateway_state` | telemetry | unifi | diagnostic | available |
| `sensor.bonticou_gateway_storage_utilization` | telemetry | unifiprotect | diagnostic | available |
| `sensor.bonticou_gateway_type_continuous_video` | telemetry | unifiprotect | diagnostic | available |
| `sensor.bonticou_gateway_type_detections_video` | telemetry | unifiprotect | diagnostic | available |
| `sensor.bonticou_gateway_type_timelapse_video` | telemetry | unifiprotect | diagnostic | available |
| `sensor.bonticou_gateway_uptime` | telemetry | unifiprotect | diagnostic | available |
| `sensor.bonticou_gateway_uptime_2` | telemetry | unifi | diagnostic | available |
| `switch.bonticou_gateway_analytics_enabled` | control | unifiprotect | config | available |
| `switch.bonticou_gateway_insights_enabled` | control | unifiprotect | config | available |
| `switch.bonticou_gateway_port_1` | control | unifi | config | disabled |
| `switch.bonticou_gateway_port_2` | control | unifi | config | disabled |
| `switch.bonticou_gateway_port_3` | control | unifi | config | disabled |
| `switch.bonticou_gateway_port_4` | control | unifi | config | disabled |
| `switch.bonticou_gateway_port_4_poe` | control | unifi | config | disabled |
| `switch.bonticou_gateway_port_5` | control | unifi | config | disabled |
| `switch.bonticou_gateway_sfp_1` | control | unifi | config | disabled |
| `switch.bonticou_gateway_sfp_2` | control | unifi | config | disabled |
| `update.bonticou_gateway` | telemetry | unifi | config | available |

#### Electrical Room - Leak Detection

- Device ID: `device_d82102de874c`
- Integration: flo, unifi
- Model: Flo by Moen puck_v1
- Capability mix: 4 telemetry, 0 control, 1 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `binary_sensor.electrical_room_leak_detection_water_detected` | telemetry | flo |  | available |
| `device_tracker.electrical_room_leak_detection_espressif` | network | unifi | diagnostic | available |
| `sensor.electrical_room_leak_detection_battery` | telemetry | flo |  | available |
| `sensor.electrical_room_leak_detection_humidity` | telemetry | flo |  | available |
| `sensor.electrical_room_leak_detection_temperature` | telemetry | flo |  | available |

#### Fios Router

- Device ID: `device_3995819518d9`
- Integration: upnp
- Model: Verizon G3100
- Capability mix: 12 telemetry, 0 control, 0 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `binary_sensor.fios_router_wan_status` | telemetry | upnp | diagnostic | unavailable |
| `sensor.fios_router_data_received` | telemetry | upnp |  | disabled |
| `sensor.fios_router_data_sent` | telemetry | upnp |  | disabled |
| `sensor.fios_router_external_ip` | telemetry | upnp | diagnostic | unavailable |
| `sensor.fios_router_number_of_port_mapping_entries_ipv4` | telemetry | upnp | diagnostic | disabled |
| `sensor.fios_router_packet_download_speed` | telemetry | upnp |  | disabled |
| `sensor.fios_router_packet_upload_speed` | telemetry | upnp |  | disabled |
| `sensor.fios_router_packets_received` | telemetry | upnp |  | disabled |
| `sensor.fios_router_packets_sent` | telemetry | upnp |  | disabled |
| `sensor.fios_router_upload_speed` | telemetry | upnp |  | unavailable |
| `sensor.fios_router_uptime` | telemetry | upnp | diagnostic | disabled |
| `sensor.fios_router_wan_status` | telemetry | upnp | diagnostic | disabled |

### Exterior

#### Exterior Yard Lights

- Device ID: `device_8aefb3b9d963`
- Integration: lutron_caseta
- Model: Lutron Electronics Co., Inc DVRF-6L (DivaSmartDimmer)
- Capability mix: 0 telemetry, 1 control, 0 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `light.exterior_yard_lights` | control | lutron_caseta |  | available |

### Family Room

#### Family Room

- Device ID: `device_dc0447a8354b`
- Integration: sonos, unifi
- Model: Sonos Arc Ultra
- Capability mix: 2 telemetry, 18 control, 1 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `binary_sensor.family_room_microphone` | telemetry | sonos | diagnostic | available |
| `device_tracker.sonoszp_6` | network | unifi | diagnostic | available |
| `media_player.family_room` | control | sonos |  | available |
| `number.family_room_audio_delay` | control | sonos | config | available |
| `number.family_room_balance` | control | sonos | config | available |
| `number.family_room_bass` | control | sonos | config | available |
| `number.family_room_music_surround_level` | control | sonos | config | available |
| `number.family_room_sub_gain` | control | sonos | config | available |
| `number.family_room_surround_level` | control | sonos | config | available |
| `number.family_room_treble` | control | sonos | config | available |
| `select.family_room_speech_enhancement` | control | sonos |  | available |
| `sensor.family_room_audio_input_format` | telemetry | sonos | diagnostic | available |
| `switch.family_room_crossfade` | control | sonos | config | available |
| `switch.family_room_loudness` | control | sonos | config | available |
| `switch.family_room_night_sound` | control | sonos | config | available |
| `switch.family_room_speech_enhancement` | control | sonos | config | available |
| `switch.family_room_status_light` | control | sonos | config | disabled |
| `switch.family_room_subwoofer_enabled` | control | sonos | config | available |
| `switch.family_room_surround_enabled` | control | sonos | config | available |
| `switch.family_room_surround_music_full_volume` | control | sonos | config | available |
| `switch.family_room_touch_controls` | control | sonos | config | disabled |

#### Family Room Frame TV

- Device ID: `device_01ce0ac533c7`
- Integration: samsungtv, unifi
- Model: Samsung QN65LS03FWFXZA
- Capability mix: 1 telemetry, 2 control, 1 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `device_tracker.family_room_frame_tv` | network | unifi | diagnostic | available |
| `media_player.family_room_frame_tv` | control | samsungtv |  | available |
| `remote.family_room_frame_tv` | control | samsungtv |  | available |
| `sensor.link_speed_21` | telemetry | unifi | diagnostic | disabled |

#### Family Room Main Lights 1

- Device ID: `device_e86078f908e1`
- Integration: lutron_caseta
- Model: Lutron Electronics Co., Inc DVRF-6L (DivaSmartDimmer)
- Capability mix: 0 telemetry, 1 control, 0 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `light.family_room_main_lights_1` | control | lutron_caseta |  | available |

#### Family Room Main Lights 2

- Device ID: `device_0d6303456418`
- Integration: lutron_caseta
- Model: Lutron Electronics Co., Inc DVRF-6L (DivaSmartDimmer)
- Capability mix: 0 telemetry, 1 control, 0 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `light.family_room_main_lights_2` | control | lutron_caseta |  | available |

#### Family Room Main Lights 3

- Device ID: `device_a26e1b05eb6b`
- Integration: lutron_caseta
- Model: Lutron Electronics Co., Inc DVRF-6L (DivaSmartDimmer)
- Capability mix: 0 telemetry, 1 control, 0 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `light.family_room_main_lights_3` | control | lutron_caseta |  | available |

#### Main Floor

- Device ID: `device_26607127a43f`
- Integration: sensorpush_cloud
- Model: SensorPush HT1
- Capability mix: 8 telemetry, 0 control, 0 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `sensor.main_floor_altitude` | telemetry | sensorpush_cloud |  | disabled |
| `sensor.main_floor_atmospheric_pressure` | telemetry | sensorpush_cloud |  | disabled |
| `sensor.main_floor_battery_voltage` | telemetry | sensorpush_cloud |  | disabled |
| `sensor.main_floor_dew_point` | telemetry | sensorpush_cloud |  | disabled |
| `sensor.main_floor_humidity` | telemetry | sensorpush_cloud |  | available |
| `sensor.main_floor_signal_strength` | telemetry | sensorpush_cloud |  | disabled |
| `sensor.main_floor_temperature` | telemetry | sensorpush_cloud |  | available |
| `sensor.main_floor_vapor_pressure` | telemetry | sensorpush_cloud |  | disabled |

#### Smart Bridge 2

- Device ID: `device_aa3c678af681`
- Integration: lutron_caseta
- Model: Lutron Electronics Co., Inc L-BDG2-WH (SmartBridge)
- Capability mix: 0 telemetry, 1 control, 0 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `switch.unassigned_smart_away` | control | lutron_caseta |  | available |

#### Uplight

- Device ID: `device_2be02e8f001e`
- Integration: tplink, unifi
- Model: TP-Link EP25
- Capability mix: 15 telemetry, 7 control, 1 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `binary_sensor.uplight_cloud_connection` | telemetry | tplink | diagnostic | available |
| `binary_sensor.uplight_overheated` | telemetry | tplink | diagnostic | available |
| `binary_sensor.uplight_overloaded` | telemetry | tplink | diagnostic | available |
| `button.uplight_restart` | control | tplink | diagnostic | disabled |
| `device_tracker.unifi_default_mac_4e99000aad0a` | network | unifi | diagnostic | available |
| `number.uplight_power_protection` | control | tplink | config | available |
| `number.uplight_turn_off_in` | control | tplink | config | available |
| `sensor.link_speed_22` | telemetry | unifi | diagnostic | disabled |
| `sensor.uplight_auto_off_at` | telemetry | tplink | diagnostic | unknown |
| `sensor.uplight_current` | telemetry | tplink |  | available |
| `sensor.uplight_current_consumption` | telemetry | tplink |  | available |
| `sensor.uplight_device_time` | telemetry | tplink | diagnostic | disabled |
| `sensor.uplight_on_since` | telemetry | tplink | diagnostic | disabled |
| `sensor.uplight_signal_level` | telemetry | tplink | diagnostic | available |
| `sensor.uplight_signal_strength` | telemetry | tplink | diagnostic | disabled |
| `sensor.uplight_ssid` | telemetry | tplink | diagnostic | disabled |
| `sensor.uplight_this_month_s_consumption` | telemetry | tplink | diagnostic | available |
| `sensor.uplight_today_s_consumption` | telemetry | tplink | diagnostic | available |
| `sensor.uplight_voltage` | telemetry | tplink |  | available |
| `switch.uplight` | control | tplink |  | available |
| `switch.uplight_auto_off_enabled` | control | tplink | config | available |
| `switch.uplight_auto_update_enabled` | control | tplink | config | available |
| `switch.uplight_led` | control | tplink | config | available |

### Family Room TV

#### Family Room TV

- Device ID: `device_f5a5522ed109`
- Integration: apple_tv
- Model: Apple Apple TV 4K
- Capability mix: 0 telemetry, 2 control, 0 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `media_player.family_room_tv_2` | control | apple_tv |  | available |
| `remote.family_room_tv` | control | apple_tv |  | available |

### Front Door

#### Front Door

- Device ID: `device_bd9feeb41bd1`
- Integration: ring
- Model: Ring Doorbell Pro 2
- Capability mix: 7 telemetry, 3 control, 0 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `camera.front_door_live_view` | telemetry | ring |  | available |
| `event.front_door_ding` | telemetry | ring |  | available |
| `event.front_door_motion` | telemetry | ring |  | available |
| `number.front_door_volume` | control | ring |  | available |
| `sensor.front_door_battery` | telemetry | ring | diagnostic | unknown |
| `sensor.front_door_last_activity` | telemetry | ring |  | available |
| `sensor.front_door_signal_strength` | telemetry | ring | diagnostic | disabled |
| `sensor.front_door_wi_fi_signal_category` | telemetry | ring | diagnostic | disabled |
| `switch.front_door_in_home_chime` | control | ring |  | available |
| `switch.front_door_motion_detection` | control | ring |  | available |

### Front Foyer

#### Front Foyer Ceiling Lights

- Device ID: `device_bc242f727014`
- Integration: lutron_caseta
- Model: Lutron Electronics Co., Inc DVRF-6L (DivaSmartDimmer)
- Capability mix: 0 telemetry, 1 control, 0 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `light.front_foyer_ceiling_lights` | control | lutron_caseta |  | available |

#### Front Foyer Chandelier

- Device ID: `device_3f88436ece9e`
- Integration: lutron_caseta
- Model: Lutron Electronics Co., Inc DVRF-6L (DivaSmartDimmer)
- Capability mix: 0 telemetry, 1 control, 0 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `light.front_foyer_chandelier` | control | lutron_caseta |  | available |

#### Front Foyer Sconces

- Device ID: `device_b0bcbe9d9a0e`
- Integration: lutron_caseta
- Model: Lutron Electronics Co., Inc DVRF-5NS (DivaSmartSwitch)
- Capability mix: 0 telemetry, 1 control, 0 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `switch.front_foyer_sconces` | control | lutron_caseta |  | available |

### Front Yard

#### Wynn's Room

- Device ID: `device_ca0387716233`
- Integration: unifi, unifiprotect
- Model: Ubiquiti G6 Instant
- Capability mix: 27 telemetry, 32 control, 1 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `binary_sensor.wynn_s_room_animal_detected` | telemetry | unifiprotect |  | available |
| `binary_sensor.wynn_s_room_audio_object_detected` | telemetry | unifiprotect |  | disabled |
| `binary_sensor.wynn_s_room_baby_cry_detected` | telemetry | unifiprotect |  | available |
| `binary_sensor.wynn_s_room_barking_detected` | telemetry | unifiprotect |  | available |
| `binary_sensor.wynn_s_room_car_alarm_detected` | telemetry | unifiprotect |  | available |
| `binary_sensor.wynn_s_room_car_horn_detected` | telemetry | unifiprotect |  | available |
| `binary_sensor.wynn_s_room_co_alarm_detected` | telemetry | unifiprotect |  | available |
| `binary_sensor.wynn_s_room_glass_break_detected` | telemetry | unifiprotect |  | available |
| `binary_sensor.wynn_s_room_is_dark` | telemetry | unifiprotect |  | available |
| `binary_sensor.wynn_s_room_motion` | telemetry | unifiprotect |  | available |
| `binary_sensor.wynn_s_room_object_detected` | telemetry | unifiprotect |  | disabled |
| `binary_sensor.wynn_s_room_person_detected` | telemetry | unifiprotect |  | available |
| `binary_sensor.wynn_s_room_siren_detected` | telemetry | unifiprotect |  | available |
| `binary_sensor.wynn_s_room_smoke_alarm_detected` | telemetry | unifiprotect |  | available |
| `binary_sensor.wynn_s_room_speaking_detected` | telemetry | unifiprotect |  | available |
| `binary_sensor.wynn_s_room_vehicle_detected` | telemetry | unifiprotect |  | available |
| `button.wynn_s_room_restart` | control | unifiprotect |  | disabled |
| `button.wynn_s_room_unadopt_device` | control | unifiprotect |  | disabled |
| `camera.wynn_s_room_high_resolution_channel` | telemetry | unifiprotect |  | available |
| `camera.wynn_s_room_high_resolution_channel_insecure` | telemetry | unifiprotect |  | disabled |
| `device_tracker.wynns_room` | network | unifi | diagnostic | available |
| `event.wynn_s_room_vehicle` | telemetry | unifiprotect |  | available |
| `media_player.wynn_s_room_speaker` | control | unifiprotect |  | available |
| `number.wynn_s_room_infrared_custom_lux_trigger` | control | unifiprotect | config | unavailable |
| `number.wynn_s_room_microphone_level` | control | unifiprotect | config | available |
| `number.wynn_s_room_system_sounds_volume` | control | unifiprotect | config | available |
| `select.wynn_s_room_hdr_mode` | control | unifiprotect | config | available |
| `select.wynn_s_room_infrared_mode` | control | unifiprotect | config | available |
| `select.wynn_s_room_recording_mode` | control | unifiprotect | config | available |
| `sensor.wynn_s_room_disk_write_rate` | telemetry | unifiprotect | diagnostic | available |
| `sensor.wynn_s_room_last_motion_detected` | telemetry | unifiprotect |  | disabled |
| `sensor.wynn_s_room_oldest_recording` | telemetry | unifiprotect | diagnostic | disabled |
| `sensor.wynn_s_room_received_data` | telemetry | unifiprotect | diagnostic | disabled |
| `sensor.wynn_s_room_storage_used` | telemetry | unifiprotect | diagnostic | available |
| `sensor.wynn_s_room_transferred_data` | telemetry | unifiprotect | diagnostic | disabled |
| `sensor.wynn_s_room_uptime` | telemetry | unifiprotect | diagnostic | disabled |
| `sensor.wynn_s_room_wi_fi_signal_strength` | telemetry | unifiprotect | diagnostic | disabled |
| `switch.wynn_s_room_animal_detection` | control | unifiprotect | config | available |
| `switch.wynn_s_room_baby_cry_detection` | control | unifiprotect | config | available |
| `switch.wynn_s_room_car_alarm_detection` | control | unifiprotect | config | available |
| `switch.wynn_s_room_car_horn_detection` | control | unifiprotect | config | available |
| `switch.wynn_s_room_co_alarm_detection` | control | unifiprotect | config | available |
| `switch.wynn_s_room_glass_break_detection` | control | unifiprotect | config | available |
| `switch.wynn_s_room_hdr_mode` | control | unifiprotect | config | disabled |
| `switch.wynn_s_room_license_plate_detection` | control | unifiprotect | config | available |
| `switch.wynn_s_room_motion` | control | unifiprotect | config | available |
| `switch.wynn_s_room_none` | control | unifiprotect | config | available |
| `switch.wynn_s_room_overlay_show_date` | control | unifiprotect | config | available |
| `switch.wynn_s_room_overlay_show_logo` | control | unifiprotect | config | available |
| `switch.wynn_s_room_overlay_show_name` | control | unifiprotect | config | available |
| `switch.wynn_s_room_overlay_show_nerd_mode` | control | unifiprotect | config | available |
| `switch.wynn_s_room_person_detection` | control | unifiprotect | config | available |
| `switch.wynn_s_room_privacy_mode` | control | unifiprotect | config | available |
| `switch.wynn_s_room_siren_detection` | control | unifiprotect | config | available |
| `switch.wynn_s_room_smoke_detection` | control | unifiprotect | config | available |
| `switch.wynn_s_room_speaking_detection` | control | unifiprotect | config | available |
| `switch.wynn_s_room_ssh_enabled` | control | unifiprotect | config | disabled |
| `switch.wynn_s_room_status_light_2` | control | unifiprotect | config | available |
| `switch.wynn_s_room_system_sounds` | control | unifiprotect | config | available |
| `switch.wynn_s_room_vehicle_detection` | control | unifiprotect | config | available |

### Garage

#### Garage

- Device ID: `device_cb1e19da3f33`
- Integration: sensorpush_cloud
- Model: SensorPush HT1
- Capability mix: 8 telemetry, 0 control, 0 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `sensor.garage_altitude` | telemetry | sensorpush_cloud |  | disabled |
| `sensor.garage_atmospheric_pressure` | telemetry | sensorpush_cloud |  | disabled |
| `sensor.garage_battery_voltage` | telemetry | sensorpush_cloud |  | disabled |
| `sensor.garage_dew_point` | telemetry | sensorpush_cloud |  | disabled |
| `sensor.garage_humidity` | telemetry | sensorpush_cloud |  | available |
| `sensor.garage_signal_strength` | telemetry | sensorpush_cloud |  | disabled |
| `sensor.garage_temperature` | telemetry | sensorpush_cloud |  | available |
| `sensor.garage_vapor_pressure` | telemetry | sensorpush_cloud |  | disabled |

#### Garage Entry Lock

- Device ID: `device_ab2b71f3a01a`
- Integration: matter
- Model: Aqara Aqara Smart Lock U100
- Capability mix: 4 telemetry, 3 control, 0 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `binary_sensor.garage_entry_lock_actuator` | telemetry | matter | diagnostic | available |
| `button.garage_entry_lock_identify` | control | matter | diagnostic | unknown |
| `lock.garage_entry_lock` | control | matter |  | available |
| `select.garage_entry_lock_operating_mode` | control | matter | config | available |
| `sensor.garage_entry_lock_battery` | telemetry | matter | diagnostic | available |
| `sensor.garage_entry_lock_battery_type` | telemetry | matter | diagnostic | available |
| `sensor.garage_entry_lock_battery_voltage` | telemetry | matter | diagnostic | available |

### Great Room Speakers

#### Great Room Sonos

- Device ID: `device_96c096ed4a91`
- Integration: sonos, unifi
- Model: Sonos Era 300
- Capability mix: 1 telemetry, 8 control, 1 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `binary_sensor.great_room_speakers_microphone` | telemetry | sonos | diagnostic | available |
| `device_tracker.sonoszp_7` | network | unifi | diagnostic | available |
| `media_player.great_room_speakers` | control | sonos |  | available |
| `number.great_room_speakers_balance` | control | sonos | config | available |
| `number.great_room_speakers_bass` | control | sonos | config | available |
| `number.great_room_speakers_treble` | control | sonos | config | available |
| `switch.great_room_speakers_crossfade` | control | sonos | config | available |
| `switch.great_room_speakers_loudness` | control | sonos | config | available |
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
| `binary_sensor.dishwasher_leak_detection_water_detected` | telemetry | flo |  | available |
| `device_tracker.dishwasher_leak_detection_espressif` | network | unifi | diagnostic | available |
| `sensor.dishwasher_leak_detection_battery` | telemetry | flo |  | available |
| `sensor.dishwasher_leak_detection_humidity` | telemetry | flo |  | available |
| `sensor.dishwasher_leak_detection_temperature` | telemetry | flo |  | available |

#### Island Sink - Leak Detection

- Device ID: `device_52ba6957f618`
- Integration: flo, unifi
- Model: Flo by Moen puck_v1
- Capability mix: 5 telemetry, 0 control, 1 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `binary_sensor.island_sink_leak_detection_water_detected` | telemetry | flo |  | available |
| `device_tracker.island_sink_leak_detection_espressif` | network | unifi | diagnostic | available |
| `sensor.espressif_link_speed_3` | telemetry | unifi | diagnostic | disabled |
| `sensor.island_sink_leak_detection_battery` | telemetry | flo |  | available |
| `sensor.island_sink_leak_detection_humidity` | telemetry | flo |  | available |
| `sensor.island_sink_leak_detection_temperature` | telemetry | flo |  | available |

#### Kitchen Fridge - Leak Detection

- Device ID: `device_4fc75f38e213`
- Integration: flo, unifi
- Model: Flo by Moen puck_v1
- Capability mix: 5 telemetry, 0 control, 1 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `binary_sensor.kitchen_fridge_leak_detection_water_detected` | telemetry | flo |  | available |
| `device_tracker.kitchen_fridge_leak_detection_espressif` | network | unifi | diagnostic | available |
| `sensor.espressif_link_speed_5` | telemetry | unifi | diagnostic | disabled |
| `sensor.kitchen_fridge_leak_detection_battery` | telemetry | flo |  | available |
| `sensor.kitchen_fridge_leak_detection_humidity` | telemetry | flo |  | available |
| `sensor.kitchen_fridge_leak_detection_temperature` | telemetry | flo |  | available |

#### Kitchen Sink - Leak Detection

- Device ID: `device_937c61cbde64`
- Integration: flo, unifi
- Model: Flo by Moen puck_v1
- Capability mix: 5 telemetry, 0 control, 1 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `binary_sensor.kitchen_sink_leak_detection_water_detected` | telemetry | flo |  | available |
| `device_tracker.kitchen_sink_leak_detection_espressif` | network | unifi | diagnostic | available |
| `sensor.espressif_link_speed_2` | telemetry | unifi | diagnostic | disabled |
| `sensor.kitchen_sink_leak_detection_battery` | telemetry | flo |  | available |
| `sensor.kitchen_sink_leak_detection_humidity` | telemetry | flo |  | available |
| `sensor.kitchen_sink_leak_detection_temperature` | telemetry | flo |  | available |

### Kitchen Speakers

#### Kitchen Sonos

- Device ID: `device_df07ddeb668b`
- Integration: sonos, unifi
- Model: Sonos Era 100
- Capability mix: 1 telemetry, 8 control, 1 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `binary_sensor.kitchen_speakers_microphone` | telemetry | sonos | diagnostic | available |
| `device_tracker.sonoszp` | network | unifi | diagnostic | available |
| `media_player.kitchen_speakers` | control | sonos |  | available |
| `number.kitchen_speakers_balance` | control | sonos | config | available |
| `number.kitchen_speakers_bass` | control | sonos | config | available |
| `number.kitchen_speakers_treble` | control | sonos | config | available |
| `switch.kitchen_speakers_crossfade` | control | sonos | config | available |
| `switch.kitchen_speakers_loudness` | control | sonos | config | available |
| `switch.kitchen_speakers_status_light` | control | sonos | config | disabled |
| `switch.kitchen_speakers_touch_controls` | control | sonos | config | disabled |

### Master

#### Master Bedroom

- Device ID: `device_92d8071e504b`
- Integration: sensorpush_cloud
- Model: SensorPush HT1
- Capability mix: 8 telemetry, 0 control, 0 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `sensor.master_altitude` | telemetry | sensorpush_cloud |  | disabled |
| `sensor.master_atmospheric_pressure` | telemetry | sensorpush_cloud |  | disabled |
| `sensor.master_battery_voltage` | telemetry | sensorpush_cloud |  | disabled |
| `sensor.master_dew_point` | telemetry | sensorpush_cloud |  | disabled |
| `sensor.master_humidity` | telemetry | sensorpush_cloud |  | available |
| `sensor.master_signal_strength` | telemetry | sensorpush_cloud |  | disabled |
| `sensor.master_temperature` | telemetry | sensorpush_cloud |  | available |
| `sensor.master_vapor_pressure` | telemetry | sensorpush_cloud |  | disabled |

#### Master Lantern

- Device ID: `device_de9e0458bd8b`
- Integration: lutron_caseta
- Model: Lutron Electronics Co., Inc PD-5WS-DV-XX (WallSwitch)
- Capability mix: 0 telemetry, 1 control, 0 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `switch.master_lantern` | control | lutron_caseta |  | available |

#### Master Thermostat

- Device ID: `device_22d9acd7ac2f`
- Integration: homekit_controller
- Model: ecobee Inc. ECB601
- Capability mix: 4 telemetry, 6 control, 0 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `binary_sensor.master_motion_2` | telemetry | homekit_controller |  | available |
| `binary_sensor.master_occupancy_2` | telemetry | homekit_controller |  | available |
| `button.master_clear_hold_2` | control | homekit_controller |  | available |
| `button.master_identify_2` | control | homekit_controller | diagnostic | unknown |
| `climate.master_2` | control | homekit_controller |  | available |
| `select.master_current_mode_2` | control | homekit_controller |  | available |
| `select.master_temperature_display_units_2` | control | homekit_controller | config | available |
| `sensor.master_current_humidity_2` | telemetry | homekit_controller |  | available |
| `sensor.master_current_temperature_2` | telemetry | homekit_controller |  | available |
| `switch.master_mute_2` | control | homekit_controller | config | available |

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

### Master Bathroom

#### Master Ecobee Sensor

- Device ID: `device_197b3d0ffca2`
- Integration: homekit_controller
- Model: ecobee Inc. EBERS41
- Capability mix: 4 telemetry, 1 control, 0 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `binary_sensor.master_sensor_new_motion_2` | telemetry | homekit_controller |  | available |
| `binary_sensor.master_sensor_new_occupancy_2` | telemetry | homekit_controller |  | available |
| `button.master_sensor_new_identify_2` | control | homekit_controller | diagnostic | unknown |
| `sensor.master_sensor_new_battery_2` | telemetry | homekit_controller | diagnostic | available |
| `sensor.master_sensor_new_temperature_2` | telemetry | homekit_controller |  | available |

### Master Bedroom

#### Master Bedroom Sconce L

- Device ID: `device_798e44b8b882`
- Integration: lutron_caseta
- Model: Lutron Electronics Co., Inc DVRF-6L (DivaSmartDimmer)
- Capability mix: 0 telemetry, 1 control, 0 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `light.master_bedroom_sconce_l` | control | lutron_caseta |  | available |

#### Master Bedroom Sconce R

- Device ID: `device_9d1d12bbe5ef`
- Integration: lutron_caseta
- Model: Lutron Electronics Co., Inc DVRF-6L (DivaSmartDimmer)
- Capability mix: 0 telemetry, 1 control, 0 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `light.master_bedroom_sconce_r` | control | lutron_caseta |  | available |

### Mechanical Room

#### Flo shutoff

- Device ID: `device_6444bcfdb6d0`
- Integration: flo, unifi
- Model: Flo by Moen flo_device_075_v2
- Capability mix: 7 telemetry, 1 control, 1 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `binary_sensor.flo_shutoff_pending_system_alerts` | telemetry | flo |  | available |
| `device_tracker.flo_d4e95ef8775b` | network | unifi | diagnostic | available |
| `sensor.flo_d4e95ef8775b_link_speed` | telemetry | unifi | diagnostic | disabled |
| `sensor.flo_shutoff_current_system_mode` | telemetry | flo |  | available |
| `sensor.flo_shutoff_today_s_water_usage` | telemetry | flo |  | available |
| `sensor.flo_shutoff_water_flow_rate` | telemetry | flo |  | available |
| `sensor.flo_shutoff_water_pressure` | telemetry | flo |  | available |
| `sensor.flo_shutoff_water_temperature` | telemetry | flo |  | available |
| `switch.flo_shutoff_shutoff_valve` | control | flo |  | available |

#### Mechanical Room

- Device ID: `device_e0835a8f890a`
- Integration: sensorpush_cloud
- Model: SensorPush HT1
- Capability mix: 8 telemetry, 0 control, 0 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `sensor.basement_altitude` | telemetry | sensorpush_cloud |  | disabled |
| `sensor.basement_atmospheric_pressure` | telemetry | sensorpush_cloud |  | disabled |
| `sensor.basement_battery_voltage` | telemetry | sensorpush_cloud |  | disabled |
| `sensor.basement_dew_point` | telemetry | sensorpush_cloud |  | disabled |
| `sensor.basement_signal_strength` | telemetry | sensorpush_cloud |  | disabled |
| `sensor.basement_vapor_pressure` | telemetry | sensorpush_cloud |  | disabled |
| `sensor.mechanical_room_humidity` | telemetry | sensorpush_cloud |  | available |
| `sensor.mechanical_room_temperature` | telemetry | sensorpush_cloud |  | available |

#### Mechanical Room - Leak Detection

- Device ID: `device_875d11919b1c`
- Integration: flo, unifi
- Model: Flo by Moen puck_v1
- Capability mix: 5 telemetry, 0 control, 1 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `binary_sensor.mechanical_room_leak_detection_water_detected` | telemetry | flo |  | available |
| `device_tracker.mechanical_room_leak_detection_espressif` | network | unifi | diagnostic | available |
| `sensor.espressif_link_speed` | telemetry | unifi | diagnostic | disabled |
| `sensor.mechanical_room_leak_detection_battery` | telemetry | flo |  | available |
| `sensor.mechanical_room_leak_detection_humidity` | telemetry | flo |  | available |
| `sensor.mechanical_room_leak_detection_temperature` | telemetry | flo |  | available |

#### Mechanical room

- Device ID: `device_a21ac907c776`
- Integration: unifi, unifiprotect
- Model: Ubiquiti G6 Instant
- Capability mix: 27 telemetry, 32 control, 1 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `binary_sensor.mechanical_room_animal_detected` | telemetry | unifiprotect |  | available |
| `binary_sensor.mechanical_room_audio_object_detected` | telemetry | unifiprotect |  | disabled |
| `binary_sensor.mechanical_room_baby_cry_detected` | telemetry | unifiprotect |  | available |
| `binary_sensor.mechanical_room_barking_detected` | telemetry | unifiprotect |  | available |
| `binary_sensor.mechanical_room_car_alarm_detected` | telemetry | unifiprotect |  | available |
| `binary_sensor.mechanical_room_car_horn_detected` | telemetry | unifiprotect |  | available |
| `binary_sensor.mechanical_room_co_alarm_detected` | telemetry | unifiprotect |  | available |
| `binary_sensor.mechanical_room_glass_break_detected` | telemetry | unifiprotect |  | available |
| `binary_sensor.mechanical_room_is_dark` | telemetry | unifiprotect |  | available |
| `binary_sensor.mechanical_room_motion` | telemetry | unifiprotect |  | available |
| `binary_sensor.mechanical_room_object_detected` | telemetry | unifiprotect |  | disabled |
| `binary_sensor.mechanical_room_person_detected` | telemetry | unifiprotect |  | available |
| `binary_sensor.mechanical_room_siren_detected` | telemetry | unifiprotect |  | available |
| `binary_sensor.mechanical_room_smoke_alarm_detected` | telemetry | unifiprotect |  | available |
| `binary_sensor.mechanical_room_speaking_detected` | telemetry | unifiprotect |  | available |
| `binary_sensor.mechanical_room_vehicle_detected` | telemetry | unifiprotect |  | available |
| `button.mechanical_room_restart` | control | unifiprotect |  | disabled |
| `button.mechanical_room_unadopt_device` | control | unifiprotect |  | disabled |
| `camera.mechanical_room_high_resolution_channel` | telemetry | unifiprotect |  | available |
| `camera.mechanical_room_high_resolution_channel_insecure` | telemetry | unifiprotect |  | disabled |
| `device_tracker.mechanical_room` | network | unifi | diagnostic | available |
| `event.mechanical_room_vehicle` | telemetry | unifiprotect |  | unknown |
| `media_player.mechanical_room_speaker` | control | unifiprotect |  | available |
| `number.mechanical_room_infrared_custom_lux_trigger` | control | unifiprotect | config | unavailable |
| `number.mechanical_room_microphone_level` | control | unifiprotect | config | available |
| `number.mechanical_room_system_sounds_volume` | control | unifiprotect | config | available |
| `select.mechanical_room_hdr_mode` | control | unifiprotect | config | available |
| `select.mechanical_room_infrared_mode` | control | unifiprotect | config | available |
| `select.mechanical_room_recording_mode` | control | unifiprotect | config | available |
| `sensor.mechanical_room_disk_write_rate` | telemetry | unifiprotect | diagnostic | available |
| `sensor.mechanical_room_last_motion_detected` | telemetry | unifiprotect |  | disabled |
| `sensor.mechanical_room_oldest_recording` | telemetry | unifiprotect | diagnostic | disabled |
| `sensor.mechanical_room_received_data` | telemetry | unifiprotect | diagnostic | disabled |
| `sensor.mechanical_room_storage_used` | telemetry | unifiprotect | diagnostic | available |
| `sensor.mechanical_room_transferred_data` | telemetry | unifiprotect | diagnostic | disabled |
| `sensor.mechanical_room_uptime` | telemetry | unifiprotect | diagnostic | disabled |
| `sensor.mechanical_room_wi_fi_signal_strength` | telemetry | unifiprotect | diagnostic | disabled |
| `switch.mechanical_room_animal_detection` | control | unifiprotect | config | available |
| `switch.mechanical_room_baby_cry_detection` | control | unifiprotect | config | available |
| `switch.mechanical_room_car_alarm_detection` | control | unifiprotect | config | available |
| `switch.mechanical_room_car_horn_detection` | control | unifiprotect | config | available |
| `switch.mechanical_room_co_alarm_detection` | control | unifiprotect | config | available |
| `switch.mechanical_room_glass_break_detection` | control | unifiprotect | config | available |
| `switch.mechanical_room_hdr_mode` | control | unifiprotect | config | disabled |
| `switch.mechanical_room_license_plate_detection` | control | unifiprotect | config | available |
| `switch.mechanical_room_motion` | control | unifiprotect | config | available |
| `switch.mechanical_room_none` | control | unifiprotect | config | available |
| `switch.mechanical_room_overlay_show_date` | control | unifiprotect | config | available |
| `switch.mechanical_room_overlay_show_logo` | control | unifiprotect | config | available |
| `switch.mechanical_room_overlay_show_name` | control | unifiprotect | config | available |
| `switch.mechanical_room_overlay_show_nerd_mode` | control | unifiprotect | config | available |
| `switch.mechanical_room_person_detection` | control | unifiprotect | config | available |
| `switch.mechanical_room_privacy_mode` | control | unifiprotect | config | available |
| `switch.mechanical_room_siren_detection` | control | unifiprotect | config | available |
| `switch.mechanical_room_smoke_detection` | control | unifiprotect | config | available |
| `switch.mechanical_room_speaking_detection` | control | unifiprotect | config | available |
| `switch.mechanical_room_ssh_enabled` | control | unifiprotect | config | disabled |
| `switch.mechanical_room_status_light` | control | unifiprotect | config | available |
| `switch.mechanical_room_system_sounds` | control | unifiprotect | config | available |
| `switch.mechanical_room_vehicle_detection` | control | unifiprotect | config | available |

### Mudroom

#### Back Stairs

- Device ID: `device_db65d45d11cd`
- Integration: ring
- Model: Ring Stick Up Cam (3rd Gen)
- Capability mix: 6 telemetry, 3 control, 0 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `camera.back_stairs_live_view` | telemetry | ring |  | unavailable |
| `event.back_stairs_motion` | telemetry | ring |  | unavailable |
| `number.back_stairs_volume` | control | ring |  | unavailable |
| `sensor.back_stairs_battery` | telemetry | ring | diagnostic | unavailable |
| `sensor.back_stairs_last_activity` | telemetry | ring |  | unavailable |
| `sensor.back_stairs_signal_strength` | telemetry | ring | diagnostic | disabled |
| `sensor.back_stairs_wi_fi_signal_category` | telemetry | ring | diagnostic | disabled |
| `siren.back_stairs_siren` | control | ring |  | unavailable |
| `switch.back_stairs_motion_detection` | control | ring |  | unavailable |

#### Laundry Sink - Leak Detection

- Device ID: `device_6f358bbfc961`
- Integration: flo, unifi
- Model: Flo by Moen puck_v1
- Capability mix: 5 telemetry, 0 control, 1 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `binary_sensor.laundry_sink_leak_detection_water_detected` | telemetry | flo |  | available |
| `device_tracker.laundry_sink_leak_detection_espressif` | network | unifi | diagnostic | available |
| `sensor.espressif_link_speed_4` | telemetry | unifi | diagnostic | disabled |
| `sensor.laundry_sink_leak_detection_battery` | telemetry | flo |  | available |
| `sensor.laundry_sink_leak_detection_humidity` | telemetry | flo |  | available |
| `sensor.laundry_sink_leak_detection_temperature` | telemetry | flo |  | available |

#### Mud room

- Device ID: `device_e5236ec8767c`
- Integration: unifi, unifiprotect
- Model: Ubiquiti G6 Instant
- Capability mix: 27 telemetry, 32 control, 1 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `binary_sensor.mud_room_animal_detected` | telemetry | unifiprotect |  | available |
| `binary_sensor.mud_room_audio_object_detected` | telemetry | unifiprotect |  | disabled |
| `binary_sensor.mud_room_baby_cry_detected` | telemetry | unifiprotect |  | available |
| `binary_sensor.mud_room_barking_detected` | telemetry | unifiprotect |  | available |
| `binary_sensor.mud_room_car_alarm_detected` | telemetry | unifiprotect |  | available |
| `binary_sensor.mud_room_car_horn_detected` | telemetry | unifiprotect |  | available |
| `binary_sensor.mud_room_co_alarm_detected` | telemetry | unifiprotect |  | available |
| `binary_sensor.mud_room_glass_break_detected` | telemetry | unifiprotect |  | available |
| `binary_sensor.mud_room_is_dark` | telemetry | unifiprotect |  | available |
| `binary_sensor.mud_room_motion` | telemetry | unifiprotect |  | available |
| `binary_sensor.mud_room_object_detected` | telemetry | unifiprotect |  | disabled |
| `binary_sensor.mud_room_person_detected` | telemetry | unifiprotect |  | available |
| `binary_sensor.mud_room_siren_detected` | telemetry | unifiprotect |  | available |
| `binary_sensor.mud_room_smoke_alarm_detected` | telemetry | unifiprotect |  | available |
| `binary_sensor.mud_room_speaking_detected` | telemetry | unifiprotect |  | available |
| `binary_sensor.mud_room_vehicle_detected` | telemetry | unifiprotect |  | available |
| `button.mud_room_restart` | control | unifiprotect |  | disabled |
| `button.mud_room_unadopt_device` | control | unifiprotect |  | disabled |
| `camera.mud_room_high_resolution_channel` | telemetry | unifiprotect |  | available |
| `camera.mud_room_high_resolution_channel_insecure` | telemetry | unifiprotect |  | disabled |
| `device_tracker.mud_room` | network | unifi | diagnostic | available |
| `event.mud_room_vehicle` | telemetry | unifiprotect |  | available |
| `media_player.mud_room_speaker` | control | unifiprotect |  | available |
| `number.mud_room_infrared_custom_lux_trigger` | control | unifiprotect | config | unavailable |
| `number.mud_room_microphone_level` | control | unifiprotect | config | available |
| `number.mud_room_system_sounds_volume` | control | unifiprotect | config | available |
| `select.mud_room_hdr_mode` | control | unifiprotect | config | available |
| `select.mud_room_infrared_mode` | control | unifiprotect | config | available |
| `select.mud_room_recording_mode` | control | unifiprotect | config | available |
| `sensor.mud_room_disk_write_rate` | telemetry | unifiprotect | diagnostic | available |
| `sensor.mud_room_last_motion_detected` | telemetry | unifiprotect |  | disabled |
| `sensor.mud_room_oldest_recording` | telemetry | unifiprotect | diagnostic | disabled |
| `sensor.mud_room_received_data` | telemetry | unifiprotect | diagnostic | disabled |
| `sensor.mud_room_storage_used` | telemetry | unifiprotect | diagnostic | available |
| `sensor.mud_room_transferred_data` | telemetry | unifiprotect | diagnostic | disabled |
| `sensor.mud_room_uptime` | telemetry | unifiprotect | diagnostic | disabled |
| `sensor.mud_room_wi_fi_signal_strength` | telemetry | unifiprotect | diagnostic | disabled |
| `switch.mud_room_animal_detection` | control | unifiprotect | config | available |
| `switch.mud_room_baby_cry_detection` | control | unifiprotect | config | available |
| `switch.mud_room_car_alarm_detection` | control | unifiprotect | config | available |
| `switch.mud_room_car_horn_detection` | control | unifiprotect | config | available |
| `switch.mud_room_co_alarm_detection` | control | unifiprotect | config | available |
| `switch.mud_room_glass_break_detection` | control | unifiprotect | config | available |
| `switch.mud_room_hdr_mode` | control | unifiprotect | config | disabled |
| `switch.mud_room_license_plate_detection` | control | unifiprotect | config | available |
| `switch.mud_room_motion` | control | unifiprotect | config | available |
| `switch.mud_room_none` | control | unifiprotect | config | available |
| `switch.mud_room_overlay_show_date` | control | unifiprotect | config | available |
| `switch.mud_room_overlay_show_logo` | control | unifiprotect | config | available |
| `switch.mud_room_overlay_show_name` | control | unifiprotect | config | available |
| `switch.mud_room_overlay_show_nerd_mode` | control | unifiprotect | config | available |
| `switch.mud_room_person_detection` | control | unifiprotect | config | available |
| `switch.mud_room_privacy_mode` | control | unifiprotect | config | available |
| `switch.mud_room_siren_detection` | control | unifiprotect | config | available |
| `switch.mud_room_smoke_detection` | control | unifiprotect | config | available |
| `switch.mud_room_speaking_detection` | control | unifiprotect | config | available |
| `switch.mud_room_ssh_enabled` | control | unifiprotect | config | disabled |
| `switch.mud_room_status_light` | control | unifiprotect | config | available |
| `switch.mud_room_system_sounds` | control | unifiprotect | config | available |
| `switch.mud_room_vehicle_detection` | control | unifiprotect | config | available |

#### Mudroom Door

- Device ID: `device_ece30c1a6455`
- Integration: ring
- Model: Ring Doorbell Pro 2
- Capability mix: 7 telemetry, 3 control, 0 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `camera.mudroom_door_live_view` | telemetry | ring |  | available |
| `event.mudroom_door_ding` | telemetry | ring |  | available |
| `event.mudroom_door_motion` | telemetry | ring |  | available |
| `number.mudroom_door_volume` | control | ring |  | available |
| `sensor.mudroom_door_battery` | telemetry | ring | diagnostic | unknown |
| `sensor.mudroom_door_last_activity` | telemetry | ring |  | available |
| `sensor.mudroom_door_signal_strength` | telemetry | ring | diagnostic | disabled |
| `sensor.mudroom_door_wi_fi_signal_category` | telemetry | ring | diagnostic | disabled |
| `switch.mudroom_door_in_home_chime` | control | ring |  | available |
| `switch.mudroom_door_motion_detection` | control | ring |  | available |

#### Mudroom Door Lock

- Device ID: `device_bf15aa774d53`
- Integration: matter
- Model: Aqara Aqara Smart Lock U100
- Capability mix: 4 telemetry, 3 control, 0 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `binary_sensor.mudroom_door_lock_actuator` | telemetry | matter | diagnostic | available |
| `button.mudroom_door_lock_identify` | control | matter | diagnostic | unknown |
| `lock.mudroom_door_lock` | control | matter |  | available |
| `select.mudroom_door_lock_operating_mode` | control | matter | config | available |
| `sensor.mudroom_door_lock_battery` | telemetry | matter | diagnostic | available |
| `sensor.mudroom_door_lock_battery_type` | telemetry | matter | diagnostic | available |
| `sensor.mudroom_door_lock_battery_voltage` | telemetry | matter | diagnostic | available |

#### Washing Machine - Leak Detection

- Device ID: `device_e9cb048d7124`
- Integration: flo, unifi
- Model: Flo by Moen puck_v1
- Capability mix: 5 telemetry, 0 control, 1 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `binary_sensor.washing_machine_leak_detection_water_detected` | telemetry | flo |  | available |
| `device_tracker.washing_machine_leak_detection_espressif` | network | unifi | diagnostic | available |
| `sensor.espressif_link_speed_6` | telemetry | unifi | diagnostic | disabled |
| `sensor.washing_machine_leak_detection_battery` | telemetry | flo |  | available |
| `sensor.washing_machine_leak_detection_humidity` | telemetry | flo |  | available |
| `sensor.washing_machine_leak_detection_temperature` | telemetry | flo |  | available |

### Office

#### Office TV

- Device ID: `device_a76f54877bef`
- Integration: apple_tv
- Model: Apple Apple TV 4K
- Capability mix: 0 telemetry, 2 control, 0 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `media_player.office_tv` | control | apple_tv |  | available |
| `remote.office_tv` | control | apple_tv |  | available |

#### Office Thermostat

- Device ID: `device_d63cde62b102`
- Integration: homekit_controller
- Model: ecobee Inc. ecobee3
- Capability mix: 4 telemetry, 5 control, 0 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `binary_sensor.office_motion` | telemetry | homekit_controller |  | available |
| `binary_sensor.office_occupancy` | telemetry | homekit_controller |  | available |
| `button.office_clear_hold` | control | homekit_controller |  | unknown |
| `button.office_identify` | control | homekit_controller | diagnostic | unknown |
| `climate.office` | control | homekit_controller |  | available |
| `select.office_current_mode` | control | homekit_controller |  | unknown |
| `select.office_temperature_display_units` | control | homekit_controller | config | available |
| `sensor.office_current_humidity` | telemetry | homekit_controller |  | available |
| `sensor.office_current_temperature` | telemetry | homekit_controller |  | available |

### Stairs

#### Stairs Front Stairs

- Device ID: `device_eb14b692d03a`
- Integration: lutron_caseta
- Model: Lutron Electronics Co., Inc DVRF-6L (DivaSmartDimmer)
- Capability mix: 0 telemetry, 1 control, 0 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `light.stairs_front_stairs` | control | lutron_caseta |  | available |

### Unassigned

#### Apple TV (Family Room)

- Device ID: `device_58f8e7ee4387`
- Integration: unifi
- Model: Apple, Inc.
- Capability mix: 1 telemetry, 0 control, 1 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `device_tracker.apple_tv_family_room` | network | unifi | diagnostic | available |
| `sensor.apple_tv_family_room_link_speed` | telemetry | unifi | diagnostic | disabled |

#### Aqara Hub M100

- Device ID: `device_a735aed44232`
- Integration: matter
- Model: Aqara Aqara Hub M100
- Capability mix: 0 telemetry, 1 control, 0 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `button.aqara_hub_m100_identify` | control | matter | diagnostic | unknown |

#### Aqara Smart Lock U100

- Device ID: `device_4c2f574a97b1`
- Integration: matter
- Model: Aqara Aqara Smart Lock U100
- Capability mix: 4 telemetry, 3 control, 0 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `binary_sensor.aqara_smart_lock_u100_actuator` | telemetry | matter | diagnostic | disabled |
| `button.aqara_smart_lock_u100_identify` | control | matter | diagnostic | disabled |
| `lock.aqara_smart_lock_u100` | control | matter |  | disabled |
| `select.aqara_smart_lock_u100_operating_mode` | control | matter | config | disabled |
| `sensor.aqara_smart_lock_u100_battery` | telemetry | matter | diagnostic | disabled |
| `sensor.aqara_smart_lock_u100_battery_type` | telemetry | matter | diagnostic | disabled |
| `sensor.aqara_smart_lock_u100_battery_voltage` | telemetry | matter | diagnostic | disabled |

#### BRW849E567C91BC

- Device ID: `device_faba3c044d32`
- Integration: unifi
- Model: unknown model
- Capability mix: 1 telemetry, 0 control, 1 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `device_tracker.brw849e567c91bc` | network | unifi | diagnostic | available |
| `sensor.brw849e567c91bc_link_speed` | telemetry | unifi | diagnostic | disabled |

#### Back Patio Live view:21074

- Device ID: `device_92f12c63d777`
- Integration: unknown
- Model: Home Assistant Camera
- Capability mix: 0 telemetry, 0 control, 0 network, 0 other

_No registered entities._

#### Backup

- Device ID: `device_aa77864d8f2c`
- Integration: backup
- Model: Home Assistant Home Assistant Backup
- Capability mix: 5 telemetry, 0 control, 0 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `event.backup_automatic_backup` | telemetry | backup |  | available |
| `sensor.backup_backup_manager_state` | telemetry | backup |  | available |
| `sensor.backup_last_attempted_automatic_backup` | telemetry | backup |  | available |
| `sensor.backup_last_successful_automatic_backup` | telemetry | backup |  | available |
| `sensor.backup_next_scheduled_automatic_backup` | telemetry | backup |  | available |

#### Basement TV

- Device ID: `device_726950982dc7`
- Integration: cast
- Model: Sony BRAVIA 4K VH21
- Capability mix: 0 telemetry, 1 control, 0 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `media_player.basement_tv` | control | cast |  | unavailable |

#### Bonticou

- Device ID: `device_af91ab644a46`
- Integration: unifi
- Model: Ubiquiti Networks UniFi WLAN
- Capability mix: 2 telemetry, 2 control, 0 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `button.bonticou_regenerate_password` | control | unifi | config | disabled |
| `image.bonticou_qr_code` | telemetry | unifi | diagnostic | disabled |
| `sensor.bonticou` | telemetry | unifi | diagnostic | available |
| `switch.bonticou` | control | unifi | config | available |

#### Bonticou Guest

- Device ID: `device_92a17863a365`
- Integration: unifi
- Model: Ubiquiti Networks UniFi WLAN
- Capability mix: 2 telemetry, 2 control, 0 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `button.bonticou_guest_regenerate_password` | control | unifi | config | disabled |
| `image.bonticou_guest_qr_code` | telemetry | unifi | diagnostic | disabled |
| `sensor.bonticou_guest` | telemetry | unifi | diagnostic | available |
| `switch.bonticou_guest` | control | unifi | config | available |

#### Claude AI Task

- Device ID: `device_e12e907a53c0`
- Integration: anthropic
- Model: Anthropic claude-haiku-4-5
- Capability mix: 0 telemetry, 0 control, 0 network, 1 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `ai_task.claude_ai_task` | other | anthropic |  | unknown |

#### Claude conversation

- Device ID: `device_f53f8bf84a9b`
- Integration: anthropic
- Model: Anthropic claude-haiku-4-5
- Capability mix: 0 telemetry, 0 control, 0 network, 1 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `conversation.claude_conversation` | other | anthropic |  | unknown |

#### DB15

- Device ID: `device_3d305b654446`
- Integration: unifi
- Model: Apple, Inc.
- Capability mix: 1 telemetry, 0 control, 1 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `device_tracker.db15` | network | unifi | diagnostic | unavailable |
| `sensor.db15_link_speed` | telemetry | unifi | diagnostic | disabled |

#### EP25

- Device ID: `device_e4732ba34afc`
- Integration: unifi
- Model: unknown model
- Capability mix: 1 telemetry, 0 control, 1 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `device_tracker.ep25` | network | unifi | diagnostic | available |
| `sensor.ep25_link_speed` | telemetry | unifi | diagnostic | disabled |

#### Family Room Frame TV:21065

- Device ID: `device_d5dab79b1a64`
- Integration: unknown
- Model: Home Assistant TelevisionMediaPlayer
- Capability mix: 0 telemetry, 0 control, 0 network, 0 other

_No registered entities._

#### Family Room TV

- Device ID: `device_3f083f58ae7d`
- Integration: cast
- Model: Unknown manufacturer LS03F
- Capability mix: 0 telemetry, 1 control, 0 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `media_player.ls03f3973` | control | cast |  | available |

#### Family Room TV

- Device ID: `device_585364ba9de2`
- Integration: cast
- Model: VIZIO PQ65-F1
- Capability mix: 0 telemetry, 1 control, 0 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `media_player.family_room_tv` | control | cast |  | unavailable |

#### File editor

- Device ID: `device_3245b94dd2f1`
- Integration: hassio
- Model: Official apps Home Assistant App
- Capability mix: 6 telemetry, 1 control, 0 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `binary_sensor.file_editor_running` | telemetry | hassio |  | disabled |
| `sensor.file_editor_cpu_percent` | telemetry | hassio |  | disabled |
| `sensor.file_editor_memory_percent` | telemetry | hassio |  | disabled |
| `sensor.file_editor_newest_version` | telemetry | hassio |  | disabled |
| `sensor.file_editor_version` | telemetry | hassio |  | disabled |
| `switch.file_editor` | control | hassio |  | disabled |
| `update.file_editor_update` | telemetry | hassio | config | available |

#### Fios-VHTx3

- Device ID: `device_0a258d606684`
- Integration: unifi
- Model: Ubiquiti Networks UniFi WLAN
- Capability mix: 2 telemetry, 2 control, 0 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `button.fios_vhtx3_regenerate_password` | control | unifi | config | disabled |
| `image.fios_vhtx3_qr_code` | telemetry | unifi | diagnostic | disabled |
| `sensor.fios_vhtx3` | telemetry | unifi | diagnostic | available |
| `switch.fios_vhtx3` | control | unifi | config | available |

#### Forecast

- Device ID: `device_9d764b6dff21`
- Integration: met
- Model: Met.no Forecast
- Capability mix: 1 telemetry, 0 control, 0 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `weather.forecast_home` | telemetry | met |  | available |

#### Front Door Live view:21072

- Device ID: `device_98fae9211a41`
- Integration: unknown
- Model: Home Assistant Camera
- Capability mix: 0 telemetry, 0 control, 0 network, 0 other

_No registered entities._

#### Front Yard

- Device ID: `device_1557543cefbd`
- Integration: unifi, unifiprotect
- Model: Ubiquiti G6 Instant
- Capability mix: 28 telemetry, 33 control, 1 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `binary_sensor.back_yard_animal_detected` | telemetry | unifiprotect |  | available |
| `binary_sensor.back_yard_audio_object_detected` | telemetry | unifiprotect |  | disabled |
| `binary_sensor.back_yard_baby_cry_detected` | telemetry | unifiprotect |  | available |
| `binary_sensor.back_yard_barking_detected` | telemetry | unifiprotect |  | available |
| `binary_sensor.back_yard_car_alarm_detected` | telemetry | unifiprotect |  | available |
| `binary_sensor.back_yard_car_horn_detected` | telemetry | unifiprotect |  | available |
| `binary_sensor.back_yard_co_alarm_detected` | telemetry | unifiprotect |  | available |
| `binary_sensor.back_yard_glass_break_detected` | telemetry | unifiprotect |  | available |
| `binary_sensor.back_yard_object_detected` | telemetry | unifiprotect |  | disabled |
| `binary_sensor.back_yard_person_detected` | telemetry | unifiprotect |  | available |
| `binary_sensor.back_yard_siren_detected` | telemetry | unifiprotect |  | available |
| `binary_sensor.back_yard_smoke_alarm_detected` | telemetry | unifiprotect |  | available |
| `binary_sensor.back_yard_speaking_detected` | telemetry | unifiprotect |  | available |
| `binary_sensor.back_yard_vehicle_detected` | telemetry | unifiprotect |  | available |
| `binary_sensor.g6_instant_is_dark_2` | telemetry | unifiprotect |  | available |
| `binary_sensor.g6_instant_motion_2` | telemetry | unifiprotect |  | available |
| `button.g6_instant_restart_2` | control | unifiprotect |  | disabled |
| `button.g6_instant_unadopt_device_2` | control | unifiprotect |  | disabled |
| `camera.front_yard_high_resolution_channel_insecure` | telemetry | unifiprotect |  | disabled |
| `camera.g6_instant_high_resolution_channel_2` | telemetry | unifiprotect |  | available |
| `device_tracker.uvc_g6_instant_2` | network | unifi | diagnostic | available |
| `event.back_yard_vehicle` | telemetry | unifiprotect |  | available |
| `media_player.back_yard_speaker` | control | unifiprotect |  | available |
| `number.back_yard_infrared_custom_lux_trigger` | control | unifiprotect | config | unavailable |
| `number.back_yard_microphone_level` | control | unifiprotect | config | available |
| `number.back_yard_system_sounds_volume` | control | unifiprotect | config | available |
| `number.g6_instant_wide_dynamic_range_2` | control | unifiprotect | config | unavailable |
| `select.back_yard_hdr_mode` | control | unifiprotect | config | available |
| `select.back_yard_infrared_mode` | control | unifiprotect | config | available |
| `select.g6_instant_recording_mode_2` | control | unifiprotect | config | available |
| `sensor.front_yard_wi_fi_signal_strength` | telemetry | unifiprotect | diagnostic | disabled |
| `sensor.g6_instant_disk_write_rate_2` | telemetry | unifiprotect | diagnostic | available |
| `sensor.g6_instant_last_motion_detected_2` | telemetry | unifiprotect |  | disabled |
| `sensor.g6_instant_link_speed` | telemetry | unifi | diagnostic | disabled |
| `sensor.g6_instant_oldest_recording_2` | telemetry | unifiprotect | diagnostic | disabled |
| `sensor.g6_instant_received_data_2` | telemetry | unifiprotect | diagnostic | disabled |
| `sensor.g6_instant_storage_used_2` | telemetry | unifiprotect | diagnostic | available |
| `sensor.g6_instant_transferred_data_2` | telemetry | unifiprotect | diagnostic | disabled |
| `sensor.g6_instant_uptime_2` | telemetry | unifiprotect | diagnostic | disabled |
| `switch.back_yard_animal_detection` | control | unifiprotect | config | available |
| `switch.back_yard_baby_cry_detection` | control | unifiprotect | config | available |
| `switch.back_yard_car_alarm_detection` | control | unifiprotect | config | available |
| `switch.back_yard_car_horn_detection` | control | unifiprotect | config | available |
| `switch.back_yard_co_alarm_detection` | control | unifiprotect | config | available |
| `switch.back_yard_glass_break_detection` | control | unifiprotect | config | available |
| `switch.back_yard_hdr_mode` | control | unifiprotect | config | disabled |
| `switch.back_yard_license_plate_detection` | control | unifiprotect | config | available |
| `switch.back_yard_none` | control | unifiprotect | config | available |
| `switch.back_yard_person_detection` | control | unifiprotect | config | available |
| `switch.back_yard_privacy_mode` | control | unifiprotect | config | available |
| `switch.back_yard_siren_detection` | control | unifiprotect | config | available |
| `switch.back_yard_smoke_detection` | control | unifiprotect | config | available |
| `switch.back_yard_speaking_detection` | control | unifiprotect | config | available |
| `switch.back_yard_status_light` | control | unifiprotect | config | available |
| `switch.back_yard_system_sounds` | control | unifiprotect | config | available |
| `switch.back_yard_vehicle_detection` | control | unifiprotect | config | available |
| `switch.g6_instant_motion_2` | control | unifiprotect | config | available |
| `switch.g6_instant_overlay_show_date_2` | control | unifiprotect | config | available |
| `switch.g6_instant_overlay_show_logo_2` | control | unifiprotect | config | available |
| `switch.g6_instant_overlay_show_name_2` | control | unifiprotect | config | available |
| `switch.g6_instant_overlay_show_nerd_mode_2` | control | unifiprotect | config | available |
| `switch.g6_instant_ssh_enabled_2` | control | unifiprotect | config | disabled |

#### Front Yard High resolution channel:21068

- Device ID: `device_29e8aef95355`
- Integration: unknown
- Model: Home Assistant Camera
- Capability mix: 0 telemetry, 0 control, 0 network, 0 other

_No registered entities._

#### Galaxy-S24-Ultra

- Device ID: `device_66bf3c0457ee`
- Integration: unifi
- Model: unknown model
- Capability mix: 1 telemetry, 0 control, 1 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `device_tracker.galaxy_s24_ultra` | network | unifi | diagnostic | unavailable |
| `sensor.galaxy_s24_ultra_link_speed` | telemetry | unifi | diagnostic | disabled |

#### Garage

- Device ID: `device_c305c1f8549c`
- Integration: unifi, unifiprotect
- Model: Ubiquiti G6 Instant
- Capability mix: 26 telemetry, 33 control, 1 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `binary_sensor.g6_instant_is_dark_3` | telemetry | unifiprotect |  | available |
| `binary_sensor.g6_instant_motion_3` | telemetry | unifiprotect |  | unavailable |
| `binary_sensor.garage_animal_detected` | telemetry | unifiprotect |  | available |
| `binary_sensor.garage_audio_object_detected` | telemetry | unifiprotect |  | disabled |
| `binary_sensor.garage_baby_cry_detected` | telemetry | unifiprotect |  | available |
| `binary_sensor.garage_barking_detected` | telemetry | unifiprotect |  | available |
| `binary_sensor.garage_car_alarm_detected` | telemetry | unifiprotect |  | available |
| `binary_sensor.garage_car_horn_detected` | telemetry | unifiprotect |  | available |
| `binary_sensor.garage_co_alarm_detected` | telemetry | unifiprotect |  | available |
| `binary_sensor.garage_glass_break_detected` | telemetry | unifiprotect |  | available |
| `binary_sensor.garage_object_detected` | telemetry | unifiprotect |  | disabled |
| `binary_sensor.garage_person_detected` | telemetry | unifiprotect |  | available |
| `binary_sensor.garage_siren_detected` | telemetry | unifiprotect |  | available |
| `binary_sensor.garage_smoke_alarm_detected` | telemetry | unifiprotect |  | available |
| `binary_sensor.garage_speaking_detected` | telemetry | unifiprotect |  | available |
| `binary_sensor.garage_vehicle_detected` | telemetry | unifiprotect |  | available |
| `button.g6_instant_restart_3` | control | unifiprotect |  | disabled |
| `button.g6_instant_unadopt_device_3` | control | unifiprotect |  | disabled |
| `camera.g6_instant_high_resolution_channel_3` | telemetry | unifiprotect |  | available |
| `device_tracker.uvc_g6_instant_3` | network | unifi | diagnostic | available |
| `event.garage_vehicle` | telemetry | unifiprotect |  | available |
| `media_player.garage_speaker` | control | unifiprotect |  | available |
| `number.g6_instant_wide_dynamic_range_3` | control | unifiprotect | config | unavailable |
| `number.garage_infrared_custom_lux_trigger` | control | unifiprotect | config | unavailable |
| `number.garage_microphone_level` | control | unifiprotect | config | available |
| `number.garage_system_sounds_volume` | control | unifiprotect | config | available |
| `select.g6_instant_recording_mode_3` | control | unifiprotect | config | available |
| `select.garage_hdr_mode` | control | unifiprotect | config | available |
| `select.garage_infrared_mode` | control | unifiprotect | config | available |
| `sensor.g6_instant_disk_write_rate_3` | telemetry | unifiprotect | diagnostic | available |
| `sensor.g6_instant_last_motion_detected_3` | telemetry | unifiprotect |  | disabled |
| `sensor.g6_instant_oldest_recording_3` | telemetry | unifiprotect | diagnostic | disabled |
| `sensor.g6_instant_received_data_3` | telemetry | unifiprotect | diagnostic | disabled |
| `sensor.g6_instant_storage_used_3` | telemetry | unifiprotect | diagnostic | available |
| `sensor.g6_instant_transferred_data_3` | telemetry | unifiprotect | diagnostic | disabled |
| `sensor.g6_instant_uptime_3` | telemetry | unifiprotect | diagnostic | disabled |
| `sensor.garage_wi_fi_signal_strength` | telemetry | unifiprotect | diagnostic | disabled |
| `switch.g6_instant_motion_3` | control | unifiprotect | config | available |
| `switch.g6_instant_overlay_show_date_3` | control | unifiprotect | config | available |
| `switch.g6_instant_overlay_show_logo_3` | control | unifiprotect | config | available |
| `switch.g6_instant_overlay_show_name_3` | control | unifiprotect | config | available |
| `switch.g6_instant_overlay_show_nerd_mode_3` | control | unifiprotect | config | available |
| `switch.g6_instant_ssh_enabled_3` | control | unifiprotect | config | disabled |
| `switch.garage` | control | unifiprotect | config | available |
| `switch.garage_animal_detection` | control | unifiprotect | config | available |
| `switch.garage_baby_cry_detection` | control | unifiprotect | config | available |
| `switch.garage_car_alarm_detection` | control | unifiprotect | config | available |
| `switch.garage_car_horn_detection` | control | unifiprotect | config | available |
| `switch.garage_co_alarm_detection` | control | unifiprotect | config | available |
| `switch.garage_glass_break_detection` | control | unifiprotect | config | available |
| `switch.garage_hdr_mode` | control | unifiprotect | config | disabled |
| `switch.garage_license_plate_detection` | control | unifiprotect | config | available |
| `switch.garage_person_detection` | control | unifiprotect | config | available |
| `switch.garage_privacy_mode` | control | unifiprotect | config | available |
| `switch.garage_siren_detection` | control | unifiprotect | config | available |
| `switch.garage_smoke_detection` | control | unifiprotect | config | available |
| `switch.garage_speaking_detection` | control | unifiprotect | config | available |
| `switch.garage_status_light` | control | unifiprotect | config | available |
| `switch.garage_system_sounds` | control | unifiprotect | config | available |
| `switch.garage_vehicle_detection` | control | unifiprotect | config | available |

#### Google Translate en com

- Device ID: `device_3995fb7fb128`
- Integration: google_translate
- Model: Google Google Translate TTS
- Capability mix: 0 telemetry, 0 control, 0 network, 1 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `tts.google_translate_en_com` | other | google_translate |  | unknown |

#### HACS

- Device ID: `device_c96e7314041e`
- Integration: hacs
- Model: hacs.xyz
- Capability mix: 1 telemetry, 1 control, 0 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `switch.hacs_pre_release` | control | hacs | diagnostic | disabled |
| `update.hacs_update` | telemetry | hacs | config | available |

#### HASS Bridge:21064

- Device ID: `device_c5fec5011800`
- Integration: unknown
- Model: Home Assistant HomeBridge
- Capability mix: 0 telemetry, 0 control, 0 network, 0 other

_No registered entities._

#### Home Assistant

- Device ID: `device_32c099f4c862`
- Integration: unifi
- Model: Nabu Casa, Inc.
- Capability mix: 1 telemetry, 0 control, 1 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `device_tracker.home_assistant` | network | unifi | diagnostic | available |
| `sensor.home_assistant_link_speed` | telemetry | unifi | diagnostic | disabled |

#### Home Assistant Core

- Device ID: `device_27a1401e8e43`
- Integration: hassio
- Model: Home Assistant Home Assistant Core
- Capability mix: 3 telemetry, 0 control, 0 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `sensor.home_assistant_core_cpu_percent` | telemetry | hassio |  | disabled |
| `sensor.home_assistant_core_memory_percent` | telemetry | hassio |  | disabled |
| `update.home_assistant_core_update` | telemetry | hassio | config | available |

#### Home Assistant Host

- Device ID: `device_d557496dfd6d`
- Integration: hassio
- Model: Home Assistant Home Assistant Host
- Capability mix: 5 telemetry, 0 control, 0 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `sensor.home_assistant_host_apparmor_version` | telemetry | hassio | diagnostic | disabled |
| `sensor.home_assistant_host_disk_free` | telemetry | hassio | diagnostic | disabled |
| `sensor.home_assistant_host_disk_total` | telemetry | hassio | diagnostic | disabled |
| `sensor.home_assistant_host_disk_used` | telemetry | hassio | diagnostic | disabled |
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
| `update.home_assistant_operating_system_update` | telemetry | hassio | config | available |

#### Home Assistant Supervisor

- Device ID: `device_ee501121995a`
- Integration: hassio
- Model: Home Assistant Home Assistant Supervisor
- Capability mix: 3 telemetry, 0 control, 0 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `sensor.home_assistant_supervisor_cpu_percent` | telemetry | hassio |  | disabled |
| `sensor.home_assistant_supervisor_memory_percent` | telemetry | hassio |  | disabled |
| `update.home_assistant_supervisor_update` | telemetry | hassio | config | available |

#### Live view:21075

- Device ID: `device_c8464794ceae`
- Integration: unknown
- Model: Home Assistant Camera
- Capability mix: 0 telemetry, 0 control, 0 network, 0 other

_No registered entities._

#### Lutron-06926f09

- Device ID: `device_d047070a23cf`
- Integration: unifi
- Model: Lutron Electronics Co., Inc.
- Capability mix: 1 telemetry, 0 control, 1 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `device_tracker.lutron_06926f09` | network | unifi | diagnostic | available |
| `sensor.lutron_06926f09_link_speed` | telemetry | unifi | diagnostic | disabled |

#### Master.localdomain

- Device ID: `device_c704d3c4101c`
- Integration: unifi
- Model: ecobee inc
- Capability mix: 1 telemetry, 0 control, 1 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `device_tracker.master_localdomain` | network | unifi | diagnostic | available |
| `sensor.master_localdomain_link_speed` | telemetry | unifi | diagnostic | disabled |

#### Matter Server

- Device ID: `device_c137b2ed9eba`
- Integration: hassio
- Model: Official apps Home Assistant App
- Capability mix: 6 telemetry, 1 control, 0 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `binary_sensor.matter_server_running` | telemetry | hassio |  | disabled |
| `sensor.matter_server_cpu_percent` | telemetry | hassio |  | disabled |
| `sensor.matter_server_memory_percent` | telemetry | hassio |  | disabled |
| `sensor.matter_server_newest_version` | telemetry | hassio |  | disabled |
| `sensor.matter_server_version` | telemetry | hassio |  | disabled |
| `switch.matter_server` | control | hassio |  | disabled |
| `update.matter_server_update` | telemetry | hassio | config | available |

#### Mechanical room High resolution channel:21070

- Device ID: `device_c51d4f559dcb`
- Integration: unknown
- Model: Home Assistant Camera
- Capability mix: 0 telemetry, 0 control, 0 network, 0 other

_No registered entities._

#### Mini Media Player

- Device ID: `device_ee47223930dd`
- Integration: hacs
- Model: kalkih plugin
- Capability mix: 1 telemetry, 1 control, 0 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `switch.mini_media_player_pre_release` | control | hacs | diagnostic | disabled |
| `update.mini_media_player_update` | telemetry | hacs | config | available |

#### Mud room High resolution channel:21067

- Device ID: `device_28cd11f48302`
- Integration: unknown
- Model: Home Assistant Camera
- Capability mix: 0 telemetry, 0 control, 0 network, 0 other

_No registered entities._

#### Mudroom Door Live view:21073

- Device ID: `device_3f4d33d7d5c4`
- Integration: unknown
- Model: Home Assistant Camera
- Capability mix: 0 telemetry, 0 control, 0 network, 0 other

_No registered entities._

#### Mushroom

- Device ID: `device_95e8ee1b21c9`
- Integration: hacs
- Model: piitaya plugin
- Capability mix: 1 telemetry, 1 control, 0 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `switch.mushroom_pre_release` | control | hacs | diagnostic | disabled |
| `update.mushroom_update` | telemetry | hacs | config | available |

#### OpenAI AI Task

- Device ID: `device_3caa73693f9b`
- Integration: openai_conversation
- Model: OpenAI gpt-4o-mini
- Capability mix: 0 telemetry, 0 control, 0 network, 1 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `ai_task.openai_ai_task` | other | openai_conversation |  | unknown |

#### OpenAI Conversation

- Device ID: `device_898f8883f5f9`
- Integration: openai_conversation
- Model: OpenAI gpt-4o-mini
- Capability mix: 0 telemetry, 0 control, 0 network, 1 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `conversation.openai_conversation` | other | openai_conversation |  | available |

#### OpenAI STT

- Device ID: `device_6ef663ffa846`
- Integration: openai_conversation
- Model: OpenAI gpt-4o-mini-transcribe
- Capability mix: 0 telemetry, 0 control, 0 network, 1 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `stt.openai_stt` | other | openai_conversation |  | unknown |

#### OpenAI TTS

- Device ID: `device_5ea1c7d00bd0`
- Integration: openai_conversation
- Model: OpenAI gpt-4o-mini-tts
- Capability mix: 0 telemetry, 0 control, 0 network, 1 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `tts.openai_tts` | other | openai_conversation |  | unknown |

#### Play Room

- Device ID: `device_5a7bbc9548a4`
- Integration: unifi, unifiprotect
- Model: Ubiquiti G6 Instant
- Capability mix: 27 telemetry, 33 control, 1 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `binary_sensor.g6_instant_is_dark` | telemetry | unifiprotect |  | available |
| `binary_sensor.g6_instant_motion` | telemetry | unifiprotect |  | available |
| `binary_sensor.play_room_animal_detected` | telemetry | unifiprotect |  | available |
| `binary_sensor.play_room_audio_object_detected` | telemetry | unifiprotect |  | disabled |
| `binary_sensor.play_room_baby_cry_detected` | telemetry | unifiprotect |  | available |
| `binary_sensor.play_room_barking_detected` | telemetry | unifiprotect |  | available |
| `binary_sensor.play_room_car_alarm_detected` | telemetry | unifiprotect |  | available |
| `binary_sensor.play_room_car_horn_detected` | telemetry | unifiprotect |  | available |
| `binary_sensor.play_room_co_alarm_detected` | telemetry | unifiprotect |  | available |
| `binary_sensor.play_room_glass_break_detected` | telemetry | unifiprotect |  | available |
| `binary_sensor.play_room_object_detected` | telemetry | unifiprotect |  | disabled |
| `binary_sensor.play_room_person_detected` | telemetry | unifiprotect |  | available |
| `binary_sensor.play_room_siren_detected` | telemetry | unifiprotect |  | available |
| `binary_sensor.play_room_smoke_alarm_detected` | telemetry | unifiprotect |  | available |
| `binary_sensor.play_room_speaking_detected` | telemetry | unifiprotect |  | available |
| `binary_sensor.play_room_vehicle_detected` | telemetry | unifiprotect |  | available |
| `button.g6_instant_restart` | control | unifiprotect |  | disabled |
| `button.g6_instant_unadopt_device` | control | unifiprotect |  | disabled |
| `camera.g6_instant_high_resolution_channel` | telemetry | unifiprotect |  | available |
| `camera.play_room_high_resolution_channel_insecure` | telemetry | unifiprotect |  | disabled |
| `device_tracker.uvc_g6_instant` | network | unifi | diagnostic | available |
| `event.play_room_vehicle` | telemetry | unifiprotect |  | available |
| `media_player.play_room_speaker` | control | unifiprotect |  | available |
| `number.g6_instant_wide_dynamic_range` | control | unifiprotect | config | unavailable |
| `number.play_room_infrared_custom_lux_trigger` | control | unifiprotect | config | unavailable |
| `number.play_room_microphone_level` | control | unifiprotect | config | available |
| `number.play_room_system_sounds_volume` | control | unifiprotect | config | available |
| `select.g6_instant_recording_mode` | control | unifiprotect | config | available |
| `select.play_room_hdr_mode` | control | unifiprotect | config | available |
| `select.play_room_infrared_mode` | control | unifiprotect | config | available |
| `sensor.g6_instant_disk_write_rate` | telemetry | unifiprotect | diagnostic | available |
| `sensor.g6_instant_last_motion_detected` | telemetry | unifiprotect |  | disabled |
| `sensor.g6_instant_oldest_recording` | telemetry | unifiprotect | diagnostic | disabled |
| `sensor.g6_instant_received_data` | telemetry | unifiprotect | diagnostic | disabled |
| `sensor.g6_instant_storage_used` | telemetry | unifiprotect | diagnostic | available |
| `sensor.g6_instant_transferred_data` | telemetry | unifiprotect | diagnostic | disabled |
| `sensor.g6_instant_uptime` | telemetry | unifiprotect | diagnostic | disabled |
| `sensor.play_room_wi_fi_signal_strength` | telemetry | unifiprotect | diagnostic | disabled |
| `switch.g6_instant_motion` | control | unifiprotect | config | available |
| `switch.g6_instant_overlay_show_date` | control | unifiprotect | config | available |
| `switch.g6_instant_overlay_show_logo` | control | unifiprotect | config | available |
| `switch.g6_instant_overlay_show_name` | control | unifiprotect | config | available |
| `switch.g6_instant_overlay_show_nerd_mode` | control | unifiprotect | config | available |
| `switch.g6_instant_ssh_enabled` | control | unifiprotect | config | disabled |
| `switch.play_room_animal_detection` | control | unifiprotect | config | available |
| `switch.play_room_baby_cry_detection` | control | unifiprotect | config | available |
| `switch.play_room_car_alarm_detection` | control | unifiprotect | config | available |
| `switch.play_room_car_horn_detection` | control | unifiprotect | config | available |
| `switch.play_room_co_alarm_detection` | control | unifiprotect | config | available |
| `switch.play_room_glass_break_detection` | control | unifiprotect | config | available |
| `switch.play_room_hdr_mode` | control | unifiprotect | config | disabled |
| `switch.play_room_license_plate_detection` | control | unifiprotect | config | available |
| `switch.play_room_none` | control | unifiprotect | config | available |
| `switch.play_room_person_detection` | control | unifiprotect | config | available |
| `switch.play_room_privacy_mode` | control | unifiprotect | config | available |
| `switch.play_room_siren_detection` | control | unifiprotect | config | available |
| `switch.play_room_smoke_detection` | control | unifiprotect | config | available |
| `switch.play_room_speaking_detection` | control | unifiprotect | config | available |
| `switch.play_room_status_light` | control | unifiprotect | config | available |
| `switch.play_room_system_sounds` | control | unifiprotect | config | available |
| `switch.play_room_vehicle_detection` | control | unifiprotect | config | available |

#### Play Room High resolution channel:21069

- Device ID: `device_ce831e5fd1e6`
- Integration: unknown
- Model: Home Assistant Camera
- Capability mix: 0 telemetry, 0 control, 0 network, 0 other

_No registered entities._

#### Samsung

- Device ID: `device_a12ed0ca1c26`
- Integration: unifi
- Model: unknown model
- Capability mix: 1 telemetry, 0 control, 1 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `device_tracker.samsung` | network | unifi | diagnostic | available |
| `sensor.samsung_link_speed` | telemetry | unifi | diagnostic | disabled |

#### Sonos Card

- Device ID: `device_02ce76119161`
- Integration: hacs
- Model: punxaphil plugin
- Capability mix: 1 telemetry, 1 control, 0 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `switch.sonos_card_pre_release` | control | hacs | diagnostic | disabled |
| `update.sonos_card_update` | telemetry | hacs | config | available |

#### Spotify

- Device ID: `device_b09ca0ad1db1`
- Integration: spotify
- Model: Spotify AB Spotify premium
- Capability mix: 0 telemetry, 1 control, 0 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `media_player.spotify` | control | spotify |  | available |

#### Sun

- Device ID: `device_a33df9341ba8`
- Integration: sun
- Model: unknown model
- Capability mix: 10 telemetry, 0 control, 0 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `binary_sensor.sun_solar_rising` | telemetry | sun | diagnostic | disabled |
| `sensor.sun_next_dawn` | telemetry | sun | diagnostic | available |
| `sensor.sun_next_dusk` | telemetry | sun | diagnostic | available |
| `sensor.sun_next_midnight` | telemetry | sun | diagnostic | available |
| `sensor.sun_next_noon` | telemetry | sun | diagnostic | available |
| `sensor.sun_next_rising` | telemetry | sun | diagnostic | available |
| `sensor.sun_next_setting` | telemetry | sun | diagnostic | available |
| `sensor.sun_solar_azimuth` | telemetry | sun | diagnostic | disabled |
| `sensor.sun_solar_elevation` | telemetry | sun | diagnostic | disabled |
| `sensor.sun_solar_rising` | telemetry | sun | diagnostic | disabled |

#### TK iPhone 16 Pro

- Device ID: `device_784e00b00a1e`
- Integration: mobile_app
- Model: Apple iPhone17,1
- Capability mix: 14 telemetry, 0 control, 0 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `device_tracker.tk_iphone_16_pro` | telemetry | mobile_app | diagnostic | available |
| `sensor.tk_iphone_16_pro_app_version` | telemetry | mobile_app | diagnostic | available |
| `sensor.tk_iphone_16_pro_audio_output` | telemetry | mobile_app |  | available |
| `sensor.tk_iphone_16_pro_battery_level` | telemetry | mobile_app |  | available |
| `sensor.tk_iphone_16_pro_battery_state` | telemetry | mobile_app |  | available |
| `sensor.tk_iphone_16_pro_bssid` | telemetry | mobile_app |  | available |
| `sensor.tk_iphone_16_pro_connection_type` | telemetry | mobile_app |  | available |
| `sensor.tk_iphone_16_pro_geocoded_location` | telemetry | mobile_app |  | available |
| `sensor.tk_iphone_16_pro_last_update_trigger` | telemetry | mobile_app |  | available |
| `sensor.tk_iphone_16_pro_location_permission` | telemetry | mobile_app |  | available |
| `sensor.tk_iphone_16_pro_sim_1` | telemetry | mobile_app |  | available |
| `sensor.tk_iphone_16_pro_sim_2` | telemetry | mobile_app |  | available |
| `sensor.tk_iphone_16_pro_ssid` | telemetry | mobile_app |  | available |
| `sensor.tk_iphone_16_pro_storage` | telemetry | mobile_app |  | available |

#### Terminal & SSH

- Device ID: `device_86ea87697a8c`
- Integration: hassio
- Model: Official apps Home Assistant App
- Capability mix: 6 telemetry, 1 control, 0 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `binary_sensor.terminal_ssh_running` | telemetry | hassio |  | disabled |
| `sensor.terminal_ssh_cpu_percent` | telemetry | hassio |  | disabled |
| `sensor.terminal_ssh_memory_percent` | telemetry | hassio |  | disabled |
| `sensor.terminal_ssh_newest_version` | telemetry | hassio |  | disabled |
| `sensor.terminal_ssh_version` | telemetry | hassio |  | disabled |
| `switch.terminal_ssh` | control | hassio |  | disabled |
| `update.terminal_ssh_update` | telemetry | hassio | config | available |

#### Tesla

- Device ID: `device_ef443339991c`
- Integration: unifi
- Model: Tesla,Inc.
- Capability mix: 1 telemetry, 0 control, 1 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `device_tracker.tesla` | network | unifi | diagnostic | unavailable |
| `sensor.tesla_link_speed` | telemetry | unifi | diagnostic | disabled |

#### Texas Instruments CC2652

- Device ID: `device_c6f095238e88`
- Integration: unknown
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
| `button.u7_pro_family_room_restart` | control | unifi | config | unknown |
| `device_tracker.u7_pro_family_room` | network | unifi | diagnostic | available |
| `light.u7_pro_family_room_led` | control | unifi | config | available |
| `sensor.u7_pro_family_room_clients` | telemetry | unifi | diagnostic | disabled |
| `sensor.u7_pro_family_room_cpu_utilization` | telemetry | unifi | diagnostic | available |
| `sensor.u7_pro_family_room_memory_utilization` | telemetry | unifi | diagnostic | available |
| `sensor.u7_pro_family_room_state` | telemetry | unifi | diagnostic | available |
| `sensor.u7_pro_family_room_uplink_mac` | telemetry | unifi | diagnostic | available |
| `sensor.u7_pro_family_room_uptime` | telemetry | unifi | diagnostic | available |
| `update.u7_pro_family_room` | telemetry | unifi | config | available |

#### U7 Pro (Mesh)

- Device ID: `device_435c14fb97bb`
- Integration: unifi
- Model: Ubiquiti Networks U7PRO
- Capability mix: 7 telemetry, 2 control, 1 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `button.u7_pro_mesh_restart` | control | unifi | config | unknown |
| `device_tracker.u7_pro_mesh` | network | unifi | diagnostic | available |
| `light.u7_pro_mesh_led` | control | unifi | config | available |
| `sensor.u7_pro_mesh_clients` | telemetry | unifi | diagnostic | disabled |
| `sensor.u7_pro_mesh_cpu_utilization` | telemetry | unifi | diagnostic | available |
| `sensor.u7_pro_mesh_memory_utilization` | telemetry | unifi | diagnostic | available |
| `sensor.u7_pro_mesh_state` | telemetry | unifi | diagnostic | available |
| `sensor.u7_pro_mesh_uplink_mac` | telemetry | unifi | diagnostic | available |
| `sensor.u7_pro_mesh_uptime` | telemetry | unifi | diagnostic | available |
| `update.u7_pro_mesh` | telemetry | unifi | config | available |

#### U7 Pro (Mud Room)

- Device ID: `device_776f62e721cd`
- Integration: unifi
- Model: Ubiquiti Networks U7PRO
- Capability mix: 7 telemetry, 2 control, 1 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `button.u7_pro_mud_room_restart` | control | unifi | config | unknown |
| `device_tracker.u7_pro_mud_room` | network | unifi | diagnostic | available |
| `light.u7_pro_mud_room_led` | control | unifi | config | available |
| `sensor.u7_pro_mud_room_clients` | telemetry | unifi | diagnostic | disabled |
| `sensor.u7_pro_mud_room_cpu_utilization` | telemetry | unifi | diagnostic | available |
| `sensor.u7_pro_mud_room_memory_utilization` | telemetry | unifi | diagnostic | available |
| `sensor.u7_pro_mud_room_state` | telemetry | unifi | diagnostic | available |
| `sensor.u7_pro_mud_room_uplink_mac` | telemetry | unifi | diagnostic | available |
| `sensor.u7_pro_mud_room_uptime` | telemetry | unifi | diagnostic | available |
| `update.u7_pro_mud_room` | telemetry | unifi | config | available |

#### U7 Pro Outdoor

- Device ID: `device_eb5e03453518`
- Integration: unifi
- Model: Ubiquiti Networks UAPA6A6
- Capability mix: 7 telemetry, 1 control, 1 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `button.u7_pro_outdoor_restart` | control | unifi | config | unknown |
| `device_tracker.u7_pro_outdoor` | network | unifi | diagnostic | available |
| `sensor.u7_pro_outdoor_clients` | telemetry | unifi | diagnostic | disabled |
| `sensor.u7_pro_outdoor_cpu_utilization` | telemetry | unifi | diagnostic | available |
| `sensor.u7_pro_outdoor_memory_utilization` | telemetry | unifi | diagnostic | available |
| `sensor.u7_pro_outdoor_state` | telemetry | unifi | diagnostic | available |
| `sensor.u7_pro_outdoor_uplink_mac` | telemetry | unifi | diagnostic | available |
| `sensor.u7_pro_outdoor_uptime` | telemetry | unifi | diagnostic | available |
| `update.u7_pro_outdoor` | telemetry | unifi | config | available |

#### USW Flex 2.5G 5

- Device ID: `device_cb39eb41896c`
- Integration: unifi
- Model: Ubiquiti Networks USWED35
- Capability mix: 12 telemetry, 6 control, 1 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `button.usw_flex_2_5g_5_restart` | control | unifi | config | unknown |
| `device_tracker.usw_flex_2_5g_5` | network | unifi | diagnostic | available |
| `sensor.usw_flex_2_5g_5_clients` | telemetry | unifi | diagnostic | disabled |
| `sensor.usw_flex_2_5g_5_cpu_utilization` | telemetry | unifi | diagnostic | available |
| `sensor.usw_flex_2_5g_5_memory_utilization` | telemetry | unifi | diagnostic | available |
| `sensor.usw_flex_2_5g_5_port_1_link_speed` | telemetry | unifi | diagnostic | disabled |
| `sensor.usw_flex_2_5g_5_port_2_link_speed` | telemetry | unifi | diagnostic | disabled |
| `sensor.usw_flex_2_5g_5_port_3_link_speed` | telemetry | unifi | diagnostic | disabled |
| `sensor.usw_flex_2_5g_5_port_4_link_speed` | telemetry | unifi | diagnostic | disabled |
| `sensor.usw_flex_2_5g_5_port_5_link_speed` | telemetry | unifi | diagnostic | disabled |
| `sensor.usw_flex_2_5g_5_state` | telemetry | unifi | diagnostic | available |
| `sensor.usw_flex_2_5g_5_uplink_mac` | telemetry | unifi | diagnostic | available |
| `sensor.usw_flex_2_5g_5_uptime` | telemetry | unifi | diagnostic | available |
| `switch.usw_flex_2_5g_5_port_1` | control | unifi | config | disabled |
| `switch.usw_flex_2_5g_5_port_2` | control | unifi | config | disabled |
| `switch.usw_flex_2_5g_5_port_3` | control | unifi | config | disabled |
| `switch.usw_flex_2_5g_5_port_4` | control | unifi | config | disabled |
| `switch.usw_flex_2_5g_5_port_5` | control | unifi | config | disabled |
| `update.usw_flex_2_5g_5` | telemetry | unifi | config | available |

#### UniFi Network

- Device ID: `device_bfecdd68ffca`
- Integration: unknown
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
| `binary_sensor.unnamed_room_microphone_7` | telemetry | sonos | diagnostic | unavailable |
| `device_tracker.sonoszp_10` | network | unifi | diagnostic | available |
| `media_player.unnamed_room_4` | control | sonos |  | unavailable |
| `number.unnamed_room_balance_9` | control | sonos | config | unavailable |
| `number.unnamed_room_bass_9` | control | sonos | config | unavailable |
| `number.unnamed_room_treble_9` | control | sonos | config | unavailable |
| `sensor.sonoszp_link_speed` | telemetry | unifi | diagnostic | disabled |
| `switch.unnamed_room_crossfade_9` | control | sonos | config | unavailable |
| `switch.unnamed_room_loudness_9` | control | sonos | config | unavailable |
| `switch.unnamed_room_status_light_9` | control | sonos | config | disabled |
| `switch.unnamed_room_touch_controls_9` | control | sonos | config | disabled |

#### Unnamed Room

- Device ID: `device_958d2caf578a`
- Integration: sonos, unifi
- Model: Sonos Era 100
- Capability mix: 2 telemetry, 8 control, 1 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `binary_sensor.unnamed_room_microphone_6` | telemetry | sonos | diagnostic | unavailable |
| `device_tracker.unifi_default_mac_e322eb2d1cf7` | network | unifi | diagnostic | available |
| `media_player.unnamed_room_3` | control | sonos |  | unavailable |
| `number.unnamed_room_balance_8` | control | sonos | config | unavailable |
| `number.unnamed_room_bass_8` | control | sonos | config | unavailable |
| `number.unnamed_room_treble_8` | control | sonos | config | unavailable |
| `sensor.link_speed_12` | telemetry | unifi | diagnostic | disabled |
| `switch.unnamed_room_crossfade_8` | control | sonos | config | unavailable |
| `switch.unnamed_room_loudness_8` | control | sonos | config | unavailable |
| `switch.unnamed_room_status_light_8` | control | sonos | config | disabled |
| `switch.unnamed_room_touch_controls_8` | control | sonos | config | disabled |

#### Unnamed Room

- Device ID: `device_cc546a11400c`
- Integration: sonos, unifi
- Model: Sonos Arc Ultra
- Capability mix: 3 telemetry, 16 control, 1 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `binary_sensor.unnamed_room_microphone_5` | telemetry | sonos | diagnostic | unavailable |
| `device_tracker.unifi_default_mac_0bbc683a0fb6` | network | unifi | diagnostic | available |
| `media_player.unnamed_room_2` | control | sonos |  | unavailable |
| `number.unnamed_room_audio_delay_2` | control | sonos | config | unavailable |
| `number.unnamed_room_balance_7` | control | sonos | config | unavailable |
| `number.unnamed_room_bass_7` | control | sonos | config | unavailable |
| `number.unnamed_room_music_surround_level_2` | control | sonos | config | unavailable |
| `number.unnamed_room_surround_level_2` | control | sonos | config | unavailable |
| `number.unnamed_room_treble_7` | control | sonos | config | unavailable |
| `select.unnamed_room_speech_enhancement` | control | sonos |  | unavailable |
| `sensor.link_speed_4` | telemetry | unifi | diagnostic | disabled |
| `sensor.unnamed_room_audio_input_format_2` | telemetry | sonos | diagnostic | unavailable |
| `switch.unnamed_room_crossfade_7` | control | sonos | config | unavailable |
| `switch.unnamed_room_loudness_7` | control | sonos | config | unavailable |
| `switch.unnamed_room_night_sound_2` | control | sonos | config | unavailable |
| `switch.unnamed_room_speech_enhancement_2` | control | sonos | config | unavailable |
| `switch.unnamed_room_status_light_7` | control | sonos | config | disabled |
| `switch.unnamed_room_surround_enabled_2` | control | sonos | config | unavailable |
| `switch.unnamed_room_surround_music_full_volume_2` | control | sonos | config | unavailable |
| `switch.unnamed_room_touch_controls_7` | control | sonos | config | disabled |

#### Watch

- Device ID: `device_db8dee8fc2aa`
- Integration: unifi
- Model: unknown model
- Capability mix: 1 telemetry, 0 control, 1 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `device_tracker.watch_3` | network | unifi | diagnostic | available |
| `sensor.watch_link_speed` | telemetry | unifi | diagnostic | disabled |

#### Wynn's Room High resolution channel:21071

- Device ID: `device_51bb5c839cfd`
- Integration: unknown
- Model: Home Assistant Camera
- Capability mix: 0 telemetry, 0 control, 0 network, 0 other

_No registered entities._

#### apexcharts-card

- Device ID: `device_c52d3866edb7`
- Integration: hacs
- Model: RomRider plugin
- Capability mix: 1 telemetry, 1 control, 0 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `switch.apexcharts_card_pre_release` | control | hacs | diagnostic | disabled |
| `update.apexcharts_card_update` | telemetry | hacs | config | available |

#### browser_mod

- Device ID: `device_9e59c4081483`
- Integration: hacs
- Model: thomasloven integration
- Capability mix: 1 telemetry, 1 control, 0 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `switch.browser_mod_pre_release` | control | hacs | diagnostic | disabled |
| `update.browser_mod_update` | telemetry | hacs | config | available |

#### button-card

- Device ID: `device_7023603357b8`
- Integration: hacs
- Model: custom-cards plugin
- Capability mix: 1 telemetry, 1 control, 0 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `switch.button_card_pre_release` | control | hacs | diagnostic | disabled |
| `update.button_card_update` | telemetry | hacs | config | available |

#### card-mod

- Device ID: `device_a8302d8a0e9a`
- Integration: hacs
- Model: thomasloven plugin
- Capability mix: 1 telemetry, 1 control, 0 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `switch.card_mod_pre_release` | control | hacs | diagnostic | disabled |
| `update.card_mod_update` | telemetry | hacs | config | available |

#### device_029571f3b27b

- Device ID: `device_029571f3b27b`
- Integration: unifi
- Model: unknown model
- Capability mix: 1 telemetry, 0 control, 1 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `device_tracker.unifi_default_mac_e52ad2d9d62a` | network | unifi | diagnostic | available |
| `sensor.link_speed_17` | telemetry | unifi | diagnostic | disabled |

#### device_1aa897c2d0b4

- Device ID: `device_1aa897c2d0b4`
- Integration: unifi
- Model: unknown model
- Capability mix: 1 telemetry, 0 control, 1 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `device_tracker.unifi_default_mac_b019bd33cc89` | network | unifi | diagnostic | unavailable |
| `sensor.link_speed_6` | telemetry | unifi | diagnostic | disabled |

#### device_1c8c7be1ef1d

- Device ID: `device_1c8c7be1ef1d`
- Integration: unifi
- Model: unknown model
- Capability mix: 1 telemetry, 0 control, 1 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `device_tracker.unifi_default_mac_92902c5c8aa5` | network | unifi | diagnostic | available |
| `sensor.link_speed_18` | telemetry | unifi | diagnostic | disabled |

#### device_1cc45f5d1971

- Device ID: `device_1cc45f5d1971`
- Integration: unifi
- Model: unknown model
- Capability mix: 1 telemetry, 0 control, 1 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `device_tracker.unifi_default_mac_de716b80d9a5` | network | unifi | diagnostic | unavailable |
| `sensor.link_speed_3` | telemetry | unifi | diagnostic | disabled |

#### device_2a3f688bcd08

- Device ID: `device_2a3f688bcd08`
- Integration: unifi
- Model: unknown model
- Capability mix: 1 telemetry, 0 control, 1 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `device_tracker.unifi_default_mac_5042130907ce` | network | unifi | diagnostic | available |
| `sensor.link_speed_7` | telemetry | unifi | diagnostic | disabled |

#### device_2c405371e8c8

- Device ID: `device_2c405371e8c8`
- Integration: unifi
- Model: unknown model
- Capability mix: 1 telemetry, 0 control, 1 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `device_tracker.unifi_default_mac_b01ea2b181ff` | network | unifi | diagnostic | unavailable |
| `sensor.link_speed_11` | telemetry | unifi | diagnostic | disabled |

#### device_3ccbd9acaad8

- Device ID: `device_3ccbd9acaad8`
- Integration: unifi
- Model: Lumi United Technology Co., Ltd
- Capability mix: 1 telemetry, 0 control, 1 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `device_tracker.unifi_default_mac_754c3a1ea02a` | network | unifi | diagnostic | available |
| `sensor.link_speed_8` | telemetry | unifi | diagnostic | disabled |

#### device_52184e4933c8

- Device ID: `device_52184e4933c8`
- Integration: unifi
- Model: unknown model
- Capability mix: 1 telemetry, 0 control, 1 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `device_tracker.unifi_default_mac_e29de8de1f70` | network | unifi | diagnostic | unavailable |
| `sensor.link_speed_9` | telemetry | unifi | diagnostic | disabled |

#### device_70d43284b9e8

- Device ID: `device_70d43284b9e8`
- Integration: unifi
- Model: unknown model
- Capability mix: 1 telemetry, 0 control, 1 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `device_tracker.unifi_default_mac_dd5079c60353` | network | unifi | diagnostic | available |
| `sensor.link_speed` | telemetry | unifi | diagnostic | disabled |

#### device_718ecc76e7ae

- Device ID: `device_718ecc76e7ae`
- Integration: unifi
- Model: unknown model
- Capability mix: 1 telemetry, 0 control, 1 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `device_tracker.unifi_default_mac_c0992a5e4e02` | network | unifi | diagnostic | available |
| `sensor.link_speed_24` | telemetry | unifi | diagnostic | disabled |

#### device_7bb64bc09fcd

- Device ID: `device_7bb64bc09fcd`
- Integration: unifi
- Model: unknown model
- Capability mix: 1 telemetry, 0 control, 1 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `device_tracker.unifi_default_mac_d129d9e3d6b1` | network | unifi | diagnostic | available |
| `sensor.link_speed_20` | telemetry | unifi | diagnostic | disabled |

#### device_7e76f4adbfbd

- Device ID: `device_7e76f4adbfbd`
- Integration: unifi
- Model: unknown model
- Capability mix: 1 telemetry, 0 control, 1 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `device_tracker.unifi_default_mac_7ed0c6182c02` | network | unifi | diagnostic | unavailable |
| `sensor.link_speed_10` | telemetry | unifi | diagnostic | disabled |

#### device_82c872eddb70

- Device ID: `device_82c872eddb70`
- Integration: unifi
- Model: unknown model
- Capability mix: 1 telemetry, 0 control, 1 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `device_tracker.unifi_default_mac_d112ffa56fc6` | network | unifi | diagnostic | available |
| `sensor.link_speed_25` | telemetry | unifi | diagnostic | disabled |

#### device_8bab5559bc0b

- Device ID: `device_8bab5559bc0b`
- Integration: unifi
- Model: unknown model
- Capability mix: 1 telemetry, 0 control, 1 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `device_tracker.unifi_default_mac_d9959f2a8987` | network | unifi | diagnostic | available |
| `sensor.link_speed_26` | telemetry | unifi | diagnostic | disabled |

#### device_a077a8676de8

- Device ID: `device_a077a8676de8`
- Integration: unifi
- Model: unknown model
- Capability mix: 1 telemetry, 0 control, 1 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `device_tracker.unifi_default_mac_3c3d46c29f27` | network | unifi | diagnostic | available |
| `sensor.link_speed_23` | telemetry | unifi | diagnostic | disabled |

#### device_ab496f7a7d51

- Device ID: `device_ab496f7a7d51`
- Integration: unifi
- Model: unknown model
- Capability mix: 1 telemetry, 0 control, 1 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `device_tracker.unifi_default_mac_f209cb9d07da` | network | unifi | diagnostic | available |
| `sensor.link_speed_28` | telemetry | unifi | diagnostic | disabled |

#### device_abb8fec33d8d

- Device ID: `device_abb8fec33d8d`
- Integration: unifi
- Model: unknown model
- Capability mix: 1 telemetry, 0 control, 1 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `device_tracker.unifi_default_mac_9878938b26f8` | network | unifi | diagnostic | available |
| `sensor.link_speed_13` | telemetry | unifi | diagnostic | disabled |

#### device_af20e0206ce0

- Device ID: `device_af20e0206ce0`
- Integration: unifi
- Model: unknown model
- Capability mix: 1 telemetry, 0 control, 1 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `device_tracker.unifi_default_mac_4e93a0a4b48b` | network | unifi | diagnostic | available |
| `sensor.link_speed_27` | telemetry | unifi | diagnostic | disabled |

#### device_bc00b8395464

- Device ID: `device_bc00b8395464`
- Integration: unifi
- Model: unknown model
- Capability mix: 1 telemetry, 0 control, 1 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `device_tracker.unifi_default_mac_a38f4e4b84a0` | network | unifi | diagnostic | unavailable |
| `sensor.link_speed_5` | telemetry | unifi | diagnostic | disabled |

#### device_c06583cbe783

- Device ID: `device_c06583cbe783`
- Integration: unifi
- Model: unknown model
- Capability mix: 1 telemetry, 0 control, 1 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `device_tracker.unifi_default_mac_29c96008c22e` | network | unifi | diagnostic | available |
| `sensor.link_speed_16` | telemetry | unifi | diagnostic | disabled |

#### device_c47d5565d225

- Device ID: `device_c47d5565d225`
- Integration: unifi
- Model: unknown model
- Capability mix: 1 telemetry, 0 control, 1 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `device_tracker.unifi_default_mac_be3f4a9ec204` | network | unifi | diagnostic | available |
| `sensor.link_speed_15` | telemetry | unifi | diagnostic | disabled |

#### device_c8b798d0e2b2

- Device ID: `device_c8b798d0e2b2`
- Integration: unifi
- Model: unknown model
- Capability mix: 1 telemetry, 0 control, 1 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `device_tracker.unifi_default_mac_2c894ada8b0b` | network | unifi | diagnostic | available |
| `sensor.link_speed_19` | telemetry | unifi | diagnostic | disabled |

#### device_e90900658a90

- Device ID: `device_e90900658a90`
- Integration: unifi
- Model: unknown model
- Capability mix: 1 telemetry, 0 control, 1 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `device_tracker.unifi_default_mac_d8484ff5d8dc` | network | unifi | diagnostic | available |
| `sensor.link_speed_14` | telemetry | unifi | diagnostic | disabled |

#### device_e9b166e8b6d8

- Device ID: `device_e9b166e8b6d8`
- Integration: unifi
- Model: unknown model
- Capability mix: 1 telemetry, 0 control, 1 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `device_tracker.unifi_default_mac_e75396edd3fe` | network | unifi | diagnostic | available |
| `sensor.link_speed_2` | telemetry | unifi | diagnostic | disabled |

#### iPad

- Device ID: `device_29a3a3367e9a`
- Integration: mobile_app
- Model: Apple iPad13,1
- Capability mix: 12 telemetry, 0 control, 0 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `device_tracker.ipad_2` | telemetry | mobile_app | diagnostic | available |
| `sensor.ipad_app_version` | telemetry | mobile_app | diagnostic | available |
| `sensor.ipad_audio_output` | telemetry | mobile_app |  | unavailable |
| `sensor.ipad_battery_level` | telemetry | mobile_app |  | available |
| `sensor.ipad_battery_state` | telemetry | mobile_app |  | available |
| `sensor.ipad_bssid` | telemetry | mobile_app |  | unavailable |
| `sensor.ipad_connection_type` | telemetry | mobile_app |  | unavailable |
| `sensor.ipad_geocoded_location` | telemetry | mobile_app |  | unavailable |
| `sensor.ipad_last_update_trigger` | telemetry | mobile_app |  | unavailable |
| `sensor.ipad_location_permission` | telemetry | mobile_app |  | available |
| `sensor.ipad_ssid` | telemetry | mobile_app |  | unavailable |
| `sensor.ipad_storage` | telemetry | mobile_app |  | unavailable |

#### iPhone

- Device ID: `device_39dfc0b93cda`
- Integration: unifi
- Model: unknown model
- Capability mix: 1 telemetry, 0 control, 1 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `device_tracker.iphone` | network | unifi | diagnostic | available |
| `sensor.iphone_link_speed` | telemetry | unifi | diagnostic | disabled |

#### mini-graph-card

- Device ID: `device_d6ad629b5b1b`
- Integration: hacs
- Model: kalkih plugin
- Capability mix: 1 telemetry, 1 control, 0 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `switch.mini_graph_card_pre_release` | control | hacs | diagnostic | disabled |
| `update.mini_graph_card_update` | telemetry | hacs | config | available |

#### ratgdo32disco c26634

- Device ID: `device_04ffe7f4ba2c`
- Integration: esphome, unifi
- Model: ratgdo v32disco_secplus2
- Capability mix: 17 telemetry, 18 control, 1 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `binary_sensor.ratgdo32disco_c26634_button` | telemetry | esphome | diagnostic | available |
| `binary_sensor.ratgdo32disco_c26634_dry_contact_close` | telemetry | esphome | diagnostic | available |
| `binary_sensor.ratgdo32disco_c26634_dry_contact_light` | telemetry | esphome | diagnostic | available |
| `binary_sensor.ratgdo32disco_c26634_dry_contact_open` | telemetry | esphome | diagnostic | available |
| `binary_sensor.ratgdo32disco_c26634_motion` | telemetry | esphome |  | available |
| `binary_sensor.ratgdo32disco_c26634_motor` | telemetry | esphome | diagnostic | available |
| `binary_sensor.ratgdo32disco_c26634_obstruction` | telemetry | esphome |  | available |
| `binary_sensor.ratgdo32disco_c26634_vehicle_arriving` | telemetry | esphome |  | available |
| `binary_sensor.ratgdo32disco_c26634_vehicle_detected` | telemetry | esphome |  | available |
| `binary_sensor.ratgdo32disco_c26634_vehicle_leaving` | telemetry | esphome |  | available |
| `button.ratgdo32disco_c26634_query_openings` | control | esphome | diagnostic | unknown |
| `button.ratgdo32disco_c26634_query_status` | control | esphome | diagnostic | unknown |
| `button.ratgdo32disco_c26634_restart` | control | esphome | config | unknown |
| `button.ratgdo32disco_c26634_safe_mode_boot` | control | esphome | diagnostic | unknown |
| `button.ratgdo32disco_c26634_sync` | control | esphome | diagnostic | unknown |
| `button.ratgdo32disco_c26634_toggle_door` | control | esphome |  | available |
| `cover.ratgdo32disco_c26634_door` | control | esphome |  | available |
| `device_tracker.ratgdo` | network | unifi | diagnostic | available |
| `light.ratgdo32disco_c26634_light` | control | esphome |  | available |
| `lock.ratgdo32disco_c26634_lock_remotes` | control | esphome |  | available |
| `number.ratgdo32disco_c26634_client_id` | control | esphome | config | available |
| `number.ratgdo32disco_c26634_closing_delay` | control | esphome | config | available |
| `number.ratgdo32disco_c26634_closing_duration` | control | esphome | config | available |
| `number.ratgdo32disco_c26634_opening_duration` | control | esphome | config | available |
| `number.ratgdo32disco_c26634_rolling_code_counter` | control | esphome | config | available |
| `number.ratgdo32disco_c26634_vehicle_distance_target` | control | esphome | config | unknown |
| `sensor.ratgdo32disco_c26634_firmware_version` | telemetry | esphome | diagnostic | available |
| `sensor.ratgdo32disco_c26634_openings` | telemetry | esphome | diagnostic | available |
| `sensor.ratgdo32disco_c26634_paired_devices` | telemetry | esphome | diagnostic | available |
| `sensor.ratgdo32disco_c26634_vehicle_distance_actual_filtered` | telemetry | esphome |  | available |
| `sensor.ratgdo32disco_c26634_voltage` | telemetry | esphome |  | available |
| `sensor.ratgdo32disco_c26634_wifi_signal` | telemetry | esphome | diagnostic | available |
| `sensor.ratgdo_link_speed` | telemetry | unifi | diagnostic | disabled |
| `switch.ratgdo32disco_c26634_laser` | control | esphome | config | available |
| `switch.ratgdo32disco_c26634_learn` | control | esphome | config | available |
| `switch.ratgdo32disco_c26634_led` | control | esphome | config | available |

#### visionOS & iOS 26 Liquid Glass Theme

- Device ID: `device_cbfb7f8b93cb`
- Integration: hacs
- Model: Nezz theme
- Capability mix: 1 telemetry, 1 control, 0 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `switch.visionos_ios_26_liquid_glass_theme_pre_release` | control | hacs | diagnostic | disabled |
| `update.visionos_ios_26_liquid_glass_theme_update` | telemetry | hacs | config | available |

### Unnamed Room

#### Master Sonos

- Device ID: `device_f1a2af0f711a`
- Integration: sonos, unifi
- Model: Sonos Beam
- Capability mix: 2 telemetry, 17 control, 1 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `binary_sensor.unnamed_room_microphone` | telemetry | sonos | diagnostic | unavailable |
| `device_tracker.sonos_beam_master` | network | unifi | diagnostic | available |
| `media_player.unnamed_room` | control | sonos |  | unavailable |
| `number.master_sonos_sub_gain` | control | sonos | config | unavailable |
| `number.unnamed_room_audio_delay` | control | sonos | config | unavailable |
| `number.unnamed_room_balance` | control | sonos | config | unavailable |
| `number.unnamed_room_bass` | control | sonos | config | unavailable |
| `number.unnamed_room_music_surround_level` | control | sonos | config | unavailable |
| `number.unnamed_room_surround_level` | control | sonos | config | unavailable |
| `number.unnamed_room_treble` | control | sonos | config | unavailable |
| `sensor.unnamed_room_audio_input_format` | telemetry | sonos | diagnostic | unavailable |
| `switch.master_sonos_subwoofer_enabled` | control | sonos | config | unavailable |
| `switch.unnamed_room_crossfade` | control | sonos | config | unavailable |
| `switch.unnamed_room_loudness` | control | sonos | config | unavailable |
| `switch.unnamed_room_night_sound` | control | sonos | config | unavailable |
| `switch.unnamed_room_speech_enhancement` | control | sonos | config | unavailable |
| `switch.unnamed_room_status_light` | control | sonos | config | disabled |
| `switch.unnamed_room_surround_enabled` | control | sonos | config | unavailable |
| `switch.unnamed_room_surround_music_full_volume` | control | sonos | config | unavailable |
| `switch.unnamed_room_touch_controls` | control | sonos | config | disabled |

#### Office

- Device ID: `device_f5cc48a3b632`
- Integration: sonos, unifi
- Model: Sonos Arc Ultra
- Capability mix: 2 telemetry, 18 control, 1 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `binary_sensor.unnamed_room_microphone_4` | telemetry | sonos | diagnostic | unavailable |
| `device_tracker.sonoszp_4` | network | unifi | diagnostic | unavailable |
| `media_player.unnamed_room_6` | control | sonos |  | unavailable |
| `number.office_audio_delay` | control | sonos | config | unavailable |
| `number.office_music_surround_level` | control | sonos | config | unavailable |
| `number.office_sub_gain` | control | sonos | config | unavailable |
| `number.office_surround_level` | control | sonos | config | unavailable |
| `number.unnamed_room_balance_6` | control | sonos | config | unavailable |
| `number.unnamed_room_bass_6` | control | sonos | config | unavailable |
| `number.unnamed_room_treble_6` | control | sonos | config | unavailable |
| `select.office_speech_enhancement` | control | sonos |  | unavailable |
| `sensor.office_audio_input_format` | telemetry | sonos | diagnostic | unavailable |
| `switch.office_night_sound` | control | sonos | config | unavailable |
| `switch.office_speech_enhancement` | control | sonos | config | unavailable |
| `switch.office_subwoofer_enabled` | control | sonos | config | unavailable |
| `switch.office_surround_enabled` | control | sonos | config | unavailable |
| `switch.office_surround_music_full_volume` | control | sonos | config | unavailable |
| `switch.unnamed_room_crossfade_6` | control | sonos | config | unavailable |
| `switch.unnamed_room_loudness_6` | control | sonos | config | unavailable |
| `switch.unnamed_room_status_light_6` | control | sonos | config | disabled |
| `switch.unnamed_room_touch_controls_6` | control | sonos | config | disabled |

#### Unnamed Room

- Device ID: `device_03b5c329a9f3`
- Integration: sonos, unifi
- Model: Sonos One SL
- Capability mix: 0 telemetry, 7 control, 1 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `device_tracker.sonoszp_15` | network | unifi | diagnostic | available |
| `number.unnamed_room_balance_3` | control | sonos | config | unavailable |
| `number.unnamed_room_bass_3` | control | sonos | config | unavailable |
| `number.unnamed_room_treble_3` | control | sonos | config | unavailable |
| `switch.unnamed_room_crossfade_3` | control | sonos | config | unavailable |
| `switch.unnamed_room_loudness_3` | control | sonos | config | unavailable |
| `switch.unnamed_room_status_light_3` | control | sonos | config | disabled |
| `switch.unnamed_room_touch_controls_3` | control | sonos | config | disabled |

#### Unnamed Room

- Device ID: `device_41760008fad9`
- Integration: sonos, unifi
- Model: Sonos Era 300
- Capability mix: 1 telemetry, 7 control, 1 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `binary_sensor.unnamed_room_microphone_3` | telemetry | sonos | diagnostic | unavailable |
| `device_tracker.sonoszp_11` | network | unifi | diagnostic | available |
| `number.unnamed_room_balance_5` | control | sonos | config | unavailable |
| `number.unnamed_room_bass_5` | control | sonos | config | unavailable |
| `number.unnamed_room_treble_5` | control | sonos | config | unavailable |
| `switch.unnamed_room_crossfade_5` | control | sonos | config | unavailable |
| `switch.unnamed_room_loudness_5` | control | sonos | config | unavailable |
| `switch.unnamed_room_status_light_5` | control | sonos | config | disabled |
| `switch.unnamed_room_touch_controls_5` | control | sonos | config | disabled |

#### Unnamed Room

- Device ID: `device_59c87770e78a`
- Integration: sonos, unifi
- Model: Sonos Era 300
- Capability mix: 1 telemetry, 7 control, 1 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `binary_sensor.unnamed_room_microphone_2` | telemetry | sonos | diagnostic | unavailable |
| `device_tracker.sonoszp_12` | network | unifi | diagnostic | available |
| `number.unnamed_room_balance_4` | control | sonos | config | unavailable |
| `number.unnamed_room_bass_4` | control | sonos | config | unavailable |
| `number.unnamed_room_treble_4` | control | sonos | config | unavailable |
| `switch.unnamed_room_crossfade_4` | control | sonos | config | unavailable |
| `switch.unnamed_room_loudness_4` | control | sonos | config | unavailable |
| `switch.unnamed_room_status_light_4` | control | sonos | config | disabled |
| `switch.unnamed_room_touch_controls_4` | control | sonos | config | disabled |

#### Unnamed Room

- Device ID: `device_73cd04bd08c1`
- Integration: sonos, unifi
- Model: Sonos One SL
- Capability mix: 0 telemetry, 7 control, 1 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `device_tracker.sonoszp_14` | network | unifi | diagnostic | available |
| `number.unnamed_room_balance_2` | control | sonos | config | unavailable |
| `number.unnamed_room_bass_2` | control | sonos | config | unavailable |
| `number.unnamed_room_treble_2` | control | sonos | config | unavailable |
| `switch.unnamed_room_crossfade_2` | control | sonos | config | unavailable |
| `switch.unnamed_room_loudness_2` | control | sonos | config | unavailable |
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
| `light.upstairs_hallway_main_lights` | control | lutron_caseta |  | available |

### Vestibule

#### Vestibule Main Lights

- Device ID: `device_bdc194038091`
- Integration: lutron_caseta
- Model: Lutron Electronics Co., Inc DVRF-6L (DivaSmartDimmer)
- Capability mix: 0 telemetry, 1 control, 0 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `light.vestibule_main_lights` | control | lutron_caseta |  | available |

### Wynn's Room

#### Wynn Ecobee Sensor

- Device ID: `device_082478169dde`
- Integration: homekit_controller
- Model: ecobee Inc. EBERS41
- Capability mix: 4 telemetry, 1 control, 0 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `binary_sensor.wynn_room_motion` | telemetry | homekit_controller |  | available |
| `binary_sensor.wynn_room_occupancy` | telemetry | homekit_controller |  | available |
| `button.wynn_room_identify` | control | homekit_controller | diagnostic | unknown |
| `sensor.wynn_room_battery` | telemetry | homekit_controller | diagnostic | available |
| `sensor.wynn_room_temperature` | telemetry | homekit_controller |  | available |

#### Wynn Sonos

- Device ID: `device_d2716c1c55b9`
- Integration: sonos, unifi
- Model: Sonos Era 100
- Capability mix: 1 telemetry, 8 control, 1 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `binary_sensor.wynn_s_room_microphone` | telemetry | sonos | diagnostic | available |
| `device_tracker.sonoszp_3` | network | unifi | diagnostic | available |
| `media_player.wynn_s_room` | control | sonos |  | available |
| `number.wynn_s_room_balance` | control | sonos | config | available |
| `number.wynn_s_room_bass` | control | sonos | config | available |
| `number.wynn_s_room_treble` | control | sonos | config | available |
| `switch.wynn_s_room_crossfade` | control | sonos | config | available |
| `switch.wynn_s_room_loudness` | control | sonos | config | available |
| `switch.wynn_s_room_status_light` | control | sonos | config | disabled |
| `switch.wynn_s_room_touch_controls` | control | sonos | config | disabled |

#### Wynn's Room Ceiling Lights

- Device ID: `device_6184e9d265d3`
- Integration: lutron_caseta
- Model: Lutron Electronics Co., Inc DVRF-6L (DivaSmartDimmer)
- Capability mix: 0 telemetry, 1 control, 0 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `light.wynn_s_room_ceiling_lights` | control | lutron_caseta |  | available |

#### Wynn's Room Chandelier

- Device ID: `device_92315b9002df`
- Integration: lutron_caseta
- Model: Lutron Electronics Co., Inc DVRF-6L (DivaSmartDimmer)
- Capability mix: 0 telemetry, 1 control, 0 network, 0 other

| Entity | Role | Integration | Detail | Availability |
| --- | --- | --- | --- | --- |
| `light.wynn_s_room_chandelier` | control | lutron_caseta |  | available |

## Orphan Entities

| Entity | Name | Role | Integration | Availability |
| --- | --- | --- | --- | --- |
| `automation.bonticou_llc_de_franchise_tax_notification_actions` | Bonticou - DE Franchise Tax Notification Actions | other | automation | available |
| `automation.bonticou_llc_de_franchise_tax_reminder` | Bonticou - DE Franchise Tax Reminder | other | automation | available |
| `automation.cameras_latest_motion_tracker` | Cameras - Latest Motion Tracker | other | automation | available |
| `automation.casey_driver_license_ai_renewal_notification_actions` | Casey Driver License — Renewal Notification Actions | other | automation | available |
| `automation.casey_driver_license_ai_renewal_reminder` | Casey Driver License — Renewal Reminder | other | automation | available |
| `automation.casey_passport_ai_renewal_notification_actions` | Casey Passport — Renewal Notification Actions | other | automation | available |
| `automation.casey_passport_ai_renewal_reminder` | Casey Passport — Renewal Reminder | other | automation | available |
| `automation.climate_basement_humidity_watch` | Climate — Basement Humidity Watch | other | automation | unavailable |
| `automation.climate_downstairs_auto_apply` | Climate — Downstairs Auto Apply | other | automation | unavailable |
| `automation.climate_downstairs_comfort_profile_actions` | Climate — Downstairs Comfort Profile Actions | other | automation | unavailable |
| `automation.climate_downstairs_comfort_profile_notification` | Environment — Main Floor Away Watch | other | automation | available |
| `automation.climate_downstairs_override_cleanup` | Climate — Downstairs Override Cleanup | other | automation | unavailable |
| `automation.climate_downstairs_pilot_startup_sync` | Environment — Startup Sync | other | automation | available |
| `automation.climate_downstairs_recommendation_actions` | Climate — Downstairs Recommendation Actions | other | automation | unavailable |
| `automation.climate_downstairs_recommendation_notification` | Environment — Main Floor Open Window Dashboard Only | other | automation | available |
| `automation.climate_downstairs_schedule_change_notification` | Climate — Downstairs Schedule Change Notification | other | automation | unavailable |
| `automation.climate_downstairs_sensor_spread_watch` | Environment — Main Floor Sensor Spread Watch | other | automation | available |
| `automation.commute_metro_north_first_weekday_departure` | Commute — Metro-North First Weekday Departure | other | automation | available |
| `automation.commute_reset_metro_north_daily_reminder` | Commute — Reset Metro-North Daily Reminder | other | automation | available |
| `automation.driver_license_ai_renewal_notification_actions` | Driver License — Renewal Notification Actions | other | automation | available |
| `automation.driver_license_ai_renewal_reminder` | Driver License — Renewal Reminder | other | automation | available |
| `automation.dryer_vent_annual_cleaning_reminder` | Dryer Vent — Annual Cleaning Reminder | other | automation | available |
| `automation.dryer_vent_maintenance_notification_actions` | Dryer Vent — Maintenance Notification Actions | other | automation | available |
| `automation.environment_basement_humidity_watch` | Environment — Basement Humidity Watch | other | automation | available |
| `automation.environment_basement_radon_notification` | Environment — Basement Radon Notification | other | automation | available |
| `automation.environment_clear_room_alerts` | Environment — Clear Room Alerts | other | automation | available |
| `automation.environment_room_actionable_alerts` | Environment — Room Actionable Alerts | other | automation | available |
| `automation.espresso_morning_maintenance_reminder` | Espresso — Morning Maintenance Reminder | other | automation | available |
| `automation.espresso_notification_actions` | Espresso — Notification Actions | other | automation | available |
| `automation.frame_tv_idle_behavior` | Frame TV — Idle Behavior | other | automation | unavailable |
| `automation.frontend_set_liquid_glass_theme` | Frontend — Set Liquid Glass Theme | other | automation | available |
| `automation.garbage_recycling_night_before_and_morning_reminders` | Garbage Recycling - Night Before And Morning Reminders | other | automation | available |
| `automation.garbage_recycling_notification_actions` | Garbage Recycling - Notification Actions | other | automation | available |
| `automation.garden_afternoon_weather_protection_notification` | Garden — Afternoon Weather Protection Notification | other | automation | available |
| `automation.garden_basil_hardening_reminder` | Garden — Basil Hardening Reminder | other | automation | unavailable |
| `automation.garden_basil_move_outside_reminder` | Garden — Basil Move Outside Reminder | other | automation | unavailable |
| `automation.garden_bok_choy_stage_dropdown_sync` | Garden — Bok Choy Stage Dropdown Sync | other | automation | available |
| `automation.garden_evening_moisture_review` | Garden — Evening Moisture Review | other | automation | unavailable |
| `automation.garden_issue_notification` | Garden — Issue Notification | other | automation | available |
| `automation.garden_marigolds_hardening_reminder` | Garden — Marigolds Hardening Reminder | other | automation | unavailable |
| `automation.garden_marigolds_move_outside_reminder` | Garden — Marigolds Move Outside Reminder | other | automation | unavailable |
| `automation.garden_morning_seedling_check` | Garden — Morning Seedling Check | other | automation | unavailable |
| `automation.garden_morning_stage_notification` | Garden — Morning Stage Notification | other | automation | available |
| `automation.garden_notification_actions` | Garden — Notification Actions | other | automation | available |
| `automation.garden_reset_daily_status` | Garden — Reset Daily Status | other | automation | unavailable |
| `automation.house_ai_clear_low_battery_notification` | House — Clear Low Battery Notification | other | automation | available |
| `automation.house_ai_low_battery_notification` | House — Low Battery Notification | other | automation | available |
| `automation.inventory_daily_change_digest` | Inventory — Daily Change Digest | other | automation | available |
| `automation.inventory_refresh_device_inventory` | Inventory — Refresh Device Inventory | other | automation | available |
| `automation.lights_door_lights_schedule_sync` | Lights — Door Lights Schedule Sync | other | automation | available |
| `automation.lights_foyer_chandelier_schedule_sync` | Lights — Foyer Chandelier Schedule Sync | other | automation | available |
| `automation.lights_front_stairs_schedule_sync` | Lights — Front Stairs Schedule Sync | other | automation | available |
| `automation.new_automation` | Noise Detection - Wynn's Room | other | automation | available |
| `automation.notices_ai_notification_action_history` | Notices — Notification Action History | other | automation | available |
| `automation.passport_ai_renewal_notification_actions` | Passport — Renewal Notification Actions | other | automation | available |
| `automation.passport_ai_renewal_reminder` | Passport — Renewal Reminder | other | automation | available |
| `automation.piano_annual_tuning_reminder` | Piano — Annual Tuning Reminder | other | automation | available |
| `automation.piano_tuning_notification_actions` | Piano — Tuning Notification Actions | other | automation | available |
| `automation.property_tax_ai_bill_and_due_week_reminders` | Property Tax - Bill And Due Week Reminders | other | automation | available |
| `automation.property_tax_ai_notification_actions` | Property Tax - Notification Actions | other | automation | available |
| `automation.robison_oil_annual_price_check_reminder` | Robison Oil — Annual Price Check Reminder | other | automation | available |
| `automation.robison_oil_annual_tune_up_reminder` | Robison Oil — Annual Tune-Up Reminder | other | automation | available |
| `automation.robison_oil_notification_actions` | Robison Oil — Notification Actions | other | automation | available |
| `automation.robison_oil_price_check_follow_up` | Robison Oil — Price Check Follow-Up | other | automation | available |
| `automation.security_alert_garage_door_unlocked` | Security Alert - Garage door unlocked | other | automation | unavailable |
| `automation.security_away_reminder_actions` | Security — Away Reminder Actions | other | automation | available |
| `automation.security_casey_left_combo_alert` | Security — Casey Left Combo Alert | other | automation | unavailable |
| `automation.security_casey_left_garage_unlocked` | Security — Casey Left Garage Unlocked | other | automation | unavailable |
| `automation.security_casey_left_lights_on` | Security — Casey Left Lights On | other | automation | unavailable |
| `automation.security_clear_away_reminder_when_resolved` | Security — Clear Away Reminder When Resolved | other | automation | available |
| `automation.security_clear_casey_left_combo_alert` | Security — Clear Casey Left Combo Alert | other | automation | available |
| `automation.security_clear_casey_left_garage_alert` | Security — Clear Casey Left Entry Alert | other | automation | available |
| `automation.security_clear_casey_left_lights_alert` | Security — Clear Casey Left Lights Alert | other | automation | available |
| `automation.security_entry_camera_notifications` | Security — Entry Camera Notifications | other | automation | unavailable |
| `automation.security_entry_ring_notifications` | Security — Entry Ring Notifications | other | automation | available |
| `automation.security_house_unsecured_while_away` | Security — House Unsecured While Away | other | automation | available |
| `automation.water_clear_notification_state_when_normal` | Water — Clear Notification State When Normal | other | automation | available |
| `automation.water_daytime_sustained_low_flow` | Water — Daytime Sustained Low Flow | other | automation | available |
| `automation.water_flo_system_alert` | Water — Flo System Alert | other | automation | available |
| `automation.water_high_daily_usage` | Water — High Daily Usage | other | automation | available |
| `automation.water_high_flow_burst_daytime` | Water — High Flow Burst (Daytime) | other | automation | available |
| `automation.water_high_flow_burst_overnight` | Water — High Flow Burst (Overnight) | other | automation | available |
| `automation.water_high_pressure` | Water — High Pressure | other | automation | available |
| `automation.water_leak_sensor_triggered` | Water — Leak Sensor Triggered | other | automation | available |
| `automation.water_low_pressure` | Water — Low Pressure | other | automation | available |
| `automation.water_low_pressure_persistent` | Water — Low Pressure Persistent | other | automation | available |
| `automation.water_notification_actions` | Water — Notification Actions | other | automation | available |
| `automation.water_overnight_continuous_flow_running_toilet` | Water — Overnight Continuous Flow (Running Toilet) | other | automation | available |
| `automation.water_pressure_drop_sudden` | Water — Pressure Drop (Sudden) | other | automation | available |
| `automation.water_pressure_recovered` | Water — Pressure Recovered | other | automation | available |
| `automation.water_shutoff_valve_closed` | Water — Shutoff Valve Closed | other | automation | available |
| `automation.water_very_low_pressure` | Water — Very Low Pressure | other | automation | available |
| `automation.water_very_low_pressure_persistent` | Water — Very Low Pressure Persistent | other | automation | available |
| `automation.wine_cave_abrupt_change_notification` | Wine Cave — Abrupt Change Notification | other | automation | available |
| `automation.wine_cave_cabinet_cleaning_reminder` | Wine Cave — Cabinet Cleaning Reminder | other | automation | available |
| `automation.wine_cave_charcoal_filter_reminder` | Wine Cave — Charcoal Filter Reminder | other | automation | available |
| `automation.wine_cave_clear_sensor_unavailable_notification` | Wine Cave — Clear Sensor Unavailable Notification | other | automation | available |
| `automation.wine_cave_condensation_risk_notification` | Wine Cave — Condensation Risk Notification | other | automation | available |
| `automation.wine_cave_cooling_cycle_notification` | Wine Cave — Cooling Cycle Notification | other | automation | available |
| `automation.wine_cave_cooling_cycle_overdue_notification` | Wine Cave — Cooling Cycle Overdue Notification | other | automation | available |
| `automation.wine_cave_cooling_cycle_settled_notification` | Wine Cave — Cooling Cycle Settled Notification | other | automation | available |
| `automation.wine_cave_cooling_cycle_unresolved_urgent` | Wine Cave — Cooling Cycle Unresolved Urgent | other | automation | available |
| `automation.wine_cave_drift_notification` | Wine Cave — Drift Notification | other | automation | available |
| `automation.wine_cave_maintenance_notification_actions` | Wine Cave — Maintenance Notification Actions | other | automation | available |
| `automation.wine_cave_moisture_anomaly_notification` | Wine Cave — Moisture Anomaly Notification | other | automation | available |
| `automation.wine_cave_rating_plate_one_time_reminder` | Wine Cave — Rating Plate One-Time Reminder | other | automation | available |
| `automation.wine_cave_recovery_notification` | Wine Cave — Clear Resolved Alert Notifications | other | automation | available |
| `automation.wine_cave_sensor_unavailable_notification` | Wine Cave — Sensor Unavailable Notification | other | automation | available |
| `automation.wine_cave_sensor_unavailable_urgent` | Wine Cave — Sensor Unavailable Urgent | other | automation | available |
| `automation.wine_cave_temperature_alerts` | Wine Cave — Temperature Alerts | other | automation | available |
| `automation.wine_cave_unresolved_attention_reminder` | Wine Cave — Unresolved Attention Reminder | other | automation | available |
| `automation.wine_refresh_cellar_som` | Wine — Refresh Cellar SOM | other | automation | unavailable |
| `binary_sensor.away_security_garage_door_open` | away_security_garage_door_open | telemetry | template | available |
| `binary_sensor.bonticou_llc_de_franchise_tax_due` | Bonticou LLC DE Franchise Tax Due | telemetry | template | available |
| `binary_sensor.casey_driver_license_renewal_due` | Casey Driver License Renewal Due | telemetry | template | available |
| `binary_sensor.casey_passport_renewal_due` | Casey Passport Renewal Due | telemetry | template | available |
| `binary_sensor.door_lights_schedule_active` | door_lights_schedule_active | telemetry | template | available |
| `binary_sensor.downstairs_everyone_away` | Main Floor Everyone Away | telemetry | template | available |
| `binary_sensor.downstairs_manual_override_active` | Downstairs Manual Override Active | telemetry | template | unavailable |
| `binary_sensor.downstairs_open_window_eligible` | Main Floor Open Window Eligible | telemetry | template | available |
| `binary_sensor.downstairs_someone_home` | Main Floor Someone Home | telemetry | template | available |
| `binary_sensor.downstairs_temp_spread_high` | Main Floor Temp Spread High | telemetry | template | available |
| `binary_sensor.driver_license_renewal_due` | Driver License Renewal Due | telemetry | template | available |
| `binary_sensor.dryer_vent_cleaning_due` | Dryer Vent Cleaning Due | telemetry | template | available |
| `binary_sensor.environment_attic_humidity_high_alert` | Environment Attic Humidity High Alert | telemetry | template | available |
| `binary_sensor.environment_attic_sensor_unavailable` | Environment Attic Sensor Unavailable | telemetry | template | available |
| `binary_sensor.environment_attic_temp_high_alert` | Environment Attic Temp High Alert | telemetry | template | available |
| `binary_sensor.environment_basement_airthings_battery_low_alert` | Environment Basement Airthings Battery Low Alert | telemetry | template | available |
| `binary_sensor.environment_basement_radon_high_alert` | Environment Basement Radon High Alert | telemetry | template | available |
| `binary_sensor.environment_basement_sensor_unavailable` | Environment Basement Sensor Unavailable | telemetry | template | available |
| `binary_sensor.environment_basement_temp_high_alert` | Environment Basement Temp High Alert | telemetry | template | available |
| `binary_sensor.environment_basement_temp_low_alert` | Environment Basement Temp Low Alert | telemetry | template | available |
| `binary_sensor.environment_dining_room_ecobee_humidity_disagreement` | Environment Dining Room Ecobee Humidity Disagreement | telemetry | template | available |
| `binary_sensor.environment_dining_room_ecobee_temp_disagreement` | Environment Dining Room Ecobee Temp Disagreement | telemetry | template | available |
| `binary_sensor.environment_dining_room_humidity_high_alert` | Environment Dining Room Humidity High Alert | telemetry | template | available |
| `binary_sensor.environment_dining_room_humidity_low_alert` | Environment Dining Room Humidity Low Alert | telemetry | template | available |
| `binary_sensor.environment_dining_room_sensor_unavailable` | Environment Dining Room Sensor Unavailable | telemetry | template | available |
| `binary_sensor.environment_dining_room_temp_high_alert` | Environment Dining Room Temp High Alert | telemetry | template | available |
| `binary_sensor.environment_dining_room_temp_low_alert` | Environment Dining Room Temp Low Alert | telemetry | template | available |
| `binary_sensor.environment_garage_humidity_high_alert` | Environment Garage Humidity High Alert | telemetry | template | available |
| `binary_sensor.environment_garage_sensor_unavailable` | Environment Garage Sensor Unavailable | telemetry | template | available |
| `binary_sensor.environment_garage_temp_high_alert` | Environment Garage Temp High Alert | telemetry | template | available |
| `binary_sensor.environment_garage_temp_low_alert` | Environment Garage Temp Low Alert | telemetry | template | available |
| `binary_sensor.environment_kitchen_humidity_high_alert` | Environment Kitchen Humidity High Alert | telemetry | template | available |
| `binary_sensor.environment_kitchen_humidity_low_alert` | Environment Kitchen Humidity Low Alert | telemetry | template | available |
| `binary_sensor.environment_kitchen_sensor_unavailable` | Environment Kitchen Sensor Unavailable | telemetry | template | available |
| `binary_sensor.environment_kitchen_temp_high_alert` | Environment Kitchen Temp High Alert | telemetry | template | available |
| `binary_sensor.environment_kitchen_temp_low_alert` | Environment Kitchen Temp Low Alert | telemetry | template | available |
| `binary_sensor.environment_primary_bedroom_battery_low_alert` | Environment Primary Bedroom Battery Low Alert | telemetry | template | available |
| `binary_sensor.environment_primary_bedroom_humidity_high_alert` | Environment Primary Bedroom Humidity High Alert | telemetry | template | available |
| `binary_sensor.environment_primary_bedroom_humidity_low_alert` | Environment Primary Bedroom Humidity Low Alert | telemetry | template | available |
| `binary_sensor.environment_primary_bedroom_sensor_unavailable` | Environment Primary Bedroom Sensor Unavailable | telemetry | template | available |
| `binary_sensor.environment_primary_bedroom_temp_high_alert` | Environment Primary Bedroom Temp High Alert | telemetry | template | available |
| `binary_sensor.environment_primary_bedroom_temp_low_alert` | Environment Primary Bedroom Temp Low Alert | telemetry | template | available |
| `binary_sensor.espresso_cafiza_clean_due` | Espresso Cafiza Clean Due | telemetry | template | available |
| `binary_sensor.espresso_maintenance_due` | Espresso Maintenance Due | telemetry | template | available |
| `binary_sensor.espresso_water_backflush_due` | Espresso Water Backflush Due | telemetry | template | available |
| `binary_sensor.foyer_chandelier_schedule_active` | foyer_chandelier_schedule_active | telemetry | template | available |
| `binary_sensor.front_stairs_schedule_active` | front_stairs_schedule_active | telemetry | template | available |
| `binary_sensor.garbage_recycling_takeout_due` | Garbage Recycling Takeout Due | telemetry | template | available |
| `binary_sensor.garden_actionable_alert` | Garden Actionable Alert | telemetry | template | available |
| `binary_sensor.garden_basil_weather_ready` | Garden Basil Weather Ready | telemetry | template | unavailable |
| `binary_sensor.garden_indoor_seedlings_active` | Garden Indoor Seedlings Active | telemetry | template | unavailable |
| `binary_sensor.garden_issue_attention_due` | Garden Issue Attention Due | telemetry | template | available |
| `binary_sensor.garden_marigolds_weather_ready` | Garden Marigolds Weather Ready | telemetry | template | unavailable |
| `binary_sensor.garden_needs_attention` | Garden Needs Attention | telemetry | template | available |
| `binary_sensor.garden_seedling_check_due` | Garden Seedling Check Due | telemetry | template | unavailable |
| `binary_sensor.garden_stage_action_due` | Garden Stage Action Due | telemetry | template | available |
| `binary_sensor.garden_water_review_due` | Garden Water Review Due | telemetry | template | unavailable |
| `binary_sensor.garden_weather_protection_due` | Garden Weather Protection Due | telemetry | template | available |
| `binary_sensor.house_battery_critical_alert` | House Battery Critical Alert | telemetry | template | available |
| `binary_sensor.house_battery_replace_soon_alert` | House Battery Replace Soon Alert | telemetry | template | available |
| `binary_sensor.house_low_battery_alert` | House Battery Getting Low Alert | telemetry | template | available |
| `binary_sensor.house_unsecured_while_away` | house_unsecured_while_away | telemetry | template | available |
| `binary_sensor.main_dashboard_sleep_hero_active` | main_dashboard_sleep_hero_active | telemetry | template | available |
| `binary_sensor.passport_renewal_due` | Passport Renewal Due | telemetry | template | available |
| `binary_sensor.piano_tuning_due` | Piano Tuning Due | telemetry | template | available |
| `binary_sensor.remote_ui` | Remote UI | telemetry | cloud | available |
| `binary_sensor.water_notification_alert_active` | Water Notification Alert Active | telemetry | template | available |
| `binary_sensor.wine_cave_actionable_alert` | Wine Cave Actionable Alert | telemetry | template | available |
| `binary_sensor.wine_cave_cabinet_cleaning_due` | Wine Cave Cabinet Cleaning Due | telemetry | template | available |
| `binary_sensor.wine_cave_charcoal_filter_due` | Wine Cave Charcoal Filter Due | telemetry | template | available |
| `binary_sensor.wine_cave_condensation_risk` | Wine Cave Condensation Risk | telemetry | template | available |
| `binary_sensor.wine_cave_cooling_cycle` | Wine Cave Cooling Cycle | telemetry | template | available |
| `binary_sensor.wine_cave_cycle_settled` | Wine Cave Cycle Settled | telemetry | template | available |
| `binary_sensor.wine_cave_drift_alert` | Wine Cave Drift Alert | telemetry | template | available |
| `binary_sensor.wine_cave_maintenance_due` | Wine Cave Maintenance Due | telemetry | template | available |
| `binary_sensor.wine_cave_moisture_anomaly` | Wine Cave Moisture Anomaly | telemetry | template | available |
| `binary_sensor.wine_cave_sensor_unavailable` | Wine Cave Sensor Unavailable | telemetry | template | available |
| `binary_sensor.wine_cave_temp_high_alert` | Wine Cave Temp High Alert | telemetry | template | available |
| `binary_sensor.wine_cave_temp_low_alert` | Wine Cave Temp Low Alert | telemetry | template | available |
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
| `device_tracker.iphone_6` | iPhone | network | unifi | disabled |
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
| `device_tracker.watch_2` | Watch | network | unifi | disabled |
| `input_boolean.business_admin_reminders_enabled` | Business Admin Reminders Enabled | control | input_boolean | available |
| `input_boolean.casey_driver_license_renewal_enabled` | Casey Driver License Renewal Enabled | control | input_boolean | available |
| `input_boolean.casey_passport_renewal_enabled` | Casey Passport Renewal Enabled | control | input_boolean | available |
| `input_boolean.downstairs_auto_apply_enabled` | Downstairs Auto Apply Enabled | control | input_boolean | unavailable |
| `input_boolean.downstairs_auto_off_for_open_windows` | Downstairs Auto Off For Open Windows | control | input_boolean | unavailable |
| `input_boolean.downstairs_mobile_alerts_enabled` | Main Floor Mobile Alerts Enabled | control | input_boolean | available |
| `input_boolean.downstairs_pilot_enabled` | Main Floor Pilot Enabled | control | input_boolean | available |
| `input_boolean.downstairs_vacation_mode` | Downstairs Vacation Mode | control | input_boolean | unavailable |
| `input_boolean.driver_license_renewal_enabled` | Driver License Renewal Enabled | control | input_boolean | available |
| `input_boolean.dryer_vent_maintenance_enabled` | Dryer Vent Maintenance Enabled | control | input_boolean | available |
| `input_boolean.environment_alerts_enabled` | Environment Alerts Enabled | control | input_boolean | available |
| `input_boolean.espresso_maintenance_enabled` | Espresso Maintenance Enabled | control | input_boolean | available |
| `input_boolean.foyer_chandelier_sleep_hold` | Foyer Chandelier Sleep Hold | control | input_boolean | available |
| `input_boolean.front_stairs_sleep_override` | Front Stairs Sleep Override | control | input_boolean | available |
| `input_boolean.garbage_recycling_reminders_enabled` | Garbage Recycling Reminders Enabled | control | input_boolean | available |
| `input_boolean.garden_action_panel_expanded` | Garden Action Panel Expanded | control | input_boolean | available |
| `input_boolean.garden_basil_hardening_off` | Garden Basil Hardening Off | control | input_boolean | unavailable |
| `input_boolean.garden_basil_outside` | Garden Basil Outside | control | input_boolean | unavailable |
| `input_boolean.garden_bok_choy_tile_expanded` | Garden Bok Choy Tile Expanded | control | input_boolean | available |
| `input_boolean.garden_cape_gooseberry_tile_expanded` | Garden Cape Gooseberry Tile Expanded | control | input_boolean | available |
| `input_boolean.garden_checked_today` | Garden Checked Today | control | input_boolean | unavailable |
| `input_boolean.garden_honeynut_squash_tile_expanded` | Garden Honeynut Squash Tile Expanded | control | input_boolean | available |
| `input_boolean.garden_marigolds_hardening_off` | Garden Marigolds Hardening Off | control | input_boolean | unavailable |
| `input_boolean.garden_marigolds_outside` | Garden Marigolds Outside | control | input_boolean | unavailable |
| `input_boolean.garden_notifications_enabled` | Garden Notifications Enabled | control | input_boolean | available |
| `input_boolean.garden_peppers_tile_expanded` | Garden Peppers Tile Expanded | control | input_boolean | available |
| `input_boolean.garden_spinach_in_ground` | Garden Spinach In Ground | control | input_boolean | available |
| `input_boolean.garden_spinach_tile_expanded` | Garden Spinach Tile Expanded | control | input_boolean | available |
| `input_boolean.garden_tomatoes_tile_expanded` | Garden Tomatoes Tile Expanded | control | input_boolean | available |
| `input_boolean.garden_tracking_enabled` | Garden Tracking Enabled | control | input_boolean | unavailable |
| `input_boolean.garden_watered_today` | Garden Watered Today | control | input_boolean | unavailable |
| `input_boolean.garden_watering_nudges_enabled` | Garden Watering Nudges Enabled | control | input_boolean | unavailable |
| `input_boolean.garden_weather_nudges_enabled` | Garden Weather Nudges Enabled | control | input_boolean | unavailable |
| `input_boolean.garden_weather_panel_expanded` | Garden Weather Panel Expanded | control | input_boolean | available |
| `input_boolean.house_battery_alerts_enabled` | House Battery Alerts Enabled | control | input_boolean | available |
| `input_boolean.interior_lights_guest_override` | Guest Lighting Override | control | input_boolean | available |
| `input_boolean.metro_north_commute_notified_today` | Metro-North Commute Notified Today | control | input_boolean | available |
| `input_boolean.passport_renewal_enabled` | Passport Renewal Enabled | control | input_boolean | available |
| `input_boolean.piano_care_enabled` | Piano Care Enabled | control | input_boolean | available |
| `input_boolean.tax_reminders_enabled` | Tax Reminders Enabled | control | input_boolean | available |
| `input_boolean.water_flow_alert_active` | Water Flow Alert Active | control | input_boolean | available |
| `input_boolean.water_leak_alert_active` | Water Leak Alert Active | control | input_boolean | available |
| `input_boolean.water_pressure_alert_active` | Water Pressure Alert Active | control | input_boolean | available |
| `input_boolean.water_usage_alert_active` | Water Usage Alert Active | control | input_boolean | available |
| `input_boolean.water_valve_alert_active` | Water Valve Alert Active | control | input_boolean | available |
| `input_boolean.wine_cave_maintenance_enabled` | Wine Cave Maintenance Enabled | control | input_boolean | available |
| `input_boolean.wine_cave_rating_plate_captured` | Wine Cave Rating Plate Captured | control | input_boolean | available |
| `input_boolean.wine_cave_rating_plate_reminder_sent` | Wine Cave Rating Plate Reminder Sent | control | input_boolean | available |
| `input_datetime.ai_garden_brief_updated` | AI Garden Brief Updated | control | input_datetime | unavailable |
| `input_datetime.ai_home_brief_updated` | AI Home Brief Updated | control | input_datetime | unavailable |
| `input_datetime.ai_wine_brief_updated` | AI Wine Brief Updated | control | input_datetime | unavailable |
| `input_datetime.away_security_snooze_until` | Away Security Snooze Until | control | input_datetime | available |
| `input_datetime.bonticou_llc_de_franchise_tax_last_paid_at` | Bonticou LLC DE Franchise Tax Last Paid At | control | input_datetime | available |
| `input_datetime.casey_driver_license_expiration_date` | Casey Driver License Expiration Date | control | input_datetime | available |
| `input_datetime.casey_driver_license_renewal_snooze_until` | Casey Driver License Renewal Snooze Until | control | input_datetime | available |
| `input_datetime.casey_driver_license_renewed_at` | Casey Driver License Renewed At | control | input_datetime | available |
| `input_datetime.casey_passport_expiration_date` | Casey Passport Expiration Date | control | input_datetime | available |
| `input_datetime.casey_passport_renewal_applied_at` | Casey Passport Renewal Applied At | control | input_datetime | available |
| `input_datetime.casey_passport_renewal_snooze_until` | Casey Passport Renewal Snooze Until | control | input_datetime | available |
| `input_datetime.downstairs_manual_override_until` | Downstairs Manual Override Until | control | input_datetime | unavailable |
| `input_datetime.driver_license_expiration_date` | Driver License Expiration Date | control | input_datetime | available |
| `input_datetime.driver_license_renewal_snooze_until` | Driver License Renewal Snooze Until | control | input_datetime | available |
| `input_datetime.driver_license_renewed_at` | Driver License Renewed At | control | input_datetime | available |
| `input_datetime.dryer_vent_cleaning_snooze_until` | Dryer Vent Cleaning Snooze Until | control | input_datetime | available |
| `input_datetime.dryer_vent_last_cleaned` | Dryer Vent Last Cleaned | control | input_datetime | available |
| `input_datetime.environment_radon_last_alert` | Environment Radon Last Alert | control | input_datetime | available |
| `input_datetime.espresso_last_cafiza_clean` | Espresso Last Cafiza Clean | control | input_datetime | available |
| `input_datetime.espresso_last_water_backflush` | Espresso Last Water Backflush | control | input_datetime | available |
| `input_datetime.espresso_maintenance_snooze_until` | Espresso Maintenance Snooze Until | control | input_datetime | available |
| `input_datetime.garbage_recycling_last_taken_out_at` | Garbage Recycling Last Taken Out At | control | input_datetime | available |
| `input_datetime.garden_basil_hardening_started` | Garden Basil Hardening Started | control | input_datetime | unavailable |
| `input_datetime.garden_basil_moved_outside` | Garden Basil Moved Outside | control | input_datetime | unavailable |
| `input_datetime.garden_bok_choy_planted` | Garden Bok Choy Planted | control | input_datetime | available |
| `input_datetime.garden_cape_gooseberry_hardening_started` | Garden Cape Gooseberry Hardening Started | control | input_datetime | available |
| `input_datetime.garden_cape_gooseberry_planted` | Garden Cape Gooseberry Planted | control | input_datetime | available |
| `input_datetime.garden_honeynut_squash_hardening_started` | Garden Honeynut Squash Hardening Started | control | input_datetime | available |
| `input_datetime.garden_honeynut_squash_planted` | Garden Honeynut Squash Planted | control | input_datetime | available |
| `input_datetime.garden_issue_last_notified_at` | Garden Issue Last Notified At | control | input_datetime | available |
| `input_datetime.garden_last_checked` | Garden Last Checked | control | input_datetime | unavailable |
| `input_datetime.garden_last_watered` | Garden Last Watered | control | input_datetime | unavailable |
| `input_datetime.garden_marigolds_hardening_started` | Garden Marigolds Hardening Started | control | input_datetime | unavailable |
| `input_datetime.garden_marigolds_moved_outside` | Garden Marigolds Moved Outside | control | input_datetime | unavailable |
| `input_datetime.garden_notifications_snooze_until` | Garden Notifications Snooze Until | control | input_datetime | available |
| `input_datetime.garden_peppers_hardening_started` | Garden Peppers Hardening Started | control | input_datetime | available |
| `input_datetime.garden_peppers_planted` | Garden Peppers Planted | control | input_datetime | available |
| `input_datetime.garden_seed_start_date` | Garden Seed Start Date | control | input_datetime | unavailable |
| `input_datetime.garden_spinach_last_watered` | Garden Spinach Last Watered | control | input_datetime | available |
| `input_datetime.garden_spinach_planted_in_ground` | Garden Spinach Planted In Ground | control | input_datetime | available |
| `input_datetime.garden_stage_last_notified_at` | Garden Stage Last Notified At | control | input_datetime | available |
| `input_datetime.garden_tomatoes_hardening_started` | Garden Tomatoes Hardening Started | control | input_datetime | available |
| `input_datetime.garden_tomatoes_planted` | Garden Tomatoes Planted | control | input_datetime | available |
| `input_datetime.garden_weather_last_notified_at` | Garden Weather Last Notified At | control | input_datetime | available |
| `input_datetime.latest_camera_motion_at` | Latest Camera Motion At | control | input_datetime | available |
| `input_datetime.passport_expiration_date` | Passport Expiration Date | control | input_datetime | available |
| `input_datetime.passport_renewal_applied_at` | Passport Renewal Applied At | control | input_datetime | available |
| `input_datetime.passport_renewal_snooze_until` | Passport Renewal Snooze Until | control | input_datetime | available |
| `input_datetime.piano_last_tuned` | Piano Last Tuned | control | input_datetime | available |
| `input_datetime.piano_tuning_snooze_until` | Piano Tuning Snooze Until | control | input_datetime | available |
| `input_datetime.robison_oil_price_check_last_done` | Robison Oil Price Check Last Done | control | input_datetime | available |
| `input_datetime.school_tax_january_last_paid_at` | School Tax January Last Paid At | control | input_datetime | available |
| `input_datetime.school_tax_september_last_paid_at` | School Tax September Last Paid At | control | input_datetime | available |
| `input_datetime.town_tax_last_paid_at` | Town Tax Last Paid At | control | input_datetime | available |
| `input_datetime.water_latest_alert_at` | Water Latest Alert At | control | input_datetime | available |
| `input_datetime.water_pressure_snooze_until` | Water Pressure Snooze Until | control | input_datetime | available |
| `input_datetime.wine_cave_cabinet_cleaning_snooze_until` | Wine Cave Cabinet Cleaning Snooze Until | control | input_datetime | available |
| `input_datetime.wine_cave_charcoal_filter_snooze_until` | Wine Cave Charcoal Filter Snooze Until | control | input_datetime | available |
| `input_datetime.wine_cave_delivery_date` | Wine Cave Delivery Date | control | input_datetime | available |
| `input_datetime.wine_cave_last_cabinet_cleaning` | Wine Cave Last Cabinet Cleaning | control | input_datetime | available |
| `input_datetime.wine_cave_last_charcoal_filter_check` | Wine Cave Last Charcoal Filter Check | control | input_datetime | available |
| `input_datetime.wine_cave_last_humidity_cartridge_check` | Wine Cave Last Humidity Cartridge Check | control | input_datetime | available |
| `input_datetime.wine_cave_parts_labor_warranty_review` | Wine Cave Parts Labor Warranty Review | control | input_datetime | available |
| `input_datetime.wine_cave_placed_in_service_date` | Wine Cave Placed In Service Date | control | input_datetime | available |
| `input_datetime.wine_cave_purchase_date` | Wine Cave Purchase Date | control | input_datetime | available |
| `input_number.downstairs_aux_cutover_temp` | Main Floor Aux Max Outdoor Temp | control | input_number | available |
| `input_number.downstairs_away_profile_delay_minutes` | Main Floor Away Profile Delay | control | input_number | available |
| `input_number.downstairs_compressor_lockout_temp` | Main Floor Compressor Lockout Temp | control | input_number | available |
| `input_number.downstairs_open_window_advantage` | Main Floor Open Window Advantage | control | input_number | available |
| `input_number.downstairs_shoulder_day_target` | Downstairs Shoulder Day Target | control | input_number | unavailable |
| `input_number.downstairs_shoulder_night_target` | Downstairs Shoulder Night Target | control | input_number | unavailable |
| `input_number.downstairs_sleep_profile_quiet_minutes` | Downstairs Sleep Quiet Minutes | control | input_number | unavailable |
| `input_number.downstairs_summer_day_target` | Downstairs Summer Day Target | control | input_number | unavailable |
| `input_number.downstairs_summer_night_target` | Downstairs Summer Night Target | control | input_number | unavailable |
| `input_number.downstairs_vacation_profile_delay_hours` | Downstairs Vacation Delay | control | input_number | unavailable |
| `input_number.downstairs_winter_day_target` | Downstairs Winter Day Target | control | input_number | unavailable |
| `input_number.downstairs_winter_night_target` | Downstairs Winter Night Target | control | input_number | unavailable |
| `input_select.downstairs_season_mode` | Main Floor Season Mode | control | input_select | available |
| `input_select.garden_basil_observation` | Garden Basil Observation | control | input_select | unavailable |
| `input_select.garden_bok_choy_observation` | Garden Bok Choy Observation | control | input_select | available |
| `input_select.garden_bok_choy_stage` | Garden Bok Choy Stage | control | input_select | available |
| `input_select.garden_cape_gooseberry_observation` | Garden Cape Gooseberry Observation | control | input_select | available |
| `input_select.garden_cape_gooseberry_stage` | Garden Cape Gooseberry Stage | control | input_select | available |
| `input_select.garden_honeynut_squash_observation` | Garden Honeynut Squash Observation | control | input_select | available |
| `input_select.garden_honeynut_squash_stage` | Garden Honeynut Squash Stage | control | input_select | available |
| `input_select.garden_marigolds_observation` | Garden Marigolds Observation | control | input_select | unavailable |
| `input_select.garden_peppers_observation` | Garden Peppers Observation | control | input_select | available |
| `input_select.garden_peppers_stage` | Garden Peppers Stage | control | input_select | available |
| `input_select.garden_spinach_observation` | Garden Spinach Observation | control | input_select | available |
| `input_select.garden_tomatoes_observation` | Garden Tomatoes Observation | control | input_select | available |
| `input_select.garden_tomatoes_stage` | Garden Tomatoes Stage | control | input_select | available |
| `input_text.ai_garden_brief` | AI Garden Brief | control | input_text | unavailable |
| `input_text.ai_home_brief` | AI Home Brief | control | input_text | unavailable |
| `input_text.ai_wine_brief` | AI Wine Brief | control | input_text | unavailable |
| `input_text.garbage_recycling_last_taken_out_pickup` | Garbage Recycling Last Taken Out Pickup | control | input_text | available |
| `input_text.latest_camera_motion_entity` | Latest Camera Motion Entity | control | input_text | available |
| `input_text.latest_camera_motion_label` | Latest Camera Motion Label | control | input_text | available |
| `input_text.water_latest_alert_kind` | Water Latest Alert Kind | control | input_text | available |
| `input_text.water_latest_alert_label` | Water Latest Alert Label | control | input_text | available |
| `light.family_room` | Family Room | control | group | available |
| `light.interior_test` | Interior (Test) | control | group | available |
| `light.wynn_s_room` | Wynn's Room | control | group | available |
| `person.bonticou` | Trevor | other | person | available |
| `person.casey` | Casey | other | person | available |
| `script.ai_refresh_garden_brief` | AI Refresh Garden Brief | other | script | unavailable |
| `script.ai_refresh_home_brief` | AI Refresh Home Brief | other | script | unavailable |
| `script.ai_refresh_wine_brief` | AI Refresh Wine Brief | other | script | unavailable |
| `script.away_security_clear_alert` | Away Security Clear Alert | other | script | available |
| `script.away_security_lock_unlocked_entry_doors` | Away Security Lock Unlocked Entry Doors | other | script | available |
| `script.away_security_send_alert` | Away Security Send Alert | other | script | available |
| `script.basement_humidity_clear_alert` | Basement Humidity Clear Alert | other | script | available |
| `script.basement_humidity_send_alert` | Basement Humidity Send Alert | other | script | available |
| `script.bonticou_llc_de_franchise_tax_clear_notification` | Bonticou - DE Franchise Tax Clear Notification | other | script | available |
| `script.bonticou_llc_de_franchise_tax_mark_paid` | Bonticou - DE Franchise Tax Mark Paid | other | script | available |
| `script.bonticou_llc_de_franchise_tax_send_reminder` | Bonticou - DE Franchise Tax Send Reminder | other | script | available |
| `script.casey_driver_license_clear_renewal_notification` | Casey Driver License Clear Renewal Notification | other | script | available |
| `script.casey_driver_license_mark_renewed` | Casey Driver License Mark Renewed | other | script | available |
| `script.casey_driver_license_send_renewal_reminder` | Casey Driver License Send Renewal Reminder | other | script | available |
| `script.casey_driver_license_snooze_renewal` | Casey Driver License Snooze Renewal | other | script | available |
| `script.casey_left_combo_clear_alert` | Casey Left Combo Clear Alert | other | script | available |
| `script.casey_left_combo_send_alert` | Casey Left Combo Send Alert | other | script | available |
| `script.casey_left_garage_clear_alert` | Casey Left Entry Clear Alert | other | script | available |
| `script.casey_left_garage_send_alert` | Casey Left Entry Send Alert | other | script | available |
| `script.casey_left_lights_clear_alert` | Casey Left Lights Clear Alert | other | script | available |
| `script.casey_left_lights_send_alert` | Casey Left Lights Send Alert | other | script | available |
| `script.casey_passport_clear_renewal_notification` | Casey Passport Clear Renewal Notification | other | script | available |
| `script.casey_passport_mark_renewal_applied` | Casey Passport Mark Renewal Applied | other | script | available |
| `script.casey_passport_send_renewal_reminder` | Casey Passport Send Renewal Reminder | other | script | available |
| `script.casey_passport_snooze_renewal` | Casey Passport Snooze Renewal | other | script | available |
| `script.common_areas_transition_toggle` | Common Areas Transition Toggle | other | script | available |
| `script.door_lights_schedule_off` | Door Lights Schedule Off | other | script | available |
| `script.door_lights_schedule_on` | Door Lights Schedule On | other | script | available |
| `script.downstairs_apply_profile_recommendation` | Downstairs Apply Profile Recommendation | other | script | unavailable |
| `script.downstairs_apply_recommendation` | Downstairs Apply Recommendation | other | script | unavailable |
| `script.downstairs_clear_override` | Downstairs Clear Override | other | script | unavailable |
| `script.downstairs_force_cool` | Downstairs Force Cool | other | script | unavailable |
| `script.downstairs_force_heat` | Downstairs Force Heat | other | script | unavailable |
| `script.downstairs_hvac_off_open_windows` | Downstairs HVAC Off Open Windows | other | script | unavailable |
| `script.downstairs_profile_away_test` | Downstairs Profile Away Test | other | script | unavailable |
| `script.downstairs_profile_clear_vacation` | Downstairs Profile Clear Vacation | other | script | unavailable |
| `script.downstairs_profile_home_test` | Downstairs Profile Home Test | other | script | unavailable |
| `script.downstairs_profile_sleep_test` | Downstairs Profile Sleep Test | other | script | unavailable |
| `script.downstairs_profile_vacation_test` | Downstairs Profile Vacation Test | other | script | unavailable |
| `script.driver_license_clear_renewal_notification` | Driver License Clear Renewal Notification | other | script | available |
| `script.driver_license_mark_renewed` | Driver License Mark Renewed | other | script | available |
| `script.driver_license_send_renewal_reminder` | Driver License Send Renewal Reminder | other | script | available |
| `script.driver_license_snooze_renewal` | Driver License Snooze Renewal | other | script | available |
| `script.dryer_vent_clear_cleaning_notification` | Dryer Vent Clear Cleaning Notification | other | script | available |
| `script.dryer_vent_mark_cleaning_done` | Dryer Vent Mark Cleaning Done | other | script | available |
| `script.dryer_vent_send_cleaning_reminder` | Dryer Vent Send Cleaning Reminder | other | script | available |
| `script.dryer_vent_snooze_cleaning` | Dryer Vent Snooze Cleaning | other | script | available |
| `script.entry_camera_send_alert` | Entry Camera Send Alert | other | script | available |
| `script.environment_send_alert` | Environment Send Alert | other | script | available |
| `script.espresso_clear_maintenance_notification` | Espresso Clear Maintenance Notification | other | script | available |
| `script.espresso_mark_cafiza_clean_done` | Espresso Mark Cafiza Clean Done | other | script | available |
| `script.espresso_mark_water_backflush_done` | Espresso Mark Water Backflush Done | other | script | available |
| `script.espresso_send_maintenance_notification` | Espresso Send Maintenance Notification | other | script | available |
| `script.espresso_snooze_maintenance` | Espresso Snooze Maintenance | other | script | available |
| `script.family_room_tv_mode_on` | Family Room TV Mode On | other | script | available |
| `script.foyer_chandelier_curved_transition` | Foyer Chandelier Linear Transition | other | script | available |
| `script.foyer_chandelier_schedule_off` | Foyer Chandelier Schedule Off | other | script | available |
| `script.foyer_chandelier_schedule_on` | Foyer Chandelier Schedule On | other | script | available |
| `script.foyer_chandelier_toggle` | Foyer Chandelier Toggle | other | script | available |
| `script.frame_tv_art_mode` | Frame TV Art Mode | other | script | unavailable |
| `script.frame_tv_off` | Frame TV Off | other | script | unavailable |
| `script.front_stairs_schedule_off` | Front Stairs Schedule Off | other | script | available |
| `script.front_stairs_schedule_on` | Front Stairs Schedule On | other | script | available |
| `script.garbage_recycling_clear_notification` | Garbage Recycling Clear Notification | other | script | available |
| `script.garbage_recycling_mark_taken_out` | Garbage Recycling Mark Taken Out | other | script | available |
| `script.garbage_recycling_send_reminder` | Garbage Recycling Send Reminder | other | script | available |
| `script.garden_apply_next_action` | Garden Apply Next Action | other | script | available |
| `script.garden_apply_next_stage` | Garden Apply Next Stage | other | script | unavailable |
| `script.garden_clear_notifications` | Garden Clear Notifications | other | script | available |
| `script.garden_mark_basil_outside` | Garden Mark Basil Outside | other | script | unavailable |
| `script.garden_mark_bok_choy_planted` | Garden Mark Bok Choy Planted | other | script | available |
| `script.garden_mark_cape_gooseberry_hardened` | Garden Mark Cape Gooseberry Hardened | other | script | available |
| `script.garden_mark_cape_gooseberry_planted` | Garden Mark Cape Gooseberry Planted | other | script | available |
| `script.garden_mark_honeynut_squash_hardened` | Garden Mark Honeynut Squash Hardened | other | script | available |
| `script.garden_mark_honeynut_squash_planted` | Garden Mark Honeynut Squash Planted | other | script | available |
| `script.garden_mark_marigolds_outside` | Garden Mark Marigolds Outside | other | script | unavailable |
| `script.garden_mark_peppers_hardened` | Garden Mark Peppers Hardened | other | script | available |
| `script.garden_mark_peppers_planted` | Garden Mark Peppers Planted | other | script | available |
| `script.garden_mark_seedlings_checked` | Garden Mark Seedlings Checked | other | script | unavailable |
| `script.garden_mark_seedlings_watered` | Garden Mark Seedlings Watered | other | script | unavailable |
| `script.garden_mark_tomatoes_hardened` | Garden Mark Tomatoes Hardened | other | script | available |
| `script.garden_mark_tomatoes_planted` | Garden Mark Tomatoes Planted | other | script | available |
| `script.garden_resolve_bok_choy_issue` | Garden Resolve Bok Choy Issue | other | script | available |
| `script.garden_resolve_cape_gooseberry_issue` | Garden Resolve Cape Gooseberry Issue | other | script | available |
| `script.garden_resolve_honeynut_squash_issue` | Garden Resolve Honeynut Squash Issue | other | script | available |
| `script.garden_resolve_peppers_issue` | Garden Resolve Peppers Issue | other | script | available |
| `script.garden_resolve_spinach_issue` | Garden Resolve Spinach Issue | other | script | available |
| `script.garden_resolve_tomatoes_issue` | Garden Resolve Tomatoes Issue | other | script | available |
| `script.garden_snooze_notifications` | Garden Snooze Notifications | other | script | available |
| `script.garden_start_basil_hardening` | Garden Start Basil Hardening | other | script | unavailable |
| `script.garden_start_marigolds_hardening` | Garden Start Marigolds Hardening | other | script | unavailable |
| `script.light_transition_toggle` | Light Transition Toggle | other | script | available |
| `script.lights_all_off_scene` | Lights All Off Scene | other | script | available |
| `script.lights_bedtime_scene` | Lights Bedtime Scene | other | script | available |
| `script.lights_evening_scene` | Lights Evening Scene | other | script | available |
| `script.lights_tv_scene` | Lights TV Scene | other | script | available |
| `script.notify_trevor_phone` | Notify Trevor Phone | other | script | available |
| `script.passport_clear_renewal_notification` | Passport Clear Renewal Notification | other | script | available |
| `script.passport_mark_renewal_applied` | Passport Mark Renewal Applied | other | script | available |
| `script.passport_send_renewal_reminder` | Passport Send Renewal Reminder | other | script | available |
| `script.passport_snooze_renewal` | Passport Snooze Renewal | other | script | available |
| `script.piano_clear_tuning_notification` | Piano Clear Tuning Notification | other | script | available |
| `script.piano_mark_tuning_done` | Piano Mark Tuning Done | other | script | available |
| `script.piano_send_tuning_reminder` | Piano Send Tuning Reminder | other | script | available |
| `script.piano_snooze_tuning` | Piano Mark Tuning Scheduled | other | script | available |
| `script.property_tax_clear_notification` | Property Tax Clear Notification | other | script | available |
| `script.property_tax_mark_paid` | Property Tax Mark Paid | other | script | available |
| `script.property_tax_send_reminder` | Property Tax Send Reminder | other | script | available |
| `script.robison_oil_mark_price_check_done` | Robison Oil Mark Price Check Done | other | script | available |
| `script.robison_oil_send_price_check_reminder` | Robison Oil Send Price Check Reminder | other | script | available |
| `script.robison_oil_send_tune_up_reminder` | Robison Oil Send Tune-Up Reminder | other | script | available |
| `script.spotify_bedtime_fade` | Spotify Bedtime Fade | other | script | available |
| `script.water_send_alert` | Water Send Alert | other | script | available |
| `script.wine_cave_clear_cabinet_cleaning_notification` | Wine Cave Clear Cabinet Cleaning Notification | other | script | available |
| `script.wine_cave_clear_charcoal_filter_notification` | Wine Cave Clear Charcoal Filter Notification | other | script | available |
| `script.wine_cave_mark_cabinet_cleaning_done` | Wine Cave Mark Cabinet Cleaning Done | other | script | available |
| `script.wine_cave_mark_charcoal_filter_replaced` | Wine Cave Mark Charcoal Filter Replaced | other | script | available |
| `script.wine_cave_mark_rating_plate_captured` | Wine Cave Mark Rating Plate Captured | other | script | available |
| `script.wine_cave_send_alert` | Wine Cave Send Alert | other | script | available |
| `script.wine_cave_send_cabinet_cleaning_reminder` | Wine Cave Send Cabinet Cleaning Reminder | other | script | available |
| `script.wine_cave_send_charcoal_filter_reminder` | Wine Cave Send Charcoal Filter Reminder | other | script | available |
| `script.wine_cave_send_rating_plate_reminder` | Wine Cave Send Rating Plate Reminder | other | script | available |
| `script.wine_cave_snooze_cabinet_cleaning` | Wine Cave Snooze Cabinet Cleaning | other | script | available |
| `script.wine_cave_snooze_charcoal_filter` | Wine Cave Snooze Charcoal Filter | other | script | available |
| `sensor.away_security_active_lights` | away_security_active_lights | telemetry | template | available |
| `sensor.away_security_entry_point_issues` | away_security_entry_point_issues | telemetry | template | available |
| `sensor.away_security_issue_summary` | away_security_issue_summary | telemetry | template | available |
| `sensor.away_security_unlocked_entry_locks` | away_security_unlocked_entry_locks | telemetry | template | available |
| `sensor.basement_radon_24h_stats` | Basement Radon 24h Stats | telemetry | statistics | available |
| `sensor.basement_radon_7d_stats` | Basement Radon 7d Stats | telemetry | statistics | available |
| `sensor.bonticou_llc_de_franchise_tax_due_date` | Bonticou LLC DE Franchise Tax Due Date | telemetry | template | available |
| `sensor.bonticou_llc_de_franchise_tax_status` | Bonticou LLC DE Franchise Tax Status | telemetry | template | available |
| `sensor.casey_driver_license_renewal_opens` | Casey Driver License Renewal Opens | telemetry | template | available |
| `sensor.casey_driver_license_renewal_status` | Casey Driver License Renewal Status | telemetry | template | available |
| `sensor.casey_passport_renewal_opens` | Casey Passport Renewal Opens | telemetry | template | available |
| `sensor.casey_passport_renewal_status` | Casey Passport Renewal Status | telemetry | template | available |
| `sensor.casey_presence_timeline` | Casey Presence Timeline | telemetry | template | unavailable |
| `sensor.device_inventory_pending_digest` | Device Inventory Pending Digest | telemetry | command_line | unknown |
| `sensor.device_inventory_status` | Device Inventory Status | telemetry | command_line | unknown |
| `sensor.downstairs_active_season` | Main Floor Active Season | telemetry | template | available |
| `sensor.downstairs_away_minutes` | Main Floor Away Minutes | telemetry | template | available |
| `sensor.downstairs_away_watch` | Main Floor Away Watch | telemetry | template | available |
| `sensor.downstairs_away_watch_reason` | Main Floor Away Watch Reason | telemetry | template | available |
| `sensor.downstairs_climate_insight` | Main Floor Climate Insight | telemetry | template | available |
| `sensor.downstairs_climate_status` | Main Floor Climate Status | telemetry | template | available |
| `sensor.downstairs_comfort_profile_reason` | Downstairs Comfort Profile Reason | telemetry | template | unavailable |
| `sensor.downstairs_comfort_profile_recommendation` | Downstairs Comfort Profile Recommendation | telemetry | template | unavailable |
| `sensor.downstairs_cooling_truth_temp` | Downstairs Cooling Truth Temp | telemetry | template | unavailable |
| `sensor.downstairs_ecobee_setpoint` | Dining Room Ecobee Setpoint | telemetry | template | unknown |
| `sensor.downstairs_heating_truth_temp` | Downstairs Heating Truth Temp | telemetry | template | unavailable |
| `sensor.downstairs_humidity_avg` | Main Floor Humidity Avg | telemetry | template | available |
| `sensor.downstairs_hvac_reason` | Downstairs HVAC Reason | telemetry | template | unavailable |
| `sensor.downstairs_hvac_recommendation` | Downstairs HVAC Recommendation | telemetry | template | unavailable |
| `sensor.downstairs_outdoor_humidity` | Main Floor Outdoor Humidity | telemetry | template | available |
| `sensor.downstairs_outdoor_temp` | Main Floor Outdoor Temp | telemetry | template | available |
| `sensor.downstairs_outdoor_wind_speed` | Main Floor Outdoor Wind Speed | telemetry | template | available |
| `sensor.downstairs_quiet_minutes` | Downstairs Quiet Minutes | telemetry | template | unavailable |
| `sensor.downstairs_source_policy` | Main Floor Source Policy | telemetry | template | available |
| `sensor.downstairs_target_temp` | Downstairs Target Temp | telemetry | template | unavailable |
| `sensor.downstairs_temp_avg` | Main Floor Temp Avg | telemetry | template | available |
| `sensor.downstairs_temp_spread` | Main Floor Temp Spread | telemetry | template | available |
| `sensor.downstairs_time_period` | Main Floor Time Period | telemetry | template | available |
| `sensor.driver_license_renewal_opens` | Driver License Renewal Opens | telemetry | template | available |
| `sensor.driver_license_renewal_status` | Driver License Renewal Status | telemetry | template | available |
| `sensor.dryer_vent_maintenance_status` | Dryer Vent Maintenance Status | telemetry | template | available |
| `sensor.dryer_vent_next_cleaning_due` | Dryer Vent Next Cleaning Due | telemetry | template | available |
| `sensor.environment_attic_status` | Environment Attic Status | telemetry | template | available |
| `sensor.environment_basement_status` | Environment Basement Status | telemetry | template | available |
| `sensor.environment_dining_room_status` | Environment Dining Room Status | telemetry | template | available |
| `sensor.environment_garage_status` | Environment Garage Status | telemetry | template | available |
| `sensor.environment_house_status` | Environment House Status | telemetry | template | available |
| `sensor.environment_kitchen_status` | Environment Kitchen Status | telemetry | template | available |
| `sensor.environment_main_floor_status` | Environment Main Floor Status | telemetry | template | available |
| `sensor.environment_office_status` | Environment Office Status | telemetry | template | available |
| `sensor.environment_primary_bedroom_status` | Environment Primary Bedroom Status | telemetry | template | available |
| `sensor.environment_second_floor_status` | Environment Second Floor Status | telemetry | template | available |
| `sensor.environment_source_map` | Environment Source Map | telemetry | template | available |
| `sensor.espresso_maintenance_status` | Espresso Maintenance Status | telemetry | template | available |
| `sensor.foyer_chandelier_schedule_brightness` | foyer_chandelier_schedule_brightness | telemetry | template | available |
| `sensor.front_stairs_schedule_brightness` | front_stairs_schedule_brightness | telemetry | template | available |
| `sensor.garbage_recycling_next_pickup` | Garbage Recycling Next Pickup | telemetry | template | available |
| `sensor.garbage_recycling_schedule` | Garbage Recycling Schedule | telemetry | template | available |
| `sensor.garbage_recycling_status` | Garbage Recycling Status | telemetry | template | available |
| `sensor.garden_basil_genovese_status` | Garden Basil Genovese Status | telemetry | template | unavailable |
| `sensor.garden_basil_lettuce_status` | Garden Basil Lettuce Status | telemetry | template | unavailable |
| `sensor.garden_bok_choy_status` | Garden Bok Choy Status | telemetry | template | available |
| `sensor.garden_cape_gooseberry_status` | Garden Cape Gooseberry Status | telemetry | template | available |
| `sensor.garden_check_status` | Garden Check Status | telemetry | template | unavailable |
| `sensor.garden_crop_summary` | Garden Crop Summary | telemetry | template | available |
| `sensor.garden_days_since_sowing` | Garden Days Since Sowing | telemetry | template | unavailable |
| `sensor.garden_honeynut_squash_status` | Garden Honeynut Squash Status | telemetry | template | available |
| `sensor.garden_indoor_seedlings_count` | Garden Indoor Seedlings Count | telemetry | template | unavailable |
| `sensor.garden_lowest_forecast_low_4_day` | Garden Lowest Forecast Low 4 Day | telemetry | template | unavailable |
| `sensor.garden_next_action` | Garden Next Action | telemetry | template | available |
| `sensor.garden_next_milestone` | Garden Next Milestone | telemetry | template | unavailable |
| `sensor.garden_next_stage_step` | Garden Next Stage Step | telemetry | template | unavailable |
| `sensor.garden_outdoor_planted_count` | Garden Outdoor Planted Count | telemetry | template | unavailable |
| `sensor.garden_outdoor_seedlings_count` | Garden Outdoor Seedlings Count | telemetry | template | unavailable |
| `sensor.garden_outdoor_snapshot` | Garden Outdoor Snapshot | telemetry | template | unavailable |
| `sensor.garden_peppers_status` | Garden Peppers Status | telemetry | template | available |
| `sensor.garden_petite_marigolds_status` | Garden Petite Marigolds Status | telemetry | template | unavailable |
| `sensor.garden_seedlings_total` | Garden Seedlings Total | telemetry | template | unavailable |
| `sensor.garden_spinach_status` | Garden Spinach Status | telemetry | template | available |
| `sensor.garden_today_focus` | Garden Today Focus | telemetry | template | unavailable |
| `sensor.garden_tomatoes_status` | Garden Tomatoes Status | telemetry | template | available |
| `sensor.garden_watering_status` | Garden Watering Status | telemetry | template | unavailable |
| `sensor.garden_weather_readiness` | Garden Weather Readiness | telemetry | template | unavailable |
| `sensor.garden_weather_window` | Garden Weather Window | telemetry | template | available |
| `sensor.garden_workflow_status` | Garden Workflow Status | telemetry | template | available |
| `sensor.house_low_battery_summary` | House Low Battery Summary | telemetry | template | available |
| `sensor.house_notice_history` | House Notice History | telemetry | template | available |
| `sensor.house_notice_timeline` | House Notice Timeline | telemetry | template | available |
| `sensor.metro_north_nwp_to_grand_central` | Metro-North NWP to Grand Central | telemetry | command_line | available |
| `sensor.passport_renewal_opens` | Passport Renewal Opens | telemetry | template | available |
| `sensor.passport_renewal_status` | Passport Renewal Status | telemetry | template | available |
| `sensor.piano_care_status` | Piano Care Status | telemetry | template | available |
| `sensor.piano_next_tuning_due` | Piano Next Tuning Due | telemetry | template | available |
| `sensor.radon_level_status` | Radon Level Status | telemetry | template | available |
| `sensor.school_tax_january_due_date` | School Tax January Due Date | telemetry | template | available |
| `sensor.school_tax_september_due_date` | School Tax September Due Date | telemetry | template | available |
| `sensor.sonos_favorites` | Sonos favorites | telemetry | sonos | disabled |
| `sensor.town_tax_due_date` | Town Tax Due Date | telemetry | template | available |
| `sensor.water_guard_alert_events` | Water Guard Alert Events | telemetry | template | available |
| `sensor.water_guard_flow_events` | Water Guard Flow Events | telemetry | template | available |
| `sensor.water_guard_leak_events` | Water Guard Leak Events | telemetry | template | unknown |
| `sensor.water_guard_pressure_events` | Water Guard Pressure Events | telemetry | template | available |
| `sensor.water_guard_usage_events` | Water Guard Usage Events | telemetry | template | unknown |
| `sensor.water_guard_valve_events` | Water Guard Valve Events | telemetry | template | available |
| `sensor.water_notification_status` | Water Notification Status | telemetry | template | available |
| `sensor.wine_cave_absolute_humidity` | wine_cave_absolute_humidity | telemetry | template | available |
| `sensor.wine_cave_absolute_humidity_24h_delta` | wine_cave_absolute_humidity_24h_delta | telemetry | template | available |
| `sensor.wine_cave_absolute_humidity_24h_stats` | Wine Cave Absolute Humidity 24h Stats | telemetry | statistics | available |
| `sensor.wine_cave_appliance_context` | Wine Cave Appliance Context | telemetry | template | available |
| `sensor.wine_cave_dew_point` | wine_cave_dew_point | telemetry | template | available |
| `sensor.wine_cave_dew_point_margin` | wine_cave_dew_point_margin | telemetry | template | available |
| `sensor.wine_cave_humidity_24h_delta_7d` | wine_cave_humidity_24h_delta_7d | telemetry | template | available |
| `sensor.wine_cave_maintenance_status` | Wine Cave Maintenance Status | telemetry | template | available |
| `sensor.wine_cave_next_charcoal_filter_due` | Wine Cave Next Charcoal Filter Due | telemetry | template | available |
| `sensor.wine_cave_next_cleaning_due` | Wine Cave Next Cleaning Due | telemetry | template | available |
| `sensor.wine_cave_rh_excursion` | wine_cave_rh_excursion | telemetry | template | available |
| `sensor.wine_cave_status` | wine_cave_status | telemetry | template | available |
| `sensor.wine_cave_temp_24h_delta_7d` | wine_cave_temp_24h_delta_7d | telemetry | template | available |
| `sensor.wine_cave_temp_excursion` | wine_cave_temp_excursion | telemetry | template | available |
| `sensor.wine_collection_snapshot` | Wine Collection Snapshot | telemetry | command_line | available |
| `sensor.wine_humidity_24h_mean` | wine_humidity_24h_mean | telemetry | template | available |
| `sensor.wine_humidity_24h_stats` | Wine Humidity 24h Stats | telemetry | statistics | available |
| `sensor.wine_humidity_30d_stats` | Wine Humidity 30d Stats | telemetry | statistics | available |
| `sensor.wine_humidity_7d_stats` | Wine Humidity 7d Stats | telemetry | statistics | available |
| `sensor.wine_temp_24h_mean` | wine_temp_24h_mean | telemetry | template | available |
| `sensor.wine_temperature_24h_stats` | Wine Temperature 24h Stats | telemetry | statistics | available |
| `sensor.wine_temperature_30d_stats` | Wine Temperature 30d Stats | telemetry | statistics | available |
| `sensor.wine_temperature_7d_stats` | Wine Temperature 7d Stats | telemetry | statistics | available |
| `stt.home_assistant_cloud` | Home Assistant Cloud | other | cloud | unknown |
| `todo.shopping_list` | Shopping List | other | shopping_list | available |
| `tts.home_assistant_cloud` | Home Assistant Cloud | other | cloud | available |

## UniFi Network Clients

| Client ID | Sources | Connection | Scope | Tracked Entities | Names |
| --- | --- | --- | --- | --- | --- |
| `network_01a7ffa721b6` | entity_registry |  |  | `device_tracker.hs103_2` | HS103 |
| `network_01b362394491` | entity_registry |  |  | `device_tracker.unifi_default_mac_4e93a0a4b48b` | Watch |
| `network_0349e3cbc41e` | entity_registry | wireless |  | `device_tracker.wynns_room` | wynns-room |
| `network_063dcd69dabd` | entity_registry |  |  | `device_tracker.sonoszp_13` | SonosZP |
| `network_0701248004f4` | entity_registry | wireless |  | `device_tracker.sonoszp_7` | SonosZP |
| `network_077f803201db` | entity_registry |  |  | `device_tracker.mechanical_room_leak_detection_espressif` | espressif |
| `network_0bb5a2bc3a59` | entity_registry |  |  | `device_tracker.apple_tv_family_room` | Apple TV (Family Room) |
| `network_1134d72f2862` | entity_registry |  |  | `device_tracker.u7_pro_mesh` | U7 Pro (Mesh) |
| `network_138dd978fd39` | entity_registry |  |  | `device_tracker.tesla` | Tesla |
| `network_162861e9f8a0` | entity_registry |  |  | `device_tracker.macbook_air_trevor` | Macbook Air (Trevor) |
| `network_1becf4615ae2` | entity_registry |  |  | `device_tracker.unifi_default_mac_b01ea2b181ff` |  |
| `network_1c390e0e7586` | entity_registry |  |  | `device_tracker.office_tv` | Apple TV (Office) |
| `network_24f2b3079862` | entity_registry |  |  | `device_tracker.unifi_default_mac_5395b13a8a3d` | iPhone |
| `network_2cad38dabb52` | entity_registry |  |  | `device_tracker.galaxy_tab_a_80_2019` | Google Tablet (Monitor) |
| `network_2dbcba4c5e25` | entity_registry |  |  | `device_tracker.unifi_default_mac_c8c81f1a78e1` |  |
| `network_2f2f22413762` | entity_registry |  |  | `device_tracker.unifi_default_mac_d9959f2a8987` | Watch |
| `network_31c6e9accc86` | entity_registry |  |  | `device_tracker.bonticou_gateway` | Bonticou Gateway |
| `network_381b44eab343` | entity_registry |  |  | `device_tracker.apple_tv_master` | Apple TV (Master) |
| `network_3aa8f46d4e01` | entity_registry | wireless |  | `device_tracker.ep25` | EP25 |
| `network_3ad07386bd1b` | entity_registry |  |  | `device_tracker.unifi_default_mac_0bbc683a0fb6` | SonosZP |
| `network_3dcc9e36ff54` | entity_registry |  |  | `device_tracker.sonoszp_2` | SonosZP |
| `network_40b057178bcb` | entity_registry | wireless |  | `device_tracker.uvc_g6_instant` | play-room |
| `network_44cdd51d8e44` | entity_registry |  |  | `device_tracker.unifi_default_mac_d112ffa56fc6` |  |
| `network_46029d337c7c` | entity_registry | wireless |  | `device_tracker.unifi_default_mac_4e99000aad0a` | EP25 |
| `network_46e900e653b2` | entity_registry |  |  | `device_tracker.sonoszp_9` | SonosZP |
| `network_4c4efc622bc9` | entity_registry |  |  | `device_tracker.unifi_default_mac_c0992a5e4e02` | MacBookAir |
| `network_4c75cbea40e0` | entity_registry |  |  | `device_tracker.unifi_default_mac_e75396edd3fe` | iPhone |
| `network_4dce3587a71b` | entity_registry |  |  | `device_tracker.dining_room` | Dining-Room |
| `network_4eb1785061b8` | entity_registry |  |  | `device_tracker.macbook_air_casey` | Macbook Air (Casey) |
| `network_50358c472a72` | entity_registry |  |  | `device_tracker.island_sink_leak_detection_espressif` | espressif |
| `network_50c937441dd5` | entity_registry |  |  | `device_tracker.hs103` | HS103 |
| `network_5200a5ded176` | entity_registry |  |  | `device_tracker.home_assistant` | Home Assistant |
| `network_52793b9da44a` | entity_registry |  |  | `device_tracker.laundry_sink_leak_detection_espressif` | espressif |
| `network_56124397cc01` | entity_registry | wireless |  | `device_tracker.flo_d4e95ef8775b` | Moen Flo |
| `network_5c77c2cb10f4` | entity_registry |  |  | `device_tracker.family_room_frame_tv` | Frame TV Pro |
| `network_5d120dfc3950` | entity_registry |  |  | `device_tracker.unifi_default_mac_de716b80d9a5` | Watch |
| `network_5d21a958dc6c` | entity_registry |  |  | `device_tracker.washing_machine_leak_detection_espressif` | espressif |
| `network_5db1c1849ddb` | entity_registry |  |  | `device_tracker.basement_ejector_leak_detection_espressif` | espressif |
| `network_5dca10f15aa3` | entity_registry |  |  | `device_tracker.lg_tv_master` | LG TV (Master) |
| `network_5f232cbd21d5` | entity_registry |  |  | `device_tracker.ecobee_office` | Ecobee (Office) |
| `network_60e35b633815` | entity_registry |  |  | `device_tracker.google_tablet` |  |
| `network_62b3b60215cc` | entity_registry |  |  | `device_tracker.unifi_default_mac_9878938b26f8` | Watch |
| `network_68a3d3ec0b4d` | entity_registry |  |  | `device_tracker.apple_tv_family_room_2` | Apple TV (Family Room) |
| `network_6b848b8b0f65` | entity_registry |  |  | `device_tracker.unifi_default_mac_d8484ff5d8dc` | iPad |
| `network_6cfb76146798` | entity_registry |  |  | `device_tracker.unifi_default_mac_29c96008c22e` |  |
| `network_6fbe104ea2f3` | entity_registry | wireless |  | `device_tracker.uvc_g6_instant_2` | front-yard |
| `network_6fbf9451dc87` | entity_registry |  |  | `device_tracker.security_camera_side_entry` | Security Camera (Side Entry) |
| `network_7392de75f9d5` | entity_registry |  |  | `device_tracker.unifi_default_mac_3c3d46c29f27` | iPhone |
| `network_73ed3aa6e508` | entity_registry |  |  | `device_tracker.sonoszp_15` | SonosZP |
| `network_75555cf80976` | entity_registry |  |  | `device_tracker.unifi_default_mac_e29de8de1f70` | Watch |
| `network_7589fd69656b` | entity_registry | wireless |  | `device_tracker.master_localdomain` | Ecobee (Master) |
| `network_7603f3886332` | entity_registry |  |  | `device_tracker.ecobee_master` | Ecobee (Master) |
| `network_78cf9ce5485a` | entity_registry |  |  | `device_tracker.iphone_5` | iPhone |
| `network_78ef6386293f` | entity_registry |  |  | `device_tracker.iphone_4` | iPhone |
| `network_7936b0ab270d` | entity_registry |  |  | `device_tracker.sonoszp_8` | SonosZP |
| `network_7a3ecf75712d` | entity_registry |  |  | `device_tracker.vizio_tv_family_room` | Vizio TV (Family Room) |
| `network_7c5c974675ea` | entity_registry |  |  | `device_tracker.sonoszp_10` | SonosZP |
| `network_7c8af86dfe2f` | entity_registry |  |  | `device_tracker.unifi_default_mac_2c894ada8b0b` |  |
| `network_7cbdb6e2ee7c` | entity_registry |  |  | `device_tracker.iphone_3` | iPhone |
| `network_7d82b3372ee2` | entity_registry | wireless |  | `device_tracker.kitchen_fridge_leak_detection_espressif` | espressif |
| `network_7e17b1e5ef19` | entity_registry |  |  | `device_tracker.jose_s_s23_fe` | Jose-s-S23-FE |
| `network_825c2d064323` | entity_registry | wireless |  | `device_tracker.ratgdo` | ratgdo |
| `network_835ec58c4a7c` | entity_registry |  |  | `device_tracker.unifi_default_mac_dd5079c60353` | iPhone |
| `network_853689a7af66` | entity_registry |  |  | `device_tracker.unifi_default_mac_b019bd33cc89` | iPhone |
| `network_88fdba8f6b4d` | entity_registry |  |  | `device_tracker.usw_flex_2_5g_5` | USW Flex 2.5G 5 |
| `network_89e7f0fa3fd2` | entity_registry |  |  | `device_tracker.db15_2` | DB15 |
| `network_8a7a9f3fb2a8` | entity_registry | wireless |  | `device_tracker.brw849e567c91bc` | Office Printer |
| `network_8b065ef7c1a0` | entity_registry |  |  | `device_tracker.lutron_06926f09` | Lutron Hub |
| `network_90db9d129b74` | entity_registry | wireless |  | `device_tracker.mud_room` | mud-room |
| `network_968a6d9f0306` | entity_registry | wireless |  | `device_tracker.sonoszp_6` | SonosZP |
| `network_9a89c65234c8` | entity_registry |  |  | `device_tracker.unifi_default_mac_a38f4e4b84a0` | iPhone |
| `network_9f52e1e5c4b5` | entity_registry |  |  | `device_tracker.trevor_s_iphone_16_pro` | Trevor's iPhone 16 Pro |
| `network_a3399227e493` | entity_registry |  |  | `device_tracker.dishwasher_leak_detection_espressif` | espressif |
| `network_a836f64560be` | entity_registry |  |  | `device_tracker.watch_2` | Watch |
| `network_a8b2458417f9` | entity_registry |  |  | `device_tracker.sonoszp_14` | SonosZP |
| `network_ab5c96352376` | entity_registry | wireless |  | `device_tracker.unifi_default_mac_754c3a1ea02a` | Aqara Hub M100 |
| `network_ac89c89ac6b9` | entity_registry |  |  | `device_tracker.watch` | Watch |
| `network_acba2652c74d` | entity_registry |  |  | `device_tracker.electrical_room_leak_detection_espressif` | espressif |
| `network_ad87894f3188` | entity_registry |  |  | `device_tracker.ipad` | iPad |
| `network_addb6fd64468` | entity_registry | wireless |  | `device_tracker.sonoszp` | SonosZP |
| `network_afc2c317cfe4` | entity_registry |  |  | `device_tracker.unifi_default_mac_7ed0c6182c02` | Watch |
| `network_b39ec9ba6c3e` | entity_registry |  |  | `device_tracker.unifi_default_mac_d129d9e3d6b1` |  |
| `network_b59508f39367` | entity_registry |  |  | `device_tracker.watch_3` | Watch |
| `network_b5f62e7218fc` | entity_registry |  |  | `device_tracker.unifi_default_mac_fd58284dab4a` |  |
| `network_b626f9bdd329` | entity_registry |  |  | `device_tracker.kitchen_sink_leak_detection_espressif` | espressif |
| `network_b65459b7ebe9` | entity_registry |  |  | `device_tracker.u7_pro_family_room` | U7 Pro (Family Room) |
| `network_bef51c8b3c76` | entity_registry |  |  | `device_tracker.unifi_default_mac_e52ad2d9d62a` | Watch |
| `network_c0277907fb7a` | entity_registry | wireless |  | `device_tracker.uvc_g6_instant_3` | uvc-g6-instant |
| `network_c1e39619d733` | entity_registry |  |  | `device_tracker.airthings_view` | airthings-view |
| `network_c1face513856` | entity_registry |  |  | `device_tracker.mac` | Mac |
| `network_c2dfbbd33698` | entity_registry |  |  | `device_tracker.security_camera_doorbell` | Security Camera (Doorbell) |
| `network_cbae0aa1353c` | entity_registry | wireless |  | `device_tracker.sonoszp_3` | SonosZP |
| `network_cc8a57ab7094` | entity_registry |  |  | `device_tracker.unifi_default_mac_e322eb2d1cf7` | SonosZP |
| `network_cc94aabe6ac8` | entity_registry |  |  | `device_tracker.u7_pro_outdoor` | U7 Pro Outdoor |
| `network_cd85e1b091a0` | entity_registry |  |  | `device_tracker.unifi_default_mac_f209cb9d07da` |  |
| `network_d24c85bd5443` | entity_registry |  |  | `device_tracker.iphone` | Steve's iPhone |
| `network_d6c8b6df39de` | entity_registry | wireless |  | `device_tracker.mechanical_room` | mechanical-room |
| `network_d8833f9e6da5` | entity_registry |  |  | `device_tracker.sonoszp_4` | SonosZP |
| `network_daaa0c318301` | entity_registry |  |  | `device_tracker.casey_s_iphone_16_pro` | Casey's iPhone 16 Pro |
| `network_db9f019d8988` | entity_registry |  |  | `device_tracker.security_camera_backyard` | Security Camera (Backyard) |
| `network_dfabd39e61a1` | entity_registry |  |  | `device_tracker.iphone_2` | iPhone |
| `network_e135643655fd` | entity_registry |  |  | `device_tracker.galaxy_s24_ultra` | Galaxy-S24-Ultra |
| `network_e1854c2ce2bc` | entity_registry |  |  | `device_tracker.unifi_default_mac_be3f4a9ec204` | iPhone |
| `network_e238f98d2452` | entity_registry |  |  | `device_tracker.sonos_beam_master` | Sonos Beam (Master) |
| `network_e26deec2f3f8` | entity_registry |  |  | `device_tracker.iphone_6` | iPhone |
| `network_ece0fee4cc8a` | entity_registry |  |  | `device_tracker.u7_pro_mud_room` | U7 Pro (Mud Room) |
| `network_f17d59d143c7` | entity_registry |  |  | `device_tracker.db15` | DB15 |
| `network_f24001ded53e` | entity_registry |  |  | `device_tracker.sonoszp_5` | SonosZP |
| `network_f2a454263d08` | entity_registry |  |  | `device_tracker.samsung` | Samsung |
| `network_f4b709ebd714` | entity_registry |  |  | `device_tracker.unifi_default_mac_92902c5c8aa5` |  |
| `network_f9edbe1f2387` | entity_registry |  |  | `device_tracker.sonoszp_12` | SonosZP |
| `network_fb15e20f5084` | entity_registry |  |  | `device_tracker.apple_tv_basement` | Apple TV (Basement) |
| `network_fb3eecf6e92b` | entity_registry | wireless |  | `device_tracker.unifi_default_mac_5042130907ce` | Casey's iPhone 17 Pro |
| `network_fce37b630e1f` | entity_registry |  |  | `device_tracker.sonoszp_11` | SonosZP |
