# Vacation foyer overnight security glow

## Request and context

User requested 20% foyer chandelier brightness overnight during vacation. Reviewed the vacation-return cleanup history, Office vacation addition, and live scripts, configuration, and automation files. The prior routine ended evening activity at 23:45 and turned the chandelier off until pre-sunrise.

## Findings and changes

- Vacation activity fallback now sets the foyer chandelier to 20% with a 30-second transition during the quiet window while the sun is below the horizon.
- Daytime fallback remains unchanged. Existing evening and pre-sunrise curves still take precedence; ending vacation retains normal schedule handoff.
- The normal foyer scheduler now requires vacation mode off. Previously it could reset vacation brightness to 10% every fifteen minutes or turn it off at the evening cutoff. Vacation's five-minute sync owns brightness while vacation is on.
- Away-light count, names, and entity IDs consistently exempt this intentional foyer glow during vacation darkness. Existing overnight vacation guard remains unchanged.

## Checks and deployment

Parsed all six local/live candidate YAML files. Semantic checks confirmed the first fallback choice sets 20%, retains the original fallback, and both automation representations guard normal scheduling during vacation. Inventory coverage passed (178 references); Recorder inventory regenerated. Prepared live diff reviewed, preserving monolithic live automation formatting and unrelated drift.

MCP deployment applied successfully with verified writes, HA validation OK, and script/template/automation reloads completed. No Core restart.

## Limits

No vacation toggle or whole-house simulation was executed for testing. The next natural overnight vacation cycle must establish physical device behavior. This is a lighting preference, not a guarantee of security protection.
