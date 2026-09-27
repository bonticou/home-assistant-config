# Trevor iPhone Replacement

Date: 2026-09-26
Updated: 2026-09-27
Status: live replacement complete; naming, presence, rich notification delivery, action callback, and old-registration removal verified

## Goal And Current Status

Trevor replaced his iPhone with an iPhone 18 Pro and requested a comprehensive
Home Assistant replacement, including appropriate naming. Trevor confirmed the
old handset is being traded in and authorized its removal after the
replacement is connected.

The task paused on September 26 while the Mac was locked, after local
preparation and initial live inspection. Access resumed September 27. The
new phone's 31 entities, device display name, and integration title have now
been renamed; all 49 live tracker references have been migrated with exact
file read-back; and Trevor's person association now excludes the old phone.
Home Assistant configuration validation and the relevant reloads succeeded.

Notification testing exposed and corrected a pre-existing live wrapper
incompatibility: `notify.send_message` rejects the nested rich notification
`data` payload in this Home Assistant version. The corrected dynamic legacy
service preserves that full payload and is now deployed and verified. A
labeled actionable migration push succeeded and a real
`TREVOR_IPHONE_MIGRATION_ACK` callback was received, confirming receipt and the
action round trip. The old Companion registration was removed without a
restart, and the final registry confirms the old device is absent. The live
replacement is complete.

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

## Initial Evidence Collected, September 26

- The old Companion device reports model `iPhone17,1`; the new device reports
  `iPhone19,2`. Both registrations retain the original name
  `TK iPhone 16 Pro`.
- The old tracker, `device_tracker.tk_iphone_16_pro`, has been `not_home` since
  September 24. The new tracker, `device_tracker.tk_iphone_16_pro_2`, reports
  `home`, uses a GPS location source, and reports location permission
  `Authorized Always`.
- Trevor's existing person entity, `person.bonticou`, initially included the
  old phone, new phone, and iPad.
- The new phone has its own notify entity,
  `notify.tk_iphone_16_pro_2`. The legacy mobile notify service still uses the
  old phone name; the duplicate naming means that service name alone is not
  reliable evidence of the intended handset destination.
- Before local edits, tracked YAML contained 49 old-phone tracker references
  and one old mobile notify-service reference. The shared
  `script.notify_trevor_phone` already serves 170 callers.
- The initial live file snapshot differed from the repository: 44 tracker references in
  live automations and one in live scripts already use the new `_2` tracker,
  while four references in live `configuration.yaml` still use the old tracker.
  The live notification wrapper already used `notify.send_message` targeting
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

1. **High confidence: rich notification delivery required a separate correction.**
   The initial live wrapper already called `notify.send_message` with nested
   `data`; testing after cutover showed that payload is rejected. Basic pushes
   and rich actionable notifications required separate verification. The
   deployed legacy-service correction passed a real notification/action test.
2. **High confidence: duplicate phone naming made delivery and maintenance
   ambiguous.** Stable tracker and notify entity names and a clear device
   display name are now applied, and the old Companion registration is gone.
   The wrapper resolves the legacy service from the new device's original
   Companion registration name rather than its display override.
3. **High confidence: whole-file deployment would include unrelated behavior
   changes.** Semantic comparison identified Main Floor sensor-spread and Flo
   valve-test differences between live files and the repository. The surgical
   live tracker migration preserved those existing live differences.
4. **High confidence: deployment size remains a reliability concern.** The
   repository's `configuration.yaml` is about 439 KB, of which about 389 KB is
   the template domain. File Editor truncation is a known project failure mode.
   This repair did not add unrelated decomposition work; the live tracker
   cutover required and obtained complete read-back before reload. Subsequent
   writes still require byte/hash read-back. Decomposition remains
   a separate reliability follow-up before unrelated feature work.

## Local Changes Completed

Replaced exactly 49 references to `device_tracker.tk_iphone_16_pro` with the
now-live stable name `device_tracker.trevor_iphone`:

| File | Tracker replacements |
| --- | ---: |
| `automations/10-lighting-security.yaml` | 26 |
| `automations/20-climate-commute.yaml` | 4 |
| `automations/30-maintenance-environment.yaml` | 14 |
| `configuration.yaml` | 4 |
| `scripts.yaml` | 1 |

The local wrapper initially matched the existing live `notify.send_message`
delivery step, targeting `notify.trevor_iphone`. The September 27 test exposed
that pre-existing payload incompatibility. The latest local wrapper instead
resolves the full-data legacy service from the stable new tracker:

```yaml
action: "{{ 'notify.mobile_app_' ~ (device_attr('device_tracker.trevor_iphone', 'name') | slugify) }}"
```

This uses the registry's original device name, which determines the service
name, rather than its user-facing display override. Title, message, nested
notification data, and internal event metadata remain intact. The correction
passed YAML parsing, complete live read-back, script reload, and a real
actionable notification test.

Timing, unknown/unavailable guards, durable completion helpers, Casey's
references, and the stable `person.bonticou` entity identity are unchanged.

## Live Changes Completed, September 27

- Renamed all 31 entities belonging to the new phone, including stable
  `device_tracker.trevor_iphone` and `notify.trevor_iphone` identities and
  descriptive iPhone 18 Pro names for the remaining entities.
- Set the device's user-facing display name and config-entry title to
  `TK iPhone 18 Pro`. This does not establish that the iOS device name or
  Companion registration name changed; the original registration name remains
  relevant to legacy push service resolution.
