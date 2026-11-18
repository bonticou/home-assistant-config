# Home Assistant operations map

Use this as the project entrypoint for locating behavior and choosing the right
inspection, change and verification path. Procedures remain in the linked
runbooks; this map does not replace them or authorize new live actions.

Last reviewed: **October 23, 2026**. Counts below describe the repository at this
review unless explicitly labelled live. Update the affected row when ownership
or access changes; do not treat these counts as a continuous health check.

## Start here

1. Read [project instructions](../AGENTS.md), including shared instructions and
   the delegated-work rule. Reuse the user's existing scoped authorization.
2. Check [audit history](audit-history/README.md) for the relevant feature or
   symptom, then locate its implementation below. Start from the user's visible
   feature: a Notification Center item is not necessarily an automation entity.
3. Inspect current live state and owning files through the appropriate MCP.
   Compare live hashes/content before editing; the repo is not a complete live mirror.
4. Make the smallest covered change, validate, deploy with recovery, then verify
   the actual state or UI. Save evidence and commit the coherent local slice.

House Manager owns service/invoice facts; this repo owns implemented HA behavior.
See [records ownership and follow-through](audit-history/2026-10-21-records-intake-context.md).
Keep source originals, private identifiers and credentials outside these docs.

## Configuration and ownership

The flow is integration/device state → derived templates and durable helpers →
automation decisions/scripts → device actions, pushes and dashboard presentation.
Some behavior lives in UI-managed integrations and registries outside YAML.

| Layer | Authoritative repository entrypoint and role |
| --- | --- |
| Global configuration | [Main YAML](../configuration.yaml): default configuration, frontend, Lovelace, HomeKit, Recorder, helpers, templates, command-line and shell-command definitions, plus includes below |
| Automations | [Include pointer](../automations.yaml) loads five [automation files](../automations); 183 definitions locally. Live currently uses a monolithic file; see coverage below |
| Scripts | [Scripts](../scripts.yaml): 146 actions, lighting modes, delivery wrappers, completion/snooze/clear operations. Named lighting scenes are implemented here; [scenes](../scenes.yaml) is empty |
| Helpers | Main YAML: 198 helpers—98 datetime, 37 text, 45 boolean, 4 select, 14 number. Inspect restoration, startup defaults and cycle semantics before changing state |
| Derived model | Main YAML `template`: 196 entities—105 sensors, 90 binary sensors, one switch. House status, presence/security, water/irrigation, environment, wine care, deadlines and notice timeline/history |
| Included sensors/lights | [Statistics sensors](../sensors.yaml): nine Wine/basement-radon sensors. [Light groups](../lights.yaml): six groups |
| HomeKit | Main YAML `homekit`: House Modes bridge exposes four lighting-mode scripts and two garage doors; separate from native MCP exposure |
| Persistent history | Main YAML `recorder`: 30-day retention with domain/glob/entity exclusions; [Recorder inventory](recorder-inventory.md) describes actual policy and its evidence limits |
| Local data tools | Main YAML `command_line` and `shell_command`; [tools directory](../tools). Nine command sensors and 15 shell commands support durable records, inventory and irrigation data |
| Themes and UI | [Themes](../themes), [primary dashboard](../dashboards/calm_mobile.yaml), [diagnostic dashboard](../dashboards/ha_safe.yaml), local [frontend modules](../www) |
| Extensions | Repository [custom integrations](../custom_components), [blueprints](../blueprints), and [administrative add-on](../addons/codex_ha_admin/README.md). Presence in the repo does not prove runtime installation/version |

All 19 top-level YAML keys were accounted for: `default_config`, `homeassistant`,
`frontend`, `lovelace`, `automation`, `script`, `scene`, `homekit`, `command_line`,
`shell_command`, the five `input_*` domains, `recorder`, `template`, `sensor`, `light`.

### Feature entrypoints

When adding or replacing a household light, use the
[required lighting onboarding checklist](lighting-onboarding.md). The shared
physical inventory in `helpers/household_lighting.yaml` owns away detection and
the explicit notification shutoff; verify both paths in the same task.

