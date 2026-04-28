#!/usr/bin/env python3
"""Return upcoming Metro-North departures for a Home Assistant command_line sensor."""

from __future__ import annotations

import argparse
import csv
import io
import json
import os
import ssl
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import zipfile
from dataclasses import dataclass
from datetime import datetime, time as datetime_time, timedelta
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo


STATIC_GTFS_URL = "https://rrgtfsfeeds.s3.amazonaws.com/gtfsmnr.zip"
REALTIME_GTFS_URL = "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/mnr%2Fgtfs-mnr"
DEFAULT_CACHE_DIR = "/tmp/mta_mnr_cache"
SECRET_NAMES = ("mta_api_key", "mta_mnr_api_key")


@dataclass
class Candidate:
    trip_id: str
    train: str
    headsign: str
    scheduled_departure: datetime
    departure: datetime
    scheduled_arrival: datetime | None
    arrival: datetime | None
    origin_sequence: int
    destination_sequence: int
    track: str
    track_source: str
    delay_minutes: int | None = None
    realtime: bool = False
    skipped: bool = False


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--origin-stop-id", default="76")
    parser.add_argument("--origin-stop-name", default="North White Plains")
    parser.add_argument("--destination-stop-id", default="1")
    parser.add_argument("--destination-stop-name", default="Grand Central")
    parser.add_argument("--route-id", default="2")
    parser.add_argument("--route-name", default="Harlem Line")
    parser.add_argument("--min-departure-minutes", type=int, default=20)
    parser.add_argument("--lookahead-hours", type=int, default=8)
    parser.add_argument("--limit", type=int, default=3)
    parser.add_argument("--timezone", default="America/New_York")
    parser.add_argument("--cache-dir", default=DEFAULT_CACHE_DIR)
    parser.add_argument("--static-url", default=STATIC_GTFS_URL)
    parser.add_argument("--realtime-url", default=REALTIME_GTFS_URL)
    parser.add_argument("--api-key")
    parser.add_argument("--api-key-file")
    parser.add_argument("--static-cache-hours", type=int, default=12)
    return parser.parse_args()


def output(payload: dict[str, Any]) -> None:
    json.dump(payload, sys.stdout, separators=(",", ":"))
    sys.stdout.write("\n")


def base_payload(args: argparse.Namespace, source: str, error: str | None = None) -> dict[str, Any]:
    now = datetime.now(ZoneInfo(args.timezone))
    return {
        "summary": "No catchable trains",
        "message": (
            f"No {args.destination_stop_name} trains more than "
            f"{args.min_departure_minutes} minutes out were found."
        ),
        "updated_at": now.isoformat(),
        "source": source,
        "realtime_available": False,
        "buffer_minutes": args.min_departure_minutes,
        "origin_stop_id": args.origin_stop_id,
        "origin_stop_name": args.origin_stop_name,
        "destination_stop_id": args.destination_stop_id,
        "destination_stop_name": args.destination_stop_name,
        "route_id": args.route_id,
        "route_name": args.route_name,
        "departures_label": "",
        "track_label": "",
        "trains": [],
        "error": error,
    }


def read_secret_from_file(path: Path) -> str | None:
    if not path.exists():
        return None
    try:
        for line in path.read_text(encoding="utf-8").splitlines():
            stripped = line.strip()
            if not stripped or stripped.startswith("#") or ":" not in stripped:
                continue
            key, value = stripped.split(":", 1)
            if key.strip() in SECRET_NAMES:
                return value.strip().strip("\"'")
    except OSError:
        return None
    return None


def resolve_api_key(args: argparse.Namespace) -> str | None:
    if args.api_key:
        return args.api_key
    env_key = os.environ.get("MTA_API_KEY") or os.environ.get("MTA_MNR_API_KEY")
    if env_key:
        return env_key
    if args.api_key_file:
        try:
            return Path(args.api_key_file).read_text(encoding="utf-8").strip()
        except OSError:
            return None
    for path in (Path("/config/secrets.yaml"), Path("secrets.yaml")):
        secret = read_secret_from_file(path)
        if secret:
            return secret
    return None


