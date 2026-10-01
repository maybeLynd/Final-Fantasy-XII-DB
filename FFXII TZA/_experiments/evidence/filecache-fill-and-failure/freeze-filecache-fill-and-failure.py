"""Checked frozen packet with pinned external dependencies and lossless control deltas."""
import hashlib,json
from pathlib import Path
import shutil
W=Path(__file__).resolve().parent;sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 out=W/'filecache-fill-and-failure-frozen-ready'
 if out.exists():raise ValueError('immutable packet exists')
 stages=[('filecache-fill-key-resolver-capture-01','capture-filecache-fill-key-provenance.py'),
 ('filecache-release-allocator-thunks-qualification-01','qualify-filecache-failure-thunks.py'),
 ('filecache-fill-and-failure-positive-02','prove-filecache-fill-and-failure.py'),
 ('filecache-fill-and-failure-controls-run-01','control-filecache-fill-and-failure.py')]
 for tag,driver in stages:
  s=json.loads((W/(tag+'.status.json')).read_text())
  if s.get('exit')!=0 or s.get('terminal') is not True or s.get('driver_sha256')!=sha(W/driver):raise ValueError('required upstream failed/incomplete/stale')
  if not(W/(tag+'.stdout')).read_bytes().strip() or (W/(tag+'.stderr')).read_bytes():raise ValueError('required upstream output missing/error')
 r=json.loads((W/'filecache-fill-and-failure-result-01.json').read_text())
 if r.get('producer_complete') is not True or r['driver_sha256']!=sha(W/'prove-filecache-fill-and-failure.py') or len(r['original_graphs'])!=12 or r['correlated_resolver_proof']['reachable_abstract_states']<=0 or not r['correlated_resolver_proof']['fill_states']:raise ValueError('required result incomplete/empty')
 for x in r['source_pins']:
  if sha(W/x['path'])!=x['sha256']:raise ValueError('source changed')
 c=json.loads((W/'filecache-fill-and-failure-controls-01/result.json').read_text())
 if c.get('complete') is not True or c.get('status')!='PASS_FOUR_ACTUAL_REFUSALS' or len(c['cases'])!=4 or not all(x['passed'] and x['terminal'] and x['exit']!=0 and x['result_absent'] for x in c['cases']):raise ValueError('controls incomplete/invalid')
 if c['driver_sha256']!=sha(W/'control-filecache-fill-and-failure.py') or c['producer_sha256']!=r['driver_sha256']:raise ValueError('control/producer identity moved')
 files=['capture-index-path.py','validate-title-source-annotations.py','prove_owner_reload_order.py','run-filecache-equal-key.py',
 'filecache-fill-key-resolver-source-01.json','filecache-release-allocator-thunks-source-01.json','filecache-release-allocator-thunks-qualified-01.json',
 'prove-filecache-fill-and-failure.py','prove-filecache-fill-and-failure-before-correlated-arm-01.py','control-filecache-fill-and-failure.py','freeze-filecache-fill-and-failure.py',
 'filecache-fill-and-failure-result-01.json','FILECACHE-FILL-KEY-PROVENANCE-METHOD-1001.md','FILECACHE-FAILURE-METHOD-1001.md',
 'filecache-fill-and-failure-controls-01/result.json']
 for tag,driver in stages:
  files.append(driver);files.extend(tag+s for s in ['.status.json','.stdout','.stderr'])
 files.extend('filecache-fill-and-failure-positive-01'+s for s in ['.status.json','.stdout','.stderr'])
 for case in c['cases']:
  base=Path('filecache-fill-and-failure-controls-01')/case['tag']
  for name,pin in case['inherited_from_baseline'].items():
   if sha(W/base/name)!=pin or sha(W/name)!=pin:raise ValueError('control delta is not lossless')
  if sha(W/base/case['changed_file'])!=case['changed_sha256']:raise ValueError('control changed input moved')
  files.extend((base/name).as_posix() for name in [case['changed_file'],'stdout','stderr','receipt.json'])
 out.mkdir()
 for name in sorted(set(files)):
  p=out/name;p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(W/name,p)
 shutil.copy2(W/'FILECACHE-FILL-AND-FAILURE-README-1001.md',out/'README.md')
 (out/'external-dependencies.json').write_text(json.dumps(dict(required=r['external_dependencies'],missing='INCOMPLETE/refusal; not a self-contained export',limits='Immutable parent source manifests are required; producer/reviewer acceptance is separate'),indent=2)+'\n')
 (out/'malloc-contract.json').write_text(json.dumps(dict(method='External named API contract, not actual loaded FF12 CRT',url='https://learn.microsoft.com/en-us/cpp/c-runtime-library/reference/malloc?view=msvc-170',read_date='2026-10-01',paraphrase='malloc may return null for insufficient memory; new-handler behavior can be configured. This does not prove the exact loaded heap or that a16-byte allocation can fail after this preceding free.'),indent=2)+'\n')
 (out/'.gitattributes').write_text('* -text\n')
 members=[dict(path=p.relative_to(out).as_posix(),bytes=p.stat().st_size,sha256=sha(p)) for p in sorted(out.rglob('*')) if p.is_file()]
 (out/'manifest.json').write_text(json.dumps(dict(kind='original cache fill-key provenance and conditional failure release',members=members),indent=2)+'\n')
 print(json.dumps(dict(members=len(members),manifest_sha256=sha(out/'manifest.json'))))
if __name__=='__main__':main()
