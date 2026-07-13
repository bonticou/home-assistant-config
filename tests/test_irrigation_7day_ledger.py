import unittest

from tools import irrigation_7day_ledger as ledger


class Irrigation7DayLedgerTest(unittest.TestCase):
    def test_merge_zone_sources_unions_history_with_hydrawise_daily_runtime(self):
        day = "2026-07-10"
        zone_names = {
            "Zone 1": "Zone 1",
            "Zone 15": "Zone 15",
            "Zone 23": "Vegetable garden",
        }
        primary = {
            day: [
                {
                    "zone": "Zone 15",
                    "zone_name": "Zone 15",
                    "duration_minutes": 22.2,
                    "gallons": 1059.01,
                    "source": "irrigation_history",
                },
                {
                    "zone": "Vegetable garden",
                    "zone_name": "Vegetable garden",
                    "duration_minutes": 6.5,
                    "gallons": 0,
                    "source": "irrigation_history",
                },
            ]
        }
        fallback = {
            day: [
                {
                    "zone": "Zone 1",
                    "zone_name": "Zone 1",
                    "duration_minutes": 15,
                    "gallons": 0,
                    "source": "hydrawise_daily_active_time",
                },
                {
                    "zone": "Zone 15",
                    "zone_name": "Zone 15",
                    "duration_minutes": 15,
                    "gallons": 0,
                    "source": "hydrawise_daily_active_time",
                },
                {
                    "zone": "Zone 23",
                    "zone_name": "Vegetable garden",
                    "duration_minutes": 10,
                    "gallons": 0,
                    "source": "hydrawise_daily_active_time",
                },
            ]
        }

        merged = ledger.merge_zone_sources(primary, fallback, [day], zone_names)[day]

        self.assertEqual({item["zone"] for item in merged}, {"Zone 1", "Zone 15", "Zone 23"})
        zone_15 = next(item for item in merged if item["zone"] == "Zone 15")
        self.assertEqual(zone_15["duration_minutes"], 22.2)
        self.assertEqual(zone_15["gallons"], 1059.01)
        self.assertEqual(zone_15["source"], "hydrawise_daily_active_time+irrigation_history")
        vegetable = next(item for item in merged if item["zone"] == "Zone 23")
        self.assertEqual(vegetable["zone_name"], "Vegetable garden")
        self.assertEqual(vegetable["duration_minutes"], 10)

    def test_zone_label_reports_source_without_overclaiming_full_cycle(self):
        hydrawise_zones = [
            {"zone": f"Zone {index}", "source": "hydrawise_daily_active_time"}
            for index in range(1, 8)
        ]
        history_zones = [
            {"zone": f"Zone {index}", "source": "irrigation_history"}
            for index in range(1, 8)
        ]

        self.assertEqual(ledger.zones_label(hydrawise_zones, 28000), "Hydrawise logged 7 zones")
        self.assertEqual(ledger.zones_label(history_zones, 28000), "7 zones recorded")


if __name__ == "__main__":
    unittest.main()
