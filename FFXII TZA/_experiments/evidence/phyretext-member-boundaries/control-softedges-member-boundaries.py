"""Concrete checker invocation refuses lost prerequisites or changed semantics.
Disposable source copies only; no original game/input/result modification.
"""
import hashlib,json,pathlib,shutil,subprocess,sys
W=pathlib.Path(__file__).resolve().parent;out=W/'softedges-member-boundaries-controls-01'
if out.exists():raise ValueError('immutable controls exist')
driver=W/'check-softedges-member-boundaries.py';result=json.loads((W/'softedges-member-boundaries-result-02.json').read_text())
if result['checker_sha256']!=hashlib.sha256(driver.read_bytes()).hexdigest() or result['producer_complete'] is not True:raise ValueError('baseline unchecked')
out.mkdir();checks=[]
for case in ['missing-callback','incomplete-continuation','changed-status-sequence']:
 c=out/case;s=c/'source';s.mkdir(parents=True)
 for item in result['inputs']:
  p=s/item['path'];p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(W/item['path'],p)
 if case=='missing-callback':(s/'softedges-elements-callback-source-01/original-code.json').unlink()
 elif case=='incomplete-continuation':
  p=s/'softedges-member-resolution-continuation-code-01.json';r=json.loads(p.read_text());r['wrapper_complete']=False;p.write_text(json.dumps(r)+'\n')
 else:
  p=s/'softedges-elements-callback-source-01/original-code.json';r=json.loads(p.read_text());q=next(q for q in r['ranges'] if q['start']=='0x60f280')
  x=next(x for x in q['instructions'] if x['pc']=='0x60f289');x.update(bytes='9090',mnemonic='nop',args='disclosed same-width mutation')
  q['sha256']=hashlib.sha256(bytes.fromhex(''.join(x['bytes'] for x in q['instructions']))).hexdigest();p.write_text(json.dumps(r)+'\n')
 receipt=dict(case=case,argv=[sys.executable,str(driver),str(s),str(c/'result.json')])
 try:
  r=subprocess.run(receipt['argv'],cwd=W.parents[4],capture_output=True,timeout=15)
  (c/'stdout.txt').write_bytes(r.stdout);(c/'stderr.txt').write_bytes(r.stderr)
  receipt.update(exit=r.returncode,result_exists=(c/'result.json').exists(),status='PASS_REFUSED' if r.returncode!=0 and not (c/'result.json').exists() else 'FAIL')
 except Exception as e:
  receipt.update(status='INCOMPLETE',exception=repr(e));(c/'invocation.json').write_text(json.dumps(receipt,indent=2)+'\n');raise
 (c/'invocation.json').write_text(json.dumps(receipt,indent=2)+'\n');checks.append(receipt)
 if receipt['status']!='PASS_REFUSED':raise ValueError('concrete invocation admitted invalid source')
(out/'result.json').write_text(json.dumps(dict(status='PASS_PRODUCER_PREREQUISITE_CONTROLS',driver_sha256=hashlib.sha256(driver.read_bytes()).hexdigest(),
 control_driver_sha256=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),baseline='Existing result02, not repeated',checks=checks,
 limits='Three actual checker refusal paths; mutation is synthetic disposable source, not changed FF12 behavior, native execution or independent acceptance.'),indent=2)+'\n')
print('Three concrete checker failures refused; children terminal; existing positive result02 unchanged')
