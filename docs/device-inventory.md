# Device Inventory

A human-readable map of the Home Assistant device model. The full audit dump is in [device-inventory-detail.md](device-inventory-detail.md); this page is the quick view.

## At A Glance

- Snapshot: `2026-05-21T02:43:09.473014+00:00`
- Scale: 176 devices, 1909 entities, 119 network clients
- Lighting: 28 light entities, 27 Lutron Caséta entities

| Thing | Count |
| --- | --- |
| Devices | 176 |
| Entities | 1909 |
| Control entities | 643 |
| Telemetry entities | 855 |
| Network clients | 119 |
| Areas | 32 |

## Area Index

| Area | Devices | Controls | Lights | Telemetry | Network |
| --- | --- | --- | --- | --- | --- |
| Attic | 1 | 0 | 0 | 8 | 0 |
| Back Stairs | 1 | 1 | 1 | 0 | 0 |
| Back Yard | 1 | 4 | 1 | 6 | 0 |
| Basement | 3 | 0 | 0 | 16 | 1 |
| Deck | 1 | 1 | 1 | 0 | 0 |
| Dining Room | 2 | 6 | 0 | 12 | 0 |
| Electrical Room | 5 | 12 | 0 | 99 | 2 |
| Exterior | 2 | 2 | 1 | 0 | 0 |
| Family Room | 8 | 31 | 3 | 26 | 3 |
| Family Room TV | 1 | 2 | 0 | 0 | 0 |
| Front Door | 1 | 3 | 0 | 7 | 0 |
| Front Foyer | 3 | 3 | 2 | 0 | 0 |
| Front Yard | 1 | 32 | 0 | 27 | 1 |
| Garage | 3 | 4 | 0 | 12 | 0 |
| Great Room Speakers | 1 | 8 | 0 | 1 | 1 |
| Kitchen | 4 | 0 | 0 | 19 | 4 |
| Kitchen Speakers | 1 | 8 | 0 | 1 | 1 |
| Master | 5 | 12 | 1 | 12 | 0 |
| Master Bathroom | 1 | 0 | 0 | 0 | 0 |
| Master Bedroom | 2 | 2 | 2 | 0 | 0 |
| Mechanical Room | 4 | 33 | 0 | 47 | 3 |
| Mudroom | 8 | 43 | 2 | 54 | 3 |
| Office | 2 | 7 | 0 | 4 | 0 |
| Stairs | 1 | 1 | 1 | 0 | 0 |
| Unassigned | 102 | 190 | 9 | 280 | 48 |
| Unnamed Room | 6 | 63 | 0 | 6 | 6 |
| Upstairs Hallway | 1 | 1 | 1 | 0 | 0 |
| Vestibule | 1 | 1 | 1 | 0 | 0 |
| Wynn's Room | 4 | 11 | 2 | 5 | 1 |

## Lighting Controls

