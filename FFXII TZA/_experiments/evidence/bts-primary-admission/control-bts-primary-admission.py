"""Actual source/upstream refusals for the original primary-admission reducer."""
import hashlib,json,pathlib,shutil,subprocess,sys
W=pathlib.Path(__file__).resolve().parent;out=W/'bts-primary-admission-controls-01'
if out.exists():raise ValueError('immutable controls exist')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
d=W/'prove-bts-primary-admission.py';positive=W/'bts-primary-admission-result-02.json';p=json.loads(positive.read_text());s=json.loads((W/'bts-primary-admission-positive-02.status.json').read_text())
if p.get('producer_complete') is not True or p.get('checker_sha256')!=sha(d) or s.get('exit')!=0 or s.get('checker_sha256')!=sha(d):raise ValueError('positive missing/stale')
pins=p['source_pins']+p['required_invocation_receipts']
if any(sha(W/x['path'])!=x['sha256'] for x in pins):raise ValueError('input changed')
names={x['path'] for x in pins};out.mkdir();cases=[]
for label,error in [('failed-capture','primary capture failed/stale'),('wrong-positive-guard','primary original bytes changed'),('missing-upstream','upstream canonical manifest missing/changed')]:
 c=out/label;c.mkdir()
 for n in names:shutil.copyfile(W/n,c/n)
 extra=[]
 if label=='failed-capture':
  q=c/'bts-primary-admission-capture-01.status.json';v=json.loads(q.read_text());v['exit']=1;q.write_text(json.dumps(v,indent=2)+'\n')
 elif label=='wrong-positive-guard':
  q=c/'bts-primary-admission-source-01.json';v=json.loads(q.read_text());g=v['ranges'][0];i=next(i for i in g['instructions'] if i['pc']=='0x330378');assert i['bytes'].startswith('0f8e');i['bytes']='0f8f'+i['bytes'][4:];i['mnemonic']='jg';g['sha256']=hashlib.sha256(bytes.fromhex(''.join(i['bytes'] for i in g['instructions']))).hexdigest();q.write_text(json.dumps(v,indent=2)+'\n')
 else:
  up=c/'absent-upstream';up.mkdir();extra=[str(up)]
 result=c/'unexpected-result.json';argv=[sys.executable,str(d),str(result),str(c)]+extra;r=subprocess.run(argv,capture_output=True);(c/'stdout').write_bytes(r.stdout);(c/'stderr').write_bytes(r.stderr);st=dict(case=label,argv=argv,exit=r.returncode,expected_error=error,expected_error_seen=error in r.stderr.decode(errors='replace'),result_absent=not result.exists());(c/'status.json').write_text(json.dumps(st,indent=2)+'\n')
 if r.returncode==0 or not st['expected_error_seen'] or not st['result_absent']:raise ValueError('concrete refusal failed '+label)
 cases.append(st)
(out/'result.json').write_text(json.dumps(dict(status='PASS_ACTUAL_PRIMARY_ADMISSION_REFUSALS_INDEPENDENT_PENDING',checker_sha256=sha(d),positive_reused=dict(path=positive.name,sha256=sha(positive)),refusals=cases,driver_sha256=sha(pathlib.Path(__file__)),limits='Producer prerequisites/identity only; not new original-code execution/independent acceptance'),indent=2)+'\n')
print('Three actual primary-admission refusals; positive reused')
