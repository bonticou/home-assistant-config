#!/usr/bin/env python3
"""Generate a Home Assistant Recorder inventory and review report."""

from __future__ import annotations

import argparse
import datetime as dt
import fnmatch
import json
import re
import sqlite3
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


SCHEMA_VERSION = 1

SUMMARY_RE = re.compile(
    r"(timeline|digest|schedule|summary|snapshot|context|status|history|reason|message|notice|"
    r"source_map|weather_window|metro_north|commute)",
    re.I,
)
SIGNAL_RE = re.compile(r"(signal|rssi|lqi|linkquality|wi[-_ ]?fi.*signal)", re.I)
INFRA_RE = re.compile(
    r"(cpu|memory|storage|disk|uptime|utilization|throughput|tx|rx|download|upload|"
    r"experience|latency|ping|firmware|version|temperature_alarm|connection_state)",
    re.I,
)
CONFIG_RE = re.compile(
    r"(motion|recording|microphone|status_light|ssh|rtsp|overlay|osd|led|beep|chime|"
    r"privacy|hdr|ir|infrared|sensitivity|volume|mode|setting|config)",
    re.I,
)
EVENT_HISTORY_RE = re.compile(
    r"(motion|person|occupancy|door|window|garage|lock|valve|leak|water|smoke|co_|"
    r"carbon|safety|security|alarm|presence|away|home)",
    re.I,
)
ENVIRONMENT_RE = re.compile(
    r"(temperature|humidity|radon|pressure|dew|moisture|water_pressure|flow|voltage|"
    r"current|power|energy|battery|illuminance|rain|wind|uv)",
    re.I,
)

LOW_VALUE_PLATFORMS = {
    "unifi",
    "unifiprotect",
    "upnp",
    "hacs",
    "hassio",
}
CONTROL_CONFIG_DOMAINS = {"button", "number", "select", "update"}
LOW_VALUE_DOMAINS = {"camera", "event", "image"}
REVIEW_DOMAINS = {"automation", "script", "media_player", "device_tracker"}


def utc_now() -> str:
    return dt.datetime.now(dt.UTC).replace(microsecond=0).isoformat()


def read_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8", errors="replace") as handle:
        return json.load(handle)


def write_json(path: Path, value: dict[str, Any]) -> bool:
    text = json.dumps(value, indent=2, sort_keys=True) + "\n"
    old = path.read_text(encoding="utf-8") if path.exists() else None
    if old == text:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return True


def write_text(path: Path, text: str) -> bool:
    old = path.read_text(encoding="utf-8") if path.exists() else None
    if old == text:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return True


def parse_recorder_config(config_path: Path) -> dict[str, Any]:
    config = {
        "purge_keep_days": None,
        "exclude": {
            "domains": [],
            "entity_globs": [],
            "entities": [],
        },
    }
    if not config_path.exists():
        return config

    lines = config_path.read_text(encoding="utf-8").splitlines()
    start = next((i for i, line in enumerate(lines) if line.strip() == "recorder:" and not line.startswith(" ")), None)
    if start is None:
        return config

    block: list[str] = []
    for line in lines[start + 1 :]:
        if line and not line.startswith(" ") and not line.startswith("#"):
            break
        block.append(line.rstrip())

    current_list: str | None = None
    in_exclude = False
    for raw in block:
        stripped = raw.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped.startswith("purge_keep_days:"):
            value = stripped.split(":", 1)[1].strip()
            try:
                config["purge_keep_days"] = int(value)
            except ValueError:
                config["purge_keep_days"] = value
            continue
        if stripped == "exclude:":
            in_exclude = True
            current_list = None
            continue
        if in_exclude and stripped.endswith(":"):
            key = stripped[:-1]
            current_list = key if key in config["exclude"] else None
            continue
        if in_exclude and current_list and stripped.startswith("- "):
            config["exclude"][current_list].append(stripped[2:].strip())
    return config


def load_device_entities(path: Path) -> dict[str, dict[str, Any]]:
    if not path.exists():
        return {}
    data = read_json(path)
    return {
        entity.get("entity_id"): entity
        for entity in data.get("entities", [])
        if entity.get("entity_id")
    }


