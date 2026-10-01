"""Four concrete CLI refusals; reuse the original positive, no native runs."""
import hashlib, importlib.util, json, pathlib, shutil, subprocess, sys

W=pathlib.Path(__file__).resolve().parent;out=W/'texture-async-bank-dispatch-controls-01'
if out.exists():raise ValueError('immutable controls exist')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
checker=W/'prove-texture-async-bank-dispatch.py';positive=W/'texture-async-bank-dispatch-result-01.json'
r=json.loads(positive.read_text());status=json.loads((W/'texture-async-bank-dispatch-positive-01.status.json').read_text())
if r.get('producer_complete') is not True or r.get('checker_sha256')!=sha(checker) or status.get('exit')!=0 or status.get('checker_sha256')!=sha(checker):raise ValueError('required positive invocation/result failed')
names=list(dict.fromkeys([p['path'] for p in r['source_pins']]+[p['path'] for p in r['required_invocation_receipts']]))
spec=importlib.util.spec_from_file_location('bank_control_roles',W/'validate-title-source-annotations.py');S=importlib.util.module_from_spec(spec);spec.loader.exec_module(S)


def mutate(source,pc,old,new,args,disp=None):
    p=source/'texture-async-bank-dispatch-source-01.json';v=json.loads(p.read_text())
    q=next(q for q in v['ranges'] if any(i['pc']==pc for i in q['instructions']))
    i=next(i for i in q['instructions'] if i['pc']==pc)
    if not i['bytes'].endswith(old):raise ValueError('mutation source preimage changed')
    i['bytes']=i['bytes'][:-len(old)]+new;i['args']=args
    if disp is not None:i['memory'][0]['displacement']=disp
    q['sha256']=hashlib.sha256(bytes.fromhex(''.join(i['bytes'] for i in q['instructions']))).hexdigest()
    S.validate(v);p.write_text(json.dumps(v,indent=2)+'\n')


out.mkdir();records=[]
for name in ('consistent-opcode','consistent-userdata-offset','missing-normal-tail','failed-capture-invocation'):
    case=out/name;source=case/'source';source.mkdir(parents=True)
    for file in names:shutil.copyfile(W/file,source/file)
    error='required bank dispatch shipping identity changed'
    if name=='consistent-opcode':
        mutate(source,'0x5feaee','2f000000','30000000','dword ptr [rcx], 0x30')
    elif name=='consistent-userdata-offset':
        mutate(source,'0x5feaf8','10','18','qword ptr [rcx + 0x18], rsi',0x18)
    elif name=='missing-normal-tail':
        p=source/'texture-async-bank-dispatch-source-01.json';v=json.loads(p.read_text())
        v['ranges']=[q for q in v['ranges'] if q['start']!='0x62ec40'];S.validate(v)
        p.write_text(json.dumps(v,indent=2)+'\n')
    else:
        p=source/'texture-async-bank-dispatch-capture-01.status.json';v=json.loads(p.read_text());v['exit']=71
        p.write_text(json.dumps(v,indent=2)+'\n');error='required bank dispatch capture invocation failed or incomplete'
    target=case/'result.json';args=[sys.executable,'-B',str(checker),str(target),str(source)]
    run=subprocess.run(args,capture_output=True,timeout=60)
    (case/'stdout').write_bytes(run.stdout);(case/'stderr').write_bytes(run.stderr)
    record=dict(case=name,argv=args,exit=run.returncode,result_absent=not target.exists(),expected_error_seen=error in run.stderr.decode(errors='replace'))
    (case/'status.json').write_text(json.dumps(record,indent=2)+'\n');records.append(record)
    if run.returncode==0 or not record['result_absent'] or not record['expected_error_seen']:raise ValueError('invalid actual refusal '+name)
(out/'result.json').write_text(json.dumps(dict(status='PASS_ACTUAL_BANK_DISPATCH_REFUSALS_INDEPENDENT_PENDING',checker_sha256=sha(checker),positive_reused=dict(path=positive.name,sha256=sha(positive)),refusals=records,limits='Four actual producer CLI refusals; original positive reused; no native/game/external review executions'),indent=2)+'\n')
print('Four actual bank-dispatch refusals; qualified original positive reused')
