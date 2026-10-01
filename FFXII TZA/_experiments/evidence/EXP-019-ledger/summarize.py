"""Summarize selected raw observations; no live process access."""
from pathlib import Path
import hashlib,json,struct,statistics
root=Path(__file__).resolve().parent
result={}
for name in ['stepping-qualified.json','combat-window-1.json','combat-window-2.json']:
 p=root/name;d=json.loads(p.read_text());assert d['status']=='OBSERVED'
 samples=d['samples'];states=d['states'];assert samples and states
 intervals=[s['end_seconds']-s['start_seconds'] for s in samples]
 gaps=[b['start_seconds']-a['start_seconds'] for a,b in zip(samples,samples[1:])]
 groups=[];slot3=[];hp0=[];hp4=[]
 for s in states:
  raw=bytes.fromhex(s['ledger_raw']);assert len(raw)==1536
  groups.append([*struct.unpack_from('<QQ',raw),raw[16]])
  slot3.append(s['slot3'])
  hp0.extend(u['hp'] for u in s['units'] if u['slot']==0 and u['hp'] is not None)
  hp4.extend(u['hp'] for u in s['units'] if u['slot']==4 and u['hp'] is not None)
 result[name]=dict(sha256=hashlib.sha256(p.read_bytes()).hexdigest(),status=d['status'],samples=len(samples),states=len(states),observed_seconds=samples[-1]['end_seconds'],read_max_seconds=max(intervals),sample_gap_max_seconds=max(gaps),sample_gap_median_seconds=statistics.median(gaps),frame_first=samples[0]['frame_before'],frame_last=samples[-1]['frame_after'],cross_frame_reads=sum(s['frame_before']!=s['frame_after'] for s in samples),group1_unique=sorted(set(map(tuple,groups))),slot3_unique=sorted(set(slot3)),player_hp_range=[min(hp0),max(hp0)],slot4_hp_range=[min(hp4),max(hp4)],scale_unique=sorted(set(s['scale'] for s in states)),actor_gates=sorted(set(s['actor_gate'] for s in states)),dispatch_gates=sorted(set(s['dispatch_gate'] for s in states)),field_gates=sorted(set(s['field_gate'] for s in states)))
(root/'normalized-observations.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