Automation filenames are broad groupings, not exclusive domain boundaries.
Search the exact entity, alias or user-facing title across the relevant group,
main YAML, scripts and dashboard before changing it.

| Feature | First implementation file | Supporting evidence |
| --- | --- | --- |
| Water, leaks, pressure, irrigation sessions/flow/schedules | [Water and irrigation](../automations/00-water-irrigation.yaml), 43 automations; also inventory refresh, camera motion tracking and Remote UI watchdog | [Water topology](audit-history/2026-06-09-irrigation-flo-topology.md), [irrigation precision](audit-history/2026-09-11-irrigation-notification-precision.md), irrigation tools/tests |
| Lighting, vacation, presence, entry/garage security, Ring | [Lighting and security](../automations/10-lighting-security.yaml), 46; also water recovery/actions and notification-action history | Lighting scripts, light groups, [audit history](audit-history/README.md) |
| Room climate, windows, batteries, Ting, espresso, commute | [Climate and commute](../automations/20-climate-commute.yaml), 29; also theme/sconce synchronization | [Climate notes](climate-notes.md), [commute tool](../tools/mta_mnr_departures.py) |
| Laundry, home care, deadlines, garden planning, Wine, radon/humidity | [Maintenance and environment](../automations/30-maintenance-environment.yaml), 64 | Templates/helpers, completion scripts, [notice reliability](notification-reliability-patterns.md), [Wine policy checker](../tools/check_wine_cave_policy.py) |
| Generator | [Generator notifications](../automations/35-generator-notifications.yaml), one | [Generator policy](generac-notifications.md) and [focused tests](../tests/test_generac_notifications.py) |
| Notification Center / Home attention | `sensor.house_notice_timeline` and related notice templates in main YAML, [notice card](../www/house-notices-card.js), primary dashboard `notices` view | [Reliability patterns](notification-reliability-patterns.md), [detail surfaces](notification-detail-surfaces.md), [action-stamp ledger](action-stamp-ledger.md) |
| Availability or frontend disconnects | [Availability investigation](home-assistant-availability-investigation.md) first | [Remote access](home-assistant-remote-access-runbook.md), [UI hardening](home-assistant-ui-hardening-runbook.md), [health probe](../tools/ha_remote_health_probe.py) |

The recorded device/platform families include UniFi/Protect, Hydrawise, Sonos,
Lutron, TP-Link, Flo, SensorPush, Ecobee through HomeKit, Ring, ESPHome/garage,
Matter/locks, ThinQ laundry, Ting, Airthings and Generac. Use the
[device inventory](device-inventory.md) and [inventory JSON](device-inventory.json)
for exact entity mappings, with the freshness limits below. Repo manifests cover
Browser Mod, HACS and Whisker Ting; they are not a complete list of live integrations.

Command sensors cover the House action ledger, Wine collection snapshot,
Metro-North departures, inventory status/digest, irrigation flow baseline,
history, actual rainfall and seven-day ledger. Shell commands update those
records, log property-tax actions and manage irrigation history/baselines.
Inspect the referenced tool and data owner before invoking one; reads and writes
are mixed in this layer.

### Dashboards and notices

`/calm-mobile` has six views: Home, Notification center, Lights, Water, Irrigation
and Wine. `/calm-mobile/notices` is the Notification Center. `/ha-safe` is the
stock diagnostic dashboard. Local modules implement notices, scrollbar/view
recovery, radon, presence timeline and Wine disclosure; seven community-card
directories are present. Check served resources and live presentation rather
than assuming a local frontend edit is visible. See the [chart audit](dashboard-chart-audit.md).

For a notice, follow the entire chain: timeline item → due/action-window logic →
durable helpers → sender/delivery wrapper → completion/snooze actions → card.
The user-visible entry and scheduled push are separate outputs. A helper toggle
with `initial: true` can reset on restart; a removed sender can leave an unavailable
registry entity. Neither is sufficient proof of the desired product outcome.

