#!/usr/bin/env python3
"""Build the 7-day irrigation ledger shown on the calm mobile dashboard."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import sqlite3
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo


UTC = dt.timezone.utc


def iso_now() -> str:
    return dt.datetime.now(UTC).isoformat(timespec="seconds")


def read_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    return payload if isinstance(payload, dict) else {}


def safe_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def home_timezone(config_dir: Path) -> dt.tzinfo:
    core_config = config_dir / ".storage" / "core.config"
    if core_config.exists():
        try:
            time_zone = read_json(core_config).get("data", {}).get("time_zone")
            if time_zone:
                return ZoneInfo(str(time_zone))
        except Exception:
            pass
    return dt.datetime.now().astimezone().tzinfo or UTC


def sqlite_table_exists(conn: sqlite3.Connection, table: str) -> bool:
    row = conn.execute(
        "SELECT 1 FROM sqlite_master WHERE type = 'table' AND name = ?",
        (table,),
    ).fetchone()
    return row is not None


def sqlite_columns(conn: sqlite3.Connection, table: str) -> set[str]:
    return {str(row[1]) for row in conn.execute(f"PRAGMA table_info({table})")}


def parse_timestamp(value: Any, timezone: dt.tzinfo) -> dt.datetime | None:
    if isinstance(value, (int, float)):
        return dt.datetime.fromtimestamp(float(value), UTC).astimezone(timezone)
    if isinstance(value, str) and value:
        try:
            parsed = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError:
            return None
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=UTC)
        return parsed.astimezone(timezone)
    return None


def recorder_rows(
    conn: sqlite3.Connection,
    *,
    entity_id: str,
    start: dt.datetime,
    end: dt.datetime,
) -> list[tuple[Any, Any]]:
    state_columns = sqlite_columns(conn, "states")
    if "state" not in state_columns:
        raise ValueError("Recorder states table does not include state")

    timestamp_column = next(
        (column for column in ("last_updated_ts", "last_changed_ts", "last_updated") if column in state_columns),
        None,
    )
    if not timestamp_column:
        raise ValueError("Recorder states table does not include a supported timestamp")

    where: list[str] = []
    params: list[Any] = []
    if "metadata_id" in state_columns and sqlite_table_exists(conn, "states_meta"):
        meta = conn.execute("SELECT metadata_id FROM states_meta WHERE entity_id = ?", (entity_id,)).fetchone()
        if meta is None:
            return []
        where.append("metadata_id = ?")
        params.append(meta[0])
    elif "entity_id" in state_columns:
        where.append("entity_id = ?")
        params.append(entity_id)
    else:
        raise ValueError("Recorder states table does not identify entities")

    if timestamp_column.endswith("_ts"):
        where.append(f"{timestamp_column} >= ?")
        where.append(f"{timestamp_column} < ?")
        params.extend([start.astimezone(UTC).timestamp(), end.astimezone(UTC).timestamp()])
    else:
        where.append(f"{timestamp_column} >= ?")
        where.append(f"{timestamp_column} < ?")
        params.extend([start.astimezone(UTC).isoformat(), end.astimezone(UTC).isoformat()])

    sql = (
        f"SELECT state, {timestamp_column} FROM states "
        f"WHERE {' AND '.join(where)} "
        f"ORDER BY {timestamp_column}"
    )
    return list(conn.execute(sql, params))


def irrigation_by_day(
    db_path: Path,
    *,
    entity_id: str,
    day_keys: list[str],
    timezone: dt.tzinfo,
    max_daily_gallons: float,
) -> dict[str, float]:
    if not db_path.exists():
        raise FileNotFoundError(f"Recorder database not found: {db_path}")

    start_date = dt.date.fromisoformat(day_keys[0])
    end_date = dt.date.fromisoformat(day_keys[-1]) + dt.timedelta(days=1)
    start = dt.datetime.combine(start_date, dt.time.min, tzinfo=timezone)
    end = dt.datetime.combine(end_date, dt.time.min, tzinfo=timezone)

    buckets: dict[str, float] = {}
    uri = f"file:{db_path.as_posix()}?mode=ro"
    with sqlite3.connect(uri, uri=True, timeout=10) as conn:
        conn.execute("PRAGMA busy_timeout = 10000")
        for raw_state, raw_timestamp in recorder_rows(conn, entity_id=entity_id, start=start, end=end):
            try:
                value = float(raw_state)
            except (TypeError, ValueError):
                continue
            if value < 0 or value > max_daily_gallons:
                continue
            timestamp = parse_timestamp(raw_timestamp, timezone)
            if timestamp is None:
                continue
            key = timestamp.date().isoformat()
            if key in day_keys:
                buckets[key] = max(value, buckets.get(key, 0.0))
    return buckets


def rainfall_by_day(cache_path: Path, day_keys: list[str]) -> dict[str, float]:
    if not cache_path.exists():
        return {}
    days = read_json(cache_path).get("days")
    if not isinstance(days, list):
        return {}

    wanted = set(day_keys)
    buckets: dict[str, float] = {}
    for item in days:
        if not isinstance(item, dict):
            continue
        key = str(item.get("date") or "")
        if key not in wanted:
            continue
        try:
            value = float(item.get("rain_in", item.get("precipitation_in", 0)) or 0)
        except (TypeError, ValueError):
            continue
        buckets[key] = max(value, 0.0)
    return buckets


def clean_zone_name(value: Any) -> str:
    text = " ".join(str(value or "").split())
    for suffix in (
        " Daily active watering time",
        " Remaining watering time",
        " Watering",
    ):
        if text.endswith(suffix):
            return text[: -len(suffix)]
    return text


def is_generic_zone_name(value: str) -> bool:
    return value.strip().lower() in {
        "",
        "daily active watering time",
        "remaining watering time",
        "watering",
    }


def zone_display_names(config_dir: Path, zone_count: int) -> dict[str, str]:
    names = {f"Zone {index}": f"Zone {index}" for index in range(1, zone_count + 1)}
    registry_path = config_dir / ".storage" / "core.entity_registry"
    device_registry_path = config_dir / ".storage" / "core.device_registry"
    if not registry_path.exists():
        return names
    try:
        entities = read_json(registry_path).get("data", {}).get("entities", [])
    except Exception:
        return names
    if not isinstance(entities, list):
        return names

    devices: dict[str, dict[str, Any]] = {}
    if device_registry_path.exists():
        try:
            raw_devices = read_json(device_registry_path).get("data", {}).get("devices", [])
        except Exception:
            raw_devices = []
        if isinstance(raw_devices, list):
            devices = {
                str(device.get("id")): device
                for device in raw_devices
                if isinstance(device, dict) and device.get("id")
            }

    for entry in entities:
        if not isinstance(entry, dict):
            continue
        entity_id = str(entry.get("entity_id") or "")
        for index in range(1, zone_count + 1):
            if entity_id not in {
                f"valve.zone_{index}",
                f"binary_sensor.zone_{index}_watering",
                f"sensor.zone_{index}_daily_active_watering_time",
            }:
                continue
            device = devices.get(str(entry.get("device_id") or ""), {})
            device_name = clean_zone_name(device.get("name_by_user") or device.get("name") or "")
            if device_name and not is_generic_zone_name(device_name):
                names[f"Zone {index}"] = device_name
                continue
            raw_name = entry.get("name") or entry.get("original_name") or ""
            name = clean_zone_name(raw_name)
            if name and not is_generic_zone_name(name):
                names[f"Zone {index}"] = name
    return names


def add_zone(
    buckets: dict[str, dict[str, dict[str, Any]]],
    *,
    day: str,
    zone: str,
    zone_name: str,
    duration_minutes: float = 0.0,
    gallons: float = 0.0,
    source: str,
) -> None:
    if not day or not zone:
        return
    day_bucket = buckets.setdefault(day, {})
    existing = day_bucket.setdefault(
        zone,
        {
            "zone": zone,
            "zone_name": zone_name or zone,
            "duration_minutes": 0.0,
            "gallons": 0.0,
            "source": source,
        },
    )
    existing["zone_name"] = zone_name or existing["zone_name"]
    existing["duration_minutes"] = round(float(existing.get("duration_minutes") or 0) + max(duration_minutes, 0), 2)
    existing["gallons"] = round(float(existing.get("gallons") or 0) + max(gallons, 0), 2)
    existing["source"] = source


def zones_from_irrigation_history(
    history_path: Path,
    *,
    day_keys: list[str],
    timezone: dt.tzinfo,
) -> dict[str, list[dict[str, Any]]]:
    if not history_path.exists():
        return {}
    try:
        zone_runs = read_json(history_path).get("zone_runs", [])
    except Exception:
        return {}
    if not isinstance(zone_runs, list):
        return {}

    wanted = set(day_keys)
    buckets: dict[str, dict[str, dict[str, Any]]] = {}
    for run in zone_runs:
        if not isinstance(run, dict):
            continue
        timestamp = parse_timestamp(run.get("ended_at") or run.get("started_at"), timezone)
        if timestamp is None:
            continue
        key = timestamp.date().isoformat()
        if key not in wanted:
            continue
        zone = str(run.get("zone") or "").strip()
        zone_name = clean_zone_name(run.get("zone_name") or zone)
        add_zone(
            buckets,
            day=key,
            zone=zone,
            zone_name=zone_name,
            duration_minutes=safe_float(run.get("duration_minutes")),
            gallons=safe_float(run.get("gallons")),
            source="irrigation_history",
        )
    return finalize_zone_buckets(buckets)


def zones_from_hydrawise_daily_activity(
    db_path: Path,
    *,
    day_keys: list[str],
    timezone: dt.tzinfo,
    zone_names: dict[str, str],
    zone_count: int,
) -> dict[str, list[dict[str, Any]]]:
    if not db_path.exists():
        return {}

    start_date = dt.date.fromisoformat(day_keys[0])
    end_date = dt.date.fromisoformat(day_keys[-1]) + dt.timedelta(days=1)
    start = dt.datetime.combine(start_date, dt.time.min, tzinfo=timezone)
    end = dt.datetime.combine(end_date, dt.time.min, tzinfo=timezone)
    wanted = set(day_keys)
    max_seconds_by_day_zone: dict[tuple[str, str], float] = {}

    uri = f"file:{db_path.as_posix()}?mode=ro"
    with sqlite3.connect(uri, uri=True, timeout=10) as conn:
        conn.execute("PRAGMA busy_timeout = 10000")
        for index in range(1, zone_count + 1):
            entity_id = f"sensor.zone_{index}_daily_active_watering_time"
            zone = f"Zone {index}"
            try:
                rows = recorder_rows(conn, entity_id=entity_id, start=start, end=end)
            except Exception:
                continue
            for raw_state, raw_timestamp in rows:
                try:
                    seconds = float(raw_state)
                except (TypeError, ValueError):
                    continue
                if seconds <= 0 or seconds > 24 * 60 * 60:
                    continue
                timestamp = parse_timestamp(raw_timestamp, timezone)
                if timestamp is None:
                    continue
                key = timestamp.date().isoformat()
                if key not in wanted:
                    continue
                previous = max_seconds_by_day_zone.get((key, zone), 0.0)
                max_seconds_by_day_zone[(key, zone)] = max(previous, seconds)

    buckets: dict[str, dict[str, dict[str, Any]]] = {}
    for (day, zone), seconds in max_seconds_by_day_zone.items():
        add_zone(
            buckets,
            day=day,
            zone=zone,
            zone_name=zone_names.get(zone, zone),
            duration_minutes=seconds / 60,
            source="hydrawise_daily_active_time",
        )
    return finalize_zone_buckets(buckets)


def finalize_zone_buckets(buckets: dict[str, dict[str, dict[str, Any]]]) -> dict[str, list[dict[str, Any]]]:
    return {
        day: sorted(
            zones.values(),
            key=lambda item: (-float(item.get("duration_minutes") or 0), str(item.get("zone") or "")),
        )
        for day, zones in buckets.items()
    }


def merge_zone_sources(
    primary: dict[str, list[dict[str, Any]]],
    fallback: dict[str, list[dict[str, Any]]],
    day_keys: list[str],
) -> dict[str, list[dict[str, Any]]]:
    return {
        day: primary.get(day) or fallback.get(day) or []
        for day in day_keys
    }


def format_minutes(value: float) -> str:
    rounded = int(round(value))
    if rounded <= 0:
        return ""
    return f"{rounded} min"


def zones_label(zones: list[dict[str, Any]], gallons: float) -> str:
    if not zones:
        return "Zone history unavailable" if gallons > 0 else "No irrigation"
    names = [str(zone.get("zone_name") or zone.get("zone") or "Zone").strip() for zone in zones]
    total_minutes = sum(float(zone.get("duration_minutes") or 0) for zone in zones)
    minutes = format_minutes(total_minutes)
    if len(zones) == 1:
        return f"{names[0]} \u00b7 {minutes}" if minutes else names[0]
    if len(zones) > 6:
        return f"Full cycle \u00b7 {len(zones)} zones" if gallons >= 5000 else f"{len(zones)} zones"
    label = f"{names[0]} + {len(zones) - 1} more"
    return f"{label} \u00b7 {minutes}" if minutes else label


def rain_context(value: float) -> str:
    if value <= 0:
        return "No rain"
    if value < 0.05:
        return "Trace rain"
    if value < 0.2:
        return "Light rain"
    if value < 0.5:
        return "Useful rain"
    if value < 1.0:
        return "Solid soak"
    return "Heavy rain"


def format_gallons(value: float) -> str:
    return f"{int(round(value)):,}"


def format_inches(value: float) -> str:
    return f"{value:.2f}"


def day_summary(gallons: float, rain_in: float) -> str:
    if gallons >= 5000:
        return "Full irrigation run"
    if gallons > 0 and rain_in >= 0.1:
        return "Irrigation and rain"
    if gallons > 0:
        return "Irrigation ran"
    if rain_in >= 0.1:
        return "Rain covered the day"
    if rain_in > 0:
        return "Trace rain"
    return "Quiet"


def build_ledger(args: argparse.Namespace) -> dict[str, Any]:
    timezone = home_timezone(args.config_dir)
    today = dt.datetime.now(timezone).date()
    start_date = today - dt.timedelta(days=args.days - 1)
    day_dates = [start_date + dt.timedelta(days=index) for index in range(args.days)]
    day_keys = [day.isoformat() for day in day_dates]

    error = ""
    try:
        gallons_by_day = irrigation_by_day(
            args.db,
            entity_id=args.entity_id,
            day_keys=day_keys,
            timezone=timezone,
            max_daily_gallons=args.max_daily_gallons,
        )
    except Exception as exc:  # noqa: BLE001 - dashboard should degrade instead of failing.
        gallons_by_day = {}
        error = str(exc)

    rain_by_day = rainfall_by_day(args.rain_cache, day_keys)
    try:
        zone_names = zone_display_names(args.config_dir, args.zone_count)
        zones_by_day = merge_zone_sources(
            zones_from_irrigation_history(args.history_file, day_keys=day_keys, timezone=timezone),
            zones_from_hydrawise_daily_activity(
                args.db,
                day_keys=day_keys,
                timezone=timezone,
                zone_names=zone_names,
                zone_count=args.zone_count,
            ),
            day_keys,
        )
    except Exception as exc:  # noqa: BLE001 - zone context should not break the ledger.
        zones_by_day = {day: [] for day in day_keys}
        error = "; ".join(part for part in (error, f"Zone history unavailable: {exc}") if part)
    max_gallons = max([gallons_by_day.get(day, 0.0) for day in day_keys] + [0.0])
    max_rain = max([rain_by_day.get(day, 0.0) for day in day_keys] + [0.0])
    total_gallons = round(sum(gallons_by_day.get(day, 0.0) for day in day_keys), 1)
    total_rain = round(sum(rain_by_day.get(day, 0.0) for day in day_keys), 2)

    days = []
    for day in day_dates:
        key = day.isoformat()
        gallons = round(gallons_by_day.get(key, 0.0), 1)
        rain = round(rain_by_day.get(key, 0.0), 2)
        zones = zones_by_day.get(key, [])
        days.append(
            {
                "date": key,
                "weekday": day.strftime("%a"),
                "short_date": f"{day.strftime('%b')} {day.day}",
                "is_today": day == today,
                "gallons": gallons,
                "rain_in": rain,
                "gallons_label": f"{format_gallons(gallons)} gal",
                "rain_label": f"{format_inches(rain)} in",
                "rain_context": rain_context(rain),
                "zones": zones,
                "zones_label": zones_label(zones, gallons),
                "zone_source": zones[0].get("source", "") if zones else "",
                "summary": day_summary(gallons, rain),
                "irrigation_ratio": round(gallons / max_gallons, 4) if max_gallons > 0 else 0,
                "rain_ratio": round(rain / max_rain, 4) if max_rain > 0 else 0,
            }
        )

    return {
        "updated_at": iso_now(),
        "source_entity": args.entity_id,
        "source": "Recorder history, Hydrawise zone history, and Open-Meteo historical rainfall cache",
        "start_date": day_keys[0],
        "end_date": day_keys[-1],
        "day_count": args.days,
        "gallons_7_day": total_gallons,
        "rain_7_day_in": total_rain,
        "gallons_7_day_label": f"{format_gallons(total_gallons)} gallons",
        "rain_7_day_label": f"{format_inches(total_rain)} inches",
        "subtitle": f"Last 7 days: {format_gallons(total_gallons)} gallons, {format_inches(total_rain)} inches",
        "max_daily_gallons": round(max_gallons, 1),
        "max_daily_rain_in": round(max_rain, 2),
        "days": days,
        "error": error,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config-dir", type=Path, default=Path("/config"))
    parser.add_argument("--db", type=Path, default=Path("/config/home-assistant_v2.db"))
    parser.add_argument("--rain-cache", type=Path, default=Path("/config/.irrigation_rain_actuals.json"))
    parser.add_argument("--history-file", type=Path, default=Path("/config/.irrigation_history.json"))
    parser.add_argument("--entity-id", default="sensor.45_crr_daily_total_water_use")
    parser.add_argument("--days", type=int, default=7)
    parser.add_argument("--max-daily-gallons", type=float, default=50000.0)
    parser.add_argument("--zone-count", type=int, default=27)
    args = parser.parse_args(argv)
    args.days = max(args.days, 1)
    args.zone_count = max(args.zone_count, 1)

    print(json.dumps(build_ledger(args), sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
