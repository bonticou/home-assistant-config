"""Execute production notification templates/actions; no Home Assistant services."""
import json
import unittest
from datetime import datetime, timezone
from pathlib import Path
from types import SimpleNamespace as NS

import yaml
from jinja2.nativetypes import NativeEnvironment

ROOT = Path(__file__).resolve().parents[1]
RULE = next(a for a in yaml.safe_load((ROOT / 'automations/30-maintenance-environment.yaml').read_text())
            if a['id'] == 'dishwasher_successful_cycle_notification')
LEDGER = 'input_text.dishwasher_notification_cycle'
OP = 'sensor.dishwasher_operation_state'
DONE = 'sensor.dishwasher_program_finished'
CONNECTED = 'binary_sensor.dishwasher_connectivity'


def dt(t):
    return datetime.fromtimestamp(t, timezone.utc)


class States:
    def __init__(self):
        self.data = {LEDGER: 'unknown', OP: 'ready', DONE: 'off', CONNECTED: 'on'}
    def __call__(self, key):
        return self.data.get(key, 'unknown')
    @property
    def input_text(self):
        return NS(**({'dishwasher_notification_cycle': NS(state=self(LEDGER))}
                     if LEDGER in self.data else {'dishwasher_notification_cycle': None}))


class Harness:
    def __init__(self):
        self.states = States()
        self.t = 1800000000
        self.loaded = self.t - 100
        self.messages = []
        self.fail = None
        self.env = NativeEnvironment()
        def from_json(value, default):
            try: return json.loads(value)
            except (ValueError, TypeError): return default
        def timestamp(value, default=0):
            return value.timestamp() if isinstance(value, datetime) else default
        self.env.filters.update(from_json=from_json, to_json=json.dumps)
        self.env.globals.update(states=self.states, is_state=lambda k, v: self.states(k) == v,
                                as_timestamp=timestamp, now=lambda: dt(self.t))

    def render(self, value, ctx):
        if isinstance(value, str):
            result = self.env.from_string(value).render(**ctx)
            if isinstance(result, str) and result.strip() in ('True', 'False'):
                return result.strip() == 'True'
            return result
        if isinstance(value, dict): return {k: self.render(v, ctx) for k, v in value.items()}
        return value

    def run(self, steps, ctx):
        for step in steps:
            if 'condition' in step:
                if not self.render(step['value_template'], ctx): return
            elif 'variables' in step:
                for k, value in step['variables'].items(): ctx[k] = self.render(value, ctx)
            elif 'choose' in step:
                for branch in step['choose']:
                    if self.render(branch['conditions'], ctx):
                        self.run(branch['sequence'], ctx)
                        break
            elif step['action'] == 'input_text.set_value':
                value = self.render(step['data']['value'], ctx)
                if isinstance(value, str): value = json.loads(value)
                if self.fail == 'before_claim' and value.get('claimed') == value['cycle'] > 0:
                    raise RuntimeError('claim write failed')
                if self.fail == 'success_stamp' and value.get('sent', 0) == value['cycle'] > 0:
                    raise RuntimeError('success stamp failed')
                if self.fail == 'claim_ignored' and value.get('claimed') == value['cycle'] > 0:
                    continue
                self.states.data[LEDGER] = json.dumps(value)
                assert len(self.states(LEDGER)) <= 255
            elif step['action'] == 'script.notify_trevor_phone':
                if self.fail == 'before_send': raise RuntimeError('failed before provider')
                self.messages.append(self.render(step['data'], ctx))
                if self.fail == 'after_send': raise RuntimeError('uncertain provider acceptance')
            else: raise AssertionError(step)

    def edge(self, kind, old=None, new=None, seconds=1, event_age=0):
        self.t += seconds
        entity = OP if kind == 'run' else DONE
        if new is not None: self.states.data[entity] = new
        trigger = NS(id=kind, platform='state' if new is not None else 'event',
                     from_state=NS(state=old) if old is not None else None,
                     to_state=NS(state=new, last_changed=dt(self.t-event_age)) if new is not None else None)
        self.run(RULE['actions'], {'trigger': trigger, 'this': NS(last_changed=dt(self.loaded))})

    def start(self): self.edge('run', 'ready', 'run')
    def finish(self):
        self.states.data[OP] = 'finished'
        self.edge('complete', 'off', 'present', seconds=3600)
    def ledger(self): return json.loads(self.states(LEDGER))


