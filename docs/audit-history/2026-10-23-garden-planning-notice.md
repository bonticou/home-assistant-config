# One-time garden planning notice

Trevor clarified that gardening planning belongs in HA Notification Center.
Added one item, Plan next season's garden, dated April 9, 2027, one calendar
month before May 9 Mother's Day. No duplicate planning entry existed in the
live configuration. The existing 365-day Upcoming horizon includes it now.

The task enters Needs Attention at 09:00 local time April 9 and sends one push.
A 15-minute daytime catch-up (09:00-19:59) handles downtime or delivery failure.
Restored done/notified timestamp helpers prevent repeat delivery and retain
completion; successful sending is followed by the notification stamp. Planning
done removes this one-time item, with no annual recurrence or fertilizer restart.
No Dot schedule was changed; its duplicate is owned by the originating agent.

Deployed using direct admin MCP with exact live hashes and reviewed diffs:
`53d71241a37b4908ab168e8692170f1c`, followed by
`7f3d2e3f141f49c0bb3aea60d157e9fa` to handle observed initial unknown helper states.
Recovery uses these guarded backup deployments in reverse order. Config checks
passed and script/template/automation reloads completed. Input texts were
reloaded through desktop YAML controls. State readback verified both helpers
exist with max 32 and initial unknown; the condition accepts that uninitialized
state only when both helpers exist, rejects unavailable, and respects timestamps.
Eight condition tests passed, along with YAML parsing and inventory coverage.
Recorder inventory regenerated without database statistics.

Live admin readbacks confirmed all three deployed files and enabled planning
automation; fertilizer sender remains absent. Native Safari accessibility
readback showed Upcoming 18 with the planning title and Apr 9, 2027 date,
Needs Attention still 1 (Water guardrail), and no Fertilizer time entry.
The originating agent also completed the final connected Safari presentation
check: Upcoming showed “🌱 Plan next season's garden” and “Plan on Apr 9, 2027,”
with the description tying that date to Mother's Day on May 9. No test push or
completion was executed against the real future task.
