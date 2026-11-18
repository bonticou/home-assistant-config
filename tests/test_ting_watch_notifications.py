import unittest
from pathlib import Path
from types import SimpleNamespace as S
import yaml
from jinja2 import Environment
ROOT=Path(__file__).resolve().parents[1]
class TingWatch(unittest.TestCase):
 def setUp(self):
  self.a=next(x for x in yaml.safe_load((ROOT/'automations/20-climate-commute.yaml').read_text()) if x['id']=='ting_unverified_hazard_notification')
 def test_only_utility_triggers(self):
  self.assertEqual([x['trigger'] for x in self.a['triggers']],['state','time_pattern'])
  self.assertEqual(self.a['triggers'][0]['entity_id'],['binary_sensor.ting_1_unverified_fire_hazard','binary_sensor.ting_2_unverified_fire_hazard'])
  self.assertEqual(self.a['triggers'][0]['to'],'on')
 def test_efh_only_never_pushes_even_when_due(self):
  t=Environment().from_string(self.a['conditions'][1]['value_template'])
  for device in [0,1,2]:
   result=t.render(is_state=lambda e,v:e==f'binary_sensor.ting_{device}_unverified_fire_hazard').strip().lower()=='true'
   self.assertEqual(result,device>0)
 def test_utility_repeat_throttle_and_activation(self):
  t=Environment().from_string(self.a['conditions'][-1]['value_template'])
  for trigger in ['utility_repeat','utility_activated']:
   for stamp,due in [('unknown',True),('recent',False),('old',True)]:
    result=t.render(trigger=S(id=trigger),states=lambda e:stamp,now=lambda:10000,as_timestamp=lambda v,*args:9999 if v=='recent' else 0 if v=='old' else v).strip().lower()=='true'
    self.assertEqual(result,trigger=='utility_activated' or due)
 def test_preserved_safety_guards_and_sender(self):
  self.assertEqual(self.a['conditions'][0],{'condition':'state','entity_id':'input_boolean.ting_watch_notifications_enabled','state':'on'})
  self.assertEqual(self.a['conditions'][2],{'condition':'state','entity_id':'binary_sensor.ting_confirmed_hazard_active','state':'off'})
  self.assertEqual(self.a['actions'],[{'action':'script.ting_send_notification','data':{'alert_kind':'unverified'}}])
if __name__=='__main__': unittest.main()
