"""Immutable scope packet; failed controls retained without duplicate identical fixtures."""
import hashlib
import json
from pathlib import Path
import shutil

HERE=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    out=HERE/'owner-admission-scope-frozen-ready'
    if out.exists():raise ValueError('immutable packet exists')
    good=[('owner-admission-capture-01','capture-owner-admission.py'),
          ('owner-uniqueness-existing-check-01','owner-uniqueness-delivery-source-01.py'),
          ('owner-admission-positive-01','prove_owner_admission_scope.py'),
          ('owner-admission-controls-run-02','control_owner_admission_scope.py')]
    for prefix,driver in good:
        s=json.loads((HERE/(prefix+'.status.json')).read_text())
        if s['exit']!=0 or s['driver_sha256']!=sha(HERE/driver):raise ValueError('upstream failed/stale')
        if not(HERE/(prefix+'.stdout')).read_bytes().strip() or (HERE/(prefix+'.stderr')).read_bytes():raise ValueError('upstream missing/error output')
    bad=json.loads((HERE/'owner-admission-controls-run-01.status.json').read_text())
    if bad['exit']==0 or bad['driver_sha256']!=sha(HERE/'control_owner_admission_scope-before-refusal-order-01.py'):raise ValueError('failed control history changed')
    r=json.loads((HERE/'owner-admission-result-01.json').read_text())
    c=json.loads((HERE/'owner-admission-controls-02/result.json').read_text())
    if r['checker_sha256']!=sha(HERE/'prove_owner_admission_scope.py') or len(r['conditional_countermodels'])!=2:raise ValueError('scientific result incomplete')
    if c['checker_sha256']!=sha(HERE/'control_owner_admission_scope.py') or len(c['cases'])!=4 or not all(x['passed'] for x in c['cases']):raise ValueError('controls incomplete')
    files=['capture-owner-admission.py','prove_owner_admission_scope.py','control_owner_admission_scope.py',
           'control_owner_admission_scope-before-refusal-order-01.py','freeze_owner_admission_scope.py',
           'validate-title-source-annotations.py','owner-admission-source-01.json','owner-admission-result-01.json',
           'owner-uniqueness-delivery-source-01.py','OWNER-UNIQUENESS-METHOD-1001.md']
    files.extend(prefix+s for prefix,_ in good for s in ['.status.json','.stdout','.stderr'])
    files.extend('owner-admission-controls-run-01'+s for s in ['.status.json','.stdout','.stderr'])
    files.extend(p.relative_to(HERE).as_posix() for p in (HERE/'owner-admission-controls-02').rglob('*')
                 if p.is_file() and '__pycache__' not in p.parts and p.suffix not in ['.pyc','.pyo'])
    failure_map=[]
    for p in (HERE/'owner-admission-controls-01').rglob('*'):
        if not p.is_file() or '__pycache__' in p.parts or p.suffix in ['.pyc','.pyo']:continue
        rel=p.relative_to(HERE/'owner-admission-controls-01')
        target=HERE/'owner-admission-controls-02'/rel
        if p.name in ['stdout','stderr']:
            files.append(p.relative_to(HERE).as_posix());dest=p.relative_to(HERE).as_posix()
        else:
            if not target.is_file() or sha(p)!=sha(target):raise ValueError('failed fixture input differs; preserve separately')
            dest=target.relative_to(HERE).as_posix()
        failure_map.append(dict(original_path=p.relative_to(HERE).as_posix(),sha256=sha(p),retained_packet_path=dest))
    if not failure_map:raise ValueError('missing failure history')
    out.mkdir()
    for name in sorted(set(files)):
        p=out/name;p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(HERE/name,p)
    shutil.copy2(HERE/'OWNER-UNIQUENESS-README-1001.md',out/'README.md')
    (out/'FAILED-CONTROL-01-INPUT-MAP.json').write_text(json.dumps(dict(status='INCOMPLETE_FAILED_CONTROL_NOT_PASS',members=failure_map),indent=2)+'\n')
    (out/'.gitattributes').write_text('* -text\n')
    members=[dict(path=p.relative_to(out).as_posix(),sha256=sha(p),bytes=p.stat().st_size)
             for p in sorted(out.rglob('*')) if p.is_file()]
    (out/'manifest.json').write_text(json.dumps(dict(kind='conditional original owner admission scope',members=members),indent=2)+'\n')
    print(json.dumps(dict(members=len(members),manifest_sha256=sha(out/'manifest.json'))))


if __name__=='__main__':main()
