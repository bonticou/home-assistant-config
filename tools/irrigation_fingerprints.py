#!/usr/bin/env python3
"""Maintain resettable legacy irrigation fingerprint memory."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import statistics
from pathlib import Path
from typing import Any


MAX_SAMPLES_PER_ZONE = 12
MIN_LEARNED_SAMPLES = 3


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
    return {"schema_version": 1, "active": {}, "zones": {}, "latest_sample": {}, "latest_anomaly": {}}


def load_data(path: Path) -> dict[str, Any]:
    data = read_json(path)
    if not data:
        return initial_data()
    data.setdefault("schema_version", 1)
    data.setdefault("active", {})
    data.setdefault("zones", {})
    data.setdefault("latest_sample", {})
    data.setdefault("latest_anomaly", {})
    return data


def median(values: list[float]) -> float:
    return round(float(statistics.median(values)), 3) if values else 0.0


def clean_samples(zone: dict[str, Any]) -> list[dict[str, Any]]:
    return [sample for sample in zone.get("samples", []) if not sample.get("contaminated")]


def baseline_for(zone: dict[str, Any]) -> dict[str, Any]:
    samples = clean_samples(zone)
    return {
        "sample_count": len(samples),
        "learned": len(samples) >= MIN_LEARNED_SAMPLES,
        "median_gallons": median([parse_float(sample.get("gallons")) for sample in samples]),
        "median_avg_flow": median([parse_float(sample.get("avg_flow")) for sample in samples]),
        "median_max_flow": median([parse_float(sample.get("max_flow")) for sample in samples]),
        "median_pressure_drop": median([parse_float(sample.get("pressure_drop")) for sample in samples]),
        "median_duration_minutes": median([parse_float(sample.get("duration_minutes")) for sample in samples]),
    }


def summarize(data: dict[str, Any]) -> dict[str, Any]:
    zones: dict[str, Any] = {}
    learned_count = 0
    for zone_id, zone in sorted((data.get("zones") or {}).items()):
        baseline = baseline_for(zone)
        if baseline["learned"]:
            learned_count += 1
        zones[zone_id] = {
            **baseline,
            "latest_sample_at": (zone.get("samples") or [{}])[-1].get("ended_at", ""),
            "latest_anomaly": zone.get("latest_anomaly", ""),
            "latest_anomaly_reason": zone.get("latest_anomaly_reason", ""),
            "clog_candidate_count": parse_int(zone.get("clog_candidate_count")),
        }
    latest_anomaly = data.get("latest_anomaly") or {}
    return {
        "updated_at": iso(dt.datetime.now(dt.timezone.utc)),
        "learned_zone_count": learned_count,
        "active_zone_count": len(data.get("active") or {}),
        "zones": zones,
        "latest_sample": data.get("latest_sample") or {},
        "latest_anomaly": latest_anomaly.get("kind", ""),
        "latest_anomaly_zone": latest_anomaly.get("zone", ""),
        "latest_anomaly_reason": latest_anomaly.get("reason", ""),
    }


def mark_status(data: dict[str, Any], status_file: Path) -> dict[str, Any]:
    status = summarize(data)
    write_json(status_file, status)
    return status


def reset_data() -> dict[str, Any]:
    return initial_data()


def start_sample(args: argparse.Namespace, data: dict[str, Any]) -> None:
    at = parse_time(args.at)
    pressure = parse_float(args.pressure)
    flow = parse_float(args.flow)
    active_count = parse_int(args.active_count)
    data["active"][args.zone] = {
        "zone": args.zone,
        "started_at": iso(at),
        "start_gallons": parse_float(args.gallons),
        "start_pressure": pressure,
        "min_pressure": pressure,
        "max_flow": flow,
        "touch_count": 0,
        "contaminated": active_count != 1,
        "contamination_reasons": ["multiple_zones_at_start"] if active_count != 1 else [],
    }


def touch_sample(args: argparse.Namespace, data: dict[str, Any]) -> None:
    active = data.get("active") or {}
    sample = active.get(args.zone)
    if not sample:
        return
    pressure = parse_float(args.pressure)
    flow = parse_float(args.flow)
    active_count = parse_int(args.active_count)
    sample["min_pressure"] = min(parse_float(sample.get("min_pressure"), pressure), pressure)
    sample["max_flow"] = max(parse_float(sample.get("max_flow"), flow), flow)
    sample["touch_count"] = parse_int(sample.get("touch_count")) + 1
    if active_count != 1:
        sample["contaminated"] = True
        reasons = sample.setdefault("contamination_reasons", [])
        if "multiple_zones_during_run" not in reasons:
            reasons.append("multiple_zones_during_run")


def anomaly_for(zone: dict[str, Any], sample: dict[str, Any]) -> dict[str, str]:
    baseline = baseline_for(zone)
    if not baseline["learned"] or sample.get("contaminated"):
        return {}

    gallons = parse_float(sample.get("gallons"))
    avg_flow = parse_float(sample.get("avg_flow"))
    max_flow = parse_float(sample.get("max_flow"))
    pressure_drop = parse_float(sample.get("pressure_drop"))
    normal_gallons = parse_float(baseline.get("median_gallons"))
    normal_avg_flow = parse_float(baseline.get("median_avg_flow"))
    normal_max_flow = parse_float(baseline.get("median_max_flow"))
    normal_pressure_drop = parse_float(baseline.get("median_pressure_drop"))

    low_water = (
        normal_gallons > 0
        and normal_avg_flow > 0
        and gallons < normal_gallons * 0.65
        and avg_flow < normal_avg_flow * 0.65
    )
    weak_pressure_drop = normal_pressure_drop <= 0 or pressure_drop < max(1.0, normal_pressure_drop * 0.7)
    if low_water and weak_pressure_drop:
        return {"kind": "clog_possible", "reason": "low_flow_low_gallons_small_pressure_drop"}

    high_flow = (
        (normal_avg_flow > 0 and avg_flow > normal_avg_flow * 1.6)
        or (normal_max_flow > 0 and max_flow > normal_max_flow * 1.6)
    )
    large_pressure_drop = normal_pressure_drop > 0 and pressure_drop > normal_pressure_drop + 8
    if high_flow and large_pressure_drop:
        return {"kind": "break_possible", "reason": "high_flow_large_pressure_drop"}

    return {}


def finish_sample(args: argparse.Namespace, data: dict[str, Any]) -> None:
    active = data.get("active") or {}
    sample = active.pop(args.zone, None)
    if not sample:
        return

    ended_at = parse_time(args.at)
    started_at = parse_time(sample.get("started_at"))
    duration_minutes = max((ended_at - started_at).total_seconds() / 60.0, 0.0)
    end_gallons = parse_float(args.gallons)
    gallons = max(end_gallons - parse_float(sample.get("start_gallons")), 0.0)
    active_count = parse_int(args.active_count)
    if active_count > 1:
        sample["contaminated"] = True
        reasons = sample.setdefault("contamination_reasons", [])
        if "multiple_zones_at_finish" not in reasons:
            reasons.append("multiple_zones_at_finish")
    if duration_minutes < 1 or gallons <= 0:
        sample["contaminated"] = True
        reasons = sample.setdefault("contamination_reasons", [])
        if "sample_too_small" not in reasons:
            reasons.append("sample_too_small")

    min_pressure = min(parse_float(sample.get("min_pressure")), parse_float(args.pressure))
    max_flow = max(parse_float(sample.get("max_flow")), parse_float(args.flow))
    pressure_drop = max(parse_float(sample.get("start_pressure")) - min_pressure, 0.0)
    finished = {
        "zone": args.zone,
        "started_at": sample.get("started_at", ""),
        "ended_at": iso(ended_at),
        "duration_minutes": round(duration_minutes, 2),
        "gallons": round(gallons, 2),
        "avg_flow": round(gallons / duration_minutes if duration_minutes > 0 else 0.0, 3),
        "max_flow": round(max_flow, 3),
        "start_pressure": round(parse_float(sample.get("start_pressure")), 2),
        "min_pressure": round(min_pressure, 2),
        "pressure_drop": round(pressure_drop, 2),
        "contaminated": bool(sample.get("contaminated")),
        "contamination_reasons": sample.get("contamination_reasons", []),
    }

    zone = data.setdefault("zones", {}).setdefault(args.zone, {"samples": []})
    zone.setdefault("samples", []).append(finished)
    zone["samples"] = zone["samples"][-MAX_SAMPLES_PER_ZONE:]
    candidate = anomaly_for(zone, finished)
    anomaly: dict[str, str] = {}
    if candidate.get("kind") == "clog_possible":
        zone["clog_candidate_count"] = parse_int(zone.get("clog_candidate_count")) + 1
        if parse_int(zone.get("clog_candidate_count")) >= 2:
            anomaly = candidate
        else:
            zone["latest_anomaly"] = "clog_candidate"
            zone["latest_anomaly_reason"] = candidate["reason"]
    elif candidate:
        zone["clog_candidate_count"] = 0
        anomaly = candidate
    else:
        zone["clog_candidate_count"] = 0

    if anomaly:
        zone["latest_anomaly"] = anomaly["kind"]
        zone["latest_anomaly_reason"] = anomaly["reason"]
        data["latest_anomaly"] = {"zone": args.zone, **anomaly, "at": finished["ended_at"]}
    elif candidate.get("kind") != "clog_possible":
        zone["latest_anomaly"] = ""
        zone["latest_anomaly_reason"] = ""
        data["latest_anomaly"] = {}
    else:
        data["latest_anomaly"] = {}
    data["latest_sample"] = finished


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-file", type=Path, default=Path(".irrigation_fingerprints.json"))
    parser.add_argument("--status-file", type=Path, default=Path(".irrigation_fingerprint_status.json"))
    parser.add_argument("--status", action="store_true")
    subparsers = parser.add_subparsers(dest="command")

    for command in ("start", "touch", "finish"):
        sub = subparsers.add_parser(command)
        sub.add_argument("--zone", required=True)
        sub.add_argument("--at", required=True)
        sub.add_argument("--pressure", required=True)
        sub.add_argument("--flow", required=True)
        sub.add_argument("--active-count", required=True)
        if command in {"start", "finish"}:
            sub.add_argument("--gallons", required=True)

    subparsers.add_parser("reset")

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    data = load_data(args.data_file)

    if args.status and not args.command:
        print(json.dumps(mark_status(data, args.status_file), sort_keys=True))
        return 0

    if args.command == "start":
        start_sample(args, data)
    elif args.command == "touch":
        touch_sample(args, data)
    elif args.command == "finish":
        finish_sample(args, data)
    elif args.command == "reset":
        data = reset_data()
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
