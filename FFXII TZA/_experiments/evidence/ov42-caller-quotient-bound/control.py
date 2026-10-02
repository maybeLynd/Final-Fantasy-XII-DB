"""Actual retained-input failures and claim-specific supplied-code controls."""
import copy,hashlib,importlib.util,json,shutil,subprocess,sys
from pathlib import Path
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent;sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def module(n,f):
 s=importlib.util.spec_from_file_location(n,P/f);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def main():
 C=P/'controls-01';out=P/'control-result-01.json'
 if C.exists() or out.exists():raise ValueError('fresh controls required')
 z=json.loads((P/'proof-02.status.json').read_text());r=json.loads((P/'result-02.json').read_text())
 if z.get('terminal') is not True or z.get('exit')!=0 or z.get('exception') is not None or z.get('driver_sha256')!=sha(P/'prove.py') or r.get('producer_complete') is not True or r['driver_sha256']!=sha(P/'prove.py') or not(P/'proof-02.stdout').read_bytes() or(P/'proof-02.stderr').read_bytes():raise ValueError('actual positive missing')
 base=[q for q in P.iterdir() if q.is_file()];C.mkdir();cases=[]
 for name,marker in [('missing-queue','queue-source-01.json'),('missing-lineage-member','retained source population differs'),('changed-current-bound','retained member changed')]:
  q=C/name;q.mkdir()
  for f in base:shutil.copyfile(f,q/f.name)
  if name=='missing-queue':(q/'queue-source-01.json').unlink()
  elif name=='missing-lineage-member':
   f=q/'lineage.json';x=json.loads(f.read_text());x.pop();f.write_text(json.dumps(x))
  else:
   f=q/'caller-source-01.json';x=json.loads(f.read_text())
   i=next(i for r in x['ranges'] for i in r['instructions'] if i['pc']=='0x3048a8');i['args']='ebx, 0xffff';f.write_text(json.dumps(x))
  dest=q/'rejected-result.json';argv=[sys.executable,'-B',str(q/'prove.py'),str(dest)]
  actual=subprocess.run(argv,stdin=subprocess.DEVNULL,capture_output=True,timeout=45)
  (q/'actual.stdout').write_bytes(actual.stdout);(q/'actual.stderr').write_bytes(actual.stderr)
  refused=actual.returncode!=0 and not dest.exists() and marker in actual.stderr.decode(errors='replace')
  inputs=[dict(path=f.name,bytes=f.stat().st_size,sha256=sha(f)) for f in q.iterdir() if f.is_file() and f.name not in ['actual.stdout','actual.stderr']]
  receipt=dict(case=name,argv=argv,terminal=True,exit=actual.returncode,exception=None,driver_sha256=sha(q/'prove.py'),expected=marker,refused_without_result=refused,inputs=inputs)
  (q/'actual.status.json').write_text(json.dumps(receipt,indent=2))
  if not refused:raise ValueError('actual prerequisite control failed '+name)
  for f in list(q.iterdir()):
   if f.is_file() and f.name not in ['actual.stdout','actual.stderr','actual.status.json'] and(P/f.name).is_file() and f.read_bytes()==(P/f.name).read_bytes():f.unlink()
  cases.append(receipt)
 M=module('composition','prove.py');G=module('cfg','prove_owner_reload_order.py');V=module('roles','validate-title-source-annotations.py');ix={}
 for f in ['caller-source-01.json','caller-source-02.json','queue-source-01.json']:
  for r in json.loads((P/f).read_text())['ranges']:ix.update({int(i['pc'],16):i for i in r['instructions']})
 import struct
 c=json.loads((P/'carrier-result-01.json').read_text());t=bytes.fromhex(next(q for q in c['original_data'] if q['address']=='0x305044')['bytes']);targets=[0x120000+n for n in struct.unpack('<13I',t)]
 counters=[]
 for label,pc,key,value in [('wrong-lookup-site',0x3068a2,'args','0x20e620'),('full64-row-add',0x304934,'args','r15, rcx'),('signed-division',0x3068b8,'mnemonic','idiv'),('current-bound65535',0x3048a8,'args','ebx, 0xffff')]:
  a=copy.deepcopy(ix);a[pc][key]=value
  try:M.derive(a,targets,G)
  except ValueError as e:
   if 'composition operation changed' not in str(e):raise
   counters.append(dict(label=label,pc=hex(pc),mutation={key:value},refused=str(e),class_='Synthetic source assertion control, not original execution'))
  else:raise ValueError('composition accepted changed source '+label)
 zero=json.loads((P/'queue-source-01.json').read_text());zero['ranges']=[]
 try:V.validate(zero)
 except ValueError as e:
  if 'missing/zero original ranges' not in str(e):raise
  counters.append(dict(label='zero-source-ranges',refused=str(e),class_='Actual shared annotation invocation on labelled invalid input'))
 else:raise ValueError('zero source accepted')
 with out.open('x') as f:json.dump(dict(complete=True,driver_sha256=sha(Path(__file__)),positive_reused=dict(receipt='proof-02.status.json',sha256=sha(P/'proof-02.status.json'),credit='Existing actual producer, not an additional run'),actual_cli_negatives=cases,source_countercontrols=counters,limits='Producer controls; mathematical countermodels and independent acceptance are separate. No game/native execution.'),f,indent=2)
 print('VALIDATED3 actual retained-input refusals/5 focused source controls; inequality covers full bounded domain')
if __name__=='__main__':main()
