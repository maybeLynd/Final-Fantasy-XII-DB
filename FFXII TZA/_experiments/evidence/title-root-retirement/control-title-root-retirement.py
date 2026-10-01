"""Three concrete invocation/prerequisite refusals; reuse valid positive once."""
import hashlib,json,pathlib,shutil,subprocess,sys
W=pathlib.Path(__file__).resolve().parent;out=W/'title-root-retirement-controls-01'
if out.exists():raise ValueError('immutable controls exist')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
driver=W/'prove-title-root-retirement.py';positive=W/'title-root-retirement-result-01.json'
p=json.loads(positive.read_text());st=json.loads((W/'title-root-retirement-positive-01.status.json').read_text())
if p.get('producer_complete') is not True or p.get('checker_sha256')!=sha(driver) or st.get('exit')!=0 or st.get('checker_sha256')!=sha(driver):raise ValueError('positive prerequisite failed or stale')
names={x['path'] for x in p['source_pins']+p['retained_source_pins']+p['required_invocation_receipts']}
for x in p['source_pins']+p['retained_source_pins']+p['required_invocation_receipts']:
 if sha(W/x['path'])!=x['sha256']:raise ValueError('positive input changed')
out.mkdir();refusals=[]
for label,error in [('failed-producer','required root capture invocation failed or stale'),('changed-root-retention','required original root identity changed'),('missing-owner-body','required retained source identity changed')]:
 case=out/label;case.mkdir()
 for name in names:
  q=case/name;q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(W/name,q)
 if label=='failed-producer':
  q=case/'title-root-retirement-capture-02.status.json';x=json.loads(q.read_text());x['exit']=1;q.write_text(json.dumps(x,indent=2)+'\n')
 elif label=='changed-root-retention':
  q=case/'title-root-retirement-source-01.json';x=json.loads(q.read_text());rg=next(r for r in x['ranges'] if r['start']=='0x2445d0');ins=next(i for i in rg['instructions'] if i['pc']=='0x2445d8');assert ins['bytes']=='83494023';ins['bytes']='83494003';ins['args']='dword ptr [rcx + 0x40], 3';rg['sha256']=hashlib.sha256(bytes.fromhex(''.join(i['bytes'] for i in rg['instructions']))).hexdigest();q.write_text(json.dumps(x,indent=2)+'\n')
 else:
  q=case/'title-watcher-lifetime-raw-02.json';x=json.loads(q.read_text());x['ranges']=[r for r in x['ranges'] if r['start']!='0x2495c0'];q.write_text(json.dumps(x,indent=2)+'\n')
 result=case/'unexpected-result.json';argv=[sys.executable,str(driver),str(result),str(case)];run=subprocess.run(argv,capture_output=True)
 (case/'stdout').write_bytes(run.stdout);(case/'stderr').write_bytes(run.stderr);receipt=dict(argv=argv,exit=run.returncode,expected_error=error,expected_error_seen=error in run.stderr.decode(errors='replace'),result_absent=not result.exists());(case/'status.json').write_text(json.dumps(receipt,indent=2)+'\n')
 if run.returncode==0 or not receipt['expected_error_seen'] or not receipt['result_absent']:raise ValueError('actual concrete refusal failed '+label)
 refusals.append(dict(case=label,**receipt))
(out/'result.json').write_text(json.dumps(dict(status='PASS_ACTUAL_TITLE_RETENTION_REFUSALS_INDEPENDENT_PENDING',checker_sha256=sha(driver),positive_reused=dict(path=positive.name,sha256=sha(positive)),refusals=refusals,driver_sha256=sha(pathlib.Path(__file__)),limits='Producer invocation/identity controls, not independent semantic acceptance or original-code execution'),indent=2)+'\n')
print('Actual3 concrete refusals; valid positive reused, no extra game/native runs')
