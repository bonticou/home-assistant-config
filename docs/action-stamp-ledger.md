# Action Stamp Ledger

Recurring reminder completion is double-entry:

- Home Assistant helpers are the operational state used by reminders.
- `.house-manager-outbox/action-stamps.jsonl` is the durable local journal.

Canonical reminder scripts must append an action stamp before updating helper
state or clearing notifications. UI buttons, push actions, and Codex chat stamps
should all call the same canonical script for the action.

## Event Shape

Each JSONL event uses:

- `notice_id`: stable reminder id, such as `bonticou-de-franchise-tax`
- `cycle_id`: handled cycle, such as `2026` or `water-backflush-2026-05-09`
- `action`: completion action, such as `paid`, `water_backflush_done`, or `cafiza_clean_done`
- `completed_at`: local completion timestamp
- `source`: `home_assistant_notification_action`, `home_assistant_dashboard_action`, or `codex_chat`
- `note`: optional short context
- `sync_state`: starts as `pending`

`sensor.house_action_stamp_ledger` exposes the pending count and latest event so
the home can see when action stamps still need to be synced into house-manager.

## House-Manager Sync

Home Assistant does not assume it can write to Trevor's Desktop
`house-manager` checkout. A later manual or automated sync should consume the
pending JSONL events, update the relevant house-manager bundle, and then mark or
archive the synced events without editing HA helper history.
