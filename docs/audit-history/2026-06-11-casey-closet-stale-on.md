# Casey Closet Stale-On Recurrence

## Symptom And Impact

Trevor reported that Casey's closet light stayed on yesterday and today without
turning itself off. The expected behavior is that the closet light should never
sit on unattended.

## Relevant Prior Context

- `2026-06-04-home-assistant-availability-ui-and-casey-closet.md` added the
  current Casey closet automation and a stale-on safety net.
- `2026-06-05-casey-closet-missed-motion.md` and
  `2026-06-06-ssd-data-disk-and-casey-closet.md` found that the UniFi Protect
  motion entity and Home Assistant availability had both been sources of missed
  behavior.
- The controlling automation is
  `automation.lights_casey_s_closet_auto_off`.
- The light is `light.master_casey_s_closet`.
- The motion entity is `binary_sensor.casey_s_closet_motion`.

## Evidence Collected

- The repository automation already covered the normal case:
  motion turns the light on, and a template trigger turns it off after three
  minutes when the light is on and the motion entity is not `on`.
- That rule does not cover a stale or stuck `on` motion entity, a missed quiet
  transition, a restart/reload while the light was already on, or an already-on
  state whose three-minute quiet trigger never fired.
- Current Safari/Home Assistant auth was not available during this pass, so no
  live history readback was captured before the YAML fix.

## Ranked Findings

1. High confidence: the prior three-minute quiet rule was not enough to
   guarantee eventual shutoff if the motion sensor stayed `on` or HA missed the
   quiet transition.
2. Medium confidence: the two reported stale-on events were caused by one of
   the uncovered stale-motion/restart/already-on paths rather than the normal
   quiet-off branch.
3. Medium confidence: a hard maximum runtime is appropriate for a closet light,
   even if it occasionally turns off during an unusually long closet visit.

## Changes Made

- Updated `automations/10-lighting-security.yaml`.
- Kept the existing motion-on and three-minute quiet-off behavior.
- Added Home Assistant start, automation reload, five-minute watchdog, and
  twelve-minute light-on hard-cap triggers.
- Added a hard-cap branch that turns off `light.master_casey_s_closet` whenever
  it has been on for at least twelve minutes, regardless of the motion entity's
  current state.

## Checks And Live Validation

- Local YAML parsing passed for `automations/10-lighting-security.yaml`.
- `git diff --check` passed for the automation and audit entry.
- Live deployment was not completed in this pass because the local Safari
  Home Assistant session had no usable auth token and the File Editor ingress
  iframe was not mounted.

## Deployment Status

- The YAML fix is ready to deploy once an authenticated Home Assistant File
  Editor or equivalent deployment path is available.

## Residual Risks And Next Follow-Ups

- Deploy the automation and reload automations live.
- After deployment, verify that the live automation config includes the
  twelve-minute hard-cap/watchdog branch.
- If the closet still misses motion or behaves oddly after this cap is live,
  inspect the UniFi Protect motion state history and consider adding a physical
  door/contact trigger.
