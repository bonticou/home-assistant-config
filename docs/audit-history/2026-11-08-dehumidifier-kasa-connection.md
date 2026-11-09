# Dehumidifier Kasa connection - November 8, 2026

Owner-identified EP25 hardware 2.6 is connected to Home Assistant as Dehumidifier.
Full MAC matched the owner screenshot. No relay command or humidity automation
was issued. Live readback: switch.dehumidifier on; sensor.dehumidifier_current_consumption
approximately 449.5-450.2 W, with approximately 3.73 A and 122.5 V also visible.
Initial energy readings: 8.393 kWh today, 77.267 kWh this month. These are plug
reports, not compressor-state or inrush certification. New history had no statistics.

The existing TP-Link discovery required authentication. Initial investigation
stopped; Trevor then supplied a one-time 1Password share. Ames-only credential
preflight passed. Shared password transferred by UI copy/paste without printing
or saving to project files. HA confirmed configuration success. Browser password
saving declined; shared tab closed and clipboard overwritten with a non-secret URL.
No new account grants, exposure changes, rename or area assignment performed.

Trevor confirms Kasa on/off works and prioritizes convenience. Compatibility
remains unknown, not a proven mismatch. Stored FHDD5033Y1 manual page 3 warns
against starting/stopping by unplugging or switching at the electrical box and
requires direct grounded connection; it does not name smart plugs. Page 11 gives
a three-minute compressor restart delay; page 15 restores settings after outages.
Stored specs give 115 V, 8.8 A, 470 W, but no compressor HP or inrush rating.
Physical model remains provisional against earlier FHDP5033Y1 identification.

Read-only preflight found Airthings humidity 32 percent but did not establish
measurement freshness. Existing basement humidity alerts use Mechanical Room
SensorPush, not this Airthings entity. Close initial monitoring was requested
but not activated. Thresholds, actual sample freshness, durable cycle guards,
load compatibility and operating-feedback verification remain follow-ups.

Validation: authenticated device and entity readback passed. Inventory contains
only the two exact verified IDs; other plug entities not fully enumerated. Local
inventory coverage and diff checks run. UI integration addition needed no YAML
reload/deployment. Unrelated work preserved.
