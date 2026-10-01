import argparse, hashlib, json
from pathlib import Path
W = Path(__file__).resolve().parent
ap=argparse.ArgumentParser();ap.add_argument('--raw',type=Path,default=W/'read-only-01/raw.json');ap.add_argument('--out',type=Path,default=W/'result.json');a=ap.parse_args()
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
r=json.loads(a.raw.read_text());prior=json.loads((W/'run-01/raw.json').read_text())
assert r['finished'] is True and r['driver_sha256']==sha(W/'read-only-controls.py')
assert r['prior_partial_raw_sha256']==sha(W/'run-01/raw.json')
assert prior['finished'] is False and prior['fatal']['type']=='TimeoutExpired'
assert prior['driver_sha256']==sha(W/'capture.py') and r['sources']==prior['sources']
for n,s in r['sources'].items():
 p=W/'run-01/source'/s['path'];assert sha(p)==s['sha256']
 data=p.read_bytes();assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==s['blob']
ids={'valid-reject','valid-accept','no-owner','missing-verdict','conflicting-verdict','malformed-string','missing-commit','typed-commit','non-sha-commit','typed-record','self-review','typed-author'}
cases={c['name']:c for c in r['cases']};assert set(cases)==ids and len(r['cases'])==len(ids)
observed={}
for name,c in cases.items():
 assert not c['timed_out'] and c['child_reaped'] and c['board_unchanged']
 assert sha(W/'read-only-01'/name/'TEAM.json')==c['input_sha256']
 assert '--apply' not in c['args']
 if name=='typed-author':
  assert c['returncode']==1 and c['parsed_report'] is None and 'TypeError' in c['stderr']
  observed[name]='UNHANDLED_TYPE_ERROR'
 else:
  assert c['returncode']==0 and not c['stderr']
  report=json.loads(c['stdout']);assert report==c['parsed_report'] and len(report)==1
  observed[name]=report[0]['transition']
for name in ('valid-reject','valid-accept','no-owner','missing-verdict','conflicting-verdict','malformed-string','missing-commit'):
 assert observed[name]==cases[name]['expected']
for name in ('typed-commit','non-sha-commit','typed-record'):assert observed[name]=='REPAIR' and cases[name]['parsed_report'][0]['status']=='planned'
assert observed['self-review']=='INCORPORATE'
mem=json.loads((W/'inmemory-controls.json').read_text());assert mem['driver_sha256']==sha(W/'inmemory-control.py')
assert {c['name'] for c in mem['cases']}=={'valid-reject','typed-commit','non-sha-commit','typed-record','self-review'}
assert all(c['schema_valid'] and c['original_fixture_unchanged'] for c in mem['cases'])
positive=prior['cases'];assert len(positive)==1 and positive[0]['name']=='valid-reject'
assert positive[0]['cli']['returncode']==0 and positive[0]['cli']['parsed_report'][0]['status']=='created'
assert len(positive[0]['added'])==1 and positive[0]['added'][0]['assigned_to']=='OPUS'
result={'verdict':'REJECT','scope':'Transition admission of malformed source links and self-review; original code and actual CLI dry-run, plus original in-memory apply/schema',
 'source_tree_commit':r['source_tree_commit'],'transitions_commit':r['sources']['transitions.py']['last_commit'],
 'raw_sha256':sha(a.raw),'partial_apply_raw_sha256':sha(W/'run-01/raw.json'),'inmemory_raw_sha256':sha(W/'inmemory-controls.json'),
 'observed':observed,'defects':['truthy dictionary and non-SHA string commit admitted as planned REPAIR','dictionary record admitted as planned REPAIR','author self-review admitted as planned INCORPORATE','list author aborts whole plan with TypeError'],
 'cause':'reviews validates author membership and commit truthiness only; no commit/record representation or reviewer != author guard. In-memory original apply/schema accepts the emitted malformed requests.',
 'controls':'Actual CLI valid REJECT/ACCEPT and no-owner/missing/conflicting/malformed-string/missing-commit discriminate. One initial actual supported-writer REJECT created exactlyone task.',
 'unresolved':'Full CLI apply campaign INCOMPLETE at20s valid-accept timeout. Later private committed incorporation row does not repair missing caller receipt or prove descendant termination. Concurrent/idempotence and misleading-success failed-writer control NOT_EXECUTED. No full A14/A16/host lifecycle acceptance.',
 'limits':'Dry-run admission and in-memory effects are not actual applied malformed queue rows. No production mutation, native FF12/live/parity claim, guard bypass or quota changes. Unmodified Windows writer has one named Local mutex for every board path; possible contention, exact timeout cause unknown. CIM unavailable/psutil absent; no unknown process killed or lock reaped.',
 'next':'OPUS repairs linked metadata/independent-review admission at cause and re-requests scoped review; preserve valid/no-owner convention. ASTRA must add owned descendant tracking/cleanup and a bounded single-write feasibility control before future complete apply/race campaign. Do not repeat unchanged capture or certify incomplete run.'}
if a.out.exists():assert json.loads(a.out.read_text())==result,'Preserve existing receipt'
else:a.out.write_text(json.dumps(result,indent=2)+'\n')
print('REJECT_TRANSITION_ADMISSION_FULL_APPLY_INCOMPLETE',flush=True)
