"""Non-actuating production-template tests for first-transition timer ownership."""
from datetime import datetime, timedelta, timezone
from pathlib import Path
from types import SimpleNamespace as NS
import unittest

import yaml
from jinja2 import StrictUndefined
from jinja2.nativetypes import NativeEnvironment

ROOT = Path(__file__).resolve().parents[1]
TARGET = 'switch.exterior_mud_room_stairs'
T = datetime(2026, 11, 19, 23, tzinfo=timezone.utc)


def state(value, second=0, context='ours', **attributes):
    return NS(state=value, last_changed=T + timedelta(seconds=second),
              context=NS(id=context), attributes=attributes)


def timestamp(value, default=None):
    try:
        return (value if isinstance(value, datetime) else datetime.fromisoformat(value)).timestamp()
    except (TypeError, ValueError):
        return default


class MotionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rule = next(a for a in yaml.safe_load((ROOT/'automations/10-lighting-security.yaml').read_text())
                        if a['id'] == 'mudroom_ring_motion_exterior_light')
        cls.watch = cls.rule['actions'][1]['parallel'][0]['sequence']
        cls.command = cls.rule['actions'][1]['parallel'][1]['sequence']

    def render(self, template, current=None, **extra):
        current = current or state('off')
        states = NS(switch=NS(exterior_mud_room_stairs=current))
        env = NativeEnvironment(undefined=StrictUndefined)
        return env.from_string(template).render(states=states,
            is_state=lambda e, s: current.state == s if e == TARGET else extra.get(e) == s,
            as_timestamp=timestamp, now=lambda: T + timedelta(seconds=extra.pop('elapsed', 1)),
            **extra)

    def motion(self, old, new):
        return self.render(self.rule['conditions'][0]['value_template'],
                           trigger=NS(from_state=old, to_state=new))

    def claim(self, old, new):
        return self.render(self.watch[1]['value_template'],
            wait=NS(trigger=NS(from_state=old, to_state=new)),
            off_stamp=T.isoformat(), owner_context='ours')

    def should_off(self, current, completed=False):
        return self.render(self.watch[4]['value_template'], current,
            on_stamp=(T+timedelta(seconds=1)).isoformat(), wait=NS(completed=completed))

    def test_only_fresh_motion_including_first_after_unknown(self):
        new = state((T+timedelta(seconds=1)).isoformat(), 1, event_type='motion')
        self.assertTrue(self.motion(state('unknown'), new))
        self.assertFalse(self.motion(None, new))
        self.assertFalse(self.motion(new, new))
        for value in ['unknown', 'unavailable', T.isoformat()]:
            self.assertFalse(self.motion(state('unknown'), state(value, 100, event_type='motion')))
        self.assertFalse(self.motion(state('unknown'), state(T.isoformat(), event_type='ding')))
        self.assertFalse(self.motion(state('unknown'), state(T.isoformat(), event_type='motion', restored=True)))

    def test_dark_hours_and_confirmed_off(self):
        self.assertEqual(self.rule['conditions'][1],
                         {'condition':'state','entity_id':'sun.sun','state':'below_horizon'})
        self.assertEqual(self.rule['conditions'][2],
                         {'condition':'state','entity_id':TARGET,'state':'off'})
        for value in ['on','unknown','unavailable']:
            self.assertFalse(self.render(self.command[1]['value_template'],state(value),off_stamp=T.isoformat()))
        self.assertFalse(self.render(self.command[1]['value_template'],state('off',2),off_stamp=T.isoformat()))

    def test_claim_first_ack_only(self):
        self.assertTrue(self.claim(state('off'),state('on',1)))
        self.assertFalse(self.claim(state('off'),state('on',1,context='manual')))
        self.assertFalse(self.claim(None,state('on',1)))
        self.assertFalse(self.claim(state('off'),state('unavailable',1)))

    def test_recent_restored_event_is_not_fresh_motion(self):
        recent = state(T.isoformat(), 2, event_type='motion')
        for previous in ['unknown','unavailable']:
            self.assertFalse(self.motion(state(previous,1),recent))
        real = state((T+timedelta(seconds=2)).isoformat(),2,event_type='motion')
        self.assertTrue(self.motion(state('unknown',1),real))
        self.assertFalse(self.motion(state('unavailable',1),real))
        self.assertFalse(self.motion(state('unknown',1,restored=True),real))
        future_previous=state((T+timedelta(seconds=3)).isoformat(),0,event_type='motion')
        self.assertFalse(self.motion(future_previous,real))

    def test_missed_first_ack_never_adopts_later_on(self):
        self.assertFalse(self.watch[0]['continue_on_timeout'])
        # No trigger means the branch terminates before accessing wait.trigger.
        # Missing the first on cannot turn the later manual on into an owned one.
        self.assertFalse(self.claim(state('off',8),state('on',9)))
        self.assertFalse(self.claim(state('unknown',8),state('on',9)))

    def test_rapid_off_on_before_ack_resumes_same_context(self):
        # Even if wait.trigger has advanced to the later manual on, its prior
        # off transition differs. A reused Lutron service context cannot own it.
        self.assertFalse(self.claim(state('off',2),state('on',3)))
        # If first acknowledgement is retained, current last_changed still
        # rejects that later cycle, including off/on before service returns.
        self.assertFalse(self.should_off(state('on',3)))

    def test_intervening_transitions_permanently_release_cycle(self):
        self.assertTrue(self.should_off(state('on',1)))
        for value in ['off','unknown','unavailable']:
            self.assertFalse(self.should_off(state(value,2)))
        self.assertFalse(self.should_off(state('on',3)))
        self.assertFalse(self.should_off(state('on',1),completed=True))

    def test_timeout_measured_from_ack_not_service_return(self):
        expr=self.watch[3]['timeout']['seconds']
        self.assertEqual(self.render(expr,on_stamp=(T+timedelta(seconds=1)).isoformat(),elapsed=4),117)
        self.assertEqual(self.render(expr,on_stamp=T.isoformat(),elapsed=130),0)
        self.assertFalse(self.watch[0]['continue_on_timeout'])

    def test_repeated_motion_has_no_restart_or_other_actions(self):
        self.assertEqual(self.rule['mode'],'single')
        self.assertEqual(self.rule['triggers'],[{'trigger':'state','entity_id':'event.mudroom_door_motion','to':None}])
        actions=[]
        def walk(value):
            if isinstance(value,dict):
                if 'action' in value: actions.append((value['action'],value['target']['entity_id']))
                for child in value.values(): walk(child)
            elif isinstance(value,list):
                for child in value: walk(child)
        walk(self.rule)
        self.assertEqual(actions,[('switch.turn_off',TARGET),('switch.turn_on',TARGET)])
        self.assertEqual(self.rule['actions'][0]['variables']['owner_context'],'{{ context.id }}')


if __name__ == '__main__':
    unittest.main()
