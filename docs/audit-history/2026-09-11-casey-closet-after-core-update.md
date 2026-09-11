# Casey closet after the Core update

## Context and evidence

Follow-up to the September 10 delayed-Protect-feed investigation. Trevor
updated the software; the live About page now shows Core 2026.9.1, Supervisor
2026.09.0, OS 18.2, and frontend 20260826.6.

The native motion binary sensor is reporting on/off transitions again. September
11 morning events at 07:38:43, 08:30:20, 08:51:21, and 08:54:59 Eastern reached
the last-motion entity within about 0.4–0.9 seconds, versus the previous 7–9
minute delays. The final three inspected native motion events were followed by
HA light-on states approximately 30–40 milliseconds later. The motion helper
shows the matching local timestamp, preserving the previous epoch-write fix.

However, HA reported light-off again about 3.5, 3.7, and 8.1 seconds after those
three light-on events. This is shorter than the configured three quiet minutes.
The history API response did not include action context, so it does not identify
whether this was physical/manual action, another control path, or a reported
state correction. Current aggregated Lutron logs retain seven connection/ping
errors, last timestamped 00:43:39 Eastern, not contemporaneous proof of the
morning light-off transitions.

## Findings and changes

- High confidence: the update restored prompt native Protect motion delivery
  for the inspected morning events.
- High confidence: HA automation/light-on state response is prompt now.
- Unresolved: physical light behavior and why HA records a quick return to off.
  Do not equate the recorded on transition with proof that the light stayed on.
- No further lighting configuration changes or physical light commands made.
  Asked Trevor to report whether the light stays on during the next closet visit.

## Status and follow-up

The delayed event-feed fault is no longer present in the observed post-update
sample. The full closet issue is not declared resolved. Preserve the earlier
Lutron and stale-motion evidence. If a physical visit still fails, capture the
motion event and command acknowledgments together, distinguishing an external
off command from a Lutron state correction before adding another retry rule.
