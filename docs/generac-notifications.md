# Generac notification recommendations

Date: 2026-10-19. Status: connected; four notification categories enabled and live execution verified.

## Verified capabilities

Generac Generator, model G0072610, connected through binarydev/ha-generac via HACS. HACS offered v0.5.4; its shipped manifest reports 0.5.3. The installed sensor implementation distinguishes Ready, Running, Exercising, Warning, Stopped, Communication Issue, Unknown, Online, and Offline. There are separate connection, warning, maintenance, battery-voltage, status-text, runtime, and last-seen entities. No dedicated utility voltage, transfer-switch position, oil-life, or fuel-level entity was exposed for this generator.

Initial observation: Ready / Ready to run, battery 14.1 V, connected, warning and maintenance clear. Cloud last-seen was approximately 12 hours old despite Connected; this timestamp is supplied by the vendor, not an integration poll timestamp. Do not use it as a short offline threshold without observing its normal update cadence. Signal strength was 14%; do not equate that field with a proven connectivity failure.

## Enabled notification behavior

| Event | Proposed treatment |
| --- | --- |
| Warning or Stopped persists for four minutes | Attention push, `⚠️ Generator needs attention`, quoting vendor status text. Stopped is not automatically a proven failed start. |
| Non-exercise Running persists across two polls | One push, `⚡ Generator is running`. Say only what is observed; no claim that utility power failed or the house transferred. |
| Running → Ready | One recovery summary, `✅ Generator ready again`, without an inferred outage duration. Do not describe it as utility restored without an independent power source. |
| Exercising → Ready | Internal history only by default. Warn if the state changes to Warning/Stopped. Do not invent a missed-exercise schedule until configured schedule/duration is known. |
| Maintenance alert becomes active | Daytime notice (9 AM–8 PM), `🔧 Generator maintenance due`, with available vendor explanation; once per incident until cleared. |
| Disconnected, Communication Issue, or integration unavailable for 30 minutes | One notice, `📡 Generator monitoring unavailable`, followed by recovery only if an outage notice was sent. Describe monitoring loss, not generator failure. |
| Battery voltage | Display initially. Enable low-voltage alerts only after model-specific guidance or a vendor battery warning establishes an appropriate threshold; do not interpret one voltage sample as battery health. |

## Implementation requirements

Use the existing central phone-notification script and notification-center conventions. Persistent timestamp/cycle helpers must suppress duplicates across HA restarts and reconnects. Stamp after successful notification dispatch, group/tag related notices, and suppress recovery claims when startup or missing data obscures the prior state. Unknown/unavailable must not be classified as Stopped. Avoid duplicating simultaneous warning/status alerts. Preserve the integration's default 120-second polling rather than increasing cloud load.

The cloud integration can lag or lose access if vendor APIs change. Keep the vendor's own alerts enabled. These rules are supplemental monitoring and do not start, stop, or exercise the generator.

Source: https://github.com/binarydev/ha-generac and the installed sensor implementation. Final mappings must use the registered entities in the device inventory.

## Exact notification previews

These are rendered examples, not real faults or test pushes. Vendor detail is appended to attention/maintenance messages when available.

**⚠️ Generator needs attention**

Generac reports stopped. Check Mobile Link for details.

**⚡ Generator is running**

Generac reports the generator is running, rather than exercising. This connection doesn't confirm whether the house has transferred to generator power.

**✅ Generator ready again**

Generac now reports Ready to run after the running alert. This connection doesn't confirm whether utility power has been restored.

**🔧 Generator reports maintenance due**

Generac has flagged maintenance. The connection hasn't provided the specific task. Check Mobile Link before arranging service.

**📡 Generator monitoring lost**

Home Assistant hasn't had a connected, usable generator status for 30 minutes. This means monitoring is unavailable; it does not confirm a generator fault. Check Mobile Link.

**✅ Generator monitoring restored**

Home Assistant is receiving generator status again. Current reported status: Ready.

## Implementation and verification

`automations/35-generator-notifications.yaml` owns the rules. Four restored `input_text.generac_*_incident` JSON records retain candidate state/time and last notified state/time. Clear attention/maintenance cycles rearm silently; run and monitoring recovery require a previously sent active notice. Attention suppresses concurrent run-start and maintenance pushes. Unknown data breaks non-monitoring confirmation timers but preserves the notified incident. Poll evaluation is once per minute; cloud polling is unchanged.

Eight tests execute the actual YAML against mocked states/services, covering persistence, stale prior incidents, recovery, unavailable states, exercise silence, maintenance hours, and failed dispatch. Live reload trace finished successfully; all four helper values were inspected and contain valid JSON. No physical generator action or synthetic phone push was performed.
