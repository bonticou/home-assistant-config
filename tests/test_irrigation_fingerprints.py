from __future__ import annotations

import argparse
import unittest

from tools import irrigation_fingerprints as fingerprints


class IrrigationFingerprintTests(unittest.TestCase):
    def record_sample(
        self,
        data: dict,
        *,
        zone: str = "Zone 1",
        start: str,
        end: str,
        gallons: float,
        pressure_start: float = 50.0,
        pressure_end: float = 44.0,
        flow_start: float = 6.0,
        flow_end: float = 6.0,
        active_count: int = 1,
    ) -> None:
        fingerprints.start_sample(
            argparse.Namespace(
                zone=zone,
                at=start,
                pressure=str(pressure_start),
                flow=str(flow_start),
                gallons="0",
                active_count=str(active_count),
            ),
            data,
        )
        fingerprints.finish_sample(
            argparse.Namespace(
                zone=zone,
                at=end,
                pressure=str(pressure_end),
                flow=str(flow_end),
                gallons=str(gallons),
                active_count=str(active_count),
            ),
            data,
        )

    def test_reset_clears_learned_samples_and_active_state(self):
        data = fingerprints.initial_data()
        data["active"] = {"Zone 1": {"zone": "Zone 1"}}
        data["zones"] = {"Zone 1": {"samples": [{"gallons": 12}]}}
        data["latest_sample"] = {"zone": "Zone 1"}
        data["latest_anomaly"] = {"zone": "Zone 1", "kind": "break_possible"}

        self.assertEqual(fingerprints.reset_data(), fingerprints.initial_data())

    def test_baseline_requires_three_clean_prior_samples(self):
        data = fingerprints.initial_data()

        self.record_sample(
            data,
            start="2026-06-29T08:00:00-04:00",
            end="2026-06-29T08:10:00-04:00",
            gallons=60,
        )
        self.record_sample(
            data,
            start="2026-06-30T08:00:00-04:00",
            end="2026-06-30T08:10:00-04:00",
            gallons=62,
        )
        self.record_sample(
            data,
            start="2026-07-01T08:00:00-04:00",
            end="2026-07-01T08:10:00-04:00",
            gallons=20,
            flow_start=2.0,
            flow_end=2.0,
            pressure_end=49.0,
        )

        status = fingerprints.summarize(data)
        self.assertEqual(status["zones"]["Zone 1"]["sample_count"], 3)
        self.assertTrue(status["zones"]["Zone 1"]["learned"])
        self.assertEqual(status["latest_anomaly"], "")

    def test_high_flow_alerts_after_baseline_is_learned(self):
        data = fingerprints.initial_data()

        for day in range(1, 4):
            self.record_sample(
                data,
                start=f"2026-07-0{day}T08:00:00-04:00",
                end=f"2026-07-0{day}T08:10:00-04:00",
                gallons=60,
                flow_start=6.0,
                flow_end=6.0,
                pressure_end=44.0,
            )

        self.record_sample(
            data,
            start="2026-07-04T08:00:00-04:00",
            end="2026-07-04T08:10:00-04:00",
            gallons=110,
            flow_start=11.0,
            flow_end=11.0,
            pressure_end=34.0,
        )

        status = fingerprints.summarize(data)
        self.assertEqual(status["latest_anomaly"], "break_possible")
        self.assertEqual(status["latest_anomaly_zone"], "Zone 1")


if __name__ == "__main__":
    unittest.main()
