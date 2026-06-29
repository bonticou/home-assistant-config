# Irrigation Hunter Flow Review

Date: 2026-06-29

## Symptom And User Impact

The irrigation system now has a Hunter flow system specifically for irrigation.
This changes the June 9 topology conclusion: Flo flow and gallons still should
not be treated as irrigation evidence, but direct Hunter irrigation flow can now
become irrigation evidence once the live Hunter entities and units are confirmed.

The current irrigation dashboard is calm but thin. It mainly shows Hydrawise
schedule/controller state plus shared-well pressure. That was the right shape
when there was no direct irrigation flow meter, but it leaves too much of the
new Hunter signal unused and keeps some primitive status tiles that can be
collapsed into better summaries.

## Relevant Prior Context

- 2026-06-09 irrigation topology cleanup established Hydrawise/controller state
  as the irrigation source of truth and Flo pressure as shared-well context.
- That cleanup removed or rewrote irrigation-only Flo flow/gallon assumptions
  because irrigation was outside the Moen Flo measured branch.
- The regular Water tab and household Flo alerts remain separate and still use
  Moen Flo flow, pressure, gallons, valve state, and leak sensors.
- Notification work should follow `docs/notification-reliability-patterns.md`
  and `docs/notification-detail-surfaces.md`: important notices need durable
  cycle/timestamp guards and designed detail surfaces, not raw more-info popups.

## Evidence Collected

- `configuration.yaml` still defines Hydrawise-derived irrigation active zone,
  up-next, schedule summary, dashboard status, weather skip context, shared-well
  pressure proxy, and pressure recovery helpers.
- `automations/00-water-irrigation.yaml` currently sends irrigation start/end
  notices, pressure collapse/recovery alerts, zone-ran-too-long, valve mismatch,
  multiple-zone, scheduled-not-started, and controller-offline alerts.
- `scripts.yaml` centralizes water and irrigation push notifications through
  `script.water_send_alert`, including alert labels, titles, severity,
  notification tags, event recording, and active alert latches.
- `dashboards/calm_mobile.yaml` has a Water tab summary card that links to the
  Irrigation subpage. The Irrigation subpage shows a hero status card, four
  primitive tiles, a schedule popup listing all 27 Hydrawise zones, and a status
  popup with raw live context entities.
- Repository search found no Hunter-named config or entity references yet.
  Exact Hunter entity IDs, units, and update cadence still need a current live
  entity discovery pass before implementation.
- Existing device and recorder inventory files still contain stale
  pre-cleanup irrigation Flo-derived entities, so a Hunter implementation should
  include an inventory refresh.

## What Hunter Flow Makes Possible

1. Direct irrigation flow truth:
   - current irrigation flow rate;
   - session gallons or volume;
   - zone gallons;
   - flow present/absent independent of Hydrawise's intended schedule.

2. Zone health checks:
   - zone active but no or very low flow after a short settle window;
   - zone active with unusually high flow, suggesting a break or stuck-open
     branch;
   - zone active with unusually low flow, suggesting clog, closed valve, or
     supply issue;
   - observed flow outside learned zone baseline after enough samples.

3. Off-schedule flow checks:
   - irrigation flow while Hydrawise reports all zones quiet;
   - flow continuing after a zone/session stop grace period;
   - flow before HA sees Hydrawise state, which can catch manual controller
     runs or state lag.

4. Flow and well correlation:
   - high irrigation flow plus low shared-well pressure;
   - slow recovery after high-volume runs;
   - season/day summaries that separate irrigation usage from household Moen
     Flo usage.

5. Better history and details:
   - per-session summary with zones, runtime, gallons, peak flow, min pressure,
     and alerts;
   - per-zone baselines and confidence;
   - compact charts for flow and pressure during the active/last session.

## Ranked Findings

1. Hunter Flow should become the direct irrigation measurement layer.
   Confidence: high. Hydrawise says what should be running; Hunter Flow can say
   whether irrigation water actually moved.

2. Do not revive old Flo-derived irrigation assumptions.
   Confidence: high. Any flow/gallon irrigation logic should reference the
   Hunter meter, not Moen Flo, while Flo pressure can remain shared-well context.

3. Add a learning period before noisy per-zone anomaly pushes.
   Confidence: high. The system has 27 zones, so zone baseline alerts should
   start as history/dashboard-only until each zone has enough good runs.

