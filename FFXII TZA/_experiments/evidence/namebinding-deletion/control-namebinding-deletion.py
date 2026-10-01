"""Actual CLI prerequisite/identity refusals; reuse the sufficient positive.

These controls protect original-source and upstream status claims. They are
not original-code executions or independent semantic acceptance.
"""
import hashlib,json,pathlib,shutil,subprocess,sys
W=pathlib.Path(__file__).resolve().parent;out=W/'namebinding-deletion-controls-01'
if out.exists():raise ValueError('immutable controls exist')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
d=W/'prove-namebinding-deletion.py';positive=W/'namebinding-deletion-result-01.json'
p=json.loads(positive.read_text());st=json.loads((W/'namebinding-deletion-positive-01.status.json').read_text())
if p.get('producer_complete') is not True or p.get('checker_sha256')!=sha(d) or st.get('exit')!=0 or st.get('checker_sha256')!=sha(d):raise ValueError('positive missing/stale')
pins=p['source_pins']+p['required_invocation_receipts']
if any(sha(W/x['path'])!=x['sha256'] for x in pins):raise ValueError('positive prerequisite changed')
names={x['path'] for x in pins};out.mkdir();cases=[]
for label,error in [('failed-capture','capture failed/stale'),('changed-removal-mask','reference byte identity changed'),('changed-generation-clear','reference byte identity changed'),('missing-source','FileNotFoundError')]:
    c=out/label;c.mkdir()
    for n in names:
        f=c/n;f.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(W/n,f)
    if label=='failed-capture':
        f=c/'namebinding-deletion-capture-01.status.json';v=json.loads(f.read_text());v['exit']=1;f.write_text(json.dumps(v,indent=2)+'\n')
    elif label in ['changed-removal-mask','changed-generation-clear']:
        f=c/'namebinding-deletion-source-01.json';v=json.loads(f.read_text());q=next(q for q in v['ranges'] if q['start']=='0x2eaeb0')
        pc='0x2eaeb8' if label=='changed-removal-mask' else '0x2eaeff';i=next(i for i in q['instructions'] if i['pc']==pc)
        if label=='changed-removal-mask':
            if i['bytes']!='41f6c002':raise ValueError('mask preimage changed')
            i.update(bytes='41f6c004',args='r8b, 4')
        else:
            if i['bytes']!='6644894a26' or i['memory'][0]['displacement']!=0x26:raise ValueError('generation preimage changed')
            i.update(bytes='6644894a28',args='word ptr [rdx + 0x28], r9w');i['memory'][0]['displacement']=0x28
        q['sha256']=hashlib.sha256(bytes.fromhex(''.join(i['bytes'] for i in q['instructions']))).hexdigest();f.write_text(json.dumps(v,indent=2)+'\n')
    else:(c/'namebinding-deletion-source-01.json').unlink()
    result=c/'unexpected-result.json';argv=[sys.executable,str(d),str(result),str(c)];r=subprocess.run(argv,capture_output=True)
    (c/'stdout').write_bytes(r.stdout);(c/'stderr').write_bytes(r.stderr)
    receipt=dict(case=label,argv=argv,exit=r.returncode,expected_error=error,expected_error_seen=error in r.stderr.decode(errors='replace'),result_absent=not result.exists())
    (c/'status.json').write_text(json.dumps(receipt,indent=2)+'\n')
    if r.returncode==0 or not receipt['expected_error_seen'] or not receipt['result_absent']:raise ValueError('concrete refusal failed '+label)
    cases.append(receipt)
(out/'result.json').write_text(json.dumps(dict(status='PASS_ACTUAL_DELETION_REFUSALS_INDEPENDENT_PENDING',checker_sha256=sha(d),positive_reused=dict(path=positive.name,sha256=sha(positive)),refusals=cases,driver_sha256=sha(pathlib.Path(__file__)),limits='Four actual CLI prerequisite/identity refusals plus sufficient retained positive; not native execution, independent semantic acceptance or new generation-width discovery'),indent=2)+'\n')
print('Four actual CLI refusals; positive reused, no game or original-code executions')
