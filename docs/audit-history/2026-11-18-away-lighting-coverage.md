# Away-light detection and one-tap shutoff

**Deployed November 18 at 6:22–6:23 PM EST.** Away detection and its explicit
shutoff now share 42 verified physical lighting endpoints, including upstairs,
foyer, front stairs and nine lighting switches. Live readback confirms the new
inventory is ready and all current household light entities are covered. The
physical shutoff was deliberately not exercised; no blackout or test push.

## Owner decision and incident evidence

Trevor authorized implementation and deployment through Eames under
`HA-AWAY-LIGHTS-COVERAGE-20261118`, superseding the preceding read-only diagnosis.
He requires all actual household lighting in both away detection and one-tap
shutoff, with future new-light work verifying both paths automatically. Existing
arrival/Evening eligibility and notification presence, timing and recipients
must remain unchanged. This explicit scope supersedes earlier alert-list
exclusions for scheduled, Wynn and vacation lights; it does not change those
lights' independent schedules or scenes.

The preceding `HA-ALL-OFF-NOTIFICATION-20261118` investigation found:

- At **5:40:45.857 PM EST**, action `TURN_OFF_AWAY_LIGHTS` reached the deployed
  handler (trace `e74c004c56ae9f7ec26d3ba5ef66e9c7`). Its 18 individual off calls
  included upstairs hallway, back stairs and foyer ceiling. It did not invoke
  household All Off or set its holds. It completed without a recorded service
  error, which does not prove physical convergence.
- The old active-light sensor intentionally excluded scheduled foyer chandelier
  and front stairs and omitted several actual lighting switches. This was a
  verified coverage mismatch with the requested whole-house action.
- Evening subsequently issued on commands at **5:42:19 PM**, trace
  `4973556c49cc5574828c3d9b9013ae01`, context
  `01M7RD6GEGR2RM60EPB2480DFN`, with explicit null parent/user. Its originating
  caller remains unproven. The known Trevor-arrival run was **5:40:20 PM**, before
  the tap. Do not attribute the later invocation to arrival or manual use from
  missing context. No fix to arrival behavior follows from that uncertainty.

Historical physical off/on transitions and the second invocation's originating
service-call record were unavailable through retained traces. Bounded logs did
not show a target-command failure; this does not establish no failure occurred.

## Implementation and coverage

- `helpers/household_lighting.yaml` owns one ID/label mapping. The existing
  `sensor.away_security_active_lights` and the explicit action both consume it.
  The old large selector was removed from `configuration.yaml` and replaced
  with a focused template include. Unknown/unavailable members are separate
  attributes, not counted as on or silently treated as off.
- Coverage: **33 physical lights + nine switches**. The switches are exterior
  mudroom stairs, Family Room Uplight, Flower Lamp, foyer sconces, garage lights,
  Master door lantern, Office Uplights, Uplight 1 and Uplight 2. The door lantern
  is distinct from the bedroom lantern. All three uplight devices remain
  distinct. Six YAML light-group aliases and the Great Room switch alias are
  represented by their physical members once each. Three UniFi equipment LEDs,
  appliance plugs, valves, security controls and settings switches are excluded.
- Trusted Lutron `light.*` physical endpoints are included automatically;
  arbitrary switches and other integrations require explicit verified onboarding.
  The checklist requires persisting newly discovered IDs in the mapping so a
  later disappearance remains unknown rather than being forgotten.
- `away_lights_turn_off_verified` snapshots that mapping, issues isolated off
  commands only to currently-on targets, waits three seconds, retries still-on
  targets once, then waits three more seconds and records remaining/unverified
  members. Every target failure is isolated. An empty/unavailable inventory
  fails closed. No blanket scene/arrival hold is added.
- Both light-only tokens and the existing Secure-home lighting step use this
  helper. Locks/garage operations and their conditions are unchanged. Light-only
  clearing is conditional on the verified result; failures use a separate
  `away-lights-result` tag so routine away/Casey clearing cannot erase them.
  There is no routine success push. Ordinary all-off acceptance is never the
  success criterion. A subsequent scheduled light-on remains possible.
