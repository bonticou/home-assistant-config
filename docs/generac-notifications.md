# Generac notification recommendations

Date: 2026-10-19. Status: connected; recommendations only, no notification automations deployed.

## Verified capabilities

Generac Generator, model G0072610, connected through binarydev/ha-generac via HACS. HACS offered v0.5.4; its shipped manifest reports 0.5.3. The installed sensor implementation distinguishes Ready, Running, Exercising, Warning, Stopped, Communication Issue, Unknown, Online, and Offline. There are separate connection, warning, maintenance, battery-voltage, status-text, runtime, and last-seen entities. No dedicated utility voltage, transfer-switch position, oil-life, or fuel-level entity was exposed for this generator.

Initial observation: Ready / Ready to run, battery 14.1 V, connected, warning and maintenance clear. Cloud last-seen was approximately 12 hours old despite Connected; this timestamp is supplied by the vendor, not an integration poll timestamp. Do not use it as a short offline threshold without observing its normal update cadence. Signal strength was 14%; do not equate that field with a proven connectivity failure.

## Proposed notification behavior

| Event | Proposed treatment |
| --- | --- |
| Warning or Stopped persists across two cloud polls | Attention push, `⚠️ Generator needs attention`, quoting vendor status text. Stopped is not automatically a proven failed start. |
| Non-exercise Running persists across two polls | One push, `⚡ Generator is running`. Say only what is observed; no claim that utility power failed or the house transferred. |
| Running → Ready | One recovery summary, `✅ Generator ready again`, with observed run duration if a valid start was captured. Do not describe it as utility restored without an independent power source. |
| Exercising → Ready | Internal history only by default. Warn if the state changes to Warning/Stopped. Do not invent a missed-exercise schedule until configured schedule/duration is known. |
| Maintenance alert becomes active | Daytime reminder, `🔧 Generator maintenance due`, with available vendor explanation; daily at most until cleared. |
| Disconnected, Communication Issue, or integration unavailable for 30 minutes | One notice, `📡 Generator monitoring unavailable`, followed by recovery only if an outage notice was sent. Describe monitoring loss, not generator failure. |
| Battery voltage | Display initially. Enable low-voltage alerts only after model-specific guidance or a vendor battery warning establishes an appropriate threshold; do not interpret one voltage sample as battery health. |

## Implementation requirements

Use the existing central phone-notification script and notification-center conventions. Persistent timestamp/cycle helpers must suppress duplicates across HA restarts and reconnects. Stamp after successful notification dispatch, group/tag related notices, and suppress recovery claims when startup or missing data obscures the prior state. Unknown/unavailable must not be classified as Stopped. Avoid duplicating simultaneous warning/status alerts. Preserve the integration's default 120-second polling rather than increasing cloud load.

The cloud integration can lag or lose access if vendor APIs change. Keep the vendor's own alerts enabled. These rules are supplemental monitoring and do not start, stop, or exercise the generator.

Source: https://github.com/binarydev/ha-generac and the installed sensor implementation. Final mappings must use the registered entities in the device inventory.
