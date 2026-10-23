# Project operations review

Trevor requested project-wide understanding after the garden notification work,
including documents, configuration and a practical guide for future HA requests.

The maintained result is the [Home Assistant operations map](../home-assistant-operations-map.md).
It indexes the configuration layers, feature owners, integrations, dashboards,
helpers, notifications, tooling, validation, deployment, recovery and access routes.
Existing runbooks remain authoritative; no second deployment procedure was created.

Evidence combined read-only repository structure/YAML analysis, current project
instructions and audit history, plus direct admin MCP health, automation discovery
and nine allowlisted live file reads in the established local HA project chat.
No secrets, authentication storage, private logs or backups were inspected.

The highest-impact findings are repository/live drift, incomplete visibility of
UI-managed configuration, an oversized main YAML file and stale inventory views.
The map records exact coverage and dated counts rather than declaring the repo a
complete live mirror. These findings did not authorize configuration refactoring,
integration changes, permission expansion or inventory reconstruction.

Documentation changes: added the map and its project entrypoint; corrected the
entrypoint's missing fifth automation chunk; recorded the final originating-agent
Safari check in today's garden-planning audit. No live changes or reloads occurred
in this review. Today's earlier notification deployments retain their own audits
and recovery IDs.

Validation: principal YAML structure parsed for inventory/counting; new/changed
documentation links and saved content checked; focused Git diff whitespace checks.
No new runtime tests or pushes were needed for this documentation-only change.

Residual gaps and next steps are in the map's dated coverage section. Future edits
must reconcile the affected live files and check the relevant runtime/UI behavior.

## Desktop registry follow-up

The parent requested the remaining UI-managed inventory/ownership coverage and
exact implications of five divergent files. Same-day inspection used the existing
authenticated Safari HA UI, through Settings. The current delegated tool catalog
still exposed no native/admin HA tools; the established admin bridge has no
registry or config-entry reader. Desktop access worked without login, permission
changes or a denied action. No raw `.storage`, account credentials, integration
configuration payloads or precise zone locations were read.

Observed sources and results:

- `/config/integrations/dashboard`: 40 distinct configured integration families,
  collected across the list and search views. The explicit Show disabled
  integrations view said “No disabled integrations.” Discovery offers are not
  configured entries. Filter searches can narrow the device/entry counts inside
  a card; those filtered counts were not used as inventory totals.
- `/config/devices/dashboard`: search placeholder reported 281 device records;
  columns expose area, integration, manufacturer/model and battery.
- `/config/entities`: original Enabled status filter reported 2,268; temporarily
  clearing it reported 2,802. Original filter was restored. Columns include
  device, area, integration and status; counts include registry entries rather
  than guaranteeing functioning or exposed entities.
- `/config/helpers`: 423 items; columns include entity ID, type and editability.
  Templates appeared alongside input helpers, explaining why this is a broader
  category than the local `input_*` count.
- `/config/areas/dashboard`: 33 area links, organized under Main Floor, Second
  Floor and Other areas. `/config/labels` reported no labels.
- `/config/lovelace/dashboards`: six built-in UI-controlled rows (Overview,
  Lights, Security, Climate, Energy, Maintenance); two user-created YAML rows
  (Home → `dashboards/calm_mobile.yaml`, HA Safe → `dashboards/ha_safe.yaml`);
  one user-created UI-controlled Overview. Contents of that Overview were not audited.
- `/config/lovelace/resources`: 13 JavaScript module registrations: Browser Mod,
  ApexCharts, button-card, custom-sonos-card, card-mod, Mushroom, mini-graph-card,
  mini-media-player, plus all five local modules. Browser Mod resource query
  carries version `3.2.0`, while the repository manifest is `2.7.3`; no running
  integration version or compatibility conclusion follows from this alone.
- `/config/apps/installed`: Codex HA Admin, File editor, Matter Server, Terminal
  & SSH. No app configuration, update, restart or runtime-control action taken.

Configured families (category inventory, not number of config entries): Airthings;
Anthropic; Apple TV; Backup; Brother Printer; Browser mod; Command Line; ESPHome;
Flo; Generac MobileLink; Google Cast; Google Translate text-to-speech; HACS; Home
Assistant Supervisor; HomeKit Bridge; HomeKit Device; Hunter Hydrawise; LG ThinQ;
Lutron Caséta; Matter; Meteorologisk institutt (Met.no); Mobile App; Model Context
Protocol Server; OpenAI; Radio Browser; Ring; Samsung Smart TV; SensorPush Cloud;
Shell Command; Shopping list; Sonos; Spotify; Sun; Tesla Wall Connector; TP-Link
Smart Home; UniFi Network; UniFi Protect; UPnP/IGD; Whisker Ting; Zigbee Home Automation.

Spotify, UPnP/IGD and Zigbee Home Automation displayed “Failed setup, will retry.”
This is observed setup status, not a root-cause diagnosis or permission to repair.
No other integration's health was certified by being listed. Display filters were
restored and Safari returned to Notification Center, still showing Upcoming 18.

The operations map now enumerates all five divergent files individually:
`configuration.yaml`, `automations.yaml`, `scripts.yaml`, `lights.yaml`, and
`dashboards/calm_mobile.yaml`. Implications concern ownership, callers and safe
comparison, without claiming uninspected semantic differences or reconciling files.

### Home Connect notice and dependency

Parent-supplied evidence: Home Connect Developer Team notice to the Ames account,
source email `1a1686f44dd50764`, reports developer-account migration opening October
26 and closing November 26, 2026, followed by temporary developer-account access
loss. The parent holds the original email; this review did not retrieve it or
independently confirm those dates publicly.

Live Integration search “Home Connect” returned “No integrations found”; showing
disabled integrations reported none. Bounded searches of repo configuration,
dashboards, docs, integrations, tools and tests also found no Home Connect reference.
This establishes no configured HA entry was found, not the status of a developer
application, unfinished setup, external appliance account or another system.

[Official HA setup](https://www.home-assistant.io/integrations/home_connect/)
requires developer-account application registration, client ID/secret as an HA
Application Credential, and separate Home Connect appliance-owner authorization.
The developer portal should be logged out before the appliance authorization step.
[Official authorization documentation](https://api-docs.home-connect.com/authorization/)
describes access tokens and refresh tokens; the
[developer FAQ](https://developer.home-connect.com/support/faq) covers application
administration. An active HA dependency on this particular developer account
cannot be established from the observed configuration.

The notice is an owner-assisted developer-account task for the reported window,
using the [official portal](https://developer.home-connect.com/user/login).
No migration, sign-in, account change, credential inspection or reminder was
performed. Developer-portal access loss could limit application administration;
the sources do not establish loss of existing API refresh, app or appliance
operation. Do not conflate this developer notice with separate appliance-user
SingleKey ID migration guidance.

Follow-up verification: saved two existing documents, checked their local link
targets and focused Git diff; no live configuration validation/reload was needed.
Coverage is established for inventories and routing. Remaining limits are full
config-entry options/credential linkage, UI Overview contents and per-entity
runtime health, not an unresolved permission request.
