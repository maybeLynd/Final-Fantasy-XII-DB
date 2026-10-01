"""Read-only reduction; an attribution counterexample is not whole-dashboard acceptance."""
import argparse,ast,gzip,hashlib,json
from datetime import datetime
from pathlib import Path
def sha(b):return hashlib.sha256(b).hexdigest()
def load(p):return json.loads(p.read_text())
def reduce(w,d):
    r=load(d/'raw.json');assert r['finished'] is True and 'fatal' not in r,'INCOMPLETE_CAPTURE'
    inv=load(d/'invocation.json');assert inv['terminal'] and inv['returncode']==0 and not inv['stderr'],'UPSTREAM_FAILED'
    assert r['driver_sha256']==inv['driver_sha256']==sha((w/'activity-controls.py').read_bytes())
    assert r['source_commit']=='8ddc8c7e8e91be7019229c3df8084f53430804bb'
    want={'activity.py':'b13a1d6b8d3a7bb891d5cb7bd1f6d4c86c5ed4673071020d420bef6118bda4a7',
          'requirements.py':'be30718c33e4cca6426fe065031495a59c928b7975854492ae174820119885d9',
          'team.py':'70068994a0313652ef4f0ec0791a4d4d64163d3ff0c754f49ae9ab817cabd1f6'}
    assert set(r['sources'])==set(want)
    for n,h in want.items():assert sha((d/'source'/n).read_bytes())==h==r['sources'][n]['sha256']
    expected={'old-claim-no-feed':('UNKNOWN','claimed',[]),'foreign-review-no-feed':('recent','working',['FABLE']),
              'foreign-review-explicit-unknown':('recent','working',['FABLE']),'own-note-no-feed':('UNKNOWN','claimed',['OPUS']),
              'busy-control':('active','working',[]),'idle-control':('idle','claimed',['FABLE'])}
    assert len(r['cases'])==6 and {x['name'] for x in r['cases']}==set(expected),'MISSING_CASE'
    for c in r['cases']:
        n=c['name'];assert c==load(d/n/'receipt.json') and c['exception'] is None
        data=(d/n/'input.json').read_bytes();assert sha(data)==c['input_sha256']
        inp=json.loads(data);assert inp['now']==r['clock'];b=inp['board']
        writers=sorted({h['agent'] for h in b['history'] if inp['now']-datetime.fromisoformat(h['at']).timestamp()<=3600})
        assert writers==c['actual_recent_writers']==expected[n][2],'WRITER_PROVENANCE_MISMATCH'
        assert (c['observed_liveness'],c['observed_claim_kind'])==expected[n][:2]
        mine=next(x for x in c['result']['by_agent'] if x['lane']=='OPUS')
        assert mine['liveness']==c['observed_liveness']
        claim=next(x for x in mine['working'] if x['task']=='LABELLED-OPUS-OLD-CLAIM')
        assert claim['kind']==c['observed_claim_kind']
        cat=next(x for x in c['result']['categories'] if x['code']=='C')
        assert cat['working']==c['combat_colored_lanes']
        assert ('OPUS' in cat['working'])==(c['observed_claim_kind']=='working')
        if n.startswith('foreign'):
            last=b['history'][-1];assert last['agent']=='FABLE' and last['operation']['action']=='add'
            queued=next(x for x in b['tasks'] if x['id']=='LABELLED-VERIFY-QUEUED')
            assert queued['agent'] is None and queued['status']=='READY' and queued['assigned_to']=='OPUS'
            assert all(x['kind']=='waiting' for x in mine['waiting']) and c['expected_claim_kind']=='claimed'
        if n=='own-note-no-feed':assert b['history'][-1]['agent']=='OPUS' and b['history'][-1]['operation']['action']=='note'
    failed=load(w/'activity-01/failure.json');assert failed['returncode']==1 and failed['semantic_results']==0 and failed['finished'] is False
    assert failed['driver_sha256']==sha((w/'activity-01/driver.py').read_bytes())
    dep=w/'deployed-01';dr=load(dep/'raw.json');iv=load(dep/'invocation.json')
    assert dr['finished'] and 'fatal' not in dr and iv['returncode']==0 and iv['terminal'] and not iv['stderr']
    assert dr['driver_sha256']==iv['driver_sha256']==sha((w/'deployed-read.py').read_bytes())
    assert len(dr['requests'])==5 and len(dr['files'])==4,'MISSING_DEPLOYED_EVIDENCE'
    for c in dr['requests']:
        p=dep/(c['name']+('.html' if c['name']=='page' else '.json'));data=p.read_bytes()
        assert c['status']==200 and sha(data)==c['sha256'] and len(data)==c['bytes']
    for c in dr['files']:
        data=(dep/c['stored']).read_bytes();data=gzip.decompress(data) if c['compressed'] else data
        assert len(data)==c['bytes'] and sha(data)==c['sha256']
    s=load(dep/'status-before.json');s2=load(dep/'status-after.json');a=load(dep/'activity.json');live=load(dep/'live.json')
    assert a['status']=='OK' and len({s['generation'],s2['generation'],a['generation'],live['generation']})==1
    assert s['reader_stale'] is False and s2['reader_stale'] is False
    assert dr['board_before_revision']==a['feed']['board_revision']==dr['board_after_revision']
    before=load(dep/'controller-before.json');after=load(dep/'controller-after.json');assert before==after
    assert live['state']=='OK' and live['interval']==1800 and live['last_rc']==0
    assert live['next_at']==live['last_run']+1800==before['dashboard']['last_run']+1800
    refs=load(dep/'current-source.json')
    for n,c in refs.items():assert sha((dep/'source-current'/n).read_bytes())==c['sha256']
    assert refs['activity.py']['sha256']==want['activity.py']
    tree=ast.parse((dep/'source-current/server.py').read_text());page=next(ast.literal_eval(x.value) for x in tree.body if isinstance(x,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='PAGE' for t in x.targets))
    assert (dep/'page.html').read_bytes()==page.encode('utf-8'),'SERVED_PAGE_DIFFERS'
    return {'verdict':'REJECT_ACTIVITY_WRITER_ATTRIBUTION','source_commit':r['source_commit'],'activity_cases':6,
            'defects':['peer assignment falsely credits recipient write','genuine lane note omitted from recent-write fallback'],
            'prior_preparation':'INVALID_NO_SEMANTIC_RESULTS','deployed_generation':s['generation'],
            'deployed_timer':'one OK sample last_run+1800 matched','deltas':'NOT_TESTED','rendered_UI':'NOT_TESTED',
            'loaded_activity_module_identity':'UNVERIFIED','whole_dashboard_acceptance':False,'full_L1_L2':False,
            'independent_acceptance_of_evidence':'PENDING'}
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--activity',type=Path);ap.add_argument('--out',type=Path);a=ap.parse_args();w=Path(__file__).resolve().parent
    result=reduce(w,a.activity or w/'activity-02')
    if a.out:a.out.write_text(json.dumps(result,indent=2)+'\n')
    print('REJECT_ACTIVITY_WRITER_ATTRIBUTION',json.dumps(result,sort_keys=True))
