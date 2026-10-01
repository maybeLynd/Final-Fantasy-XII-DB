"""Real reducer CLI refusals; inherited baseline + exact changed inputs retained."""
import copy
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
sys.dont_write_bytecode = True
P = Path(__file__).resolve().parent
W = P / 'controls-02'
W.mkdir(exist_ok=False)
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
positive = json.loads((P/'proof-01.status.json').read_text())
result = json.loads((P/'result-01.json').read_text())
if positive.get('exit') != 0 or positive.get('terminal') is not True or positive.get('exception') is not None or positive['driver_sha256'] != sha(P/'prove.py') or result.get('producer_complete') is not True or result['finite_classification']['partitions'] != 33930:
    raise RuntimeError('required positive producer control failed/incomplete')
diagnostics = {'failed-upstream':'RuntimeError: required capture failed/incomplete',
               'missing-terminal':'ValueError: empty/mixed original bytes',
               'changed-stem-subtract':'RuntimeError: original full body identity changed/incomplete',
               'wrong-store-role':'ValueError: memory/address/access annotation disagrees at 0x377f12'}
baseline = ['capture.py','source-01.json','capture-01.status.json','capture-01.stdout','capture-01.stderr']
cases = []
for label in ('failed-upstream','missing-terminal','changed-stem-subtract','wrong-store-role'):
    directory = W / label
    directory.mkdir()
    for name in baseline: shutil.copyfile(P / name, directory / name)
    if label == 'failed-upstream':
        changed = 'capture-01.status.json'
        value = json.loads((directory / changed).read_text());value['exit']=1
    else:
        changed = 'source-01.json'
        value = json.loads((directory / changed).read_text())
        r = value['ranges'][0]
        if label == 'missing-terminal':
            r['instructions'] = r['instructions'][:-1]
        elif label == 'changed-stem-subtract':
            i = next(i for i in r['instructions'] if i['pc'] == '0x377e83')
            if i['bytes'] != '83ef05': raise RuntimeError('control preimage changed')
            i['bytes']='83ef04';i['args']='edi, 4'
            r['sha256']=hashlib.sha256(bytes.fromhex(''.join(i['bytes'] for i in r['instructions']))).hexdigest()
        else:
            i = next(i for i in r['instructions'] if i['pc'] == '0x377f12')
            if i['memory'][0]['role'] != 'w': raise RuntimeError('control role preimage changed')
            i['memory'][0]['role']='r'
    (directory / changed).write_text(json.dumps(value,indent=2)+'\n')
    out = directory / 'result.json'
    argv = [sys.executable,'-B',str(P/'prove.py'),str(out),'--src',str(directory)]
    p = subprocess.run(argv,stdin=subprocess.DEVNULL,capture_output=True,timeout=20)
    (directory/'stdout').write_bytes(p.stdout);(directory/'stderr').write_bytes(p.stderr)
    record = {'case':label,'argv':argv,'terminal':True,'exit':p.returncode,'exception':None,'result_absent':not out.exists(),
       'diagnostic':p.stderr.decode('utf-8','replace').splitlines()[-1] if p.stderr else '',
       'changed_file':changed,'changed_sha256':sha(directory/changed),
       'inherited_from_baseline':{name:sha(P/name) for name in baseline if name!=changed},
       'producer_sha256':sha(P/'prove.py'),'control_sha256':sha(Path(__file__))}
    record['expected_diagnostic']=diagnostics[label]
    record['passed']=p.returncode!=0 and record['result_absent'] and not p.stdout and record['diagnostic']==record['expected_diagnostic']
    (directory/'receipt.json').write_text(json.dumps(record,indent=2)+'\n')
    cases.append(record)
complete = len(cases)==4 and all(c['passed'] for c in cases)
result={'status':'FOUR_ACTUAL_PREREQUISITE_REFUSALS' if complete else 'INVALID','complete':complete,'cases':cases,
 'limits':'Source/observer integrity and checked upstream controls; mutated bytes are synthetic inputs, not modified shipping behavior or semantic executions.'}
(W/'result.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':result['status'],'cases':[{'case':c['case'],'passed':c['passed'],'diagnostic':c['diagnostic']} for c in cases]}))
raise SystemExit(0 if complete else 1)
