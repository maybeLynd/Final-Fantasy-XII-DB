"""Three actual prerequisite refusals, reuse the sufficient valid source result."""
import hashlib,json,pathlib,shutil,subprocess,sys
W=pathlib.Path(__file__).resolve().parent;out=W/'ard-callback-width-controls-01'
if out.exists():raise ValueError('immutable controls exist')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
driver=W/'prove-ard-callback-width.py';positive=W/'ard-callback-width-result-01.json';p=json.loads(positive.read_text());s=json.loads((W/'ard-callback-width-positive-01.status.json').read_text())
if p.get('producer_complete') is not True or p.get('checker_sha256')!=sha(driver) or s.get('exit')!=0 or s.get('checker_sha256')!=sha(driver):raise ValueError('positive prerequisite failed/stale')
pins=p['source_pins']+p['required_invocation_receipts']
for x in pins:
 if sha(W/x['path'])!=x['sha256']:raise ValueError('positive source/receipt changed')
names={x['path'] for x in pins};out.mkdir();cases=[]
for label,error in [('failed-capture','required ARD capture invocation failed or stale'),('wrong-root-input','required original ARD identity changed'),('missing-loader-tail','required original ARD identity changed')]:
 case=out/label;case.mkdir()
 for n in names:shutil.copyfile(W/n,case/n)
 if label=='failed-capture':
  q=case/'ard-callback-width-capture-01.status.json';r=json.loads(q.read_text());r['exit']=1;q.write_text(json.dumps(r,indent=2)+'\n')
 else:
  q=case/'ard-callback-width-source-01.json';r=json.loads(q.read_text())
  if label=='wrong-root-input':
   rg=next(g for g in r['ranges'] if g['start']=='0x3ea710');ins=next(i for i in rg['instructions'] if i['pc']=='0x3ea732');assert ins['bytes']=='8be9';ins['bytes']='8bea';ins['args']='ebp, edx';rg['sha256']=hashlib.sha256(bytes.fromhex(''.join(i['bytes'] for i in rg['instructions']))).hexdigest()
  else:r['ranges']=[g for g in r['ranges'] if g['start']!='0x3ea947']
  q.write_text(json.dumps(r,indent=2)+'\n')
 result=case/'unexpected-result.json';argv=[sys.executable,str(driver),str(result),str(case)];x=subprocess.run(argv,capture_output=True);(case/'stdout').write_bytes(x.stdout);(case/'stderr').write_bytes(x.stderr);st=dict(case=label,argv=argv,exit=x.returncode,expected_error=error,expected_error_seen=error in x.stderr.decode(errors='replace'),result_absent=not result.exists());(case/'status.json').write_text(json.dumps(st,indent=2)+'\n')
 if x.returncode==0 or not st['expected_error_seen'] or not st['result_absent']:raise ValueError('concrete refusal failed '+label)
 cases.append(st)
(out/'result.json').write_text(json.dumps(dict(status='PASS_ACTUAL_ARD_WIDTH_REFUSALS_INDEPENDENT_PENDING',checker_sha256=sha(driver),positive_reused=dict(path=positive.name,sha256=sha(positive)),refusals=cases,driver_sha256=sha(pathlib.Path(__file__)),limits='Actual producer prerequisite/identity controls, not new original execution or independent semantic acceptance'),indent=2)+'\n')
print('Actual3 refusals; original valid source result reused')
