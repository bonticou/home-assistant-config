# Audit History

This directory is the durable memory for Home Assistant audits, diagnostics,
incident reviews, and reliability fixes.

Before starting a new audit, read this index and the entries that sound related.
The goal is to keep historical context in the repo so future work can build on
prior evidence instead of rediscovering it in chat.

## How To Use This History

For every meaningful diagnostic or reliability change, add a dated Markdown file
using this naming pattern:

```text
YYYY-MM-DD-short-incident-name.md
```

Each entry should include:

- symptom and user impact;
- relevant prior context;
- evidence collected;
- ranked findings and confidence;
- files/config changed;
- checks and live validation performed;
- deployment status;
- residual risks and next follow-ups.

Do not commit secrets, bearer tokens, raw private URLs, unredacted logs, or
sensitive account identifiers. Redact Nabu Casa hosts and local network details
unless the exact value is necessary and safe to store.

## Recurring Availability Investigation

Home Assistant stalling, fresh-HTTP failures, unexpected offline periods, and
Remote UI disconnects are a continuing longitudinal investigation. Do not treat
each recurrence as a new dashboard problem or assume that every visible
disconnect has the same cause.

The living synthesis is
[Home Assistant Availability Investigation](../home-assistant-availability-investigation.md).
It combines the dated incident record, current failure model, evidence gaps,
active hypotheses, and the reliability optimization idea bank. The idea bank is
not a to-do list or authorization to make changes.

The accumulated evidence currently distinguishes at least three failure
families:

- Home Assistant Core/app-layer stalls or unexpected Core termination;
- Nabu Casa Remote UI/tunnel or TLS-path outages while local Core may remain
  healthy;
- client authentication, session, or local/remote URL handoff failures while
  the underlying Remote UI route remains reachable.

Start with these entries when investigating another recurrence:

- [Unexpected Core restart during Tesla setup, 2026-08-02](2026-08-02-unexpected-core-restart-during-tesla-setup.md)
- [Recorder health gate after cleanup, 2026-07-13](2026-07-13-recorder-health-gate.md)
- [Recorder pressure follow-up, 2026-07-13](2026-07-13-recorder-pressure-follow-up.md)
- [Mobile disconnected with Nabu route reachable, 2026-06-22](2026-06-22-mobile-disconnected-nabu-session.md)
- [Remote UI overnight flapping, 2026-06-16](2026-06-16-remote-ui-overnight-flapping.md)
- [Backend availability audit, 2026-06-06](2026-06-06-backend-availability-audit.md)
- [Home Assistant transient app-layer stall, 2026-06-04](2026-06-04-home-assistant-transient-app-layer-stall.md)
- [Remote UI and fresh HTTP stall, 2026-06-04](2026-06-04-remote-ui-http-stall.md)
- [Home Assistant availability, UI hardening, and Casey closet recovery,
  2026-06-04](2026-06-04-home-assistant-availability-ui-and-casey-closet.md)
- [Legacy mobile disconnect audit, 2026-05-26](../home-assistant-mobile-disconnect-audit-2026-05-26.md)

Supporting material:

- [Home Assistant remote-access runbook](../home-assistant-remote-access-runbook.md)
- [Home Assistant UI-hardening runbook](../home-assistant-ui-hardening-runbook.md)
- [Recorder inventory](../recorder-inventory.md)

## Entries

