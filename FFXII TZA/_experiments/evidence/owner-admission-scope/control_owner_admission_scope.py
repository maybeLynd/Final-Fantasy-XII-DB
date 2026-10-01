"""Actual scope reducer CLI refusals; no canonical producer edits."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys

HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'Database').is_dir())


def main(out):
    if out.exists():raise ValueError('immutable controls directory exists')
    out.mkdir();cases=[]
    files=['capture-owner-admission.py','owner-admission-source-01.json','validate-title-source-annotations.py',
           'owner-uniqueness-delivery-source-01.py']
    for prefix in ['owner-admission-capture-01','owner-uniqueness-existing-check-01']:
        files.extend(prefix+s for s in ['.status.json','.stdout','.stderr'])
    for tag,message in [('failed-capture','required admission capture failed/stale'),
                        ('changed-armer','retained boundary/hash changed'),
                        ('missing-reset','No such file'),
                        ('failed-original-O','original O control failed/stale')]:
        case=out/tag;case.mkdir()
        for name in files:shutil.copy2(HERE/name,case/name)
        upstream=None
        if tag in ['failed-capture','failed-original-O']:
            name='owner-admission-capture-01.status.json' if tag=='failed-capture' else 'owner-uniqueness-existing-check-01.status.json'
            p=case/name;v=json.loads(p.read_text());v['exit']=1;p.write_text(json.dumps(v,indent=2)+'\n')
        elif tag=='changed-armer':
            p=case/'owner-admission-source-01.json';v=json.loads(p.read_text())
            for r in v['ranges']:
                for i in r['instructions']:
                    if i['pc']=='0x3dda40':
                        b=bytearray.fromhex(i['bytes']);b[0]^=1;i['bytes']=b.hex();i['mnemonic']='je'
                r['sha256']=hashlib.sha256(bytes.fromhex(''.join(i['bytes'] for i in r['instructions']))).hexdigest()
            p.write_text(json.dumps(v,indent=2)+'\n')
        else:
            upstream=case/'missing-reset';upstream.mkdir()
            shutil.copy2(ROOT/'Database/FFXII TZA/_experiments/evidence/owner-reset-barrier/qualified-02/manifest.json',upstream/'manifest.json')
        result=case/'result.json';args=[sys.executable,str(HERE/'prove_owner_admission_scope.py'),str(result),str(case)]
        if upstream:args.append(str(upstream))
        r=subprocess.run(args,capture_output=True,timeout=30)
        (case/'stdout').write_bytes(r.stdout);(case/'stderr').write_bytes(r.stderr)
        good=r.returncode!=0 and message in r.stderr.decode(errors='replace') and not result.exists()
        cases.append(dict(tag=tag,command=args,exit=r.returncode,expected_refusal=message,
                          refusal_seen=message in r.stderr.decode(errors='replace'),result_absent=not result.exists(),passed=good))
        if not good:raise AssertionError('actual refusal failed '+tag)
    (out/'result.json').write_text(json.dumps(dict(status='PASS_ACTUAL_ADMISSION_SCOPE_REFUSALS',
      checker_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),cases=cases),indent=2)+'\n')
    print('PASS_ACTUAL_ADMISSION_SCOPE_REFUSALS:4; producer O cannot hide upstream failure')


if __name__=='__main__':main(Path(sys.argv[1]))