| Area | Light | Entity | Integration | Original name |
| --- | --- | --- | --- | --- |
| Unassigned | Family Room | `light.family_room` | group |  |
| Unassigned | Interior (Test) | `light.interior_test` | group |  |
| Unassigned | LED | `light.u7_pro_family_room_led` | unifi |  |
| Unassigned | LED | `light.u7_pro_mesh_led` | unifi |  |
| Unassigned | LED | `light.u7_pro_mud_room_led` | unifi |  |
| Unassigned | Light | `light.ratgdo32disco_c26634_light` | esphome |  |
| Unassigned | Master Bedroom Sconces | `light.master_bedroom_sconces` | group |  |
| Unassigned | Mudroom | `light.mudroom` | group |  |
| Unassigned | Wynn's Room | `light.wynn_s_room` | group |  |
| Back Stairs | Back Stairs Back Stairs | `light.back_stairs_back_stairs` | lutron_caseta |  |
| Back Yard | Light | `light.back_patio_light` | ring |  |
| Deck | Deck Deck Lights | `light.deck_deck_lights` | lutron_caseta |  |
| Exterior | Exterior Yard Lights | `light.exterior_yard_lights` | lutron_caseta |  |
| Family Room | Family Room Main Lights 1 | `light.family_room_main_lights_1` | lutron_caseta |  |
| Family Room | Family Room Main Lights 2 | `light.family_room_main_lights_2` | lutron_caseta |  |
| Family Room | Family Room Main Lights 3 | `light.family_room_main_lights_3` | lutron_caseta |  |
| Front Foyer | Front Foyer Ceiling Lights | `light.front_foyer_ceiling_lights` | lutron_caseta |  |
| Front Foyer | Front Foyer Chandelier | `light.front_foyer_chandelier` | lutron_caseta |  |
| Master | Casey's closet | `light.master_casey_s_closet` | lutron_caseta | Master Casey's Closet |
| Master Bedroom | Master Bedroom Sconce L | `light.master_bedroom_sconce_l` | lutron_caseta |  |
| Master Bedroom | Master Bedroom Sconce R | `light.master_bedroom_sconce_r` | lutron_caseta |  |
| Mudroom | Mudroom Main Lights | `light.mudroom_main_lights` | lutron_caseta |  |
| Mudroom | Mudroom Nook Lights | `light.mudroom_nook_lights` | lutron_caseta |  |
| Stairs | Stairs Front Stairs | `light.stairs_front_stairs` | lutron_caseta |  |
| Upstairs Hallway | Upstairs Hallway Main Lights | `light.upstairs_hallway_main_lights` | lutron_caseta |  |
| Vestibule | Vestibule Main Lights | `light.vestibule_main_lights` | lutron_caseta |  |
| Wynn's Room | Wynn's Room Ceiling Lights | `light.wynn_s_room_ceiling_lights` | lutron_caseta |  |
| Wynn's Room | Wynn's Room Chandelier | `light.wynn_s_room_chandelier` | lutron_caseta |  |

## Control Devices By Area

### Back Stairs

| Device | Integration | Main controls | Original name |
| --- | --- | --- | --- |
| Back Stairs Back Stairs | lutron_caseta | Back Stairs Back Stairs (`light.back_stairs_back_stairs`) |  |

### Back Yard

| Device | Integration | Main controls | Original name |
| --- | --- | --- | --- |
| Back Patio | ring | Light (`light.back_patio_light`); Volume (`number.back_patio_volume`); Siren (`siren.back_patio_siren`); Motion detection (`switch.back_patio_motion_detection`) |  |

### Deck

| Device | Integration | Main controls | Original name |
| --- | --- | --- | --- |
| Deck Deck Lights | lutron_caseta | Deck Deck Lights (`light.deck_deck_lights`) |  |

### Dining Room

| Device | Integration | Main controls | Original name |
| --- | --- | --- | --- |
| Dining Room Thermostat | homekit_controller | Dining Room Clear Hold (`button.dining_room_clear_hold`); Dining Room Identify (`button.dining_room_identify`); Dining Room (`climate.dining_room`); Dining Room Current Mode (`select.dining_room_current_mode`); Dining Room Temperature Display Units (`select.dining_room_temperature_display_units`); +1 more | Dining Room |

### Electrical Room

| Device | Integration | Main controls | Original name |
| --- | --- | --- | --- |
| Bonticou Gateway | unifi, unifiprotect | Port 4 Power Cycle (`button.bonticou_gateway_port_4_power_cycle`); Restart (`button.bonticou_gateway_restart`); Analytics enabled (`switch.bonticou_gateway_analytics_enabled`); Insights enabled (`switch.bonticou_gateway_insights_enabled`); Port 1 (`switch.bonticou_gateway_port_1`); +7 more |  |

### Exterior

| Device | Integration | Main controls | Original name |
| --- | --- | --- | --- |
| Exterior Mud Room Stairs | lutron_caseta | Exterior Mud Room Stairs (`switch.exterior_mud_room_stairs`) |  |
| Exterior Yard Lights | lutron_caseta | Exterior Yard Lights (`light.exterior_yard_lights`) |  |

### Family Room

