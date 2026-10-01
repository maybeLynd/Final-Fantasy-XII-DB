"""Concrete actual-reader controls; reuse the one completed positive result."""
import copy,hashlib,json,pathlib,subprocess,sys
W=pathlib.Path(__file__).resolve().parent;out=W/'title-reset-order-controls-01';out.mkdir()
raw=json.loads((W/'title-reset-order-source-01.json').read_text())
positive=json.loads((W/'title-reset-order-result-01.json').read_text())
assert positive.get('producer_complete') is True and len(positive['established'])==6
records=[]
for name in ['missing-wrapper','false-object-annotation','consistent-al-zero','wrong-root']:
    case=out/name;case.mkdir();v=copy.deepcopy(raw)
    if name=='missing-wrapper':v['wrapper_complete']=False
    elif name=='false-object-annotation':
        next(i for q in v['ranges'] for i in q['instructions'] if i['pc']=='0x611f8f')['args']='rbx, rcx'
    elif name=='consistent-al-zero':
        q=next(q for q in v['ranges'] if q['start']=='0x611f80');i=next(i for i in q['instructions'] if i['pc']=='0x611fda');i['bytes']='b000';i['args']='al, 0'
        q['sha256']=hashlib.sha256(bytes.fromhex(''.join(i['bytes'] for i in q['instructions']))).hexdigest()
    else:v['pdata_entries'][0][2]+=4
    (case/'title-reset-order-source-01.json').write_text(json.dumps(v,indent=2)+'\n')
    result=case/'unexpected-result.json';args=[sys.executable,str(W/'prove-title-reset-order.py'),str(result),str(case)]
    p=subprocess.run(args,capture_output=True,timeout=30)
    (case/'stdout').write_bytes(p.stdout);(case/'stderr').write_bytes(p.stderr)
    expected={'missing-wrapper':'missing original/adapter prerequisite','false-object-annotation':'disagree','consistent-al-zero':'wrong/incomplete original body','wrong-root':'wrong named root metadata'}[name]
    record=dict(case=name,exit=p.returncode,result_absent=not result.exists(),expected_error=expected,expected_error_seen=expected in p.stderr.decode('utf-8','replace'))
    (case/'status.json').write_text(json.dumps(record,indent=2)+'\n')
    assert record['exit']!=0 and record['result_absent'] and record['expected_error_seen'],record
    records.append(record)
summary=dict(status='PASS_ACTUAL_READER_REFUSALS_INDEPENDENT_PENDING',producer_complete=True,positive_result_sha256=hashlib.sha256((W/'title-reset-order-result-01.json').read_bytes()).hexdigest(),positive_reused=True,refusals=records,
             driver_sha256=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),reader_sha256=hashlib.sha256((W/'prove-title-reset-order.py').read_bytes()).hexdigest(),limits='Producer CLI regression controls, not independent acceptance or native/live tests. All subprocesses terminal.')
(out/'result.json').write_text(json.dumps(summary,indent=2)+'\n');print(summary['status'],len(records))
