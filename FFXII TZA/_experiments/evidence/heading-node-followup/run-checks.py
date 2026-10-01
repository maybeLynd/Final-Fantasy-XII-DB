"""Retain the real gate exit and three focused refusal controls."""
import hashlib, json, shutil, subprocess, sys
from pathlib import Path

sys.dont_write_bytecode=True
W=Path(__file__).resolve().parent
cases=W/'preflight-cases';receipt=W/'checks-terminal.json'
assert not cases.exists() and not receipt.exists(), 'Prior gate evidence must remain immutable'
cases.mkdir()
names=('check.py','tool-identity.json','result.json','node-67-reader-source.py',
       'node-67-reader-result.json','node-67-002F2530.bin','node-67-004607C0.bin',
       'oscillator-gate-source.py','oscillator-gate-result.json','oscillator-gate-0052BBD0.bin',
       'node-followup-terminal.json')
records=[]
def run(label,root):
    argv=[sys.executable,'-B',str(root/'check.py')]
    p=subprocess.run(argv,capture_output=True,text=True)
    records.append({'case':label,'argv':argv,'returncode':p.returncode,
                    'stdout':p.stdout,'stderr':p.stderr,'terminal':True,
                    'checker_sha256':hashlib.sha256((root/'check.py').read_bytes()).hexdigest()})
run('positive',W)
assert records[-1]['returncode']==0 and not records[-1]['stderr']
for label in ('failed-upstream','changed-original-bytes','fictional-live-claim'):
    root=cases/label;root.mkdir();(root/'retained').mkdir()
    for name in names:shutil.copy2(W/name,root/name)
    shutil.copy2(W/'retained/the-per-model-oscillator-subsystem.md',root/'retained/the-per-model-oscillator-subsystem.md')
    if label=='failed-upstream':
        p=root/'node-followup-terminal.json';x=json.loads(p.read_bytes());x[0]['returncode']=1
        p.write_text(json.dumps(x,indent=2)+'\n')
    elif label=='changed-original-bytes':
        p=root/'node-67-004607C0.bin';b=bytearray(p.read_bytes());b[0]^=1;p.write_bytes(b)
    else:
        p=root/'result.json';x=json.loads(p.read_bytes());x['live_observation']=True
        p.write_text(json.dumps(x,indent=2)+'\n')
    run(label,root)
    assert records[-1]['returncode']!=0 and records[-1]['stderr'],label
receipt.write_text(json.dumps(records,indent=2)+'\n')
print('NODE_FOLLOWUP_GATE_POSITIVE_THREE_REFUSALS',len(records))