def load_live_entities(path: Path | None) -> dict[str, dict[str, Any]]:
    if not path or not path.exists():
        return {}
    data = read_json(path)
    if isinstance(data.get("states"), list):
        return {item["entity_id"]: item for item in data["states"] if item.get("entity_id")}
    if isinstance(data.get("topAttr"), list):
        return {item["entity_id"]: item for item in data["topAttr"] if item.get("entity_id")}
    return {}


def matches_exclude(entity_id: str, config: dict[str, Any]) -> tuple[bool, str]:
    domain = entity_id.split(".", 1)[0]
    exclude = config.get("exclude", {})
    if domain in set(exclude.get("domains", [])):
        return True, f"domain:{domain}"
    if entity_id in set(exclude.get("entities", [])):
        return True, f"entity:{entity_id}"
    for pattern in exclude.get("entity_globs", []):
        if fnmatch.fnmatch(entity_id, pattern):
            return True, f"glob:{pattern}"
    return False, ""


def classify(entity: dict[str, Any]) -> dict[str, str]:
    entity_id = entity.get("entity_id", "")
    domain = entity.get("domain") or entity_id.split(".", 1)[0]
    platform = entity.get("platform", "")
    entity_category = entity.get("entity_category", "")
    role = entity.get("role", "")
    text = " ".join(
        str(entity.get(key, ""))
        for key in ["entity_id", "friendly_name", "name", "device_class", "unit", "area", "platform"]
    )

    if SUMMARY_RE.search(text):
        return {
            "category": "derived_summary_or_dashboard_state",
            "stateful_need": "low",
            "recommendation": "review_current_only",
            "reason": "Derived summary/status data is usually regenerated or shown as current state.",
        }
    if SIGNAL_RE.search(text):
        return {
            "category": "signal_quality_diagnostic",
            "stateful_need": "low",
            "recommendation": "review_current_only",
            "reason": "Signal quality is useful live, but long raw history rarely drives home behavior.",
        }
    if platform in LOW_VALUE_PLATFORMS and INFRA_RE.search(text):
        return {
            "category": "infrastructure_health_diagnostic",
            "stateful_need": "low",
            "recommendation": "review_current_only",
            "reason": "Infrastructure health telemetry is noisy and usually only needs current status or short diagnostics.",
        }
    if role == "telemetry" and platform in {"command_line", "template"} and domain == "sensor":
        return {
            "category": "derived_summary_or_dashboard_state",
            "stateful_need": "low",
            "recommendation": "review_current_only",
            "reason": "Template/command-line dashboard sensors should prove they need long raw Recorder history.",
        }
    if domain in CONTROL_CONFIG_DOMAINS:
        return {
            "category": "integration_config_or_update_state",
            "stateful_need": "low",
            "recommendation": "review_current_only",
            "reason": "Config/update controls rarely need 30-day Recorder history.",
        }
    if domain == "switch" and (entity_category == "config" or platform in LOW_VALUE_PLATFORMS or CONFIG_RE.search(text)):
        return {
            "category": "integration_config_or_update_state",
            "stateful_need": "low",
            "recommendation": "review_current_only",
            "reason": "Integration config switches usually need current state, not long history.",
        }
    if domain in LOW_VALUE_DOMAINS:
        return {
            "category": "camera_or_event_state",
            "stateful_need": "low",
            "recommendation": "review_short_or_current_only",
            "reason": "Camera/event entity state is often high churn; keep only if specific automations need history.",
        }
    if domain in REVIEW_DOMAINS:
        return {
            "category": "operational_state_history",
            "stateful_need": "medium",
            "recommendation": "review_selectively",
            "reason": "Useful for diagnostics, but not every automation/script/device tracker needs long raw state history.",
        }
    if EVENT_HISTORY_RE.search(text):
        return {
            "category": "event_or_safety_history",
            "stateful_need": "high",
            "recommendation": "keep",
            "reason": "Motion, presence, doors, valves, safety, and security history can support alerts and incident review.",
        }
    if role == "telemetry" and ENVIRONMENT_RE.search(text):
        return {
            "category": "physical_timeseries",
            "stateful_need": "high",
            "recommendation": "keep_or_shorten_by_dashboard_need",
            "reason": "Physical telemetry often powers charts, alerts, and trend comparisons.",
        }
    if platform in LOW_VALUE_PLATFORMS:
        return {
            "category": "infrastructure_or_camera_misc",
            "stateful_need": "medium",
            "recommendation": "review_selectively",
            "reason": "Infrastructure/camera entities should prove they need long history.",
        }
    return {
        "category": "uncategorized",
        "stateful_need": "unknown",
        "recommendation": "review",
        "reason": "No specific Recorder policy has been assigned yet.",
    }


