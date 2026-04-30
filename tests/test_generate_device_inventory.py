from __future__ import annotations

import copy
import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path

from tools import generate_device_inventory as inventory


FIXTURE_CONFIG = Path(__file__).parent / "fixtures" / "inventory_config"
TEST_SALT = "unit-test-salt"


class DeviceInventoryTests(unittest.TestCase):
    def build_fixture_inventory(self):
        registries = inventory.load_registries(FIXTURE_CONFIG)
        states = [
            {"entity_id": "binary_sensor.kitchen_motion", "state": "off", "attributes": {}},
            {"entity_id": "switch.kitchen_light", "state": "unavailable", "attributes": {}},
        ]
        return inventory.build_inventory(registries, states, services={}, salt=TEST_SALT)

    def test_classifies_entity_roles(self):
        self.assertEqual(inventory.classify_role({"entity_id": "sensor.temperature"}), "telemetry")
        self.assertEqual(inventory.classify_role({"entity_id": "switch.lamp"}), "control")
        self.assertEqual(inventory.classify_role({"entity_id": "input_boolean.flag"}), "control")
        self.assertEqual(
            inventory.classify_role({"entity_id": "device_tracker.phone", "platform": "unifi"}),
            "network",
        )

    def test_redacts_network_identifiers(self):
        sanitized = inventory.sanitize_string(
            "device_tracker.unifi_default_aa_bb_cc_dd_ee_ff at 192.168.1.10",
            TEST_SALT,
        )
        self.assertNotIn("aa_bb_cc_dd_ee_ff", sanitized)
        self.assertNotIn("192.168.1.10", sanitized)
        self.assertIn("mac_", sanitized)
        self.assertIn("ip_", sanitized)

    def test_builds_devices_entities_and_network_clients(self):
        result = self.build_fixture_inventory()
        self.assertEqual(result["summary"]["device_count"], 2)
        self.assertEqual(result["summary"]["entity_count"], 4)
        self.assertEqual(result["summary"]["orphan_entity_count"], 1)
        self.assertEqual(result["summary"]["role_counts"]["network"], 1)
        self.assertEqual(result["summary"]["role_counts"]["control"], 2)
        self.assertEqual(result["summary"]["role_counts"]["telemetry"], 1)

        rendered = json.dumps(result, sort_keys=True)
        self.assertNotIn("aa:bb:cc:dd:ee:ff", rendered)
        self.assertNotIn("aa_bb_cc_dd_ee_ff", rendered)
        self.assertNotIn("secret-serial", rendered)
        self.assertEqual(len(result["network_clients"]), 2)

    def test_write_if_changed_is_stable(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "out.json"
            self.assertTrue(inventory.write_if_changed(path, "{}\n"))
            first_mtime = path.stat().st_mtime_ns
            self.assertFalse(inventory.write_if_changed(path, "{}\n"))
            self.assertEqual(first_mtime, path.stat().st_mtime_ns)
            self.assertTrue(inventory.write_if_changed(path, "{\"changed\": true}\n"))

    def test_first_run_is_silent_baseline(self):
        current = self.build_fixture_inventory()
        report = inventory.build_change_report(None, current, "2026-04-30T12:00:00+00:00", "missing")

        self.assertTrue(report["baseline"])
        self.assertEqual(report["severity"], "none")
        self.assertEqual(report["change_counts"]["total"], 0)
        self.assertEqual(report["summary_message"], "Inventory baseline captured")

    def test_detects_added_removed_and_modified_inventory_items(self):
        previous = self.build_fixture_inventory()
        current = copy.deepcopy(previous)
        current["entities"].pop(0)
        current["entities"].append(
            {
                "entity_id": "sensor.kitchen_air_quality",
                "name": "Kitchen Air Quality",
                "domain": "sensor",
                "role": "telemetry",
                "platform": "zha",
                "device_class": "aqi",
                "unit": "",
                "entity_category": "",
                "disabled_by": "",
                "hidden_by": "",
                "availability": "available",
                "capability_keys": [],
                "device_id": "",
                "area": "Kitchen",
            }
        )
        current["devices"][0]["area"] = "Pantry"
        current["network_clients"].append(
            {
                "client_id": "network_test_unknown",
                "sources": ["entity_registry"],
                "tracked_entity_ids": [],
                "device_ids": [],
                "names": ["Test Client"],
                "connection_types": [],
                "network_scopes": [],
            }
        )
        current["orphan_entities"].append(current["entities"][-1])

        report = inventory.build_change_report(previous, current, "2026-04-30T12:00:00+00:00")

        self.assertEqual(report["severity"], "review")
        self.assertEqual(report["change_counts"]["entities_added"], 1)
        self.assertEqual(report["change_counts"]["entities_removed"], 1)
        self.assertEqual(report["change_counts"]["devices_modified"], 1)
        self.assertEqual(report["change_counts"]["network_clients_added"], 1)
        self.assertEqual(report["change_counts"]["orphan_entities_added"], 1)

    def test_sensitive_added_entity_is_security_change(self):
        previous = self.build_fixture_inventory()
        current = copy.deepcopy(previous)
        device_id = "device_test_lock"
        current["devices"].append(
            {
                "device_id": device_id,
                "name": "Front Door Lock",
                "area": "Entry",
                "manufacturer": "Aqara",
                "model": "U100",
                "integrations": ["matter"],
                "disabled_by": "",
                "entry_type": "",
                "entity_count": 1,
                "telemetry_count": 0,
                "control_count": 1,
                "network_count": 0,
                "other_count": 0,
                "entities": ["lock.front_door"],
            }
        )
        current["entities"].append(
            {
                "entity_id": "lock.front_door",
                "name": "Front Door",
                "domain": "lock",
                "role": "control",
                "platform": "matter",
                "device_class": "",
                "unit": "",
                "entity_category": "",
                "disabled_by": "",
                "hidden_by": "",
                "availability": "available",
                "capability_keys": [],
                "device_id": device_id,
                "area": "Entry",
            }
        )

        report = inventory.build_change_report(previous, current, "2026-04-30T12:00:00+00:00")

        self.assertEqual(report["severity"], "security")
        self.assertTrue(any("lock" in reason for reason in report["security_reasons"]))

    def test_unknown_network_clients_are_review_unless_wired_or_trusted(self):
        previous = self.build_fixture_inventory()
        review_current = copy.deepcopy(previous)
        review_current["network_clients"].append(
            {
                "client_id": "network_review_only",
                "sources": ["entity_registry"],
                "tracked_entity_ids": [],
                "device_ids": [],
                "names": ["Unknown Wireless"],
                "connection_types": [],
                "network_scopes": [],
            }
        )
        review_report = inventory.build_change_report(previous, review_current, "2026-04-30T12:00:00+00:00")
        self.assertEqual(review_report["severity"], "review")

        security_current = copy.deepcopy(previous)
        security_current["network_clients"].append(
            {
                "client_id": "network_wired",
                "sources": ["entity_registry"],
                "tracked_entity_ids": [],
                "device_ids": [],
                "names": ["Unknown Wired"],
                "connection_types": ["wired"],
                "network_scopes": [],
            }
        )
        security_report = inventory.build_change_report(previous, security_current, "2026-04-30T12:00:00+00:00")
        self.assertEqual(security_report["severity"], "security")

    def test_unifi_state_attributes_add_safe_network_hints(self):
        registries = inventory.load_registries(FIXTURE_CONFIG)
        states = [
            {
                "entity_id": "device_tracker.unifi_default_aa_bb_cc_dd_ee_ff",
                "state": "home",
                "attributes": {
                    "is_wired": True,
                    "network": "Default",
                    "ip": "192.168.1.10",
                    "mac": "aa:bb:cc:dd:ee:ff",
                },
            }
        ]
        result = inventory.build_inventory(registries, states, services={}, salt=TEST_SALT)
        clients = [client for client in result["network_clients"] if client["tracked_entity_ids"]]

        self.assertEqual(clients[0]["connection_types"], ["wired"])
        self.assertEqual(clients[0]["network_scopes"], ["trusted"])
        rendered = json.dumps(result, sort_keys=True)
        self.assertNotIn("192.168.1.10", rendered)
        self.assertNotIn("aa:bb:cc:dd:ee:ff", rendered)

    def test_pending_digest_deduplicates_and_clears(self):
        report = {
            "generated_at": "2026-04-30T12:00:00+00:00",
            "severity": "review",
            "changes": {
                "devices": {"added": [{"id": "device_new", "summary": "Device added: Sensor"}], "removed": [], "modified": []},
                "entities": {"added": [], "removed": [], "modified": []},
                "network_clients": {"added": [], "removed": [], "modified": []},
                "orphan_entities": {"added": [], "removed": []},
            },
        }
        with tempfile.TemporaryDirectory() as temp_dir:
            digest_path = Path(temp_dir) / "digest.json"
            first = inventory.update_pending_digest(digest_path, report)
            second = inventory.update_pending_digest(digest_path, report)
            self.assertEqual(first["pending_count"], 1)
            self.assertEqual(second["pending_count"], 1)
            self.assertEqual(second["items"][0]["occurrences"], 2)

            cleared = inventory.clear_pending_digest(digest_path)
            self.assertEqual(cleared["pending_count"], 0)
            self.assertEqual(inventory.load_digest(digest_path)["pending_count"], 0)

    def test_main_no_api_succeeds_and_records_status(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            output_dir = temp_path / "docs"
            status_path = temp_path / "status.json"
            with contextlib.redirect_stdout(io.StringIO()):
                result = inventory.main(
                    [
                        "--config-dir",
                        str(FIXTURE_CONFIG),
                        "--output-dir",
                        str(output_dir),
                        "--salt-file",
                        str(temp_path / "salt"),
                        "--status-file",
                        str(status_path),
                        "--changes-file",
                        str(temp_path / "changes.json"),
                        "--digest-file",
                        str(temp_path / "digest.json"),
                        "--no-api",
                    ]
                )

            self.assertEqual(result, 0)
            status = json.loads(status_path.read_text(encoding="utf-8"))
            self.assertFalse(status["api_enriched"])
            self.assertEqual(status["severity"], "none")
            self.assertEqual(status["summary_message"], "Inventory baseline captured")

    def test_print_status_has_safe_default_without_file(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            buffer = io.StringIO()
            with contextlib.redirect_stdout(buffer):
                result = inventory.main(
                    [
                        "--config-dir",
                        temp_dir,
                        "--status-file",
                        str(Path(temp_dir) / "missing-status.json"),
                        "--print-status",
                    ]
                )

            self.assertEqual(result, 0)
            payload = json.loads(buffer.getvalue())
            self.assertEqual(payload["summary_message"], "Inventory status pending")


if __name__ == "__main__":
    unittest.main()
