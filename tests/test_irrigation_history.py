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
                "--min-pressure",
                "46",
                "--max-flow",
                "5.8",
                "--current-pressure",
                "50",
            )
            self.assertEqual(status["session_count"], 1)
            self.assertEqual(status["latest_session"]["runtime_minutes"], 12)
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


if __name__ == "__main__":
    unittest.main()
