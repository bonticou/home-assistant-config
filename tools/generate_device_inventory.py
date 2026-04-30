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


SCHEMA_VERSION = 1

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


def build_network_clients(
    entities: list[dict[str, Any]],
    devices_by_raw_id: dict[str, str],
    unifi_data: dict[str, Any],
    salt: str,
) -> list[dict[str, Any]]:
    clients: dict[str, dict[str, Any]] = {}

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

    public_clients: list[dict[str, Any]] = []
    for client in clients.values():
        public_clients.append(
            {
                "client_id": client["client_id"],
                "sources": sorted(client["sources"]),
                "tracked_entity_ids": sorted(client["tracked_entity_ids"]),
                "device_ids": sorted(client["device_ids"]),
                "names": sorted(client["names"]),
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
    network_clients = build_network_clients(raw_entities, device_public_ids, registries.get("unifi_data") or {}, salt)

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
                ["Client ID", "Sources", "Tracked Entities", "Names"],
                [
                    [
                        f"`{client['client_id']}`",
                        ", ".join(client["sources"]),
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
    parser.add_argument("--api-url", default="http://127.0.0.1:8123")
    parser.add_argument("--api-timeout", type=float, default=10.0)
    parser.add_argument("--no-api", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    config_dir = args.config_dir.resolve()
    output_dir = (args.output_dir or config_dir / "docs").resolve()
    salt_file = (args.salt_file or config_dir / ".inventory_salt").resolve()
    token_file = (args.token_file or config_dir / ".inventory_token").resolve()
    status_file = (args.status_file or config_dir / ".device_inventory_status.json").resolve()

    salt = ensure_salt(salt_file)
    warnings: list[str] = []
    states = None
    services = None
    if not args.no_api:
        states, services, api_warnings = load_api_data(args.api_url, token_file, args.api_timeout)
        warnings.extend(api_warnings)

    registries = load_registries(config_dir, args.backup.resolve() if args.backup else None)
    inventory = build_inventory(registries, states, services, salt)

    json_text = json.dumps(inventory, indent=2, sort_keys=True) + "\n"
    markdown_text = render_markdown(inventory)
    changed = {
        "json": write_if_changed(output_dir / "device-inventory.json", json_text),
        "markdown": write_if_changed(output_dir / "device-inventory.md", markdown_text),
    }

    status = {
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "api_enriched": states is not None,
        "states_loaded": len(states or []),
        "services_loaded": len(services or []) if isinstance(services, list) else len(services or {}),
        "schema_version": SCHEMA_VERSION,
        "output_changed": changed,
        "warnings": warnings,
    }
    write_if_changed(status_file, json.dumps(status, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"summary": inventory["summary"], "changed": changed, "api_enriched": states is not None}, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
