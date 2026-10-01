"""Concrete chained-tail, predicate and checked-upstream controls."""
import copy,hashlib,json,pathlib,shutil,subprocess,sys
W=pathlib.Path(__file__).resolve().parent;out=W/'texture-copy-capacity-caller-controls-01';out.mkdir()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
reader=W/'prove-texture-copy-capacity-caller.py';positive_path=W/'texture-copy-capacity-caller-result-02.json';positive=json.loads(positive_path.read_text())
if not positive.get('producer_complete') or positive['checker_sha256']!=sha(reader):raise ValueError('missing/stale positive')
records=[]
for name,error in [('missing-helper-result','FileNotFoundError'),('failed-helper-result','missing/failed helper prerequisite'),('consistent-wrong-min','wrong/incomplete capacity caller body'),('missing-chained-fragment','missing normal caller fragments')]:
    case=out/name;case.mkdir()
    for n in ['texture-copy-capacity-caller-source-01.json','texture-copy-construction-source-01.json','texture-copy-construction-result-01.json']:
        if name=='missing-helper-result' and n.endswith('result-01.json'):continue
        shutil.copyfile(W/n,case/n)
    if name=='failed-helper-result':
        p=case/'texture-copy-construction-result-01.json';v=json.loads(p.read_text());v['producer_complete']=False;p.write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8')
    elif name in ('consistent-wrong-min','missing-chained-fragment'):
        p=case/'texture-copy-capacity-caller-source-01.json';v=json.loads(p.read_text())
        if name=='missing-chained-fragment':v['pdata_entries'].pop()
        else:
            q=v['ranges'][0];i=next(i for i in q['instructions'] if i['pc']=='0x627de4')
            if i['bytes']!='440f42ce':raise ValueError('wrong min mutation target')
            i['bytes']='440f47ce';i['mnemonic']='cmova';q['sha256']=hashlib.sha256(bytes.fromhex(''.join(i['bytes'] for i in q['instructions']))).hexdigest()
        p.write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8')
    result=case/'unexpected-result.json';p=subprocess.run([sys.executable,str(reader),str(result),str(case)],capture_output=True,timeout=30)
    (case/'stdout').write_bytes(p.stdout);(case/'stderr').write_bytes(p.stderr)
    r=dict(case=name,exit=p.returncode,result_absent=not result.exists(),expected_error=error,expected_error_seen=error in p.stderr.decode('utf-8','replace'))
    (case/'status.json').write_text(json.dumps(r,indent=2)+'\n',encoding='utf-8')
    if p.returncode==0 or not r['result_absent'] or not r['expected_error_seen']:raise ValueError(r)
    records.append(r)
r=dict(status='PASS_ACTUAL_CAPACITY_CALLER_REFUSALS_INDEPENDENT_PENDING',producer_complete=True,positive_reused=True,positive_result_sha256=sha(positive_path),refusals=records,driver_sha256=sha(pathlib.Path(__file__)),reader_sha256=sha(reader),limits='Producer CLI controls on altered/missing source; no native/live, independent acceptance or extra positive capture. All children terminal.')
(out/'result.json').write_text(json.dumps(r,indent=2)+'\n',encoding='utf-8');print(r['status'],len(records))
