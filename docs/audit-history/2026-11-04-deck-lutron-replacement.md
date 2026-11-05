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

## Follow-up reference and presentation verification

Observed clock 2026-11-05 00:18:39 UTC converts to November 4, 19:18:39 EST
(America/New_York); the audit date and retired suffix are correct.
The old device's Related panel now reports no automations, scripts or scenes.
The replacement device's Related panel lists both late-night exterior reminder
and clear automations, plus All Off, Bedtime, Late Night Exterior Off, Vacation
Activity Apply and Vacation Mode End. No scenes are listed. Thus the visible HA
relationships follow the replacement, with no remaining old-device target found.
The retired entity's Related view shows only integration context, no helper,
automation, script or dashboard relationship. Raw registry IDs were returned
privately to the originating task and are intentionally omitted here.

The current Lights page loads all existing sections without unavailable controls.
It does not have a dedicated Deck tile: the unchanged live dashboard has no direct
reference to this entity. Replacement details show the expected name, Deck area,
available/off state and dimmer control. No tile was added under replacement scope.
A complete raw audit of UI-managed Overview contents or every helper definition
was not performed; the supported old-device/entity Related views and live YAML
reference checks above are the verified coverage, not a whole-storage guarantee.

## Additional supported-source checks and inventory-check limits

Admin MCP additionally read live scenes.yaml, lights.yaml and dashboards/ha_safe.yaml:
none contained the old device identifier, temporary discovered entity ID or
retired entity ID. Earlier exact live checks cover configuration.yaml (including
YAML helpers/templates), scripts.yaml, monolithic automations.yaml and
calm_mobile.yaml. These checks do not traverse arbitrary storage or hidden includes.

Opened the user-created Overview at /lovelace/0 and its supported configuration
editor without saving. It reports “No strategy type found” and an editor validation
error. The editor's regex search for the old device ID and temporary/retired entity
identifiers did not select a match; rendered editor text contained none. Because
this editor is erroring and its accessibility text is virtualized, this is a
bounded UI inspection, not a certified complete stored-config export. No unrelated
Overview repair was attempted. Built-in generated dashboards were not exported.

Compared both entities' settings and voice-assistant panes: replacement retains
Deck device-area inheritance, prior name, enabled/visible state and no custom icon
or labels shown. Both voice panes show default-name alias only, Assist enabled,
Alexa/Google disabled; no exposure setting was changed. No additional entity-option
controls were offered in these settings panes. Raw integration-specific option
payloads, every UI-created helper/group definition, and external device-ID consumers
remain outside the verified coverage. Old-device Related and retired-entity Related
inspection found no residual dependency; no further migration was identified.

The “178 active control references” check is local regex membership against
inventory JSON entities/orphans for 12 control domains across a hardcoded file
list: configuration.yaml, automations.yaml, the first four automation chunks,
scripts.yaml, scenes.yaml and dashboards/calm_mobile.yaml. It does not traverse
includes, query HA, validate device IDs or availability, cover all files (notably
lights.yaml, the generator chunk and ha_safe), or inspect stored dashboards/helpers.
It is not evidence of complete replacement coverage. All above limitations remain
explicit; no raw .storage access, grants, actuation or additional live edits occurred.
