"""Focused actual CLI source-count/prerequisite controls; positive reused."""
import copy,hashlib,json,pathlib,subprocess,sys
W=pathlib.Path(__file__).resolve().parent;out=W/'texture-copy-construction-controls-01';out.mkdir()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
reader=W/'prove-texture-copy-construction.py';pos=W/'texture-copy-construction-result-01.json';v=json.loads(pos.read_text())
if not v.get('producer_complete') or v['checker_sha256']!=sha(reader):raise ValueError('missing/stale positive')
raw=json.loads((W/'texture-copy-construction-source-01.json').read_text());records=[]
for name,error in [('missing-wrapper','missing original/adapter prerequisite'),('false-copy-count','disagree'),('consistent-copy-count','wrong/incomplete construction body'),('wrong-initializer-leaf','wrong construction root/leaf')]:
    case=out/name;case.mkdir();q=copy.deepcopy(raw)
    if name=='missing-wrapper':q['wrapper_complete']=False
    elif name=='wrong-initializer-leaf':q['leaves'][1]['end_exclusive']='0x61c2ae'
    else:
        r=next(r for r in q['ranges'] if r['start']=='0x61d100');i=next(i for i in r['instructions'] if i['pc']=='0x61d143');i['args']='r8d, edi'
        if name=='consistent-copy-count':
            if i['bytes']!='448bc6':raise ValueError('wrong count mutation target')
            i['bytes']='448bc7';r['sha256']=hashlib.sha256(bytes.fromhex(''.join(i['bytes'] for i in r['instructions']))).hexdigest()
    (case/'texture-copy-construction-source-01.json').write_text(json.dumps(q,indent=2)+'\n',encoding='utf-8')
    result=case/'unexpected-result.json';p=subprocess.run([sys.executable,str(reader),str(result),str(case)],capture_output=True,timeout=30)
    (case/'stdout').write_bytes(p.stdout);(case/'stderr').write_bytes(p.stderr)
    r=dict(case=name,exit=p.returncode,result_absent=not result.exists(),expected_error=error,expected_error_seen=error in p.stderr.decode('utf-8','replace'))
    (case/'status.json').write_text(json.dumps(r,indent=2)+'\n',encoding='utf-8')
    if p.returncode==0 or not r['result_absent'] or not r['expected_error_seen']:raise ValueError(r)
    records.append(r)
r=dict(status='PASS_ACTUAL_COPY_CONSTRUCTION_REFUSALS_INDEPENDENT_PENDING',producer_complete=True,positive_reused=True,positive_result_sha256=sha(pos),refusals=records,driver_sha256=sha(pathlib.Path(__file__)),reader_sha256=sha(reader),limits='Synthetic source CLI controls only; no new positive/shipping execution/native/live/independent acceptance. All children terminal.')
(out/'result.json').write_text(json.dumps(r,indent=2)+'\n',encoding='utf-8');print(r['status'],len(records))
