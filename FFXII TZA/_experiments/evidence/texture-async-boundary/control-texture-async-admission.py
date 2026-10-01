"""Focused actual reducer refusals; reuse the completed positive, no native run."""
import copy,hashlib,json,pathlib,subprocess,sys
W=pathlib.Path(__file__).resolve().parent
out=W/'texture-async-admission-controls-01';out.mkdir()
raw=json.loads((W/'texture-async-count-path-source-01.json').read_text())
positive_path=W/'texture-async-admission-boundary-result-01.json'
positive=json.loads(positive_path.read_text())
reader=W/'prove-texture-async-admission-boundary.py'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
if not positive.get('producer_complete') or positive['checker_sha256']!=sha(reader):raise ValueError('missing/stale positive')
expected={
 'missing-wrapper':'missing original/adapter prerequisite',
 'wrong-root':'root/leaf prerequisite changed',
 'wrong-table':'physical RTTI/slot0 prerequisite changed',
 'false-copy-role':'disagree',
 'consistent-copy-byte':'wrong/incomplete original body',
 'missing-copy-record':'assembled bytes disagree',
}
records=[]
for name,error in expected.items():
    case=out/name;case.mkdir();v=copy.deepcopy(raw)
    if name=='missing-wrapper':v['wrapper_complete']=False
    elif name=='wrong-root':v['pdata_entries'][1][2]+=4
    elif name=='wrong-table':v['table']['slot0']='0x622000'
    else:
        q=next(q for q in v['ranges'] if q['start']=='0x62c360')
        i=next(i for i in q['instructions'] if i['pc']=='0x62c40d')
        if name=='false-copy-role':i['memory'][0]['role']='r'
        elif name=='consistent-copy-byte':
            # Store offset C0 changes to C1, with a matching annotation and raw hash.
            b=bytearray.fromhex(i['bytes']);b[-1]+=1;i['bytes']=b.hex()
            i['args']=i['args'].replace('[rcx]', '[rcx + 1]')
            i['memory'][0]['displacement']+=1
            q['sha256']=hashlib.sha256(bytes.fromhex(''.join(z['bytes'] for z in q['instructions']))).hexdigest()
        else:q['instructions'].remove(i)
    source=case/'texture-async-count-path-source-01.json'
    source.write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8')
    result=case/'unexpected-result.json'
    p=subprocess.run([sys.executable,str(reader),str(result),str(case)],capture_output=True,timeout=30)
    (case/'stdout').write_bytes(p.stdout);(case/'stderr').write_bytes(p.stderr)
    r=dict(case=name,exit=p.returncode,result_absent=not result.exists(),expected_error=error,expected_error_seen=error in p.stderr.decode('utf-8','replace'))
    (case/'status.json').write_text(json.dumps(r,indent=2)+'\n',encoding='utf-8')
    if p.returncode==0 or not r['result_absent'] or not r['expected_error_seen']:raise ValueError(r)
    records.append(r)
summary=dict(status='PASS_ACTUAL_ADMISSION_READER_REFUSALS_INDEPENDENT_PENDING',producer_complete=True,positive_reused=True,positive_result_sha256=sha(positive_path),refusals=records,driver_sha256=sha(pathlib.Path(__file__)),reader_sha256=sha(reader),limits='Synthetic altered-source CLI controls only, not shipping-code execution, independent acceptance or live observation; all subprocesses terminal')
(out/'result.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8')
print(summary['status'],len(records))
