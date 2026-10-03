from pathlib import Path
import json
from datetime import datetime, timezone, timedelta
rows=[
('CG-DEMO-001','Large pothole near the school gate is causing vehicles to slow down.','Roads','Road Damage','High',0.92,1),
('CG-DEMO-002','Several potholes have appeared on the main road after the rain.','Roads','Road Damage','High',0.89,1),
('CG-DEMO-003','Road pavement is damaged near the bus stop and needs repair.','Roads','Road Damage','Medium',0.86,1),
('CG-DEMO-004','Water supply has been interrupted since morning in our lane.','Water','Water Supply','High',0.87,2),
('CG-DEMO-005','There is a leaking water pipeline outside the market.','Water','Water Supply','High',0.91,2),
('CG-DEMO-006','Streetlight is not working and the road is dark at night.','Electrical','Street Lighting','Medium',0.90,3),
('CG-DEMO-007','Three street lights near the park are broken.','Electrical','Street Lighting','Medium',0.88,3),
('CG-DEMO-008','Garbage has not been collected for four days.','Sanitation','Sanitation','High',0.91,4),
('CG-DEMO-009','Overflowing waste bins are creating a bad smell.','Sanitation','Sanitation','Medium',0.84,4),
('CG-DEMO-010','Traffic signal is malfunctioning at the junction.','Traffic','Traffic','High',0.86,None),
('CG-DEMO-011','Power cut has continued for several hours.','Electrical','Electricity','High',0.88,None),
('CG-DEMO-012','There is a mosquito problem around stagnant water.','Health','Public Health','Medium',0.82,None),
]
now=datetime.now(timezone.utc)
out=[]
for i,(cid,text,dept,cat,urg,conf,cluster) in enumerate(rows):
 out.append({'complaint_id':cid,'text':text,'source_name':'demo','location_text':'Mumbai','category':cat,'department':dept,'confidence':conf,'urgency':urg,'urgency_score':{'Routine':.3,'Medium':.55,'High':.75,'Critical':.95}[urg],'status':'new','cluster_id':cluster,'created_at':(now-timedelta(days=11-i)).isoformat()})
p=Path('data/demo/complaints.json');p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(out,indent=2,ensure_ascii=False));Path('data/demo/complaints.json').replace('data/demo/complaints.json')
# API repository reads data/demo/complaints.json directly.
print(f'Seeded {len(out)} demo complaints.')
