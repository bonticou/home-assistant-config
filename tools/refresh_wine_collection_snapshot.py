#!/usr/bin/env python3

import csv
import io
import json
from collections import Counter
from datetime import datetime
from pathlib import Path
from urllib.error import URLError
from urllib.request import Request, urlopen


SHEET_ID = "13f61tOxK8E61GL3phvjiBzCuyYRybymtKPGOduIOvDc"
SHEET_GID = "1865301611"
SHEET_URL = (
    f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/edit"
    f"?gid={SHEET_GID}#gid={SHEET_GID}"
)
CSV_URL = (
    f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export"
    f"?format=csv&gid={SHEET_GID}"
)
READY_PHASES = {"early", "stabilizing", "mature"}
HOLD_PHASES = {"premature"}
STYLE_ALIASES = {
    "Bordeaux red blend": "Bordeaux blend",
    "Bordeaux-style red blend": "Bordeaux blend",
    "Cabernet Franc": "Cab Franc",
    "Southern Rhone red blend (Grenache-led)": "Rhone blend",
    "Southern Rhône red blend (Grenache-led)": "Rhone blend",
    "Tempranillo-based red blend": "Rioja blend",
    "Grenache (85%), Syrah (15%)": "Grenache/Syrah",
    "Sangiovese-based blend": "Sangiovese blend",
}
ROOT = Path(__file__).resolve().parent.parent
CACHE_PATH = ROOT / ".wine_collection_snapshot.json"


def clean(value):
    return " ".join((value or "").strip().split())


def parse_int(value):
    raw = clean(value)
    if not raw:
        return 0
    try:
        return int(float(raw))
    except ValueError:
        return 0


def short_time(dt):
    hour = dt.hour % 12 or 12
    suffix = "a" if dt.hour < 12 else "p"
    return f"{hour}:{dt.minute:02d}{suffix}"


def stamp_label(dt):
    return f"{dt.strftime('%b')} {dt.day} · {short_time(dt)}"


def normalize_style(style):
    normalized = clean(style)
    return STYLE_ALIASES.get(normalized, normalized or "Unclassified")


def inventory_rows(csv_text):
    rows = []
    for row in csv.DictReader(io.StringIO(csv_text)):
        producer = clean(row.get("Producer"))
        wine = clean(row.get("Wine"))
        qty = parse_int(row.get("Qty"))
        if qty <= 0:
            continue
        if not producer and not wine:
            continue
        normalized = {
            "phase": clean(row.get("Phase")).lower(),
            "producer": producer,
            "wine": wine,
            "country": clean(row.get("Country")),
            "region": clean(row.get("Region")),
            "style": normalize_style(row.get("Style")),
            "vintage": clean(row.get("Vintage")),
            "vintage_year": parse_int(row.get("Vintage")),
            "qty": qty,
            "from_year": parse_int(row.get("From")),
            "to_year": parse_int(row.get("To")),
        }
        rows.append(normalized)
    return rows


def display_name(row):
    if row["vintage"]:
        return f"{row['wine']} {row['vintage']}"
    return row["wine"] or row["producer"] or "Unnamed bottle"


def bottle_kind(row):
    if row["style"] != "Unclassified":
        return row["style"]
    if row["region"]:
        return row["region"]
    if row["country"]:
        return row["country"]
    return "Cellar"


def bucket_row(row, mode):
    kind = bottle_kind(row)
    if mode == "hold":
        kind = f"opens {row['from_year']}" if row["from_year"] else "Hold"
    return {
        "qty": f"{row['qty']}x",
        "name": display_name(row),
        "kind": kind,
    }


def sort_bucket(rows, mode):
    key_fn = lambda row: (
        row["vintage_year"] or 9999,
        display_name(row).lower(),
        bottle_kind(row).lower(),
    )
    return [bucket_row(row, mode) for row in sorted(rows, key=key_fn)]


def top_rows(counter, limit=5):
    return [
        {"label": label, "value": value}
        for label, value in sorted(counter.items(), key=lambda item: (-item[1], item[0]))[:limit]
        if label
    ]


