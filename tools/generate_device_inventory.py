#!/usr/bin/env python3
"""Generate a redacted Home Assistant device and capability inventory."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import io
import json
import os
import re
import secrets
import sys
import tarfile
import tempfile
import urllib.error
import urllib.request
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


SCHEMA_VERSION = 2
CHANGE_REPORT_VERSION = 1
DIGEST_VERSION = 1

REGISTRY_MEMBERS = {
    "areas": "core.area_registry",
    "config_entries": "core.config_entries",
    "devices": "core.device_registry",
    "entities": "core.entity_registry",
}

TELEMETRY_DOMAINS = {
    "binary_sensor",
    "camera",
    "device_tracker",
    "event",
    "image",
    "sensor",
    "update",
    "weather",
}

CONTROL_DOMAINS = {
    "alarm_control_panel",
    "button",
    "climate",
    "cover",
    "fan",
    "light",
    "lock",
    "media_player",
    "number",
    "remote",
    "select",
    "siren",
    "switch",
    "text",
    "vacuum",
    "valve",
}

SENSITIVE_DOMAINS = {
    "alarm_control_panel",
    "camera",
    "cover",
    "lock",
    "siren",
    "valve",
}
SENSITIVE_NAME_RE = re.compile(r"(?i)\b(garage|door|gate|security|alarm|lock|shutoff|shut[- ]?off|valve)\b")
WIRED_RE = re.compile(r"(?i)\b(wired|ethernet|lan)\b")
WIRELESS_RE = re.compile(r"(?i)\b(wireless|wi-?fi|wlan|2\.4|5\s*ghz|6\s*ghz)\b")
GUEST_NETWORK_RE = re.compile(r"(?i)\b(guest|visitor)\b")
IOT_NETWORK_RE = re.compile(r"(?i)\b(iot|device|things)\b")
TRUSTED_NETWORK_RE = re.compile(r"(?i)\b(main|trusted|default|private|secure|home|lan)\b")

MAC_COLON_RE = re.compile(r"(?i)(?:[0-9a-f]{2}:){5}[0-9a-f]{2}")
MAC_DASH_RE = re.compile(r"(?i)(?:[0-9a-f]{2}-){5}[0-9a-f]{2}")
MAC_UNDERSCORE_RE = re.compile(r"(?i)(?:[0-9a-f]{2}_){5}[0-9a-f]{2}")
IPV4_RE = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")


def default_config_dir() -> Path:
    env_dir = os.environ.get("HA_CONFIG_DIR")
    if env_dir:
        return Path(env_dir)
    return Path("/config") if Path("/config").exists() else Path(".")


def read_json_file(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def find_tar_member(archive: tarfile.TarFile, candidates: list[str]) -> tarfile.TarInfo | None:
    normalized = {candidate.strip("./") for candidate in candidates}
    for member in archive.getmembers():
        if member.name.strip("./") in normalized:
            return member
    return None


def read_backup_json(backup_path: Path, inner_name: str) -> dict[str, Any] | None:
    candidates = [
        f"data/.storage/{inner_name}",
        f".storage/{inner_name}",
    ]
    with tarfile.open(backup_path, "r:*") as outer:
        nested_member = find_tar_member(outer, ["homeassistant.tar.gz", "homeassistant.tar"])
        if nested_member is None:
            return None
        nested_file = outer.extractfile(nested_member)
        if nested_file is None:
            return None
        nested_bytes = nested_file.read()

    with tarfile.open(fileobj=io.BytesIO(nested_bytes), mode="r:*") as inner:
        member = find_tar_member(inner, candidates)
        if member is None:
            return None
        extracted = inner.extractfile(member)
        if extracted is None:
            return None
        return json.load(io.TextIOWrapper(extracted, encoding="utf-8"))


def load_registries(config_dir: Path, backup_path: Path | None = None) -> dict[str, dict[str, Any]]:
    registries: dict[str, dict[str, Any]] = {}
    for key, filename in REGISTRY_MEMBERS.items():
        if backup_path:
            payload = read_backup_json(backup_path, filename)
        else:
            payload = read_json_file(config_dir / ".storage" / filename)
        registries[key] = payload or {"data": {}}

    if backup_path:
        registries["unifi_data"] = read_backup_json(backup_path, "unifi_data") or {"data": {}}
    else:
        unifi_path = config_dir / ".storage" / "unifi_data"
        registries["unifi_data"] = read_json_file(unifi_path) if unifi_path.exists() else {"data": {}}

    return registries


def ensure_salt(path: Path) -> str:
    if path.exists():
        return path.read_text(encoding="utf-8").strip()
    path.parent.mkdir(parents=True, exist_ok=True)
    salt = secrets.token_hex(16)
    path.write_text(f"{salt}\n", encoding="utf-8")
    try:
        path.chmod(0o600)
    except OSError:
        pass
    return salt


def stable_hash(value: Any, salt: str, prefix: str = "") -> str:
    text = "" if value is None else str(value)
    digest = hashlib.blake2s(
        text.encode("utf-8"),
        key=salt.encode("utf-8")[:32],
        digest_size=6,
    ).hexdigest()
    return f"{prefix}{digest}" if prefix else digest


def normalize_mac(value: str) -> str:
    return re.sub(r"[^0-9a-f]", "", value.lower())


def extract_mac(value: Any) -> str | None:
    text = "" if value is None else str(value)
    for regex in (MAC_COLON_RE, MAC_DASH_RE, MAC_UNDERSCORE_RE):
        match = regex.search(text)
        if match:
            return normalize_mac(match.group(0))
    return None


def sanitize_string(value: Any, salt: str) -> str:
    text = "" if value is None else str(value)

    def replace_mac(match: re.Match[str]) -> str:
        return stable_hash(normalize_mac(match.group(0)), salt, "mac_")

    def replace_ip(match: re.Match[str]) -> str:
        return stable_hash(match.group(0), salt, "ip_")

    text = MAC_COLON_RE.sub(replace_mac, text)
    text = MAC_DASH_RE.sub(replace_mac, text)
    text = MAC_UNDERSCORE_RE.sub(replace_mac, text)
    return IPV4_RE.sub(replace_ip, text)


def domain_from_entity_id(entity_id: str) -> str:
    return entity_id.split(".", 1)[0] if "." in entity_id else entity_id


def classify_role(entity: dict[str, Any]) -> str:
    entity_id = entity.get("entity_id") or ""
    domain = domain_from_entity_id(entity_id)
    platform = entity.get("platform") or ""
    if platform == "unifi" and domain == "device_tracker":
        return "network"
    if domain.startswith("input_") or domain in CONTROL_DOMAINS:
        return "control"
    if domain in TELEMETRY_DOMAINS:
        return "telemetry"
    return "other"


def registry_items(registry: dict[str, Any], key: str) -> list[dict[str, Any]]:
    data = registry.get("data") or {}
    value = data.get(key) or []
    return value if isinstance(value, list) else []


def entries_by_id(entries: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {entry.get("entry_id"): entry for entry in entries if entry.get("entry_id")}


def area_names(areas: list[dict[str, Any]], salt: str) -> dict[str, str]:
    return {
        (area.get("area_id") or area.get("id")): sanitize_string(
            area.get("name") or area.get("area_id") or area.get("id"),
            salt,
        )
        for area in areas
        if area.get("area_id") or area.get("id")
    }


def integration_domains_for_device(
    device: dict[str, Any],
    entities: list[dict[str, Any]],
    config_entries: dict[str, dict[str, Any]],
) -> list[str]:
    domains = {
        config_entries[entry_id].get("domain")
        for entry_id in device.get("config_entries") or []
        if entry_id in config_entries
    }
    domains.update(entity.get("platform") for entity in entities if entity.get("platform"))
    return sorted(domain for domain in domains if domain)


def entity_availability(entity: dict[str, Any], state: dict[str, Any] | None) -> str:
    if entity.get("disabled_by"):
        return "disabled"
    if entity.get("hidden_by"):
        return "hidden"
    if state is None:
        return "not_enriched"
    raw_state = state.get("state")
    if raw_state in {"unavailable", "unknown"}:
        return raw_state
    return "available"


def display_entity_name(entity: dict[str, Any], state: dict[str, Any] | None, salt: str) -> str:
    attributes = state.get("attributes") if state else {}
    friendly_name = attributes.get("friendly_name") if isinstance(attributes, dict) else None
    name = entity.get("name") or entity.get("original_name") or friendly_name or entity.get("entity_id")
    return sanitize_string(name, salt)


def public_entity(entity: dict[str, Any], state: dict[str, Any] | None, salt: str) -> dict[str, Any]:
    entity_id = entity.get("entity_id") or ""
    capabilities = entity.get("capabilities") or {}
    domain = domain_from_entity_id(entity_id)
    return {
        "entity_id": sanitize_string(entity_id, salt),
        "name": display_entity_name(entity, state, salt),
        "domain": domain,
        "role": classify_role(entity),
        "platform": entity.get("platform") or domain,
        "device_class": entity.get("device_class") or entity.get("original_device_class") or "",
        "unit": entity.get("unit_of_measurement") or "",
        "entity_category": entity.get("entity_category") or "",
        "disabled_by": entity.get("disabled_by") or "",
        "hidden_by": entity.get("hidden_by") or "",
        "availability": entity_availability(entity, state),
        "capability_keys": sorted(capabilities.keys()) if isinstance(capabilities, dict) else [],
    }


def state_map(states: list[dict[str, Any]] | None) -> dict[str, dict[str, Any]]:
    return {state["entity_id"]: state for state in states or [] if state.get("entity_id")}


def normalize_network_key(raw_value: Any) -> str:
    mac = extract_mac(raw_value)
    return f"mac:{mac}" if mac else str(raw_value)


def attribute_text(attributes: dict[str, Any], keys: tuple[str, ...]) -> str:
    values = []
    for key in keys:
        value = attributes.get(key)
        if value not in (None, ""):
            values.append(str(value))
    return " ".join(values)


def connection_type_from_state(state: dict[str, Any] | None) -> str:
    attributes = state.get("attributes") if state else {}
    if not isinstance(attributes, dict):
        return ""

    for key in ("is_wired", "wired", "wired_client"):
        if attributes.get(key) is True:
            return "wired"
        if attributes.get(key) is False:
            return "wireless"

    connection_text = attribute_text(
        attributes,
        (
            "connection_type",
            "connection",
            "type",
            "radio",
            "radio_name",
        ),
    )
    wireless_text = attribute_text(attributes, ("ssid", "essid", "wlan", "wlan_name", "radio", "radio_name"))
    if WIRED_RE.search(connection_text):
        return "wired"
    if WIRELESS_RE.search(wireless_text) or attributes.get("ap_mac") or attributes.get("ssid") or attributes.get("essid"):
        return "wireless"
    return ""


def network_scope_from_state(state: dict[str, Any] | None) -> str:
    attributes = state.get("attributes") if state else {}
    if not isinstance(attributes, dict):
        return ""
    network_text = attribute_text(
        attributes,
        (
            "network",
            "network_name",
            "ssid",
            "essid",
            "wlan",
            "wlan_name",
        ),
    )
    if GUEST_NETWORK_RE.search(network_text):
        return "guest"
    if IOT_NETWORK_RE.search(network_text):
        return "iot"
    if TRUSTED_NETWORK_RE.search(network_text):
        return "trusted"
    return ""


def build_network_clients(
    entities: list[dict[str, Any]],
    devices_by_raw_id: dict[str, str],
    unifi_data: dict[str, Any],
    salt: str,
    states_by_entity: dict[str, dict[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    clients: dict[str, dict[str, Any]] = {}
    states_by_entity = states_by_entity or {}

    def ensure_client(raw_key: Any) -> dict[str, Any]:
        normalized = normalize_network_key(raw_key)
        client_id = stable_hash(normalized, salt, "network_")
        clients.setdefault(
            client_id,
            {
                "client_id": client_id,
                "sources": set(),
                "tracked_entity_ids": set(),
                "device_ids": set(),
                "names": set(),
                "connection_types": set(),
                "network_scopes": set(),
            },
        )
        return clients[client_id]

    wireless_clients = (unifi_data.get("data") or {}).get("wireless_clients") or []
    if isinstance(wireless_clients, list):
        for raw_client in wireless_clients:
            client = ensure_client(raw_client)
            client["sources"].add("unifi_data.wireless_clients")

    for entity in entities:
        if entity.get("platform") != "unifi":
            continue
        if not (entity.get("entity_id") or "").startswith("device_tracker."):
            continue
        raw_key = entity.get("unique_id") or entity.get("entity_id")
        client = ensure_client(raw_key)
        client["sources"].add("entity_registry")
        client["tracked_entity_ids"].add(sanitize_string(entity.get("entity_id"), salt))
        if entity.get("device_id") in devices_by_raw_id:
            client["device_ids"].add(devices_by_raw_id[entity["device_id"]])
        name = entity.get("name") or entity.get("original_name")
        if name:
            client["names"].add(sanitize_string(name, salt))
        state = states_by_entity.get(entity.get("entity_id") or "")
        connection_type = connection_type_from_state(state)
        network_scope = network_scope_from_state(state)
        if connection_type:
            client["connection_types"].add(connection_type)
        if network_scope:
            client["network_scopes"].add(network_scope)

    public_clients: list[dict[str, Any]] = []
    for client in clients.values():
        public_clients.append(
            {
                "client_id": client["client_id"],
                "sources": sorted(client["sources"]),
                "tracked_entity_ids": sorted(client["tracked_entity_ids"]),
                "device_ids": sorted(client["device_ids"]),
                "names": sorted(client["names"]),
                "connection_types": sorted(client["connection_types"]),
                "network_scopes": sorted(client["network_scopes"]),
            }
        )
    return sorted(public_clients, key=lambda item: item["client_id"])


def build_inventory(
    registries: dict[str, dict[str, Any]],
    states: list[dict[str, Any]] | None,
    services: dict[str, Any] | list[Any] | None,
    salt: str,
) -> dict[str, Any]:
    areas = registry_items(registries["areas"], "areas")
    config_entries = entries_by_id(registry_items(registries["config_entries"], "entries"))
    raw_devices = registry_items(registries["devices"], "devices")
    raw_entities = registry_items(registries["entities"], "entities")
    states_by_entity = state_map(states)
    areas_by_id = area_names(areas, salt)

    device_public_ids = {
        device.get("id"): stable_hash(device.get("id"), salt, "device_")
        for device in raw_devices
        if device.get("id")
    }
    raw_entities_by_device: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for entity in raw_entities:
        if entity.get("device_id"):
            raw_entities_by_device[entity["device_id"]].append(entity)

    public_entities: list[dict[str, Any]] = []
    for entity in sorted(raw_entities, key=lambda item: item.get("entity_id") or ""):
        state = states_by_entity.get(entity.get("entity_id") or "")
        public = public_entity(entity, state, salt)
        device_id = entity.get("device_id")
        public["device_id"] = device_public_ids.get(device_id, "")
        device_area = ""
        if device_id:
            device_area = next((device.get("area_id") or "" for device in raw_devices if device.get("id") == device_id), "")
        area_id = entity.get("area_id") or device_area
        public["area"] = areas_by_id.get(area_id, sanitize_string(area_id, salt) if area_id else "")
        public_entities.append(public)

    entity_lookup = {entity["entity_id"]: entity for entity in public_entities}
    public_devices: list[dict[str, Any]] = []
    for device in sorted(raw_devices, key=lambda item: (item.get("name_by_user") or item.get("name") or item.get("id") or "")):
        raw_id = device.get("id")
        public_id = device_public_ids.get(raw_id)
        if not public_id:
            continue
        device_entities_raw = sorted(raw_entities_by_device.get(raw_id, []), key=lambda item: item.get("entity_id") or "")
        entity_ids = [sanitize_string(entity.get("entity_id"), salt) for entity in device_entities_raw]
        role_counts = Counter(entity_lookup[entity_id]["role"] for entity_id in entity_ids if entity_id in entity_lookup)
        domains = integration_domains_for_device(device, device_entities_raw, config_entries)
        area_id = device.get("area_id") or ""
        public_devices.append(
            {
                "device_id": public_id,
                "name": sanitize_string(device.get("name_by_user") or device.get("name") or public_id, salt),
                "area": areas_by_id.get(area_id, sanitize_string(area_id, salt) if area_id else ""),
                "manufacturer": sanitize_string(device.get("manufacturer") or "", salt),
                "model": sanitize_string(device.get("model") or device.get("model_id") or "", salt),
                "integrations": domains,
                "disabled_by": device.get("disabled_by") or "",
                "entry_type": device.get("entry_type") or "",
                "entity_count": len(entity_ids),
                "telemetry_count": role_counts.get("telemetry", 0),
                "control_count": role_counts.get("control", 0),
                "network_count": role_counts.get("network", 0),
                "other_count": role_counts.get("other", 0),
                "entities": entity_ids,
            }
        )

    known_public_device_ids = {device["device_id"] for device in public_devices}
    orphan_entities = [
        entity
        for entity in public_entities
        if not entity.get("device_id") or entity.get("device_id") not in known_public_device_ids
    ]
    network_clients = build_network_clients(
        raw_entities,
        device_public_ids,
        registries.get("unifi_data") or {},
        salt,
        states_by_entity,
    )

    domain_counts = Counter(entity["domain"] for entity in public_entities)
    role_counts = Counter(entity["role"] for entity in public_entities)
    integration_counts = Counter(entity["platform"] for entity in public_entities)
    service_domains: list[str] = []
    if isinstance(services, dict):
        service_domains = sorted(services.keys())
    elif isinstance(services, list):
        service_domains = sorted(item.get("domain") for item in services if isinstance(item, dict) and item.get("domain"))

    return {
        "schema_version": SCHEMA_VERSION,
        "summary": {
            "device_count": len(public_devices),
            "entity_count": len(public_entities),
            "orphan_entity_count": len(orphan_entities),
            "network_client_count": len(network_clients),
            "area_count": len(areas_by_id),
            "integration_count": len(integration_counts),
            "domain_counts": dict(sorted(domain_counts.items())),
            "role_counts": dict(sorted(role_counts.items())),
            "integration_counts": dict(sorted(integration_counts.items())),
            "service_domain_count": len(service_domains),
        },
        "devices": sorted(public_devices, key=lambda item: (item["area"], item["name"], item["device_id"])),
        "entities": sorted(public_entities, key=lambda item: item["entity_id"]),
        "orphan_entities": sorted(orphan_entities, key=lambda item: item["entity_id"]),
        "network_clients": network_clients,
    }


def markdown_table(headers: list[str], rows: list[list[Any]]) -> str:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(value).replace("\n", " ") for value in row) + " |")
    return "\n".join(lines)


def render_markdown(inventory: dict[str, Any]) -> str:
    summary = inventory["summary"]
    lines = [
        "# Device Inventory",
        "",
        "Generated from Home Assistant registries and UniFi-tracked network clients. Sensitive network identifiers are redacted.",
        "",
        "## Summary",
        "",
        markdown_table(
            ["Metric", "Count"],
            [
                ["Devices", summary["device_count"]],
                ["Entities", summary["entity_count"]],
                ["Orphan entities", summary["orphan_entity_count"]],
                ["Network clients", summary["network_client_count"]],
                ["Areas", summary["area_count"]],
                ["Integrations", summary["integration_count"]],
            ],
        ),
        "",
        "### Roles",
        "",
        markdown_table(["Role", "Entities"], sorted(summary["role_counts"].items())),
        "",
        "### Top Integrations",
        "",
        markdown_table(
            ["Integration", "Entities"],
            sorted(summary["integration_counts"].items(), key=lambda item: (-item[1], item[0]))[:20],
        ),
        "",
        "## Devices By Area",
        "",
    ]

    entities_by_id = {entity["entity_id"]: entity for entity in inventory["entities"]}
    devices_by_area: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for device in inventory["devices"]:
        devices_by_area[device.get("area") or "Unassigned"].append(device)

    for area in sorted(devices_by_area):
        lines.extend([f"### {area}", ""])
        for device in sorted(devices_by_area[area], key=lambda item: item["name"]):
            integrations = ", ".join(device["integrations"]) or "unknown"
            model = " ".join(part for part in [device["manufacturer"], device["model"]] if part) or "unknown model"
            lines.extend(
                [
                    f"#### {device['name']}",
                    "",
                    f"- Device ID: `{device['device_id']}`",
                    f"- Integration: {integrations}",
                    f"- Model: {model}",
                    f"- Capability mix: {device['telemetry_count']} telemetry, {device['control_count']} control, {device['network_count']} network, {device['other_count']} other",
                    "",
                ]
            )
            rows = []
            for entity_id in device["entities"]:
                entity = entities_by_id.get(entity_id)
                if not entity:
                    continue
                detail = entity["device_class"] or entity["entity_category"] or ""
                if entity["unit"]:
                    detail = f"{detail} ({entity['unit']})" if detail else entity["unit"]
                rows.append([f"`{entity_id}`", entity["role"], entity["platform"], detail, entity["availability"]])
            if rows:
                lines.extend([markdown_table(["Entity", "Role", "Integration", "Detail", "Availability"], rows), ""])
            else:
                lines.append("_No registered entities._")
                lines.append("")

    if inventory["orphan_entities"]:
        lines.extend(["## Orphan Entities", ""])
        lines.extend(
            [
                markdown_table(
                    ["Entity", "Name", "Role", "Integration", "Availability"],
                    [
                        [
                            f"`{entity['entity_id']}`",
                            entity["name"],
                            entity["role"],
                            entity["platform"],
                            entity["availability"],
                        ]
                        for entity in inventory["orphan_entities"]
                    ],
                ),
                "",
            ]
        )

    lines.extend(["## UniFi Network Clients", ""])
    if inventory["network_clients"]:
        lines.append(
            markdown_table(
                ["Client ID", "Sources", "Connection", "Scope", "Tracked Entities", "Names"],
                [
                    [
                        f"`{client['client_id']}`",
                        ", ".join(client["sources"]),
                        ", ".join(client.get("connection_types") or []) or "",
                        ", ".join(client.get("network_scopes") or []) or "",
                        ", ".join(f"`{entity_id}`" for entity_id in client["tracked_entity_ids"]) or "",
                        ", ".join(client["names"]) or "",
                    ]
                    for client in inventory["network_clients"]
                ],
            )
        )
    else:
        lines.append("_No UniFi network clients found._")
    lines.append("")
    return "\n".join(lines)


def write_if_changed(path: Path, content: str) -> bool:
    path.parent.mkdir(parents=True, exist_ok=True)
    existing = path.read_text(encoding="utf-8") if path.exists() else None
    if existing == content:
        return False
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False) as handle:
        handle.write(content)
        temp_name = handle.name
    os.replace(temp_name, path)
    return True


def write_json_if_changed(path: Path, payload: dict[str, Any]) -> bool:
    return write_if_changed(path, json.dumps(payload, indent=2, sort_keys=True) + "\n")


def read_json_or_none(path: Path) -> dict[str, Any] | None:
    try:
        payload = read_json_file(path)
    except (FileNotFoundError, OSError, json.JSONDecodeError):
        return None
    return payload if isinstance(payload, dict) else None


def empty_change_counts() -> dict[str, int]:
    return {
        "devices_added": 0,
        "devices_removed": 0,
        "devices_modified": 0,
        "entities_added": 0,
        "entities_removed": 0,
        "entities_modified": 0,
        "orphan_entities_added": 0,
        "orphan_entities_removed": 0,
        "network_clients_added": 0,
        "network_clients_removed": 0,
        "network_clients_modified": 0,
        "total": 0,
    }


def default_status() -> dict[str, Any]:
    return {
        "generated_at": "",
        "api_enriched": False,
        "states_loaded": 0,
        "services_loaded": 0,
        "schema_version": SCHEMA_VERSION,
        "output_changed": {"json": False, "markdown": False},
        "severity": "none",
        "summary_message": "Inventory status pending",
        "change_counts": empty_change_counts(),
        "security_reasons": [],
        "warnings": [],
    }


def empty_digest(updated_at: str = "") -> dict[str, Any]:
    return {
        "schema_version": DIGEST_VERSION,
        "updated_at": updated_at,
        "pending_count": 0,
        "summary_message": "No inventory changes pending",
        "items": [],
    }


def collection_by_id(items: list[dict[str, Any]], key: str) -> dict[str, dict[str, Any]]:
    return {item[key]: item for item in items if item.get(key)}


def change_label(kind: str, item: dict[str, Any]) -> str:
    if kind == "network_clients":
        names = item.get("names") or []
        return names[0] if names else item.get("client_id", "network client")
    return item.get("name") or item.get("entity_id") or item.get("device_id") or "inventory item"


def change_summary(kind: str, action: str, item: dict[str, Any], changed_fields: list[str] | None = None) -> str:
    label = change_label(kind, item)
    kind_label = {
        "devices": "Device",
        "entities": "Entity",
        "orphan_entities": "Orphan entity",
        "network_clients": "Network client",
    }.get(kind, kind[:-1].replace("_", " ").title())
    action_label = {"added": "added", "removed": "removed", "modified": "changed"}.get(action, action)
    if action == "modified" and changed_fields:
        return f"{kind_label} {action_label}: {label} ({', '.join(changed_fields)})"
    return f"{kind_label} {action_label}: {label}"


def summarize_change_item(
    kind: str,
    action: str,
    item: dict[str, Any],
    changed_fields: list[str] | None = None,
) -> dict[str, Any]:
    identifier_key = {
        "devices": "device_id",
        "entities": "entity_id",
        "orphan_entities": "entity_id",
        "network_clients": "client_id",
    }[kind]
    summary = {
        "id": item.get(identifier_key, ""),
        "name": change_label(kind, item),
        "summary": change_summary(kind, action, item, changed_fields),
    }
    if kind == "entities":
        summary.update(
            {
                "domain": item.get("domain", ""),
                "role": item.get("role", ""),
                "platform": item.get("platform", ""),
                "device_id": item.get("device_id", ""),
            }
        )
    elif kind == "devices":
        summary.update(
            {
                "area": item.get("area", ""),
                "integrations": item.get("integrations", []),
                "control_count": item.get("control_count", 0),
                "telemetry_count": item.get("telemetry_count", 0),
                "network_count": item.get("network_count", 0),
            }
        )
    elif kind == "network_clients":
        summary.update(
            {
                "connection_types": item.get("connection_types", []),
                "network_scopes": item.get("network_scopes", []),
                "tracked_entity_ids": item.get("tracked_entity_ids", []),
                "device_ids": item.get("device_ids", []),
            }
        )
    if changed_fields:
        summary["changed_fields"] = changed_fields
    return summary


def diff_collection(
    previous_items: list[dict[str, Any]],
    current_items: list[dict[str, Any]],
    key: str,
    fields: tuple[str, ...],
    kind: str,
) -> dict[str, list[dict[str, Any]]]:
    previous_by_id = collection_by_id(previous_items, key)
    current_by_id = collection_by_id(current_items, key)
    previous_ids = set(previous_by_id)
    current_ids = set(current_by_id)

    added = [
        summarize_change_item(kind, "added", current_by_id[item_id])
        for item_id in sorted(current_ids - previous_ids)
    ]
    removed = [
        summarize_change_item(kind, "removed", previous_by_id[item_id])
        for item_id in sorted(previous_ids - current_ids)
    ]
    modified = []
    for item_id in sorted(previous_ids & current_ids):
        changed_fields = [
            field
            for field in fields
            if previous_by_id[item_id].get(field) != current_by_id[item_id].get(field)
        ]
        if changed_fields:
            modified.append(summarize_change_item(kind, "modified", current_by_id[item_id], changed_fields))
    return {"added": added, "removed": removed, "modified": modified}


def diff_orphan_entities(previous: dict[str, Any], current: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    previous_by_id = collection_by_id(previous.get("orphan_entities") or [], "entity_id")
    current_by_id = collection_by_id(current.get("orphan_entities") or [], "entity_id")
    previous_ids = set(previous_by_id)
    current_ids = set(current_by_id)
    return {
        "added": [
            summarize_change_item("orphan_entities", "added", current_by_id[item_id])
            for item_id in sorted(current_ids - previous_ids)
        ],
        "removed": [
            summarize_change_item("orphan_entities", "removed", previous_by_id[item_id])
            for item_id in sorted(previous_ids - current_ids)
        ],
    }


def count_changes(changes: dict[str, Any]) -> dict[str, int]:
    counts = empty_change_counts()
    for kind in ("devices", "entities", "network_clients"):
        for action in ("added", "removed", "modified"):
            counts[f"{kind}_{action}"] = len(changes[kind][action])
    counts["orphan_entities_added"] = len(changes["orphan_entities"]["added"])
    counts["orphan_entities_removed"] = len(changes["orphan_entities"]["removed"])
    counts["total"] = sum(value for key, value in counts.items() if key != "total")
    return counts


def security_reason_for_entity(entity: dict[str, Any], devices_by_id: dict[str, dict[str, Any]]) -> str:
    domain = entity.get("domain") or domain_from_entity_id(entity.get("id", ""))
    device = devices_by_id.get(entity.get("device_id", "")) or {}
    device_name = device.get("name") or ""
    location = f" on {device_name}" if device_name else ""
    entity_id = entity.get("id") or entity.get("entity_id") or entity.get("name") or "entity"
    entity_name = entity.get("name") or ""
    searchable = " ".join([entity_id, entity_name, device_name, entity.get("platform", "")])
    if domain in SENSITIVE_DOMAINS:
        return f"New sensitive {domain.replace('_', ' ')} entity{location}: {entity_id}"
    if entity.get("role") == "control" and SENSITIVE_NAME_RE.search(searchable):
        return f"New security-adjacent control{location}: {entity_id}"
    return ""


def security_reason_for_network_client(client: dict[str, Any]) -> str:
    label = client.get("name") or client.get("id") or "network client"
    connection_types = set(client.get("connection_types") or [])
    network_scopes = set(client.get("network_scopes") or [])
    if "wired" in connection_types:
        return f"New wired network client: {label}"
    if "trusted" in network_scopes:
        return f"New trusted-network client: {label}"
    return ""


def status_summary(severity: str, counts: dict[str, int], security_reasons: list[str], baseline: bool) -> str:
    if baseline:
        return "Inventory baseline captured"
    if counts["total"] == 0:
        return "Inventory unchanged"
    if severity == "security":
        return f"Security review needed: {len(security_reasons)} sensitive inventory change(s)"

    phrases = []
    for key, label in (
        ("devices_added", "devices added"),
        ("devices_removed", "devices removed"),
        ("devices_modified", "devices changed"),
        ("entities_added", "entities added"),
        ("entities_removed", "entities removed"),
        ("entities_modified", "entities changed"),
        ("network_clients_added", "network clients added"),
        ("network_clients_removed", "network clients removed"),
        ("network_clients_modified", "network clients changed"),
        ("orphan_entities_added", "orphan entities added"),
    ):
        if counts.get(key):
            phrases.append(f"{counts[key]} {label}")
    if not phrases:
        return f"Inventory changed: {counts['total']} change(s)"
    return "Inventory changed: " + "; ".join(phrases[:4])


def load_previous_inventory(path: Path) -> tuple[dict[str, Any] | None, str]:
    if not path.exists():
        return None, "previous inventory not found; baseline captured"
    previous = read_json_or_none(path)
    if previous is None:
        return None, "previous inventory unreadable; baseline captured"
    if previous.get("schema_version") != SCHEMA_VERSION:
        return None, "previous inventory schema changed; baseline captured"
    return previous, ""


def build_change_report(
    previous: dict[str, Any] | None,
    current: dict[str, Any],
    generated_at: str,
    baseline_reason: str = "",
) -> dict[str, Any]:
    empty_changes = {
        "devices": {"added": [], "removed": [], "modified": []},
        "entities": {"added": [], "removed": [], "modified": []},
        "orphan_entities": {"added": [], "removed": []},
        "network_clients": {"added": [], "removed": [], "modified": []},
    }
    if previous is None:
        counts = empty_change_counts()
        return {
            "schema_version": CHANGE_REPORT_VERSION,
            "generated_at": generated_at,
            "baseline": True,
            "baseline_reason": baseline_reason,
            "severity": "none",
            "summary_message": status_summary("none", counts, [], True),
            "change_counts": counts,
            "security_reasons": [],
            "changes": empty_changes,
        }

    changes = {
        "devices": diff_collection(
            previous.get("devices") or [],
            current.get("devices") or [],
            "device_id",
            (
                "name",
                "area",
                "manufacturer",
                "model",
                "integrations",
                "disabled_by",
                "entry_type",
                "entities",
            ),
            "devices",
        ),
        "entities": diff_collection(
            previous.get("entities") or [],
            current.get("entities") or [],
            "entity_id",
            (
                "name",
                "domain",
                "role",
                "platform",
                "device_class",
                "unit",
                "entity_category",
                "disabled_by",
                "hidden_by",
                "capability_keys",
                "device_id",
                "area",
            ),
            "entities",
        ),
        "orphan_entities": diff_orphan_entities(previous, current),
        "network_clients": diff_collection(
            previous.get("network_clients") or [],
            current.get("network_clients") or [],
            "client_id",
            (
                "sources",
                "tracked_entity_ids",
                "device_ids",
                "names",
                "connection_types",
                "network_scopes",
            ),
            "network_clients",
        ),
    }
    counts = count_changes(changes)
    devices_by_id = collection_by_id(current.get("devices") or [], "device_id")
    added_entities = collection_by_id(current.get("entities") or [], "entity_id")
    added_network_clients = collection_by_id(current.get("network_clients") or [], "client_id")

    security_reasons = []
    for change in changes["entities"]["added"]:
        entity = added_entities.get(change["id"]) or {}
        reason = security_reason_for_entity(entity, devices_by_id)
        if reason:
            security_reasons.append(reason)
    for change in changes["network_clients"]["added"]:
        client = added_network_clients.get(change["id"]) or {}
        reason = security_reason_for_network_client({**client, **change})
        if reason:
            security_reasons.append(reason)

    security_reasons = sorted(dict.fromkeys(security_reasons))
    severity = "none"
    if counts["total"]:
        severity = "security" if security_reasons else "review"

    return {
        "schema_version": CHANGE_REPORT_VERSION,
        "generated_at": generated_at,
        "baseline": False,
        "baseline_reason": "",
        "severity": severity,
        "summary_message": status_summary(severity, counts, security_reasons, False),
        "change_counts": counts,
        "security_reasons": security_reasons,
        "changes": changes,
    }


def digest_items_from_report(report: dict[str, Any]) -> list[dict[str, Any]]:
    items = []
    changes = report.get("changes") or {}
    for kind in ("devices", "entities", "network_clients"):
        for action in ("added", "removed", "modified"):
            for change in (changes.get(kind) or {}).get(action) or []:
                signature_source = f"{kind}:{action}:{change.get('id', '')}:{','.join(change.get('changed_fields') or [])}"
                signature = hashlib.blake2s(signature_source.encode("utf-8"), digest_size=8).hexdigest()
                items.append(
                    {
                        "signature": signature,
                        "kind": kind,
                        "action": action,
                        "summary": change.get("summary", ""),
                    }
                )
    for action in ("added", "removed"):
        for change in (changes.get("orphan_entities") or {}).get(action) or []:
            signature_source = f"orphan_entities:{action}:{change.get('id', '')}"
            signature = hashlib.blake2s(signature_source.encode("utf-8"), digest_size=8).hexdigest()
            items.append(
                {
                    "signature": signature,
                    "kind": "orphan_entities",
                    "action": action,
                    "summary": change.get("summary", ""),
                }
            )
    return sorted(items, key=lambda item: (item["summary"], item["signature"]))


def load_digest(path: Path) -> dict[str, Any]:
    digest = read_json_or_none(path)
    if not digest or digest.get("schema_version") != DIGEST_VERSION:
        return empty_digest()
    digest.setdefault("pending_count", len(digest.get("items") or []))
    digest.setdefault("summary_message", "No inventory changes pending")
    digest.setdefault("items", [])
    return digest


def update_pending_digest(path: Path, report: dict[str, Any]) -> dict[str, Any]:
    digest = load_digest(path)
    if report.get("severity") != "review":
        return digest

    now = report.get("generated_at") or dt.datetime.now(dt.timezone.utc).isoformat()
    existing = {item.get("signature"): item for item in digest.get("items") or [] if item.get("signature")}
    for item in digest_items_from_report(report):
        previous = existing.get(item["signature"])
        if previous:
            previous["last_seen"] = now
            previous["occurrences"] = int(previous.get("occurrences") or 1) + 1
        else:
            item["first_seen"] = now
            item["last_seen"] = now
            item["occurrences"] = 1
            existing[item["signature"]] = item

    items = sorted(existing.values(), key=lambda item: (item.get("first_seen", ""), item.get("summary", "")))
    if len(items) > 100:
        items = items[-100:]
    pending_count = len(items)
    digest = {
        "schema_version": DIGEST_VERSION,
        "updated_at": now,
        "pending_count": pending_count,
        "summary_message": f"{pending_count} inventory change(s) pending review",
        "items": items,
    }
    write_json_if_changed(path, digest)
    return digest


def clear_pending_digest(path: Path) -> dict[str, Any]:
    now = dt.datetime.now(dt.timezone.utc).isoformat()
    digest = empty_digest(now)
    digest["cleared_at"] = now
    write_json_if_changed(path, digest)
    return digest


def api_get_json(api_url: str, token: str, path: str, timeout: float) -> Any:
    request = urllib.request.Request(
        f"{api_url.rstrip('/')}{path}",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.load(response)


def load_api_data(api_url: str, token_file: Path, timeout: float) -> tuple[list[dict[str, Any]] | None, Any, list[str]]:
    warnings: list[str] = []
    if not token_file.exists():
        warnings.append(f"token file not found: {token_file}")
        return None, None, warnings
    token = token_file.read_text(encoding="utf-8").strip()
    if not token:
        warnings.append(f"token file is empty: {token_file}")
        return None, None, warnings
    try:
        states = api_get_json(api_url, token, "/api/states", timeout)
        services = api_get_json(api_url, token, "/api/services", timeout)
    except (OSError, urllib.error.URLError, json.JSONDecodeError) as exc:
        warnings.append(f"api enrichment failed: {exc}")
        return None, None, warnings
    return states if isinstance(states, list) else None, services, warnings


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    default_dir = default_config_dir()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config-dir", type=Path, default=default_dir)
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--backup", type=Path, help="Read registries from a Home Assistant backup tarball.")
    parser.add_argument("--salt-file", type=Path)
    parser.add_argument("--token-file", type=Path)
    parser.add_argument("--status-file", type=Path)
    parser.add_argument("--changes-file", type=Path)
    parser.add_argument("--digest-file", type=Path)
    parser.add_argument("--api-url", default="http://127.0.0.1:8123")
    parser.add_argument("--api-timeout", type=float, default=10.0)
    parser.add_argument("--no-api", action="store_true")
    parser.add_argument("--print-status", action="store_true", help="Print safe status JSON for Home Assistant sensors.")
    parser.add_argument("--print-digest", action="store_true", help="Print safe pending digest JSON for Home Assistant sensors.")
    parser.add_argument("--clear-digest", action="store_true", help="Clear the pending inventory digest queue.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    config_dir = args.config_dir.resolve()
    output_dir = (args.output_dir or config_dir / "docs").resolve()
    salt_file = (args.salt_file or config_dir / ".inventory_salt").resolve()
    token_file = (args.token_file or config_dir / ".inventory_token").resolve()
    status_file = (args.status_file or config_dir / ".device_inventory_status.json").resolve()
    changes_file = (args.changes_file or config_dir / ".device_inventory_changes.json").resolve()
    digest_file = (args.digest_file or config_dir / ".device_inventory_digest.json").resolve()

    if args.print_status:
        print(json.dumps(read_json_or_none(status_file) or default_status(), sort_keys=True))
        return 0
    if args.print_digest:
        print(json.dumps(load_digest(digest_file), sort_keys=True))
        return 0
    if args.clear_digest:
        print(json.dumps(clear_pending_digest(digest_file), sort_keys=True))
        return 0

    salt = ensure_salt(salt_file)
    warnings: list[str] = []
    states = None
    services = None
    if not args.no_api:
        states, services, api_warnings = load_api_data(args.api_url, token_file, args.api_timeout)
        warnings.extend(api_warnings)

    registries = load_registries(config_dir, args.backup.resolve() if args.backup else None)
    inventory = build_inventory(registries, states, services, salt)
    generated_at = dt.datetime.now(dt.timezone.utc).isoformat()
    previous_inventory, baseline_warning = load_previous_inventory(output_dir / "device-inventory.json")
    change_report = build_change_report(previous_inventory, inventory, generated_at, baseline_warning)

    json_text = json.dumps(inventory, indent=2, sort_keys=True) + "\n"
    markdown_text = render_markdown(inventory)
    changed = {
        "json": write_if_changed(output_dir / "device-inventory.json", json_text),
        "markdown": write_if_changed(output_dir / "device-inventory.md", markdown_text),
    }
    write_json_if_changed(changes_file, change_report)
    update_pending_digest(digest_file, change_report)

    status_warnings = warnings[:]
    if baseline_warning:
        status_warnings.append(baseline_warning)

    status = {
        "generated_at": generated_at,
        "api_enriched": states is not None,
        "states_loaded": len(states or []),
        "services_loaded": len(services or []) if isinstance(services, list) else len(services or {}),
        "schema_version": SCHEMA_VERSION,
        "output_changed": changed,
        "severity": change_report["severity"],
        "summary_message": change_report["summary_message"],
        "change_counts": change_report["change_counts"],
        "security_reasons": change_report["security_reasons"],
        "warnings": status_warnings,
    }
    write_json_if_changed(status_file, status)
    print(
        json.dumps(
            {
                "summary": inventory["summary"],
                "changed": changed,
                "api_enriched": states is not None,
                "severity": change_report["severity"],
                "summary_message": change_report["summary_message"],
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
