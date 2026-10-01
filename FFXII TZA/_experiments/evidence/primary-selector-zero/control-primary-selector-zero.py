"""Three actual prerequisite/identity refusals; no duplicate original execution."""
import hashlib,json,pathlib,shutil,subprocess,sys
W=pathlib.Path(__file__).resolve().parent;out=W/'primary-selector-zero-controls-01'
if out.exists():raise ValueError('immutable controls exist')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
d=W/'prove-primary-selector-zero.py';positive=W/'primary-selector-zero-result-01.json';p=json.loads(positive.read_text());s=json.loads((W/'primary-selector-zero-positive-01.status.json').read_text())
if p.get('producer_complete') is not True or p.get('checker_sha256')!=sha(d) or s.get('exit')!=0 or s.get('checker_sha256')!=sha(d):raise ValueError('positive missing/stale')
pins=p['source_pins']+p['required_invocation_receipts']
if any(sha(W/x['path'])!=x['sha256'] for x in pins):raise ValueError('positive source changed')
names={x['path'] for x in pins};out.mkdir();cases=[]
for label,error in [('failed-capture','selector capture failed/stale'),('nonconstant-leaf','reference byte identity changed'),('changed-condition-same-count','retained caller identity changed')]:
 c=out/label;c.mkdir()
 for n in names:shutil.copyfile(W/n,c/n)
 if label=='failed-capture':
  q=c/'primary-selector-zero-capture-01.status.json';v=json.loads(q.read_text());v['exit']=1;q.write_text(json.dumps(v,indent=2)+'\n')
 elif label=='nonconstant-leaf':
  q=c/'primary-selector-zero-source-01.json';v=json.loads(q.read_text());g=v['ranges'][0];i=g['instructions'][0];assert i['bytes']=='33c0';i['bytes']='33c1';i['args']='eax, ecx';g['sha256']=hashlib.sha256(bytes.fromhex(''.join(i['bytes'] for i in g['instructions']))).hexdigest();q.write_text(json.dumps(v,indent=2)+'\n')
 else:
  q=c/'index-path-raw-02.json';v=json.loads(q.read_text());g=next(g for g in v['ranges'] if g['start']=='0x32fca0');i=next(i for i in g['instructions'] if i['pc']=='0x32fce8');assert '0f95' in i['bytes'];i['bytes']=i['bytes'].replace('0f95','0f94');i['mnemonic']='sete';g['sha256']=hashlib.sha256(bytes.fromhex(''.join(i['bytes'] for i in g['instructions']))).hexdigest();q.write_text(json.dumps(v,indent=2)+'\n')
 result=c/'unexpected-result.json';argv=[sys.executable,str(d),str(result),str(c)];r=subprocess.run(argv,capture_output=True);(c/'stdout').write_bytes(r.stdout);(c/'stderr').write_bytes(r.stderr);st=dict(case=label,argv=argv,exit=r.returncode,expected_error=error,expected_error_seen=error in r.stderr.decode(errors='replace'),result_absent=not result.exists());(c/'status.json').write_text(json.dumps(st,indent=2)+'\n')
 if r.returncode==0 or not st['expected_error_seen'] or not st['result_absent']:raise ValueError('concrete refusal failed '+label)
 cases.append(st)
(out/'result.json').write_text(json.dumps(dict(status='PASS_ACTUAL_SELECTOR_REFUSALS_INDEPENDENT_PENDING',checker_sha256=sha(d),positive_reused=dict(path=positive.name,sha256=sha(positive)),refusals=cases,driver_sha256=sha(pathlib.Path(__file__)),limits='Actual producer prerequisite/identity controls, not independent semantic review or native runs'),indent=2)+'\n')
print('Three actual selector refusals; sufficient positive reused')
