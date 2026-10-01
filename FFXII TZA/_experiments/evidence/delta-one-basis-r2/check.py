"""Read-only returned-repair reducer. No new builds/selectors or producer suites."""
import copy,hashlib,json
from pathlib import Path
sha=lambda b:hashlib.sha256(b).hexdigest()

def reduce(r,run):
 assert r['terminal'] and r['exception'] is None and r['verdict']=='ACCEPT_SCOPED_ONE_PRIOR_BASIS_AT_RETAINED_HISTORY_BOUNDARY'
 assert sha((run/'capture.py').read_bytes())==r['driver_sha256']
 assert r['source_commit']=='17d6cdc2915b22b1743cdd2e2c6acc2fcdf6f5e2'
 for p,z in r['sources'].items():
  assert sha((run/'source'/p).read_bytes())==z['sha256']
  assert sha((run/'current-preimages'/p).read_bytes())==z['current_sha256']
 for n,rel in [('build_views','Database/Tools/dashboard/build_views.py'),('requirements','Database/Tools/dashboard/requirements.py'),('generation','Database/Tools/analysis-kit/gfz-scripts/generation.py')]:
  assert Path(r['loaded_paths'][n]).parts[-len(Path(rel).parts):]==Path(rel).parts
 assert [(x['name'],x['args']) for x in r['static_build_calls']]==[('prior_generation',['st']),('prior_progress',['pman','pdir']),('annotate_deltas',['views','pdir','pman'])]
 oldb=(run/'parent-raw.json').read_bytes();mb=(run/'parent-manifest.json').read_bytes()
 assert sha(oldb)==r['parent']['raw_sha256'] and sha(mb)==r['parent']['manifest_sha256']
 old=json.loads(oldb);members={m['path']:m for m in json.loads(mb)['members']}
 assert members['run-03/raw.json']['sha256']==sha(oldb)
 cs={x['name']:x for x in r['cases']}
 assert len(cs)==len(r['cases'])==3 and set(cs)=={'empty-history','aligned-latest','latest-missing-progress'}
 for name,x in cs.items():
  store=run/name/'store';h={f.relative_to(store).as_posix():sha(f.read_bytes()) for f in store.rglob('*') if f.is_file()}
  parent=next(y for y in old['cases'] if y['name']==name)
  assert h==x['store_hashes']==parent['store_hashes'] and x['store_unchanged']
  for rel,value in h.items():assert members[x['parent_store_relative']+'/'+rel]['sha256']==value
  assert x['generations']==parent['generations']
  assert len(x['verification_receipts'])==len(x['generations'])
  for q in x['verification_receipts']:
   cm=json.loads((store/x['generations'][-1]['generation']/'MANIFEST.json').read_bytes())
   expected='CURRENT %s committed %s; %d outputs; sources unchanged\n'%(cm['generation'],cm['committed_at'],len(cm['outputs']))
   assert q['terminal'] and q['returncode']==0 and not q['stderr'] and q['stdout']==expected
   assert q['argv'][-2]=='verify'
  assert x['annotated']['delta_basis']['generation']==(x['general_prior'] or {}).get('generation')
  if name=='aligned-latest':
   assert x['progress_prior']['generation']==x['general_prior']['generation']==x['generations'][-1]['generation']
   assert x['change_expression_result']['scopes']['union']=={'accepted':10,'scope':0,'pct':10.0}
   assert x['annotated']['measures'][0]['delta']['pp']==10.0
  else:
   assert x['progress_prior'] is None and x['change_expression_result'] is None
   assert x['annotated']['measures'][0]['delta']['na']=='no prior'
   if name=='empty-history':assert x['general_prior'] is None and not x['generations']
   else:assert x['general_prior']['generation']==x['generations'][-1]['generation']
 return {'verdict':'ACCEPT scoped to exact17d6 selectors/change expression/annotator on retained history inputs',
 'latest_missing_progress':'None/no prior, basis names newest verified generation; no older fallback',
 'aligned_latest':'+10pp on same named generation','empty_history':'None/no prior',
 'limits':'Synthetic counts and copied retained Store histories, static build argument flow, extracted change expression; no full measure/adapter/build, deployed/browser or real progress award.'}

if __name__=='__main__':
 run=Path(__file__).resolve().parent/'run-01';raw=json.loads((run/'raw.json').read_bytes());result=reduce(raw,run);controls=[]
 for n in ['missing-case','failed-verifier']:
  bad=copy.deepcopy(raw)
  if n=='missing-case':bad['cases']=bad['cases'][:-1]
  else:bad['cases'][-1]['verification_receipts'][0]['returncode']=1
  try:reduce(bad,run)
  except AssertionError:controls.append({'name':n,'refused':True})
  else:raise AssertionError('Incomplete/failed prerequisite admitted')
 print(json.dumps({'result':result,'receipt_controls':controls},indent=2))
