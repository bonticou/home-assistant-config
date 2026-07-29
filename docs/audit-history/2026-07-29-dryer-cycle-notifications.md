# Dryer Cycle Notifications

Date: 2026-07-29

## Symptom And Goal

The LG ThinQ dryer appeared in Home Assistant with completion, failure, status,
time, power, and energy entities, but only annual dryer-vent maintenance
notifications existed. The desired behavior is useful dryer-cycle awareness
without notifications that are not actionable while Trevor is away or while
the housekeeper is handling laundry.

## Relevant Prior Context

- Washer notifications already use durable timestamps and event keys, defer
  routine notices until Trevor has been home for five minutes, and time
  follow-ups from the first delivered push.
- The expected housekeeper window is Tuesdays from 7:45 AM through 3:00 PM.
- The housekeeper handles laundry during that window. Routine pushes should be
  quiet while she is there, but the washer should remain unresolved until a
  dryer start proves turnover or the window ends.
- Annual dryer-vent maintenance remains a separate reminder cycle.

## Evidence Collected

The live LG ThinQ dryer exposes:

- `event.dryer_notification` with `drying_is_complete` and `drying_failed`;
- `event.dryer_error` with `power_code_connection_error`,
  `temperature_sensor_error`, and `high_power_supply_error`;
- `sensor.dryer_current_status` with observed enum options including `running`,
  `detecting`, `cooling`, `wrinkle_care`, `error`, `end`, and `power_off`;
- remaining time, total time, remote start, power, operation, and energy
  entities.

The energy entities currently report zero and do not yet have enough history
for anomaly alerts.

## Changes Made

### Completion and follow-up

- Records each new ThinQ completion with a durable event key and completion
  timestamp.
- Sends an immediate completion push only when Trevor is home and the time is
  between 7:00 AM and 10:00 PM.
- Defers routine completion notices until Trevor has been home for five minutes
  and quiet hours have ended.
- Sends one unattended-load follow-up after 90 minutes.
- Allows one additional follow-up only after Trevor explicitly chooses
  `Remind me in 30`.
- Provides `Unloaded` and `Remind me in 30` actions.

### Housekeeper handling

- Keeps washer completions pending but silent during the housekeeper window.
- Uses a dryer `running` transition as positive evidence that the pending washer
  load was turned over.
- When the housekeeper window ends at 3:00 PM, immediately reevaluates a washer
  completion that still has no turnover evidence. It notifies only while Trevor
  is home; otherwise the existing arrival gate waits until he has been home for
  five minutes.
- When the housekeeper window begins, clears any pending washer push without
  stamping the washer load handled.
- Continues to treat dryer completions as handled during the window because
  there is no dryer-door telemetry to distinguish unloaded from still full.
- Suppresses and records generic `drying_failed` events during that window.
- Keeps the three hardware/power/temperature dryer errors eligible for
  notification.

### Dryer and washer handoff

- When the dryer enters `running`, clears any older dryer completion reminder.
- If the washer completed within the prior four hours and remains unhandled,
  the dryer start marks that washer load handled.
- During the housekeeper window, any dryer start can resolve the current pending
  washer completion even when it is older than four hours.

### Errors

- Deduplicates dryer failures by event entity, timestamp, and event type.
- Sends errors immediately while Trevor is home.
- Sends hardware/power/temperature errors immediately while away when the dryer
  still reports an active or error state.
- Defers other unresolved errors until Trevor has been home for five minutes.
- Uses a sticky high-priority notification with a `Got it` action.
- Does not add remote-power actions or automatic shutdown behavior.

### Inventory

- Refreshed the generated device inventory from the live registries, adding the
  LG dryer and its enabled ThinQ entities to the durable device map.

## Checks

- Ruby/Psych parsed `automations/30-maintenance-environment.yaml` and
  `scripts.yaml`, and parsed the full `configuration.yaml` syntax tree.
- Targeted structural checks confirmed:
  - all seven new dryer/laundry automations;
  - all seven dryer notification scripts;
  - the `drying_is_complete` event gate;
  - the 90-minute follow-up interval;
  - all four supported dryer failure event types;
  - the four-hour washer-to-dryer handoff;
  - washer and dryer housekeeper handling.
- `python3 tools/check_device_inventory_coverage.py` passed with all 91 active
  control references covered.
- `git diff --check` passed after removing one trailing space emitted by the
  inventory generator.
- A safety-scope search confirmed no dryer power or operation service action was
  added.
- Live File Editor write/read-back matched the generated SHA-256 payloads for:
  - `/homeassistant/configuration.yaml`;
  - `/homeassistant/automations.yaml`;
  - `/homeassistant/automations/30-maintenance-environment.yaml`;
  - `/homeassistant/scripts.yaml`.
- Home Assistant configuration validation returned `valid` with no errors or
  warnings.
- The deploy helper's short reload calls timed out. Individual follow-up reloads
  for `input_boolean`, `input_datetime`, `input_text`, `script`, and
  `automation` each completed successfully with the longer live-config parse
  time.
- All seven new dryer scripts were present and idle.
- All seven new dryer/laundry automations were present and enabled.
- The live automation config API confirmed:
  - `drying_is_complete` completion gating and quiet hours;
  - housekeeper handling for washer and dryer completions;
  - all three hardware error types and generic `drying_failed`;
  - the four-hour dryer-start washer handoff;
  - the housekeeper-start cleanup for both machines.
- The new durable helpers loaded successfully. Their initial timestamp baseline
  was the current date at midnight, with event-key helpers still `unknown`, so
  no pending completion or error existed.
- Follow-up targeted checks confirmed that:
  - a washer completion during the housekeeper window is cleared but not marked
    handled;
  - the 3:00 PM window-end transition triggers pending-washer reevaluation;
  - a dryer start remains the positive washer-turnover signal;
  - housekeeper-window start no longer stamps a pending washer handled.
- The follow-up automation-only deployment read back
  `automations/30-maintenance-environment.yaml` with SHA-256
  `23be9646cd4e3f4f7507d386cf332063adc07361be55cb5d726f0cefe09b2884`.
- Home Assistant again returned a valid configuration with no errors or
  warnings, and the direct `automation.reload` request completed with HTTP 200.
- The live automation config API confirmed the corrected rules, and the
  corresponding washer, dryer-handoff, and housekeeper-window automations were
  all enabled.

## Deployment Status

Deployed live on 2026-07-29 through the authenticated Nabu Casa File Editor
ingress route with byte-for-byte read-back, valid config check, successful
targeted reloads, and live entity/config verification.

## Residual Risks And Follow-Up

- There is no enabled dryer-door entity, so unload detection relies on the
  notification action, a new dryer cycle, or the housekeeper window.
- The four-hour washer-to-dryer handoff assumes the new dryer run is the recent
  washer load outside the housekeeper window. During the window, the known
  laundry-handling context allows any dryer start to resolve the pending washer.
- A real ThinQ completion and error payload should be observed after deployment
  before adding cycle-name copy or remote-power actions.
- Energy alerts should wait until non-zero history confirms those sensors are
  reliable.
- No synthetic completion or error push was generated during deployment; the
  first real dryer cycle will validate the device-specific event payload.
