"""Focused actual proof-CLI prerequisite refusals; own isolated inputs only."""
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
    out.mkdir()
    files=['capture-owner-reset-barrier.py','owner-reset-barrier-source-01.json',
           'owner-reset-barrier-capture-01.status.json','owner-reset-barrier-capture-01.stdout',
           'owner-reset-barrier-capture-01.stderr','validate-title-source-annotations.py']
    result=dict(status='INVALID',cases=[],driver_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    for tag,message in [('failed-capture','required original capture failed/stale'),
                        ('missing-wait','original operation changed'),
                        ('changed-branch','original byte mismatch'),
                        ('missing-retained-fst','No such file')]:
        case=out/tag;case.mkdir()
        for name in files:shutil.copy2(HERE/name,case/name)
        upstream=None
        if tag=='failed-capture':
            path=case/'owner-reset-barrier-capture-01.status.json'
            data=json.loads(path.read_text());data['exit']=1;path.write_text(json.dumps(data,indent=2)+'\n')
        elif tag=='missing-wait':
            path=case/'owner-reset-barrier-source-01.json'
            data=json.loads(path.read_text());data['ranges']=[r for r in data['ranges'] if r['start']!='0x32e520'];path.write_text(json.dumps(data,indent=2)+'\n')
        elif tag=='changed-branch':
            path=case/'owner-reset-barrier-source-01.json';data=json.loads(path.read_text())
            for r in data['ranges']:
                for i in r['instructions']:
                    if i['pc']=='0x32f625':
                        b=bytearray.fromhex(i['bytes']);b[0]^=1;i['bytes']=b.hex();i['mnemonic']='jg'
                r['sha256']=hashlib.sha256(bytes.fromhex(''.join(i['bytes'] for i in r['instructions']))).hexdigest()
            path.write_text(json.dumps(data,indent=2)+'\n')
        else:
            upstream=case/'missing-upstream';upstream.mkdir()
            shutil.copy2(ROOT/'Database/FFXII TZA/_experiments/evidence/bts-index-binding/manifest.json',upstream/'manifest.json')
        output=case/'result.json'
        args=[sys.executable,str(HERE/'prove_owner_reset_barrier.py'),str(output),str(case)]
        if upstream:args.append(str(upstream))
        p=subprocess.run(args,capture_output=True,text=True,timeout=30)
        (case/'stdout').write_text(p.stdout);(case/'stderr').write_text(p.stderr)
        passed=p.returncode!=0 and message in p.stderr and not output.exists()
        result['cases'].append(dict(tag=tag,command=args,exit=p.returncode,expected_refusal=message,
                                     refusal_seen=message in p.stderr,result_absent=not output.exists(),passed=passed))
        if not passed:raise AssertionError('actual refusal missing '+tag)
    result['status']='PASS_ACTUAL_OWNER_RESET_PREREQUISITE_REFUSALS'
    (out/'result.json').write_text(json.dumps(result,indent=2)+'\n')
    print(result['status'])


if __name__=='__main__':main(Path(sys.argv[1]))
