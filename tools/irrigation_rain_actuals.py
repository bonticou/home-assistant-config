#!/usr/bin/env python3
"""Fetch recent historical rainfall actuals for irrigation context.

The sensor output intentionally omits latitude/longitude so Home Assistant
state history and repo artifacts do not expose the home location.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import sys
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any


OPEN_METEO_ARCHIVE_URL = "https://archive-api.open-meteo.com/v1/archive"


def iso_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")


def read_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    return payload if isinstance(payload, dict) else {}


def home_location(config_dir: Path) -> tuple[float, float, str]:
    core_config = config_dir / ".storage" / "core.config"
    if core_config.exists():
        data = read_json(core_config).get("data") or {}
        latitude = data.get("latitude")
        longitude = data.get("longitude")
        if isinstance(latitude, (int, float)) and isinstance(longitude, (int, float)):
            return float(latitude), float(longitude), "home_assistant_core_config"

    env_lat = os.environ.get("HA_LATITUDE")
    env_lon = os.environ.get("HA_LONGITUDE")
    if env_lat and env_lon:
        return float(env_lat), float(env_lon), "environment"

    raise ValueError("Home latitude/longitude were not available")


def fetch_archive(latitude: float, longitude: float, start_date: dt.date, end_date: dt.date, timeout: float) -> dict[str, Any]:
    params = {
        "latitude": f"{latitude:.5f}",
        "longitude": f"{longitude:.5f}",
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
        "daily": "rain_sum,precipitation_sum",
        "timezone": "auto",
        "precipitation_unit": "inch",
        "temperature_unit": "fahrenheit",
        "wind_speed_unit": "mph",
        "timeformat": "iso8601",
    }
    url = f"{OPEN_METEO_ARCHIVE_URL}?{urllib.parse.urlencode(params)}"
    request = urllib.request.Request(url, headers={"User-Agent": "HA-Irrigation-Rain-Actuals/1.0"})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def normalize_days(payload: dict[str, Any]) -> list[dict[str, Any]]:
    daily = payload.get("daily") if isinstance(payload, dict) else {}
    if not isinstance(daily, dict):
        return []

    dates = daily.get("time") or []
    rain = daily.get("rain_sum") or []
    precipitation = daily.get("precipitation_sum") or []
    days: list[dict[str, Any]] = []

    for index, raw_date in enumerate(dates):
        rain_value = rain[index] if index < len(rain) else None
        precip_value = precipitation[index] if index < len(precipitation) else None
        try:
            rain_in = float(rain_value)
        except (TypeError, ValueError):
            rain_in = None
        try:
            precipitation_in = float(precip_value)
        except (TypeError, ValueError):
            precipitation_in = None

        value = rain_in if rain_in is not None else precipitation_in
        if value is None:
            continue
        days.append(
            {
                "date": str(raw_date),
                "rain_in": round(max(value, 0.0), 2),
                "precipitation_in": round(max(precipitation_in if precipitation_in is not None else value, 0.0), 2),
            }
        )
    return days


def build_status(days: list[dict[str, Any]], *, location_source: str, start_date: dt.date, end_date: dt.date) -> dict[str, Any]:
    latest = days[-1] if days else {}
    total = sum(float(day.get("rain_in") or 0) for day in days)
    return {
        "updated_at": iso_now(),
        "source": "Open-Meteo Historical Weather API",
        "source_type": "historical_reanalysis",
        "location_source": location_source,
        "unit": "in",
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
        "day_count": len(days),
        "latest_date": latest.get("date", "unknown"),
        "latest_rain_in": round(float(latest.get("rain_in") or 0), 2),
        "total_rain_in": round(total, 2),
        "days": days,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config-dir", type=Path, default=Path("/config"))
    parser.add_argument("--cache-file", type=Path, default=Path("/config/.irrigation_rain_actuals.json"))
    parser.add_argument("--days", type=int, default=14)
    parser.add_argument("--timeout", type=float, default=20.0)
    args = parser.parse_args(argv)

    today = dt.date.today()
    start_date = today - dt.timedelta(days=max(args.days, 1) - 1)
    end_date = today

    try:
        latitude, longitude, location_source = home_location(args.config_dir)
        payload = fetch_archive(latitude, longitude, start_date, end_date, args.timeout)
        status = build_status(normalize_days(payload), location_source=location_source, start_date=start_date, end_date=end_date)
        args.cache_file.write_text(json.dumps(status, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    except Exception as exc:  # noqa: BLE001 - HA sensor should degrade to cached context.
        if args.cache_file.exists():
            status = read_json(args.cache_file)
            status["stale"] = True
            status["error"] = str(exc)
            status["updated_at"] = status.get("updated_at") or iso_now()
        else:
            status = {
                "updated_at": iso_now(),
                "source": "Open-Meteo Historical Weather API",
                "source_type": "historical_reanalysis",
                "unit": "in",
                "day_count": 0,
                "latest_date": "unknown",
                "latest_rain_in": 0,
                "total_rain_in": 0,
                "days": [],
                "error": str(exc),
            }

    print(json.dumps(status, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
