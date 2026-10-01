"""Four real reducer CLI refusals; preserve deltas and checked prerequisites."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys

W=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
BASE=['capture-index-path.py','capture-filecache-hash-loop.py',
      'capture-filecache-key-boundaries.py',
      'capture-filecache-key-boundaries-before-normalizer-closure-01.py',
      'validate-title-source-annotations.py','prove_owner_reload_order.py',
      'filecache-key-boundaries-source-01.json','filecache-key-boundaries-source-02.json',
      'filecache-hash-loop-source-01.json','filecache-import-declarations-01.json']
BASE += [p+s for p in ['filecache-key-boundaries-capture-01',
                      'filecache-key-boundaries-capture-02','filecache-hash-loop-capture-01']
         for s in ['.status.json','.stdout','.stderr']]


def main():
    ap=argparse.ArgumentParser();ap.add_argument('out',type=Path)
    args=ap.parse_args();out=args.out
    if out.exists():raise ValueError('immutable controls directory exists')
    out.mkdir();records=[]
    for tag,message,changed in [
      ('failed-upstream','required upstream capture failed/stale','filecache-key-boundaries-capture-02.status.json'),
      ('prologue-only','normalizer semantic boundary incomplete','filecache-key-boundaries-source-02.json'),
      ('changed-prefix','exact original prefix literal prerequisite failed','filecache-key-boundaries-source-02.json'),
      ('wrong-compare-import','exact static import declarations missing','filecache-import-declarations-01.json')]:
        case=out/tag;case.mkdir()
        for n in BASE:shutil.copy2(W/n,case/n)
        p=case/changed;v=json.loads(p.read_text())
        if tag=='failed-upstream':v['exit']=1
        elif tag=='prologue-only':
            old=json.loads((case/'filecache-key-boundaries-source-01.json').read_text())
            v['ranges'][0]=old['ranges'][0]
        elif tag=='changed-prefix':v['prefix_literals'][0]['bytes']=b'/HOSTAPP/\0'.hex()
        else:v['imports'][1]['name']='_strnicmp'
        p.write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8')
        result=case/'unexpected-result.json'
        argv=[sys.executable,'-B',str(W/'prove-filecache-key-preprocessing.py'),
              '--inputs',str(case),'--out',str(result)]
        r=subprocess.run(argv,capture_output=True,timeout=20)
        (case/'stdout').write_bytes(r.stdout);(case/'stderr').write_bytes(r.stderr)
        passed=r.returncode!=0 and message in r.stderr.decode(errors='replace') and not result.exists()
        # Unchanged copies are losslessly reconstructible from the baseline.
        # Freeze their identity map, the changed file and actual CLI outputs;
        # do not multiply identical source bodies across four cases.
        inherited={n:sha(case/n) for n in BASE if n!=changed}
        if any(h!=sha(W/n) for n,h in inherited.items()):
            raise ValueError('unexpected change to a supposedly inherited input')
        rec={'tag':tag,'argv':argv,'exit':r.returncode,'terminal':True,
             'expected_error':message,'refusal_seen':message in r.stderr.decode(errors='replace'),
             'result_absent':not result.exists(),'passed':passed,
             'changed_file':changed,'changed_sha256':sha(p),'inherited_from_baseline':inherited}
        (case/'receipt.json').write_text(json.dumps(rec,indent=2)+'\n',encoding='utf-8')
        records.append(rec)
        if not passed:raise ValueError('required actual refusal failed: '+tag)
    result={'complete':len(records)==4,'status':'PASS_FOUR_ACTUAL_REFUSALS',
            'driver_sha256':sha(Path(__file__)),'producer_sha256':sha(W/'prove-filecache-key-preprocessing.py'),
            'baseline_sha256':{n:sha(W/n) for n in BASE},'cases':records}
    (out/'result.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print('PASS_FOUR_ACTUAL_REFUSALS; original/native/game executions0')


if __name__=='__main__':main()
