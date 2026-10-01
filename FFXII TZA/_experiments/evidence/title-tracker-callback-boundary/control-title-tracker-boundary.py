"""Actual reducer CLI refusals for missing queue, wrong getter and store role.
Labelled synthetic source copies only; do not mutate retained originals.
"""
import hashlib,importlib.util,json,pathlib,shutil,sys
W=pathlib.Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('delivery',W/'prepare-residue-packet-publication.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
driver=W/'prove-title-tracker-callback-boundary.py';positive=W/'title-tracker-callback-boundary-result-01.json';r=json.loads(positive.read_text())
if not r.get('producer_complete') or r['checker_sha256']!=hashlib.sha256(driver.read_bytes()).hexdigest():raise ValueError('missing/moved completed positive')
out=W/'title-tracker-boundary-controls-01';out.mkdir();checks=[]
for name in ['missing-queue-source','wrong-global-getter','old-store-role']:
 case=out/name;src=case/'source';src.mkdir(parents=True)
 for pin in r['source_pins']:shutil.copyfile(W/pin['path'],src/pin['path'])
 p=src/'title-cleanup-callback-queue-source-01.json'
 if name=='missing-queue-source':p.unlink()
 else:
  z=json.loads(p.read_text());hits=0
  for q in z['ranges']:
   for i in q['instructions']:
    if int(i['pc'],16)==(0x189120 if name=='wrong-global-getter' else 0x185acf):
     if name=='wrong-global-getter':i['memory'][0]['rip_target']='0x1f7f5a0'
     else:i['memory'][0]['role']='r'
     hits+=1
  if hits!=1:raise ValueError('control target missing/ambiguous')
  p.write_text(json.dumps(z,indent=2)+'\n')
 target=case/'must-not-exist.json';error=None
 try:m.checked_run([sys.executable,str(driver),str(target),str(src)],timeout=45,receipt_prefix=case/'invocation')
 except RuntimeError as e:error=str(e)
 if error is None or target.exists():raise AssertionError('invalid evidence reached result '+name)
 checks.append(dict(case=name,status='PASS_REFUSED_NO_RESULT',error=error,labelled_synthetic=True))
with (out/'result.json').open('x') as f:json.dump(dict(status='PASS_PRODUCER_CONTROLS',checks=checks,driver_sha256=hashlib.sha256(driver.read_bytes()).hexdigest(),positive_sha256=hashlib.sha256(positive.read_bytes()).hexdigest(),limits='Three actual failed-prerequisite CLI invocations; completed positive reused, no original-code executions or independent acceptance.'),f,indent=2)
print('Missing queue/wrong getter/incorrect actual store role refused before result')