def fetch_url(url: str, headers: dict[str, str] | None = None, timeout: int = 20) -> bytes:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "HomeAssistant-MetroNorth-Commute/1.0",
            **(headers or {}),
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return response.read()
    except urllib.error.URLError as exc:
        if "CERTIFICATE_VERIFY_FAILED" not in str(exc):
            raise
        try:
            import certifi
        except ImportError:
            raise
        context = ssl.create_default_context(cafile=certifi.where())
        try:
            with urllib.request.urlopen(request, timeout=timeout, context=context) as response:
                return response.read()
        except urllib.error.URLError as certifi_exc:
            if "CERTIFICATE_VERIFY_FAILED" not in str(certifi_exc):
                raise
            if urllib.parse.urlparse(url).hostname != "api-endpoint.mta.info":
                raise
            context = ssl._create_unverified_context()
            with urllib.request.urlopen(request, timeout=timeout, context=context) as response:
                return response.read()


def cached_static_zip(args: argparse.Namespace) -> Path:
    cache_dir = Path(args.cache_dir)
    cache_dir.mkdir(parents=True, exist_ok=True)
    zip_path = cache_dir / "gtfsmnr.zip"
    max_age = args.static_cache_hours * 60 * 60
    if zip_path.exists() and time.time() - zip_path.stat().st_mtime < max_age:
        return zip_path

    data = fetch_url(args.static_url, timeout=30)
    tmp_path = zip_path.with_suffix(".zip.tmp")
    tmp_path.write_bytes(data)
    tmp_path.replace(zip_path)
    return zip_path


def csv_rows(feed: zipfile.ZipFile, name: str) -> list[dict[str, str]]:
    with feed.open(name) as handle:
        text = io.TextIOWrapper(handle, encoding="utf-8-sig", newline="")
        return list(csv.DictReader(text))


def service_active_on(row: dict[str, str], service_date: datetime.date, weekday_name: str) -> bool:
    start = row.get("start_date", "")
    end = row.get("end_date", "")
    date_key = service_date.strftime("%Y%m%d")
    return start <= date_key <= end and row.get(weekday_name, "0") == "1"


def active_services_by_date(
    feed: zipfile.ZipFile, service_dates: list[datetime.date]
) -> dict[datetime.date, set[str]]:
    active = {service_date: set() for service_date in service_dates}
    weekday_names = {
        0: "monday",
        1: "tuesday",
        2: "wednesday",
        3: "thursday",
        4: "friday",
        5: "saturday",
        6: "sunday",
    }

    names = set(feed.namelist())
    if "calendar.txt" in names:
        for row in csv_rows(feed, "calendar.txt"):
            for service_date in service_dates:
                weekday = weekday_names[service_date.weekday()]
                if service_active_on(row, service_date, weekday):
                    active[service_date].add(row["service_id"])

    if "calendar_dates.txt" in names:
        for row in csv_rows(feed, "calendar_dates.txt"):
            try:
                service_date = datetime.strptime(row["date"], "%Y%m%d").date()
            except (KeyError, ValueError):
                continue
            if service_date not in active:
                continue
            if row.get("exception_type") == "1":
                active[service_date].add(row["service_id"])
            elif row.get("exception_type") == "2":
                active[service_date].discard(row["service_id"])
    return active


def gtfs_time_to_datetime(service_date: datetime.date, value: str, tz: ZoneInfo) -> datetime:
    hour, minute, second = [int(part) for part in value.split(":")]
    midnight = datetime.combine(service_date, datetime_time(0, 0, 0), tzinfo=tz)
    return midnight + timedelta(hours=hour, minutes=minute, seconds=second)


