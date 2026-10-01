import hashlib,json,sys
from datetime import datetime,timezone
from pathlib import Path
HERE=Path(__file__).resolve().parent;sha=lambda b:hashlib.sha256(b).hexdigest()
root=Path('Database/FFXII TZA/_experiments/evidence/skeletal-reset-live')
paths=[root/'skeletal/capture/result.json',root/'runtime-error.json',root/'session-health.json',root/'preflight.json',
 Path('Database/FFXII TZA/_experiments/EXP-127-skeletal-reset-live.md'),
 Path('Database/Tools/work/SWE2-AUDIT-SPEC/REVIEW-EXP127-SKELETAL-FAILED-SESSION.md')]
(HERE/'retained').mkdir(exist_ok=True);pins=[];sources={}
for i,p in enumerate(paths):
 b=p.read_bytes();sources[i]=b
 # The immutable existing raw event file is pinned in place, not duplicated or regenerated.
 name=None if i==0 else f'{i:02d}-'+p.name
 if name:(HERE/'retained'/name).write_bytes(b)
 pins.append({'path':p.as_posix(),'bytes':len(b),'sha256':sha(b),'retained':'retained/'+name if name else None})
r=json.loads(sources[0]);hits=r['hits'];assert hits
times=[h['unix'] for h in hits];assert all(isinstance(t,(int,float)) for t in times)
lo,hi=min(times),max(times)
selected=[{'raw_index':times.index(t),'event':hits[times.index(t)]} for t in [lo,hi]]
error=json.loads(sources[1]);health=json.loads(sources[2]);det=datetime.fromisoformat(error['at'].replace('Z','+00:00'))
assert det.tzinfo is not None
board=Path('Database/FFXII TZA/_index/_inbox/TEAM.json');b=json.loads(board.read_text())
task=next(t for t in b['tasks'] if t['id']=='ASTRA-REVIEW-EXP127-FAILED-SESSION')
(HERE/'primary.json').write_text(json.dumps({'method':'A existing timestamp/field meaning/proof-boundary analysis; no trace replay or new execution',
 'python_version':sys.version,'python_sha256':sha(Path(sys.executable).read_bytes()),'refs':pins,
 'selected_raw_events':selected,'event_unix_range':[lo,hi],
 'event_recorded_utc_range':[datetime.fromtimestamp(t,timezone.utc).isoformat() for t in [lo,hi]],
 'dialog_observed_utc':error['at'],'reported_clock_gap_seconds':det.timestamp()-hi,
 'health_fields':health,'board_review_recovery':{'board_revision':b['revision'],'epoch':b['recovery_epoch'],
 'task':task['id'],'status':task['status'],'recorded_refs':task.get('result_refs',[]),
 'actual_review_path':paths[-1].as_posix(),'note':'Recorded filename omitted SKELETAL; actual recoverable review inspected, no peer task overwritten.'},
 'limits':'Historical recorded wall clocks, no continuous health/dialog observer, no fatal-condition/onset timestamp and no proved clock synchronization/monotonicity between event and UI writers. Apparent chronology is not causal independence.'},indent=2)+'\n')
print('Retained timestamp meanings/raw pins; error dialog detected',det.isoformat(),'reported gap',det.timestamp()-hi)
