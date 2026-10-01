"""Two actual retained-input admission refusals; no repeated capture/native tests."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent;W=P/'controls-01';W.mkdir(exist_ok=False)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
s=json.loads((P/'proof-01.status.json').read_text());r=json.loads((P/'result-01.json').read_text())
if s.get('exit')!=0 or s.get('terminal') is not True or s.get('exception') is not None or s['driver_sha256']!=sha(P/'prove.py') or not r['producer_complete'] or r['instruction_assertions']!=29 or len(r['symbolic_partitions'])!=3:raise RuntimeError('positive proof prerequisite invalid/incomplete')
cases=[]
for label in ['mixed-parent','missing-source']:
    directory=W/label;retained=directory/'retained';shutil.copytree(P/'retained',retained)
    if label=='mixed-parent':
        changed='retained/parent-manifest.json';value=json.loads((directory/changed).read_text());value['package']='synthetic-other-generation';(directory/changed).write_text(json.dumps(value,indent=2)+'\n')
        expected='RuntimeError: retained parent manifest identity failed'
    else:
        changed='retained/source-01.json';(directory/changed).unlink();expected='FileNotFoundError'
    out=directory/'result.json';argv=[sys.executable,'-B',str(P/'prove.py'),str(out),'--src',str(directory)]
    p=subprocess.run(argv,stdin=subprocess.DEVNULL,capture_output=True,timeout=20)
    (directory/'stdout').write_bytes(p.stdout);(directory/'stderr').write_bytes(p.stderr)
    diagnostic=p.stderr.decode('utf-8','replace').splitlines()[-1] if p.stderr else ''
    record={'case':label,'argv':argv,'exit':p.returncode,'terminal':True,'exception':None,'result_absent':not out.exists(),'stdout_empty':not p.stdout,
      'expected_error':expected,'diagnostic':diagnostic,'expected_error_seen':diagnostic==expected if label=='mixed-parent' else expected in diagnostic,
      'changed_file':changed,'changed_sha256':sha(directory/changed) if (directory/changed).exists() else None,
      'inherited_from_baseline':{('retained/'+f.name):sha(f) for f in (P/'retained').iterdir() if 'retained/'+f.name!=changed},'producer_sha256':sha(P/'prove.py'),'control_sha256':sha(Path(__file__))}
    record['passed']=record['exit']!=0 and record['terminal'] and record['result_absent'] and record['stdout_empty'] and record['expected_error_seen']
    (directory/'receipt.json').write_text(json.dumps(record,indent=2)+'\n');cases.append(record)
complete=len(cases)==2 and all(c['passed'] for c in cases)
(W/'result.json').write_text(json.dumps({'complete':complete,'status':'TWO_ACTUAL_RETAINED_ADMISSION_REFUSALS' if complete else 'INVALID','cases':cases,'limits':'Mixed/missing retained evidence detection, not semantic machine-code mutations/executions.'},indent=2)+'\n')
print(json.dumps({'status':'TWO_ACTUAL_RETAINED_ADMISSION_REFUSALS' if complete else 'INVALID','cases':[{'case':c['case'],'passed':c['passed'],'diagnostic':c['diagnostic']} for c in cases]}))
raise SystemExit(0 if complete else 1)