class DishwasherNotifications(unittest.TestCase):
    def test_success_and_duplicate_edges(self):
        h=Harness();h.start();h.finish()
        self.assertEqual(len(h.messages),1)
        h.edge('complete','confirmed','present');h.edge('complete','off','present')
        self.assertEqual(len(h.messages),1)
        self.assertEqual(h.ledger()['sent'],h.ledger()['cycle'])
        self.assertEqual(h.messages[0]['data']['push'],{'interruption-level':'passive','sound':'none'})

    def test_run_before_provider_reset_and_reset_cannot_arm_alone(self):
        h=Harness();h.start();h.finish()
        h.start();self.assertFalse(h.ledger()['baseline'])
        h.edge('baseline','present','off');self.assertTrue(h.ledger()['baseline'])
        h.finish();self.assertEqual(len(h.messages),2)
        h=Harness();h.states.data[OP]='run';h.edge('baseline','present','off');h.finish()
        self.assertEqual(h.messages,[])

    def test_next_cycle_and_pause_resume(self):
        h=Harness();h.start();first=h.ledger()['cycle']
        h.edge('run','pause','run');self.assertEqual(h.ledger()['cycle'],first)
        h.finish();h.states.data[DONE]='confirmed';h.start();h.finish()
        self.assertEqual(len(h.messages),2)

    def test_enable_reconnect_and_cached_present(self):
        for old in (None,'unknown','unavailable','present'):
            h=Harness();h.start();h.states.data[OP]='finished'
            h.edge('complete',old,'present');self.assertEqual(h.messages,[])
        h=Harness();h.states.data[DONE]='present';h.start();h.finish()
        self.assertEqual(h.messages,[])

    def test_abort_generic_finished_is_not_completion(self):
        h=Harness();h.start();h.edge('invalidate');h.states.data[OP]='finished'
        self.assertEqual(h.messages,[])
        h.edge('complete','off','present');self.assertEqual(h.messages,[])
        self.assertFalse(any(t.get('to')=='finished' for t in RULE['triggers']))

    def test_restart_reload_disconnect_invalidate(self):
        for reason in ('startup','reload','disconnect'):
            h=Harness();h.start();h.edge('invalidate');h.finish()
            self.assertEqual(h.messages,[],reason)
        h=Harness();h.start();h.loaded=h.t+1;h.finish()
        self.assertEqual(h.messages,[])  # Even a restored cycle cannot cross a new load.

    def test_preserves_success_stamp_after_reset_and_restore(self):
        h=Harness();h.start();h.finish();sent=h.ledger()['sent'];h.edge('invalidate')
        self.assertEqual(h.ledger()['sent'],sent)
        restored=Harness();restored.states.data=h.states.data.copy();restored.t=h.t
        restored.edge('complete','off','present');self.assertEqual(restored.messages,[])

    def test_corrupt_unknown_unavailable_missing_ledger(self):
        for value in ('broken','null','[]','unknown','unavailable'):
            h=Harness();h.states.data[LEDGER]=value;h.finish();self.assertEqual(h.messages,[])
        h=Harness();del h.states.data[LEDGER];h.start();h.finish();self.assertEqual(h.messages,[])
        h=Harness();h.states.data[LEDGER]='broken';h.start();h.finish();self.assertEqual(len(h.messages),1)

    def test_send_error_and_uncertain_acceptance_never_replayed(self):
        for fail in ('before_send','after_send','success_stamp'):
            h=Harness();h.start();h.fail=fail
            with self.assertRaises(RuntimeError):h.finish()
            self.assertEqual(h.ledger()['sent'],0)
            self.assertEqual(h.ledger()['claimed'],h.ledger()['cycle'])
            count=len(h.messages);h.fail=None;h.edge('complete','off','present')
            self.assertEqual(len(h.messages),count)
            h.states.data[DONE]='off';h.start();h.finish();self.assertEqual(len(h.messages),count+1)

    def test_silently_ignored_claim_cannot_dispatch(self):
        h=Harness();h.start();h.fail='claim_ignored';h.finish()
        self.assertEqual(h.messages,[])

    def test_claim_failure_prevents_dispatch(self):
        h=Harness();h.start();h.fail='before_claim'
        with self.assertRaises(RuntimeError):h.finish()
        self.assertEqual(h.messages,[]);self.assertEqual(h.ledger()['claimed'],0)

    def test_stale_cycle_delayed_queue_and_offline_rejected(self):
        h=Harness();h.start();h.t+=86400;h.finish();self.assertEqual(h.messages,[])
        h=Harness();h.start();h.edge('complete','off','present',seconds=3600,event_age=61);self.assertEqual(h.messages,[])
        h=Harness();h.start();h.states.data[CONNECTED]='off';h.finish();self.assertEqual(h.messages,[])

    def test_ambiguous_new_run_clears_old_cycle(self):
        h=Harness();h.start();h.states.data[DONE]='present';h.start();h.finish();self.assertEqual(h.messages,[])
        h=Harness();h.start();h.edge('run','unavailable','run');h.finish();self.assertEqual(h.messages,[])

    def test_only_expected_actions_and_serialization(self):
        self.assertEqual(RULE['mode'],'queued')
        source=yaml.safe_dump(RULE)
        self.assertNotIn('switch.turn',source)
        self.assertNotIn('button.press',source)
        self.assertEqual(source.count('script.notify_trevor_phone'),1)

if __name__=='__main__':unittest.main()
