"""Overnight retries preserve protection, boundaries and durable notice windows."""
import unittest
from pathlib import Path
from datetime import datetime, timedelta
from jinja2 import Environment, StrictUndefined
import yaml
ROOT=Path(__file__).resolve().parents[1]

class OvernightTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  rules=yaml.safe_load((ROOT/'automations/10-lighting-security.yaml').read_text())
  cls.rule=next(a for a in rules if a['id']=='overnight_lights_one_am_auto_off')
  cls.morning=next(a for a in rules if a['id']=='overnight_lights_morning_review')
  cls.reporter=next(a for a in rules if a['id']=='overnight_lights_cleanup_report')
  cls.script=yaml.safe_load((ROOT/'scripts.yaml').read_text())['lights_overnight_sweep_off']
  cls.env=Environment(undefined=StrictUndefined)
 def render(self,t,hour=2,minute=0,guard='clear',snooze='unknown',last='unknown',**extra):
  now=datetime(2026,11,14,hour,minute)
  def stamp(v,default=0):
   try:return (v if isinstance(v,datetime) else datetime.fromisoformat(v)).timestamp()
   except (ValueError,TypeError):return default
  def states(id):return snooze if id.endswith('snooze_until') else last
  ctx=dict(guard=guard,now=lambda:now,states=states,state_attr=lambda *_:guard,as_timestamp=stamp,
   today_at=lambda s:datetime.combine(now.date(),datetime.strptime(s,'%H:%M').time()),is_number=lambda x:str(x).isdigit())
  ctx.update(extra)
  return self.env.from_string(t).render(**ctx).strip()
 def truth(self,t,**kw):return self.render(t,**kw)=='True'
 def test_watchdog_coverage_and_boundaries(self):
  t=self.rule['triggers'][0]['value_template']
  for h in range(24):
   for m in range(60):
    self.assertEqual(self.truth(t,hour=h,minute=m),1<=h<6 and (m%5==0 or (h==5 and m==59)))
 def test_scheduled_script_rechecks_each_pass(self):
  passes=[a['repeat'] for a in self.script['sequence'] if 'repeat' in a]
  self.assertEqual(len(passes),2)
  for p in passes:
   t=p['sequence'][0]['value_template']
   self.assertTrue(self.truth(t,scheduled=True))
   for guard in ['guest_override','up_late_media','vacation','unknown','unavailable','']:
    self.assertFalse(self.truth(t,scheduled=True,guard=guard))
   self.assertFalse(self.truth(t,scheduled=True,snooze='2026-11-14 03:00:00'))
   self.assertTrue(self.truth(t,scheduled=True,snooze='2026-11-14 01:00:00'))
   self.assertFalse(self.truth(t,scheduled=True,hour=6))
   self.assertFalse(self.truth(t,scheduled=True,hour=0))
   # An explicit manual Turn off now remains usable outside the schedule.
   self.assertTrue(self.truth(t,scheduled=False,hour=12,guard='guest_override'))
   self.assertTrue(self.truth(t,hour=12,guard='guest_override'))
   self.assertTrue(p['sequence'][1]['continue_on_error'])
 def test_durable_notice_windows(self):
  failure=self.reporter['actions'][-1]['default'][1]['value_template']
  morning=[a['value_template'] for a in self.morning['actions'] if a.get('condition')=='template'][-1]
  for t,hour,boundary in [(failure,2,'01:00:00'),(morning,6,'06:00:00')]:
   for old in ['unknown','unavailable','2026-11-13 08:00:00','2026-11-14 00:00:10']:
    self.assertTrue(self.truth(t,hour=hour,last=old))
   self.assertFalse(self.truth(t,hour=hour,last='2026-11-14 '+boundary))
  self.assertTrue(self.truth(morning,hour=6,last='2026-11-14 02:00:00'))
 def test_reason_does_not_conflate_guest_modes(self):
  t=self.rule['actions'][1]['variables']['decision_reason']
  base=dict(watched_count='2',snooze_until='unknown',guest_lighting='off',scene='Evening',tv_hold='off',tv_player='paused',vacation='off',house_guests_motion_only='on')
  self.assertEqual(self.render(t,**base),'No protection is blocking cleanup')
  for changes,contains in [({'guest_lighting':'on'},'Guest Lighting'),({'tv_hold':'on'},'TV protection'),({'scene':'TV'},'TV protection'),({'tv_player':'playing'},'TV protection'),({'vacation':'on'},'Vacation'),({'watched_count':'unavailable'},'unavailable')]:
   self.assertIn(contains,self.render(t,**(base|changes)))
 def test_bounded_wait_and_recovery_triggers(self):
  waits=[a for a in self.rule['actions'] if 'wait_template' in a]
  self.assertEqual(waits[0]['timeout'],'00:01:00')
  types={t['trigger'] for t in self.rule['triggers']}
  self.assertTrue({'time','homeassistant','event','template'}<=types)
  self.assertGreaterEqual(self.rule['trace']['stored_traces'],200)
  for rule in [self.rule,self.morning]:
   # Diagnostics precede conditions, so reload captures real state without switching.
   self.assertIn('guard',rule['actions'][0]['variables'])
   self.assertEqual(rule['mode'],'single')
  # Only record sent cycle after the notification returns successfully.
  self.assertEqual(self.morning['actions'][-2]['action'],'script.notify_trevor_phone')
  self.assertEqual(self.morning['actions'][-1]['action'],'input_datetime.set_datetime')
  for a in self.rule['actions']:
   if a.get('action')=='logbook.log':self.assertTrue(a['continue_on_error'])
 def test_notification_isolation(self):
  self.assertEqual(self.rule['actions'][-1]['event'],'overnight_lights_cleanup_evaluated')
  self.assertNotIn('script.notify_trevor_phone',str(self.rule))
  branch=self.reporter['actions'][-1]['default']
  self.assertEqual(branch[-2]['action'],'script.notify_trevor_phone')
  self.assertEqual(branch[-1]['action'],'input_datetime.set_datetime')
  self.assertEqual(self.reporter['mode'],'single')
 def test_ready_trigger_respects_guards_and_window(self):
  t=self.rule['triggers'][1]['value_template']
  # The test state accessor supplies the count through last and snooze separately.
  self.assertTrue(self.truth(t,last='2'))
  self.assertFalse(self.truth(t,last='0'))
  self.assertFalse(self.truth(t,last='unavailable'))
  self.assertFalse(self.truth(t,last='2',hour=8))
  for guard in ['guest_override','up_late_media','vacation','unknown']:
   self.assertFalse(self.truth(t,last='2',guard=guard))
  self.assertFalse(self.truth(t,last='2',snooze='2026-11-14 03:00:00'))

if __name__=='__main__': unittest.main()