| Device | Integration | Main controls | Original name |
| --- | --- | --- | --- |
| Family Room | sonos, unifi | `media_player.family_room`; Audio delay (`number.family_room_audio_delay`); Balance (`number.family_room_balance`); Bass (`number.family_room_bass`); Music surround level (`number.family_room_music_surround_level`); +13 more |  |
| Family Room Frame TV | samsungtv, unifi | `media_player.family_room_frame_tv`; `remote.family_room_frame_tv` |  |
| Family Room Main Lights 1 | lutron_caseta | Family Room Main Lights 1 (`light.family_room_main_lights_1`) |  |
| Family Room Main Lights 2 | lutron_caseta | Family Room Main Lights 2 (`light.family_room_main_lights_2`) |  |
| Family Room Main Lights 3 | lutron_caseta | Family Room Main Lights 3 (`light.family_room_main_lights_3`) |  |
| Smart Bridge 2 | lutron_caseta | Unassigned Smart Away (`switch.unassigned_smart_away`) |  |
| Uplight | tplink, unifi | Restart (`button.uplight_restart`); Power protection (`number.uplight_power_protection`); Turn off in (`number.uplight_turn_off_in`); `switch.uplight`; Auto-off enabled (`switch.uplight_auto_off_enabled`); +2 more |  |

### Family Room TV

| Device | Integration | Main controls | Original name |
| --- | --- | --- | --- |
| Family Room TV | apple_tv | `media_player.family_room_tv_2`; `remote.family_room_tv` |  |

### Front Door

| Device | Integration | Main controls | Original name |
| --- | --- | --- | --- |
| Front Door | ring | Volume (`number.front_door_volume`); In-home chime (`switch.front_door_in_home_chime`); Motion detection (`switch.front_door_motion_detection`) |  |

### Front Foyer

| Device | Integration | Main controls | Original name |
| --- | --- | --- | --- |
| Front Foyer Ceiling Lights | lutron_caseta | Front Foyer Ceiling Lights (`light.front_foyer_ceiling_lights`) |  |
| Front Foyer Chandelier | lutron_caseta | Front Foyer Chandelier (`light.front_foyer_chandelier`) |  |
| Front Foyer Sconces | lutron_caseta | Front Foyer Sconces (`switch.front_foyer_sconces`) |  |

### Front Yard

| Device | Integration | Main controls | Original name |
| --- | --- | --- | --- |
| Wynn's Room | unifi, unifiprotect | Restart (`button.wynn_s_room_restart`); Unadopt device (`button.wynn_s_room_unadopt_device`); Speaker (`media_player.wynn_s_room_speaker`); Infrared custom lux trigger (`number.wynn_s_room_infrared_custom_lux_trigger`); Microphone level (`number.wynn_s_room_microphone_level`); +27 more |  |

### Garage

| Device | Integration | Main controls | Original name |
| --- | --- | --- | --- |
| Garage Entry Lock | matter | Identify (`button.garage_entry_lock_identify`); `lock.garage_entry_lock`; Operating mode (`select.garage_entry_lock_operating_mode`) | Aqara Smart Lock U100 |
| Garage Garage Lights | lutron_caseta | Garage Garage Lights (`switch.garage_garage_lights`) |  |

### Great Room Speakers

| Device | Integration | Main controls | Original name |
| --- | --- | --- | --- |
| Great Room Sonos | sonos, unifi | `media_player.great_room_speakers`; Balance (`number.great_room_speakers_balance`); Bass (`number.great_room_speakers_bass`); Treble (`number.great_room_speakers_treble`); Crossfade (`switch.great_room_speakers_crossfade`); +3 more |  |

### Kitchen Speakers

| Device | Integration | Main controls | Original name |
| --- | --- | --- | --- |
| Kitchen Sonos | sonos, unifi | `media_player.kitchen_speakers`; Balance (`number.kitchen_speakers_balance`); Bass (`number.kitchen_speakers_bass`); Treble (`number.kitchen_speakers_treble`); Crossfade (`switch.kitchen_speakers_crossfade`); +3 more |  |

### Master

| Device | Integration | Main controls | Original name |
| --- | --- | --- | --- |
| Casey's closet | lutron_caseta | Casey's closet (`light.master_casey_s_closet`) | Master Casey's Closet |
| Master Lantern | lutron_caseta | Master Lantern (`switch.master_lantern`) |  |
| Master Thermostat | homekit_controller | Master Clear Hold (`button.master_clear_hold_2`); Master Identify (`button.master_identify_2`); Master Thermostat (`climate.master_2`); Master Current Mode (`select.master_current_mode_2`); Master Temperature Display Units (`select.master_temperature_display_units_2`); +1 more | Master |
| Master Wall Remote | lutron_caseta | Unassigned Accent Lights Remote 1 Lower (`button.unassigned_accent_lights_remote_1_lower`); Unassigned Accent Lights Remote 1 Off (`button.unassigned_accent_lights_remote_1_off`); Unassigned Accent Lights Remote 1 On (`button.unassigned_accent_lights_remote_1_on`); Unassigned Accent Lights Remote 1 Raise (`button.unassigned_accent_lights_remote_1_raise`) | Unassigned Accent Lights Remote 1 |

