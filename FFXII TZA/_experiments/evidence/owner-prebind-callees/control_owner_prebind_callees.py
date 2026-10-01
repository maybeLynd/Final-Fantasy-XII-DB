"""Required refusal controls on the real reducer CLI, not a helper-only check."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys

HERE=Path(__file__).resolve().parent


def main(out):
    if out.exists():raise ValueError('immutable controls directory exists')
    out.mkdir();cases=[]
    files=['validate-title-source-annotations.py','qualify_owner_prebind_source.py','owner-prebind-source-01.json']
    files.append('owner-prebind-bounds-premise-01.json')
    files.extend('owner-prebind-source-run-01'+suffix for suffix in ['.status.json','.stdout','.stderr'])
    for tag,message in [('failed-qualifier','required qualifier failed/stale'),
                        ('changed-flag-leaf','original byte mismatch'),
                        ('missing-tail-body','required range population missing/changed'),
                        ('broadened-depth-premise','required valid-context bounds premise changed')]:
        case=out/tag;case.mkdir()
        for file in files:shutil.copy2(HERE/file,case/file)
        if tag=='failed-qualifier':
            p=case/'owner-prebind-source-run-01.status.json';v=json.loads(p.read_text());v['exit']=1;p.write_text(json.dumps(v,indent=2)+'\n')
        else:
            p=case/'owner-prebind-source-01.json';v=json.loads(p.read_text())
            if tag=='changed-flag-leaf':
                for r in v['ranges']:
                    for i in r['instructions']:
                        if i['pc']=='0x36b208':
                            blob=bytearray.fromhex(i['bytes']);blob[1]=0xbb;i['bytes']=blob.hex();i['mnemonic']='btc'
                    r['sha256']=hashlib.sha256(bytes.fromhex(''.join(i['bytes'] for i in r['instructions']))).hexdigest()
            elif tag=='missing-tail-body':v['ranges']=[r for r in v['ranges'] if r['start']!='0x36c1f0']
            else:
                premise=case/'owner-prebind-bounds-premise-01.json'
                bounds=json.loads(premise.read_text());bounds['depth_max']=31
                premise.write_text(json.dumps(bounds,indent=2)+'\n')
            p.write_text(json.dumps(v,indent=2)+'\n')
        result=case/'result.json';argv=[sys.executable,str(HERE/'prove_owner_prebind_callees.py'),str(result),str(case)]
        r=subprocess.run(argv,capture_output=True,timeout=30)
        (case/'stdout').write_bytes(r.stdout);(case/'stderr').write_bytes(r.stderr)
        good=r.returncode!=0 and message in r.stderr.decode(errors='replace') and not result.exists()
        cases.append(dict(tag=tag,argv=argv,exit=r.returncode,expected_refusal=message,
                          refusal_seen=message in r.stderr.decode(errors='replace'),result_absent=not result.exists(),passed=good))
        if not good:raise AssertionError('required actual refusal failed '+tag)
    (out/'result.json').write_text(json.dumps(dict(status='PASS_ACTUAL_PREBIND_PREREQUISITE_REFUSALS',
      driver_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),cases=cases),indent=2)+'\n')
    print('PASS_ACTUAL_PREBIND_PREREQUISITE_REFUSALS:4; static/algebraic scope only; native/game0')


if __name__=='__main__':main(Path(sys.argv[1]))