def build_snapshot(csv_text, source):
    rows = inventory_rows(csv_text)
    ready_rows = [row for row in rows if row["phase"] in READY_PHASES]
    hold_rows = [row for row in rows if row["phase"] in HOLD_PHASES]
    unknown_rows = [row for row in rows if row["phase"] not in READY_PHASES | HOLD_PHASES]

    phase_counts = Counter()
    style_counts = Counter()
    region_counts = Counter()
    country_counts = Counter()
    for row in ready_rows:
        phase_counts[row["phase"]] += row["qty"]
        style_counts[row["style"]] += row["qty"]
        if row["region"]:
            region_counts[row["region"]] += row["qty"]
        if row["country"]:
            country_counts[row["country"]] += row["qty"]

    now = datetime.now().astimezone()
    return {
        "sheet_url": SHEET_URL,
        "data_source": source,
        "refreshed_at": now.isoformat(timespec="seconds"),
        "refreshed_label": stamp_label(now),
        "total_bottles": sum(row["qty"] for row in rows),
        "ready_total": sum(row["qty"] for row in ready_rows),
        "stabilizing_total": phase_counts.get("stabilizing", 0),
        "mature_total": phase_counts.get("mature", 0),
        "early_total": phase_counts.get("early", 0),
        "hold_total": sum(row["qty"] for row in hold_rows),
        "unknown_total": sum(row["qty"] for row in unknown_rows),
        "ready_styles": top_rows(style_counts, 5),
        "ready_regions": top_rows(region_counts, 5),
        "ready_countries": top_rows(country_counts, 5),
        "stabilizing_rows": sort_bucket(
            [row for row in ready_rows if row["phase"] == "stabilizing"],
            "stabilizing",
        ),
        "mature_rows": sort_bucket(
            [row for row in ready_rows if row["phase"] == "mature"],
            "mature",
        ),
        "early_rows": sort_bucket(
            [row for row in ready_rows if row["phase"] == "early"],
            "early",
        ),
        "hold_rows": sort_bucket(hold_rows, "hold"),
    }


def fetch_csv():
    request = Request(CSV_URL, headers={"User-Agent": "HomeAssistantWineSnapshot/1.0"})
    with urlopen(request, timeout=30) as response:
        return response.read().decode("utf-8-sig")


def load_cache():
    if not CACHE_PATH.exists():
        return None
    try:
        return json.loads(CACHE_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def write_cache(snapshot):
    CACHE_PATH.write_text(
        json.dumps(snapshot, ensure_ascii=True, separators=(",", ":")),
        encoding="utf-8",
    )


def main():
    try:
        snapshot = build_snapshot(fetch_csv(), "live")
        write_cache(snapshot)
    except (OSError, URLError, TimeoutError, ValueError):
        snapshot = load_cache()
        if snapshot is None:
            fallback_now = datetime.now().astimezone()
            snapshot = {
                "sheet_url": SHEET_URL,
                "data_source": "fallback",
                "refreshed_at": fallback_now.isoformat(timespec="seconds"),
                "refreshed_label": stamp_label(fallback_now),
                "total_bottles": 92,
                "ready_total": 70,
                "stabilizing_total": 35,
                "mature_total": 19,
                "early_total": 16,
                "hold_total": 12,
                "unknown_total": 10,
                "ready_styles": [
                    {"label": "Bordeaux blend", "value": 22},
                    {"label": "Nebbiolo", "value": 17},
                    {"label": "Pinot Noir", "value": 7},
                    {"label": "Super Tuscan", "value": 5},
                    {"label": "Red blend", "value": 4},
                ],
                "ready_regions": [
                    {"label": "Piedmont", "value": 17},
                    {"label": "California", "value": 16},
                    {"label": "Bordeaux", "value": 15},
                    {"label": "Tuscany", "value": 13},
                    {"label": "Mendoza", "value": 3},
                ],
                "ready_countries": [
                    {"label": "Italy", "value": 35},
                    {"label": "USA", "value": 19},
                    {"label": "France", "value": 16},
                ],
                "stabilizing_rows": [
                    {"qty": "3x", "name": "Saint-Julien 2019", "kind": "Bordeaux blend"},
                    {"qty": "3x", "name": "Barolo Ginestra DOCG 2018", "kind": "Nebbiolo"},
                    {"qty": "3x", "name": "Barolo Ravera 2021", "kind": "Nebbiolo"},
                    {"qty": "3x", "name": "Kissing Vipers 2021", "kind": "Grenache/Syrah"},
                ],
                "mature_rows": [
                    {"qty": "3x", "name": "Pessac-Leognan Rouge 2016", "kind": "Bordeaux blend"},
                    {"qty": "4x", "name": "Abstract Red", "kind": "Red blend"},
                    {"qty": "2x", "name": "Enrico VI (Villero) 2004", "kind": "Nebbiolo"},
                    {"qty": "2x", "name": "Papillon", "kind": "Bordeaux blend"},
                ],
                "early_rows": [
                    {"qty": "3x", "name": "Pessac-Leognan Rouge 2022", "kind": "Bordeaux blend"},
                    {"qty": "3x", "name": "Tongue 'N Cheek 2022", "kind": "Pinot Noir"},
                    {"qty": "3x", "name": "Tignanello 2022", "kind": "Sangiovese blend"},
                    {"qty": "3x", "name": "Cabernet Sauvignon 2023", "kind": "Cabernet Sauvignon"},
                ],
                "hold_rows": [
                    {"qty": "3x", "name": "Barolo Ravera 2021", "kind": "opens 2027"},
                    {"qty": "3x", "name": "Margaux 2022", "kind": "opens 2035"},
                    {"qty": "3x", "name": "Saint-Emilion Grand Cru 2022", "kind": "opens 2037"},
                    {"qty": "3x", "name": "Sidecar 2021", "kind": "opens 2028"},
                ],
            }

    print(json.dumps(snapshot, ensure_ascii=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
