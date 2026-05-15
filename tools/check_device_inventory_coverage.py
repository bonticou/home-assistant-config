#!/usr/bin/env python3
"""Check that active HA config entity references are represented in inventory."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


CONTROL_DOMAINS = {
    "alarm_control_panel",
    "climate",
    "cover",
    "fan",
    "light",
    "lock",
    "media_player",
    "remote",
    "siren",
    "switch",
    "vacuum",
    "valve",
}

SERVICE_OR_TEMPLATE_SUFFIXES = {
    "close_cover",
    "entity_id",
    "lock",
    "media_pause",
    "name",
    "open_cover",
    "select_source",
    "turn_off",
    "turn_on",
    "volume_set",
}

DEFAULT_CONFIG_FILES = (
    "configuration.yaml",
    "automations.yaml",
    "scripts.yaml",
    "scenes.yaml",
    "dashboards/calm_mobile.yaml",
)


def load_known_entities(path: Path) -> set[str]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    known = {entity["entity_id"] for entity in payload.get("entities", [])}
    known.update(entity["entity_id"] for entity in payload.get("orphan_entities", []))
    return known


def referenced_entities(repo: Path, files: tuple[str, ...]) -> set[str]:
    pattern = re.compile(
        r"(?<![A-Za-z0-9_])("
        + "|".join(sorted(CONTROL_DOMAINS))
        + r")\.([a-z0-9_]+)"
    )
    found: set[str] = set()
    for relative in files:
        path = repo / relative
        if not path.exists():
            continue
        for line in path.read_text(encoding="utf-8").splitlines():
            if re.search(r"\bexample\s*:", line):
                continue
            for match in pattern.finditer(line):
                suffix = match.group(2)
                if suffix in SERVICE_OR_TEMPLATE_SUFFIXES:
                    continue
                found.add(match.group(0))
    return found


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path("."))
    parser.add_argument("--inventory", type=Path, default=Path("docs/device-inventory.json"))
    parser.add_argument("--config-file", action="append", dest="config_files")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    repo = args.repo.resolve()
    inventory_path = args.inventory if args.inventory.is_absolute() else repo / args.inventory
    config_files = tuple(args.config_files or DEFAULT_CONFIG_FILES)
    known = load_known_entities(inventory_path)
    referenced = referenced_entities(repo, config_files)
    missing = sorted(entity_id for entity_id in referenced if entity_id not in known)
    if missing:
        print("Inventory is missing active config entity references:", file=sys.stderr)
        for entity_id in missing:
            print(f"- {entity_id}", file=sys.stderr)
        print("Regenerate or update docs/device-inventory.json and docs/device-inventory.md.", file=sys.stderr)
        return 1
    print(f"Inventory coverage ok: {len(referenced)} active control entity references are recorded.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
