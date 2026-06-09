from __future__ import annotations

import unittest

from tools import irrigation_fingerprints as fingerprints


class IrrigationFingerprintTests(unittest.TestCase):
    def test_reset_clears_learned_samples_and_active_state(self):
        data = fingerprints.initial_data()
        data["active"] = {"Zone 1": {"zone": "Zone 1"}}
        data["zones"] = {"Zone 1": {"samples": [{"gallons": 12}]}}
        data["latest_sample"] = {"zone": "Zone 1"}
        data["latest_anomaly"] = {"zone": "Zone 1", "kind": "break_possible"}

        self.assertEqual(fingerprints.reset_data(), fingerprints.initial_data())


if __name__ == "__main__":
    unittest.main()