### Master Bedroom

| Device | Integration | Main controls | Original name |
| --- | --- | --- | --- |
| Master Bedroom Sconce L | lutron_caseta | Master Bedroom Sconce L (`light.master_bedroom_sconce_l`) |  |
| Master Bedroom Sconce R | lutron_caseta | Master Bedroom Sconce R (`light.master_bedroom_sconce_r`) |  |

### Mechanical Room

| Device | Integration | Main controls | Original name |
| --- | --- | --- | --- |
| Flo shutoff | flo, unifi | Shutoff valve (`switch.flo_shutoff_shutoff_valve`) |  |
| Mechanical room | unifi, unifiprotect | Restart (`button.mechanical_room_restart`); Unadopt device (`button.mechanical_room_unadopt_device`); Speaker (`media_player.mechanical_room_speaker`); Infrared custom lux trigger (`number.mechanical_room_infrared_custom_lux_trigger`); Microphone level (`number.mechanical_room_microphone_level`); +27 more |  |

### Mudroom

| Device | Integration | Main controls | Original name |
| --- | --- | --- | --- |
| Back Stairs | ring | Volume (`number.back_stairs_volume`); Siren (`siren.back_stairs_siren`); Motion detection (`switch.back_stairs_motion_detection`) |  |
| Mud room | unifi, unifiprotect | Restart (`button.mud_room_restart`); Unadopt device (`button.mud_room_unadopt_device`); Speaker (`media_player.mud_room_speaker`); Infrared custom lux trigger (`number.mud_room_infrared_custom_lux_trigger`); Microphone level (`number.mud_room_microphone_level`); +27 more |  |
| Mudroom Door | ring | Volume (`number.mudroom_door_volume`); In-home chime (`switch.mudroom_door_in_home_chime`); Motion detection (`switch.mudroom_door_motion_detection`) |  |
| Mudroom Door Lock | matter | Identify (`button.mudroom_door_lock_identify`); `lock.mudroom_door_lock`; Operating mode (`select.mudroom_door_lock_operating_mode`) | Aqara Smart Lock U100 |
| Mudroom Main Lights | lutron_caseta | Mudroom Main Lights (`light.mudroom_main_lights`) |  |
| Mudroom Nook Lights | lutron_caseta | Mudroom Nook Lights (`light.mudroom_nook_lights`) |  |

### Office

| Device | Integration | Main controls | Original name |
| --- | --- | --- | --- |
| Office TV | apple_tv | `media_player.office_tv`; `remote.office_tv` |  |
| Office Thermostat | homekit_controller | Office Clear Hold (`button.office_clear_hold`); Office Identify (`button.office_identify`); Office (`climate.office`); Office Current Mode (`select.office_current_mode`); Office Temperature Display Units (`select.office_temperature_display_units`) | Office |

### Stairs

| Device | Integration | Main controls | Original name |
| --- | --- | --- | --- |
| Stairs Front Stairs | lutron_caseta | Stairs Front Stairs (`light.stairs_front_stairs`) |  |

### Unassigned

