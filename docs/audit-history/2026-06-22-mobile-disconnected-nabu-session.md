# Mobile Disconnected With Nabu Route Reachable

Date: 2026-06-22

## Symptom And Impact

Trevor reported that the Home Assistant mobile app again showed a
"disconnected" state while away, shortly after it had been working. He expected
the app to be using the Nabu Casa Remote UI path.

## Relevant Prior Context

- `docs/home-assistant-mobile-disconnect-audit-2026-05-26.md`
- `docs/home-assistant-remote-access-runbook.md`
- `docs/home-assistant-ui-hardening-runbook.md`
- `docs/audit-history/2026-06-16-remote-ui-overnight-flapping.md`
- `docs/audit-history/2026-06-08-late-night-exterior-lighting-and-remote-ui-handoff.md`

Prior incidents often showed either Nabu Casa's fallback page, Remote UI sensor
dropouts, or local/remote handoff confusion. Those patterns remain relevant, but
this incident had a different current probe result.

## Evidence Collected

- Safari had a Home Assistant tab on the Nabu Casa Remote UI host, but it was
  parked on an `/auth/authorize` URL with a redirect back to
  `/calm-mobile/home`.
- The external Python health probe reached DNS and TCP but hit the previously
  documented Mac certificate-chain false positive, so that result was not used
  as the primary classification signal.
- A direct HTTPS fetch with certificate verification bypassed returned the Home
  Assistant frontend shell for `/calm-mobile/home`.
- A direct websocket upgrade to `/api/websocket` succeeded and returned Home
  Assistant's `auth_required` greeting.

## Findings

1. High confidence: at the moment of testing, the Nabu Casa route could reach
   Home Assistant.

   Evidence: Remote UI served the HA shell and the websocket upgraded far enough
   to get HA's unauthenticated greeting.

2. Medium-high confidence: the immediate phone-visible failure is more likely a
   client/session/auth handoff issue than a current Nabu tunnel outage.

   Evidence: Safari was on the auth handoff path rather than the Nabu fallback
   page, and the Remote UI websocket was reachable from the Mac.

3. Medium confidence: URL selection can still be part of the failure family.

   Evidence: the repo still does not define `homeassistant.external_url` or
   `homeassistant.internal_url`, so mobile path selection is mostly managed by
   the iOS companion app, HA Cloud, and network context rather than repo YAML.

## Changes Made

No Home Assistant configuration was changed in this pass.

## Checks Run

- Reviewed prior remote/mobile disconnect audits and runbooks.
- Probed the Nabu Casa shell path.
- Probed the Remote UI websocket path.

## Deployment Status

No deployment was needed.

## Residual Risks And Follow-Ups

- Inspect the iOS companion app server connection settings during the next
  recurrence: external URL/cloud path, internal URL, SSID matching, VPN/private
  relay/filtering, and frontend cache/session state.
- Build the previously recommended external monitor so Remote UI root,
  `/ha-safe/home`, `/calm-mobile/home`, and websocket reachability are recorded
  continuously from outside Home Assistant.
- Keep the Remote UI watchdog, but do not treat `cloud.remote_connect` as a full
  recovery guarantee.
