"""One predefined forward block with per-pulse progress/health stops, not a pathfinder."""
import json
import math
from pathlib import Path
import subprocess
import sys
import time

root=Path(__file__).resolve().parent
pid=int(sys.argv[1]);prefix=sys.argv[2]
assert prefix.isalnum()
result=dict(pid=pid,phase='prospective second attempt',start_unix=time.time(),pulses=[],status='INCOMPLETE')
summary=root/(prefix+'-block.json');assert not summary.exists()
def invoke(key,hold,index):
    path=root/(prefix+'-%02d.json'%index)
    command=[sys.executable,str(root/'step.py'),'--pid',str(pid),'--field','--out',str(path)]
    if key:command+=['--key',key,'--hold',str(hold)]
    p=subprocess.run(command,capture_output=True,text=True)
    result['pulses'].append(dict(command=command,exit_code=p.returncode,stdout=p.stdout,stderr=p.stderr))
    assert p.returncode==0,result['pulses'][-1]
    return json.loads(path.read_text())['after']
def pair(state,actor=None):
    player=next(r for r in state['rows'] if r['slot']==0)
    targets=[r for r in state['rows'] if r['group']==1 and (actor is None or r['actor']==actor)]
    assert len(targets)==1,'tracked group actor missing/ambiguous'
    return player,targets[0]
try:
    baseline=invoke(None,0,0)
    player,target=pair(baseline);actor=target['actor']
    assert player['hp']==103 and target['hp']==134
    baseline_gap=math.dist(player['position'],target['position'])
    result.update(initial_gap=baseline_gap,tracked_actor=actor)
    state=invoke('Left',.125,1)
    previous=baseline_gap;nonprogress=0
    for index in range(2,10):
        if time.time()-result['start_unix']>=20:
            result['status']='WALL_LIMIT';break
        state=invoke('W',1,index)
        player,target=pair(state,actor)
        gap=math.dist(player['position'],target['position'])
        nonprogress=nonprogress+1 if gap>=previous else 0
        result['pulses'][-1].update(gap=gap,player_hp=player['hp'],target_hp=target['hp'],nonprogress=nonprogress)
        if player['hp']<70:
            result['status']='HEALTH_STOP';break
        if nonprogress>=2:
            result['status']='NONPROGRESS_STOP';break
        previous=gap
    else:result['status']='PULSE_LIMIT'
except BaseException as e:
    result['error']=repr(e)
    raise
finally:
    result['end_unix']=time.time()
    summary.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k!='pulses'}))
