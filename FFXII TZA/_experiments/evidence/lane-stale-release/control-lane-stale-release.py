"""Actual CLI controls for the release-retry producer; positive reused."""
import hashlib,json,pathlib,shutil,subprocess,sys
W=pathlib.Path(__file__).resolve().parent;out=W/'lane-stale-release-controls-01'
if out.exists():raise ValueError('immutable controls exist')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
d=W/'prove-lane-stale-release.py';positive=W/'lane-stale-release-result-01.json'
p=json.loads(positive.read_text());st=json.loads((W/'lane-stale-release-positive-01.status.json').read_text())
if p.get('producer_complete') is not True or p.get('checker_sha256')!=sha(d) or st.get('exit')!=0 or st.get('checker_sha256')!=sha(d):raise ValueError('positive missing/stale')
if len(p.get('request_partition',[]))!=8 or p.get('early_retry_calls_or_memory_writes')!=0:raise ValueError('branch proof missing')
pins=p['source_pins']+p['required_invocation_receipts']
if any(sha(W/x['path'])!=x['sha256'] for x in pins):raise ValueError('positive prerequisite changed')
names={x['path'] for x in pins};out.mkdir();cases=[]
for label,error in [('failed-capture','capture failed/stale'),('inverted-request-gate','reference byte identity changed'),('changed-count-operation','reference byte identity changed'),('missing-source','FileNotFoundError')]:
    c=out/label;c.mkdir()
    for n in names:
        f=c/n;f.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(W/n,f)
    if label=='failed-capture':
        f=c/'lane-stale-release-capture-01.status.json';v=json.loads(f.read_text());v['exit']=1;f.write_text(json.dumps(v,indent=2)+'\n')
    elif label in ['inverted-request-gate','changed-count-operation']:
        f=c/'lane-stale-release-source-01.json';v=json.loads(f.read_text());q=next(q for q in v['ranges'] if q['start']==('0x2eafa0' if label=='inverted-request-gate' else '0x2eb890'))
        pc='0x2eafb2' if label=='inverted-request-gate' else '0x2eb8fc';i=next(i for i in q['instructions'] if i['pc']==pc)
        if label=='inverted-request-gate':
            if i['bytes']!='7572':raise ValueError('branch preimage changed')
            i.update(bytes='7472',mnemonic='je')
        else:
            if i['bytes']!='66ff89e0000000':raise ValueError('count preimage changed')
            i.update(bytes='66ff81e0000000',mnemonic='inc')
        q['sha256']=hashlib.sha256(bytes.fromhex(''.join(i['bytes'] for i in q['instructions']))).hexdigest();f.write_text(json.dumps(v,indent=2)+'\n')
    else:(c/'lane-stale-release-source-01.json').unlink()
    result=c/'unexpected-result.json';argv=[sys.executable,str(d),str(result),str(c)];r=subprocess.run(argv,capture_output=True)
    (c/'stdout').write_bytes(r.stdout);(c/'stderr').write_bytes(r.stderr)
    receipt=dict(case=label,argv=argv,exit=r.returncode,expected_error=error,expected_error_seen=error in r.stderr.decode(errors='replace'),result_absent=not result.exists())
    (c/'status.json').write_text(json.dumps(receipt,indent=2)+'\n')
    if r.returncode==0 or not receipt['expected_error_seen'] or not receipt['result_absent']:raise ValueError('concrete refusal failed '+label)
    cases.append(receipt)
(out/'result.json').write_text(json.dumps(dict(status='PASS_ACTUAL_STALE_LANE_REFUSALS_INDEPENDENT_PENDING',checker_sha256=sha(d),positive_reused=dict(path=positive.name,sha256=sha(positive)),refusals=cases,driver_sha256=sha(pathlib.Path(__file__)),limits='Four actual CLI prerequisite/identity refusals plus reused original instruction branch proof; no native/live executions or independent acceptance'),indent=2)+'\n')
print('Four concrete CLI refusals; sufficient positive and original branch partitions reused')
