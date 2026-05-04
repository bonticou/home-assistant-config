# Upgrade Backlog

Future improvements to consider once the current system is calm and stable.

This is a living brainstorm and tracking list, not gospel. Add to it, remove from it, and reorder it as the house teaches us what actually matters. Only the best ideas should survive into real build work.

Grounding from `docs/device-inventory.md`: 114 devices, 962 entities, 469 telemetry entities, and 380 control entities. The house already has a lot of the organs built; the biggest unbuilt value is a calmer brain layer that turns existing telemetry into trust, timing, and summaries.

## Highest-Value Ideas

1. **House Health / Reliability Center**
   Use HA host, supervisor, update sensors, backup sensors, UniFi gateway/AP/switch entities, Fios WAN status, Protect storage, HACS updates, disk, CPU, and memory. Build one calm status: `All systems normal`, `Backup stale`, `Network issue`, `Protect storage high`, etc. This protects the whole system and is probably the best next reliability investment.

2. **Critical Device Staleness Watch**
   Separate from low battery. Alert when important things stop reporting: Flo shutoff, leak pucks, SensorPush rooms, Airthings radon, cameras, UniFi APs, Home Assistant host, gateway, and wine cave sensor. The missing layer is: `this guardrail is no longer trustworthy`.

3. **Perimeter / Camera Event Brain**
   UniFi Protect exposes person, vehicle, smoke alarm, CO alarm, glass break, siren, car horn, baby cry, motion, recording, storage, and Ring doorbell events. Tier events: emergency audio gets immediate push, person/vehicle becomes away/night-contextual, ordinary motion becomes digest only.

4. **Morning / Evening House Brief**
   Use `sensor.house_notice_timeline`, water, wine, weather, Metro-North, property tax/admin reminders, batteries, and environment status. A daily push like `All quiet. Train at 8:12. Basement humidity steady.` would make the system feel more useful without new hardware.

5. **HVAC Runtime + Comfort Advisor**
   Add runtime intelligence: heating/cooling duration, aux-vs-heat-pump policy, comfort lag by room, open-window timing, humidity recovery, and away/home mode sanity checks. Mostly buildable from `climate.dining_room`, SensorPush, weather, and presence.

6. **Water Guard 2.0: Dampness Before Leak**
   Use each leak puck's humidity and temperature trend to catch `something is getting damp here` before `water_detected` trips, plus stale/offline detection per leak location.

7. **Battery + Consumables Shopping Assistant**
   Map devices to battery/supply type, then auto-create gentle shopping tasks for leak puck batteries, Ring batteries, Cafiza, wine charcoal filters, HVAC filters, and similar consumables.

8. **Adaptive House Modes**
   Build prompt-first modes, not over-automation: `Away`, `Return`, `Goodnight`, `Quiet`, `Hosting`, `Movie`. Inputs could include scenes, presence, sun position, lights, lock, Sonos, Apple TV, cameras, and environment state.

9. **Wine Drink-This Assistant**
   Use the wine collection snapshot's ready/mature/hold rows and styles to suggest a Friday bottle or dashboard pick, with a quick link to the sheet.

## Presence Upgrade Candidate

- Consider adding Casey's Home Assistant Companion App GPS tracker to `person.casey`.
  - Keep the current UniFi tracker as a useful Wi-Fi presence signal.
  - Add the mobile-app GPS tracker for better real-world home/away truth.
  - Before enabling it, confirm Casey is comfortable with the app permissions: Location Always, precise location, and background refresh.
  - Leave the UniFi detection timeout alone for now unless the normal departure lag becomes a recurring problem.

## Suggested Order

1. House Health / Reliability Center
2. Critical Device Staleness Watch
3. Morning / Evening House Brief
