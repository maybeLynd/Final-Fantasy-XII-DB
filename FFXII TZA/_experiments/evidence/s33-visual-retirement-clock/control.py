"""Real proof CLI prerequisite failures, with a required valid positive receipt."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
status=json.loads((P/'proof-03.status.json').read_text())
positive=json.loads((P/'result-03.json').read_text())
if status.get('exit')!=0 or status.get('terminal') is not True or status.get('exception') is not None or status['driver_sha256']!=sha(P/'prove.py') or not(P/'proof-03.stdout').read_bytes() or(P/'proof-03.stderr').read_bytes() or positive.get('producer_complete') is not True or positive['instruction_assertions']!=75 or len(positive['graphs'])!=5:
    raise RuntimeError('valid positive proof missing/incomplete')
W=P/'proof-controls-01';W.mkdir(exist_ok=False)
cases=[]
for label in ['failed-capture','missing-source','zero-bodies']:
    d=W/label;d.mkdir()
    for name in ['capture.py','capture-01.status.json','capture-01.stdout','capture-01.stderr','source-01.json']:
        shutil.copyfile(P/name,d/name)
    if label=='failed-capture':
        changed='capture-01.status.json';v=json.loads((d/changed).read_text());v['exit']=1
        (d/changed).write_text(json.dumps(v,indent=2)+'\n');expected='RuntimeError: upstream capture failed/incomplete'
    elif label=='missing-source':
        changed='source-01.json';(d/changed).unlink();expected='FileNotFoundError:'
    else:
        changed='source-01.json';v=json.loads((d/changed).read_text());v['ranges']=[]
        (d/changed).write_text(json.dumps(v,indent=2)+'\n');expected='ValueError: missing/zero original ranges'
    out=d/'result.json';argv=[sys.executable,'-B',str(P/'prove.py'),str(out),'--src',str(d)]
    run=subprocess.run(argv,stdin=subprocess.DEVNULL,capture_output=True,timeout=20)
    (d/'stdout').write_bytes(run.stdout);(d/'stderr').write_bytes(run.stderr)
    diagnostic=run.stderr.decode(errors='replace').splitlines()[-1] if run.stderr else ''
    matched=diagnostic==expected if label!='missing-source' else diagnostic.startswith(expected) and 'source-01.json' in diagnostic
    row={'case':label,'argv':argv,'exit':run.returncode,'terminal':True,'exception':None,'diagnostic':diagnostic,'expected_error':expected,'expected_error_seen':matched,'stdout_empty':not run.stdout,'result_absent':not out.exists(),'changed_file':changed,'changed_sha256':sha(d/changed) if(d/changed).exists() else None,'inherited_from_baseline':{name:sha(P/name) for name in ['capture.py','capture-01.status.json','capture-01.stdout','capture-01.stderr','source-01.json'] if name!=changed},'producer_sha256':sha(P/'prove.py'),'control_sha256':sha(Path(__file__))}
    row['passed']=run.returncode!=0 and matched and row['stdout_empty'] and row['result_absent']
    (d/'receipt.json').write_text(json.dumps(row,indent=2)+'\n');cases.append(row)
complete=len(cases)==3 and all(c['passed'] for c in cases)
(W/'result.json').write_text(json.dumps({'complete':complete,'status':'THREE_ACTUAL_PROOF_PREREQUISITE_REFUSALS' if complete else'INVALID_CONTROL','cases':cases,'limits':'Host admission controls, not original-code/native/game executions. The required positive is the retained terminal proof-03.'},indent=2)+'\n')
print(json.dumps({'complete':complete,'cases':[{'case':r['case'],'passed':r['passed'],'diagnostic':r['diagnostic']} for r in cases]}))
raise SystemExit(0 if complete else 1)
