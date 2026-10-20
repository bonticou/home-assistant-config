"""Exercise the actual automation YAML with fake states and notification dispatch."""
import json
import unittest
from datetime import datetime, timezone
from pathlib import Path
import yaml
from jinja2.nativetypes import NativeEnvironment

AUTOMATION = yaml.safe_load((Path(__file__).parents[1] / 'automations/35-generator-notifications.yaml').read_text())[0]
PREFIX = 'generac_generator_generac_5053300_'

class Harness:
    def __init__(self):
        self.states = {}
        self.messages = []
        self.fail_send = False
        self.t = 1800000000
        self.hour = 12
        self.update()
        self.env = NativeEnvironment()
        self.env.filters['from_json'] = lambda s, default: json.loads(s) if s.startswith('{') else default
        self.env.filters['to_json'] = json.dumps
        self.env.globals.update(states=lambda e: self.states.get(e, 'unknown'),
                                now=lambda: datetime(2026, 10, 20, self.hour, tzinfo=timezone.utc),
                                as_timestamp=lambda value: self.t)

    def update(self, status='Ready', connection='on', warning='off', maintenance='off', text='The generator is ready to run'):
        for domain, name, value in [('sensor','status',status), ('sensor','status_text',text),
                                   ('binary_sensor','is_connected',connection),
                                   ('binary_sensor','show_warning',warning), ('binary_sensor','has_maintenance_alert',maintenance)]:
            self.states[f'{domain}.{PREFIX}{name}'] = value

    def render(self, value, ctx):
        if isinstance(value, str): return self.env.from_string(value).render(**ctx)
        if isinstance(value, dict): return {k:self.render(v,ctx) for k,v in value.items()}
        if isinstance(value, list): return [self.render(v,ctx) for v in value]
        return value

    def run(self, steps, ctx):
        for step in steps:
            if 'variables' in step:
                for k,v in step['variables'].items(): ctx[k] = self.render(v,ctx)
            elif 'repeat' in step:
                for item in step['repeat']['for_each']:
                    self.run(step['repeat']['sequence'], dict(ctx, repeat={'item':item}))
            elif 'if' in step:
                ok = all(self.render(c['value_template'],ctx) for c in step['if'])
                self.run(step.get('then' if ok else 'else',[]),ctx)
            elif step['action'] == 'input_text.set_value':
                eid=self.render(step['target']['entity_id'],ctx);value=self.render(step['data']['value'],ctx)
                self.states[eid]=json.dumps(value) if isinstance(value,dict) else value
                assert len(self.states[eid]) <= 255
            elif step['action'] == 'script.notify_trevor_phone':
                if self.fail_send: raise RuntimeError('dispatch failed')
                self.messages.append(self.render(step['data'],ctx))
            else: raise AssertionError(step)

    def tick(self, seconds=0):
        self.t += seconds
        self.run(AUTOMATION['actions'],{})

class Notifications(unittest.TestCase):
    def test_run_once_restore_and_recovery(self):
        h=Harness();h.update(status='Running');h.tick();h.tick(239);self.assertEqual(h.messages,[])
        h.tick(1);self.assertEqual(len(h.messages),1)
        restored=Harness();restored.states=h.states.copy();restored.t=h.t;restored.tick(600)
        self.assertEqual(restored.messages,[])
        restored.update();restored.tick();restored.tick(240)
        self.assertIn('ready again',restored.messages[0]['title'])
        restored.tick(600);self.assertEqual(len(restored.messages),1)

    def test_exercise_is_quiet(self):
        h=Harness();h.update(status='Exercising');h.tick();h.tick(900);h.update();h.tick();h.tick(300)
        self.assertEqual(h.messages,[])

    def test_monitoring_delay_and_recovery(self):
        h=Harness();h.update(status='unavailable',connection='unavailable');h.tick();h.tick(1799)
        self.assertEqual(h.messages,[]);h.tick(1);self.assertEqual(len(h.messages),1)
        h.tick(600);self.assertEqual(len(h.messages),1)
        h.update();h.tick();h.tick(240);self.assertIn('restored',h.messages[-1]['title'])

    def test_short_disconnect_no_recovery_and_no_last_seen_dependency(self):
        h=Harness();h.update(connection='off');h.tick();h.tick(600);h.update();h.tick();h.tick(240)
        self.assertEqual(h.messages,[])

    def test_attention_combined_and_new_cycle(self):
        h=Harness();h.update(status='Warning',warning='on',maintenance='on',text='Inspect battery');h.tick();h.tick(240)
        self.assertEqual(len(h.messages),1);self.assertIn('Inspect battery',h.messages[0]['message'])
        h.tick(86400);self.assertEqual(len(h.messages),1)
        h.update();h.tick();h.tick(240);h.update(status='Stopped');h.tick();h.tick(240)
        self.assertEqual(len(h.messages),2)

    def test_maintenance_daytime_and_no_invented_task(self):
        h=Harness();h.hour=22;h.update(maintenance='on');h.tick();h.tick(600);self.assertEqual(h.messages,[])
        h.hour=9;h.tick(36000);self.assertEqual(len(h.messages),1)
        self.assertIn("hasn't provided the specific task",h.messages[0]['message'])
        h.tick(86400);self.assertEqual(len(h.messages),1)

    def test_failed_dispatch_retry(self):
        h=Harness();h.update(status='Running');h.tick();h.fail_send=True
        with self.assertRaises(RuntimeError):h.tick(240)
        h.fail_send=False;h.tick(60);self.assertEqual(len(h.messages),1)

    def test_unknown_breaks_confirmation_but_preserves_incident(self):
        h=Harness();h.update(status='Running');h.tick();h.tick(180);h.update(status='unknown');h.tick()
        h.update(status='Running');h.tick(60);h.tick(180);self.assertEqual(h.messages,[])
        h.tick(60);self.assertEqual(len(h.messages),1)
        h.update(status='unknown');h.tick();h.update(status='Running');h.tick();h.tick(300)
        self.assertEqual(len(h.messages),1)

if __name__ == '__main__': unittest.main()
