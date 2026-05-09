#!/usr/bin/env python3
"""Append durable Home Assistant action stamps to the local house-manager outbox."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any


SAFE_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.:-]{0,120}$")
MAX_NOTE_LENGTH = 500


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def outbox_dir(explicit: str | None = None) -> Path:
    if explicit:
        return Path(explicit).expanduser()
    return repo_root() / ".house-manager-outbox"


def ledger_path(directory: Path) -> Path:
    return directory / "action-stamps.jsonl"


def status_path(directory: Path) -> Path:
    return directory / "action-stamps-status.json"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--status", action="store_true", help="Print ledger status JSON and exit.")
    parser.add_argument("--outbox-dir")
    parser.add_argument("--notice-id")
    parser.add_argument("--cycle-id")
    parser.add_argument("--action")
    parser.add_argument("--completed-at")
    parser.add_argument("--source", default="home_assistant")
    parser.add_argument("--note", default="")
    return parser.parse_args()


def require_safe_id(name: str, value: str | None) -> str:
    if value is None or not SAFE_ID_RE.match(value):
        raise ValueError(f"{name} must be a stable identifier matching {SAFE_ID_RE.pattern}")
    return value


def normalize_completed_at(value: str | None) -> str:
    if value is None or not value.strip():
        raise ValueError("completed_at is required")
    trimmed = value.strip()
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S"):
        try:
            datetime.strptime(trimmed, fmt)
            return trimmed
        except ValueError:
            pass
    raise ValueError("completed_at must be YYYY-MM-DD HH:MM:SS or YYYY-MM-DDTHH:MM:SS")


def event_id_for(event: dict[str, Any]) -> str:
    parts = [
        str(event["notice_id"]),
        str(event["cycle_id"]),
        str(event["action"]),
        str(event["completed_at"]),
        str(event["source"]),
    ]
    return hashlib.sha256("|".join(parts).encode("utf-8")).hexdigest()[:20]


def build_event(args: argparse.Namespace) -> dict[str, Any]:
    event = {
        "schema_version": 1,
        "event_type": "house_action_stamp",
        "notice_id": require_safe_id("notice_id", args.notice_id),
        "cycle_id": require_safe_id("cycle_id", args.cycle_id),
        "action": require_safe_id("action", args.action),
        "completed_at": normalize_completed_at(args.completed_at),
        "source": require_safe_id("source", args.source),
        "note": (args.note or "")[:MAX_NOTE_LENGTH],
        "recorded_at": datetime.now().isoformat(timespec="seconds"),
        "sync_state": "pending",
    }
    event["event_id"] = event_id_for(event)
    return event


def append_event(path: Path, event: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event, sort_keys=True) + "\n")


def read_events(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    events: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            try:
                payload = json.loads(line)
            except json.JSONDecodeError:
                continue
            if isinstance(payload, dict):
                events.append(payload)
    return events


def write_status(directory: Path, events: list[dict[str, Any]]) -> dict[str, Any]:
    latest = events[-1] if events else {}
    pending_count = sum(1 for event in events if event.get("sync_state") == "pending")
    status = {
        "ledger_path": str(ledger_path(directory)),
        "event_count": len(events),
        "pending_count": pending_count,
        "latest_event_id": latest.get("event_id", ""),
        "latest_notice_id": latest.get("notice_id", ""),
        "latest_cycle_id": latest.get("cycle_id", ""),
        "latest_action": latest.get("action", ""),
        "latest_completed_at": latest.get("completed_at", ""),
        "updated_at": datetime.now().isoformat(timespec="seconds"),
    }
    directory.mkdir(parents=True, exist_ok=True)
    status_path(directory).write_text(json.dumps(status, sort_keys=True) + "\n", encoding="utf-8")
    return status


def main() -> int:
    args = parse_args()
    directory = outbox_dir(args.outbox_dir)
    path = ledger_path(directory)

    if args.status:
        print(json.dumps(write_status(directory, read_events(path)), sort_keys=True))
        return 0

    event = build_event(args)
    append_event(path, event)
    write_status(directory, read_events(path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
