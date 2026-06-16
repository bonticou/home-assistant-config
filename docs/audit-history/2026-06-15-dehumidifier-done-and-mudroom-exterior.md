# Dehumidifier Done Action And Mudroom Exterior Schedule

Date: 2026-06-15

## Symptom

Trevor cleaned the dehumidifier air filter on Saturday, June 13, 2026 and
marked the reminder done, but the reminder continued to appear daily.

Trevor also noticed the mudroom exterior stairs light still turning on with
normal evening lighting. The intended policy is that vacation lighting may use
that exterior light, but normal Evening and door-light schedule automations
should not turn it on.

## Relevant Prior Context

- `2026-06-11-dehumidifier-air-filter-reminder.md` introduced the
  alternate-Friday dehumidifier air filter reminder.
- The reminder was designed to use durable helpers so a Done action clears only
  the current cycle.
- Prior lighting policy clarified that the mudroom interior lights are not part
  of generic Evening mode, while exterior utility lights remain subject to
  late-night and overnight shutoff paths.

## Evidence

Live state before the fix showed:

- `input_datetime.dehumidifier_air_filter_last_done_at` =
  `1970-01-01 00:00:00`;
- `input_datetime.dehumidifier_air_filter_snooze_until` =
  `1970-01-01 00:00:00`;
- `sensor.dehumidifier_air_filter_status` = `Due`;
- `sensor.dehumidifier_air_filter_status.current_cycle` = `2026-06-12`;
- `binary_sensor.dehumidifier_air_filter_due` = `on`.

That means the Done tap did not reach the durable completion helper. The likely
failure path was that `script.dehumidifier_air_filter_mark_done` logged to
`shell_command.log_house_action_stamp` before updating
`input_datetime.dehumidifier_air_filter_last_done_at`. If ledger logging failed
or rejected a cycle value, the script could abort before the reminder was
actually marked complete.

The mudroom exterior light was still referenced by
`script.door_lights_schedule_on`, which is called by the normal dusk/door-light
schedule and also by some exterior shutoff handoff paths when the door schedule
is still active.

## Findings

1. High confidence: dehumidifier completion state was never persisted, so the
   current June 12 cycle remained due.
2. High confidence: reminder Done scripts should stamp their durable HA helper
   before nonessential external logging.
3. High confidence: `door_lights_schedule_on` was a non-vacation turn-on path
   for `switch.exterior_mud_room_stairs`.
4. Medium confidence: the same stamp-before-ledger ordering should be applied
   to the paired garden fertilizer Done script because it uses the same reminder
   profile and ledger pattern.

## Changes Made

- Updated `script.dehumidifier_air_filter_mark_done` so it:
  - trims the current cycle id before ledger logging;
  - updates `input_datetime.dehumidifier_air_filter_last_done_at` and
    `input_datetime.dehumidifier_air_filter_snooze_until` before logging;
  - marks `shell_command.log_house_action_stamp` as `continue_on_error`.
- Applied the same defensive ordering to `script.garden_fertilizer_mark_done`.
- Removed `switch.exterior_mud_room_stairs` from
  `script.door_lights_schedule_on` and `script.door_lights_schedule_off`.
- Updated `sensor.away_security_active_lights` so the mudroom exterior light is
  no longer considered expected merely because the normal door-light schedule
  is active. Vacation activity windows still exempt their explicitly simulated
  lights.

## Live Remediation

After deploying the config, the live dehumidifier helper was stamped to
`2026-06-13 12:00:00` to reflect Saturday's cleaning, the stale dehumidifier
notification was cleared, and the mudroom exterior switch was turned off because
vacation mode was not active.

Live state after remediation showed:

- `input_datetime.dehumidifier_air_filter_last_done_at` =
  `2026-06-13 12:00:00`;