def load_static_candidates(args: argparse.Namespace, now: datetime) -> list[Candidate]:
    zip_path = cached_static_zip(args)
    service_dates = [now.date(), (now + timedelta(days=1)).date()]
    candidates: list[Candidate] = []

    with zipfile.ZipFile(zip_path) as feed:
        active_by_date = active_services_by_date(feed, service_dates)
        service_dates_by_id: dict[str, list[datetime.date]] = {}
        for service_date, service_ids in active_by_date.items():
            for service_id in service_ids:
                service_dates_by_id.setdefault(service_id, []).append(service_date)

        trips: dict[str, dict[str, Any]] = {}
        for row in csv_rows(feed, "trips.txt"):
            if row.get("route_id") != args.route_id:
                continue
            dates = service_dates_by_id.get(row.get("service_id", ""), [])
            if not dates:
                continue
            trips[row["trip_id"]] = {
                "dates": dates,
                "headsign": row.get("trip_headsign", ""),
                "train": row.get("trip_short_name", ""),
            }

        stop_rows: dict[str, dict[str, dict[str, str]]] = {
            trip_id: {} for trip_id in trips
        }
        with feed.open("stop_times.txt") as handle:
            text = io.TextIOWrapper(handle, encoding="utf-8-sig", newline="")
            for row in csv.DictReader(text):
                trip_id = row.get("trip_id", "")
                if trip_id not in stop_rows:
                    continue
                stop_id = row.get("stop_id", "")
                if stop_id == args.origin_stop_id:
                    stop_rows[trip_id]["origin"] = row
                elif stop_id == args.destination_stop_id:
                    stop_rows[trip_id]["destination"] = row

    for trip_id, stops in stop_rows.items():
        origin = stops.get("origin")
        destination = stops.get("destination")
        if not origin or not destination:
            continue
        try:
            origin_sequence = int(origin["stop_sequence"])
            destination_sequence = int(destination["stop_sequence"])
        except (KeyError, ValueError):
            continue
        if origin_sequence >= destination_sequence:
            continue

        trip = trips[trip_id]
        for service_date in trip["dates"]:
            scheduled_departure = gtfs_time_to_datetime(
                service_date,
                origin.get("departure_time") or origin.get("arrival_time", ""),
                now.tzinfo,
            )
            scheduled_arrival = gtfs_time_to_datetime(
                service_date,
                destination.get("arrival_time") or destination.get("departure_time", ""),
                now.tzinfo,
            )
            if scheduled_departure < now - timedelta(hours=2):
                continue
            if scheduled_departure > now + timedelta(hours=args.lookahead_hours):
                continue
            candidates.append(
                Candidate(
                    trip_id=trip_id,
                    train=trip["train"],
                    headsign=trip["headsign"],
                    scheduled_departure=scheduled_departure,
                    departure=scheduled_departure,
                    scheduled_arrival=scheduled_arrival,
                    arrival=scheduled_arrival,
                    origin_sequence=origin_sequence,
                    destination_sequence=destination_sequence,
                    track=(origin.get("track") or "").strip(),
                    track_source="scheduled" if (origin.get("track") or "").strip() else "unknown",
                )
            )

    return candidates


def read_varint(data: bytes, pos: int) -> tuple[int, int]:
    shift = 0
    result = 0
    while True:
        if pos >= len(data):
            raise ValueError("unexpected end of protobuf varint")
        byte = data[pos]
        pos += 1
        result |= (byte & 0x7F) << shift
        if not byte & 0x80:
            return result, pos
        shift += 7
        if shift > 70:
            raise ValueError("protobuf varint too long")


def iter_fields(data: bytes):
    pos = 0
    while pos < len(data):
        key, pos = read_varint(data, pos)
        field_number = key >> 3
        wire_type = key & 0x7
        if wire_type == 0:
            value, pos = read_varint(data, pos)
        elif wire_type == 1:
            value = data[pos : pos + 8]
            pos += 8
        elif wire_type == 2:
            length, pos = read_varint(data, pos)
            value = data[pos : pos + length]
            pos += length
        elif wire_type == 5:
            value = data[pos : pos + 4]
            pos += 4
        else:
            raise ValueError(f"unsupported protobuf wire type {wire_type}")
        yield field_number, wire_type, value


def proto_text(value: bytes) -> str:
    return value.decode("utf-8", errors="replace")


def parse_stop_time_event(data: bytes) -> dict[str, int]:
    event: dict[str, int] = {}
    for field, wire, value in iter_fields(data):
        if wire != 0:
            continue
        if field == 1:
            event["delay"] = int(value)
        elif field == 2:
            event["time"] = int(value)
    return event


def parse_stop_time_properties(data: bytes) -> dict[str, str]:
    properties: dict[str, str] = {}
    for field, wire, value in iter_fields(data):
        if field == 1 and wire == 2:
            properties["assigned_stop_id"] = proto_text(value)
    return properties


def parse_mta_railroad_stop_time_update(data: bytes) -> dict[str, str]:
    extension: dict[str, str] = {}
    for field, wire, value in iter_fields(data):
        if field == 1 and wire == 2:
            extension["track"] = proto_text(value)
        elif field == 2 and wire == 2:
            extension["train_status"] = proto_text(value)
    return extension