| Device | Integration | Main controls | Original name |
| --- | --- | --- | --- |
| Aqara Hub M100 | matter | Identify (`button.aqara_hub_m100_identify`) |  |
| Aqara Smart Lock U100 | matter | Identify (`button.aqara_smart_lock_u100_identify`); `lock.aqara_smart_lock_u100`; Operating mode (`select.aqara_smart_lock_u100_operating_mode`) |  |
| Basement TV | cast | `media_player.basement_tv` |  |
| Bonticou | unifi | Regenerate Password (`button.bonticou_regenerate_password`); `switch.bonticou` |  |
| Bonticou Guest | unifi | Regenerate Password (`button.bonticou_guest_regenerate_password`); `switch.bonticou_guest` |  |
| Family Room TV | cast | `media_player.ls03f3973` |  |
| Family Room TV | cast | `media_player.family_room_tv` |  |
| File editor | hassio | `switch.file_editor` |  |
| Fios-VHTx3 | unifi | Regenerate Password (`button.fios_vhtx3_regenerate_password`); `switch.fios_vhtx3` |  |
| Front Yard | unifi, unifiprotect | Restart (`button.g6_instant_restart_2`); Unadopt device (`button.g6_instant_unadopt_device_2`); Speaker (`media_player.back_yard_speaker`); Infrared custom lux trigger (`number.back_yard_infrared_custom_lux_trigger`); Microphone level (`number.back_yard_microphone_level`); +28 more |  |
| Garage | unifi, unifiprotect | Restart (`button.g6_instant_restart_3`); Unadopt device (`button.g6_instant_unadopt_device_3`); Speaker (`media_player.garage_speaker`); Wide dynamic range (`number.g6_instant_wide_dynamic_range_3`); Infrared custom lux trigger (`number.garage_infrared_custom_lux_trigger`); +28 more |  |
| HACS | hacs | Pre-release (`switch.hacs_pre_release`) |  |
| Kitchen | homekit_controller | Kitchen Identify (`button.rqn8_identify`) |  |
| Matter Server | hassio | `switch.matter_server` |  |
| Mini Media Player | hacs | Pre-release (`switch.mini_media_player_pre_release`) |  |
| Mushroom | hacs | Pre-release (`switch.mushroom_pre_release`) |  |
| Play Room | unifi, unifiprotect | Restart (`button.g6_instant_restart`); Unadopt device (`button.g6_instant_unadopt_device`); Speaker (`media_player.play_room_speaker`); Wide dynamic range (`number.g6_instant_wide_dynamic_range`); Infrared custom lux trigger (`number.play_room_infrared_custom_lux_trigger`); +28 more |  |
| Sonos Card | hacs | Pre-release (`switch.sonos_card_pre_release`) |  |
| Spotify | spotify | `media_player.spotify` | Spotify Trevor Kiv |
| Terminal & SSH | hassio | `switch.terminal_ssh` |  |
| U7 Pro (Family Room) | unifi | Restart (`button.u7_pro_family_room_restart`); LED (`light.u7_pro_family_room_led`) |  |
| U7 Pro (Mesh) | unifi | Restart (`button.u7_pro_mesh_restart`); LED (`light.u7_pro_mesh_led`) |  |
| U7 Pro (Mud Room) | unifi | Restart (`button.u7_pro_mud_room_restart`); LED (`light.u7_pro_mud_room_led`) |  |
| U7 Pro Outdoor | unifi | Restart (`button.u7_pro_outdoor_restart`) |  |
| USW Flex 2.5G 5 | unifi | Restart (`button.usw_flex_2_5g_5_restart`); Port 1 (`switch.usw_flex_2_5g_5_port_1`); Port 2 (`switch.usw_flex_2_5g_5_port_2`); Port 3 (`switch.usw_flex_2_5g_5_port_3`); Port 4 (`switch.usw_flex_2_5g_5_port_4`); +1 more |  |
| Unnamed Room | sonos, unifi | `media_player.unnamed_room_4`; Balance (`number.unnamed_room_balance_9`); Bass (`number.unnamed_room_bass_9`); Treble (`number.unnamed_room_treble_9`); Crossfade (`switch.unnamed_room_crossfade_9`); +3 more |  |
| Unnamed Room | sonos, unifi | `media_player.unnamed_room_3`; Balance (`number.unnamed_room_balance_8`); Bass (`number.unnamed_room_bass_8`); Treble (`number.unnamed_room_treble_8`); Crossfade (`switch.unnamed_room_crossfade_8`); +3 more |  |
| Unnamed Room | sonos, unifi | `media_player.unnamed_room_2`; Audio delay (`number.unnamed_room_audio_delay_2`); Balance (`number.unnamed_room_balance_7`); Bass (`number.unnamed_room_bass_7`); Music surround level (`number.unnamed_room_music_surround_level_2`); +11 more |  |
| apexcharts-card | hacs | Pre-release (`switch.apexcharts_card_pre_release`) |  |
| browser_mod | hacs | Pre-release (`switch.browser_mod_pre_release`) |  |
| button-card | hacs | Pre-release (`switch.button_card_pre_release`) |  |
| card-mod | hacs | Pre-release (`switch.card_mod_pre_release`) |  |
| mini-graph-card | hacs | Pre-release (`switch.mini_graph_card_pre_release`) |  |
| ratgdo32disco c26634 | esphome, unifi | Query openings (`button.ratgdo32disco_c26634_query_openings`); Query status (`button.ratgdo32disco_c26634_query_status`); Restart (`button.ratgdo32disco_c26634_restart`); Safe mode boot (`button.ratgdo32disco_c26634_safe_mode_boot`); Sync (`button.ratgdo32disco_c26634_sync`); +13 more |  |
| visionOS & iOS 26 Liquid Glass Theme | hacs | Pre-release (`switch.visionos_ios_26_liquid_glass_theme_pre_release`) |  |

