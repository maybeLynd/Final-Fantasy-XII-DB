"""Freeze source result and lossless control deltas after actual CLI checks."""
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil

W=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    out=W/'filecache-key-preprocessing-frozen-ready'
    if out.exists():raise ValueError('immutable packet exists')
    for prefix,driver in [('filecache-key-preprocessing-positive-02','prove-filecache-key-preprocessing.py'),
                          ('filecache-key-preprocessing-controls-run-01','control-filecache-key-preprocessing.py')]:
        s=json.loads((W/(prefix+'.status.json')).read_text())
        if s.get('exit')!=0 or s.get('terminal') is not True or s.get('driver_sha256')!=sha(W/driver):
            raise ValueError('required upstream failed/incomplete/stale')
        if not (W/(prefix+'.stdout')).read_bytes().strip() or (W/(prefix+'.stderr')).read_bytes():
            raise ValueError('required upstream output missing/error')
    r=json.loads((W/'filecache-key-preprocessing-result-02.json').read_text())
    if (r.get('producer_complete') is not True or r.get('driver_sha256')!=sha(W/'prove-filecache-key-preprocessing.py')
            or len(r['graphs'])!=6 or len(r['first_byte_classification'])!=256
            or len(r['illustrations'])!=7 or not r.get('source_pins')):
        raise ValueError('required source result incomplete')
    for name,pin in r['source_pins'].items():
        if sha(W/name)!=pin:raise ValueError('source preimage changed')
    c=json.loads((W/'filecache-key-preprocessing-controls-01/result.json').read_text())
    if (c.get('status')!='PASS_FOUR_ACTUAL_REFUSALS' or len(c['cases'])!=4 or
            not c.get('complete') or not all(x['passed'] for x in c['cases']) or
            c['producer_sha256']!=sha(W/'prove-filecache-key-preprocessing.py') or
            c['driver_sha256']!=sha(W/'control-filecache-key-preprocessing.py')):
        raise ValueError('required controls incomplete')
    spec=importlib.util.spec_from_file_location('existing_case_members',W/'control-filecache-key-preprocessing.py')
    M=importlib.util.module_from_spec(spec);spec.loader.exec_module(M)
    files=list(M.BASE)+['prove-filecache-key-preprocessing.py',
      'prove-filecache-key-preprocessing-before-immediate-encoding-01.py',
      'control-filecache-key-preprocessing.py','freeze-filecache-key-preprocessing.py',
      'filecache-key-preprocessing-result-02.json','FILECACHE-COLLISION-METHOD-1001.md',
      'filecache-key-preprocessing-controls-01/result.json']
    for prefix in ['filecache-key-preprocessing-positive-01','filecache-key-preprocessing-positive-02',
                   'filecache-key-preprocessing-controls-run-01']:
        files.extend(prefix+s for s in ['.status.json','.stdout','.stderr'])
    for case in c['cases']:
        base=Path('filecache-key-preprocessing-controls-01')/case['tag']
        for name,pin in case['inherited_from_baseline'].items():
            if sha(W/base/name)!=pin or pin!=sha(W/name):
                raise ValueError('control deduplication is not lossless')
        if sha(W/base/case['changed_file'])!=case['changed_sha256']:
            raise ValueError('control changed input moved')
        files.extend((base/name).as_posix() for name in [case['changed_file'],'stdout','stderr','receipt.json'])
    out.mkdir()
    for name in sorted(set(files)):
        p=out/name;p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(W/name,p)
    shutil.copy2(W/'FILECACHE-KEY-README-1001.md',out/'README.md')
    (out/'.gitattributes').write_text('* -text\n')
    members=[{'path':p.relative_to(out).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p)}
             for p in sorted(out.rglob('*')) if p.is_file()]
    (out/'manifest.json').write_text(json.dumps({'kind':'conditional original cache-key preprocessing','members':members},indent=2)+'\n')
    print(json.dumps({'members':len(members),'manifest_sha256':sha(out/'manifest.json')}))


if __name__=='__main__':main()
