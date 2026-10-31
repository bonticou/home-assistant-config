# Dining Room disagreement alerts retired

The October 26 cleanup missed a separate Dining Room SensorPush-versus-Ecobee
comparison. Trevor's October 31 “I thought we killed this” screenshot identified
that active sender. Both temperature and humidity disagreement alerts are now
removed from live HA and the repository. Do not recreate equivalent comparisons.

## Exact source and prior activity

`automation.environment_room_actionable_alerts` (Environment — Room Actionable
Alerts), YAML ID `environment_room_actionable_alerts`, had two disagreement
triggers: `binary_sensor.environment_dining_room_ecobee_temp_disagreement` and
`binary_sensor.environment_dining_room_ecobee_humidity_disagreement`. Temperature
used a 3°F difference lasting 45 minutes; humidity used 10 points for 90 minutes.

Retained trace `579379e736c770d8b449437240c3f72d` started October 31 at
15:46:27.778 UTC, triggered by temperature disagreement. Its message exactly
matched the screenshot, including SensorPush 67.54°F / 39.2% and Ecobee
70.88°F / 45.0%. It finished at 15:46:28.053 UTC after calling
`script.environment_send_alert` with Dining Room / source_disagreement. The
wrapper constructs title “Dining Room readings disagree” and tag
`environment-dining-room-source_disagreement`. This was an active-rule run today,
not merely a surviving notification from the October 26 retirement. Device
delivery/display timing is not established by the automation trace.

## Applied change

Administrative MCP bridge deployment `3714471911e249578ca2c33dd752fcba` applied
the reviewed live-hash-guarded patch, with recoverable originals, validation ok,
automation reload completed and template reload completed. No Core restart.
Removed both dedicated comparison templates, their delta attributes, room/main-
floor disagreement status branches, both sender triggers and message/kind
branches, startup refresh references and matching clear-handler references.

Preserved the live monolithic automation layout, repository split layout and
unrelated drift. Shared scripts and dashboard were byte-identical before/after.
The generic formatter still understands the historical source_disagreement kind
for compatibility; there is no remaining live or repository automation caller
that produces it. No disagreement generator remains in the inspected live main
config, complete automation file, scripts or dashboard. Previous Kitchen–Dining
Room spread retirement remains intact.

## Verification

- Live config and automation readback exactly match reviewed after hashes:
  `be038d5de5ca0a6befe29146c5392db48ba88ad83363519d0cc8c0963ad90503` and
  `88cf03de28548b109b5843e3c9870486ed3ebd95cca61d81e26137089889dd6c`.
- Live health reports no recovery required. Both comparison entities are
  unavailable historical registry remnants after reload, not active trackers.
- Read-only Developer Tools: SensorPush 67.19°F / 38.25%; Ecobee 69.26°F / 45%;
  average 68.4°F; HVAC heat; room-alert automation on. Values are observation-time.
- Dining Room issue Steady; four ordinary high/low temperature/humidity alert
  entities present and off. Notification timeline contains no disagreement item.
- Semantic comparison preserved all other template entities and all non-template
  config. All automation IDs retained; only startup sync, actionable alerts and
  clear-handler internals changed. All 20 remaining actionable triggers preserved.
- Local YAML parsing, inventory coverage (178 controls), diff check and Recorder
  regeneration passed. No database supplied; no frequency/history claims.
- Post-reload shared automation trace at 18:17:07 UTC was the existing Primary
  Bedroom sensor-unavailable branch, not disagreement. Reload caused normal
  reevaluation; no physical routines or alerts were manually triggered for tests.

Raw live snapshots/traces remain outside Git. Inventory annotations retain
historical entities rather than deleting recorded history. Climate notes now
correct the earlier scope interpretation. The focused Git commit provides local
recovery; the admin deployment provides guarded live rollback. No broad
notification, access, credential, network or security settings changed.

No implementation blocker remains. An already-delivered phone card may remain in
iOS history; this task did not send Trevor a message or verify removal from his
phone. The source of future comparison notifications has been removed.
