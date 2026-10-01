"""Actual scoped frame composition refusals; preserve and reuse positive02."""
import hashlib,importlib.util,json,pathlib,shutil,subprocess,sys
W=pathlib.Path(__file__).resolve().parent;out=W/'texture-async-callback-frame-controls-01'
if out.exists():raise ValueError('immutable controls exist')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
checker=W/'prove-texture-async-callback-frame.py';positive=W/'texture-async-callback-frame-result-01.json'
r=json.loads(positive.read_text());status=json.loads((W/'texture-async-callback-frame-positive-02.status.json').read_text())
if r.get('producer_complete') is not True or r.get('checker_sha256')!=sha(checker) or status.get('exit')!=0 or status.get('checker_sha256')!=sha(checker):raise ValueError('required actual positive invocation failed')
names=list(dict.fromkeys([q['path'] for q in r['source_pins']+r['required_invocation_receipts']]))+['capture-index-path.py']
spec=importlib.util.spec_from_file_location('callback_frame_control_roles',W/'validate-title-source-annotations.py');S=importlib.util.module_from_spec(spec);spec.loader.exec_module(S)

def mutate(source,name,pc,old,new,args,disp=None,size=None):
 p=source/name;v=json.loads(p.read_text());q=next(q for q in v['ranges'] if any(i['pc']==pc for i in q['instructions']))
 i=next(i for i in q['instructions'] if i['pc']==pc)
 if old not in i['bytes']:raise ValueError('mutation preimage changed')
 i['bytes']=i['bytes'].replace(old,new,1);i['args']=args
 if disp is not None:i['memory'][0]['displacement']=disp
 if size is not None:i['memory'][0]['size']=size
 q['sha256']=hashlib.sha256(bytes.fromhex(''.join(i['bytes'] for i in q['instructions']))).hexdigest()
 S.validate(v);p.write_text(json.dumps(v,indent=2)+'\n')

out.mkdir();records=[]
for name in ('consistent-frame-data-offset','consistent-bank-read-width','missing-frame-store','failed-bank-invocation'):
 case=out/name;source=case/'source';source.mkdir(parents=True)
 for n in names:shutil.copyfile(W/n,source/n)
 if name=='consistent-frame-data-offset':
  mutate(source,'render-executor-consumption-raw-01.json','0x60a8ca','a0','98','rax, qword ptr [rbx - 0x68]',-0x68)
  error='required retained executor identity changed'
 elif name=='consistent-bank-read-width':
  mutate(source,'texture-async-bank-dispatch-source-01.json','0x186610','8b','8a','dl, byte ptr [rcx + 0x10]',size=1)
  p=source/'texture-async-bank-dispatch-result-01.json';v=json.loads(p.read_text())
  for pin in v['source_pins']:
   if pin['path']=='texture-async-bank-dispatch-source-01.json':pin['sha256']=sha(source/pin['path'])
  p.write_text(json.dumps(v,indent=2)+'\n');error='required retained bank identity changed'
 elif name=='missing-frame-store':
  p=source/'render-executor-consumption-raw-01.json';v=json.loads(p.read_text());q=next(q for q in v['ranges'] if q['start']=='0x60a410')
  q['instructions']=[i for i in q['instructions'] if i['pc']!='0x60a8ce']
  p.write_text(json.dumps(v,indent=2)+'\n');error='empty/mixed original bytes'
 else:
  p=source/'texture-async-bank-dispatch-positive-01.status.json';v=json.loads(p.read_text());v['exit']=71
  p.write_text(json.dumps(v,indent=2)+'\n');error='required bank producer invocation/result failed or stale'
 target=case/'result.json';args=[sys.executable,'-B',str(checker),str(target),str(source)]
 run=subprocess.run(args,capture_output=True,timeout=60)
 (case/'stdout').write_bytes(run.stdout);(case/'stderr').write_bytes(run.stderr)
 record=dict(case=name,argv=args,exit=run.returncode,result_absent=not target.exists(),expected_error_seen=error in run.stderr.decode(errors='replace'))
 (case/'status.json').write_text(json.dumps(record,indent=2)+'\n');records.append(record)
 if not run.returncode or not record['result_absent'] or not record['expected_error_seen']:raise ValueError('invalid actual refusal '+name)
(out/'result.json').write_text(json.dumps(dict(status='PASS_ACTUAL_CALLBACK_FRAME_REFUSALS_INDEPENDENT_PENDING',checker_sha256=sha(checker),positive_reused=dict(path=positive.name,sha256=sha(positive)),refusals=records,limits='Four actual producer CLI refusals; positive02 reused; no recapture/native/game/external review executions'),indent=2)+'\n')
print('Four actual callback-frame refusals; qualified positive02 reused')
