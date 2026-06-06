# SSD Data-Disk Migration And Casey Closet Miss

## Symptom And Impact

After the Home Assistant data disk was moved to the USB-attached SanDisk SSD,
Trevor walked into Casey's closet and the closet light did not turn on. Around
the same period, the Storage page reported roughly 60 GB used, up from roughly
25 GB before the migration.

The user impact was twofold: the closet motion automation could not be trusted
for a real walk-in, and the new storage reading looked like an immediate
post-migration storage blow-up.

## Relevant Prior Context

- `2026-06-04-home-assistant-availability-ui-and-casey-closet.md` recorded a
  previous local/remote availability investigation and the original Casey closet
  motion entity repair.
- `2026-06-05-casey-closet-missed-motion.md` recorded a prior missed closet
  entry and raised the UniFi Protect motion sensitivity from 70 to 90.
- The current automation is `automation.lights_casey_s_closet_auto_off`.
- The current motion entity is `binary_sensor.casey_s_closet_motion`.
- The current light entity is `light.master_casey_s_closet`.

## Evidence Collected

- The user initiated the data disk move from the Home Assistant Storage UI after
  the UI showed `SanDisk Extreme 55AE`, size 931.48 GB, as an available target.
- The device was recorded in the inventory as `Home Assistant USB SSD`; the
  serial number was intentionally omitted from repository files.
- During the migration/recovery period, Home Assistant Core repeatedly moved
  between apparently reachable and unreachable states:
  - local TCP/HTTP probes to port 8123 alternated between success, timeout,
    connection refusal, and reset;
  - websocket probes alternated between `auth_required` success and TCP failure;
  - the Safari dashboard shell sometimes remained visible while frontend API or
    websocket calls timed out or failed;
  - the frontend later explicitly reported `hass.connected: false` with no
    active websocket while the stale dashboard shell was still visible.
- When Core was live again, a fresh websocket read showed:
  - `automation.lights_casey_s_closet_auto_off`: `on`;
  - `light.master_casey_s_closet`: `off` before manual intervention;
  - `binary_sensor.casey_s_closet_motion`: `off`;
  - `switch.casey_s_closet_motion_detection`: `on`;
  - `number.casey_s_closet_motion_sensitivity`: `90`;
  - `sensor.casey_s_closet_battery`: `93`;
  - the automation's `last_triggered` was still from earlier in the day, not the
    reported walk-in.
- The full Casey closet entity scan showed no alternate reliable occupancy
  entity. The available UniFi Protect entities included motion, motion
  detection, motion sensitivity, battery, tamper, status light, paired camera,
  and several disabled or unavailable environmental/contact sensors.
- The Storage page later rendered:
  - `61.2 GB of 916.8 GB used`;
  - `System`: 43.5 GB;
  - `Home Assistant`: 13.9 GB;
  - `Backups`: 3.9 GB;
  - `App data`: 0 GB;
  - `Free space`: 855.6 GB.

## Ranked Findings

1. High confidence: the failed closet walk-in was not caused by the automation
   receiving motion and ignoring it. Core was unstable during the test window,
   and when Core recovered the motion entity still had not reported an `on`
   event.
2. High confidence: a visible Home Assistant dashboard shell was not reliable
   proof that Core was healthy. Browser state and direct probes showed stale or
   partial frontend availability while backend API and websocket calls failed.
3. Medium-high confidence: the post-migration 60 GB storage reading is mostly
   the new data disk's System bucket, not sudden user-data growth. Home
   Assistant plus Backups accounted for about 17.8 GB.
4. Medium confidence: the System bucket includes HAOS-managed system/container
   data and filesystem allocation/overhead on the newly prepared external data
   disk. This should be monitored, but it is not itself evidence of a runaway
   Recorder or backup problem.
5. Medium confidence: Casey's closet UniFi Protect motion sensitivity at 90 was
   still not enough for the reported walk-in, or the sensor event was missed
   during Core instability.

## Changes Made

- Recorded the SanDisk USB SSD in:
  - `docs/device-inventory.json`;
  - `docs/device-inventory.md`;
  - `docs/device-inventory-detail.md`.
- Raised `number.casey_s_closet_motion_sensitivity` live from 90 to 100.
- Turned `light.master_casey_s_closet` on live at 50% after the failed walk-in
  so the room was usable.
- No YAML automation changes were made during this incident.

## Checks And Live Validation

- `python3 tools/check_device_inventory_coverage.py` passed after inventory
  update.
- `python3 tools/ha_remote_health_probe.py --url http://<local-ha>:8123`
  alternated between `ok` and `tcp_error`, confirming instability rather than a
  pure Lovelace rendering problem.
- Fresh websocket state readback confirmed the sensitivity value reached `100`
  and the closet light accepted the manual turn-on command.
- The Storage page was scraped from the local Safari session to capture the
  category breakdown above.

## Deployment Status

- Inventory documentation was committed in a separate commit.
- The live motion sensitivity and light service calls were applied directly
  through the running Home Assistant frontend.
- No Home Assistant YAML deployment or automation reload was performed.

## Residual Risks And Next Follow-Ups

- Home Assistant Core was still flapping after the SSD migration. Until Core
  remains stable, motion automations should be treated as degraded.
- If Core continues to cycle, perform a full host reboot with the SSD left
  connected, then inspect Supervisor/Core logs from a stable session.
- After stability returns, retest Casey's closet with sensitivity 100 and watch
  `binary_sensor.casey_s_closet_motion` live during the walk-in.
- If the sensor still does not report motion reliably at sensitivity 100, add a
  faster physical trigger source, such as a closet door/contact sensor, rather
  than relying only on the UniFi Protect motion event.
- Monitor the Storage page after the system stabilizes. The important values are
  the Home Assistant and Backups buckets, not just the total used number.
