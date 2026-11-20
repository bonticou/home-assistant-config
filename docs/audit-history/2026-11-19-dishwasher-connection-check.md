# Replacement dishwasher connection check

**The replacement dishwasher is not currently connected as an appliance in Home
Assistant.** A network-presence tracker and the independent dishwasher-area leak
sensor are present; neither supplies wash-cycle status or completion alerts.
This was a read-only review for `HA-DISHWASHER-VERIFY-20261120`, performed on
November 19, 2026, approximately 20:18–20:20 Eastern.

## Identity and live integration

The canonical [House dishwasher record](../../../house%20manager/appliances/dishwasher.md)
identifies the replacement as **Bosch Benchmark SHV9PCM3N**, installed October 13,
2026. That is more specific than the conversational “Bosch 800” label. House
Manager remains the appliance identity/source owner; no serial is reproduced here.

Live full-state search found no Bosch dishwasher operating, program, remaining-
time or completion entities. `integration_entities('home_connect')` returned an
empty list. The actual Integrations UI search for Home Connect displayed **No
integrations found**; showing disabled integrations displayed **No disabled
integrations**. The viewing filter was restored afterward.

One Bosch-named `device_tracker` was `home` and verified as belonging to UniFi.
Its name contains an appliance identifier, omitted here. It has no usable model
metadata and does not independently establish the replacement identity or any
appliance integration. No separate stale old Bosch appliance entity was proven.

## What is visible and protected

The live, rendered **Water** view at `/calm-mobile/water` visibly shows
**Dishwasher — Clear** under Leak Sensors. Both the saved tile and its detail
configuration refer to `binary_sensor.dishwasher_leak_detection_water_detected`.
This is **Flo by Moen, puck_v1**, not the Bosch dishwasher. At 20:18:28 Eastern,
it was `off` (dry), with its separate temperature/humidity/battery readings
available. Visual inspection of the desktop dashboard confirmed the tile;
this was not merely a repository search.

The live primary-dashboard file hash was
`8a4b617809ff41b1665aa7979894bd5560597047b89228ad3d724e8c5fa033d7`.
Its only dishwasher-specific display is this leak detector and detail surface.
No Bosch operating-status card was found in that dashboard. Other UI-managed
dashboards were not exhaustively inspected.

## Notifications and retained evidence

Live automation/script files contain these exact dishwasher-area references:

| Existing path | Binding and result |
| --- | --- |
| `automation.water_leak_sensor_triggered` | Enabled. The Flo binary sensor becoming `on` calls `script.water_send_alert` with `alert_kind: leak`, critical severity and the detector's friendly name, then the Trevor notification wrapper. Title resolves to **💦 Leak detected**. Last triggered September 14, 15:52:56 Eastern; retained traces were empty. That timestamp predates installation and does not prove a post-installation detector test or delivered notification. |
| `automation.water_shutoff_valve_closed` | Enabled. Uses this detector in the shared leak-zone assessment of a Flo valve closure; it does not observe the dishwasher's operating state. Last triggered November 19, 00:01:31 Eastern. |
| `automation.water_clear_notification_state_when_normal` | Enabled. Uses the same detector among shared water-normal/clear guards. Last triggered November 19, 20:05:27 Eastern. |
| `script.water_send_alert` | Includes the same detector in the active leak-zone list and routes shared water alerts. This is not a dishwasher cycle sender. |

No replacement-dishwasher cycle-complete, appliance-fault, remaining-time or
program notification wiring was found in current live automation/script files.
The admin search for dishwasher-named automations also returned none. Native
MCP exposure search had no dishwasher match; that exposure limitation was not
used alone as evidence of absence.

## Limits and next step

No pairing, login, credential access, control, cycle start, test notification,
configuration edit or reload was performed. Appliance operation/current cycle
cannot be checked until the replacement is connected through an appliance
integration. Its network tracker and independent leak protection must not be
presented as equivalent to that connection. This review did not itself authorize setup.

## Subsequent authorized connection attempt — pending secure login

Trevor subsequently said **“Connect”**. Under `HA-DISHWASHER-CONNECT-20261120`,
that authorizes the official connection of the replacement, without appliance
control, new notification/dashboard work or acceptance of broader unexpected
OAuth grants. Ring, Flo and dehumidifier settings remain unchanged.

The existing HA **Application credentials** page already contains a Home Connect
credential. Its identifiers and secret are omitted here. Starting the official
Home Connect integration reused that credential and reached the genuine Home
Connect SingleKey ID login. No new developer account or application was created.

The required scoped 1Password CLI preflight authenticated exactly the Ames vault.
A metadata-only lookup found the Bosch Dishwasher item and separate Home Connect
Developer item. No item secrets were printed or read into chat. The present
native CUA runtime exposes no documented in-memory CLI-to-form credential bridge;
the historical bridge qualification does not establish current tool support.

The permitted Safari autofill fallback found a saved SingleKey ID login, but
selecting it opened the desktop 1Password unlock prompt: **password confirmation
is required every 14 days**. The exact next step is for the owner to unlock
1Password directly on the Mac, then resume login. Do not ask for that password in
chat or bypass the unlock. This secure handoff was returned to Eames through the
existing relay.

No OAuth consent was accepted and no appliance association was completed.
The setup remains pending at login; requested provider scopes must still be
reviewed before any grant. No physical action, test push, configuration reload,
dashboard change or unrelated account change occurred.
