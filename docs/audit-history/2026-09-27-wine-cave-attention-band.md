# Wine Cave Attention Band

Date: 2026-09-27

## Symptom And Prior Context

The Home tile frequently said **Needs attention** for the wine cabinet, making
ordinary conditions appear actionable. Trevor confirmed red-wine storage and
authorized using judgment to correct the policy.

Reviewed the audit-history index, July 20 EuroCave identity reconciliation,
July 13/20 Wine chart disclosure work, dashboard chart audit, deployment
runbook, notification reliability patterns, and the confirmed House Manager
La Première L appliance record and manual. Chart loading and completed
appliance maintenance tasks are separate from this environmental issue.

## Evidence And Ranked Findings

1. **High confidence: narrow instantaneous status caused false attention.**
   The old status required 53–57°F and 50–65% RH for `Optimal`. Home translated
   raw `Warning` into `Needs attention`, even without a sustained actionable
   alert. The Wine page instead called the same state slightly outside target.
   Raw humidity above 72% became `Critical` immediately.
2. **High confidence: the cabinet was steady.** Seven days of live Recorder
   history ending September 27 showed temperature 53.94–55.36°F, time-weighted
   mean 54.70°F; RH 54.01–67.67%, mean 64.32%. Humidity exceeded the old 65%
   ceiling for 62.75% of valid time. Status was `Warning` for about 105.41 of
   168 hours; the actionable alert stayed off. The query returned 6,801
   temperature and 8,006 humidity entries.
3. **High confidence: humidity criteria were narrower than manufacturer
   storage guidance.** EuroCave Netherlands distinguishes 60–75% optimal RH
   from 50–80% good RH. The manual specifies above 50%, ideally 60–75%, and
   separates ageing temperature from red-wine serving temperature.
4. **High confidence: old humidity alerts could contradict the broader band.**
   Air temperature minus derived dew point below 7°F can occur near 77% RH at
   55°F; this is not a measured cabinet surface temperature. The moisture
   anomaly rule also allowed a high-humidity alert above 70%.
5. **High confidence, separate follow-up: statistics windows are incomplete.**
   Live statistics showed about 71% coverage for nominal 24-hour temperature/RH
   buffers and 24% for nominal 30-day buffers. Seven-day coverage was complete.
   This audit uses raw seven-day history, not the nominal 30-day average.

## Decision And Changes

- Keep the storage aim near **55°F**. Use **50–60°F / 50–80% RH** as the calm
  monitoring band. These are operational choices, not hard wine-damage limits.
- Make `sensor.wine_cave_status` the display authority. Preserve legacy states
  but publish plain-language `display_label`, `detail`, icon and range
  attributes. A brief excursion or drift means `Monitoring`. `Needs attention`
  requires the delayed actionable sensor. Missing readings are explicit and
  no longer become a zero-degree critical condition.
- Prioritize delayed problems over recovered readings during clearing delays.
- Align Home, Wine hero/detail popup/status chips and Notification Center
  narrative. Measurement colors use the central bounds. Keep all chart content
  and lazy disclosures unchanged.
- Require RH **above 80%** for the existing high-moisture and dew-point-risk
  branches. Retain absolute-humidity/dew-point criteria and their 15-/10-minute
  onset delays. Normal RH alone cannot begin a high-humidity action.
- Allow recovered low-humidity episodes to settle at up to 80% RH; align
  informational excursion flags and add availability checks to them.
- Preserve temperature protection: above 60°F or below 50°F for 15 minutes,
  clearing after 10 minutes back in range. Preserve low-humidity, drift,
  unavailable-sensor, reminder and push-delivery policies.
- Regenerate Recorder inventory; its Markdown report is unchanged. No database
  copy was available and no new row-count claim is made. No physical devices
  or entity IDs were added or renamed.

## Checks And Deployment Status

- Eight regression tests evaluate actual YAML/Jinja templates: inclusive range
  boundaries, 66/75/80% RH, pending excursions, alert priority during recovery,
  missing readings, cooling/drift monitoring, moisture/dew guards and unchanged
  temperature delays. The prior configuration fails the new policy checks.
- Dashboard YAML and JavaScript status cases passed. Structural comparison
  confirms ten Wine charts and three lazy disclosures are unchanged; other
  views are unchanged except the Home Wine tile.
- Device inventory coverage passes for 174 active control references.
- Prepared exact-match patches that preserve unrelated live Main Floor drift.
  Configuration patches also match the saved live snapshot from the phone task.
- **Live deployment pending:** the Mac locked after the connected history
  inspection. No Wine changes have been written live. The user was asked to
  unlock it. Next: fresh preflight, full read-back, HA config validation,
  template reload, then served-dashboard and live-status verification.

Scratch files are in the dedicated Codex work folder; nothing from this audit
was created in Downloads.

## Residual Risks And Follow-Ups

- Dew point remains a moisture-risk estimate, not proof of condensation. Check
  bottle/rear-wall contact and actual moisture if it trips.
- Low-humidity reminders remain stricter than the cabinet's native alarm
  (manual: below 50% for over 72 hours). The observed week contained no low-RH
  episode, so that separate policy was not tuned.
- Existing delay and automation `for` periods can reset on reload/restart;
  durable episode timestamps are a separate reliability improvement.
- Correct statistics buffer coverage before treating nominal 24-hour/30-day
  averages as full-window measurements. No restart/buffer expansion was bundled.
- Large-file decomposition remains a known separate risk; require complete
  read-back for this focused patch.

## Sources

- [EuroCave Netherlands storage guidance](https://eurocave.nl/en/wine-cabinets/wine-storage-cabinets/):
  60–75% optimal humidity; 50–80% good humidity.
- [La Première manual](https://eurocave.nl/en/wp-content/uploads/2024/01/ec-la-premiere-user-manual-notice-0623-7l-md.pdf):
  printed English pp. 4/17 humidity; p. 15 ageing versus serving; p. 19 native
  alarms. Exact pages checked in the preserved House Manager manual after the
  online parser hit its file-size limit.
