"""Read-only receipt reducer. Upstream failure or absent evidence cannot pass."""
import argparse, hashlib, json
from pathlib import Path
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def reduce(run, driver):
    r=json.loads((run/'raw.json').read_text())
    assert r['finished'] is True and 'fatal' not in r, 'INCOMPLETE_CAPTURE'
    assert r['source_commit']=='f21fe80440fc9d24df09fc19172753394fe61773'
    assert r['driver_sha256']==sha(driver)
    want={'transitions.py':'265dcd8b33b600060ff1482820816b23e13252c5395aa2fd4937aae14642e9e7',
          'team.py':'70068994a0313652ef4f0ec0791a4d4d64163d3ff0c754f49ae9ab817cabd1f6'}
    assert set(r['sources'])==set(want)
    for n,h in want.items():
        p=run/'source/Database/Tools/analysis-kit/gfz-scripts'/n
        assert sha(p)==h==r['sources'][n]['sha256'] and p.stat().st_size==r['sources'][n]['bytes']
    assert sha(run/'prior-read-only-raw.json')==r['prior_raw_sha256']=='779e95eddb19cb6a6c851922242852c99a4be34105da7d9207fcf88a6b0484c5'
    prior=json.loads((run/'prior-read-only-raw.json').read_text())
    old={c['name']:c for c in prior['cases']};assert prior['finished'] and len(old)==12
    expected={n:'MALFORMED' for n in old}
    expected.update({'valid-reject':'REPAIR','valid-accept':'INCORPORATE','no-owner':'ACCEPTED',
     'missing-verdict':'VERDICT-MISSING','conflicting-verdict':'VERDICT-CONFLICT',
     'self-review':'SELF-REVIEW','self-review-reject':'SELF-REVIEW'})
    cases=r['cases'];assert len(cases)==13 and {c['name'] for c in cases}==set(expected), 'MISSING_OR_DUPLICATE_CASE'
    for c in cases:
        n=c['name'];d=run/n
        assert c==json.loads((d/'receipt.json').read_text()), 'RECEIPT_DISAGREES'
        assert c['returncode']==0 and c['stderr']=='' and c['parse_error'] is None, 'UPSTREAM_FAILED'
        assert c['timed_out'] is False and c['child_reaped'] is True and c['writer_invoked'] is False
        assert c['board_unchanged'] is True and sha(d/'TEAM.json')==c['input_sha256']
        if n in old: assert c['input_sha256']==old[n]['input_sha256'], 'CHANGED_REUSED_INPUT'
        else:
            b=json.loads((d/'TEAM.json').read_text());origin=json.loads((run/'self-review/TEAM.json').read_text())
            origin['tasks'][0]['result_refs']=['verdict:REJECT'];assert b==origin
        args=c['args'];assert len(args)==6 and args[1]=='-B' and args[-1]=='--json' and args[3]=='--board' and '--apply' not in args
        assert Path(args[2]).name=='transitions.py' and Path(args[4]).name=='TEAM.json'
        report=json.loads(c['stdout']);assert report==c['parsed_report'] and len(report)==1
        row=report[0];assert row['transition']==expected[n] and c['expected']==expected[n], 'WRONG_DISPOSITION'
        plan=c['original_plan'];assert len(plan)==1 and plan[0][:3]==[row['transition'],row['review'],row['detail']]
        op=plan[0][3]
        if n in ('valid-reject','valid-accept'):
            assert row['status']=='planned' and isinstance(op,dict) and op['action']=='add'
            owner='OPUS' if n=='valid-reject' else 'FABLE'
            assert op['task']['assigned_to']==owner and op['task']['id']==row['detail'], 'WRONG_ROUTE_OWNER'
            assert op['task']['transition_of']['review']==row['review']
        else: assert row['status']=='-' and op is None, 'INVALID_ROUTE'
    return {'verdict':'ACCEPT_SCOPED_ADMISSION','cases':13,'reused_inputs':12,'new_minimal_self_review_reject':1,
            'source_commit':r['source_commit'],'write_campaign':'OPEN_NOT_EXECUTED',
            'complete_M2':False,'full_L1_L2':False,'independent_acceptance_of_this_package':'PENDING'}
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--run',type=Path);ap.add_argument('--out',type=Path);a=ap.parse_args()
    w=Path(__file__).resolve().parent
    result=reduce(a.run or w/'run-01',w/'capture.py')
    if a.out:a.out.write_text(json.dumps(result,indent=2)+'\n')
    print('ACCEPT_SCOPED_ADMISSION',json.dumps(result,sort_keys=True))
