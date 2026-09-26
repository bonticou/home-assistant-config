# Trevor iPhone Replacement

Date: 2026-09-26
Status: local migration prepared and syntax-checked; live migration and inventory reconciliation pending

## Goal And Current Status

Trevor replaced his iPhone with an iPhone 18 Pro and requested a comprehensive
Home Assistant replacement, including appropriate naming. The new Companion
registration is already present, but the old and new registrations share the
same original name and the home configuration only partially follows the new
phone. Trevor confirmed the old handset is being traded in and authorized its
removal after the replacement is connected.

At the time of this entry, this task has made **no live entity or device
renames, person-association changes, file deployments, or registration
removals**. The Mac is temporarily locked, preventing continuation through the
authenticated browser. Local edits are prepared; the target entity names below
must not be treated as verified live names. Inventory reconciliation remains
pending.

## Relevant Prior Context

- [Washer presence-aware notifications, 2026-07-28](2026-07-28-washer-presence-aware-notifications.md)
  established the phone tracker as Trevor's explicit home/away source and
  preserves five-minute arrival timing for deferred laundry notices.
- [Overnight Evening retrigger, 2026-06-22](2026-06-22-overnight-evening-retrigger.md)
  guards against interpreting unknown/unavailable recovery as a real arrival.
- [Vacation return lighting and Wynn protection, 2026-06-21](2026-06-21-vacation-return-wynn-lighting.md)
  depends on the household person entities as well as phone-specific presence.
- [Notification reliability audit, 2026-08-07](2026-08-07-notification-reliability-audit.md)
  distinguishes an accepted Home Assistant notify call from confirmed handset
  receipt and an action callback.
- [Sonos device-tracker Recorder cleanup, 2026-08-21](2026-08-21-sonos-device-tracker-recorder-cleanup.md)
  already records the inventory check's `light.state` / `light.last_changed`
  boundary.
- [Notification reliability patterns](../notification-reliability-patterns.md),
  [deployment runbook](../home-assistant-deploy-runbook.md), and the device and
  Recorder inventories informed the migration scope and validation plan.

## Evidence Collected

- The old Companion device reports model `iPhone17,1`; the new device reports
  `iPhone19,2`. Both registrations retain the original name
  `TK iPhone 16 Pro`.
- The old tracker, `device_tracker.tk_iphone_16_pro`, has been `not_home` since
  September 24. The new tracker, `device_tracker.tk_iphone_16_pro_2`, reports
  `home`, uses a GPS location source, and reports location permission
  `Authorized Always`.
- Trevor's existing person entity, `person.bonticou`, currently includes the
  old phone, new phone, and iPad. That association has not yet been adjusted.
- The new phone has its own notify entity,
  `notify.tk_iphone_16_pro_2`. The legacy mobile notify service still uses the
  old phone name; the duplicate naming means that service name alone is not
  reliable evidence of the intended handset destination.
- Before local edits, tracked YAML contained 49 old-phone tracker references
  and one old mobile notify-service reference. The shared
  `script.notify_trevor_phone` already serves 170 callers.
- The live file snapshot differs from the repository: 44 tracker references in
  live automations and one in live scripts already use the new `_2` tracker,
  while four references in live `configuration.yaml` still use the old tracker.
  The live notification wrapper already uses `notify.send_message` targeting
  the new phone's notify entity.
- Live `automations.yaml` is a monolithic list, whereas the repository uses an
  include pointer and four coherent automation files. The snapshot contains
  181 automations; the repository contains 182.
- The inspected live configuration, automation, script, and Calm dashboard
  files contain no direct iPhone sensor references or phone-specific
  `device_id`, `sourceDeviceID`, or `source_device_id` action filters. This does
  not establish coverage of every UI-managed or storage dashboard.

Private live snapshots and registry evidence are retained only in ignored
local audit scratch space. This report omits raw registry identifiers,
location coordinates, account identifiers, and private URLs.

## Ranked Findings

1. **High confidence: the replacement is only partly connected to the home
   model.** Four live templates still follow the old tracker, and the person
   association still includes both phones and the iPad. Direct-tracker and
   person-based presence can consequently disagree.
2. **High confidence: duplicate phone naming makes delivery and maintenance
   ambiguous.** The new device's dedicated notify entity provides an explicit
   destination; stable tracker and notify entity names avoid another widespread
   replacement on the next handset upgrade.
3. **High confidence: whole-file deployment would include unrelated behavior
   changes.** Semantic comparison identified Main Floor sensor-spread and Flo
   valve-test differences between live files and the repository. The phone
   migration should preserve those existing live differences.
