"""Bounded EXP-015 windows; unchanged hwbp instrument, external liveness observer."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time

p = argparse.ArgumentParser()
p.add_argument('--mode', choices=['baseline', 'baseline2', 'cold', 'positive', 'postcold', 'postpositive'], required=True)
p.add_argument('--pid', type=int, required=True)
a = p.parse_args()
out = Path(__file__).resolve().parent
kit = out.parents[3] / 'Tools/analysis-kit/gfz-scripts'
receipt = out / (a.mode + '-run.json')
assert not receipt.exists(), 'Never overwrite a prior run'
record = dict(mode=a.mode, pid=a.pid, start_unix=time.time(), status='INCOMPLETE', commands=[],
              sources={str(f): hashlib.sha256(f.read_bytes()).hexdigest()
                       for f in [Path(__file__), out/'observe.py', out/'input_receipt.py',
                                 out/'probe_extension.py', kit/'hwbp.py', kit/'runtime_probe.py',
                                 kit/'ffxii_runtime.py', kit/'process_liveness.py']})
children = []
streams = []

def launch(cmd, label):
    stream = (out/(a.mode+'-'+label+'.txt')).open('x', encoding='utf-8')
    streams.append(stream)
    child = subprocess.Popen(cmd, stdout=stream, stderr=subprocess.STDOUT)
    entry = dict(command=cmd, label=label, pid=child.pid, start_unix=time.time())
    record['commands'].append(entry)
    children.append((child, entry))
    return child

try:
    state = subprocess.run([sys.executable,str(kit/'ffxii_runtime.py'),'state'],capture_output=True,text=True,timeout=15)
    record['state_before'] = dict(stdout=state.stdout,stderr=state.stderr,exit_code=state.returncode)
    assert state.returncode == 0 and 'IN-WORLD' in state.stdout and ('pid '+str(a.pid)) in state.stdout
    launch([sys.executable,str(out/'observe.py'),'--pid',str(a.pid),'--seconds','35',
            '--out',str(out/(a.mode+'-window.json'))], 'observer')
    time.sleep(2)
    if a.mode in ['cold', 'positive']:
        sites = ['003250F0'] if a.mode == 'cold' else ['003A1C50','003A1C8C']
        cmd = [sys.executable,str(kit/'hwbp.py'),'--pid',str(a.pid),'--seconds','30' if a.mode == 'cold' else '10',
               '--stop-after','2','--trace-out',str(out/(a.mode+'-trace.tsv'))]
        for site in sites:
            cmd += ['--addr',site]
        launch(cmd,'debugger')
    start = time.monotonic()
    for offset,key in [(5,'Enter'),(20,'C')]:
        time.sleep(max(0,start+offset-time.monotonic()))
        child = launch([sys.executable,str(out/'input_receipt.py'),'--keys',key,
                        '--out',str(out/(a.mode+'-'+key+'.json'))],key)
        assert child.wait(timeout=10) == 0, 'input probe failed'
    for child,entry in children:
        entry['exit_code'] = child.wait(timeout=45)
        entry['observed_end_unix'] = time.time()
        assert entry['exit_code'] == 0, entry
    record['status'] = 'COMPLETED'  # execution only; no automatic scientific verdict
finally:
    record['end_unix'] = time.time()
    record['live_children'] = [c.pid for c,e in children if c.poll() is None]
    # Inputs have guaranteed key release in their own finally. On a timeout, keep
    # child handles in the receipt for explicit recovery; never silently restart.
    for stream in streams:
        stream.close()
    receipt.write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
print(record['status'],a.mode,flush=True)
