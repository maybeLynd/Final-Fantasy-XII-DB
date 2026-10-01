"""Actual sparse prerequisite refusals; no repeated positive/native tests."""
import pathlib,json,hashlib,shutil,subprocess,sys
W=pathlib.Path(__file__).resolve().parent;out=W/'handle-accounting-qualification-controls-02'
if out.exists():raise ValueError('immutable controls exist')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
d=W/'prove-handle-accounting-qualification-03.py';positive=W/'handle-accounting-qualification-result-03.json'
p=json.loads(positive.read_text());st=json.loads((W/'handle-accounting-qualification-positive-03.status.json').read_text())
if p.get('producer_complete') is not True or p.get('checker_sha256')!=sha(d) or st.get('exit')!=0 or st.get('checker_sha256')!=sha(d):raise ValueError('positive missing/stale')
if any(sha(W/x['path'])!=x['sha256'] for x in p['source_pins']+p['required_invocation_receipts']):raise ValueError('positive prerequisite changed')
if sha(W/p['normalized_result']['path'])!=p['normalized_result']['sha256']:raise ValueError('normalized semantic result changed')
core=['capture-handle-accounting-qualification.py','handle-accounting-qualification-capture-01.status.json','handle-accounting-qualification-capture-01.stdout','handle-accounting-qualification-capture-01.stderr','handle-accounting-qualification-source-01.json']
tree=['capture-handle-access-release.py','handle-access-release-capture-01.status.json','handle-access-release-capture-01.stdout','handle-access-release-capture-01.stderr','handle-access-release-source-01.json']
cases=[('changed-guard-clear',core,'reference byte identity changed'),('missing-semantic-preimage',core+tree+['handle-accounting-retained-provenance-01.json','handle-accounting-retained-namebinding-deletion-source-01.json'],'FileNotFoundError')]
out.mkdir()
old=W/'handle-accounting-qualification-controls-01/failed-tree-capture'
reuse=json.loads((old/'status.json').read_text())
if not(reuse['exit'] and reuse['expected_error_seen'] and reuse['result_absent'] and reuse['normalized_absent']):raise ValueError('prior upstream refusal invalid')
shutil.copytree(old,out/'failed-tree-capture')
reuse.update(reused_receipt_sha256=sha(old/'status.json'))
receipts=[reuse]
for label,names,error in cases:
 c=out/label;c.mkdir()
 for n in names:shutil.copyfile(W/n,c/n)
 if label=='failed-tree-capture':
  f=c/'handle-access-release-capture-01.status.json';v=json.loads(f.read_text());v['exit']=1;f.write_text(json.dumps(v,indent=2)+'\n')
 elif label=='changed-guard-clear':
  f=c/'handle-accounting-qualification-source-01.json';v=json.loads(f.read_text());q=v['ranges'][0];i=next(i for i in q['instructions'] if i['pc']=='0x36c61a')
  if i['bytes']!='6689423e':raise ValueError('guard preimage moved')
  i.update(bytes='6689423f',args='word ptr [rdx + 0x3f], ax');i['memory'][0]['displacement']=0x3f;q['sha256']=hashlib.sha256(bytes.fromhex(''.join(i['bytes'] for i in q['instructions']))).hexdigest();f.write_text(json.dumps(v,indent=2)+'\n')
 result=c/'unexpected-result.json';argv=[sys.executable,str(d),str(result),str(c)];r=subprocess.run(argv,capture_output=True)
 (c/'stdout').write_bytes(r.stdout);(c/'stderr').write_bytes(r.stderr)
 rec=dict(case=label,argv=argv,exit=r.returncode,expected_error=error,expected_error_seen=error in r.stderr.decode(errors='replace'),result_absent=not result.exists(),normalized_absent=not(c/'namebinding-deletion-qualified-02.json').exists())
 (c/'status.json').write_text(json.dumps(rec,indent=2)+'\n')
 if not(r.returncode and rec['expected_error_seen'] and rec['result_absent'] and rec['normalized_absent']):raise ValueError('concrete refusal failed '+label)
 receipts.append(rec)
(out/'result.json').write_text(json.dumps(dict(status='PASS_ACTUAL_ACCOUNTING_REFUSALS_INDEPENDENT_PENDING',checker_sha256=sha(d),positive_reused=dict(path=positive.name,sha256=sha(positive)),refusals=receipts,driver_sha256=sha(pathlib.Path(__file__)),limits='Sparse actual invocation fixtures stop at the exact named prerequisite; no claim sparse fixtures are complete valid datasets. Sufficient positive reused, not repeated; no native/live/external test credit'),indent=2)+'\n')
print('Three distinct actual refusals; prior upstream refusal reused, coherent guard/preimage controls finished')
