#!/usr/bin/env python3
"""Keep a compact human-readable irrigation history ledger for Home Assistant."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
from pathlib import Path
from typing import Any


MAX_SESSIONS = 30
MAX_ZONE_RUNS = 120
MAX_EVENTS = 200

FLO_DERIVED_EVENT_KINDS = {
    "irrigation_flow_after_stop",
    "irrigation_no_flow",
    "irrigation_break_suspected",
    "irrigation_clog_possible",
    "irrigation_flo_unavailable",
    "irrigation_blind_watering",
}

FLO_DERIVED_NOTE_RE = re.compile(
    r"\b("
    r"flo|flow|gpm|gal/min|gallons?|"
    r"fingerprint|learned|profile|clog(?:ged)?|break|"
    r"max flow|avg flow|water used"
    r")\b",
    re.IGNORECASE,
)


def parse_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def parse_int(value: Any, default: int = 0) -> int:
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return default


def parse_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"1", "true", "yes", "on"}


def clean_text(value: Any) -> str:
    return " ".join(str(value or "").split())


def base_event_kind(kind: Any) -> str:
    text = clean_text(kind)
    if text.startswith("alert_"):
        return text[len("alert_") :]
    return text


def sanitize_note(note: Any) -> str:
    text = clean_text(note)
    if not text:
        return ""
    parts = re.split(r"(?<=[.!?])\s+", text)
    kept = [part for part in parts if part and not FLO_DERIVED_NOTE_RE.search(part)]
    return clean_text(" ".join(kept))


def is_flo_derived_event(event: dict[str, Any]) -> bool:
    kind = base_event_kind(event.get("kind"))
    if kind in FLO_DERIVED_EVENT_KINDS:
        return True
    text = " ".join(
        clean_text(event.get(key))
        for key in ("kind", "title", "note")
    )
    return bool(FLO_DERIVED_NOTE_RE.search(text)) and kind not in {
        "weather_skip_likely",
        "irrigation_scheduled_not_started",
        "irrigation_controller_offline",
        "irrigation_controller_offline_during_watering",
        "irrigation_zone_ran_too_long",
        "irrigation_valve_mismatch",
        "irrigation_multiple_zones",
        "irrigation_pressure_collapse",
        "irrigation_recovery_slow",
        "irrigation_recovery_failed",
    }


def parse_time(value: str | None) -> dt.datetime:
    if not value:
        return dt.datetime.now(dt.timezone.utc)
    normalized = value.strip().replace("Z", "+00:00")
    try:
        parsed = dt.datetime.fromisoformat(normalized)
    except ValueError:
        try:
            parsed = dt.datetime.strptime(normalized, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            return dt.datetime.now(dt.timezone.utc)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=dt.datetime.now().astimezone().tzinfo)
    return parsed.astimezone(dt.timezone.utc)


def iso(value: dt.datetime) -> str:
    return value.astimezone(dt.timezone.utc).isoformat()


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return payload if isinstance(payload, dict) else {}


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def initial_data() -> dict[str, Any]:
    return {
        "schema_version": 1,
        "active_session": {},
        "active_zones": {},
        "sessions": [],
        "zone_runs": [],
        "events": [],
    }


def load_data(path: Path) -> dict[str, Any]:
    data = read_json(path)
    if not data:
        return initial_data()
    data.setdefault("schema_version", 1)
    data.setdefault("active_session", {})
    data.setdefault("active_zones", {})
    data.setdefault("sessions", [])
    data.setdefault("zone_runs", [])
    data.setdefault("events", [])
    return data


def bounded_prepend(items: list[dict[str, Any]], item: dict[str, Any], limit: int) -> list[dict[str, Any]]:
    return [item] + items[: max(limit - 1, 0)]


def event_payload(
    *,
    kind: str,
    at: str,
    severity: str = "info",
    title: str = "",
    note: str = "",
    session_id: str = "",
    zone: str = "",
    zone_name: str = "",
) -> dict[str, Any]:
    return {
        "at": at,
        "kind": clean_text(kind),
        "severity": clean_text(severity) or "info",
        "title": clean_text(title) or clean_text(kind).replace("_", " ").title(),
        "note": clean_text(note),
        "session_id": clean_text(session_id),
        "zone": clean_text(zone),
        "zone_name": clean_text(zone_name),
    }


def add_event(data: dict[str, Any], event: dict[str, Any]) -> None:
    data["events"] = bounded_prepend(data.get("events", []), event, MAX_EVENTS)
    active = data.get("active_session") or {}
    if event.get("kind", "").startswith("alert") or event.get("severity") in {"warning", "critical"}:
        alerts = active.setdefault("alerts", [])
        alerts.append(event)
        data["active_session"] = active


def session_start(args: argparse.Namespace, data: dict[str, Any]) -> None:
    at = iso(parse_time(args.at))
    session = {
        "session_id": clean_text(args.session_id),
        "started_at": at,
        "start_zone": clean_text(args.zone),
        "start_zone_name": clean_text(args.zone_name),
        "start_pressure": round(parse_float(args.pressure), 2),
        "start_flow": round(parse_float(args.flow), 3),
        "start_gallons": round(parse_float(args.gallons), 2),
        "next_cycle": clean_text(args.next_cycle),
        "alerts": [],
    }
    data["active_session"] = session
    add_event(
        data,
        event_payload(
            kind="session_started",
            at=at,
            title="Sprinklers started",
            note=args.note or f"{session['start_zone_name'] or session['start_zone'] or 'Unknown zone'} started.",
            session_id=session["session_id"],
            zone=session["start_zone"],
            zone_name=session["start_zone_name"],
        ),
    )


def session_finish(args: argparse.Namespace, data: dict[str, Any]) -> None:
    at = iso(parse_time(args.at))
    active = data.get("active_session") or {}
    session_id = clean_text(args.session_id) or clean_text(active.get("session_id"))
    started_at = clean_text(args.started_at) or clean_text(active.get("started_at"))
    start_zone = clean_text(args.start_zone) or clean_text(active.get("start_zone"))
    runtime = parse_float(args.runtime_minutes)
    if runtime <= 0 and started_at:
        runtime = max((parse_time(at) - parse_time(started_at)).total_seconds() / 60.0, 0.0)
    alerts = active.get("alerts", []) if isinstance(active.get("alerts"), list) else []
    alert_outcome = clean_text(args.alert_outcome)
    if not alert_outcome and alerts:
        alert_outcome = ", ".join(event.get("title", "Alert") for event in alerts[-3:])
    session = {
        "session_id": session_id,
        "started_at": started_at,
        "ended_at": at,
        "runtime_minutes": round(runtime, 1),
        "gallons": round(parse_float(args.gallons), 2),
        "start_zone": start_zone,
        "start_zone_name": clean_text(args.start_zone_name) or clean_text(active.get("start_zone_name")),
        "min_pressure": round(parse_float(args.min_pressure), 2),
        "max_flow": round(parse_float(args.max_flow), 3),
        "current_pressure": round(parse_float(args.current_pressure), 2),
        "recovery_status": clean_text(args.recovery_status) or "watching",
        "alert_outcome": alert_outcome or "None",
        "alerts": alerts[-10:],
    }
    data["sessions"] = bounded_prepend(data.get("sessions", []), session, MAX_SESSIONS)
    data["active_session"] = {}
    add_event(
        data,
        event_payload(
            kind="session_finished",
            at=at,
            title="Sprinklers finished",
            note=args.note
            or f"{session['runtime_minutes']} min, {session['gallons']} gal, lowest {session['min_pressure']} psi.",
            session_id=session_id,
            zone=start_zone,
            zone_name=session["start_zone_name"],
        ),
    )


def zone_start(args: argparse.Namespace, data: dict[str, Any]) -> None:
    at = iso(parse_time(args.at))
    zone = clean_text(args.zone)
    zone_name = clean_text(args.zone_name) or zone
    data.setdefault("active_zones", {})[zone] = {
        "zone": zone,
        "zone_name": zone_name,
        "session_id": clean_text(args.session_id),
        "started_at": at,
        "start_pressure": round(parse_float(args.pressure), 2),
        "start_flow": round(parse_float(args.flow), 3),
        "start_gallons": round(parse_float(args.gallons), 2),
        "active_count": parse_int(args.active_count),
    }
    add_event(
        data,
        event_payload(
            kind="zone_started",
            at=at,
            title=f"{zone_name} started",
            note=args.note or f"Flow {parse_float(args.flow):.2f} gpm, pressure {parse_float(args.pressure):.1f} psi.",
            session_id=args.session_id,
            zone=zone,
            zone_name=zone_name,
        ),
    )


def zone_finish(args: argparse.Namespace, data: dict[str, Any]) -> None:
    at = iso(parse_time(args.at))
    zone = clean_text(args.zone)
    active = (data.get("active_zones") or {}).pop(zone, {})
    zone_name = clean_text(args.zone_name) or clean_text(active.get("zone_name")) or zone
    latest_sample: dict[str, Any] = {}
    if getattr(args, "fingerprint_status_file", None):
        fingerprint_status = read_json(args.fingerprint_status_file)
        sample = fingerprint_status.get("latest_sample") or {}
        if clean_text(sample.get("zone")) == zone:
            latest_sample = sample
    started_at = clean_text(args.started_at) or clean_text(active.get("started_at"))
    duration = parse_float(args.duration_minutes)
    if duration <= 0 and latest_sample:
        duration = parse_float(latest_sample.get("duration_minutes"))
    if duration <= 0 and started_at:
        duration = max((parse_time(at) - parse_time(started_at)).total_seconds() / 60.0, 0.0)
    start_gallons = parse_float(active.get("start_gallons"))
    gallons = parse_float(args.gallons) or parse_float(latest_sample.get("gallons"))
    if gallons < start_gallons:
        gallons = 0.0
    run = {
        "zone": zone,
        "zone_name": zone_name,
        "session_id": clean_text(args.session_id) or clean_text(active.get("session_id")),
        "started_at": started_at or clean_text(latest_sample.get("started_at")),
        "ended_at": clean_text(latest_sample.get("ended_at")) or at,
        "duration_minutes": round(duration, 2),
        "gallons": round(gallons, 2),
        "avg_flow": round(parse_float(args.avg_flow) or parse_float(latest_sample.get("avg_flow")), 3),
        "max_flow": round(parse_float(args.max_flow) or parse_float(latest_sample.get("max_flow")), 3),
        "pressure_drop": round(
            parse_float(args.pressure_drop) or parse_float(latest_sample.get("pressure_drop")), 2
        ),
        "start_pressure": round(
            parse_float(active.get("start_pressure")) or parse_float(latest_sample.get("start_pressure")), 2
        ),
        "min_pressure": round(parse_float(args.min_pressure) or parse_float(latest_sample.get("min_pressure")), 2),
        "contaminated": parse_bool(args.contaminated) or parse_bool(latest_sample.get("contaminated")),
        "contamination_reasons": clean_text(args.contamination_reasons)
        or clean_text(", ".join(latest_sample.get("contamination_reasons") or [])),
        "anomaly": clean_text(args.anomaly),
        "anomaly_reason": clean_text(args.anomaly_reason),
    }
    data["zone_runs"] = bounded_prepend(data.get("zone_runs", []), run, MAX_ZONE_RUNS)
    add_event(
        data,
        event_payload(
            kind="zone_finished",
            at=at,
            severity="warning" if run["anomaly"] else "info",
            title=f"{zone_name} finished",
            note=args.note
            or f"{run['duration_minutes']} min, {run['gallons']} gal, {run['pressure_drop']} psi drop.",
            session_id=run["session_id"],
            zone=zone,
            zone_name=zone_name,
        ),
    )


def generic_event(args: argparse.Namespace, data: dict[str, Any]) -> None:
    add_event(
        data,
        event_payload(
            kind=args.kind,
            at=iso(parse_time(args.at)),
            severity=args.severity,
            title=args.title,
            note=args.note,
            session_id=args.session_id,
            zone=args.zone,
            zone_name=args.zone_name,
        ),
    )


def purge_flo_derived(data: dict[str, Any]) -> None:
    data["active_session"] = {}
    data["active_zones"] = {}
    data["sessions"] = []
    data["zone_runs"] = []

    retained_events = []
    for event in data.get("events", []):
        if is_flo_derived_event(event):
            continue
        cleaned = dict(event)
        cleaned["note"] = sanitize_note(cleaned.get("note"))
        retained_events.append(cleaned)
    data["events"] = retained_events[:MAX_EVENTS]


def summarize(data: dict[str, Any]) -> dict[str, Any]:
    sessions = data.get("sessions", [])
    zone_runs = data.get("zone_runs", [])
    events = data.get("events", [])
    return {
        "updated_at": iso(dt.datetime.now(dt.timezone.utc)),
        "active_session": data.get("active_session") or {},
        "active_zone_count": len(data.get("active_zones") or {}),
        "active_zones": data.get("active_zones") or {},
        "session_count": len(sessions),
        "zone_run_count": len(zone_runs),
        "event_count": len(events),
        "latest_session": sessions[0] if sessions else {},
        "latest_zone_run": zone_runs[0] if zone_runs else {},
        "latest_event": events[0] if events else {},
        "sessions": sessions,
        "zone_runs": zone_runs,
        "events": events,
    }


def mark_status(data: dict[str, Any], status_file: Path) -> dict[str, Any]:
    status = summarize(data)
    write_json(status_file, status)
    return status


def add_common_file_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--data-file", type=Path, default=Path(".irrigation_history.json"))
    parser.add_argument("--status-file", type=Path, default=Path(".irrigation_history_status.json"))
    parser.add_argument("--fingerprint-status-file", type=Path, default=None)
    parser.add_argument("--status", action="store_true")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    add_common_file_args(parser)
    subparsers = parser.add_subparsers(dest="command")

    event = subparsers.add_parser("event")
    event.add_argument("--kind", required=True)
    event.add_argument("--at", default="")
    event.add_argument("--severity", default="info")
    event.add_argument("--title", default="")
    event.add_argument("--note", default="")
    event.add_argument("--session-id", default="")
    event.add_argument("--zone", default="")
    event.add_argument("--zone-name", default="")

    start = subparsers.add_parser("session-start")
    start.add_argument("--session-id", required=True)
    start.add_argument("--at", required=True)
    start.add_argument("--zone", default="")
    start.add_argument("--zone-name", default="")
    start.add_argument("--pressure", default="0")
    start.add_argument("--flow", default="0")
    start.add_argument("--gallons", default="0")
    start.add_argument("--next-cycle", default="")
    start.add_argument("--note", default="")

    finish = subparsers.add_parser("session-finish")
    finish.add_argument("--session-id", default="")
    finish.add_argument("--at", required=True)
    finish.add_argument("--started-at", default="")
    finish.add_argument("--runtime-minutes", default="0")
    finish.add_argument("--gallons", default="0")
    finish.add_argument("--start-zone", default="")
    finish.add_argument("--start-zone-name", default="")
    finish.add_argument("--min-pressure", default="0")
    finish.add_argument("--max-flow", default="0")
    finish.add_argument("--current-pressure", default="0")
    finish.add_argument("--recovery-status", default="")
    finish.add_argument("--alert-outcome", default="")
    finish.add_argument("--note", default="")

    zone_start_parser = subparsers.add_parser("zone-start")
    zone_start_parser.add_argument("--zone", required=True)
    zone_start_parser.add_argument("--zone-name", default="")
    zone_start_parser.add_argument("--session-id", default="")
    zone_start_parser.add_argument("--at", required=True)
    zone_start_parser.add_argument("--pressure", default="0")
    zone_start_parser.add_argument("--flow", default="0")
    zone_start_parser.add_argument("--gallons", default="0")
    zone_start_parser.add_argument("--active-count", default="1")
    zone_start_parser.add_argument("--note", default="")

    zone_finish_parser = subparsers.add_parser("zone-finish")
    zone_finish_parser.add_argument("--zone", required=True)
    zone_finish_parser.add_argument("--zone-name", default="")
    zone_finish_parser.add_argument("--session-id", default="")
    zone_finish_parser.add_argument("--at", required=True)
    zone_finish_parser.add_argument("--started-at", default="")
    zone_finish_parser.add_argument("--duration-minutes", default="0")
    zone_finish_parser.add_argument("--gallons", default="0")
    zone_finish_parser.add_argument("--avg-flow", default="0")
    zone_finish_parser.add_argument("--max-flow", default="0")
    zone_finish_parser.add_argument("--pressure-drop", default="0")
    zone_finish_parser.add_argument("--min-pressure", default="0")
    zone_finish_parser.add_argument("--contaminated", default="false")
    zone_finish_parser.add_argument("--contamination-reasons", default="")
    zone_finish_parser.add_argument("--anomaly", default="")
    zone_finish_parser.add_argument("--anomaly-reason", default="")
    zone_finish_parser.add_argument("--note", default="")

    subparsers.add_parser("purge-flo-derived")

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    data = load_data(args.data_file)

    if args.status and not args.command:
        print(json.dumps(mark_status(data, args.status_file), sort_keys=True))
        return 0

    if args.command == "event":
        generic_event(args, data)
    elif args.command == "session-start":
        session_start(args, data)
    elif args.command == "session-finish":
        session_finish(args, data)
    elif args.command == "zone-start":
        zone_start(args, data)
    elif args.command == "zone-finish":
        zone_finish(args, data)
    elif args.command == "purge-flo-derived":
        purge_flo_derived(data)
    elif args.status:
        pass
    else:
        parser.error("expected --status or a command")

    write_json(args.data_file, data)
    status = mark_status(data, args.status_file)
    print(json.dumps(status, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
