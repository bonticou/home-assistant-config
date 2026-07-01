# Notification Center Due Boundaries And Parking Pass Cycle

## Symptom And Impact

Trevor reported that Notification Center's Needs Attention section showed items
that were not due yet. During the same flow, the newly renewed NWP parking pass
also disappeared from the reminder timeline after being marked replaced for one
month.

## Relevant Prior Context

- Notification Center should separate timeline due dates from reminder/action
  windows.
- The NWP parking pass replacement action had just been added with 1-month and
  3-month options, and the July 1, 2026 1-month renewal should roll the next
  pass expiration to July 31, 2026.
- Earlier notification reminder work established that Upcoming can show future
  due dates, while Needs Attention should feel like the current action queue.

## Evidence Collected

- Live `sensor.house_notice_timeline` contained future-dated `due` rows, most
  visibly garbage pickup on July 2, 2026.
- Garden fertilizer and dehumidifier air filter rows were flagged due by their
  binary sensors, but their timeline dates were using the next scheduled Friday
  rather than the missed active cycle.
- `input_datetime.nwp_parking_pass_expiration_date` briefly reverted to
  `2026-06-30` after reload because the YAML helper still had a stale `initial`
  value.
- After repair, live parking pass state showed:
  - expiration `2026-07-31`;
  - reminder opens `2026-07-30`;
  - status `Expires Jul 31, 2026`;
  - due sensor `off`;
  - timeline item `nwp-parking-pass-2026-07-31` as `upcoming`.

## Ranked Findings

1. High confidence: Needs Attention filtering was too broad. The card treated
   any `state: due` item as Needs Attention even when its visible due date was
   in the future.
2. High confidence: the parking pass cycle guard was not durable enough. It
   inferred replacement from `replaced_at` relative to the current reminder-open
   date, which could hide the newly advanced cycle.
3. High confidence: `nwp_parking_pass_expiration_date` should not have a YAML
   `initial` value because the live helper state is the durable source of truth.
4. Medium confidence: the reminder summary count should be date-aware and
   should include bespoke due-today rows such as the wine cave serial number.

## Changes Made

- Added `input_text.nwp_parking_pass_replaced_expiration_date` to stamp the
  exact parking-pass expiration cycle that was handled.
- Updated the NWP parking pass script to stamp the handled expiration while
  advancing the live expiration helper.
- Removed the stale YAML `initial` value from the parking pass expiration
  helper.
- Updated NWP pass status, due sensor, and timeline item suppression to compare
  against the handled expiration cycle instead of only the replacement date.
- Updated the custom Notification Center card so future-dated `due` rows remain
  out of Needs Attention and expose no completion actions until their visible
  date is today or overdue.
- Changed garden fertilizer and dehumidifier timeline dates to show the active
  missed cycle while their due sensors are on.
- Updated the timeline state and `attention_count` to use the same due-date
  boundary and count wine cave serial capture when it is open.
- Bumped the `house-notices-card.js` Lovelace resource cache version.
- Updated Notification Center detail-surface guidance to document the stricter
  Needs Attention boundary.

## Checks And Live Validation

- Local YAML parsing passed for:
  - `configuration.yaml`;
  - `scripts.yaml`;
  - `dashboards/calm_mobile.yaml`.
- `node --check www/house-notices-card.js` passed.
- `git diff --check` passed.
- Live File Editor deployment wrote and read back:
  - `/homeassistant/configuration.yaml`;
  - `/homeassistant/scripts.yaml`;
  - `/homeassistant/www/house-notices-card.js`.
- Live Home Assistant config check returned valid with no errors or warnings.
- `input_text.reload`, `template.reload`, and `script.reload` returned HTTP
  200. `lovelace.reload` returned HTTP 400, matching the known unsupported
  service behavior on this instance; the Lovelace resource URL was cache-busted.
- Live state repair restored:
  - `input_datetime.nwp_parking_pass_expiration_date` = `2026-07-31`;
  - `input_text.nwp_parking_pass_replaced_expiration_date` = `2026-06-30`.
- Live API read after deployment showed:
  - `sensor.house_notice_timeline` = `3 need attention`;
  - `attention_count` = `3`;
  - Needs Attention rows:
    - Fertilizer time, `2026-06-19`;
    - Clean dehumidifier air filter, `2026-06-26`;
    - Wine cave serial number, `2026-07-01`;
  - Garbage + paper recycling, `2026-07-02`, was suppressed from Needs
    Attention as a future-dated row.

## Deployment Status

- Deployed live and validated on July 1, 2026.

## Residual Risks And Next Follow-Ups

- Phones may need the cache-busted Lovelace resource to load before the card
  rendering change appears visually.
- The due sensors can still open push/action windows before the visible due
  date; the card now filters those future rows out of Needs Attention.