def sqlite_table_columns(conn: sqlite3.Connection, table: str) -> set[str]:
    return {row[1] for row in conn.execute(f"PRAGMA table_info({table})")}


def sqlite_tables(conn: sqlite3.Connection) -> set[str]:
    return {row[0] for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}


def load_db_stats(db_path: Path | None) -> tuple[dict[str, dict[str, Any]], dict[str, Any]]:
    if not db_path:
        return {}, {"available": False}
    if not db_path.exists():
        return {}, {"available": False, "error": f"DB path not found: {db_path}"}

    conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    try:
        tables = sqlite_tables(conn)
        if "states" not in tables:
            return {}, {"available": False, "error": "states table not found"}
        state_cols = sqlite_table_columns(conn, "states")
        ts_col = next(
            (column for column in ["last_updated_ts", "last_reported_ts", "last_changed_ts"] if column in state_cols),
            None,
        )
        if "states_meta" in tables and "metadata_id" in state_cols:
            entity_expr = "sm.entity_id"
            join = "JOIN states_meta sm ON sm.metadata_id = s.metadata_id"
        elif "entity_id" in state_cols:
            entity_expr = "s.entity_id"
            join = ""
        else:
            return {}, {"available": False, "error": "entity id column not found"}

        attrs_join = ""
        attr_expr = "0"
        distinct_attr_expr = "0"
        if "state_attributes" in tables and "attributes_id" in state_cols:
            attrs_join = "LEFT JOIN state_attributes sa ON sa.attributes_id = s.attributes_id"
            attr_expr = "SUM(CASE WHEN sa.shared_attrs IS NULL THEN 0 ELSE LENGTH(sa.shared_attrs) END)"
            distinct_attr_expr = "COUNT(DISTINCT s.attributes_id)"

        if ts_col:
            min_expr = f"MIN(s.{ts_col})"
            max_expr = f"MAX(s.{ts_col})"
        else:
            min_expr = "NULL"
            max_expr = "NULL"

        query = f"""
            SELECT
              {entity_expr} AS entity_id,
              COUNT(*) AS rows,
              {min_expr} AS first_ts,
              {max_expr} AS last_ts,
              {distinct_attr_expr} AS distinct_attribute_ids,
              {attr_expr} AS repeated_attribute_bytes
            FROM states s
            {join}
            {attrs_join}
            WHERE {entity_expr} IS NOT NULL
            GROUP BY {entity_expr}
        """
        stats: dict[str, dict[str, Any]] = {}
        total_rows = 0
        for row in conn.execute(query):
            first_ts = row["first_ts"]
            last_ts = row["last_ts"]
            rows = int(row["rows"] or 0)
            span_days = None
            rows_per_day = None
            if first_ts is not None and last_ts is not None and last_ts > first_ts:
                span_days = (float(last_ts) - float(first_ts)) / 86400
                rows_per_day = rows / span_days if span_days > 0 else None
            total_rows += rows
            stats[row["entity_id"]] = {
                "rows": rows,
                "first_ts": first_ts,
                "last_ts": last_ts,
                "span_days": round(span_days, 2) if span_days is not None else None,
                "rows_per_day": round(rows_per_day, 1) if rows_per_day is not None else None,
                "distinct_attribute_ids": int(row["distinct_attribute_ids"] or 0),
                "repeated_attribute_bytes": int(row["repeated_attribute_bytes"] or 0),
            }
        return stats, {
            "available": True,
            "path_name": db_path.name,
            "entity_count": len(stats),
            "state_rows": total_rows,
        }
    finally:
        conn.close()


