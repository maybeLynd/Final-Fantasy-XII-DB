"""Actual upstream-artifact counterexample, repair controls and width checks."""
import copy,hashlib,importlib.util,json,shutil,subprocess,sys
from pathlib import Path
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent;ROOT=next(p for p in P.parents if(p/'Database/Tools/work/exe/FFXII_TZA.exe').is_file());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def module(n,f):
 s=importlib.util.spec_from_file_location(n,P/f);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def actual(argv,q,prefix):
 z=subprocess.run(argv,stdin=subprocess.DEVNULL,capture_output=True,timeout=45);(q/(prefix+'.stdout')).write_bytes(z.stdout);(q/(prefix+'.stderr')).write_bytes(z.stderr);receipt=dict(argv=argv,terminal=True,exit=z.returncode,exception=None);(q/(prefix+'.status.json')).write_text(json.dumps(receipt,indent=2));return z
def trim(q,base):
 for f in list(q.iterdir()):
  if f.is_file() and(base/f.name).is_file() and f.read_bytes()==(base/f.name).read_bytes():f.unlink()
def main():
 out=P/'control-result-01.json';D=P/'controls-01'
 if out.exists() or D.exists():raise ValueError('fresh controls required')
 r=json.loads((P/'result-02.json').read_text());s=json.loads((P/'proof-02.status.json').read_text())
 if r.get('producer_complete') is not True or r.get('driver_sha256')!=sha(P/'prove.py') or s.get('exit')!=0 or s.get('terminal') is not True or s.get('driver_sha256')!=sha(P/'prove.py'):raise ValueError('actual current positive absent')
 D.mkdir();files=[f for f in P.iterdir() if f.is_file()];cases=[]
 for label,marker in [('false-extent-result','required complete current extent artifact'),('false-capture-wrapper','required complete current capture wrapper'),('missing-metadata','extents-01.json'),('changed-physical-extent','extent/capture byte identity differs')]:
  q=D/label;q.mkdir()
  for f in files:shutil.copyfile(f,q/f.name)
  if label=='missing-metadata':(q/'extents-01.json').unlink()
  else:
   name='source-01.json' if label=='false-capture-wrapper' else 'extents-01.json';x=json.loads((q/name).read_text())
   if label=='false-extent-result':x['complete']=False
   elif label=='false-capture-wrapper':x['wrapper_complete']=False
   else:x['bodies'][0]['physical_bytes']='00'+x['bodies'][0]['physical_bytes'][2:]
   (q/name).write_text(json.dumps(x))
  inputs=[dict(path=f.name,sha256=sha(f),bytes=f.stat().st_size) for f in q.iterdir() if f.is_file()]
  if label=='false-extent-result':
   z=actual([sys.executable,'-B',str(q/'prove-before-prerequisite-hardening.py'),'old-accepted.json'],q,'old-producer')
   if z.returncode!=0 or not(q/'old-accepted.json').is_file() or json.loads((q/'old-accepted.json').read_text()).get('producer_complete') is not True:raise ValueError('old metadata-gap reproducer did not reproduce')
  z=actual([sys.executable,'-B',str(q/'prove.py'),'refused.json'],q,'current-producer')
  if z.returncode==0 or(q/'refused.json').exists() or marker not in z.stderr.decode(errors='replace'):raise ValueError('artifact refusal failed '+label)
  cases.append(dict(label=label,inputs=inputs,expected=marker,refused_without_result=True,old_pass_reproduced=label=='false-extent-result'));trim(q,P)
 # Same defect in the newly published sibling binder. Raw semantics were
 # independently checked; strengthen its missing artifact gate additively.
 base=ROOT/'Database/FFXII TZA/_experiments/evidence/ov42-action-table-binding';q=D/'binding-false-extent';q.mkdir()
 for f in base.iterdir():
  if f.is_file():shutil.copyfile(f,q/f.name)
 x=json.loads((q/'binding-extents-01.json').read_text());x['complete']=False;(q/'binding-extents-01.json').write_text(json.dumps(x))
 z=actual([sys.executable,'-B',str(q/'prove.py'),'old-accepted.json'],q,'old-binding-producer')
 if z.returncode!=0 or not(q/'old-accepted.json').is_file():raise ValueError('sibling binder gap not reproduced')
 z=actual([sys.executable,'-B',str(P/'qualify-binding.py'),str(q/'refused.json'),str(q)],q,'binding-qualification')
 if z.returncode==0 or(q/'refused.json').exists() or 'required complete current extent artifact' not in z.stderr.decode(errors='replace'):raise ValueError('binding qualification gap control failed')
 cases.append(dict(label='binding-false-extent',base_commit='ca2dd6483fdcd24535237d727d8ea2fa34e2c19b',old_pass_reproduced=True,new_refused_without_result=True));trim(q,base)
 M=module('cost','prove.py');G=module('cfg','prove_owner_reload_order.py');V=module('roles','validate-title-source-annotations.py');ix={}
 for f in ['source-01.json','caller-source-01.json']:
  for r in json.loads((P/f).read_text())['ranges']:ix.update({int(i['pc'],16):i for i in r['instructions']})
 controls=[]
 for label,pc,key,value in [('cost-full32',0x3056c1,'args','edx, edi'),('counter-low16',0x30578a,'args','edx, ax'),('raw-mode',0x3056f0,'args','r8d, r12d'),('omit-later-stats-read',0x305704,'args','edx, 0')]:
  a=copy.deepcopy(ix);a[pc][key]=value
  try:M.derive(a,G)
  except ValueError as e:controls.append(dict(label=label,pc=hex(pc),mutation={key:value},refused=str(e),method='Synthetic source assertion, not original execution'))
  else:raise ValueError('cost source mutation accepted')
 with out.open('x')as f:json.dump(dict(complete=True,driver_sha256=sha(Path(__file__)),positive_reused='proof-02 actual result; not another semantic run',artifact_cases=cases,source_controls=controls,limits='Two old producer PASS counterexamples demonstrate missing required artifact guards, not false original bytes. New guards reject them. No native/live experiment or independent acceptance.'),f,indent=2)
 print('VALIDATED old helper/binder metadata-gap counterexamples;5 artifact refusal cases/4 focused width-mode controls')
if __name__=='__main__':main()
