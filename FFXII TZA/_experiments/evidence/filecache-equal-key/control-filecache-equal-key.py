"""Actual reducer CLI refusals; losslessly qualified input deltas, no live tests."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
W=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
BASE=['capture-filecache-equal-key.py','capture-index-path.py','validate-title-source-annotations.py',
      'prove_owner_reload_order.py','filecache-equal-key-source-01.json',
      'filecache-equal-key-capture-01.status.json','filecache-equal-key-capture-01.stdout',
      'filecache-equal-key-capture-01.stderr']
def main():
    out=W/'filecache-equal-key-controls-01'
    if out.exists():raise ValueError('immutable controls exist')
    out.mkdir();cases=[]
    defs=[('upstream-failed','filecache-equal-key-capture-01.status.json','upstream capture failed'),
          ('incomplete-body','filecache-equal-key-source-01.json','required original body population/identity incomplete'),
          ('changed-key-move','filecache-equal-key-source-01.json','required original body population/identity incomplete'),
          ('wrong-release-import','filecache-equal-key-source-01.json','release import declaration mismatch')]
    for tag,changed,error in defs:
        folder=out/tag;folder.mkdir()
        for name in BASE:shutil.copy2(W/name,folder/name)
        p=folder/changed;v=json.loads(p.read_text())
        if tag=='upstream-failed':v['exit']=1
        elif tag=='incomplete-body':
            q=v['ranges'][0];q['instructions']=q['instructions'][:-1]
            blob=bytes.fromhex(''.join(i['bytes'] for i in q['instructions']))
            q['end_exclusive']=hex(int(q['start'],16)+len(blob));q['sha256']=hashlib.sha256(blob).hexdigest()
        elif tag=='changed-key-move':
            q=v['ranges'][0];i=next(i for i in q['instructions'] if i['pc']=='0x1d6a51')
            i.update(bytes='8bd1',args='edx, ecx') # coherent MOV, not a broken annotation control
            q['sha256']=hashlib.sha256(bytes.fromhex(''.join(i['bytes'] for i in q['instructions']))).hexdigest()
        elif tag=='wrong-release-import':v['static_release_imports'][0]['name']='realloc'
        p.write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8')
        dest=folder/'result.json';cmd=[sys.executable,str(W/'prove-filecache-equal-key.py'),'--source',str(folder),'--out',str(dest)]
        r=subprocess.run(cmd,cwd=W,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=30)
        (folder/'stdout').write_bytes(r.stdout);(folder/'stderr').write_bytes(r.stderr)
        passed=r.returncode!=0 and error in r.stderr.decode('utf-8',errors='replace') and not dest.exists()
        receipt=dict(tag=tag,command=cmd,terminal=True,exit=r.returncode,expected_error=error,passed=passed,result_absent=not dest.exists(),
            changed_file=changed,changed_sha256=sha(p),inherited_from_baseline={n:sha(folder/n) for n in BASE if n!=changed},
            producer_sha256=sha(W/'prove-filecache-equal-key.py'))
        (folder/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
        cases.append(receipt)
    result=dict(status='PASS_FOUR_ACTUAL_REFUSALS' if all(x['passed'] for x in cases) else 'INVALID_CONTROLS',complete=all(x['passed'] for x in cases),cases=cases,driver_sha256=sha(Path(__file__)),producer_sha256=sha(W/'prove-filecache-equal-key.py'))
    (out/'result.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(result['status'],len(cases))
    if not result['complete']:raise ValueError('actual controls incomplete/failed')
if __name__=='__main__':main()
