"""Render production templates and simulate the explicit action without HA calls."""
import copy
import ast
import json
from pathlib import Path
from types import SimpleNamespace
import unittest
from datetime import datetime

import yaml
from jinja2 import StrictUndefined
from jinja2.nativetypes import NativeEnvironment

ROOT = Path(__file__).resolve().parents[1]


class States:
    def __init__(self, values, lights=()):
        self.values = values
        self.light = list(lights)

    def __call__(self, entity):
        return self.values.get(entity, 'unknown')


class CoverageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sensors = yaml.safe_load((ROOT/'helpers/household_lighting.yaml').read_text())['sensor']
        cls.scripts = yaml.safe_load((ROOT/'scripts.yaml').read_text())
        cls.action = cls.scripts['away_lights_turn_off_verified']
        cls.rules = yaml.safe_load((ROOT/'automations/10-lighting-security.yaml').read_text())

    def context(self, values=None, lights=(), lutron=()):
        values = values or {}
        states = States(values, lights)
        env = NativeEnvironment(undefined=StrictUndefined)
        context = dict(states=states, is_state=lambda e, s: states(e) == s,
                       integration_entities=lambda _: list(lutron), now=lambda: datetime(2026, 11, 18, 18))
        def render(template, extra=None):
            value = env.from_string(template).render(**(context | (extra or {})))
            if isinstance(value, str):
                value = value.strip()
                try:
                    return ast.literal_eval(value)
                except (ValueError, SyntaxError):
                    pass
            return value
        targets = render(self.sensors[0]['attributes']['targets'])
        context['state_attr'] = lambda e, a: targets if (e, a) == ('sensor.household_lighting_inventory', 'targets') else None
        return states, context, render, targets

    def test_complete_verified_physical_inventory(self):
        _, _, _, targets = self.context()
        records = json.loads((ROOT/'docs/device-inventory.json').read_text())
        physical = {e['entity_id'] for e in records['entities'] if e['domain'] == 'light'
                    and e.get('platform') != 'group' and e.get('entity_category') != 'config'
                    and not e.get('disabled_by')}
        self.assertTrue(physical <= targets.keys())
        expected_switches = {'switch.exterior_mud_room_stairs', 'switch.family_room_uplight',
                            'switch.flower_lamp', 'switch.front_foyer_sconces', 'switch.garage_garage_lights',
                            'switch.master_lantern', 'switch.office_uplights', 'switch.uplight', 'switch.uplight_2'}
        self.assertEqual(set(targets)-physical, expected_switches)
        self.assertEqual(len(targets), 42)
        for alias in ['light.interior_test', 'light.wynn_s_room', 'switch.great_room_uplights',
                      'light.u7_pro_family_room_led', 'switch.dehumidifier', 'switch.flo_shutoff']:
            self.assertNotIn(alias, targets)

    def test_new_lutron_load_is_shared_but_arbitrary_switch_and_group_are_not(self):
        new = SimpleNamespace(entity_id='light.new_room_dimmer', name='New room', attributes={})
        group = SimpleNamespace(entity_id='light.new_group', name='Group', attributes={'entity_id': ['light.new_room_dimmer']})
        led = SimpleNamespace(entity_id='light.network_led', name='LED', attributes={})
        values = {'light.new_room_dimmer':'on', 'switch.new_random_plug':'on'}
        _, _, render, targets = self.context(values, [new, group, led], [new.entity_id, group.entity_id])
        self.assertIn(new.entity_id, targets)
        self.assertNotIn(group.entity_id, targets)
        self.assertNotIn(led.entity_id, targets)
        self.assertEqual(render(self.sensors[1]['state']), 1)
        self.assertEqual(render(self.sensors[1]['attributes']['entity_ids']), new.entity_id)

    def test_unknown_and_unavailable_are_not_off_or_dropped(self):
        _, _, _, targets = self.context()
        values = {e:'off' for e in targets}
        values.update({'switch.flower_lamp':'unavailable', 'switch.master_lantern':'unknown',
                       'light.front_foyer_chandelier':'on', 'light.stairs_front_stairs':'on',
                       'light.wynn_s_room_chandelier':'on'})
        _, _, render, _ = self.context(values)
        self.assertEqual(render(self.sensors[1]['state']), 3)
        self.assertEqual(set(render(self.sensors[1]['attributes']['unavailable_entity_ids'])),
                         {'switch.flower_lamp','switch.master_lantern'})

    def simulate(self, values, fail=(), after_delay=None, inventory_missing=False):
        states, context, render, targets = self.context(values)
        values['sensor.household_lighting_inventory'] = 'ready'
        if inventory_missing:
            context['state_attr'] = lambda *_: None
            values['sensor.household_lighting_inventory'] = 'unavailable'
        calls = []
        delays = []
        scope = {}
        def walk(sequence):
            for step in sequence:
                if 'variables' in step:
                    for k, v in step['variables'].items():
                        scope[k] = render(v, scope) if isinstance(v, str) else v
                elif 'if' in step:
                    if all(render(c['value_template'], scope) for c in step['if']):
                        walk(step['then'])
                elif 'repeat' in step:
                    repeat = step['repeat']
                    items = render(repeat['for_each'], scope) if 'for_each' in repeat else range(repeat['count'])
                    saved = scope.get('repeat')
                    for item in items:
                        scope['repeat'] = SimpleNamespace(item=item)
                        walk(repeat['sequence'])
                    scope['repeat'] = saved
                elif 'action' in step:
                    self.assertEqual(step['action'], 'homeassistant.turn_off')
                    entity = render(step['target']['entity_id'], scope)
                    calls.append(entity)
                    if entity in fail:
                        self.assertTrue(step['continue_on_error'])
                    else:
                        values[entity] = 'off'
                elif 'delay' in step:
                    delays.append(step['delay']['seconds'])
                    if after_delay:
                        after_delay(len(delays), values)
                elif 'stop' in step:
                    self.assertEqual(step['response_variable'], 'result')
                else:
                    self.fail(f'Unsupported action in simulation: {step}')
        walk(self.action['sequence'])
        return scope['result'], calls, delays

    def test_failure_isolation_retry_and_truthful_partial_result(self):
        _, _, _, targets = self.context()
        values = {e:'off' for e in targets}
        first, second = 'light.front_foyer_ceiling_lights', 'light.upstairs_hallway_main_lights'
        values.update({first:'on', second:'on', 'switch.flower_lamp':'unavailable'})
        result, calls, delays = self.simulate(values, fail=[first])
        self.assertEqual(calls.count(first), 2)
        self.assertEqual(calls.count(second), 1)
        self.assertEqual(delays, [3,3])
        self.assertFalse(result['complete'])
        self.assertEqual(result['remaining'], [first])
        self.assertEqual(result['unavailable'], ['switch.flower_lamp'])

    def test_relight_is_retried_and_late_relight_remains_visible(self):
        _, _, _, targets = self.context()
        for when, expected_calls, complete in [(1,2,True),(2,1,False)]:
            values = {e:'off' for e in targets}; target = 'light.stairs_front_stairs'; values[target]='on'
            result, calls, _ = self.simulate(values, after_delay=lambda n,v: v.update({target:'on'}) if n==when else None)
            self.assertEqual(calls.count(target), expected_calls)
            self.assertEqual(result['complete'], complete)

    def test_missing_inventory_fails_closed_without_false_success(self):
        result, calls, delays = self.simulate({}, inventory_missing=True)
        self.assertFalse(result['complete'])
        self.assertFalse(result['inventory_ready'])
        self.assertEqual(calls, [])

    def test_both_notification_branches_use_same_verified_action(self):
        rule = next(r for r in self.rules if r['id']=='away_security_notification_actions')
        for index in [0,3]:
            sequence=rule['actions'][0]['choose'][index]['sequence']
            call=next(a for a in sequence if a.get('action')=='script.away_lights_turn_off_verified')
            self.assertEqual(call['response_variable'],'lighting_result')
            self.assertEqual(sequence[-1]['action'],'script.away_lights_report_result')
            self.assertNotIn('homeassistant.turn_off',str(sequence))
        self.assertNotIn('input_boolean',str(self.action))
        self.assertNotIn('input_select',str(self.action))
        self.assertNotIn('notify',str(self.action))


if __name__ == '__main__':
    unittest.main()
