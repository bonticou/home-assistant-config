# Generac notifications enabled

## Request and context

Following the connection and capability review, user authorized the four prudent notification categories and requested exact previews. Reviewed the connection history and notification reliability patterns. No oil-level, oil-service prediction, battery-health prediction, or inferred utility/transfer event is supported by these rules.

## Changes

Added a purpose-specific generator automation file in the repository; appended only the same rule to the currently monolithic live automation file. Four persistent text helpers store incident candidate/time and last-notified state/time. Main configuration receives only their definitions; broader decomposition remains separate reliability work.

Attention and non-exercise runs require four stable minutes. Monitoring loss requires 30 minutes; recovery requires four stable minutes and a prior sent loss alert. Maintenance sends once per incident during 9 AM–8 PM. Normal exercises remain quiet; their warning/stopped states can alert. Concurrent attention suppresses maintenance/run-start pushes. Recoveries say only what Generac reports, without inferring utility restoration. Invalid data pauses non-monitoring evaluation and resets its confirmation timer while preserving deduplication state. Dispatch occurs before marking a notice sent.

Notifications use the existing central phone script, named tags, generator grouping, Recent history, and the Mobile Link destination. Exact rendered example wording is in `docs/generac-notifications.md`.

## Checks and live verification

- Eight tests execute actual automation YAML with mocked states/actions: normal trigger, already sent, restored helpers, prior incident rearming, unavailable/reconnect, routine exercise, daytime maintenance, and send failure/retry.
- Four YAML parses and inventory coverage (178 references) passed; Recorder report regenerated.
- Fresh live hashes and reviewed minimal diff; MCP applied with HA validation OK and verified writes.
- Reloaded Input texts then Automations through the developer UI because the admin MCP reload allowlist excludes input_text. No Core restart.
- Automation on. Reload-triggered and subsequent minute-triggered traces both finished without errors. Initial live state Ready, connected, no warning/maintenance; no notification sent.
- Browser state view confirmed all four helper JSON values. Subsequent trace confirmed the stored records read back correctly and retained their original candidate timestamps.

## Residual limits

Cloud data may lag. Last-seen timestamp is deliberately unused. No physical generator actions or fabricated live sensor states were used. Real mobile delivery uses the existing shared notification path; synthetic fault pushes were not sent. A process interruption between successful phone dispatch and the helper stamp can still cause a duplicate, as with other non-transactional push systems. Review the first natural incident trace if delivery or vendor wording needs refinement.
