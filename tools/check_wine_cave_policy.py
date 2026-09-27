#!/usr/bin/env python3
"""Render the configured Wine Cave templates at storage-policy boundaries.

Requires PyYAML and Jinja2. Run from the repo with an interpreter that has them:
    python3 tools/check_wine_cave_policy.py
This checks template semantics and configured delays, not HA timer execution.
"""

import argparse
import math
from pathlib import Path
import unittest

import jinja2
import yaml


class HomeAssistantLoader(yaml.SafeLoader):
    """Preserve !include and !secret values without opening external files."""


def tagged_value(loader, tag, node):
    if isinstance(node, yaml.ScalarNode):
        return loader.construct_scalar(node)
    if isinstance(node, yaml.SequenceNode):
        return loader.construct_sequence(node)
    return loader.construct_mapping(node)


HomeAssistantLoader.add_multi_constructor("!", tagged_value)


def is_number(value):
    try:
        return math.isfinite(float(value))
    except (TypeError, ValueError):
        return False


class WinePolicyTests(unittest.TestCase):
    config_path = Path(__file__).resolve().parents[1] / "configuration.yaml"

    @classmethod
    def setUpClass(cls):
        config = yaml.load(cls.config_path.read_text(), Loader=HomeAssistantLoader)
        cls.templates = {
            entity["unique_id"]: entity
            for block in config["template"]
            for domain in ("sensor", "binary_sensor")
            for entity in block.get(domain, [])
            if entity.get("unique_id", "").startswith("wine_cave_")
        }
        cls.environment = jinja2.Environment(undefined=jinja2.StrictUndefined)

    def readings(self, temperature=55, humidity=65, **flags):
        values = {
            "sensor.wine_temperature": str(temperature),
            "sensor.wine_humidity": str(humidity),
            "sensor.wine_cave_absolute_humidity_24h_delta": "1",
            "sensor.wine_cave_dew_point_margin": "4",
        }
        for flag in (
            "sensor_unavailable", "cooling_cycle", "drift_alert",
            "temp_high_alert", "temp_low_alert", "moisture_anomaly",
            "condensation_risk", "actionable_alert",
        ):
            values[f"binary_sensor.wine_cave_{flag}"] = flags.get(flag, "off")
        values["binary_sensor.wine_cave_actionable_alert"] = (
            "on" if self.boolean("actionable_alert", values) else "off"
        )
        return values

    def render(self, source, values):
        return self.environment.from_string(source).render(
            states=lambda entity: values.get(entity, "unknown"),
            is_state=lambda entity, expected: values.get(entity, "unknown") == expected,
            is_number=is_number,
        ).strip()

    def boolean(self, suffix, values, field="state"):
        actual = self.render(self.templates[f"wine_cave_{suffix}"][field], values)
        self.assertIn(actual.lower(), ("true", "false"))
        return actual.lower() == "true"

    def assert_status(self, values, expected_state, expected_label, expected_icon):
        status = self.templates["wine_cave_status"]
        self.assertEqual(self.render(status["state"], values), expected_state)
        self.assertEqual(self.render(status["attributes"]["display_label"], values), expected_label)
        self.assertEqual(self.render(status["icon"], values), expected_icon)

    def test_preferred_storage_band_is_inclusive(self):
        for temperature in (53, 55, 57):
            for humidity in (55, 66, 70):
                with self.subTest(temperature=temperature, humidity=humidity):
                    self.assert_status(self.readings(temperature, humidity), "Optimal", "Healthy", "mdi:check-circle")
        self.assert_status(self.readings(54.7, 67), "Optimal", "Healthy", "mdi:check-circle")

    def test_pending_excursions_and_advisory_flags_only_monitor(self):
        cases = [
            self.readings(temperature=50),
            self.readings(temperature=60),
            self.readings(humidity=50),
            self.readings(humidity=80),
            self.readings(humidity=72),
            self.readings(humidity=75),
            self.readings(humidity=76),
            self.readings(temperature=61),
            self.readings(humidity=49),
            self.readings(humidity=45, cooling_cycle="on"),
            self.readings(cooling_cycle="on"),  # Recovery hysteresis.
            self.readings(drift_alert="on"),
        ]
        for values in cases:
            with self.subTest(values=values):
                self.assert_status(values, "Warning", "Monitoring", "mdi:chart-line")

    def test_sustained_alert_stays_critical_during_recovery(self):
        for flag in ("temp_high_alert", "temp_low_alert", "moisture_anomaly", "condensation_risk"):
            with self.subTest(flag=flag):
                self.assert_status(self.readings(55, 65, **{flag: "on"}), "Critical", "Needs attention", "mdi:alert-circle-outline")

    def test_unavailable_and_missing_readings_take_priority(self):
        for temperature in (55, "unknown"):
            self.assert_status(self.readings(temperature, sensor_unavailable="on", temp_high_alert="on"), "Unavailable", "Sensor unavailable", "mdi:wifi-alert")
        for entity in ("sensor.wine_temperature", "sensor.wine_humidity"):
            values = self.readings(temp_high_alert="on")
            values.pop(entity)
            with self.subTest(missing=entity):
                self.assert_status(values, "Unknown", "Waiting for readings", "mdi:clock-outline")

    def test_preferred_humidity_does_not_create_moisture_or_condensation_alerts(self):
        # Neither a large AH change nor a narrow air/dew-point gap turns
        # preferred humidity into an actionable moisture condition.
        for humidity in (55, 66, 70):
            for alert in ("moisture_anomaly", "condensation_risk"):
                with self.subTest(humidity=humidity, alert=alert):
                    self.assertFalse(self.boolean(alert, self.readings(humidity=humidity)))

    def test_steady_high_humidity_needs_attention_without_derived_readings(self):
        self.assertFalse(self.boolean("moisture_anomaly", self.readings(humidity=75)))
        values = self.readings(humidity=76)
        values["sensor.wine_cave_absolute_humidity_24h_delta"] = "0"
        self.assertTrue(self.boolean("moisture_anomaly", values))
        # A missing trend baseline or dew-point estimate must not suppress a
        # sustained high-humidity alert when both raw readings are present.
        values.pop("sensor.wine_cave_absolute_humidity_24h_delta")
        values.pop("sensor.wine_cave_dew_point_margin")
        self.assertTrue(self.boolean("moisture_anomaly", values, "availability"))
        self.assertTrue(self.boolean("moisture_anomaly", values))
        self.assertEqual(self.templates["wine_cave_moisture_anomaly"]["delay_on"], {"minutes": 15})

    def test_condensation_requires_high_humidity_and_a_narrow_gap(self):
        self.assertFalse(self.boolean("condensation_risk", self.readings(humidity=75)))
        values = self.readings(humidity=76)
        self.assertTrue(self.boolean("condensation_risk", values))
        values["sensor.wine_cave_dew_point_margin"] = "8"
        self.assertFalse(self.boolean("condensation_risk", values))
        self.assertEqual(self.templates["wine_cave_condensation_risk"]["delay_on"], {"minutes": 10})

    def test_cycle_settled_uses_recovery_band_not_preferred_band(self):
        self.assertTrue(self.boolean("cycle_settled", self.readings(55, 75)))
        self.assertFalse(self.boolean("cycle_settled", self.readings(55, 76)))

    def test_dry_cycle_and_abnormally_dry_conditions_remain_distinct(self):
        self.assertFalse(self.boolean("moisture_anomaly", self.readings(55, 45)))
        self.assertTrue(self.boolean("moisture_anomaly", self.readings(55, 41)))
        self.assertTrue(self.boolean("moisture_anomaly", self.readings(61, 49)))

    def test_temperature_protection_boundaries_and_delays_are_preserved(self):
        for suffix, outside, boundary in (("temp_high_alert", 60.1, 60), ("temp_low_alert", 49.9, 50)):
            with self.subTest(alert=suffix):
                self.assertTrue(self.boolean(suffix, self.readings(temperature=outside)))
                self.assertFalse(self.boolean(suffix, self.readings(temperature=boundary)))
                self.assertFalse(self.boolean(suffix, self.readings(temperature="unavailable"), "availability"))
                template = self.templates[f"wine_cave_{suffix}"]
                self.assertEqual(template["delay_on"], {"minutes": 15})
                self.assertEqual(template["delay_off"], {"minutes": 10})


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=WinePolicyTests.config_path)
    args = parser.parse_args()
    WinePolicyTests.config_path = args.config
    unittest.main(argv=[__file__], verbosity=2)