Upcoming uses the actual deadline within its horizon; Needs Attention uses the
action window and can overlap Upcoming. Completion must clear only the intended
cycle. The current [project notification rule](../AGENTS.md#notification-style)
controls over older due-today-only wording in the detail-surface guide. Keep
routine completion receipts out of Recent by default. Use durable timestamps
or cycle IDs and verify uninitialized/unavailable helper states.

## Access and execution

| Route | Supported use | Boundary |
| --- | --- | --- |
| Native `homeassistant` MCP | Exposed entity states and supported device actions | Unexposed/match-failed is not evidence that the entity does not exist. Not a complete config or registry interface |
| `homeassistant_admin` MCP | Health, automation discovery, retained traces, bounded logs, allowlisted live files/hashes, config check, deployment prepare/apply/rollback | No arbitrary service/device caller, shell/API proxy, Core restart, secrets or `.storage` access |
| Documented admin bridge CLI | Same admin operations via [bridge](../tools/ha_admin_mcp.py) when the supported local context lacks direct registration | Same capability/SSH boundaries; not a separate Codex CLI session or a way around a denied operation |
| Connected desktop HA | Visual QA and normal UI operations outside MCP coverage | Use authenticated, connected HA. Browser deployment requires the specific File Editor ingress procedure, not an ordinary dashboard |

The [admin guide](home-assistant-admin-mcp.md) owns setup and exact tool details.
Transport is Mac stdio MCP → pinned, dedicated SSH → Terminal & SSH → local Unix
socket → repo-owned admin add-on → Core/Supervisor and allowlisted files.
Keep keys, host pin and private diagnostics outside Git; never disable verification.

On October 23 the existing local HA project chat **MCP startup** had working
native and admin tools. The Dot delegated executor did not expose them directly.
Check the current context's tool catalog and reuse the established capable HA
context when authorized; a tool registered elsewhere is not automatically loaded
here. Report the exact missing capability promptly instead of making the user
repeat authorization or revisit a Full Access setting already enabled.

Today's separate nested Codex CLI inherited `approval_policy=never`, which blocked
its prerequisite; it made no HA mutation. That failure did not establish bad HA
credentials or an outage. Native automation/helper attempts then failed because
the targets were unexposed. Do not confuse those failures, broaden exposure or
permissions as a workaround, or retry a denied operation without a permitted
material change. Full Access in one chat does not retrofit another process.

## Change, validate, recover

Follow the [deployment runbook](home-assistant-deploy-runbook.md); this is its
navigation summary, not a second deployment implementation:

1. Read live files and hashes. Preserve unrelated live changes and respect live
   include structure; never replace an entire file from a stale checkout.
2. Prepare a minimal local diff. Parse YAML and run relevant behavioral checks.
   For entity changes, update inventory and run
   `python3 tools/check_device_inventory_coverage.py`. For Recorder/history
   assumptions, regenerate Recorder inventory and disclose absent database evidence.
3. `ha_admin_deploy_prepare` uses expected live SHA256 values; inspect its diff.
   Plans expire after one hour. Apply only the reviewed plan and needed reloads.
4. Supported admin reload domains are `automation`, `script`, `template`, `scene`
   and `group`. Other helpers can need their normal UI reload; restart-only changes
   require their own plan. No automatic Core restart.
5. Verify content readback, config validity, loaded state and actual presentation
   or behavior. Treat reload timeout as uncertain; inspect before retrying.
6. Record deployment IDs and checks. The helper journals originals, checks writes
   and validity, and restores on failure; guarded rollback refuses unknown drift.
   Inspect `recovery_required` before further deployment. Commit only relevant files.

For browser deployment, verify connected HA and mounted `/api/hassio_ingress/`
File Editor. The helper must not run from a dashboard. Use the runbook through
currently supported browser tools; a documented snippet does not override tool
limitations. Prefer exact readback over repeatedly changing values when UI looks stale.

Focused tests exist for inventory, admin recovery, remote health, irrigation and
generator notifications; Wine has a separate policy checker. Pick checks for the
change. Never trigger real devices or send real alerts merely to test connectivity.

## Coverage and open gaps — October 23, 2026

The review inspected principal YAML structure, all automation groups, script/helper
counts, dashboard structure, tool/extension metadata and existing docs. YAML
structure parsed successfully; this review did not run a new HA validation or
health-test every integration. Read-only admin checks were performed in the local
HA chat. No live configuration, permissions, integrations or credentials changed.

Live health reported Core/API **2026.9.2**, config access available and no pending
recovery. Automation discovery returned **209 entities: 182 on, 27 unavailable,
zero off**. Unavailable includes deliberately unloaded registry remnants; it is
not a count of 27 proven faults. Live YAML has **182 definitions** versus **183**
in the repo; `downstairs_climate_sensor_spread_watch` is repo-only, with no live-only
IDs. It was not deployed or deleted during this review.

| Exact divergent file | Observation and practical implication |
| --- | --- |
| `configuration.yaml` | Different hash. Owns global settings, helpers, templates, Recorder and include wiring. Compare the affected section and dependencies; replacing the whole file could overwrite unrelated live behavior |
| `automations.yaml` | Live monolithic list versus repo include pointer/five chunks, plus the one-definition difference above. Matching IDs do not establish matching triggers/actions. Preserve the live layout for scoped edits unless a migration is separately authorized |
| `scripts.yaml` | Different hash. Contains shared lighting actions, notification delivery and reminder actions. Compare the edited script and its callers/helpers; no specific behavioral difference has yet been established |
| `lights.yaml` | Different hash. Defines light groups; bytes alone do not establish a membership change. Check the relevant group and callers before changing shared lighting actions |
| `dashboards/calm_mobile.yaml` | Different hash. Owns primary UI presentation and controls. Compare the affected view/card/resources and verify the served UI; this mismatch does not establish an automation defect |

`scenes.yaml`, `sensors.yaml`, `dashboards/ha_safe.yaml` and
`www/house-notices-card.js` matched byte-for-byte. These comparisons establish file
divergence and the stated automation layout/ID difference, not all semantic
differences, which copy is correct, or that a discrepancy is a fault.

### UI-managed inventory and dependencies

A same-day follow-up inspected the authenticated desktop HA Settings UI. This
closes the inventory/navigation gap without reading raw `.storage` or credential
values. Detailed observations and all 40 integration names are in the
[review evidence](audit-history/2026-10-23-project-operations-review.md#desktop-registry-follow-up).

| Live UI source | Verified coverage and ownership |
| --- | --- |
| Devices & services → Integrations (`/config/integrations/dashboard`) | 40 configured integration families. Showing disabled integrations returned “No disabled integrations.” Discovered cards are separate from configured entries. Spotify, UPnP/IGD and Zigbee Home Automation displayed “Failed setup, will retry”; no diagnosis or repair performed |
| Devices (`/config/devices/dashboard`) | 281 displayed device records, with area, integration, manufacturer/model and battery columns. This includes service/network records, not 281 distinct physical appliances |
| Entities (`/config/entities`) | 2,802 with the status filter cleared; 2,268 with the original Enabled filter, restored afterward. Device, area, integration and status columns establish the lookup path. Registered/enabled does not mean available or MCP-exposed |
| Helpers (`/config/helpers`) | 423 displayed items with entity ID, type and editability columns. Includes templates and other helper types, so it is not comparable to the repo's 198 `input_*` definitions. Check the item's owner before editing |
| Areas and labels (`/config/areas/dashboard`, `/config/labels`) | 33 areas; Main Floor and Second Floor plus unassigned “Other areas.” Labels page reported no labels. Device/area assignments are registry metadata, independent of YAML logic |
| Dashboards (`/config/lovelace/dashboards`) | Nine rows: six built-in UI-controlled dashboards, YAML Home and HA Safe, and a user-created UI-controlled Overview. The latter is outside the two repo dashboard files |
| Resources (`/config/lovelace/resources`) | 13 JavaScript module registrations: seven HACS cards, five local modules and Browser Mod. Browser Mod URL carries `3.2.0`; repo manifest says `2.7.3`. A registration/version string does not prove runtime loading or compatibility |
| Apps (`/config/apps/installed`) | Codex HA Admin, Terminal & SSH, File editor and Matter Server. Admin transport depends on the first two; File editor supports browser deployment; Matter Server is the adjacent Matter service |

Configured integration cards may contain multiple entries. Inventory scope is the
UI-visible category list, registry totals/columns and ownership paths, not an
export of every entity or every integration option. No login or permission block
occurred. Native MCP remains exposure-limited; admin MCP has no registry/config-entry
reader. The desktop UI supplies these views. Credential ownership, full option
payloads and per-device health were neither required nor inspected. UI-controlled
Overview contents were not audited; its existence and ownership were verified.

### Home Connect developer-account dependency

The live integration search for “Home Connect” returned **No integrations found**;
the disabled list was also empty, and bounded repo searches found no implementation.
An active HA dependency on the Ames developer account is therefore **not established**.

Official [HA setup documentation](https://www.home-assistant.io/integrations/home_connect/)
requires a developer application and HA Application Credential, followed by separate
appliance-owner authorization. [Home Connect authorization](https://api-docs.home-connect.com/authorization/)
uses access/refresh tokens; a developer-portal login session is not the runtime API
path. Account/application linkage cannot be verified without an existing entry
and appropriate account evidence; no credentials were opened.

The parent-held Developer Team notice reports an **October 26–November 26, 2026**
developer-account migration window, followed by temporary developer-account access
loss. Preserve that owner-assisted account task using the
[official portal](https://developer.home-connect.com/user/login); no migration or
account changes were performed here. The dates come from that notice, not an
independent public confirmation. Do not infer appliance, mobile-app, API or token-
refresh outage from developer-portal access loss. See the review evidence for provenance.

Three priorities for future work, with no remediation performed here:

- **Reconcile at the point of change.** Repo/live drift makes whole-file deployment
  unsafe without comparison. Desktop registry metadata is now verified above;
  integration options, UI-controlled dashboard contents and every entity's runtime
  behavior remain task-specific checks. Credentials and authentication storage were
  intentionally excluded. This is not permission expansion or a claim that every
  HA setting has been inspected.
- **Plan decomposition separately.** Main YAML is 445,929 bytes, above the project's
  approximately 300 KB reliability threshold; the primary dashboard is 560,810 bytes.
  The main template block dominates the file. Record the reliability concern without
  turning a scoped feature request into an unapproved structural migration.
- **Treat inventories as dated evidence.** Current inventory JSON reports 237 devices,
  2,610 entities, 45 platform categories and 35 entity domains, based on July 29 with
  targeted later reconciliation. Detail Markdown still says 231/2,539, overview role
  subtotals lag JSON, and the upgrade backlog uses 114/962. Recorder inventory lacks
  database row/frequency measurements. None is a fresh whole-system census.

## Verified workflow from today's notification changes

The [fertilizer audit](audit-history/2026-10-23-fertilizer-notification-removal.md)
records removal of the Notification Center item and its exclusive sender through
reviewed admin deployment, preserving unrelated alerts, irrigation and historical
helpers/actions. Safari verified the entry absent. A generic automation toggle
would not have satisfied the user's corrected request.

The [garden planning audit](audit-history/2026-10-23-garden-planning-notice.md)
records **Plan next season's garden — Apr 9, 2027** in HA Upcoming, one-time push
and durable completion, with admin readback, config checks and desktop verification.
The existing 365-day horizon already included it. A separate Dot reminder was the
wrong destination for this request; its cleanup is owned by the originating task,
not established by this repository review. No annual/fertilizer reactivation was added.

These results establish the process: identify the user's surface, use the capable
existing context, inspect ownership, make the scoped change with recovery, and
read back the user-visible outcome. Keep dated evidence in the audits rather than
copying implementation details into multiple runbooks.

### October 26 main-floor spread reconciliation

The previously repo-only `downstairs_climate_sensor_spread_watch` and dedicated
spread templates have now been removed from the repository. Live configuration
and loaded state already lacked this feature. Trevor explicitly does not want
Kitchen–Dining Room spread monitoring or notifications recreated. See
[retirement evidence](audit-history/2026-10-26-main-floor-spread-retirement.md).
The October 23 divergence figures above remain dated historical observations.

### October 31 disagreement correction

The separate Dining Room SensorPush/Ecobee temperature and humidity comparison
alerts are now retired live and in the repository. Both main-floor comparison
features must remain retired; ordinary climate/safety alerts remain enabled.
See [corrective deployment](audit-history/2026-10-31-dining-disagreement-retirement.md).
