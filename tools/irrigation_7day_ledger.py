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
    max_gallons = max([gallons_by_day.get(day, 0.0) for day in day_keys] + [0.0])
    max_rain = max([rain_by_day.get(day, 0.0) for day in day_keys] + [0.0])
    total_gallons = round(sum(gallons_by_day.get(day, 0.0) for day in day_keys), 1)
    total_rain = round(sum(rain_by_day.get(day, 0.0) for day in day_keys), 2)

    days = []
    for day in day_dates:
        key = day.isoformat()
        gallons = round(gallons_by_day.get(key, 0.0), 1)
        rain = round(rain_by_day.get(key, 0.0), 2)
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
                "summary": day_summary(gallons, rain),
                "irrigation_ratio": round(gallons / max_gallons, 4) if max_gallons > 0 else 0,
                "rain_ratio": round(rain / max_rain, 4) if max_rain > 0 else 0,
            }
        )

    return {
        "updated_at": iso_now(),
        "source_entity": args.entity_id,
        "source": "Recorder history plus Open-Meteo historical rainfall cache",
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
    parser.add_argument("--entity-id", default="sensor.45_crr_daily_total_water_use")
    parser.add_argument("--days", type=int, default=7)
    parser.add_argument("--max-daily-gallons", type=float, default=50000.0)
    args = parser.parse_args(argv)
    args.days = max(args.days, 1)

    print(json.dumps(build_ledger(args), sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
