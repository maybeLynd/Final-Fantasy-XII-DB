"""Concrete prerequisite failures and claim-specific original-source controls."""
import copy,hashlib,importlib.util,json,shutil,subprocess,sys
from pathlib import Path
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent;sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def module(n,f):
 s=importlib.util.spec_from_file_location(n,P/f);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def main():
 C=P/'controls-01';out=P/'control-result-01.json'
 if C.exists() or out.exists():raise ValueError('fresh controls required')
 M=module('binding_proof','prove.py');M.receipt('proof-02','prove.py');r=json.loads((P/'result-02.json').read_text())
 if r.get('producer_complete') is not True or r.get('driver_sha256')!=sha(P/'prove.py'):raise ValueError('actual positive result missing/stale')
 files=[f for f in P.iterdir() if f.is_file()];C.mkdir();negatives=[]
 for label,marker in [('failed-extents','required successful current binding-extents-01'),('capture-exception','required successful current binding-capture-01'),('empty-capture-output','required nonempty clean binding-helper-capture-01'),('missing-encoder','retained-encoder-source-01.json')]:
  q=C/label;q.mkdir()
  for f in files:shutil.copyfile(f,q/f.name)
  if label in ['failed-extents','capture-exception']:
   file='binding-extents-01.status.json' if label=='failed-extents' else 'binding-capture-01.status.json';x=json.loads((q/file).read_text());x['exit']=1 if label=='failed-extents' else 0;x['exception']=None if label=='failed-extents' else 'supplied capture exception';(q/file).write_text(json.dumps(x))
  elif label=='empty-capture-output':(q/'binding-helper-capture-01.stdout').write_bytes(b'')
  else:(q/'retained-encoder-source-01.json').unlink()
  dest=q/'rejected-result.json';argv=[sys.executable,'-B',str(q/'prove.py'),dest.name]
  z=subprocess.run(argv,stdin=subprocess.DEVNULL,capture_output=True,timeout=45);(q/'actual.stdout').write_bytes(z.stdout);(q/'actual.stderr').write_bytes(z.stderr)
  refused=z.returncode!=0 and not dest.exists() and marker in z.stderr.decode(errors='replace')
  inputs=[dict(path=f.name,bytes=f.stat().st_size,sha256=sha(f)) for f in q.iterdir() if f.is_file() and f.name not in ['actual.stdout','actual.stderr']]
  receipt=dict(case=label,argv=argv,terminal=True,exit=z.returncode,exception=None,driver_sha256=sha(q/'prove.py'),expected=marker,refused_without_result=refused,inputs=inputs);(q/'actual.status.json').write_text(json.dumps(receipt,indent=2))
  if not refused:raise ValueError('actual prerequisite refusal failed '+label)
  for f in list(q.iterdir()):
   if f.is_file() and f.name not in ['actual.stdout','actual.stderr','actual.status.json'] and(P/f.name).is_file() and f.read_bytes()==(P/f.name).read_bytes():f.unlink()
  negatives.append(receipt)
 G=module('cfg','prove_owner_reload_order.py');V=module('roles','validate-title-source-annotations.py');ix={}
 for n in ['binding-source-01.json','binding-helper-source-01.json','retained-resolver-source-01.json','retained-encoder-source-01.json']:
  for r in json.loads((P/n).read_text())['ranges']:ix.update({int(i['pc'],16):i for i in r['instructions']})
 controls=[]
 for label,pc,key,val in [('full64-row-rebase',0x38460c,'args','rax, rdx'),('encoder-called-decoder',0x38465d,'args','0x20e600'),('signed-input-lost',0x237fcf,'mnemonic','mov'),('wrong-action-slot',0x237fd5,'memory',[dict(ix[0x237fd5]['memory'][0],rip_target='0x2ebf140')])]:
  a=copy.deepcopy(ix);a[pc][key]=val
  try:M.derive(a,G)
  except ValueError as e:controls.append(dict(label=label,pc=hex(pc),mutation={key:val},refused=str(e),method='Supplied source mutation, not original execution'))
  else:raise ValueError('changed source accepted '+label)
 zero=json.loads((P/'binding-source-01.json').read_text());zero['ranges']=[]
 try:V.validate(zero)
 except ValueError as e:
  if 'missing/zero original ranges' not in str(e):raise
  controls.append(dict(label='zero-source-ranges',refused=str(e),method='Actual shared annotation invocation'))
 else:raise ValueError('zero ranges accepted')
 allpaths=G.graph(ix,0x3845f0,0x3846ec);prefix=G.graph(ix,0x3845f0,0x3846ec,fixed={0x3845fa:False,0x38460a:False})
 if G.dominates(allpaths,0x38460e,0x38465d) or not G.dominates(prefix,0x38460e,0x38465d):raise ValueError('zero-row conditional-order regression')
 controls.append(dict(label='zero-row-bypasses-store',unconditional_dominance=False,nonnull_nonzero_dominance=True,method='Original local CFG, not execution',affected_failure='proof-01 rejected before result; corrected producer02 condition is required'))
 with out.open('x') as f:json.dump(dict(complete=True,driver_sha256=sha(Path(__file__)),positive_reused=dict(receipt='proof-02.status.json',sha256=sha(P/'proof-02.status.json'),credit='Existing actual producer; not another run'),actual_cli_negatives=negatives,source_countercontrols=controls,limits='Producer controls only. Mathematical alias/rebind countermodels are not original/native/live runs or independent project acceptance.'),f,indent=2)
 print('VALIDATED4 concrete prerequisite refusals and6 focused source/CFG controls; no missing or empty upstream evidence passes')
if __name__=='__main__':main()
