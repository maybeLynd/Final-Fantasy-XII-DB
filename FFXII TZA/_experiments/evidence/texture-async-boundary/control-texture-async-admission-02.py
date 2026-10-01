"""Repair the malformed mutation control, retaining the refused original run.

The old consistent-copy fixture changed ModRM base, not displacement, so its
annotation was inconsistent and it failed earlier than intended. A same-length
XMM source-register change is byte/annotation-consistent and reaches body pins.
Reuse four completed controls and the single shipping positive; no replay.
"""
import copy,hashlib,json,pathlib,subprocess,sys
W=pathlib.Path(__file__).resolve().parent;out=W/'texture-async-admission-controls-02';out.mkdir()
reader=W/'prove-texture-async-admission-boundary.py'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
positive_path=W/'texture-async-admission-boundary-result-01.json';positive=json.loads(positive_path.read_text())
if not positive.get('producer_complete') or positive['checker_sha256']!=sha(reader):raise ValueError('missing/stale positive')
records=[]
for name in ['missing-wrapper','wrong-root','wrong-table','false-copy-role']:
    p=W/'texture-async-admission-controls-01'/name/'status.json';r=json.loads(p.read_text())
    if r['exit']==0 or not r['result_absent'] or not r['expected_error_seen']:raise ValueError('unusable historical control')
    records.append(dict(r,reused_receipt=p.relative_to(W).as_posix(),receipt_sha256=sha(p)))
raw=json.loads((W/'texture-async-count-path-source-01.json').read_text())
for name,error in [('consistent-copy-register','wrong/incomplete original body'),('missing-copy-record','mixed original bytes')]:
    case=out/name;case.mkdir();v=copy.deepcopy(raw)
    q=next(q for q in v['ranges'] if q['start']=='0x62c360');i=next(i for i in q['instructions'] if i['pc']=='0x62c40d')
    if name=='consistent-copy-register':
        if i['bytes']!='0f1101':raise ValueError('wrong mutation target')
        i['bytes']='0f1109';i['args']='xmmword ptr [rcx], xmm1'
        q['sha256']=hashlib.sha256(bytes.fromhex(''.join(z['bytes'] for z in q['instructions']))).hexdigest()
    else:q['instructions'].remove(i)
    (case/'texture-async-count-path-source-01.json').write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8')
    result=case/'unexpected-result.json'
    p=subprocess.run([sys.executable,str(reader),str(result),str(case)],capture_output=True,timeout=30)
    (case/'stdout').write_bytes(p.stdout);(case/'stderr').write_bytes(p.stderr)
    r=dict(case=name,exit=p.returncode,result_absent=not result.exists(),expected_error=error,expected_error_seen=error in p.stderr.decode('utf-8','replace'))
    (case/'status.json').write_text(json.dumps(r,indent=2)+'\n',encoding='utf-8')
    if p.returncode==0 or not r['result_absent'] or not r['expected_error_seen']:raise ValueError(r)
    records.append(r)
summary=dict(status='PASS_SIX_ACTUAL_ADMISSION_READER_REFUSALS_INDEPENDENT_PENDING',producer_complete=True,positive_reused=True,positive_result_sha256=sha(positive_path),refusals=records,driver_sha256=sha(pathlib.Path(__file__)),reader_sha256=sha(reader),failed_fixture='texture-async-admission-controls-01/consistent-copy-byte',failed_fixture_limit='Inconsistent ModRM/annotation fixture correctly refused upstream; it did not test the intended body-pin gate',limits='Synthetic source CLI controls only; no native/live or independent acceptance. All subprocesses terminal.')
(out/'result.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8');print(summary['status'],len(records))
