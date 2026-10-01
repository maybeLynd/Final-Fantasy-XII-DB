"""Actual new CLI regression: reviewer fast-CALL counterexample and dependencies.

One positive is reused. Fresh disposable outputs; never modify published input.
Controls are producer tests, not FF12 executions or independent acceptance.
"""
import hashlib,importlib.util,json,pathlib,shutil,struct,subprocess,sys
W=pathlib.Path(__file__).resolve().parent;out=W/'title-tracker-qualification-controls-02'
if out.exists():raise ValueError('immutable control output exists')
positive=W/'title-tracker-callback-boundary-result-02.json';v=json.loads(positive.read_text())
checker=W/'prove-title-tracker-callback-boundary-02.py'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
if v.get('producer_complete') is not True or v.get('checker_sha256')!=sha(checker) or v['prerequisite_execution']['exit']!=0:raise ValueError('missing/failed final positive')
out.mkdir();names=['title-tracker-cleanup-source-01.json','title-cleanup-callback-queue-source-01.json']
spec=importlib.util.spec_from_file_location('actual_annotation_control',W/'validate-title-source-annotations.py');S=importlib.util.module_from_spec(spec);spec.loader.exec_module(S)
def fast_call(z):
    q=next(r for r in z['ranges'] if r['start']=='0x185a90');k=next(k for k,i in enumerate(q['instructions']) if i['pc']=='0x185ad2')
    if ''.join(i['bytes'] for i in q['instructions'][k:k+2])!='4883c438c3':raise ValueError('reviewer counterexample preimage changed')
    q['instructions'][k:k+2]=[dict(pc='0x185ad2',bytes='e8'+struct.pack('<i',0x1858a0-0x185ad7).hex(),mnemonic='call',args='0x1858a0',memory=[])]
    q['sha256']=hashlib.sha256(bytes.fromhex(''.join(i['bytes'] for i in q['instructions']))).hexdigest()
def cfg(z):z['normal_cfg']['returns']=[]
def role(z):
    next(i for r in z['ranges'] for i in r['instructions'] if i['pc']=='0x185acf')['memory'][0]['role']='r'
def incomplete(z):z['wrapper_complete']=False
cases=[('reviewer-fast-call',names[1],fast_call,'original full body identity changed'),('forged-recorded-cfg',names[0],cfg,'recorded CFG differs'),('old-store-role',names[1],role,'memory/address/access annotation disagrees'),('failed-upstream-wrapper',names[0],incomplete,'missing original/adapter prerequisite'),('missing-source',names[1],None,'FileNotFoundError')]
records=[]
for label,name,mutation,error in cases:
    case=out/label;src=case/'source';src.mkdir(parents=True)
    for n in names:shutil.copyfile(W/n,src/n)
    p=src/name
    if mutation is None:p.unlink()
    else:
        z=json.loads(p.read_text());mutation(z)
        if label=='reviewer-fast-call':S.validate(z) # consistent real CALL, not an annotation mismatch
        p.write_text(json.dumps(z,indent=2)+'\n')
    target=case/'result.json';run=subprocess.run([sys.executable,'-B',str(checker),str(target),str(src)],capture_output=True,timeout=60)
    (case/'stdout').write_bytes(run.stdout);(case/'stderr').write_bytes(run.stderr)
    record=dict(case=label,exit=run.returncode,result_absent=not target.exists(),retained_output_absent=not (case/'result-retained-producer.json').exists(),expected_error_seen=error in run.stderr.decode(errors='replace'))
    (case/'status.json').write_text(json.dumps(record,indent=2)+'\n');records.append(record)
    if run.returncode==0 or not all(record[k] for k in ('result_absent','retained_output_absent','expected_error_seen')):raise ValueError('invalid refusal control '+label)
r=dict(status='PASS_ACTUAL_TITLE_TRACKER_QUALIFICATION_REFUSALS_INDEPENDENT_PENDING',positive_reused=dict(path=positive.name,sha256=sha(positive)),checker_sha256=sha(checker),controls_sha256=sha(pathlib.Path(__file__)),refusals=records,limits='Five synthetic producer CLI controls; no game/native runs, original semantic proof unchanged; reviewer executions not ours')
(out/'result.json').write_text(json.dumps(r,indent=2)+'\n');print('Five actual qualification refusals including consistent reviewer CALL; original positive reused')
