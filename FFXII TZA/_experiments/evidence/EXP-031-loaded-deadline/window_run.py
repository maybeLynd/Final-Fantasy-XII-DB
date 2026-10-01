"""Matched loaded-state windows; exact EXP030 CLI, no modified capture source."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time

p=argparse.ArgumentParser()
p.add_argument('--mode',choices=['baseline','capture','postcapture'],required=True)
p.add_argument('--pid',type=int,required=True)
a=p.parse_args()
out=Path(__file__).resolve().parent
kit=out.parents[3]/'Tools/analysis-kit/gfz-scripts'
candidate=out.parent/'EXP-030-deadline-integration'
sys.path.insert(0,str(kit))
import team
board=json.loads(team.BOARD.read_text())
assert any(t['id']=='ASTRA-HWBP-LOADED-DEADLINE-RUNTIME' and t['status']=='ACTIVE'
           and t['agent']=='ASTRA' for t in board['tasks'])
receipt=out/(a.mode+'-run.json')
assert not receipt.exists()
record=dict(mode=a.mode,pid=a.pid,start_unix=time.time(),status='INCOMPLETE',commands=[],
 sources={str(f):hashlib.sha256(f.read_bytes()).hexdigest() for f in
 [Path(__file__),out/'observe.py',out/'input_receipt.py',out/'probe_extension.py',
 candidate/'capture.py',candidate/'timeout_cleanup.py',candidate/'hwbp-source.py',
 candidate/'api_receipts.py',kit/'runtime_probe.py',kit/'ffxii_runtime.py',kit/'process_liveness.py']})
children=[]
streams=[]


def launch(cmd,label):
    stream=(out/(a.mode+'-'+label+'.txt')).open('x')
    streams.append(stream)
    child=subprocess.Popen(cmd,stdout=stream,stderr=subprocess.STDOUT)
    entry=dict(command=cmd,label=label,pid=child.pid,start_unix=time.time())
    record['commands'].append(entry)
    children.append((child,entry))
    return child


try:
    state=subprocess.run([sys._base_executable,str(kit/'ffxii_runtime.py'),'state'],
                         capture_output=True,text=True,timeout=15)
    record['state_before']=dict(stdout=state.stdout,stderr=state.stderr,exit_code=state.returncode)
    assert state.returncode==0 and 'IN-WORLD' in state.stdout and ('pid '+str(a.pid)) in state.stdout
    start=time.monotonic()
    launch([sys._base_executable,str(out/'observe.py'),'--pid',str(a.pid),'--seconds','65',
            '--out',str(out/(a.mode+'-window.json'))],'observer')
    time.sleep(2)
    if a.mode=='capture':
        launch([sys._base_executable,str(candidate/'capture.py'),'--pid',str(a.pid),
                '--addr','003A1C50','--seconds','1','--out',str(out/'deadline-capture')],'debugger')
    for offset,key in [(5,'Enter'),(50,'C')]:
        time.sleep(max(0,start+offset-time.monotonic()))
        child=launch([sys._base_executable,str(out/'input_receipt.py'),'--keys',key,
                      '--out',str(out/(a.mode+'-'+key+'.json'))],key)
        assert child.wait(timeout=10)==0,'input probe failed'
    for child,entry in children:
        entry['exit_code']=child.wait(timeout=45)
        entry['observed_end_unix']=time.time()
        assert entry['exit_code']==0,entry
    record['status']='COMPLETED'
finally:
    record['end_unix']=time.time()
    record['live_children']=[c.pid for c,e in children if c.poll() is None]
    for stream in streams:stream.close()
    receipt.write_text(json.dumps(record,indent=2)+'\n')
print(record['status'],a.mode,flush=True)
