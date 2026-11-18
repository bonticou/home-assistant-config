import unittest
from pathlib import Path
from types import SimpleNamespace as S
import yaml
from jinja2 import Environment
ROOT=Path(__file__).resolve().parents[1]
class TingWatch(unittest.TestCase):
 def setUp(self):
  self.a=next(x for x in yaml.safe_load((ROOT/'automations/20-climate-commute.yaml').read_text()) if x['id']=='ting_unverified_hazard_notification')
 def test_only_utility_has_periodic_repeat(self):
  self.assertEqual([x['trigger'] for x in self.a['triggers']],['state','state','time_pattern'])
  self.assertEqual(self.a['triggers'][2]['id'],'utility_repeat')
  self.assertEqual(self.a['triggers'][0]['from'],'off')
  self.assertEqual(self.a['triggers'][0]['to'],'on')
 def test_event_guard(self):
  t=Environment().from_string(self.a['conditions'][-1]['value_template'])
  for old,new,expected in [('Ting 1','Ting 1',False),('Ting 1','Ting 1, Ting 2',True),('Ting 1, Ting 2','Ting 1',False),('Ting 1','Ting 2',True),('None','Ting 1',False),('Ting 1','None',False),(None,'Ting 1',False)]:
   trigger=S(id='devices_changed',from_state=S(attributes={'unverified_devices':old}) if old else None,to_state=S(attributes={'unverified_devices':new}))
   self.assertEqual(t.render(trigger=trigger).strip().lower()=='true',expected,(old,new))
  self.assertEqual(t.render(trigger=S(id='activated')).strip().lower(),'true')
 def test_repeat_only_actual_utility_and_due(self):
  t=Environment().from_string(self.a['conditions'][-1]['value_template'])
  for utility in [False,True]:
   for stamp,due in [('unknown',True),('recent',False),('old',True)]:
    for device in [1,2]:
     result=t.render(trigger=S(id='utility_repeat'),is_state=lambda e,v: utility and e==f'binary_sensor.ting_{device}_unverified_fire_hazard',states=lambda e:stamp,now=lambda:10000,as_timestamp=lambda v,*args: 9999 if v=='recent' else 0 if v=='old' else v).strip().lower()=='true'
     self.assertEqual(result,utility and due,(utility,stamp,device))
 def test_preserved_safety_guards_and_sender(self):
  self.assertEqual(self.a['conditions'][2],{'condition':'state','entity_id':'binary_sensor.ting_confirmed_hazard_active','state':'off'})
  self.assertEqual(self.a['actions'],[{'action':'script.ting_send_notification','data':{'alert_kind':'unverified'}}])
if __name__=='__main__': unittest.main()
