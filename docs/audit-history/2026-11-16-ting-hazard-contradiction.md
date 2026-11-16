# Ting hazard contradiction — November 16, 2026

Read-only investigation at approximately 5:05–5:10 AM EST. Owner screenshot
reported via the parent shows Ting connected with no fire hazards; this worker
did not independently inspect that screenshot or the vendor account.

Live admin MCP works. At 5:05 AM, confirmed-hazard automation trace
`ffb585c17ec66fbb927581b4651c22fc` explicitly records
binary_sensor.ting_confirmed_hazard_active on, repeat due, and invocation of
ting_send_notification. Its prior timestamp is 4:55 AM. Retained sender runs
also cover 4:22:04, 4:35, 4:45 and 4:55 AM.

Sender trace `6fad7adf303047fbf54293d79d0c497c` at 5:05:00 records confirmed
devices Ting 1, vendor-message summary "No Hazards Detected", and both voltages
122.8 V. It sends the contradictory text "Ting is flagging a confirmed electrical
hazard on Ting 1. No Hazards Detected" with critical sound/volume, then stamps
last-sent after the call returns. This proves the HA alert path and conflicting
inputs, not vendor hazard confirmation or handset delivery.

Fresh live configuration confirms the aggregate hazard template ORs primary
fire_hazard and electrical_fire_hazard binaries from either device, with no
status interpretation. Repository custom integration electrical_fire_hazard
is simply efh level > 0, whereas its status sensor explicitly recognizes
ReviewedNotFire before treating positive EFH level as hazard_detected. This is
a concrete semantic inconsistency and a plausible source of this alert, but
the raw live Ting 1 primary flag, EFH flag, EFH level and status have not been
retrieved. Do not label ReviewedNotFire as today's proven raw payload.

Native MCP query for Ting returned no exposed matches; admin MCP does not
provide arbitrary state/template reads. No diagnostic deployment, browser login,
credentials, integration reload, access change or hazard disabling performed.

Proposed narrow correction, conditional on raw-status verification: preserve
the independent primary is_fire indication and valid active hazard statuses;
exclude explicitly reviewed-not-fire EFH status from level-only promotion.
Apply consistent semantics to the aggregate, device list and attention surfaces.
Do not suppress all hazards based solely on a free-text message or normal voltage.
Implementation/deployment awaits confirmed cause and scoped authorization.
