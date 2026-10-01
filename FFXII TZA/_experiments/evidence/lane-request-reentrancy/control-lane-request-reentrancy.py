"""Three meaningful actual CLI refusals, reusing the sufficient positive."""
import hashlib,json,pathlib,shutil,subprocess,sys
W=pathlib.Path(__file__).resolve().parent;out=W/'lane-request-reentrancy-controls-01'
if out.exists():raise ValueError('immutable controls exist')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
d=W/'prove-lane-request-reentrancy.py';positive=W/'lane-request-reentrancy-result-01.json'
p=json.loads(positive.read_text());st=json.loads((W/'lane-request-reentrancy-positive-01.status.json').read_text())
if p.get('producer_complete') is not True or p.get('checker_sha256')!=sha(d) or st.get('exit')!=0 or st.get('checker_sha256')!=sha(d):raise ValueError('positive missing/stale')
pins=p['source_pins']+p['required_invocation_receipts']
if any(sha(W/x['path'])!=x['sha256'] for x in pins):raise ValueError('positive prerequisite changed')
names={x['path'] for x in pins};out.mkdir();cases=[]
for label,error in [('failed-capture','capture failed/stale'),('changed-pump-call','reference byte identity changed'),('missing-table','FileNotFoundError')]:
    c=out/label;c.mkdir()
    for n in names:
        f=c/n;f.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(W/n,f)
    if label=='failed-capture':
        f=c/'lane-request-reentrancy-capture-01.status.json';v=json.loads(f.read_text());v['exit']=1;f.write_text(json.dumps(v,indent=2)+'\n')
    elif label=='changed-pump-call':
        f=c/'lane-request-reentrancy-source-01.json';v=json.loads(f.read_text());q=next(q for q in v['ranges'] if q['start']=='0x32e870');i=next(i for i in q['instructions'] if i['pc']=='0x32e8aa')
        if i['mnemonic']!='call' or i['args']!='0x32e070':raise ValueError('pump preimage changed')
        i.update(bytes=(bytes([0xe8])+(0x32e040-(0x32e8aa+5)).to_bytes(4,'little',signed=True)).hex(),args='0x32e040');q['sha256']=hashlib.sha256(bytes.fromhex(''.join(i['bytes'] for i in q['instructions']))).hexdigest();f.write_text(json.dumps(v,indent=2)+'\n')
    else:(c/'lane-request-pump-dispatch-table-01.json').unlink()
    result=c/'unexpected-result.json';argv=[sys.executable,str(d),str(result),str(c)];r=subprocess.run(argv,capture_output=True)
    (c/'stdout').write_bytes(r.stdout);(c/'stderr').write_bytes(r.stderr)
    receipt=dict(case=label,argv=argv,exit=r.returncode,expected_error=error,expected_error_seen=error in r.stderr.decode(errors='replace'),result_absent=not result.exists())
    (c/'status.json').write_text(json.dumps(receipt,indent=2)+'\n')
    if r.returncode==0 or not receipt['expected_error_seen'] or not receipt['result_absent']:raise ValueError('concrete refusal failed '+label)
    cases.append(receipt)
(out/'result.json').write_text(json.dumps(dict(status='PASS_ACTUAL_REENTRY_REFUSALS_INDEPENDENT_PENDING',checker_sha256=sha(d),positive_reused=dict(path=positive.name,sha256=sha(positive)),refusals=cases,driver_sha256=sha(pathlib.Path(__file__)),limits='Three actual CLI prerequisite/identity refusals and sufficient original-code positive; not native/live runs or independent semantic acceptance'),indent=2)+'\n')
print('Three actual CLI refusals; original oldcallback/descriptor/pending-order proof reused')
