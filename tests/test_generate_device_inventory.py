from __future__ import annotations

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


if __name__ == "__main__":
    unittest.main()
