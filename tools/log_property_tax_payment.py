#!/usr/bin/env python3
"""Record Home Assistant property-tax payment confirmations for house-manager."""

from __future__ import annotations

import argparse
import json
import os
from datetime import datetime
from pathlib import Path


VALID_TAX_TYPES = {"school", "town"}
MONTH_NAMES = {
    1: "January",
    4: "April",
    9: "September",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tax-type", required=True, choices=sorted(VALID_TAX_TYPES))
    parser.add_argument("--bill-month", required=True, type=int, choices=sorted(MONTH_NAMES))
    parser.add_argument("--bill-year", required=True, type=int)
    parser.add_argument("--due-date", required=True)
    parser.add_argument("--paid-date", required=True)
    parser.add_argument("--source", default="home_assistant_notification_action")
    parser.add_argument("--house-manager-dir")
    return parser.parse_args()


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def find_house_manager(explicit: str | None) -> Path | None:
    candidates: list[Path] = []
    if explicit:
        candidates.append(Path(explicit).expanduser())
    if os.environ.get("HOUSE_MANAGER_DIR"):
        candidates.append(Path(os.environ["HOUSE_MANAGER_DIR"]).expanduser())

    root = repo_root()
    candidates.extend(
        [
            root.parent / "house-manager",
            Path("/config").parent / "house-manager",
        ]
    )

    for candidate in candidates:
        if (candidate / "ownership").is_dir():
            return candidate
    return None


def cycle_details(event: dict[str, str | int]) -> dict[str, str]:
    year = int(event["bill_year"])
    month = int(event["bill_month"])
    month_name = MONTH_NAMES[month]
    tax_type = str(event["tax_type"])

    if tax_type == "school":
        return {
            "heading": f"{year} Byram Hills School Tax - {month_name} Installment",
            "cycle_label": f"{year} school tax {month_name.lower()} installment",
            "authority": "Byram Hills School District",
            "installment": f"{month_name} school-tax bill",
            "summary": (
                f"Marked paid from Home Assistant on {event['paid_date']}. "
                "The bill document and payment confirmation should still be ingested when available."
            ),
        }

    return {
        "heading": f"{year} Town of North Castle - Town/County Tax Bill",
        "cycle_label": f"{year} town/county tax",
        "authority": "Town of North Castle",
        "installment": "Annual town/county bill",
        "summary": (
            f"Marked paid from Home Assistant on {event['paid_date']}. "
            "Payment confirmation should still be ingested when available."
        ),
    }


def replace_field(lines: list[str], key: str, value: str) -> list[str]:
    prefix = f"- {key}:"
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = f"{prefix} {value}"
            return lines
    lines.append(f"{prefix} {value}")
    return lines


def update_existing_cycle(section: str, event: dict[str, str | int]) -> str:
    lines = section.splitlines()
    lines = replace_field(lines, "paid_date", str(event["paid_date"]))
    lines = replace_field(lines, "status", "`paid`")
    lines = replace_field(lines, "next_action", "Ingest the payment confirmation when available and attach it to this tax cycle.")
    for index, line in enumerate(lines):
        if line.startswith("- amount_paid:") and line.strip() == "- amount_paid:":
            lines[index] = "- amount_paid: `unknown`"
    return "\n".join(lines)


def build_new_cycle(event: dict[str, str | int]) -> str:
    details = cycle_details(event)
    bill_date = f"{event['bill_year']}-{int(event['bill_month']):02d}-01"
    return "\n".join(
        [
            f"### {details['heading']}",
            "",
            f"- cycle_label: `{details['cycle_label']}`",
            f"- authority: {details['authority']}",
            f"- tax_period_or_fiscal_year: `{event['bill_year']}`",
            f"- installment_or_cycle: {details['installment']}",
            "- ownership_era: `owner`",
            f"- bill_date: {bill_date}",
            f"- due_date: {event['due_date']}",
            f"- paid_date: {event['paid_date']}",
            "- amount_due: `unknown`",
            "- amount_paid: `unknown`",
            "- payment_method: `unknown`",
            "- status: `paid`",
            f"- summary: {details['summary']}",
            f"- source_files: Home Assistant notification action (`{event['source']}`)",
            "- next_action: Ingest the payment confirmation when available and attach it to this tax cycle.",
        ]
    )


def upsert_property_tax_cycle(property_taxes_path: Path, event: dict[str, str | int]) -> None:
    details = cycle_details(event)
    text = property_taxes_path.read_text(encoding="utf-8") if property_taxes_path.exists() else "# Property Taxes\n\n## Tax Cycle History\n"
    heading = f"### {details['heading']}"

    if heading in text:
        start = text.index(heading)
        next_start = text.find("\n### ", start + len(heading))
        end = next_start if next_start != -1 else len(text)
        updated = update_existing_cycle(text[start:end].strip("\n"), event)
        text = text[:start] + updated + text[end:]
    else:
        new_cycle = build_new_cycle(event)
        marker = "## Tax Cycle History"
        if marker in text:
            insert_at = text.index(marker) + len(marker)
            text = text[:insert_at] + "\n\n" + new_cycle + text[insert_at:]
        else:
            text = text.rstrip() + "\n\n## Tax Cycle History\n\n" + new_cycle + "\n"

    property_taxes_path.write_text(text, encoding="utf-8")


def append_event(outbox_path: Path, event: dict[str, str | int]) -> None:
    outbox_path.parent.mkdir(parents=True, exist_ok=True)
    with outbox_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event, sort_keys=True) + "\n")


def main() -> int:
    args = parse_args()
    event: dict[str, str | int] = {
        "event_type": "property_tax_paid",
        "tax_type": args.tax_type,
        "bill_month": args.bill_month,
        "bill_year": args.bill_year,
        "due_date": args.due_date,
        "paid_date": args.paid_date,
        "source": args.source,
        "recorded_at": datetime.now().isoformat(timespec="seconds"),
    }

    house_manager = find_house_manager(args.house_manager_dir)
    if house_manager is not None:
        append_event(house_manager / "ownership" / "sources" / "inbox" / "home-assistant-tax-payment-log.jsonl", event)
        upsert_property_tax_cycle(house_manager / "ownership" / "property-taxes.md", event)
        return 0

    append_event(repo_root() / ".house-manager-outbox" / "property-tax-payments.jsonl", event)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
