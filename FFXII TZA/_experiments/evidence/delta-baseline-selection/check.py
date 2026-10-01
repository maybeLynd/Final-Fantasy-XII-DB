import argparse,hashlib,json,subprocess
from pathlib import Path
W=Path(__file__).resolve().parent;R=W/'run-03';sha=lambda b:hashlib.sha256(b).hexdigest();p=argparse.ArgumentParser();p.add_argument('--raw',type=Path);a=p.parse_args();r=json.loads((a.raw or R/'raw.json').read_text())
assert r['terminal'] and r['exception'] is None and r['verdict']=='REJECT_UNIVERSAL_SAME_PRIOR_FOR_VERIFIED_MISSING_PROGRESS_VIEW','INVALID_OR_INCOMPLETE'
assert r['driver_sha256']==sha((W/'capture.py').read_bytes())==sha((R/'driver-before-run.py').read_bytes())
t=json.loads((W/'capture-terminal-03.json').read_text());assert t['terminal'] and t['returncode']==0 and not t['stderr'],'CAPTURE_FAILED'
for path,z in r['sources'].items():
 b=(R/'source'/path).read_bytes();assert sha(b)==z['sha256'];q=subprocess.run(['git','show',r['source_commit']+':'+path],capture_output=True);assert q.returncode==0 and q.stdout==b
 q=subprocess.run(['git','rev-parse',r['source_commit']+':'+path],capture_output=True,text=True);assert q.returncode==0 and q.stdout.strip()==z['blob'];assert sha((R/'current-preimages'/path).read_bytes())==z['current_sha256']
for n,rel in [('build_views','Database/Tools/dashboard/build_views.py'),('requirements','Database/Tools/dashboard/requirements.py'),('generation','Database/Tools/analysis-kit/gfz-scripts/generation.py')]:assert Path(r['loaded_paths'][n]).parts[-len(Path(rel).parts):]==Path(rel).parts
assert [x['name'] for x in r['static_build_calls']]==['prior_progress','prior_generation','annotate_deltas']
for nr,terminal,key in [('run-01','capture-terminal.json','preparation_failure'),('run-02','capture-terminal-02.json','second_preparation_failure')]:
 b=(W/nr/'raw.json').read_bytes();z=json.loads(b);assert sha(b)==r[key]['raw_sha256'] and z['terminal'] and z['verdict']=='INVALID' and z['exception'] is not None
 b=(W/terminal).read_bytes();z=json.loads(b);assert sha(b)==r[key]['terminal_sha256'] and z['terminal'] and z['returncode']!=0
cs={x['name']:x for x in r['cases']};assert len(cs)==len(r['cases'])==3 and set(cs)=={'empty-history','aligned-latest','latest-missing-progress'},'MISSING_CASE'
assert sha((R/'labelled-input.json').read_bytes())==r['fixture_input_sha256']
allverify=[]
for name,x in cs.items():
 root=(R/x['store_relative']).resolve();assert root.is_relative_to(W.resolve()) and x['store_unchanged']
 h={f.relative_to(root).as_posix():sha(f.read_bytes()) for f in root.rglob('*') if f.is_file()};assert h==x['store_hashes'],'STORE_CHANGED'
 for g in x['generations']:
  d=root/g['generation'];b=(d/'MANIFEST.json').read_bytes();assert sha(b)==g['manifest_sha256'];m=json.loads(b)
  assert m['generation']==g['generation'] and set(m['outputs'])==set(g['required_outputs']) and m['inputs']['fixture']['sha256']==r['fixture_input_sha256']
  assert set(f.name for f in (d/'outputs').iterdir())==set(m['outputs'])
  for fn,z in m['outputs'].items():assert sha((d/'outputs'/fn).read_bytes())==z['sha256'] and (d/'outputs'/fn).stat().st_size==z['size']
  q=g['verify'];expected='CURRENT %s committed %s; %d outputs; sources unchanged\n'%(g['generation'],m['committed_at'],len(m['outputs']))
  assert q['terminal'] and q['returncode']==0 and not q['stderr'] and q['stdout']==expected,'VERIFIER_PREREQUISITE'
  assert q['argv'][-2]=='verify' and Path(q['argv'][-1]).resolve().parts[-3:]==root.parts[-3:];allverify.append(q)
 assert x['annotated']['delta_basis']['generation']==(x['general_prior'] or {}).get('generation')
assert allverify==r['prerequisite_verifications'],'VERIFICATION_RECEIPT_CHANGED'
x=cs['empty-history'];assert x['retained_from_run01'] and not x['generations'] and x['progress_prior'] is None and x['general_prior'] is None and x['composed_change'] is None
old=next(x for x in json.loads((W/'run-01/raw.json').read_text())['cases'] if x['name']=='empty-history');assert {k:v for k,v in cs['empty-history'].items() if k not in ('retained_from_run01','store_relative')}==old
x=cs['aligned-latest'];assert x['generations'][0]['created_in_run01'] and x['progress_prior']['generation']==x['general_prior']['generation']==x['generations'][0]['generation'] and x['composed_change']['scopes']['union']['pct']==x['annotated']['measures'][0]['delta']['pp']==10.0
x=cs['latest-missing-progress'];assert x['progress_prior']['generation']==x['generations'][0]['generation'] and x['general_prior']['generation']==x['generations'][1]['generation'] and x['progress_prior']['generation']!=x['general_prior']['generation']
assert x['composed_change']['scopes']['union']==dict(accepted=20,scope=0,pct=20.0) and x['annotated']['measures'][0]['delta']['na']=='no prior'
print('REJECT_SAME_PRIOR_AT_VERIFIED_MISSING_VIEW_BOUNDARY; NOT_FULL_BUILD_OR_DEPLOYMENT')