- `sensor.dehumidifier_air_filter_status` = `Scheduled`;
- `sensor.dehumidifier_air_filter_status.next_due_date` = `2026-06-26`;
- `binary_sensor.dehumidifier_air_filter_due` = `off`;
- `input_boolean.vacation_mode` = `off`;
- `switch.exterior_mud_room_stairs` = `off`;
- loaded `script.door_lights_schedule_on` no longer referenced
  `switch.exterior_mud_room_stairs`;
- loaded `script.dehumidifier_air_filter_mark_done` stamped the helper before
  ledger logging and used `continue_on_error`.

## Checks

- Ruby YAML parse passed for `configuration.yaml` and `scripts.yaml`.
- `git diff --check` passed.
- Live File Editor write/read-back succeeded for `configuration.yaml` and
  `scripts.yaml`.
- Home Assistant config check returned `valid` with no warnings or errors.
- `template.reload` and `script.reload` returned HTTP 200.

## Deployment Status

Deployed live on 2026-06-15 and verified through Home Assistant's remote route.

## Residual Risks

If mobile notification action delivery itself fails, Home Assistant will still
not see the Done tap. The dashboard Done action calls the same hardened script,
so future failures should be easier to distinguish: either the action never
arrived, or the helper stamp should persist regardless of ledger logging.

## 2026-06-16 Follow-Up

### Symptom

Trevor received another dehumidifier air filter notification on Tuesday,
June 16, 2026, after the live helper had been stamped to Saturday,
June 13, 2026.

### Evidence

After the repeat notification, live state initially showed the helper had reset
to the original sentinel values:

- `input_datetime.dehumidifier_air_filter_last_done_at` =
  `1970-01-01 00:00:00`;
- `input_datetime.dehumidifier_air_filter_snooze_until` =
  `1970-01-01 00:00:00`;
- `sensor.dehumidifier_air_filter_status` = `Due`;
- `binary_sensor.dehumidifier_air_filter_due` = `on`;
- `input_datetime.dehumidifier_air_filter_last_notified_at` =
  `2026-06-16 09:50:43`;
- `input_text.dehumidifier_air_filter_last_notified_cycle` = `2026-06-12`.

The YAML helpers for the paired garden fertilizer and dehumidifier air filter
reminders still had `initial:` values. For Home Assistant helpers, `initial:`
overrides restored state after restart/reload. That made these helpers look
durable in ordinary service calls but allowed restarts to put them back at the
seed values, re-opening a completed reminder cycle.

### Changes Made

- Removed `initial:` from the garden fertilizer reminder's completion,
  notification, snooze, and cycle helpers.
- Removed `initial:` from the dehumidifier air filter reminder's completion,
  notification, snooze, and cycle helpers.
- Re-stamped the live dehumidifier air filter completion and snooze helpers to
  `2026-06-13 12:00:00`.
- Cleared the stale dehumidifier air filter notification again.

### Checks

- Local Ruby YAML parse passed for `configuration.yaml`.
- Live File Editor write/read-back succeeded for `configuration.yaml`
  with SHA-256 `2ad726f4848edb992ec0c1312c4162191cf67f8bf42cb10aea6b16034b2e32d6`.
- Home Assistant config check returned `valid` with no warnings or errors.
- `input_datetime.reload`, `input_text.reload`, and `template.reload` all
  returned HTTP 200.
- Live read-back confirmed none of the garden fertilizer or dehumidifier air
  filter helper blocks still has `initial:`.
- Live dehumidifier air filter state after remediation:
  - `sensor.dehumidifier_air_filter_status` = `Scheduled`;
  - `sensor.dehumidifier_air_filter_status.next_due_date` = `2026-06-26`;
  - `binary_sensor.dehumidifier_air_filter_due` = `off`.

### Deployment Status

Deployed live on 2026-06-16 through the remote Home Assistant route.

### Residual Risks

This should survive future Home Assistant restarts because these helpers can
now restore their actual state. If a future reminder repeats inside a completed
cycle, the next diagnostic should focus on whether the mobile action arrived or
whether the recurrence template is computing the cycle boundary incorrectly.
