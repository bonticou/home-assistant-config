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

## Autonomous follow-through and passive monitoring

Trevor asked to continue autonomously and confirmed the appliance is only in
Kasa, not the Frigidaire app. Automatic switching remains incomplete. No claim
of proven electrical mismatch is made; manufacturer guidance and motor/inrush
compatibility remain unresolved. Both candidate Frigidaire model product pages
advertise native app control, which avoids repetitive mains interruption.

Deployed `dehumidifier_observation_only`: five-minute snapshots plus relay-state,
startup and reload observations. Only logbook.log is called, on actual relay-state
changes; no physical services or push notifications. Ninety-six retained traces
provide a bounded diagnostic window (approximately eight hours without extra
triggers), not a permanent monitoring service or a promise of autonomous review.
Existing Recorder configuration retains humidity, relay and watts for 30 days;
actual database row counts were not measured. Recorder inventory regenerated from
current local inventory, including the already-recorded lantern addition.

Live Airthings humidity is numeric and percent. HA 2026.9.2 Airthings source
polls every six minutes. The humidity entity exposes last_reported but no source
measurement timestamp. Last report cannot certify source-sample freshness and
last numeric change cannot identify a stale sensor. Do not gate future automatic
control on numeric-change age alone.

MCP plan/deployment 6487fd5cbe284c12ae6b8cbce6dd419d applied successfully,
configuration valid, automation reload completed, no Core restart. Live SHA
readback matched a2212786807650667b4c1d9f550011b2cd9e2cafff5797f202303b86f725e0d4.
Loaded automation is on. First natural reload trace finished November 8 at
8:36:47 PM Eastern: humidity 32 percent, plug on, 456.7 W,
control_enabled false. No test device operation or test push performed.

Provisional control design, not deployed: 50 percent on /45 percent off with
sustained valid readings, manufacturer-compatible minimum run/off intervals,
durable timestamps across restart, startup reconciliation, manual override,
source-freshness failure handling, and observed power response checks. Thresholds
are a working design, not an owner-confirmed choice. Power thresholds need baseline
fan/compressor observations; 450 W is a load observation, not proof of safe inrush.
Native appliance pairing and supported HA access remain the next dependencies.

Sources:
- https://www.frigidaire.com/en/p/home-comfort/dehumidifiers/FHDP5033Y1
- https://www.frigidaire.com/en/p/home-comfort/dehumidifiers/FHDD5033Y1
- https://www.tp-link.com/us/home-networking/smart-plug/ep25p4/
- https://github.com/home-assistant/core/blob/2026.9.2/homeassistant/components/airthings/coordinator.py