def parse_stop_time_update(data: bytes) -> dict[str, Any]:
    update: dict[str, Any] = {}
    for field, wire, value in iter_fields(data):
        if field == 1 and wire == 0:
            update["stop_sequence"] = int(value)
        elif field == 2 and wire == 2:
            update["arrival"] = parse_stop_time_event(value)
        elif field == 3 and wire == 2:
            update["departure"] = parse_stop_time_event(value)
        elif field == 4 and wire == 2:
            update["stop_id"] = proto_text(value)
        elif field == 5 and wire == 0:
            update["schedule_relationship"] = int(value)
        elif field == 6 and wire == 2:
            update["stop_time_properties"] = parse_stop_time_properties(value)
        elif field == 1005 and wire == 2:
            update["mta_railroad_stop_time_update"] = parse_mta_railroad_stop_time_update(value)
    return update


def parse_trip_descriptor(data: bytes) -> dict[str, Any]:
    descriptor: dict[str, Any] = {}
    for field, wire, value in iter_fields(data):
        if field == 2 and wire == 2:
            descriptor["start_date"] = proto_text(value)
        elif field == 3 and wire == 2:
            descriptor["trip_id"] = proto_text(value)
        elif field == 4 and wire == 0:
            descriptor["schedule_relationship"] = int(value)
        elif field == 5 and wire == 2:
            descriptor["route_id"] = proto_text(value)
    return descriptor


def parse_trip_update(data: bytes) -> dict[str, Any] | None:
    trip: dict[str, Any] = {}
    stop_updates: list[dict[str, Any]] = []
    for field, wire, value in iter_fields(data):
        if field == 1 and wire == 2:
            trip = parse_trip_descriptor(value)
        elif field == 2 and wire == 2:
            stop_updates.append(parse_stop_time_update(value))
    trip_id = trip.get("trip_id")
    if not trip_id:
        return None
    return {
        "trip_id": trip_id,
        "route_id": trip.get("route_id"),
        "schedule_relationship": trip.get("schedule_relationship"),
        "stop_updates": stop_updates,
    }


def parse_feed_entity(data: bytes) -> dict[str, Any] | None:
    entity_id: str | None = None
    update: dict[str, Any] | None = None
    for field, wire, value in iter_fields(data):
        if field == 1 and wire == 2:
            entity_id = proto_text(value)
        elif field == 3 and wire == 2:
            update = parse_trip_update(value)
    if update and entity_id:
        update["entity_id"] = entity_id
    return update


def parse_realtime_trip_updates(data: bytes) -> dict[str, dict[str, Any]]:
    updates: dict[str, dict[str, Any]] = {}
    for field, wire, value in iter_fields(data):
        if field != 2 or wire != 2:
            continue
        update = parse_feed_entity(value)
        if update:
            updates[update["trip_id"]] = update
            entity_id = update.get("entity_id")
            if entity_id:
                updates[entity_id] = update
    return updates


def find_stop_update(update: dict[str, Any], stop_id: str, sequence: int) -> dict[str, Any] | None:
    for stop_update in update.get("stop_updates", []):
        if stop_update.get("stop_id") == stop_id:
            return stop_update
        if stop_update.get("stop_sequence") == sequence:
            return stop_update
    return None


def event_datetime(
    event: dict[str, int] | None,
    scheduled: datetime,
) -> datetime | None:
    if not event:
        return None
    if "time" in event:
        return datetime.fromtimestamp(event["time"], tz=scheduled.tzinfo)
    if "delay" in event:
        return scheduled + timedelta(seconds=event["delay"])
    return None


def apply_realtime(
    candidates: list[Candidate], args: argparse.Namespace, api_key: str | None
) -> tuple[bool, str | None]:
    try:
        headers = {"Accept": "application/x-protobuf"}
        if api_key:
            headers["x-api-key"] = api_key
        data = fetch_url(
            args.realtime_url,
            headers=headers,
            timeout=20,
        )
        updates = parse_realtime_trip_updates(data)
    except (OSError, ValueError, urllib.error.URLError, urllib.error.HTTPError) as exc:
        return False, f"Realtime unavailable; using scheduled times. {exc}"

    for candidate in candidates:
        update = updates.get(candidate.trip_id) or updates.get(candidate.train)
        if not update:
            continue
        if update.get("schedule_relationship") == 3:
            candidate.skipped = True
            continue

        origin_update = find_stop_update(update, args.origin_stop_id, candidate.origin_sequence)
        if origin_update:
            if origin_update.get("schedule_relationship") == 1:
                candidate.skipped = True
                continue
            departure = event_datetime(
                origin_update.get("departure") or origin_update.get("arrival"),
                candidate.scheduled_departure,
            )
            if departure:
                candidate.departure = departure
                candidate.realtime = True
                delay = departure - candidate.scheduled_departure
                candidate.delay_minutes = round(delay.total_seconds() / 60)

            assigned_stop_id = (
                origin_update.get("stop_time_properties", {}).get("assigned_stop_id")
            )
            if assigned_stop_id and assigned_stop_id != args.origin_stop_id:
                candidate.track = assigned_stop_id
                candidate.track_source = "realtime"
            realtime_track = (
                origin_update.get("mta_railroad_stop_time_update", {}).get("track")
            )
            if realtime_track:
                candidate.track = realtime_track
                candidate.track_source = "realtime"

        destination_update = find_stop_update(
            update, args.destination_stop_id, candidate.destination_sequence
        )
        if destination_update:
            arrival = event_datetime(
                destination_update.get("arrival") or destination_update.get("departure"),
                candidate.scheduled_arrival or candidate.departure,
            )
            if arrival:
                candidate.arrival = arrival

    return True, None


