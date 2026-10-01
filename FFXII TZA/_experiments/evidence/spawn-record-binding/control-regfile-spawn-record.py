"""Concrete prerequisite/identity refusals; reuse the validated positive."""
import hashlib,json,pathlib,shutil,subprocess,sys
W=pathlib.Path(__file__).resolve().parent;out=W/'regfile-spawn-record-controls-01'
if out.exists():raise ValueError('immutable controls exist')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
d=W/'prove-regfile-spawn-record.py';positive=W/'regfile-spawn-record-result-01.json'
p=json.loads(positive.read_text());st=json.loads((W/'regfile-spawn-record-positive-02.status.json').read_text())
if p.get('producer_complete') is not True or p.get('checker_sha256')!=sha(d) or st.get('exit')!=0 or st.get('checker_sha256')!=sha(d):raise ValueError('positive missing/stale')
carrier=p['submit_carrier_control']
if carrier['actor_writes']!=['0x26986c'] or carrier['excluded_failure_pop']!='0x269883' or carrier['reaching_nodes']<=0:raise ValueError('actual return-path regression control failed')
pins=p['source_pins']+p['required_invocation_receipts']
if any(sha(W/x['path'])!=x['sha256'] for x in pins):raise ValueError('positive input changed')
names={x['path'] for x in pins};out.mkdir();cases=[]
for label,error in [('failed-capture','capture failed/stale'),('different-actor-argument','reference byte identity changed'),('changed-authored-selector','authored source changed'),('missing-retained-input','FileNotFoundError')]:
    c=out/label;c.mkdir()
    for n in names:
        f=c/n;f.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(W/n,f)
    if label=='failed-capture':
        f=c/'regfile-spawn-record-capture-01.status.json';v=json.loads(f.read_text());v['exit']=1;f.write_text(json.dumps(v,indent=2)+'\n')
    elif label=='different-actor-argument':
        f=c/'regfile-spawn-record-source-01.json';v=json.loads(f.read_text());q=next(q for q in v['ranges'] if q['start']=='0x34fa70');i=next(i for i in q['instructions'] if i['pc']=='0x34fab1')
        if i['bytes']!='488bd6':raise ValueError('argument mutation preimage changed')
        i.update(bytes='488bd7',args='rdx, rdi');q['sha256']=hashlib.sha256(bytes.fromhex(''.join(i['bytes'] for i in q['instructions']))).hexdigest();f.write_text(json.dumps(v,indent=2)+'\n')
    elif label=='changed-authored-selector':
        f=c/'regfile-spawn-record-authored-01/gol_b01.s000';z=bytearray(f.read_bytes())
        if z[0x28c6:0x28c8]!=b'\x02\x00':raise ValueError('authored mutation preimage changed')
        z[0x28c6:0x28c8]=b'\x05\x00';f.write_bytes(z)
    else:(c/'regfile-spawn-record-inputs-01/section12-original-body-manifest.json').unlink()
    result=c/'unexpected-result.json';argv=[sys.executable,str(d),str(result),str(c)];r=subprocess.run(argv,capture_output=True)
    (c/'stdout').write_bytes(r.stdout);(c/'stderr').write_bytes(r.stderr)
    receipt=dict(case=label,argv=argv,exit=r.returncode,expected_error=error,expected_error_seen=error in r.stderr.decode(errors='replace'),result_absent=not result.exists())
    (c/'status.json').write_text(json.dumps(receipt,indent=2)+'\n')
    if r.returncode==0 or not receipt['expected_error_seen'] or not receipt['result_absent']:raise ValueError('concrete refusal failed '+label)
    cases.append(receipt)
(out/'result.json').write_text(json.dumps(dict(status='PASS_ACTUAL_RECORD_BINDING_REFUSALS_INDEPENDENT_PENDING',checker_sha256=sha(d),positive_reused=dict(path=positive.name,sha256=sha(positive)),return_path_control=carrier,refusals=cases,driver_sha256=sha(pathlib.Path(__file__)),limits='Four actual CLI prerequisite/identity refusals and reused original return-path control, not independent semantic acceptance or native tests'),indent=2)+'\n')
print('Four actual refusals; source-return path control and sufficient positive reused')