def load_db_stats_json(stats_path: Path | None) -> tuple[dict[str, dict[str, Any]], dict[str, Any]]:
    if not stats_path:
        return {}, {"available": False}
    if not stats_path.exists():
        return {}, {"available": False, "error": f"DB stats path not found: {stats_path}"}

    data = read_json(stats_path)
    stats = data.get("entity_stats") or data.get("stats") or {}
    summary = data.get("database") or data.get("summary") or {}
    if not isinstance(stats, dict):
        return {}, {"available": False, "error": f"DB stats payload has no entity stats: {stats_path}"}
    if not isinstance(summary, dict):
        summary = {}

    summary = {
        "available": True,
        "path_name": summary.get("path_name") or stats_path.name,
        "entity_count": summary.get("entity_count") or len(stats),
        **summary,
        "stats_source": stats_path.name,
    }
    return stats, summary


def build_inventory(
    device_entities: dict[str, dict[str, Any]],
    live_entities: dict[str, dict[str, Any]],
    recorder_config: dict[str, Any],
    db_stats: dict[str, dict[str, Any]],
    db_summary: dict[str, Any],
) -> dict[str, Any]:
    entity_ids = sorted(set(device_entities) | set(live_entities) | set(db_stats))
    rows: list[dict[str, Any]] = []
    for entity_id in entity_ids:
        device = device_entities.get(entity_id, {})
        live = live_entities.get(entity_id, {})
        entity = {
            "entity_id": entity_id,
            "domain": device.get("domain") or live.get("domain") or entity_id.split(".", 1)[0],
            "platform": device.get("platform", ""),
            "area": device.get("area", ""),
            "role": device.get("role", ""),
            "entity_category": device.get("entity_category", ""),
            "availability": device.get("availability", ""),
            "friendly_name": live.get("friendly_name") or device.get("friendly_name") or device.get("name") or "",
            "device_class": live.get("device_class") or device.get("device_class", ""),
            "unit": live.get("unit") or device.get("unit", ""),
            "disabled_by": device.get("disabled_by", ""),
            "hidden_by": device.get("hidden_by", ""),
        }
        excluded, exclude_match = matches_exclude(entity_id, recorder_config)
        disabled = bool(entity.get("disabled_by"))
        classification = classify(entity)
        status = "excluded_by_config" if excluded else "disabled_in_registry" if disabled else "recorded_candidate"
        live_age = live.get("age_seconds")
        if live_age is None and live.get("last_reported"):
            try:
                reported = dt.datetime.fromisoformat(str(live["last_reported"]).replace("Z", "+00:00"))
                live_age = int((dt.datetime.now(dt.UTC) - reported).total_seconds())
            except ValueError:
                live_age = None
        row = {
            **entity,
            "recorder_status": status,
            "exclude_match": exclude_match,
            "retention_days": recorder_config.get("purge_keep_days"),
            **classification,
            "live_attr_bytes": live.get("attr_bytes"),
            "live_last_reported": live.get("last_reported"),
            "live_age_seconds": live_age,
            "db": db_stats.get(entity_id),
        }
        rows.append(row)

    summary = {
        "entity_count": len(rows),
        "recorded_candidate_count": sum(1 for row in rows if row["recorder_status"] == "recorded_candidate"),
        "excluded_by_config_count": sum(1 for row in rows if row["recorder_status"] == "excluded_by_config"),
        "disabled_count": sum(1 for row in rows if row["recorder_status"] == "disabled_in_registry"),
        "retention_days": recorder_config.get("purge_keep_days"),
        "stateful_need_counts": dict(Counter(row["stateful_need"] for row in rows if row["recorder_status"] == "recorded_candidate")),
        "recommendation_counts": dict(Counter(row["recommendation"] for row in rows if row["recorder_status"] == "recorded_candidate")),
        "category_counts": dict(Counter(row["category"] for row in rows if row["recorder_status"] == "recorded_candidate")),
        "db": db_summary,
    }
    return {
        "schema_version": SCHEMA_VERSION,
        "generated_at": utc_now(),
        "sources": {
            "device_inventory": "docs/device-inventory.json" if device_entities else None,
            "live_state": bool(live_entities),
            "database": db_summary,
        },
        "recorder_config": recorder_config,
        "summary": summary,
        "domains": summarize_group(rows, "domain"),
        "integrations": summarize_group(rows, "platform"),
        "categories": summarize_group(rows, "category"),
        "entities": rows,
    }


