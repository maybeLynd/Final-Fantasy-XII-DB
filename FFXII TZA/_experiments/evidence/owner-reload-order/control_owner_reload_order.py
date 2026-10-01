"""Exercise the actual reducer CLI's source and upstream failure gates."""
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
    files=['validate-title-source-annotations.py','capture-owner-reload-order.py','capture-owner-reload-gate.py']
    for prefix in ['owner-reload-order','owner-reload-gate']:
        files.append(prefix+'-source-01.json')
        files.extend(prefix+'-capture-01'+suffix for suffix in ['.status.json','.stdout','.stderr'])
    for tag,message in [('failed-capture','required capture failed/stale'),
                        ('missing-definition','required range population missing/changed'),
                        ('changed-group-branch','original byte mismatch'),
                        ('missing-retained-source','No such file')]:
        case=out/tag;case.mkdir()
        for file in files:shutil.copy2(HERE/file,case/file)
        upstream=None
        if tag=='failed-capture':
            p=case/'owner-reload-order-capture-01.status.json';v=json.loads(p.read_text());v['exit']=1;p.write_text(json.dumps(v,indent=2)+'\n')
        elif tag=='missing-definition':
            p=case/'owner-reload-order-source-01.json';v=json.loads(p.read_text())
            v['ranges']=[r for r in v['ranges'] if r['start']!='0x32f850'];p.write_text(json.dumps(v,indent=2)+'\n')
        elif tag=='changed-group-branch':
            p=case/'owner-reload-order-source-01.json';v=json.loads(p.read_text())
            for r in v['ranges']:
                for i in r['instructions']:
                    if i['pc']=='0x2628ee':
                        blob=bytearray.fromhex(i['bytes']);blob[0]^=1;i['bytes']=blob.hex();i['mnemonic']='jne'
                r['sha256']=hashlib.sha256(bytes.fromhex(''.join(i['bytes'] for i in r['instructions']))).hexdigest()
            p.write_text(json.dumps(v,indent=2)+'\n')
        else:
            upstream=case/'missing-retained';upstream.mkdir()
            shutil.copy2(ROOT/'Database/FFXII TZA/_experiments/evidence/bts-index-binding/manifest.json',upstream/'manifest.json')
        result=case/'result.json';args=[sys.executable,str(HERE/'prove_owner_reload_order.py'),str(result),str(case)]
        if upstream:args.append(str(upstream))
        p=subprocess.run(args,capture_output=True,timeout=30)
        (case/'stdout').write_bytes(p.stdout);(case/'stderr').write_bytes(p.stderr)
        good=p.returncode!=0 and message in p.stderr.decode(errors='replace') and not result.exists()
        cases.append(dict(tag=tag,command=args,exit=p.returncode,expected_refusal=message,
                          refusal_seen=message in p.stderr.decode(errors='replace'),result_absent=not result.exists(),passed=good))
        if not good:raise AssertionError('required actual refusal failed '+tag)
    (out/'result.json').write_text(json.dumps(dict(status='PASS_ACTUAL_RELOAD_PREREQUISITE_REFUSALS',
      driver_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),cases=cases),indent=2)+'\n')
    print('PASS_ACTUAL_RELOAD_PREREQUISITE_REFUSALS:4; no native/game')


if __name__=='__main__':main(Path(sys.argv[1]))
