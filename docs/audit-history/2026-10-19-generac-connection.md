# Generac MobileLink connection

## Request and evidence

User requested connecting the generator and developing appropriate notifications. Historical inventory and live integration/entity registry had no Generac entry. User confirmed it was online in Mobile Link and authorized using a shared login for HA setup.

## Changes

Installed binarydev/ha-generac from HACS. Configuration check passed before a required Core restart. Restart completed successfully and administrative MCP confirmed API/config access with no recovery required. Completed integration sign-in and named the device Generac Generator. HA displayed model G0072610, Ready to run, battery voltage, and clear warning/maintenance sensors.

Credentials were transferred through browser copy/paste without printing their values or writing a project copy. Declined Safari password saving, closed the shared-item tab, and replaced clipboard content. The integration retains its own authentication. No shared link, credentials, address, serial number, or raw logs are recorded here.

## Findings

The sensor set supports status, warnings, maintenance, and monitoring availability. The vendor last-seen timestamp was old despite Connected; avoid a short staleness threshold until its cadence is understood. No utility/transfer sensor or fuel-level sensor was exposed, so Running alone does not prove an outage or house transfer.

## Verification and status

Browser confirmed successful setup and live readings. Registered 26 entities; targeted device inventory updated and coverage passed (178 active control references). Recorder inventory regenerated without database statistics. Notification recommendations saved in `docs/generac-notifications.md`. No generator actions, test runs, or notification automations were executed/deployed.

## Follow-up

Implement agreed notifications with durable cycle/timestamp guards. Validate the first natural run/exercise and monitoring-loss events. Model-specific battery limits and exercise expectations remain unverified. The community integration depends on the vendor cloud and is supplemental to vendor alerts.
