# Master bedroom lantern integration

## Status

Trevor said the held former left-sconce dimmer is now a lantern in the master
bedroom and asked what is needed to integrate it with the home's rules. He approved
the proposed integration and specified: “Yes it should slowly dim up to 40%”.
The implementation is now deployed. The working left/right sconce pairing remains
separate and unchanged.

## Pre-implementation findings

The retained DVRF-6L device remains in Master Bedroom with one disabled entity,
`light.master_sconce_l_spare_20261108`. Its Related view reports no automation,
script or scene references. It has not yet been enabled or renamed as the lantern.

Fresh live reads of main configuration, automations, scripts, light groups and the
main dashboard matched the hashes from the sconce deployment. The existing
`switch.master_lantern` is a different identity used by the door-light overnight
schedule and excluded from the overnight sweep. Do not reuse or replace that ID
for this interior lantern. Its physical installation was not inspected.

## Approved plan (historical)

1. Rename the retained device/entity to Master Bedroom Lantern, use an available
   stable `light.master_bedroom_lantern` identity, and enable it. Keep it in Master
   Bedroom and preserve the physical device/history. Verify availability and
   capabilities after enabling; no assumption about the lantern bulb's dimming
   compatibility follows from the dimmer model alone.
2. Add a separate Lantern control in the bedroom's compact Lights dashboard grid,
   with brightness control if the actual load supports dimming. Do not put it in
   the Sconces group or either direction of the sconce synchronization automation.
3. Add it to the explicit Sleep / All Off shutdown list. The normal list uses a
   three-second fade; retain the special paired-sconce sequence unchanged.
4. Decide Bedtime behavior before editing that script. Currently Bedtime raises
   the two sconces from 30 to 40 percent while switching off other listed lights.
   Valid lantern choices are off, a chosen soft level, or unchanged. Do not guess
   a new bedroom lighting preference from the hardware repurposing alone.
5. Preserve the existing generic away-light detection and quick shutoff actions.
   They enumerate ordinary enabled light entities, so the lantern will join
   automatically rather than requiring duplicated entity lists.
6. Preserve the normal midnight reminder and 1 AM sweep, including snooze, guest,
   late-media and vacation guards. The sweep also discovers ordinary light
   entities automatically. No extra timer or special overnight exemption is
   recommended unless the lantern is intended as a nightlight.
7. Add it to Vacation Start's explicit cleanup/off list as a reasonable baseline.
   Do not add bedroom activity simulation or a vacation exemption without an
   explicit choice. If simulation is desired, coordinated start/end cleanup and
   away-notification exemptions must be updated together.
8. Leave Evening and TV behavior unchanged by default. Those scenes currently
   target common areas rather than this bedroom. The existing HomeKit House Modes
   commands will pick up script changes automatically; a separate lantern voice
   exposure is a separate choice, not required for the existing modes.

After the behavior decision, use the normal minimal deployment: refresh live
hashes, make scoped script/dashboard changes, update device inventory, validate
YAML and coverage, check HA configuration, reload only affected domains and read
back the registry/configuration/dashboard. Runtime verification should avoid
unnecessary physical actuation and distinguish observed state from user testing.

## Planning scope and evidence limits

No registry, scene, schedule, dashboard or device output was changed during the
initial planning pass. The disabled entity cannot provide fresh operating state. Supported
UI and five current live configuration files were inspected; arbitrary external
consumers were not audited. The separate door-light lantern is identified by its
configuration role, not a new physical-location confirmation.


## Deployed result

- Reused the same retained physical Diva dimmer; renamed device and entity
  **Master Bedroom Lantern**, entity `light.master_bedroom_lantern`, area Master
  Bedroom. Enabled/visible, no exposure or credential changes. HA showed the
  lantern available at 40 percent after enable, before any script replay. Its
  historical activity remains visible under the new identity.
- Bedtime sends one `light.turn_on` command to 40 percent with a five-second
  transition, immediately before the existing sconce sequence. There is no
  forced intermediate 30-percent jump for the lantern. This starts from its
  current output; if already brighter than 40 percent it settles down to 40.
- Sleep / All Off and Vacation Start include it in their existing three-second
  off transitions. Evening, TV and vacation simulation remain unchanged.
- Added a separate Lantern card beside Sconces in the Master Bedroom section,
  with the existing compact brightness control and three-second tap transition.
- Existing generic away-light and overnight templates automatically include the
  enabled ordinary light entity. Existing snoozes, guest/media and vacation
  guards remain intact. The sconce group/synchronization and separate door-light
  `switch.master_lantern` are unchanged.

## Deployment and validation

Deployment `3ed1889085bf46ca9301f75c4c9bb3e3` changed only `scripts.yaml` and
`dashboards/calm_mobile.yaml`. HA configuration validation passed, script reload
completed, and no Core restart was performed. Refreshed live hashes exactly
matched the prepared files. Main configuration, automations and light groups
retained their preceding hashes. Only three script definitions changed.

Thirteen focused offline tests passed: six new lantern tests and seven existing
sconce tests. Coverage includes the single five-second 40-percent command,
shutdown lists, scene isolation, separate dashboard card, actual generic-template
rendering with an enabled lantern and preserved door-light actions. Active
inventory coverage passed for 179 references. Independent read-only review found
no blocking issue. Updated inventory is targeted; baseline counts were not
represented as a new whole-home census.

The live device's Related view lists All Off, Bedtime and Vacation Start. The
Lights dashboard shows the separate Lantern at 40 percent and the Sconces tile
alongside it. No light command, scene replay or notification test was issued.
Configuration and current availability are verified; the visible five-second
fade, physical bulb response and actual scene shutoff remain normal-use tests.
