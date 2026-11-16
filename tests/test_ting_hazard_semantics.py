"""Reviewed metadata must not override the primary fire alarm or become confirmed."""
import itertools
import unittest
from pathlib import Path
from datetime import datetime
import yaml
from jinja2 import Environment, StrictUndefined
ROOT=Path(__file__).resolve().parents[1]

class TingHazardTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  config=yaml.load((ROOT/'configuration.yaml').read_text(),Loader=yaml.BaseLoader)
  cls.entities={e.get('unique_id'):e for group in config['template'] for domain in ['sensor','binary_sensor'] for e in group.get(domain,[])}
  cls.env=Environment(undefined=StrictUndefined)
 def render(self,template,values):
  return self.env.from_string(template).render(states=lambda e:values.get(e,'unknown'),is_state=lambda e,s:values.get(e,'off')==s).strip()
 def test_primary_reviewed_and_unknown_matrix(self):
  for device,primary,efh,ufh,status in itertools.product([1,2],[False,True],[False,True],[False,True],['ReviewedNotFire','ReviewedSuspicious','Active','none','unknown','unavailable','']):
   with self.subTest(device=device,primary=primary,efh=efh,ufh=ufh,status=status):
    v={f'binary_sensor.ting_{device}_fire_hazard':'on' if primary else 'off',f'binary_sensor.ting_{device}_electrical_fire_hazard':'on' if efh else 'off',f'binary_sensor.ting_{device}_unverified_fire_hazard':'on' if ufh else 'off',f'sensor.ting_{device}_electrical_fire_hazard_status':status}
    confirmed=primary or (efh and status not in ['ReviewedNotFire','ReviewedSuspicious'])
    watch=(ufh or (efh and status=='ReviewedSuspicious')) and not confirmed
    for id,expected in [('ting_confirmed_hazard_active',confirmed),('ting_unverified_hazard_active',watch)]:
     self.assertEqual(self.render(self.entities[id]['state'],v)=='True',expected)
    listed=self.render(self.entities['ting_notification_status']['attributes']['confirmed_devices'],v)
    self.assertEqual(listed,f'Ting {device}' if confirmed else 'None')
 def test_one_reviewed_device_never_masks_other_primary(self):
  v={'binary_sensor.ting_1_electrical_fire_hazard':'on','sensor.ting_1_electrical_fire_hazard_status':'ReviewedSuspicious','binary_sensor.ting_2_fire_hazard':'on'}
  self.assertEqual(self.render(self.entities['ting_confirmed_hazard_active']['state'],v),'True')
  self.assertEqual(self.render(self.entities['ting_notification_status']['attributes']['confirmed_devices'],v),'Ting 2')
 def test_message_text_never_controls_hazard_classification(self):
  for message,status,primary in itertools.product(['No Hazards Detected','unknown','unavailable','','Possible hazard'],['ReviewedSuspicious','ReviewedNotFire','Active','unknown'],[False,True]):
   with self.subTest(message=message,status=status,primary=primary):
    v={'binary_sensor.ting_1_fire_hazard':'on' if primary else 'off','binary_sensor.ting_1_electrical_fire_hazard':'on','sensor.ting_1_electrical_fire_hazard_status':status,'sensor.ting_1_hazard_message':message,'sensor.ting_1_electrical_fire_hazard_message':message}
    expected=primary or status not in ['ReviewedNotFire','ReviewedSuspicious']
    self.assertEqual(self.render(self.entities['ting_confirmed_hazard_active']['state'],v)=='True',expected)
    self.assertEqual(self.render(self.entities['ting_unverified_hazard_active']['state'],v)=='True',status=='ReviewedSuspicious' and not primary)
 def test_owner_snooze_expires_and_preserves_other_kinds(self):
  script=yaml.safe_load((ROOT/'scripts.yaml').read_text())['ting_send_notification']
  gate=script['sequence'][1]['value_template']
  for kind in ['confirmed','unverified','confirmed_clear','voltage','offline','offline_clear','freeze','learning_complete']:
   for date in ['2026-11-16T08:18:07-05:00','2026-11-16T08:18:08-05:00','2026-11-17T01:00:00-05:00']:
    result=self.env.from_string(gate).render(kind=kind,now=lambda:date,as_timestamp=lambda x:datetime.fromisoformat(x).timestamp()).strip()=='True'
    self.assertEqual(result,kind not in ['confirmed','unverified','confirmed_clear'] or date!='2026-11-16T08:18:07-05:00')
 def test_message_placeholder_filter_preserves_useful_text(self):
  template=self.entities['ting_notification_status']['attributes']['ting_messages']
  for text in ['No Hazards Detected','no hazards detected','  No hazards detected  ','UNKNOWN',' unavailable ','None','']:
   values={'sensor.ting_1_hazard_message':text}
   self.assertEqual(self.render(template,values),'')
  values={'sensor.ting_1_hazard_message':'  Check outlet wiring  ',
          'sensor.ting_2_hazard_message':'Check outlet wiring',
          'sensor.ting_1_electrical_fire_hazard_message':'Call Ting support'}
  self.assertEqual(self.render(template,values),'Check outlet wiring Call Ting support')
if __name__=='__main__':unittest.main()
