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

    def test_extracts_startup_resources_from_shell_html(self):
        html = """
        <link rel="modulepreload" href="/frontend_latest/core.abc.js">
        <script>import("/frontend_latest/app.def.js");</script>
        <script>window.customPanelJS="/frontend_latest/custom-panel.ghi.js"</script>
        <script>_ls("/frontend_es5/core.legacy.js", true)</script>
        <script src="/browser_mod.js?2.7.3"></script>
        """

        self.assertEqual(
            probe.extract_startup_resources(html),
            [
                "/frontend_latest/core.abc.js",
                "/browser_mod.js?2.7.3",
                "/frontend_latest/app.def.js",
                "/frontend_es5/core.legacy.js",
                "/frontend_latest/custom-panel.ghi.js",
            ],
        )

    def test_classifies_frontend_resource_failure(self):
        payload = {
            "dns": {"ok": True},
            "tcp": {"ok": True},
            "tls": {"ok": True},
            "http": {"ok": True, "fallback_detected": False},
            "websocket": {"ok": True, "stage": "auth_required"},
            "pages": {
                "/": {
                    "ok": True,
                    "fallback_detected": False,
                    "resource_results": [
                        {"ok": True, "path": "/frontend_latest/core.abc.js"},
                        {"ok": False, "path": "/browser_mod.js?2.7.3"},
                    ],
                }
            },
        }

        self.assertEqual(probe.classify_result(payload), "resource_error")

    def test_dedupes_and_normalizes_compare_paths(self):
        self.assertEqual(
            probe.dedupe_paths(["/", "calm-mobile/home", "/calm-mobile/home", "https://example.test/ha-safe/home?x=1"]),
            ["/", "/calm-mobile/home", "/ha-safe/home?x=1"],
        )

    def test_skips_external_startup_resources(self):
        html = """
        <script src="https://cdn.example.test/external.js"></script>
        <script src="/frontend_latest/core.abc.js"></script>
        """

        self.assertEqual(probe.extract_startup_resources(html), ["/frontend_latest/core.abc.js"])


if __name__ == "__main__":
    unittest.main()
