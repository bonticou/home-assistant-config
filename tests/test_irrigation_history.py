from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from tools import irrigation_history as history


class IrrigationHistoryTests(unittest.TestCase):
    def run_tool(self, temp_dir: str, *args: str) -> dict:
        data_file = Path(temp_dir) / "history.json"
        status_file = Path(temp_dir) / "status.json"
        argv = [
            "--data-file",
            str(data_file),
            "--status-file",
            str(status_file),
            *args,
        ]
        parser = history.build_parser()
        parsed = parser.parse_args(argv)
        data = history.load_data(parsed.data_file)

        if parsed.command == "event":
            history.generic_event(parsed, data)
        elif parsed.command == "session-start":
            history.session_start(parsed, data)
        elif parsed.command == "session-finish":
            history.session_finish(parsed, data)
        elif parsed.command == "zone-start":
            history.zone_start(parsed, data)
        elif parsed.command == "zone-finish":
            history.zone_finish(parsed, data)
        elif parsed.status:
            pass
        else:
            self.fail(f"unsupported command {parsed.command}")

        history.write_json(parsed.data_file, data)
        return history.mark_status(data, parsed.status_file)

    def test_records_session_zone_and_event_history(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            self.run_tool(
                temp_dir,
                "session-start",
                "--session-id",
                "s1",
                "--at",
                "2026-05-27T08:00:00-04:00",
                "--zone",
                "Zone 1",
                "--pressure",
                "52.1",
                "--flow",
                "5.4",
                "--gallons",
                "100",
                "--flow-source",
                "hunter",
            )
            self.run_tool(
                temp_dir,
                "zone-start",
                "--zone",
                "Zone 1",
                "--session-id",
                "s1",
                "--at",
                "2026-05-27T08:00:00-04:00",
                "--pressure",
                "52.1",
                "--flow",
                "5.4",
                "--gallons",
                "100",
                "--flow-source",
                "hunter",
            )
            status = self.run_tool(
                temp_dir,
                "zone-finish",
                "--zone",
                "Zone 1",
                "--session-id",
                "s1",
                "--at",
                "2026-05-27T08:10:00-04:00",
                "--duration-minutes",
                "10",
                "--gallons",
                "54",
                "--flow-source",
                "hunter",
                "--avg-flow",
                "5.4",
                "--max-flow",
                "5.8",
                "--pressure-drop",
                "6.1",
            )
            self.assertEqual(status["zone_run_count"], 1)
            self.assertEqual(status["latest_zone_run"]["zone"], "Zone 1")
            self.assertEqual(status["latest_zone_run"]["duration_minutes"], 10)
            self.assertEqual(status["latest_zone_run"]["flow_source"], "hunter")

            status = self.run_tool(
                temp_dir,
                "session-finish",
                "--session-id",
                "s1",
                "--at",
                "2026-05-27T08:12:00-04:00",
                "--runtime-minutes",
                "12",
                "--gallons",
                "54",
                "--flow-source",
                "hunter",
                "--min-pressure",
                "46",
                "--max-flow",
                "5.8",
                "--current-pressure",
                "50",
            )
            self.assertEqual(status["session_count"], 1)
            self.assertEqual(status["latest_session"]["runtime_minutes"], 12)
            self.assertEqual(status["latest_session"]["flow_source"], "hunter")
            self.assertEqual(status["latest_event"]["kind"], "session_finished")

    def test_bounds_history_lists(self):
        data = history.initial_data()
        for index in range(history.MAX_EVENTS + 5):
            history.add_event(
                data,
                history.event_payload(
                    kind=f"event_{index}",
                    at=f"2026-05-27T08:{index % 60:02d}:00+00:00",
                    title=f"Event {index}",
                ),
            )

        self.assertEqual(len(data["events"]), history.MAX_EVENTS)
        self.assertEqual(data["events"][0]["kind"], f"event_{history.MAX_EVENTS + 4}")

    def test_status_file_is_json(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            data_file = Path(temp_dir) / "history.json"
            status_file = Path(temp_dir) / "status.json"
            data = history.initial_data()
            history.write_json(data_file, data)
            status = history.mark_status(data, status_file)

            self.assertEqual(json.loads(status_file.read_text(encoding="utf-8")), status)
            self.assertEqual(status["event_count"], 0)

    def test_purge_flo_derived_memory(self):
        data = history.initial_data()
        data["active_session"] = {"session_id": "s1"}
        data["active_zones"] = {"Zone 1": {"zone": "Zone 1"}}
        data["sessions"] = [{"session_id": "s1", "gallons": 40}]
        data["zone_runs"] = [{"zone": "Zone 1", "avg_flow": 4.2}]
        data["events"] = [
            history.event_payload(
                kind="zone_finished",
                at="2026-06-09T10:00:00+00:00",
                title="Zone 1 finished",
                note="Zone 1 used 40 gallons at 4 gpm.",
            ),
            history.event_payload(
                kind="alert_irrigation_clog_possible",
                at="2026-06-09T10:05:00+00:00",
                title="Possible clogged irrigation zone",
                note="Fingerprint reason: low_flow_low_gallons_small_pressure_drop.",
            ),
            history.event_payload(
                kind="alert_irrigation_zone_ran_too_long",
                at="2026-06-09T10:10:00+00:00",
                title="Irrigation zone ran too long",
                note="Zone 4 ran for 48 minutes. Flow is 5 gpm.",
            ),
            history.event_payload(
                kind="weather_skip_likely",
                at="2026-06-09T10:15:00+00:00",
                title="Weather skip likely",
                note="Hydrawise advanced past the scheduled cycle.",
            ),
            history.event_payload(
                kind="session_started",
                at="2026-06-09T10:20:00+00:00",
                title="Sprinklers started",
                note="Zone 2 started. Shared well pressure is 52 psi.",
            ),
        ]

        history.purge_flo_derived(data)

        self.assertEqual(data["active_session"], {})
        self.assertEqual(data["active_zones"], {})
        self.assertEqual(data["sessions"], [])
        self.assertEqual(data["zone_runs"], [])
        self.assertEqual([event["kind"] for event in data["events"]], [
            "alert_irrigation_zone_ran_too_long",
            "weather_skip_likely",
            "session_started",
        ])
        self.assertEqual(data["events"][0]["note"], "Zone 4 ran for 48 minutes.")
        self.assertNotIn("gpm", data["events"][0]["note"])

    def test_purge_flo_derived_preserves_hunter_history(self):
        data = history.initial_data()
        data["active_session"] = {"session_id": "s2", "flow_source": "hunter"}
        data["active_zones"] = {"Zone 2": {"zone": "Zone 2", "flow_source": "hunter"}}
        data["sessions"] = [
            {"session_id": "s2", "gallons": 55, "flow_source": "hunter"},
            {"session_id": "old", "gallons": 40},
        ]
        data["zone_runs"] = [
            {"zone": "Zone 2", "avg_flow": 5.5, "flow_source": "hunter"},
            {"zone": "Zone 1", "avg_flow": 4.2},
        ]
        data["events"] = [
            history.event_payload(
                kind="zone_finished",
                at="2026-06-29T10:00:00+00:00",
                title="Zone 2 finished",
                note="Hunter flow baseline run used 55 gallons at 5.5 gpm.",
                flow_source="hunter",
            ),
            history.event_payload(
                kind="zone_finished",
                at="2026-06-09T10:00:00+00:00",
                title="Zone 1 finished",
                note="Zone 1 used 40 gallons at 4 gpm.",
            ),
        ]

        history.purge_flo_derived(data)

        self.assertEqual(data["active_session"]["session_id"], "s2")
        self.assertEqual(list(data["active_zones"]), ["Zone 2"])
        self.assertEqual([session["session_id"] for session in data["sessions"]], ["s2"])
        self.assertEqual([run["zone"] for run in data["zone_runs"]], ["Zone 2"])
        self.assertEqual([event["title"] for event in data["events"]], ["Zone 2 finished"])


if __name__ == "__main__":
    unittest.main()
