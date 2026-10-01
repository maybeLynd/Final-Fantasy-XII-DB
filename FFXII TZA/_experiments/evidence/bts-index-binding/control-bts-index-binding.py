"""Actual prerequisite and identity refusals; reuse the sufficient positive result."""
import hashlib,json,pathlib,shutil,struct,subprocess,sys
W=pathlib.Path(__file__).resolve().parent;out=W/'bts-index-binding-controls-01'
if out.exists():raise ValueError('immutable controls exist')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
driver=W/'prove-bts-index-binding.py';positive=W/'bts-index-binding-result-03.json';p=json.loads(positive.read_text());st=json.loads((W/'bts-index-binding-positive-03.status.json').read_text())
if p.get('producer_complete') is not True or p.get('checker_sha256')!=sha(driver) or st.get('exit')!=0 or st.get('checker_sha256')!=sha(driver):raise ValueError('positive missing/stale')
pins=p['source_pins']+p['required_invocation_receipts']
if any(sha(W/x['path'])!=x['sha256'] for x in pins):raise ValueError('positive input moved')
out.mkdir();names={x['path'] for x in pins};cases=[]
for label,error in [('failed-capture','required capture failed or stale'),('wrong-mrf-word','original instruction identity mismatch'),('missing-focused-index','required focused index missing'),('changed-primary-coherent-pin','required primary identity set changed')]:
 c=out/label;c.mkdir()
 for n in names:
  q=c/n;q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(W/n,q)
 if label=='failed-capture':
  q=c/'bts-index-binding-capture-02.status.json';v=json.loads(q.read_text());v['exit']=1;q.write_text(json.dumps(v,indent=2)+'\n')
 else:
  q=c/'bts-index-binding-source-02.json';v=json.loads(q.read_text())
  if label=='wrong-mrf-word':
   g=next(g for g in v['ranges'] if g['start']=='0x264ed0');i=next(i for i in g['instructions'] if i['pc']=='0x264ef9');assert i['bytes']=='0fb74004';i['bytes']='0fb74006';i['args']='eax, word ptr [rax + 6]';i['memory'][0]['displacement']=6;g['sha256']=hashlib.sha256(bytes.fromhex(''.join(i['bytes'] for i in g['instructions']))).hexdigest()
  elif label=='missing-focused-index':
   g=next(g for g in v['focused_pointer_arrays'] if g['destination']=='0x215f028');assert any(i['index']==219 for i in g['values']);g['values']=[i for i in g['values'] if i['index']!=219]
  else:
   n='bts-index-binding-inputs-01/map-ref-ch.bin';p0=c/n;blob=bytearray(p0.read_bytes());a=struct.unpack_from('<I',blob,4)[0];struct.pack_into('<H',blob,a+8*73+4,94);p0.write_bytes(blob);next(p for p in v['inputs'] if p['path']==n)['sha256']=sha(p0)
  q.write_text(json.dumps(v,indent=2)+'\n')
 result=c/'unexpected-result.json';argv=[sys.executable,str(driver),str(result),str(c)];r=subprocess.run(argv,capture_output=True);(c/'stdout').write_bytes(r.stdout);(c/'stderr').write_bytes(r.stderr)
 status=dict(case=label,argv=argv,exit=r.returncode,expected_error=error,expected_error_seen=error in r.stderr.decode(errors='replace'),result_absent=not result.exists());(c/'status.json').write_text(json.dumps(status,indent=2)+'\n')
 if r.returncode==0 or not status['expected_error_seen'] or not status['result_absent']:raise ValueError('concrete refusal failed '+label)
 cases.append(status)
(out/'result.json').write_text(json.dumps(dict(status='PASS_ACTUAL_BTS_BINDING_REFUSALS_INDEPENDENT_PENDING',checker_sha256=sha(driver),positive_reused=dict(path=positive.name,sha256=sha(positive)),refusals=cases,driver_sha256=sha(pathlib.Path(__file__)),limits='Producer prerequisite/identity tests, not original FF12 execution or independent semantic acceptance'),indent=2)+'\n')
print('Four actual CLI refusals complete; positive reused; no game/original execution')