def summarize_group(rows: list[dict[str, Any]], key: str) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[row.get(key) or "unknown"].append(row)
    result = []
    for name, items in grouped.items():
        candidates = [row for row in items if row["recorder_status"] == "recorded_candidate"]
        db_rows = sum((row.get("db") or {}).get("rows", 0) for row in items)
        result.append({
            key: name,
            "entities": len(items),
            "recorded_candidates": len(candidates),
            "low_stateful_need": sum(1 for row in candidates if row["stateful_need"] == "low"),
            "medium_stateful_need": sum(1 for row in candidates if row["stateful_need"] == "medium"),
            "high_stateful_need": sum(1 for row in candidates if row["stateful_need"] == "high"),
            "unknown_stateful_need": sum(1 for row in candidates if row["stateful_need"] == "unknown"),
            "db_rows": db_rows or None,
            "live_attr_bytes": sum(row.get("live_attr_bytes") or 0 for row in items) or None,
        })
    return sorted(result, key=lambda item: (item["db_rows"] or 0, item["recorded_candidates"]), reverse=True)


def table(headers: list[str], rows: list[list[Any]]) -> str:
    out = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in rows:
        out.append("| " + " | ".join(str(value) for value in row) + " |")
    return "\n".join(out)


def entity_link(entity_id: str) -> str:
    return f"`{entity_id}`"


