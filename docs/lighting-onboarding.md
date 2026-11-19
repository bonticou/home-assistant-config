# Adding a household light

Trevor's November 18, 2026 instruction: adding a light to household lighting also
means adding it to **away detection and the notification's one-tap shutoff**.
Verify both paths in the same task; do not wait for a separate request.

## One inventory, two consumers

`helpers/household_lighting.yaml` owns the shared physical-light inventory exposed
as `sensor.household_lighting_inventory.targets`. The away-light sensor and
`script.away_lights_turn_off_verified` both consume this mapping. This includes
upstairs, foyer, front stairs, Wynn's lights and the actual lighting switches;
there are no bedtime, scheduled-light or vacation exclusions in this explicit
notification action. Other scenes and arrival rules retain their own policies.

Lutron `light.*` entities without group members are automatically included as
physical lighting loads. Other integrations and `switch.*` loads require explicit
classification in the verified mapping. Do not use a name substring to classify
arbitrary plugs: valves, appliances, camera/security controls, indicator LEDs and
equipment settings are not household lights. Do not enumerate every light domain
entity indiscriminately: UniFi access-point LEDs also use that domain.

## Required onboarding checks

1. Read the live entity and integration/device identity. Establish whether it is
   a real lighting endpoint, a group alias, a replacement or unrelated equipment.
   Check group membership and operate on actual members once each. An unavailable
   entity is not proof of retirement or duplication.
2. For a trusted Lutron load, verify that the rendered inventory actually contains
   it, then persist its verified ID/label in the mapping so later disappearance
   is reported as unknown rather than forgotten. For another real light or lighting switch, add its exact entity ID and a
   clear label to the shared mapping. Remove a replaced endpoint only when its
   retirement is evidenced; preserve separately installed hardware.
3. Update `docs/device-inventory.json` and its readable companion. Run
   `python3 tools/check_device_inventory_coverage.py` and the focused tests:
   `python3 -m unittest discover -s tests -p test_away_lighting_coverage.py -v`.
   Check both the new-light on-state detection and the shutoff selection in local
   simulation, including unavailable state, group exclusion and partial failures.
4. Follow the MCP deployment runbook: fresh live hashes, reconciliation, reviewed
   diff, backup/rollback and smallest reloads. Preserve arrival/Evening eligibility,
   notification presence/timing/recipient gates and unrelated live changes.
5. Read back deployed configuration and the rendered shared inventory/away sensor
   through supported access. Report separately: inventory coverage, detection,
   action wiring, tests, live reload/readback and physical behavior. Do not run a
   house blackout or send test notifications without explicit authority.
6. Completion must explicitly state **away detection verified** and **one-tap
   shutoff coverage verified**, with the evidence level. If a device is unavailable
   or state inspection is blocked, name that precise limitation; do not claim
   physical success from accepted service calls or a configuration write.

The explicit action retries currently-on members once after a three-second wait,
then waits another three seconds and returns remaining-on and unverified members.
Unknown/unavailable/missing entities remain unresolved, never silently off. It
does not set a blanket lighting hold or alter genuine first-arrival behavior;
normal schedules may subsequently turn a light on. New schedules are not part of
onboarding unless specifically requested.

Trevor's November 19 presentation decision: routine away/Casey alerts show
confirmed unsecured entry points and lights on, without unavailable/unverified
diagnostics or their device names. Keep that diagnostic evidence in inventory
attributes and action traces. An explicitly requested shutoff must still report
incomplete results truthfully; never turn unknown into confirmed off.