def time_label(value: datetime) -> str:
    return value.strftime("%-I:%M %p").lower()


def delay_label(delay_minutes: int | None) -> str:
    if delay_minutes is None:
        return "scheduled"
    if delay_minutes >= 2:
        return f"{delay_minutes} min late"
    if delay_minutes <= -2:
        return f"{abs(delay_minutes)} min early"
    return "on time"


def track_label(track: str) -> str:
    return f"T{track}" if track.isdigit() else track


def train_payload(candidate: Candidate, now: datetime) -> dict[str, Any]:
    arrival = candidate.arrival
    minutes_until = max(0, round((candidate.departure - now).total_seconds() / 60))
    duration_minutes = (
        max(0, round((arrival - candidate.departure).total_seconds() / 60))
        if arrival
        else None
    )
    return {
        "train": candidate.train,
        "headsign": candidate.headsign,
        "departure": candidate.departure.isoformat(),
        "departure_label": time_label(candidate.departure),
        "scheduled_departure": candidate.scheduled_departure.isoformat(),
        "arrival": arrival.isoformat() if arrival else None,
        "arrival_label": time_label(arrival) if arrival else "",
        "duration_minutes": duration_minutes,
        "track": candidate.track or "TBA",
        "track_label": track_label(candidate.track) if candidate.track else "TBA",
        "track_source": candidate.track_source,
        "minutes_until": minutes_until,
        "delay_minutes": candidate.delay_minutes,
        "status": delay_label(candidate.delay_minutes),
        "realtime": candidate.realtime,
    }


def train_message(train: dict[str, Any]) -> str:
    duration = train.get("duration_minutes")
    duration_label = f" ({duration} min)" if duration is not None else ""
    return (
        f"{train['minutes_until']} min: "
        f"{train['departure_label']}, {train['track_label']}{duration_label}"
    )


def main() -> None:
    args = parse_args()
    tz = ZoneInfo(args.timezone)
    now = datetime.now(tz)
    payload = base_payload(args, "static_schedule")

    try:
        candidates = load_static_candidates(args, now)
    except (OSError, zipfile.BadZipFile, KeyError, ValueError) as exc:
        payload["source"] = "unavailable"
        payload["error"] = f"Unable to load Metro-North schedule. {exc}"
        output(payload)
        return

    realtime_available, realtime_error = apply_realtime(candidates, args, resolve_api_key(args))
    payload["realtime_available"] = realtime_available
    payload["source"] = "realtime" if realtime_available else "static_schedule"
    payload["error"] = realtime_error

    earliest = now + timedelta(minutes=args.min_departure_minutes)
    latest = now + timedelta(hours=args.lookahead_hours)
    catchable = [
        candidate
        for candidate in candidates
        if not candidate.skipped and earliest < candidate.departure <= latest
    ]
    catchable.sort(key=lambda candidate: candidate.departure)
    selected = catchable[: args.limit]

    trains = [train_payload(candidate, now) for candidate in selected]
    payload["trains"] = trains
    payload["departures_label"] = ", ".join(train["departure_label"] for train in trains)
    payload["track_label"] = ", ".join(
        f"{train['departure_label']} {train['track_label']}" for train in trains
    )

    if trains:
        first = trains[0]
        payload["summary"] = f"{first['departure_label']} {first['track_label']}"
        payload["message"] = "\n".join(train_message(train) for train in trains)

    output(payload)


if __name__ == "__main__":
    main()
