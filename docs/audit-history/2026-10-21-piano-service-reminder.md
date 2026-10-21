# Piano service reminder reconciliation - October 21, 2026

The piano reminder still used a September 26, 2025 tuning date after the latest
service had been completed. Trevor confirmed the September 11, 2026 service
invoice paid and specified tuning at least annually. He approved updating the
existing Home Assistant reminder and clarified that this should leave no piano
pill or reminder on Home after completion.

## Evidence and scope

House Manager's [piano record](../../../house%20manager/assets/antique-steinway-piano.md)
owns the invoice, payment confirmation, date provenance and retained serial
discrepancy. Its next annual due date is September 11, 2027.

The existing live helper was September 26, 2025, the due date September 26,
2026, and care status Tuning due. The YAML `initial` value would restore that
stale date at startup. The July 1 notification-center audit identified the same
initial-value failure for the parking-pass cycle.

## Changes

- Set the existing `input_datetime.piano_last_tuned` to September 11, 2026 using
  its date-specific action, avoiding the Done script that stamps today.
- Removed the helper's stale `initial` value so saved service dates can restore
  on startup.
- Changed reminder text to render the saved last-tuned date and derived next due
  date. It says tuning, keeps the at-least-annual/sooner-if-needed intent and
  existing technician contact, and does not label this service a new appraisal.
- Corrected the source-record comment and removed the obsolete local path from
  the phone message.
- Preserved the annual schedule, existing completion/snooze actions, and enable
  setting. No new Home pill or dashboard card was added. The existing due-only
  Home card becomes hidden when this cycle is current.

## Validation and deployment

- YAML parsing and focused semantic checks passed for both repository and live
  candidates. Only the piano helper initial value and reminder message changed.
- Message rendering passed for the current dates and unavailable-date fallback.
- Device inventory coverage passed for 178 active control references.
- Recorder inventory regenerated successfully; only its generation timestamp
  changed. No Recorder policy change or live database audit was needed.
- Live/repository differences in unrelated templates and two lighting scripts
  were retained. Deployment used exact live bytes with only the reviewed piano
  changes, rather than replacing live files with the repository versions.
- Administrative MCP deployment `3f366bdad3054d23af1bc4eb04188eb3` applied both
  files, passed Home Assistant's configuration check, and completed script reload.
  Exact live file hashes matched the prepared results afterward.
- Native MCP did not expose the piano entities or a date-helper write. The
  existing authenticated HA interface supplied the targeted date action and
  live state verification; administrative MCP handled file deployment.
- Verified live last-tuned September 11, 2026, next due September 11, 2027,
  due sensor off, care status Current, and care enabled.
- Refreshed Home and inspected its accessibility tree and rendered screen:
  no piano reminder or pill remains. No dashboard edit was necessary.

No Core restart, test push, booking or vendor contact occurred. Startup
persistence is supported by removal of the initial override; a restart was not
performed to test restoration. Future notification delivery is not claimed from
configuration and state checks alone.
