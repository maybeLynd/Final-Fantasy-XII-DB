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
    files=['validate-title-source-annotations.py','qualify_owner_fullpool_source.py','qualify_owner_queue_order_source.py','owner-fullpool-source-01.json']
    files.extend('owner-fullpool-source-run-01'+suffix for suffix in ['.status.json','.stdout','.stderr'])
    for tag,message in [('failed-qualifier','required qualifier failed/stale'),
                        ('changed-free-branch','original byte mismatch'),
                        ('missing-owner-caller','required range population missing/changed'),
                        ('changed-selection','required bounded selection changed')]:
        case=out/tag;case.mkdir()
        for file in files:shutil.copy2(HERE/file,case/file)
        if tag=='failed-qualifier':
            p=case/'owner-fullpool-source-run-01.status.json';v=json.loads(p.read_text());v['exit']=1;p.write_text(json.dumps(v,indent=2)+'\n')
        else:
            p=case/'owner-fullpool-source-01.json';v=json.loads(p.read_text())
            if tag=='changed-free-branch':
                for r in v['ranges']:
                    for i in r['instructions']:
                        if i['pc']=='0x32e8a0':
                            blob=bytearray.fromhex(i['bytes']);blob[0]=0x74;i['bytes']=blob.hex();i['mnemonic']='je'
                    r['sha256']=hashlib.sha256(bytes.fromhex(''.join(i['bytes'] for i in r['instructions']))).hexdigest()
            elif tag=='missing-owner-caller':v['ranges']=[r for r in v['ranges'] if r['start']!='0x3dda70']
            else:v['selected_entries']=[]
            p.write_text(json.dumps(v,indent=2)+'\n')
        result=case/'result.json';argv=[sys.executable,str(HERE/'prove_owner_fullpool_admission.py'),str(result),str(case)]
        r=subprocess.run(argv,capture_output=True,timeout=30)
        (case/'stdout').write_bytes(r.stdout);(case/'stderr').write_bytes(r.stderr)
        good=r.returncode!=0 and message in r.stderr.decode(errors='replace') and not result.exists()
        cases.append(dict(tag=tag,argv=argv,exit=r.returncode,expected_refusal=message,
                          refusal_seen=message in r.stderr.decode(errors='replace'),result_absent=not result.exists(),passed=good))
        if not good:raise AssertionError('required actual refusal failed '+tag)
    api=[]
    for tag,entries in [('zero-selection',[]),('duplicate-selection',[0x3dda70,0x3dda70])]:
        case=out/tag;case.mkdir();result=case/'source.json'
        code='import importlib.util; from pathlib import Path; s=importlib.util.spec_from_file_location("bounded_q",'+repr(str(HERE/'qualify_owner_queue_order_source.py'))+'); q=importlib.util.module_from_spec(s); s.loader.exec_module(q); q.main(Path('+repr(str(result))+'),q.UP,entries='+repr(entries)+',include_pump_table=False)'
        argv=[sys.executable,'-c',code];r=subprocess.run(argv,capture_output=True,timeout=30)
        (case/'stdout').write_bytes(r.stdout);(case/'stderr').write_bytes(r.stderr)
        passed=r.returncode!=0 and 'missing/invalid bounded original selection' in r.stderr.decode(errors='replace') and not result.exists()
        api.append(dict(tag=tag,argv=argv,exit=r.returncode,result_absent=not result.exists(),passed=passed))
        if not passed:raise AssertionError('invalid selection was accepted '+tag)
    (out/'result.json').write_text(json.dumps(dict(status='PASS_ACTUAL_FULLPOOL_PREREQUISITE_REFUSALS',
      driver_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),cases=cases,selection_api_controls=api),indent=2)+'\n')
    print('PASS_ACTUAL_FULLPOOL_PREREQUISITE_REFUSALS:4 reducer +2 actual API invalid-selection; no native/game')


if __name__=='__main__':main(Path(sys.argv[1]))
