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

## Entries

| Date | Entry | Scope |
| --- | --- | --- |
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