def render_markdown(inventory: dict[str, Any]) -> str:
    summary = inventory["summary"]
    entities = inventory["entities"]
    candidates = [row for row in entities if row["recorder_status"] == "recorded_candidate"]
    low = [row for row in candidates if row["stateful_need"] == "low"]
    db_available = inventory["sources"]["database"].get("available")

    largest_low = sorted(
        low,
        key=lambda row: (
            (row.get("db") or {}).get("rows", 0),
            row.get("live_attr_bytes") or 0,
        ),
        reverse=True,
    )[:30]
    live_attr = sorted(candidates, key=lambda row: row.get("live_attr_bytes") or 0, reverse=True)[:25]

    lines = [
        "# Recorder Inventory",
        "",
        "A recording-focused inventory for Home Assistant Recorder. This sits next to the device inventory, but answers a different question: what state history Home Assistant is saving, how long it is retained, and which classes of entities should prove they need long-term stateful history.",
        "",
        "## At A Glance",
        "",
        table(
            ["Thing", "Count"],
            [
                ["Configured retention", f"{summary.get('retention_days')} days"],
                ["Entities reviewed", summary["entity_count"]],
                ["Recorder candidates", summary["recorded_candidate_count"]],
                ["Excluded by Recorder config", summary["excluded_by_config_count"]],
                ["Disabled in registry", summary["disabled_count"]],
                ["Low stateful-need candidates", summary["stateful_need_counts"].get("low", 0)],
                ["Medium stateful-need candidates", summary["stateful_need_counts"].get("medium", 0)],
                ["High stateful-need candidates", summary["stateful_need_counts"].get("high", 0)],
            ],
        ),
        "",
        "## Data Quality",
        "",
    ]
    if db_available:
        db = inventory["sources"]["database"]
        lines.extend([
            f"- Exact DB row counts are included from `{db.get('path_name')}`.",
            f"- State rows counted: {db.get('state_rows')}.",
        ])
    else:
        lines.extend([
            "- Exact per-entity row counts are not included in this run.",
            "- Frequency should be treated as pending until the tool is run against a `home-assistant_v2.db` copy.",
            "- Live attr sizes and live recency are useful triage signals, not a substitute for SQLite row counts.",
        ])

    low_categories = sorted(
        inventory["categories"],
        key=lambda row: (row["low_stateful_need"], row.get("live_attr_bytes") or 0, row["recorded_candidates"]),
        reverse=True,
    )

    lines.extend([
        "",
        "## Current Recorder Config",
        "",
        table(
            ["Setting", "Value"],
            [
                ["purge_keep_days", summary.get("retention_days")],
                ["excluded domains", ", ".join(inventory["recorder_config"]["exclude"].get("domains", [])) or "(none)"],
                ["excluded entity globs", ", ".join(inventory["recorder_config"]["exclude"].get("entity_globs", [])) or "(none)"],
                ["excluded entities", ", ".join(inventory["recorder_config"]["exclude"].get("entities", [])) or "(none)"],
            ],
        ),
        "",
        "## Largest Low-Stateful-Need Review Sets",
        "",
        table(
            ["Category", "Entities", "Low", "Medium", "High", "DB rows", "Live attr bytes"],
            [
                [
                    row["category"],
                    row["recorded_candidates"],
                    row["low_stateful_need"],
                    row["medium_stateful_need"],
                    row["high_stateful_need"],
                    row.get("db_rows") or "",
                    row.get("live_attr_bytes") or "",
                ]
                for row in low_categories[:12]
            ],
        ),
        "",
        "## Domain Review",
        "",
        table(
            ["Domain", "Recorder candidates", "Low", "Medium", "High", "Unknown", "DB rows"],
            [
                [
                    row["domain"],
                    row["recorded_candidates"],
                    row["low_stateful_need"],
                    row["medium_stateful_need"],
                    row["high_stateful_need"],
                    row["unknown_stateful_need"],
                    row.get("db_rows") or "",
                ]
                for row in inventory["domains"][:24]
            ],
        ),
        "",
        "## High-Impact Entities To Review First",
        "",
        table(
            ["Entity", "Category", "Integration", "Reason", "DB rows", "Rows/day", "Live attr bytes"],
            [
                [
                    entity_link(row["entity_id"]),
                    row["category"],
                    row.get("platform") or "",
                    row["reason"],
                    (row.get("db") or {}).get("rows", ""),
                    (row.get("db") or {}).get("rows_per_day", ""),
                    row.get("live_attr_bytes") or "",
                ]
                for row in largest_low
            ],
        ),
        "",
        "## Largest Live Attribute Payloads",
        "",
        table(
            ["Entity", "Recommendation", "Integration", "Live attr bytes", "Reason"],
            [
                [
                    entity_link(row["entity_id"]),
                    row["recommendation"],
                    row.get("platform") or "",
                    row.get("live_attr_bytes") or "",
                    row["reason"],
                ]
                for row in live_attr
                if row.get("live_attr_bytes")
            ],
        ),
        "",
        "## Use",
        "",
        "Regenerate after Recorder config changes, major integration additions, or storage incidents:",
        "",
        "```bash",
        "python3 tools/generate_recorder_inventory.py",
        "```",
        "",
        "For exact frequency and largest historical writers, run against a copied Recorder DB:",
        "",
        "```bash",
        "python3 tools/generate_recorder_inventory.py --db /path/to/home-assistant_v2.db",
        "```",
        "",
        "For remote systems where copying the full DB is impractical, first collect a small DB stats JSON on the HA host, then run:",
        "",
        "```bash",
        "python3 tools/generate_recorder_inventory.py --db-stats-json .tmp/recorder-db-row-stats.json",
        "```",
        "",
        "Do not use this inventory as an automatic exclusion list. Treat it as the audit map for deciding what should be kept, shortened, or made current-only.",
        "",
    ])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=Path("configuration.yaml"))
    parser.add_argument("--device-inventory", type=Path, default=Path("docs/device-inventory.json"))
    parser.add_argument("--live-states", type=Path, default=None)
    parser.add_argument("--db", type=Path, default=None)
    parser.add_argument("--db-stats-json", type=Path, default=None)
    parser.add_argument("--output-json", type=Path, default=Path("docs/recorder-inventory.json"))
    parser.add_argument("--output-md", type=Path, default=Path("docs/recorder-inventory.md"))
    args = parser.parse_args()

    recorder_config = parse_recorder_config(args.config)
    device_entities = load_device_entities(args.device_inventory)
    live_entities = load_live_entities(args.live_states)
    if args.db_stats_json:
        db_stats, db_summary = load_db_stats_json(args.db_stats_json)
    else:
        db_stats, db_summary = load_db_stats(args.db)
    inventory = build_inventory(device_entities, live_entities, recorder_config, db_stats, db_summary)
    json_changed = write_json(args.output_json, inventory)
    markdown_changed = write_text(args.output_md, render_markdown(inventory))
    print(json.dumps({
        "ok": True,
        "json_changed": json_changed,
        "markdown_changed": markdown_changed,
        "recorded_candidates": inventory["summary"]["recorded_candidate_count"],
        "low_stateful_need": inventory["summary"]["stateful_need_counts"].get("low", 0),
        "db_available": db_summary.get("available", False),
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
