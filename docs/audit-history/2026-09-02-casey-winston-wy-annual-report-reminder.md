# Casey Winston Wyoming Annual Report Reminder

## Symptom And User Impact

Casey Winston LLC needed the same calm, durable annual business-administration
reminder pattern already used for Bonticou LLC's Delaware franchise tax. The
first open cycle is due January 1, 2027, and includes a $60.00 Wyoming license
tax.

## Relevant Prior Context

- Bonticou's Delaware tax reminder established the notification, dashboard,
  detail-sheet, action-stamp, and annual-cycle pattern.
- The 2026 Casey Winston LLC Wyoming report was confirmed paid. The new logic
  therefore starts at the January 1, 2027 cycle and does not create a false
  overdue item for 2026.
- Notification Center separates the real deadline from the action window and
  clears only the cycle explicitly marked paid.

## Evidence Collected

- The Wyoming Secretary of State's official annual-report portal is
  `https://wyobiz.wyo.gov/Business/AnnualReport.aspx`.
- The user supplied the January 1 annual deadline and $60.00 license-tax amount
  for Casey Winston LLC.
- The existing shared `input_boolean.business_admin_reminders_enabled` control
  is the appropriate enablement boundary.

## Ranked Findings

1. High confidence: the 2027 due date must remain visible in Upcoming before
   the reminder window opens.
2. High confidence: the action window should begin December 1, 2026, while the
   timeline continues to show the real January 1, 2027 deadline.
3. High confidence: the Paid action must stamp the due year, not `now().year`,
   because filing may occur in December of the preceding calendar year.
4. High confidence: startup and automation reloads need a durable daily send
   guard so they cannot duplicate a push already delivered that day.

## Changes Made

- Added due-date, status, and due binary sensors for Casey Winston LLC.
- Added durable paid-cycle, last-paid, and last-notified helpers.
- Added opening and final-business-day push reminders with a concise
  `🏔️🧾` title, a Paid quick action, and the official Wyoming filing page.
- Added a Notification Center item with a bespoke detail surface, the $60.00
  amount, the December 1 reminder-opening date, and cycle-specific completion.
- Added action-stamp logging and automatic advancement to the next January 1
  cycle after payment.
- Reconciled the new entities into the repository device inventory.

## Checks Run

- Local YAML parsing passed for `configuration.yaml`, `scripts.yaml`, and
  `automations/30-maintenance-environment.yaml`.
- `jq empty docs/device-inventory.json` passed.
- `python3 tools/check_device_inventory_coverage.py` still reports the existing
  false-positive references `light.state` and `light.last_changed` from a
  Jinja loop in `automations/10-lighting-security.yaml`; the Wyoming reminder
  introduced no missing control-entity references.
- `git diff --check` passed.

## Deployment Status

- Pending live deployment. The Remote UI File Editor mounted successfully, but
  the current browser-control surface could not execute the repository's
  verified deploy payload or open its upload chooser. No live files were
  written, and no reload was attempted.

## Residual Risks And Next Follow-Ups

- Verify the live due-date sensor resolves to `2027-01-01` and the Notification
  Center shows the item in Upcoming after template reload.
- Verify the first push sends once on or after December 1, 2026, then stamps the
  last-notified helper.
