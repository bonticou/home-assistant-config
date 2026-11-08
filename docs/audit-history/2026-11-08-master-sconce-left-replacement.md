# Master sconce left replacement and paired response

## Result

The replacement Lutron Diva dimmer is now **Master Sconce L** in **Master Bedroom**,
using the existing `light.master_bedroom_sconce_l` identity. The right dimmer and
`light.master_bedroom_sconces` group remain unchanged. The prior left dimmer and
its history are retained as `light.master_sconce_l_spare_20261108`, disabled and
named **Former Master Sconce L - held for repurposing**. It has not been deleted
or assigned another purpose.

Trevor requested discovery and replacement everywhere, then clarified that the
two physical switches must function as a linked pair: operating either should
control both, including dimming. He also requested less perceptible lag.

## Evidence and migration

- Existing pinned administrative MCP bridge health passed on Core 2026.9.2.
  Its documented CLI was used because direct admin tools were not exposed here.
- Reloaded only the existing Lutron integration through authenticated HA settings.
  Discovery increased from 37 devices / 44 entities to 38 / 45. The single new
  device was explicitly named Master Sconce L new, model DVRF-6L (DivaSmartDimmer).
- Paused only the sconce synchronization automation during the identity swap,
  then restored it. The new device took the stable entity ID, display name and
  room. Enabled/visible state remained on. No exposure, credentials or grants
  were changed.
- New device Related view lists the two-way sconce automation and All Off /
  Bedtime scripts. Old device Related view reports no automations, scripts or
  scenes; its one disabled entity remains present.
- Inspected live main configuration, automations, scripts, scenes, light groups,
  primary dashboard and diagnostic dashboard. No old physical-device-ID reference
  was present. Left/right references are in the sync automation, paired scripts
  and group; the primary dashboard uses the combined group. Stable-ID migration
  preserves these references without broad replacement of unrelated settings.
- New light was available at 3 percent after migration. No light actuation, scene
  replay or physical wall-switch testing was performed. The temporary rename
  was read back and corrected before restoring sync; final registry list remained
  45 Lutron entities with the expected stable and held identifiers.

## Response improvement

The previous sync had no deliberate delay but mirrored any state/attribute update
and did not specify follower transition time. Its retained trace list showed
completed commands in about 40–50 ms; that is not wall-to-light latency.

The minimal patch keeps bidirectional on/off and brightness mapping, equality
guard and restart mode. Follower commands now explicitly request `transition: 0`.
It accepts actual on/off or brightness changes only when both old and new source
states are known. It ignores startup/reconnection and unrelated attribute updates.
While All Off or Bedtime is active, those paired scripts own their intentional
fades, avoiding a zero-transition follower command competing with them. Neither
script was modified. No cooldown, artificial delay or persistent lock was added.

This does not establish electrically simultaneous control or eliminate every
asynchronous two-sided race. Lutron reporting/radio latency remains. Scene
protection lasts while the script is active, and manual linking is suppressed
during that short interval. Physical tests should check both directions, on/off,
rapid dimming, off during dimming, and the existing paired scene fades.

## Validation and deployment

- Seven focused YAML/Jinja tests passed in `tests/test_master_sconce_sync.py`.
  They cover both directions, exact payloads, equal-state echo avoidance,
  unrelated updates, unknown/unavailable recovery, scene ownership and no delay.
- Local inventory coverage passed for 178 active control references. This is a
  bounded repository membership check, not a full live registry audit.
- Prepared and reviewed a change to only the sconce block in the actual live
  monolithic automations file, preserving unrelated live content and structure.
- Deployment `57199bc50bdc469b8c4cd18488cb6c29` applied; HA config check passed;
  automation reload completed; no Core restart. Exact live automation hash
  matched the prepared output. The other six inspected files retained their
  pre-change hashes. Live automation state is enabled.
- Inventory received a targeted replacement reconciliation, not a broad census.
- The Lights dashboard loaded with its combined Sconces tile available. Existing
  output levels were not forcibly aligned; the next actual on/off/dim operation
  is the remaining runtime check. No post-deployment sync action was observed
  before handoff to the user.

## Recovery and scope limits

The admin deployment can be rolled back through the documented bridge to restore
previous synchronization behavior. Registry rollback is separate: move the new
entity off the stable ID, restore that ID/name to the held entity and re-enable it
only if the old hardware should control the sconces again. Preserve the spare
until Trevor gives step-two instructions.

Supported entity/device Related views and seven live configuration files were
inspected. Arbitrary external device-ID consumers and every UI-managed storage
object were not exported. The current combined dashboard was not physically
actuated, and offline tests do not measure visible synchronization speed.


## Follow-up: latency after the user test

Trevor confirmed: “OK, is there any possible way to reduce the latency? Otherwise,
they work perfectly”. This confirms his functional test; the following measurements
are from retained Home Assistant traces, not a new physical test by the assistant.

Two completed post-deployment right-to-left dimming runs at 23:10:24 and 23:10:27
UTC were retained. Both sent the expected brightness with `transition: 0`, and the
returning left-side event failed the equality condition as intended, rather than
issuing a command back. Measured timings were:

| Segment | Run 1 | Run 2 |
| --- | ---: | ---: |
| Source state timestamp to follower service-dispatch step | 3.621 ms | 2.968 ms |
| Source state timestamp to matching follower state timestamp | 49.307 ms | 54.501 ms |
| Automation start to completion | 56.372 ms | 53.147 ms |

This is a small retained sample of one direction. It does not measure time from
finger movement to the source report, radio transit independently, or visible
light response. The remaining retained entries are equality-filtered follower
updates. No additional lights were operated and no live configuration changed.

The Home Assistant dispatch portion is already only a few milliseconds. Removing
safety/equality checks, aggressive polling, or a custom integration is not justified
by this evidence. The local dimmer must first publish a state change before this
state-based pairing can act. Historical third-party reports quote Lutron support
describing delayed local dimmer status reports, but an exact three-second delay
has not been measured or established for these installed devices.

The practical architecture option is a dimming-capable Pico at each preferred
control position, each natively assigned to both sconces in Lutron. Lutron documents
that one Pico can operate multiple dimmers together for on/off/dimming; this avoids
waiting for one wired dimmer's reported level before commanding the other. It
changes which controls the person uses, and does not make the existing sliders
report sooner. Any change to wired controls or load wiring would first need a
specific approved plan and a qualified electrician. No purchase, pairing, wiring
change or architecture migration was made.

Sources checked for the follow-up:
- [Lutron: Pico control of multiple dimmers](https://www.casetawireless.com/us/en/caseta-advantage/pico-smart-remote).
- [Lutron: Pico pairing and simultaneous device control](https://support.lutron.com/us/en/product/casetawireless/article/troubleshooting/How-to-program-a-Pico-remote-with-a-Cas%C3%A9ta-device-or-the-Lutron-app).
- [Home Assistant: Lutron Caseta local integration and supported button events](https://www.home-assistant.io/integrations/lutron_caseta/).
- [Historical Hubitat discussion quoting Lutron support](https://community.hubitat.com/t/lutron-caseta-integration-delay/1490/15), secondary evidence only, not a benchmark for this house.
