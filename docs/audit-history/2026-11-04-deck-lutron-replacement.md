# Deck Lutron replacement

Replaced the removed deck dimmer in HA while retaining its stable entity ID and
existing behavior. User authorized full replacement and discovery refresh.

Admin MCP health worked (Core 2026.9.2); authenticated desktop settings loaded.
Native MCP could not match Deck lights because they are unexposed. Reloaded only
the existing Lutron integration: 36 devices/43 entities became 37/44. Old Deck
Deck Lights then reported no longer provided by the integration; the newly
found Deck Deck Lights 1 was available/off. The other dimmer refreshed its
vendor name to Deck Deck Lights 2 but retained light.exterior_deck_lights.

Renamed the old entity to light.deck_deck_lights_retired_20261104, labeled it
retired and disabled it without deletion. Renamed the new
light.deck_deck_deck_lights_1 to light.deck_deck_lights, preserving the old display
name, Deck area, enabled and visible settings. Both had no entity labels shown.
The replacement device name was also set to Deck Deck Lights.

Live readbacks confirmed the replacement off under the stable ID and the second
dimmer available/off at its unchanged ID. Main configuration, scripts, automations,
Lights dashboard and light-group files retained exact pre-change hashes; they
contain no retired or temporary replacement references. No old-device-ID
references were present in those live files. Existing entity references therefore
follow the new physical dimmer, including Bedtime/All Off, vacation and alerts.
HA configuration check passed. No scene replay or light actuation was performed.
Device inventory received a targeted reconciliation; no broad registry census.

Recovery is through the same HA registry UI: rename the replacement back to its
discovered ID before restoring the old ID/name/enabled state to the retained
retired entity. Restoring the old hardware connection is a separate prerequisite.
No YAML deployment or deployment-backup ID applies; this was a recoverable
registry replacement. No credentials, exposure, grants or integration reconnect
were changed. UI-managed references by stable entity ID remain valid; arbitrary
external consumers using the former physical device identifier were not inspected.
