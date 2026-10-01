"""Bounded EXP-010 paired window. Original hwbp.py runs unchanged."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time

p = argparse.ArgumentParser()
p.add_argument('--mode', choices=['baseline', 'noarm', 'post', 'visual'], required=True)
p.add_argument('--pid', type=int, required=True)
a = p.parse_args()
out = Path(__file__).resolve().parent
kit = out.parents[3] / 'Tools/analysis-kit/gfz-scripts'
record = dict(mode=a.mode, pid=a.pid, start_unix=time.time(), status='INCOMPLETE', commands=[],
              sources={str(f):hashlib.sha256(f.read_bytes()).hexdigest()
                       for f in [Path(__file__), out/'observe.py', out/'input_receipt.py',
                                 out/'probe_extension.py', kit/'hwbp.py']})
children = []
streams = []
def launch(cmd, label):
    stream = (out/(a.mode+'-'+label+'.txt')).open('w', encoding='utf-8')
    streams.append(stream)
    child = subprocess.Popen(cmd, stdout=stream, stderr=subprocess.STDOUT)
    entry = dict(command=cmd, label=label, pid=child.pid, start_unix=time.time())
    record['commands'].append(entry)
    children.append((child, entry))
    return child
try:
    state = subprocess.run([sys.executable,str(kit/'ffxii_runtime.py'),'state'],capture_output=True,text=True)
    record['state_before'] = dict(stdout=state.stdout,stderr=state.stderr,exit_code=state.returncode)
    assert state.returncode == 0 and 'IN-WORLD' in state.stdout and ('pid '+str(a.pid)) in state.stdout
    obs = launch([sys.executable,str(out/'observe.py'),'--pid',str(a.pid),'--seconds','50' if a.mode == 'visual' else '35',
                  '--out',str(out/(a.mode+'-window.json'))], 'observer')
    time.sleep(2)
    if a.mode in ['noarm', 'visual']:
        launch([sys.executable,str(kit/'hwbp.py'),'--pid',str(a.pid),'--no-arm','--seconds','45' if a.mode == 'visual' else '30',
                '--trace-out',str(out/(a.mode+'-trace.tsv'))], 'debugger')
    start = time.monotonic()
    for offset, key in ([(5,'Enter')] if a.mode == 'visual' else [(5,'Enter'),(15,'C')]):
        time.sleep(max(0, start+offset-time.monotonic()))
        child = launch([sys.executable,str(out/'input_receipt.py'),'--keys',key,
                        '--out',str(out/(a.mode+'-'+key+'.json'))], key)
        assert child.wait() == 0, 'input probe failed'
    for child, entry in children:
        entry['exit_code'] = child.wait()
        entry['observed_end_unix'] = time.time()
        assert entry['exit_code'] == 0, entry
    state = subprocess.run([sys.executable,str(kit/'ffxii_runtime.py'),'state'],capture_output=True,text=True)
    record['state_after'] = dict(stdout=state.stdout,stderr=state.stderr,exit_code=state.returncode)
    record['status'] = 'COMPLETED'  # execution status only, never a scientific pass
finally:
    record['end_unix'] = time.time()
    record['live_children'] = [c.pid for c,e in children if c.poll() is None]
    for stream in streams:
        stream.close()
    (out/(a.mode+'-run.json')).write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
print(record['status'], a.mode, flush=True)