- Removed the old phone from `person.bonticou`, retained its existing iPad
  association, and retained the new phone. Current Trevor presence is `home`
  with the new phone as its active source.
- Applied 49 tracker-reference changes across the three live files:
  `configuration.yaml` (four), `automations.yaml` (44), and `scripts.yaml`
  (one). Each complete live file matched the prepared candidate on read-back.
  The first scripts deployment also migrated the notify-entity target while
  retaining the pre-existing `notify.send_message` action.
- Preserved the live monolithic automation layout and unrelated Main Floor/Flo
  behavior through surgical changes based on captured live content.
- Home Assistant configuration validation returned valid, with `errors: null`
  and `warnings: null`. Template, script, and automation reloads completed.
- Verified `binary_sensor.downstairs_someone_home` is `on` after cutover.
- Deployed the corrected dynamic legacy-service wrapper and reloaded scripts.
  Final read-back verified all three live files, and the final Home Assistant
  config check again returned valid with null errors and warnings.
- Removed the authorized old Companion config entry. The removal returned
  `require_restart: false`; the post-removal device registry confirms the old
  Companion device is absent and the new device retains all 31 renamed
  entities.
- Rechecked Trevor's tracker and person after removal: both report `home`, and
  `person.bonticou` selects `device_tracker.trevor_iphone` as its active source.
  Its configured trackers are the new phone and the existing iPad tracker;
  the old phone is no longer associated.

## Notification Test Finding, September 27

The first actionable test through the wrapper failed because
`notify.send_message` rejected nested notification `data`. This was already
present in the live wrapper captured before this task; entity renaming did
not introduce that action choice. A separate basic push through the new notify
entity was accepted by Home Assistant, but acceptance does not prove receipt.

The version-matched [Home Assistant Core 2026.9.2 mobile_app notification
implementation](https://github.com/home-assistant/core/blob/2026.9.2/homeassistant/components/mobile_app/notify.py#L72-L108)
supports title and message on `MobileAppNotifyEntity`. The same file's
[legacy notification service](https://github.com/home-assistant/core/blob/2026.9.2/homeassistant/components/mobile_app/notify.py#L175-L196)
also forwards nested `data`. That explains the observed rejection and why the
correction uses the legacy service for actions, tags, and other rich payloads.

After the correction and old-registration removal, one labeled actionable
migration push was accepted and the real `TREVOR_IPHONE_MIGRATION_ACK` callback
was received. This verifies the new handset received the actionable push and
returned its acknowledgment. That result is stronger than the earlier basic
service acceptance or the wrapper's internal history event. It does not claim
that every source automation or future delivery condition was retested.

## Device Inventory Reconciliation

Updated `docs/device-inventory.json`, `docs/device-inventory.md`, and
`docs/device-inventory-detail.md` with the verified September 27 phone changes.
The resulting inventory has 231 devices and 2,539 entities, includes all 31
renamed new-phone entities, and removes the old Companion device and its
entities. The existing disabled UniFi network record is preserved and labeled
as historical, not an active presence source.

The phone-specific verification date is September 27; the wider inventory's
base live snapshot remains July 29. Unrelated inventory records were preserved
rather than represented as freshly audited. The person-source notes record the
new phone plus the existing iPad and the verified notification acknowledgment.

The live inventory refresh command and its status-sensor refresh also completed.
Regenerated `docs/recorder-inventory.json` and `docs/recorder-inventory.md` from
the reconciled inventory: 2,539 entities reviewed and 1,537 Recorder candidates.
No Recorder database was copied for this migration; database row/frequency
measurements were not refreshed, and no history was purged.

## Checks Run

- Ruby/Psych YAML syntax parsing passed for all five edited YAML files.
- Surgical candidates built from the captured live configuration, scripts,
  and monolithic automations also passed Ruby/Psych parsing. Their tracker
  cutover was deployed and matched on complete live read-back September 27.
- A comparison against the original tracked files confirmed the tracker edit
  was exactly the intended 49 substitutions. The notification wrapper was
  first aligned with the observed live `notify.send_message` payload. The
  subsequent legacy-service correction preserves that metadata and full data.
- `git diff --check` passed.
- Loaded all three live dashboard configurations (`calm-mobile`, `ha-safe`,
  and `lovelace`); none contains an old-phone entity reference.
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
  validate tracker or notify entity existence. The new tracker and notify
  entity were separately verified live, and the rich delivery/action path was
  verified with the migration test.
- Live Home Assistant config validation, tracker-cutover file read-back,
  template/script/automation reloads, and post-migration person-source checks
  completed. Final notification-correction read-back and script reload also
  completed, as did the real handset acknowledgment test and post-removal
  registry verification.

## Residual Risks And Next Follow-Ups

The internal Companion registration still uses `TK iPhone 16 Pro`, while the
Home Assistant display name and integration title are `TK iPhone 18 Pro`.
The dynamic wrapper follows the registry's original name, so no handset rename
is required to keep notifications working. Renaming the iOS or Companion label
later is optional; the service resolver is designed to follow the registration
name when it updates.

The retained, disabled UniFi tracker for the old phone is a historical network
record, not the active Companion presence source. Casey's tracker and person
identity remain unchanged. Trevor's existing iPad association is also
preserved; current presence selects the new phone. Observe the next real
departure and return to confirm background location behavior and existing
arrival timing in normal use.

Stable tracker and notify entity identities reduce the scope of the next
phone replacement, but the next device's registration and person association
will still need deliberate verification. The repository/live Main Floor and
Flo differences and large configuration-file follow-up remain separate from
this completed migration.
