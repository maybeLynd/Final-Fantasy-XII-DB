import argparse,hashlib,json
from pathlib import Path
W=Path(__file__).resolve().parent;R=W/'run-01';ap=argparse.ArgumentParser();ap.add_argument('--raw',type=Path,default=R/'raw.json');ap.add_argument('--out',type=Path,default=W/'result.json');a=ap.parse_args();r=json.loads(a.raw.read_text())
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
assert r['finished'] and r['helper_unchanged'] and r['driver_sha256']==sha(W/'capture.py') and r['helper_sha256']==sha(R/'prereq.py')
cases={x['name']:x for x in r['cases']};assert len(cases)==len(r['cases'])==16
expected={'valid-tagged':True,'fail-with-zero-exit':False,'nonzero-exit':False,'missing-file':False,'upstream-exception':False,'malformed-output':False,'same-count-changed-tags':False,'missing-object':False,'missing-footer':False,'data-declared-findings':True,'data-exit-two':False,'data-half-built':False,'default-tab-fail':False,'custom-tab-pass':True,'custom-tab-fail':False,'bounded-timeout':False}
assert set(cases)==set(expected)
for name,want in expected.items():
 c=cases[name];assert c['expected_accepted'] is want
 assert json.loads((R/name/'declaration.json').read_text())==c['declaration']
 p=R/name/'upstream.py'
 if name=='missing-file':assert not p.exists() and c['upstream_sha256'] is None
 else:assert sha(p)==c['upstream_sha256']
 if name=='bounded-timeout':
  assert c['timed_out'] is True and c['returncode'] is None and 'COMPOSER_PASS' not in c['stdout']
 else:
  assert c['timed_out'] is False
  accepted=c['returncode']==0 and c['stdout'].startswith('COMPOSER_PASS ')
  assert accepted==c['actually_accepted']
  assert accepted==(True if name=='custom-tab-fail' else want)
  if not accepted:assert c['returncode']==1 and c['stdout'].startswith('COMPOSER_FAIL ')
 assert c['expectation_met']==(name!='custom-tab-fail')
s=json.loads((W/'standalone-format-control.json').read_text());assert s['returncode']==s['composer_returncode']==0 and s['matched_verdict']=='FAIL' and s['matched_tag']=='A' and not s['literal_space_prefix'] and s['composer_stdout'].startswith('COMPOSER_PASS ')
first=r['first_adopter'];assert first['available'] and first['returncode']==0 and not first['timed_out'] and first['stdout'].rstrip().endswith('FAILS 0') and sha(R/'first-adopter-test.py')==first['sha256']
result=dict(verdict='REJECT',status='REJECT_A03_CONFIGURED_FAIL_TAG_ACCEPTED',method=r['method'],raw_sha256=sha(a.raw),helper_sha256=r['helper_sha256'],helper_commit=r['helper_commit'],cases=16,
 established='Default tagged failures/missing/exception/malformed/changed-set/missing-object/footer rejected, valid tagged/custom PASS and explicit complete-data findings accepted, exit2/half-built rejected by named validator. External timeout controlled, not an intrinsic in-process deadline. Authored first-adopter suite re-executed/exit0, not independent native semantics.',
 defect='Public custom line regex recognizes FAIL-tab-A, upstream footer falsely says FAILS0/exit0, literal startswith FAIL-space detector misses it and actual composer passes. Baseline same configured format PASS accepted; default format rejects tab failure as malformed.',
 cause='Required verdict detection uses a hardcoded literal space prefix while custom line parser uses its captured PASS/FAIL group. The configured parser and failure predicate disagree.',
 consumer='OPUS owns prereq.py actual recognition/negative control repair. Legacy sn1_prereq.py contains the same textual-prefix predicate; its default suite remains valid, custom-format boundary is source-only followup, not independently executed here. Do not blanket retract current default/FABLE single-space consumers.',
 acceptance_discriminator='Recognized FAIL group under declared format must return refusal and actual composer exit1 with no downstream PASS; preserve matching configured PASS/default/data controls and exact repaired source identity.',
 limits='Synthetic software prerequisite controls, no FF12 native/live execution. Caller-specific object completeness requires explicit validator; names-only presence is not universal completeness. First-adopter test source/output pinned, its complete native/resource dependency closure not independently sealed here. Whole A03 integration/host/migration/full L1+L2 acceptance not awarded.')
if a.out.exists():assert json.loads(a.out.read_text())==result,'Preserve differing receipt; use new explicit output path'
else:a.out.write_text(json.dumps(result,indent=2)+'\n')
print(result['status'])
