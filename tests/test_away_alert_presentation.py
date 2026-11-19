"""Routine notices omit diagnostics; explicit failed actions remain truthful."""
from pathlib import Path
import unittest
import yaml
from jinja2 import Environment, StrictUndefined

ROOT = Path(__file__).resolve().parents[1]


def notifications(value):
    if isinstance(value, dict):
        if value.get('action') == 'script.notify_trevor_phone':
            yield value['data']
        for child in value.values():
            yield from notifications(child)
    elif isinstance(value, list):
        for child in value:
            yield from notifications(child)


class AwayPresentationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.scripts = yaml.safe_load((ROOT/'scripts.yaml').read_text())
        cls.env = Environment(undefined=StrictUndefined)

    def render(self, text, **values):
        return ' '.join(self.env.from_string(text).render(**values).split())

    def test_all_routine_variants_ignore_unavailable_diagnostics(self):
        for missing in [None, [], ['Flower Lamp','Master door lantern','Uplight 1']]:
            context = dict(notification_message='Casey and Trevor are away, and 2 entry points unsecured · 3 lights on.',
                           active_light_names=['Kitchen','Foyer','Upstairs hallway'],
                           casey_departure_entry_message_clause='2 entry points unsecured',
                           state_attr=lambda *_: missing)
            count = 0
            for key in ['away_security_send_alert','casey_left_combo_send_alert','casey_left_lights_send_alert']:
                for notice in notifications(self.scripts[key]):
                    message = self.render(notice['message'], **context)
                    self.assertIn('3 lights', message)
                    for forbidden in ['check:', 'Flower Lamp', 'Master door lantern', 'Uplight 1', 'all off', 'everything is off']:
                        self.assertNotIn(forbidden, message)
                    self.assertTrue(notice['data']['actions'])
                    count += 1
            self.assertEqual(count,10)

    def test_confirmed_single_pair_and_multiple_light_counts(self):
        for key in ['casey_left_combo_send_alert','casey_left_lights_send_alert']:
            notice = next(notifications(self.scripts[key]))
            for names, expected in [(['Kitchen'],'Kitchen is still on'),
                                    (['Kitchen','Foyer'],'Kitchen and Foyer are still on'),
                                    (['Kitchen','Foyer','Hallway'],'3 lights are still on')]:
                message = self.render(notice['message'], active_light_names=names,
                                      casey_departure_entry_message_clause='2 entry points unsecured')
                self.assertIn(expected,message)
                if key=='casey_left_combo_send_alert':
                    self.assertIn('2 entry points unsecured',message)

    def test_explicit_incomplete_action_keeps_exact_failure_information(self):
        notices=list(notifications(self.scripts['away_lights_report_result']))
        template=next(n['message'] for n in notices if n['message']!='clear_notification')
        result=dict(inventory_ready=True,remaining=['light.foyer'],unavailable=['switch.flower_lamp'],
                    targets={'light.foyer':'Foyer','switch.flower_lamp':'Flower Lamp'})
        message=self.render(template,result=result)
        self.assertIn('Still on after two attempts: Foyer.',message)
        self.assertIn("Couldn't verify: Flower Lamp.",message)
        self.assertNotIn('all lights are off',message.lower())
        message=self.render(template,result=dict(inventory_ready=False))
        self.assertIn("haven't confirmed the lights are off",message)


if __name__=='__main__':
    unittest.main()