4. **High confidence: deployment size remains a reliability concern.** The
   repository's `configuration.yaml` is about 439 KB, of which about 389 KB is
   the template domain. File Editor truncation is a known project failure mode.
   This repair does not add unrelated decomposition work; any eventual write
   requires complete byte/hash read-back before reload. Decomposition remains
   a separate reliability follow-up before unrelated feature work.

## Local Changes Completed

Replaced exactly 49 references to `device_tracker.tk_iphone_16_pro` with the
planned stable name `device_tracker.trevor_iphone`:

| File | Tracker replacements |
| --- | ---: |
| `automations/10-lighting-security.yaml` | 26 |
| `automations/20-climate-commute.yaml` | 4 |
| `automations/30-maintenance-environment.yaml` | 14 |
| `configuration.yaml` | 4 |
| `scripts.yaml` | 1 |

Updated the local `script.notify_trevor_phone` delivery step to
`notify.send_message`, targeting the planned `notify.trevor_iphone` entity.
Existing title, message, nested notification data, and internal event metadata
are preserved. Timing, unknown/unavailable guards, durable completion helpers,
Casey's references, and `person.bonticou` references are unchanged.

No device inventory, Recorder inventory, or device-registry changes have been
completed yet.

## Live Migration Planned, Not Completed

- Rename the new device for display as `TK iPhone 18 Pro` and reconcile its
  Companion name with the handset settings. Do not infer that changing a
  Home Assistant display name changes the iOS device or Companion setting.
- Apply and verify the prepared 31-entity rename mapping for the new phone,
  including stable `device_tracker.trevor_iphone` and `notify.trevor_iphone`
  identities and descriptive iPhone 18 Pro names for its remaining entities.
- Adjust `person.bonticou` to use the new phone as Trevor's active presence
  source; the old phone and iPad association currently remains in place.
- Surgically update the live files from their captured live content: change
  44 automation references, one script reference, the wrapper notify target,
  and four configuration references. Preserve the live monolithic automation
  layout and unrelated Main Floor/Flo behavior during this migration.
- Reconcile the device inventory JSON and human-readable inventory after live
  names and associations are verified; regenerate the Recorder inventory.
- Verify notification receipt, a harmless notification action round trip, and
  current presence-derived states before deciding whether to retire the old
  registration. No old registration has been removed.

## Checks Run

- Ruby/Psych YAML syntax parsing passed for all five edited YAML files.
- Surgical candidates built from the captured live configuration, scripts,
  and monolithic automations also passed Ruby/Psych parsing; they remain in
  ignored scratch space and have not been deployed.
- A comparison against the original tracked files confirmed the tracker edit
  was exactly the intended 49 substitutions. The notification wrapper was
  then aligned with the observed live `notify.send_message` payload, retaining
  existing notification metadata.
- `git diff --check` passed.
- Semantic comparison, accounting for phone-name mappings and equivalent YAML
  duration representations, found no unrelated script differences.
- Configuration comparison found five affected Main Floor template entities:
  two spread entities present only in the repository and three differing
  status/insight entities. Four automation objects differ:
  `downstairs_climate_pilot_startup_sync`,
  `downstairs_climate_sensor_spread_watch`, `environment_room_alert_clears`, and
  `water_shutoff_valve_closed`. One Calm dashboard details-sheet field also
  differs because of Main Floor spread presentation.
- `python3 tools/check_device_inventory_coverage.py` initially reported the
  two pre-existing false positives `light.state` and `light.last_changed`.
  These are attributes of a local Jinja variable in the Wynn lighting
  automation, not real missing light entities; the August 21 audit already
  recorded this boundary. Added those two State-object properties to the
  checker's existing service/template suffix exclusions. Coverage now passes
  for 174 active control references without inventing inventory devices.
- That inventory checker only covers physical control domains; it cannot
  validate tracker or notify entity existence. Explicit live verification of
  the new tracker and notify target is still required.
- Live Home Assistant config validation, deployment read-back, reloads,
  handset receipt/action confirmation, and post-migration person-source
  verification have **not** been completed for this migration.

## Residual Risks And Next Follow-Ups

Resume authenticated live access after the Mac is available. Recheck current
registrations and file contents before applying the prepared mapping because
handset naming or configuration may have changed during the pause. Preserve
Casey's tracker and person identity, avoid stale-device contributions to
Trevor's presence, and do not interpret a successful push service call as proof
of handset receipt.

Update this entry with actual rename, deployment, read-back, configuration
validation, inventory, and end-to-end test results when they occur. Until then,
the migration remains prepared locally and incomplete live.
