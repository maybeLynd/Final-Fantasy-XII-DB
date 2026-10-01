import argparse,hashlib,json,subprocess
from pathlib import Path
W=Path(__file__).resolve().parent;R=W/'run-01';sha=lambda b:hashlib.sha256(b).hexdigest()
p=argparse.ArgumentParser();p.add_argument('--raw',type=Path);a=p.parse_args();r=json.loads((a.raw or R/'raw.json').read_text())
assert r['terminal'] and r['exception'] is None and r['verdict']=='ACCEPT_SCOPED_WRITER_ATTRIBUTION_REPAIR','INVALID_OR_INCOMPLETE'
assert r['driver_sha256']==sha((W/'capture.py').read_bytes())==sha((R/'driver-before-run.py').read_bytes())
assert r['probe_sha256']==sha((W/'probe.py').read_bytes())
q=json.loads((W/'capture-terminal.json').read_text());assert q['terminal'] and q['returncode']==0 and not q['stderr'],'CAPTURE_FAILED'
assert q['argv'][-1].endswith('capture.py') and 'ACCEPT_SCOPED_WRITER_ATTRIBUTION_REPAIR' in q['stdout']
def git(*args):
 z=subprocess.run(['git',*args],capture_output=True);assert z.returncode==0,(args,z.stderr);return z.stdout
for name,z in r['sources'].items():
 b=(W/'source'/name).read_bytes();assert sha(b)==z['sha256'] and git('show',r['source_commit']+':'+z['path'])==b
 assert git('rev-parse',r['source_commit']+':'+z['path']).decode().strip()==z['blob']
assert set(r['sources'])=={'activity.py','requirements.py'}
old=Path('Database/FFXII TZA/_experiments/evidence/migration-activity-deltas-independent');mb=(old/'manifest.json').read_bytes()
assert sha(mb)==r['prior_manifest_sha256'] and git('show',r['prior_commit']+':'+(old/'manifest.json').as_posix())==mb
members={m['path']:m for m in json.loads(mb)['members']}
expected={'old-claim-no-feed':('UNKNOWN','claimed'),'foreign-review-no-feed':('UNKNOWN','claimed'),'foreign-review-explicit-unknown':('UNKNOWN','claimed'),'own-note-no-feed':('recent','working'),'busy-control':('active','working'),'idle-control':('idle','claimed')}
cs={x['name']:x for x in r['cases']};assert len(cs)==len(r['cases'])==6 and set(cs)==set(expected),'MISSING_CASE'
for name,x in cs.items():
 assert x['terminal'] and x['returncode']==0 and not x['stderr'] and x['input_unchanged'],'CHILD_FAILED'
 assert len(x['argv'])==4 and x['argv'][1]=='-B' and Path(x['argv'][2]).name=='probe.py' and Path(x['argv'][3]).name=='input.json'
 assert x==json.loads((R/name/'receipt.json').read_text()),'RECEIPT_CHANGED'
 b=(R/name/'input.json').read_bytes();rel='activity-02/'+name+'/input.json'
 assert sha(b)==x['input_sha256']==members[rel]['sha256'] and len(b)==members[rel]['bytes']
 assert git('show',r['prior_commit']+':'+(old/rel).as_posix())==b
 z=json.loads(x['stdout']);assert z==x['result'] and z['exception'] is None and isinstance(z['result'],dict),'MISSING_RESULT'
 assert Path(z['module_paths']['activity']).resolve()==(Path(x['argv'][2]).parent/'source/activity.py').resolve(),'WRONG_MODULE'
 out=z['result'];opus=next(y for y in out['by_agent'] if y['lane']=='OPUS');cat=next(y for y in out['categories'] if y['code']=='C');claim=next(y for y in opus['working'] if y['task']=='LABELLED-OPUS-OLD-CLAIM')
 live,kind=expected[name]
 assert (x['expected_liveness'],x['expected_kind'])==(live,kind)
 assert opus['liveness']==out['liveness']['OPUS'][0]==x['observed_liveness']==live and claim['kind']==x['observed_kind']==kind,'ATTRIBUTION_CHANGED'
 assert cat['working']==x['combat_colored'] and ('OPUS' in cat['working'])==(kind=='working')
print('ACCEPT_SCOPED_WRITER_ATTRIBUTION_REPAIR; SYNTHETIC_CLASSIFICATION_ONLY')
