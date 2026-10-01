"""Retain the actual A23 evidence gate and three consequential refusals."""
import hashlib,json,shutil,subprocess,sys
from pathlib import Path
sys.dont_write_bytecode=True
W=Path(__file__).resolve().parent
cases=W/'preflight-cases';receipt=W/'checks-terminal.json'
assert not cases.exists() and not receipt.exists(),'Prior gate evidence remains immutable'
cases.mkdir()
root_files=('check.py','capture.py','capture.json','capture-terminal.json',
            'verify-captured-generation.py','verify-result.json','verify-terminal.json',
            'source-identity.json','historical-export-terminal.json','verdict.json')
raw_names=('status-before.body','root.body','progress.body','overview.body','status-after.body')
retained_names=('MANIFEST.json','view-progress.json','view-overview.json','history.jsonl',
                'RELEASE-DASHBOARD-2026-09-29.md','ACCEPTANCE-MATRIX.md')
records=[]
def run(label,root):
    argv=[sys.executable,'-B',str(root/'check.py')]
    p=subprocess.run(argv,capture_output=True,text=True)
    records.append({'case':label,'argv':argv,'returncode':p.returncode,
                    'stdout':p.stdout,'stderr':p.stderr,'terminal':True,
                    'checker_sha256':hashlib.sha256((root/'check.py').read_bytes()).hexdigest()})
run('positive',W)
assert records[-1]['returncode']==0 and not records[-1]['stderr']
for label in ('failed-verifier','changed-served-view','fictional-a23-pass'):
    root=cases/label;root.mkdir();(root/'raw-http').mkdir();(root/'retained').mkdir()
    for name in root_files:shutil.copy2(W/name,root/name)
    for name in raw_names:shutil.copy2(W/'raw-http'/name,root/'raw-http'/name)
    for name in retained_names:shutil.copy2(W/'retained'/name,root/'retained'/name)
    if label=='failed-verifier':
        p=root/'verify-terminal.json';x=json.loads(p.read_bytes());x['returncode']=1
        p.write_text(json.dumps(x,indent=2)+'\n')
    elif label=='changed-served-view':
        p=root/'raw-http/progress.body';b=bytearray(p.read_bytes());b[-2]^=1;p.write_bytes(b)
    else:
        p=root/'verdict.json';x=json.loads(p.read_bytes());x['status']='PASS'
        p.write_text(json.dumps(x,indent=2)+'\n')
    run(label,root)
    assert records[-1]['returncode']!=0 and records[-1]['stderr'],label
receipt.write_text(json.dumps(records,indent=2)+'\n')
print('A23_GATE_POSITIVE_AND_THREE_REFUSALS',len(records))
