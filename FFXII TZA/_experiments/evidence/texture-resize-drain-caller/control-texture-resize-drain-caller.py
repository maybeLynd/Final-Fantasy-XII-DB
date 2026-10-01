"""Bounded controls for actual higher-caller reduction/prerequisite path."""
import hashlib,json,pathlib,shutil,subprocess,sys
W=pathlib.Path(__file__).resolve().parent;out=W/'texture-resize-drain-caller-controls-01'
if out.exists():raise ValueError('immutable controls exist')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
positive=W/'texture-resize-drain-caller-result-01.json';r=json.loads(positive.read_text());checker=W/'prove-texture-resize-drain-caller.py'
if not r.get('producer_complete') or r['checker_sha256']!=sha(checker):raise ValueError('missing final positive')
out.mkdir();names=[p['path'] for p in r['source_pins']+r['prerequisite_result_pins']]
def bypass(z):
    q=z['ranges'][0];i=next(i for i in q['instructions'] if i['pc']=='0x628116')
    if i['bytes']!='7409':raise ValueError('branch preimage changed')
    i['bytes']='7416';i['args']='0x62812e'
    q['sha256']=hashlib.sha256(bytes.fromhex(''.join(i['bytes'] for i in q['instructions']))).hexdigest()
def fragment(z):z['pdata_entries'].pop()
def failed(z):z['producer_complete']=False
cases=[('bypass-drain','texture-resize-drain-caller-source-01.json',bypass,'higher caller full body identity changed'),('missing-tail-fragment','texture-resize-drain-caller-source-01.json',fragment,'missing normal higher caller fragments'),('failed-capacity-prerequisite','texture-copy-capacity-caller-result-02.json',failed,'required retained dependency changed'),('missing-wait-source','title-cleanup-count-selector-source-01.json',None,'FileNotFoundError')]
records=[]
for name,file,mut,error in cases:
    case=out/name;src=case/'source';src.mkdir(parents=True)
    for n in names:shutil.copyfile(W/n,src/n)
    p=src/file
    if mut is None:p.unlink()
    else:z=json.loads(p.read_text());mut(z);p.write_text(json.dumps(z,indent=2)+'\n')
    target=case/'result.json';run=subprocess.run([sys.executable,'-B',str(checker),str(target),str(src)],capture_output=True,timeout=60)
    (case/'stdout').write_bytes(run.stdout);(case/'stderr').write_bytes(run.stderr)
    q=dict(case=name,exit=run.returncode,result_absent=not target.exists(),expected_error_seen=error in run.stderr.decode(errors='replace'))
    (case/'status.json').write_text(json.dumps(q,indent=2)+'\n');records.append(q)
    if run.returncode==0 or not q['result_absent'] or not q['expected_error_seen']:raise ValueError('invalid refusal '+name)
(out/'result.json').write_text(json.dumps(dict(status='PASS_ACTUAL_HIGHER_RESIZE_REFUSALS_INDEPENDENT_PENDING',positive_reused=dict(path=positive.name,sha256=sha(positive)),checker_sha256=sha(checker),refusals=records,limits='Four producer CLI controls, no FF12/native/game executions or independent acceptance'),indent=2)+'\n');print('Four actual higher-caller CLI refusals; one final positive reused')
