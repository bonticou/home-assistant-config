from __future__ import annotations

import unittest

from tools import ha_remote_health_probe as probe


class HomeAssistantRemoteHealthProbeTests(unittest.TestCase):
    def test_redacts_remote_url_host(self):
        redacted = probe.redact_url("https://example.ui.nabu.casa/lovelace/home")

        self.assertEqual(redacted, "https://<redacted-host>/lovelace/home")
        self.assertNotIn("example", redacted)
        self.assertNotIn("nabu", redacted)

    def test_detects_nabu_fallback_page(self):
        self.assertTrue(
            probe.detect_nabu_fallback(
                "Unable to connect to Home Assistant. "
                "It is possible that your Home Assistant is not currently connected."
            )
        )
        self.assertFalse(probe.detect_nabu_fallback("<home-assistant></home-assistant>"))

    def test_auth_required_websocket_greeting_classifies_ok(self):
        payload = {
            "dns": {"ok": True},
            "tcp": {"ok": True},
            "tls": {"ok": True},
            "http": {"ok": True, "fallback_detected": False},
            "websocket": {"ok": True, "stage": "auth_required"},
        }

        self.assertEqual(probe.classify_result(payload), "ok")

    def test_nabu_fallback_beats_http_status(self):
        payload = {
            "dns": {"ok": True},
            "tcp": {"ok": True},
            "tls": {"ok": True},
            "http": {"ok": True, "fallback_detected": True},
            "websocket": {"ok": False, "stage": "upgrade"},
        }

        self.assertEqual(probe.classify_result(payload), "remote_fallback")


if __name__ == "__main__":
    unittest.main()
