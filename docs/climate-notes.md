# Climate Notes

Durable notes for climate behavior, labels, and future tuning.

## Dining Room Thermostat Control Sensor

- The Dining Room thermostat is governed by the Kitchen/main-floor Ecobee sensor, serial `RQN8`.
- When the home page chip is summarizing the controlling thermostat signal, label it as `Kitchen`, even though the HA thermostat entity is `climate.dining_room`.
- The Dining Room Ecobee entities remain useful HVAC context and disagreement checks, but they should not make the controlling chip read as `Dining`.

## Future Comfort Logic

- Consider smarter downstairs climate logic that blends SensorPush readings and averaging rather than relying on one control sensor alone.
- Good candidates: `sensor.downstairs_temp_avg`, room-level SensorPush readings, humidity recovery trends, thermostat runtime, and open-window advantage.