- All three away-light alert presentations disclose unverified lights. The
  light button says **Turn all lights off**. Existing contextual clear rules now
  react to the shared sensor, including lighting-switch changes; their daylight
  and presence conditions are unchanged.

## Checks and independent review

- Seven focused tests render production templates and simulate selection,
  automatic new Lutron inclusion, group/equipment exclusions, unknown states,
  per-target failure, bounded retry, late relighting and missing inventory.
- Seven existing Evening/manual-override tests pass. Parsed local/live semantic
  comparisons prove arrival/Evening, main All Off, reminder gates and unrelated
  lock/garage branches unchanged. Independent review confirmed coverage, tests
  and durable guidance before application. Serializer wrapping causes extra
  textual churn inside the three modified senders/action blocks; semantic
  comparison isolates the actual changes.
- YAML parses; inventory checker passes **181 active control references**.
  Recorder inventory generator ran: policy unchanged, no DB copy available,
  JSON refresh timestamp only and Markdown unchanged. No Recorder cleanup.
- Fresh deployed files were reconciled. Live-only `ting_send_notification`
  differences were preserved, not overwritten by the repository copy. Live
  automations remain monolithic; repository automations remain split.

## Deployment, backup and rollback

Reviewed plan/deployment **`8715aa308e0b43b8ab102406f7e11669`**. The admin helper
validated the existing configuration, journaled/backed up originals, wrote and
verified the four files, validated the resulting configuration and completed
**template, script and automation reloads**. No Core restart. The prepared script
diff exceeded the tool display limit; complete local candidate semantics and
hashes were reviewed independently before application.

All four fresh live hashes match the reviewed candidates:

| File | SHA-256 |
| --- | --- |
| configuration.yaml | `5a2811569e34f51631bf8bd3715769c11404afe4a791fc5e36bf75667b963384` |
| scripts.yaml | `291367be94d243ac565d1462b6f2c237f284b2ec27db63a87e9282bf73945ac8` |
| automations.yaml | `6b127b2849297368d388e5470b44c130c7fb3fa24548fba6dfd5158eb7d1a620` |
| helpers/household_lighting.yaml | `40a8c71fc7ede1c233f768edd72d5a18a076ec1871d00244a98c4c45ae922dcf` |

Rollback is the existing admin `deploy_rollback` for that deployment ID with
the same reload domains, after reviewing current drift. It restores the
journaled originals and removes the newly created helper. No rollback needed.

## Live verification and remaining limits

MCP handles configuration/health/deployment. Native MCP lacks full inventory
attributes, so an already authenticated **local** HA browser session rendered
read-only templates; no credentials or permissions changed. Before reload:
33 physical lights, 30 Lutron light entities, Trevor home, Casey away, Evening
current and no scripts executing. After reload:

- inventory `ready`, **42** targets;
- direct physical-light comparison: **missing_physical=[]**;
- inventory-derived on count **18**, identical to the active-light sensor;
- foyer chandelier, front stairs, upstairs hallway and foyer sconces explicitly
  present and counted while on;
- unavailable: `switch.flower_lamp`, `switch.master_lantern`, `switch.uplight`;
- both new scripts loaded and idle; action handler enabled;
- Evening last run remains **5:42:19 PM**. Reload trace
  `317639d31bc0d80b4a54c3122fc88443` at **6:22:52.972 PM** stops at eligibility
  condition 9; a template-reload schedule transition also stopped before action.

**Away detection verified live. One-tap shutoff coverage/wiring verified by live
file/entity readback and offline failure-mode simulation. Physical shutoff is
untested by instruction**, and the three unavailable devices cannot be confirmed
off. No light/scene/action execution, test notification, new schedule, security
setting or unrelated repair was performed.

## Durable onboarding guidance

The canonical [lighting onboarding checklist](../lighting-onboarding.md) is
required by the [actual MCP workflow guide](../home-assistant-admin-mcp.md) and
linked from the [operations map](../home-assistant-operations-map.md). Existing
AGENTS.md MCP-first instructions already require that guide, making the rule
discoverable without modifying unrelated working-tree AGENTS edits. All three
locations were read back. Future new-light work must report verification of
both detection and one-tap action coverage, or a precise blocker.
