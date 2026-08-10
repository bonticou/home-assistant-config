# Washer Notification Copy Cleanup

Date: 2026-08-10
Status: Deployed and verified

## Symptom

Trevor reported that a washer notification used bot-like internal wording such
as a numbered load/cycle value instead of normal household language.

## Evidence

- Live `sensor.washer_cycles` reported a numeric counter.
- Live `input_text.washer_last_cycle_name` held `19`.
- `script.washer_send_completion_notification` used that helper in the
  deferred push body, so a deferred completion could say something like "The 19
  cycle finished..."
- No dashboard or other user-facing config referenced
  `input_text.washer_last_cycle_name`; the leak was isolated to the washer
  completion script and the internal handled-action note.

## Change

- Washer completion pushes now say "The washer finished around..." when
  deferred until Trevor is home.
- The handled-action stamp now records "Washer cycle handled" instead of the
  stored cycle label.
- The washer completion automation now stores `Wash` when ThinQ exposes a bare
  number or `load_*` style counter as the cycle value.

## Intent

Keep the durable completion keys and notification guards intact, but never
expose ThinQ counters or opaque identifiers in user-facing copy.

## Deployment

- Wrote and read back `/homeassistant/automations/30-maintenance-environment.yaml`.
- Wrote and read back `/homeassistant/scripts.yaml`.
- Home Assistant config check returned `valid`.
- `script.reload` and `automation.reload` both returned HTTP 200.
- Cleaned live `input_text.washer_last_cycle_name` from the numeric counter to
  `Wash`.
- Verified live `automation.laundry_washer_cycle_complete_notification` remains
  `on`.
