"""One fixed EXP127 window using unchanged EXP030/031 instruments; no input."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time

E = Path(__file__).resolve().parent
R = E.parents[4]
sys.path.insert(0, str(R/'Database/Tools/analysis-kit/gfz-scripts'))
import team
import ffxii_runtime as rt

p = argparse.ArgumentParser()
p.add_argument('arm', choices=['control', 'skeletal'])
a = p.parse_args()
out = E / a.arm
out.mkdir()
record = dict(status='INVALID', arm=a.arm, start_unix=time.time(),
              runner_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
observer = None
try:
    b = json.loads(team.BOARD.read_text())
    assert any(t['id']=='ASTRA-SKELETAL-RUNTIME' and t['status']=='ACTIVE'
               and t['agent']=='ASTRA' for t in b['tasks'])
    for name, digest in json.loads((E/'preflight.json').read_text())['sources'].items():
        assert hashlib.sha256((R/name).read_bytes()).hexdigest()==digest, name
    process = json.loads((E/'process.json').read_text())
    assert rt.list_processes()==[process]
    pid = process['pid']
    if a.arm=='skeletal':
        control = json.loads((E/'control/run.json').read_text())
        assert control['status']=='QUALIFIED_WINDOW' and control['positive_hits']>0
        assert control['live_cpu_after_detach_seconds']>0
    addresses = ['003A1C50'] + (['003E3C30','003E3C7A','003E3C7F'] if a.arm=='skeletal' else [])
    obs_cmd = [sys.executable, '-u', str(E.parent/'EXP-031-loaded-deadline/recovered/observe.py'),
               '--pid', str(pid), '--seconds', '12', '--out', str(out/'liveness.json')]
    cap_cmd = [sys.executable, str(E.parent/'EXP-030-deadline-integration/capture.py'),
               '--pid', str(pid), '--seconds', '1', '--out', str(out/'capture')]
    for address in addresses:
        cap_cmd += ['--addr', address]
    record.update(process=process, observer_command=obs_cmd, capture_command=cap_cmd)
    with (out/'observer.log').open('xb') as log:
        observer = subprocess.Popen(obs_cmd, stdout=log, stderr=subprocess.STDOUT,
                                    creationflags=subprocess.CREATE_NO_WINDOW)
        record['observer_pid'] = observer.pid
        deadline = time.monotonic()+8
        while b'OBSERVING ' not in (out/'observer.log').read_bytes():
            assert observer.poll() is None, 'Observer exited before ready'
            assert time.monotonic()<deadline, 'Observer readiness deadline'
            time.sleep(.05)
        record['observer_ready_unix'] = time.time()
        time.sleep(1)
        record['capture_start_unix'] = time.time()
        with (out/'capture.log').open('xb') as cap_log:
            cap = subprocess.run(cap_cmd, stdout=cap_log, stderr=subprocess.STDOUT,
                                 timeout=15, creationflags=subprocess.CREATE_NO_WINDOW)
        record['capture_returncode'] = cap.returncode
        record['capture_end_unix'] = time.time()
        record['observer_returncode'] = observer.wait(timeout=20)
    trace = json.loads((out/'capture/result.json').read_text())
    live = json.loads((out/'liveness.json').read_text())
    assert cap.returncode==0 and trace['status']=='PASS' and trace['detach']
    assert trace['cleanup']['status']=='PASS' and not trace['errors']
    assert live['status']=='OBSERVED' and record['observer_returncode']==0
    before = [s for s in live['samples'] if live['window_start_unix']+s['seconds'] < record['capture_start_unix']]
    after = [s for s in live['samples'] if live['window_start_unix']+s['seconds'] > record['capture_end_unix']]
    assert before and not any(s['debugger_present'] for s in before)
    assert len(after)>=100 and not any(s['debugger_present'] for s in after)
    assert after[-1]['seconds']-after[0]['seconds']>=1
    record['live_cpu_after_detach_seconds'] = after[-1]['cpu_seconds']-after[0]['cpu_seconds']
    assert record['live_cpu_after_detach_seconds']>0
    assert not any(s['held'] for s in live['samples']), 'Unexpected held input'
    record['positive_hits'] = sum(h['rip']==0x3A1C50 for h in trace['hits'])
    assert record['positive_hits']>0, 'Missing known-entry positive'
    record['hits_by_rip'] = {addr:sum(h['rip']==int(addr,16) for h in trace['hits']) for addr in addresses}
    record['status'] = 'QUALIFIED_WINDOW'
except BaseException as error:
    record['error'] = repr(error)
finally:
    if observer is not None and observer.poll() is None:
        observer.terminate()
        record['observer_terminated'] = True
        observer.wait(timeout=5)
    record['end_unix'] = time.time()
    with (out/'run.json').open('x', encoding='utf-8') as f:
        json.dump(record, f, indent=2)
        f.write('\n')
print(json.dumps({k:record.get(k) for k in ['status','error','hits_by_rip','live_cpu_after_detach_seconds']}))
raise SystemExit(0 if record['status']=='QUALIFIED_WINDOW' else 1)
