"""Scoped configuration tests; no commands to HA or physical lights."""
import unittest
from pathlib import Path
from types import SimpleNamespace

import yaml
from jinja2.nativetypes import NativeEnvironment

ROOT = Path(__file__).resolve().parents[1]
LANTERN = 'light.master_bedroom_lantern'


class ConfigLoader(yaml.SafeLoader):
    pass


ConfigLoader.add_multi_constructor('!', lambda loader, tag, node: None)


def load(path):
    return yaml.load((ROOT / path).read_text(), Loader=ConfigLoader)


def nodes(value):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from nodes(child)
    elif isinstance(value, list):
        for child in value:
            yield from nodes(child)


def calls(script, entity):
    return [n for n in nodes(script) if 'action' in n and entity in
            (lambda ids: ids if isinstance(ids, list) else [ids])(
                n.get('target', {}).get('entity_id', n.get('data', {}).get('entity_id')))]


class MasterLanternTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.scripts = load('scripts.yaml')
        cls.config = load('configuration.yaml')

    def test_bedtime_one_smooth_five_second_ramp_to_40(self):
        actions = calls(self.scripts['lights_bedtime_scene'], LANTERN)
        self.assertEqual(actions, [{'action': 'light.turn_on',
            'target': {'entity_id': LANTERN},
            'data': {'brightness_pct': 40, 'transition': 5}}])

    def test_sleep_and_vacation_cleanup(self):
        for key in ('lights_all_off_scene', 'vacation_mode_start'):
            with self.subTest(script=key):
                action, = calls(self.scripts[key], LANTERN)
                self.assertEqual(action['action'], 'light.turn_off')
                self.assertEqual(action['data']['transition'], 3)

    def test_other_scenes_and_sconce_pair_do_not_gain_lantern(self):
        for key, script in self.scripts.items():
            if key not in ('lights_all_off_scene', 'lights_bedtime_scene', 'vacation_mode_start'):
                self.assertEqual(calls(script, LANTERN), [], key)
        self.assertNotIn(LANTERN, (ROOT / 'lights.yaml').read_text())
        self.assertNotIn(LANTERN, (ROOT / 'automations/20-climate-commute.yaml').read_text())

    def test_one_independent_dashboard_control(self):
        cards = [n for n in nodes(load('dashboards/calm_mobile.yaml'))
                 if n.get('entity') == LANTERN]
        self.assertEqual(len(cards), 1)
        self.assertEqual(cards[0]['name'], 'Lantern')
        self.assertTrue(cards[0]['show_brightness_control'])
        self.assertEqual(cards[0]['tap_action']['data']['light_entity'], LANTERN)

    def test_generic_away_and_overnight_enumeration(self):
        light = SimpleNamespace(entity_id=LANTERN, state='on', name='Master Bedroom Lantern', attributes={})
        env = NativeEnvironment()
        env.globals.update(states=SimpleNamespace(light=[light]), is_state=lambda *args: False,
                           state_attr=lambda *args: None)
        # states is callable for the vacation-window checks as well as iterable by domain.
        class States:
            def __init__(self): self.light = [light]
            def __call__(self, entity): return 'off'
        env.globals['states'] = States()
        for key in ('away_security_active_lights', 'overnight_lights_left_on'):
            sensor = next(n for n in nodes(self.config) if n.get('unique_id') == key)
            self.assertEqual(int(str(env.from_string(sensor['state']).render()).strip()), 1)
            self.assertEqual(env.from_string(sensor['attributes']['entity_ids']).render().strip(), LANTERN)
            self.assertEqual(env.from_string(sensor['attributes']['names']).render().strip(), 'Master Bedroom Lantern')

    def test_existing_door_lantern_unchanged(self):
        for key, action in (('door_lights_schedule_on', 'switch.turn_on'),
                            ('door_lights_schedule_off', 'switch.turn_off')):
            call, = calls(self.scripts[key], 'switch.master_lantern')
            self.assertEqual(call['action'], action)
            self.assertEqual(call['data']['entity_id'], ['switch.master_lantern', 'switch.front_foyer_sconces'])


if __name__ == '__main__':
    unittest.main()
