"""Offline execution of the actual sconce YAML; no HA or bridge commands.

These tests verify policy and payloads, not asynchronous Lutron timing or fades.
"""
import unittest
from pathlib import Path
from types import SimpleNamespace

import yaml
from jinja2.nativetypes import NativeEnvironment

ROOT = Path(__file__).resolve().parents[1]
AUTOMATION = next(a for a in yaml.safe_load(
    (ROOT / 'automations/20-climate-commute.yaml').read_text()
) if a['id'] == 'master_bedroom_sconces_sync')
LEFT = 'light.master_bedroom_sconce_l'
RIGHT = 'light.master_bedroom_sconce_r'
SCENES = ('script.lights_all_off_scene', 'script.lights_bedtime_scene')


def state(value, brightness=None, **attributes):
    attributes['brightness'] = brightness
    return SimpleNamespace(state=value, attributes=attributes)


class Harness:
    def __init__(self, target, active_scene=None):
        self.target = target
        self.active_scene = active_scene
        self.env = NativeEnvironment()
        self.env.globals.update(
            states=lambda entity: self.target.state,
            state_attr=lambda entity, attr: self.target.attributes.get(attr),
            is_state=lambda entity, value: (
                ('on' if entity == self.active_scene else 'off') == value
            ),
        )

    def render(self, value, context):
        if isinstance(value, str):
            result = self.env.from_string(value).render(**context)
            # HA strips rendered output before interpreting a template result.
            if isinstance(result, str):
                result = result.strip()
                if result in ('True', 'False'):
                    return result == 'True'
            return result
        if isinstance(value, dict):
            return {k: self.render(v, context) for k, v in value.items()}
        return value

    def run(self, source, previous, current):
        context = {'trigger': SimpleNamespace(
            entity_id=source, from_state=previous, to_state=current
        )}
        if not all(self.render(c['value_template'], context)
                   for c in AUTOMATION['conditions']):
            return []
        calls = []
        for step in AUTOMATION['actions']:
            if 'variables' in step:
                for key, value in step['variables'].items():
                    context[key] = self.render(value, context)
            elif 'choose' in step:
                for branch in step['choose']:
                    if all(self.render(c['value_template'], context)
                           for c in branch['conditions']):
                        calls.extend(self.render(call, context)
                                     for call in branch['sequence'])
                        break
            else:
                raise AssertionError(f'Unexpected action: {step}')
        return calls


class SconceSyncTests(unittest.TestCase):
    def test_on_off_and_brightness_both_directions(self):
        for source, target in ((LEFT, RIGHT), (RIGHT, LEFT)):
            for before, after, follower, action, brightness in (
                (state('off', 0), state('on', 102), state('off', 0), 'light.turn_on', 102),
                (state('on', 102), state('off', 0), state('on', 102), 'light.turn_off', None),
                (state('on', 102), state('on', 153), state('on', 102), 'light.turn_on', 153),
                (state('on', 153), state('on', 2), state('on', 153), 'light.turn_on', 2),
            ):
                with self.subTest(source=source, action=action, brightness=brightness):
                    data = {'entity_id': target, 'transition': 0}
                    if brightness is not None:
                        data['brightness'] = brightness
                    self.assertEqual(Harness(follower).run(source, before, after),
                                     [{'action': action, 'data': data}])

    def test_equal_targets_do_not_echo(self):
        for source in (LEFT, RIGHT):
            for before, after in ((state('off', 0), state('on', 102)),
                                  (state('on', 102), state('off', 0)),
                                  (state('on', 102), state('on', 153))):
                self.assertEqual(Harness(after).run(source, before, after), [])

    def test_unrelated_attribute_changes_do_not_repair_divergence(self):
        for source in (LEFT, RIGHT):
            self.assertEqual(Harness(state('on', 80)).run(
                source, state('on', 102, friendly_name='Before'),
                state('on', 102, friendly_name='After')), [])

    def test_unknown_unavailable_and_startup_are_ignored(self):
        for source in (LEFT, RIGHT):
            for invalid in (None, state('unknown'), state('unavailable')):
                self.assertEqual(Harness(state('off', 0)).run(
                    source, invalid, state('on', 102)), [])
                self.assertEqual(Harness(state('on', 102)).run(
                    source, state('on', 102), invalid), [])
            for invalid_target in ('unknown', 'unavailable'):
                self.assertEqual(Harness(state(invalid_target)).run(
                    source, state('off', 0), state('on', 102)), [])

    def test_both_coordinated_scenes_suppress_on_off_and_dimming(self):
        for scene in SCENES:
            for source in (LEFT, RIGHT):
                for before, after in ((state('off', 0), state('on', 102)),
                                      (state('on', 102), state('off', 0)),
                                      (state('on', 102), state('on', 153))):
                    self.assertEqual(Harness(before, scene).run(source, before, after), [])

    def test_retains_brightness_fallback_and_off_semantics(self):
        self.assertEqual(Harness(state('off')).run(LEFT, state('off'), state('on')),
                         [{'action': 'light.turn_on', 'data': {
                             'entity_id': RIGHT, 'brightness': 255, 'transition': 0}}])
        self.assertEqual(Harness(state('off', 90)).run(
            LEFT, state('off', 50), state('off', 60)), [])

    def test_structure_has_no_added_delay_or_cooldown(self):
        self.assertEqual(AUTOMATION['mode'], 'restart')
        self.assertEqual(AUTOMATION['triggers'], [
            {'trigger': 'state', 'entity_id': [LEFT, RIGHT]}])
        self.assertEqual(len(AUTOMATION['actions']), 2)
        self.assertEqual(set(AUTOMATION['actions'][0]), {'variables'})
        self.assertEqual(set(AUTOMATION['actions'][1]), {'choose'})
        scripts = yaml.safe_load((ROOT / 'scripts.yaml').read_text())
        for scene in SCENES:
            self.assertIn(scene.removeprefix('script.'), scripts)


if __name__ == '__main__':
    unittest.main()
