# EuroCave Identity Reconciliation

Date: 2026-07-20

## Symptom And User Impact

House Manager contains confirmed EuroCave model and serial evidence, but Home
Assistant's durable capture helper still defaulted to incomplete. That could
leave the Wine dashboard and Notification Center showing `Serial pending` even
though the appliance identity is complete.

## Relevant Prior Context

- House Manager's `eurocave-la-premiere-l-wine-cellar.md` records the
  `2026-05-09` rating-plate photo.
- A `2026-07-19` factory quality-control card independently corroborates the
  model, serial, manufacture date, and appliance ratings.
- The July 1 Notification Center audit recorded the wine-cave serial task as a
  live Needs Attention item.

## Evidence

- Confirmed model: `V-LAPREMIERE-L`.
- Confirmed serial: `1001571294`.
- Confirmed manufacture date: `2025-11`.
- `configuration.yaml` still set
  `input_boolean.wine_cave_rating_plate_captured` to an initial value of
  `false`.
- `sensor.wine_cave_appliance_context` linked the durable House Manager record
  but did not expose the confirmed identity fields or evidence paths.

## Ranked Findings

1. High confidence: the HA serial-capture state was stale relative to the
   durable House Manager evidence.
2. High confidence: the HA appliance-context sensor should expose the confirmed
   identity needed for future support and automation context.
3. Medium confidence: an already-restored live helper may remain off until its
   completion script is called even after the YAML default changes.

## Changes Made

- Changed the rating-plate-captured helper's default to `true`, with a comment
  identifying both corroborating sources.
- Added manufacturer, model, serial number, manufacture date, identity
  confidence, rating-plate path, and factory quality-control-card path to the
  Wine Cave Appliance Context sensor.

## Checks Run

- Ruby YAML parsing passed for `configuration.yaml`.
- `python3 tools/check_device_inventory_coverage.py` passed.
- `git diff --check` passed.

## Deployment Status

Pending. The Nabu Casa Remote UI was reachable, but the fresh in-app browser
session required authentication. A terminal deployment path that reads auth
material from a signed-in Safari session was not used without explicit approval.

## Residual Risks And Next Follow-Ups

- Deploy `configuration.yaml` through an authenticated File Editor ingress
  session with byte-for-byte read-back and a valid HA config check.
- Reload templates and call
  `script.wine_cave_mark_rating_plate_captured` so the restored live helper
  immediately becomes `on` and the stale notice clears.
- Verify the live appliance-context sensor exposes the confirmed model, serial,
  manufacture date, and identity confidence.