4. The current irrigation dashboard should be simplified and made flow-first.
   Confidence: high. The page duplicates status, exposes raw entity surfaces,
   and lists all zones by default. Hunter Flow allows a more useful first
   viewport: status, active zone, flow now, session gallons, next run, and well
   pressure.

5. Current routine start/finish push notifications are likely lower value once
   flow detail exists.
   Confidence: medium. Start/finish events are useful history, but default push
   should probably be reserved for exceptions, unless Trevor wants routine
   watering receipts.

## Recommended Build

Phase 1 - Discovery and normalization:

- Run a current live entity discovery for Hunter/Hydrawise flow entities.
- Add normalized template sensors such as irrigation flow rate, flow meter
  availability, current session gallons, and active zone observed flow.
- Confirm units and update cadence before thresholds.
- Refresh device and recorder inventory after entity naming is stable.

Phase 2 - Flow-aware history:

- Repurpose or replace the old irrigation fingerprint path as explicit
  irrigation zone flow baselines.
- Record session and zone events from Hunter Flow only.
- Store per-zone observed flow/gallons with sample count and confidence.
- Treat the first several clean runs per zone as learning/history, not push
  alerts, except for extreme no-flow or very-high-flow conditions.

Phase 3 - Notifications:

- Add new `script.water_send_alert` kinds for Hunter flow:
  - irrigation no flow;
  - irrigation high flow or break suspected;
  - irrigation low flow or clog suspected;
  - irrigation flow after stop;
  - irrigation unscheduled flow;
  - Hunter flow meter unavailable/stale during watering.
- Use durable session or zone-cycle IDs so each condition sends once per
  meaningful event.
- Send critical pushes for no-flow, break/high-flow, unscheduled continuing
  flow, and high-flow plus low-pressure combinations.
- Keep baseline deviations as warnings once confidence is high; before then,
  record them in history and dashboard only.
- Add designed details for active Hunter flow alerts with observed flow,
  expected range, zone, schedule state, pressure, and a short "what to check"
  section.

Phase 4 - Dashboard:

- Make the Irrigation hero show the real state in one glance:
  `Quiet`, `Running`, `Needs attention`, `Learning flow`, or `Recovering`.
- Add primary flow-first metrics:
  - Flow now;
  - Session gallons;
  - Active zone;
  - Next run;
  - Shared well pressure.
- Add one compact session chart: Hunter flow plus shared-well pressure over the
  active/last session.
- Replace the all-27-zone default list with:
  - active zone;
  - next few zones;
  - zones with warnings;
  - an optional "all zones" detail drawer.

## Primitive Dashboard Items To Kill Or Demote

- Kill the duplicate main "Status" tile on the irrigation subpage once the hero
  carries state. Replace that slot with Hunter flow now.
- Demote the "Controller" tile to a small status badge or only show it when
  offline; the hero already surfaces controller-offline state.
- Demote the standalone "Shared well" tile. Keep pressure, but show it as
  context beside Hunter flow rather than the primary irrigation measurement.
- Replace the "Schedule - tap for Hydrawise zones" card and all-zone popup with
  a calmer next-run/active/problem-zone view.
- Replace the raw "Irrigation Status" entities popup with a designed status
  sheet or inline panel.
- Remove or repurpose unused focus-zone/fingerprint primitives if Hunter Flow
  baselines take over. Do not keep stale "fingerprint" terminology if the user
  surface can say "zone flow baseline."

## Checks Run

- Reviewed audit history index and the 2026-06-09 irrigation/Flo topology
  correction.
- Reviewed notification reliability and notification detail surface docs.
- Searched repository-owned YAML, docs, dashboard, scripts, and inventory for
  irrigation, Hydrawise, Hunter, flow, and Flo references.
- Inspected the current irrigation dashboard, irrigation templates, irrigation
  automations, and `script.water_send_alert`.

No live current Home Assistant entity discovery was performed during this pass.
No config was changed.

## Deployment Status

Audit only. No Home Assistant deployment or reload required.

## Residual Risks And Follow-Ups

- Confirm the Hunter Flow entity IDs, unit of measurement, precision, and update
  cadence before writing thresholds.
- Confirm whether Hunter exposes total volume directly. If not, build a
  recorder/utility-meter-backed integration path from flow rate.
- Validate alert thresholds with real runs by zone; do not assume each zone has
  similar expected flow.
- Refresh `docs/device-inventory.*` and `docs/recorder-inventory.*` after the
  implementation because existing inventories still show stale pre-cleanup
  irrigation Flo-derived entities.
