"""Actual reducer CLI refusal controls for the new conditional cleanup proof.
Synthetic copies/changed normalization are labelled; never change retained source.
"""
import hashlib,importlib.util,json,pathlib,shutil,sys
W=pathlib.Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('delivery',W/'prepare-residue-packet-publication.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
out=W/'softedges-preassignment-controls-01';out.mkdir()
producer=W/'reduce-softedges-preassignment-cleanup.py'
r=json.loads((W/'softedges-preassignment-cleanup-result-01.json').read_text());checks=[]
for name,fn,pc,args in [('missing-parent-getter','softedges-array-parent-getter-code-01.json',None,None),
                       ('false-parent-store','softedges-array-descriptor-offset-code-01.json',0x632dda,'qword ptr [rcx + 0x78], rdx'),
                       ('false-borrowed-flag','softedges-member-assignment-code-01.json',0x60f01f,'eax, 0x1e')]:
 case=out/name;source=case/'source';source.mkdir(parents=True)
 for pin in r['source_pins']:
  dest=source/pin['path'];dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(W/pin['path'],dest)
 if pc is None:(source/fn).unlink()
 else:
  p=source/fn;z=json.loads(p.read_text());hits=0
  for q in z['ranges']:
   for i in q['instructions']:
    if int(i['pc'],16)==pc:i['args']=args;hits+=1
  if hits!=1:raise ValueError('control target absent/ambiguous')
  p.write_text(json.dumps(z,indent=2)+'\n')
 target=case/'must-not-exist.json';error=None
 try:m.checked_run([sys.executable,str(producer),str(target),str(source)],timeout=45,receipt_prefix=case/'invocation')
 except RuntimeError as e:error=str(e)
 if error is None or target.exists():raise AssertionError('failed prerequisite accepted '+name)
 checks.append(dict(case=name,status='PASS_REFUSED_NO_RESULT',error=error,labelled_synthetic=True))
target=W/'softedges-preassignment-cleanup-result-02.json'
m.checked_run([sys.executable,str(producer),str(target)],timeout=45,receipt_prefix=out/'positive-invocation')
valid=json.loads(target.read_text())
if valid.get('producer_complete') is not True or len(valid['exhaustive_path_partition'])!=8:raise ValueError('positive incomplete/zero cases')
result=dict(status='PASS_PRODUCER_CONTROLS',checks=checks,positive_result=target.name,
 reducer_sha256=hashlib.sha256(producer.read_bytes()).hexdigest(),positive_sha256=hashlib.sha256(target.read_bytes()).hexdigest(),
 limits='Three actual subprocess refusals plus one static reduction; no native/live runs, independent review or external audit credited.')
with (out/'result.json').open('x') as f:json.dump(result,f,indent=2)
print('Three concrete false/missing prerequisite controls refused; final02 static proof available')
