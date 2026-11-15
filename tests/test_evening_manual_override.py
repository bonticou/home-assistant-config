"""Evening scheduler respects manual changes; explicit scene buttons still reset."""
import unittest
from pathlib import Path
from types import SimpleNamespace

import yaml
from jinja2 import Environment, StrictUndefined

ROOT = Path(__file__).resolve().parents[1]


class EveningManualOverrideTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rule = next(a for a in yaml.safe_load((ROOT / 'automations/10-lighting-security.yaml').read_text())
                        if a['id'] == 'interior_evening_mode_schedule_sync')
        cls.env = Environment(undefined=StrictUndefined)

    def eligible(self, trigger, scene, last_run):
        # Deliberately provide no light states: eligibility must not depend on them.
        def states(entity):
            self.assertEqual(entity, 'input_select.lighting_active_scene')
            return scene
        return self.env.from_string(self.rule['conditions'][-1]['value_template']).render(
            states=states, trigger=SimpleNamespace(id=trigger),
            state_attr=lambda *args: last_run,
            as_timestamp=lambda value, default=0: value if value is not None else default,
            today_at=lambda time: 1200).strip().lower() == 'true'

    def test_current_evening_not_repaired_without_arrival(self):
        for trigger in ['refresh', 'startup', 'automation_reloaded', 'dusk']:
            for last_run in [1200, 1201, 2000]:
                with self.subTest(trigger=trigger, last_run=last_run):
                    self.assertFalse(self.eligible(trigger, 'Evening', last_run))

    def test_arrival_reapplies_current_evening(self):
        # Arrival authenticity and first-person filtering remain a separate gate.
        for last_run in [1200, 1201, 2000]:
            self.assertTrue(self.eligible('arrival', 'Evening', last_run))

    def test_initial_and_stale_day_catchup(self):
        for trigger in ['refresh', 'startup', 'automation_reloaded', 'dusk', 'arrival']:
            for scene, last_run in [('None', None), ('Evening', None), ('Evening', 1199)]:
                with self.subTest(trigger=trigger, scene=scene, last_run=last_run):
                    self.assertTrue(self.eligible(trigger, scene, last_run))

    def test_tv_bedtime_and_all_off(self):
        for trigger in ['refresh', 'startup', 'automation_reloaded', 'dusk', 'arrival']:
            for scene in ['TV', 'Bedtime']:
                self.assertFalse(self.eligible(trigger, scene, 1199))
        for trigger in ['refresh', 'startup', 'automation_reloaded']:
            self.assertFalse(self.eligible(trigger, 'All off', 1199))
        # Preserve existing explicit dusk/arrival behavior for All off.
        for trigger in ['dusk', 'arrival']:
            self.assertTrue(self.eligible(trigger, 'All off', 1199))

    def test_genuine_arrival_guard(self):
        template = self.env.from_string(self.rule['conditions'][-2]['value_template'])
        for origin, other, expected in [('not_home', 'not_home', True), ('Work', 'not_home', True),
                                        ('unknown', 'not_home', False), ('unavailable', 'not_home', False),
                                        ('home', 'not_home', False), ('not_home', 'home', False)]:
            for person in ['person.bonticou', 'person.casey']:
                result = template.render(trigger=SimpleNamespace(id='arrival', entity_id=person,
                                         from_state=SimpleNamespace(state=origin)), states=lambda _: other)
                self.assertEqual(result.strip().lower() == 'true', expected)
        result = template.render(trigger=SimpleNamespace(id='arrival', entity_id='person.bonticou',
                                 from_state=None), states=lambda _: 'not_home')
        self.assertEqual(result.strip().lower(), 'false')

    def test_hold_exception_only_for_all_off_arrival(self):
        template = self.env.from_string(self.rule['conditions'][1]['value_template'])
        for trigger in ['arrival', 'refresh', 'startup', 'automation_reloaded', 'dusk']:
            for scene in ['All off', 'Evening', 'None', 'TV', 'Bedtime']:
                for hold in ['on', 'off', 'unknown', 'unavailable']:
                    states = {'input_boolean.tv_lighting_scene_hold': hold,
                              'input_select.lighting_active_scene': scene}
                    result = template.render(trigger=SimpleNamespace(id=trigger),
                                             is_state=lambda entity, state: states[entity] == state)
                    expected = hold == 'off' or (trigger == 'arrival' and scene == 'All off')
                    self.assertEqual(result.strip().lower() == 'true', expected)
        # Authenticity/first-person and TV/Bedtime guards remain separate gates.
        self.assertIn("not in ['TV', 'Bedtime']", self.rule['conditions'][0]['value_template'])
        self.assertIn("states(other_person) != 'home'", self.rule['conditions'][-2]['value_template'])

    def test_explicit_evening_is_not_scene_change_dependent(self):
        script = yaml.safe_load((ROOT / 'scripts.yaml').read_text())['lights_evening_scene']
        self.assertEqual(script['mode'], 'restart')
        self.assertEqual(script['sequence'][0]['action'], 'input_select.select_option')
        self.assertEqual(script['sequence'][0]['data']['option'], 'Evening')
        self.assertTrue(any('light.family_room_main_lights_1' in str(step)
                            for step in script['sequence']))
        dashboard = yaml.safe_load((ROOT / 'dashboards/calm_mobile.yaml').read_text())
        buttons = []
        def walk(value):
            if isinstance(value, dict):
                if value.get('name') == 'Evening' and value.get('type') == 'custom:button-card':
                    buttons.append(value)
                for child in value.values():
                    walk(child)
            elif isinstance(value, list):
                for child in value:
                    walk(child)
        walk(dashboard)
        self.assertEqual(len(buttons), 2)
        for button in buttons:
            self.assertEqual(button['tap_action']['service'], 'script.turn_on')
            self.assertEqual(button['tap_action']['service_data']['entity_id'], 'script.lights_evening_scene')


if __name__ == '__main__':
    unittest.main()
