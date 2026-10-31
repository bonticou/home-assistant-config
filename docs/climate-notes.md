# Climate Notes

Durable notes for climate behavior, labels, and future tuning.

## Dining Room Thermostat Control Sensor

- The Dining Room thermostat is governed by the Kitchen/main-floor Ecobee sensor, serial `RQN8`.
- When the home page chip is summarizing the controlling thermostat signal, label it as `Kitchen`, even though the HA thermostat entity is `climate.dining_room`.
- The Dining Room Ecobee entities remain useful HVAC context, but they should not make the controlling chip read as `Dining`.

## Future Comfort Logic

- Consider smarter downstairs climate logic that blends SensorPush readings and averaging rather than relying on one control sensor alone.
- Good candidates: `sensor.downstairs_temp_avg`, room-level SensorPush readings, humidity recovery trends, thermostat runtime, and open-window advantage.

## Main-floor sensor comparison retired — October 26, 2026

Trevor explicitly does not want the Kitchen and Dining Room SensorPush readings
compared for spread monitoring or notifications. Do not recreate Main Floor Temp
Spread, Main Floor Temp Spread High, or Environment — Main Floor Sensor Spread
Watch. Preserve both sensors, ordinary temperature/humidity readings, averages,
HVAC control and unrelated room alerts. The separate Dining Room SensorPush versus
Ecobee checks were outside that initial change; the October 31 correction below
also retires them.

Live configuration and loaded state already had the spread feature removed; this
change removes stale repository definitions that could otherwise restore it. See
[verification and recovery evidence](audit-history/2026-10-26-main-floor-spread-retirement.md).

## Correction: all main-floor disagreement alerts retired — October 31, 2026

Trevor's “I thought we killed this” screenshot identified the separate Dining Room
SensorPush–Ecobee comparison missed on October 26. Do not track or notify on either
temperature or humidity disagreement, including reintroducing equivalent sender
branches or comparison helpers. Ordinary temperature/humidity limits, sensor
availability, batteries, radon, physical readings, averages and HVAC remain intact.
See [the corrective deployment evidence](audit-history/2026-10-31-dining-disagreement-retirement.md).
