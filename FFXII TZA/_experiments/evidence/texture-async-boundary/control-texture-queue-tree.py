"""Actual original-source reducer failure controls; positive result reused."""
import copy,hashlib,json,pathlib,subprocess,sys
W=pathlib.Path(__file__).resolve().parent;out=W/'texture-queue-tree-controls-01';out.mkdir()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
reader=W/'prove-texture-queue-tree-boundary.py';positive_path=W/'texture-queue-tree-result-01.json'
positive=json.loads(positive_path.read_text())
if not positive.get('producer_complete') or positive['checker_sha256']!=sha(reader):raise ValueError('missing/stale positive')
raw=json.loads((W/'texture-queue-tree-source-02.json').read_text());records=[]
for name,error in [('missing-wrapper','missing original/adapter prerequisite'),('false-count-field','disagree'),('consistent-count-byte','wrong/incomplete tree body'),('wrong-helper-extent','wrong helper leaf boundaries')]:
    case=out/name;case.mkdir();v=copy.deepcopy(raw)
    if name=='missing-wrapper':v['wrapper_complete']=False
    elif name=='wrong-helper-extent':v['leaves'][1]['end_exclusive']='0x16da55'
    else:
        q=next(q for q in v['ranges'] if q['start']=='0x199db0');i=next(i for i in q['instructions'] if i['pc']=='0x199e93')
        i['args']='dword ptr [rbp + 0x38]';i['memory'][0]['displacement']=0x38
        if name=='consistent-count-byte':
            if i['bytes']!='ff4528':raise ValueError('wrong count mutation target')
            i['bytes']='ff4538';q['sha256']=hashlib.sha256(bytes.fromhex(''.join(z['bytes'] for z in q['instructions']))).hexdigest()
    (case/'texture-queue-tree-source-02.json').write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8')
    result=case/'unexpected-result.json';p=subprocess.run([sys.executable,str(reader),str(result),str(case)],capture_output=True,timeout=30)
    (case/'stdout').write_bytes(p.stdout);(case/'stderr').write_bytes(p.stderr)
    r=dict(case=name,exit=p.returncode,result_absent=not result.exists(),expected_error=error,expected_error_seen=error in p.stderr.decode('utf-8','replace'))
    (case/'status.json').write_text(json.dumps(r,indent=2)+'\n',encoding='utf-8')
    if p.returncode==0 or not r['result_absent'] or not r['expected_error_seen']:raise ValueError(r)
    records.append(r)
summary=dict(status='PASS_ACTUAL_TREE_REDUCER_REFUSALS_INDEPENDENT_PENDING',producer_complete=True,positive_reused=True,positive_result_sha256=sha(positive_path),refusals=records,driver_sha256=sha(pathlib.Path(__file__)),reader_sha256=sha(reader),limits='Producer CLI controls on synthetic altered source, not native execution, new shipping samples or independent acceptance. All children terminal.')
(out/'result.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8');print(summary['status'],len(records))