### Unnamed Room

| Device | Integration | Main controls | Original name |
| --- | --- | --- | --- |
| Master Sonos | sonos, unifi | `media_player.unnamed_room`; Sub gain (`number.master_sonos_sub_gain`); Audio delay (`number.unnamed_room_audio_delay`); Balance (`number.unnamed_room_balance`); Bass (`number.unnamed_room_bass`); +12 more |  |
| Office | sonos, unifi | `media_player.unnamed_room_6`; Audio delay (`number.office_audio_delay`); Music surround level (`number.office_music_surround_level`); Sub gain (`number.office_sub_gain`); Surround level (`number.office_surround_level`); +13 more |  |
| Unnamed Room | sonos, unifi | Balance (`number.unnamed_room_balance_3`); Bass (`number.unnamed_room_bass_3`); Treble (`number.unnamed_room_treble_3`); Crossfade (`switch.unnamed_room_crossfade_3`); Loudness (`switch.unnamed_room_loudness_3`); +2 more |  |
| Unnamed Room | sonos, unifi | Balance (`number.unnamed_room_balance_5`); Bass (`number.unnamed_room_bass_5`); Treble (`number.unnamed_room_treble_5`); Crossfade (`switch.unnamed_room_crossfade_5`); Loudness (`switch.unnamed_room_loudness_5`); +2 more |  |
| Unnamed Room | sonos, unifi | Balance (`number.unnamed_room_balance_4`); Bass (`number.unnamed_room_bass_4`); Treble (`number.unnamed_room_treble_4`); Crossfade (`switch.unnamed_room_crossfade_4`); Loudness (`switch.unnamed_room_loudness_4`); +2 more |  |
| Unnamed Room | sonos, unifi | Balance (`number.unnamed_room_balance_2`); Bass (`number.unnamed_room_bass_2`); Treble (`number.unnamed_room_treble_2`); Crossfade (`switch.unnamed_room_crossfade_2`); Loudness (`switch.unnamed_room_loudness_2`); +2 more |  |

### Upstairs Hallway

| Device | Integration | Main controls | Original name |
| --- | --- | --- | --- |
| Upstairs Hallway Main Lights | lutron_caseta | Upstairs Hallway Main Lights (`light.upstairs_hallway_main_lights`) |  |

### Vestibule

| Device | Integration | Main controls | Original name |
| --- | --- | --- | --- |
| Vestibule Main Lights | lutron_caseta | Vestibule Main Lights (`light.vestibule_main_lights`) |  |

### Wynn's Room

| Device | Integration | Main controls | Original name |
| --- | --- | --- | --- |
| Wynn Ecobee Sensor | homekit_controller | Wynn Room Identify (`button.wynn_room_identify`) | Wynn Room |
| Wynn Sonos | sonos, unifi | `media_player.wynn_s_room`; Balance (`number.wynn_s_room_balance`); Bass (`number.wynn_s_room_bass`); Treble (`number.wynn_s_room_treble`); Crossfade (`switch.wynn_s_room_crossfade`); +3 more |  |
| Wynn's Room Ceiling Lights | lutron_caseta | Wynn's Room Ceiling Lights (`light.wynn_s_room_ceiling_lights`) |  |
| Wynn's Room Chandelier | lutron_caseta | Wynn's Room Chandelier (`light.wynn_s_room_chandelier`) |  |

## Files

| File | Use |
| --- | --- |
| [device-inventory-detail.md](device-inventory-detail.md) | Full per-device audit view |
| [device-inventory.json](device-inventory.json) | Structured inventory for scripts and checks |