| Date | Entry | Scope |
| --- | --- | --- |
| 2026-08-03 | [Tesla overnight plug reminder](2026-08-03-tesla-overnight-plug-reminder.md) | Adds a durable after-10 PM Tesla plug-in reminder gated on Trevor home, Tesla home, charge-cable disconnected, and battery-level telemetry while documenting the remaining Tesla Fleet setup dependency |
| 2026-08-03 | [Evening mode catch-up and scene resilience](2026-08-03-evening-mode-catchup.md) | Diagnoses an Evening scene that triggered but only partially applied before later Core restarts, then adds guarded startup/reload/refresh catch-up and parallel fault-tolerant scene chunks |
| 2026-08-02 | [Unexpected Core restart during Tesla setup](2026-08-02-unexpected-core-restart-during-tesla-setup.md) | Confirms the visible outage coincided with an unclean Home Assistant Core restart, rules out repo-owned restart actions, and preserves the Supervisor/previous-Core log follow-up needed to identify the trigger |
| 2026-07-31 | [Wynn daylight light timeout](2026-07-31-wynn-daylight-light-timeout.md) | Shortens Wynn's daylight camera-quiet light timeout from 30 to 20 minutes while retaining the five-minute watchdog and vacation safeguard |
| 2026-07-29 | [Garage transient-open notification grace](2026-07-29-garage-transient-open-notification-grace.md) | Requires a garage door to remain open for five minutes before the one-person-away reminder and removes unsupported blame from its title while preserving immediate both-away and overnight alerts |
| 2026-07-29 | [Dryer cycle notifications](2026-07-29-dryer-cycle-notifications.md) | Adds durable presence- and quiet-hour-aware ThinQ dryer notifications, uses dryer starts as washer-turnover evidence, and reevaluates unresolved washer loads after the housekeeper window |
| 2026-07-29 | [Housekeeper away-security suppression](2026-07-29-housekeeper-away-security-suppression.md) | Suppresses routine lights-on and unsecured-home reminders during the expected housekeeper window, clears active related pushes, and reevaluates at 3:00 PM while preserving safety alerts |
| 2026-07-28 | [Washer presence-aware notifications](2026-07-28-washer-presence-aware-notifications.md) | Records ThinQ completions and machine errors while Trevor is away, defers pushes until five minutes after arrival, and starts follow-ups from the first delivered notice while preserving immediate Flo leak protection |
| 2026-07-20 | [Washer cycle notifications](2026-07-20-washer-cycle-notifications.md) | Adds durable ThinQ completion, unattended-laundry follow-up, snooze/handled actions, and deduplicated high-priority washer error notifications while preserving Flo leak coverage |
| 2026-07-20 | [Wine trend disclosure state](2026-07-20-wine-trend-disclosure-state.md) | Replaces restored helper-backed Wine chart expansion with local ephemeral disclosure state so every page load starts collapsed and charts mount only on demand |
| 2026-07-20 | [EuroCave identity reconciliation](2026-07-20-eurocave-identity-reconciliation.md) | Reconciles confirmed House Manager model/serial evidence into HA appliance context, closes the stale serial-capture task, and validates the live Nabu Casa deployment |
| 2026-07-13 | [Wine chart lazy disclosure](2026-07-13-wine-chart-lazy-disclosure.md) | Converts Wine tab 24-hour, 7-day, and 30-day charts into collapsed summary disclosures so ApexCharts load only when opened |
| 2026-07-13 | [Recorder health gate after cleanup](2026-07-13-recorder-health-gate.md) | Read-only post-cleanup health gate confirming Recorder backlog is zero, Remote UI is online, disk space is ample, and DB-backed writer measurement is the next step |
| 2026-07-13 | [Irrigation ledger zone count](2026-07-13-irrigation-ledger-zone-count.md) | Corrects misleading "full cycle" zone counts by merging Hydrawise daily runtime with custom irrigation history and expanding irrigation templates to zones 1-30 |
| 2026-07-13 | [Recorder config-control slice](2026-07-13-recorder-config-control-slice.md) | Excludes current-only `number`, `select`, Sonos config, and UniFi Protect config-control history from Recorder while preserving durable helpers and safety/physical history |
| 2026-07-13 | [Recorder pressure follow-up](2026-07-13-recorder-pressure-follow-up.md) | Reviews persistent Recorder/storage pressure after updates, captures live Recorder health and large generated state payloads, and defines the next DB-backed cleanup slice |
| 2026-07-06 | [Matter Server 9.0.4 post-update validation](2026-07-06-matter-server-9-validation.md) | Confirms Matter Server migration-class update completed cleanly with active locks reporting fresh states and no integration changes required |
| 2026-07-06 | [File Editor ingress 401 after update](2026-07-06-file-editor-ingress-401-after-update.md) | Diagnoses File Editor `6.0.0` panel load failure after update as stale duplicate ingress-session cookies, not add-on or YAML failure |
| 2026-07-04 | [Irrigation no-flow false alerts](2026-07-04-irrigation-no-flow-false-alerts.md) | Diagnoses Hunter cumulative-total lag causing critical no-flow false positives and downgrades the alert to pressure-corroborated flow-not-confirmed warning |
| 2026-07-01 | [Notification Center due boundaries and parking pass cycle](2026-07-01-notification-center-due-boundaries.md) | Hardens Needs Attention due-date filtering and fixes NWP parking pass replacement cycle tracking after a 1-month renewal |
| 2026-06-30 | [Hunter Flow irrigation build](2026-06-30-hunter-flow-irrigation-build.md) | Implements Hunter-derived irrigation measurement, flow-baseline alerts, dashboard rebuild, inventory refresh, and live deployment/restart validation |
| 2026-06-29 | [Irrigation Hunter Flow review](2026-06-29-irrigation-hunter-flow-review.md) | Reviews what direct Hunter irrigation flow enables for notifications and dashboard design, and identifies primitive irrigation tab items to remove or demote |
| 2026-06-25 | [Profitec Saturday due policy](2026-06-25-profitec-saturday-due-policy.md) | Opens water backflush and Cafiza due cycles on Saturday, including Sunday pull-forward, while weekday reminders continue only for open weekend-originated cycles |
| 2026-06-25 | [Casey closet Lutron bridge disconnect](2026-06-25-casey-closet-lutron-bridge-disconnect.md) | Motion reached HA and automation matched, but Lutron light service failed with bridge disconnect; added motion-on retries |
| 2026-06-24 | [Foyer chandelier overnight schedule](2026-06-24-foyer-chandelier-overnight-schedule.md) | Separates foyer chandelier from front-stairs overnight schedule so it is evening-only and turns off before overnight |
| 2026-06-23 | [HA update readiness and remote auth bootstrap](2026-06-23-ha-update-readiness-and-remote-auth.md) | Pre-update repo backup, auth-provider failure evidence, Zscaler Mac/TLS factor, and authenticated-check blocker |
| 2026-06-22 | [Mobile disconnected with Nabu route reachable](2026-06-22-mobile-disconnected-nabu-session.md) | Current Nabu shell and websocket reachable while mobile/Safari appeared stuck in auth/session handoff |
| 2026-06-22 | [Overnight Evening retrigger](2026-06-22-overnight-evening-retrigger.md) | Blocks presence tracker recovery from re-running Evening while someone is already home overnight |
| 2026-06-21 | [Vacation return lighting and Wynn protection](2026-06-21-vacation-return-wynn-lighting.md) | Ends vacation lighting when Trevor or Casey returns, then restores normal Evening mode without turning on Wynn's lights |
| 2026-06-16 | [Remote UI overnight flapping](2026-06-16-remote-ui-overnight-flapping.md) | Mobile app network errors matched repeated Nabu Casa Remote UI-off windows, including a 54-minute overnight outage |
| 2026-06-15 | [Dehumidifier Done action and mudroom exterior schedule](2026-06-15-dehumidifier-done-and-mudroom-exterior.md) | Hardened dehumidifier/fertilizer Done scripts and removed mudroom exterior light from normal door-light schedule |
| 2026-06-12 | [Front stairs cloudy evening threshold](2026-06-12-front-stairs-cloudy-evening-threshold.md) | Earlier evening-light threshold for cloudy/partly-cloudy dusk when the front stairs stayed off too long |
| 2026-06-11 | [Garbage recycling Home sticky bar](2026-06-11-garbage-recycling-home-sticky-bar.md) | Home-tab sticky garbage/recycling reminder with taken-out action and holiday-delay priority |
| 2026-06-11 | [Dehumidifier air filter reminder](2026-06-11-dehumidifier-air-filter-reminder.md) | Alternate-Friday growing-season dehumidifier air filter notification with Done/Snooze and Notification Center item |
| 2026-06-11 | [Garden fertilizer reminder](2026-06-11-garden-fertilizer-reminder.md) | Every-other-Friday growing-season fertilizer notification with Done/Snooze and Notification Center item |
| 2026-06-11 | [Profitec GO weekend notification policy](2026-06-11-profitec-weekend-notification-policy.md) | Weekend-first espresso cleaning notifications, weekday only after snooze or away-weekend deferral |
| 2026-06-11 | [Casey closet stale-on recurrence](2026-06-11-casey-closet-stale-on.md) | Twelve-minute hard cap and watchdog for Casey closet light stale-on failures |
| 2026-06-10 | [Overnight lights sweep](2026-06-10-overnight-lights-sweep.md) | Midnight whole-house left-on lighting reminder, snooze, and guarded 1 AM auto-off |
| 2026-06-09 | [Irrigation Flo topology correction](2026-06-09-irrigation-flo-topology.md) | Hydrawise as irrigation source of truth, Flo pressure as shared-well context, Flo-derived irrigation memory cleanup |
| 2026-06-04 | [Garden decommission](2026-06-04-garden-decommission.md) | Crop-garden UI/config removal, Recorder purge, entity-registry cleanup, inventory refresh |
| 2026-06-04 | [Home Assistant availability, UI hardening, and Casey closet recovery](2026-06-04-home-assistant-availability-ui-and-casey-closet.md) | Remote/mobile disconnect audit, diagnostic hardening, config recovery, Casey closet motion fix |
| 2026-06-04 | [Home Assistant transient app-layer stall](2026-06-04-home-assistant-transient-app-layer-stall.md) | Local HTTP/websocket stall, Remote UI loading failure, recovered without config change |
| 2026-06-04 | [Remote UI and fresh HTTP stall](2026-06-04-remote-ui-http-stall.md) | Existing websocket stayed live while fresh local HTTP and Remote UI TLS failed |
| 2026-06-04 | [Casey closet unexpected light-on](2026-06-04-casey-closet-unexpected-light-on.md) | Manual-on hypothesis, sensitivity calibration, quiet-off validation |
| 2026-06-05 | [Casey closet missed motion](2026-06-05-casey-closet-missed-motion.md) | Missed real closet entry, Core availability window, UniFi Protect sensitivity correction |
| 2026-06-06 | [SSD data-disk migration and Casey closet miss](2026-06-06-ssd-data-disk-and-casey-closet.md) | External data disk migration, storage breakdown, Core flapping, Casey closet missed motion |
| 2026-06-06 | [Backend availability audit](2026-06-06-backend-availability-audit.md) | Core/Supervisor/storage/Recorder/add-on/network evidence, probe-path finding, monitoring next step |

## Related Legacy Reports And Runbooks

- [Home Assistant mobile disconnect audit, 2026-05-26](../home-assistant-mobile-disconnect-audit-2026-05-26.md)
- [Home Assistant deploy runbook](../home-assistant-deploy-runbook.md)
- [Home Assistant remote access runbook](../home-assistant-remote-access-runbook.md)
- [Home Assistant UI hardening runbook](../home-assistant-ui-hardening-runbook.md)
- [Dashboard chart audit](../dashboard-chart-audit.md)
- [Device inventory](../device-inventory.md)
- [Recorder inventory](../recorder-inventory.md)
