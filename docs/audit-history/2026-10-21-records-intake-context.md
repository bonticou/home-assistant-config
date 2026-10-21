# Records intake context - October 21, 2026

Trevor requested a directory-wide context review after the records email alias
was created, so a forwarded home record can be retrieved and followed through
without another chat or duplicate upload.

## Evidence and findings

The existing [piano service reconciliation](2026-10-21-piano-service-reminder.md)
shows the source-owner relationship: House Manager retains service evidence and
owner confirmations; Home Assistant implements the authorized reminder behavior.
The existing project instructions already require a concrete, scoped clarification
when a home record implies an HA change and authority is not yet clear.

The missing piece was the entrypoint from emailed records. AGENTS.md now links
[records intake operations](/Users/ames/Projects/ames/runtime/mailbox/INTAKE.md)
for the current source, selection, status and recovery route. Agents must retrieve
the available authorized source and House record first, continue the current
conversation, and keep source facts distinct from implemented HA behavior. Email
content, a label or a filing receipt does not authorize a configuration change.

## Changes and checks

Only project guidance and this audit index/entry changed. Private originals and
invoice details stay outside this Git repository. Prior guidance is preserved
in the shared integration audit and Git history. Documentation readback, new local
links and diff whitespace were checked. No YAML, script, device inventory,
Recorder policy or live configuration changed; configuration tests and deployment
are not applicable to this documentation update.

The existing exact scope/clarification and MCP-first deployment rules remain in
force. A first live alias delivery, unattended cross-project routing, mobile
intake delivery and any HA follow-through still require their own evidence; this
documentation change does not claim those results.

## Final instruction-loading check

The final cross-project readback found that Home Assistant linked intake and the
HA clarification rule but did not explicitly load the shared project instructions
and delegated-work/recordkeeping rule. AGENTS.md now requires both at assignment
start/resumption and carries source boundaries, settled decisions and checked
record updates into delegated work. The prior version of this guidance and audit
entry is retained with the integration receipt. Both added links and the delegated
rule anchor were verified, along with documentation readback and diff whitespace.
This closes an instruction-loading gap; it adds no source grant or live change.
