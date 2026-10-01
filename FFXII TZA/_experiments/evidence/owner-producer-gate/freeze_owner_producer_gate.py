"""Freeze only explicitly selected scientific files after checked prerequisites."""
import hashlib
import json
from pathlib import Path
import shutil

HERE=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    out=HERE/'owner-producer-gate-frozen-ready'
    if out.exists():raise ValueError('immutable packet exists')
    receipts=[('owner-producer-gate-source-run-01','qualify_owner_producer_gate_source.py'),
              ('owner-producer-gate-positive-01','prove_owner_producer_gate.py'),
              ('owner-producer-gate-controls-run-01','control_owner_producer_gate.py')]
    for prefix,driver in receipts:
        s=json.loads((HERE/(prefix+'.status.json')).read_text())
        if s['exit']!=0 or s['driver_sha256']!=sha(HERE/driver):raise ValueError('required upstream failed/stale')
        if not(HERE/(prefix+'.stdout')).read_bytes().strip() or (HERE/(prefix+'.stderr')).read_bytes():raise ValueError('upstream missing/error output')
    r=json.loads((HERE/'owner-producer-gate-result-01.json').read_text())
    c=json.loads((HERE/'owner-producer-gate-controls-01/result.json').read_text())
    if r['driver_sha256']!=sha(HERE/'prove_owner_producer_gate.py') or len(r['graphs'])!=4 or r.get('producer_complete') is not True:raise ValueError('positive incomplete')
    if c['driver_sha256']!=sha(HERE/'control_owner_producer_gate.py') or len(c['cases'])!=4 or not all(x['passed'] for x in c['cases']):raise ValueError('controls incomplete')
    files=['qualify_owner_producer_gate_source.py','prove_owner_producer_gate.py',
           'control_owner_producer_gate.py','freeze_owner_producer_gate.py',
           'validate-title-source-annotations.py','prove_owner_reload_order.py',
           'owner-producer-gate-source-01.json','owner-producer-gate-result-01.json',
           'OWNER-PRODUCER-GATE-METHOD-1001.md']
    files.extend(prefix+s for prefix,_ in receipts for s in ['.status.json','.stdout','.stderr'])
    files.extend(p.relative_to(HERE).as_posix() for p in (HERE/'owner-producer-gate-controls-01').rglob('*')
                 if p.is_file() and '__pycache__' not in p.parts and p.suffix not in ['.pyc','.pyo'])
    if any('__pycache__' in Path(n).parts or Path(n).suffix in ['.pyc','.pyo'] for n in files):raise ValueError('generated cache in scientific selection')
    out.mkdir()
    for name in sorted(set(files)):
        p=out/name;p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(HERE/name,p)
    shutil.copy2(HERE/'OWNER-PRODUCER-GATE-README-1001.md',out/'README.md')
    (out/'.gitattributes').write_text('* -text\n')
    members=[dict(path=p.relative_to(out).as_posix(),sha256=sha(p),bytes=p.stat().st_size)
             for p in sorted(out.rglob('*')) if p.is_file()]
    (out/'manifest.json').write_text(json.dumps(dict(kind='local original owner producer gate',members=members),indent=2)+'\n')
    print(json.dumps(dict(members=len(members),manifest_sha256=sha(out/'manifest.json'))))


if __name__=='__main__':main()
