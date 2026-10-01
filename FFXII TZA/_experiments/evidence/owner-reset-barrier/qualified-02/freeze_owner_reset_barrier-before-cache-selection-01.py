"""Explicit immutable source/control receipts; no board or peer mutations."""
import hashlib
import json
from pathlib import Path
import shutil

HERE=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    for prefix,driver in [('owner-reset-barrier-capture-01','capture-owner-reset-barrier.py'),
                          ('owner-reset-barrier-positive-04','prove_owner_reset_barrier.py'),
                          ('owner-reset-barrier-controls-run-01','control_owner_reset_barrier.py')]:
        s=json.loads((HERE/(prefix+'.status.json')).read_text())
        if s['exit']!=0 or s['driver_sha256']!=sha(HERE/driver):raise ValueError('upstream failed/stale')
        if not(HERE/(prefix+'.stdout')).read_bytes().strip() or (HERE/(prefix+'.stderr')).read_bytes():raise ValueError('upstream output missing/error')
    result=json.loads((HERE/'owner-reset-barrier-result-04.json').read_text())
    controls=json.loads((HERE/'owner-reset-barrier-controls-01/result.json').read_text())
    if result['driver_sha256']!=sha(HERE/'prove_owner_reset_barrier.py') or len(result['fst_dependency']['members'])!=12:raise ValueError('scientific result incomplete')
    if controls['status']!='PASS_ACTUAL_OWNER_RESET_PREREQUISITE_REFUSALS' or len(controls['cases'])!=4 or not all(x['passed'] for x in controls['cases']):raise ValueError('actual controls incomplete')
    files=['capture-owner-reset-barrier.py','prove_owner_reset_barrier.py','control_owner_reset_barrier.py',
           'freeze_owner_reset_barrier.py','validate-title-source-annotations.py','OWNER-RESET-METHOD-1001.md']
    files += [p.relative_to(HERE).as_posix() for p in HERE.glob('prove_owner_reset_barrier-before-*.py')]
    files += [p.relative_to(HERE).as_posix() for p in HERE.glob('owner-reset-barrier-*') if p.is_file()]
    files += [p.relative_to(HERE).as_posix() for p in (HERE/'owner-reset-barrier-controls-01').rglob('*') if p.is_file()]
    out=HERE/'owner-reset-barrier-frozen-ready'
    if out.exists():raise ValueError('immutable packet exists')
    out.mkdir()
    for file in sorted(set(files)):
        dst=out/file;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(HERE/file,dst)
    shutil.copy2(HERE/'OWNER-RESET-README-1001.md',out/'README.md')
    (out/'.gitattributes').write_text('* -text\n')
    members=[dict(path=p.relative_to(out).as_posix(),sha256=sha(p),bytes=p.stat().st_size)
             for p in sorted(out.rglob('*')) if p.is_file()]
    (out/'manifest.json').write_text(json.dumps(dict(kind='conditional original owner-reset barrier',members=members),indent=2)+'\n')
    print(json.dumps(dict(members=len(members),manifest_sha256=sha(out/'manifest.json'))))


if __name__=='__main__':main()
