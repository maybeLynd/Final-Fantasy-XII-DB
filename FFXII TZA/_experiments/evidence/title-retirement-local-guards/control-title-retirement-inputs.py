"""Two actual failed-prerequisite CLI cases; reuse the completed positive.
Changed evidence is synthetic and confined to this case directory.
"""
import hashlib,importlib.util,json,pathlib,shutil,sys
W=pathlib.Path(__file__).resolve().parent;ROOT=W.parents[4]
s=importlib.util.spec_from_file_location('delivery',W/'prepare-residue-packet-publication.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
positive=W/'title-retirement-local-guards-result-02.json';driver=W/'prove-title-retirement-guards.py';r=json.loads(positive.read_text())
if not r['producer_complete'] or r['checker_sha256']!=hashlib.sha256(driver.read_bytes()).hexdigest() or len(r['bounded_arithmetic'])!=64:raise ValueError('missing/moved/zero positive')
out=W/'title-retirement-input-controls-02';out.mkdir()
retained=ROOT/'Database/FFXII TZA/_experiments/evidence/title-member-notification-routing/section04-title-member-source';checks=[]
for name in ['missing-manifest','same-count-changed-mask']:
 case=out/name;case.mkdir();source=case/'source';shutil.copytree(retained,source)
 if name=='missing-manifest':(source/'original_body_manifest.json').unlink()
 else:
  p=source/'original_disassembly.txt';z=p.read_text()
  if z.count('0024A6D1 25003f0000')!=1:raise ValueError('control target missing')
  before=z.count('\n');z=z.replace('0024A6D1 25003f0000               and      eax, 0x3f00','0024A6D1 25003f0000               and      eax, 0x3f20')
  if '0024A6D1 25003f0000               and      eax, 0x3f20' not in z or z.count('\n')!=before:raise ValueError('same-count mutation failed')
  p.write_text(z)
 target=case/'must-not-exist.json';error=None
 try:m.checked_run([sys.executable,str(driver),str(target),str(source)],timeout=45,receipt_prefix=case/'invocation')
 except RuntimeError as e:error=str(e)
 if error is None or target.exists():raise AssertionError('invalid prerequisite reached result '+name)
 checks.append(dict(case=name,status='PASS_REFUSED_NO_RESULT',error=error,labelled_synthetic=True))
with (out/'result.json').open('x') as f:json.dump(dict(status='PASS_PRODUCER_INPUT_CONTROLS',checks=checks,positive_result=positive.name,positive_sha256=hashlib.sha256(positive.read_bytes()).hexdigest(),driver_sha256=hashlib.sha256(driver.read_bytes()).hexdigest(),limits='Two actual CLI refusal cases; prior positive reused, not recounted/replayed. No native/live execution or independent acceptance.'),f,indent=2)
print('Missing/changed retained evidence refused; completed positive not repeated')
