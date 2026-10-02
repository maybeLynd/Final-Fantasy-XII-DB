"""Actual prerequisite failures plus targeted supplied-source countercontrols."""
import copy,hashlib,importlib.util,json,shutil,subprocess,sys
from pathlib import Path
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent;sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def module(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def main():
 out=P/'control-result-01.json';C=P/'controls-01'
 if out.exists() or C.exists():raise ValueError('fresh controls required')
 result=json.loads((P/'result-01.json').read_text());status=json.loads((P/'proof-01.status.json').read_text())
 if result.get('producer_complete') is not True or result['driver_sha256']!=sha(P/'prove.py') or status.get('exit')!=0 or status.get('terminal') is not True or status.get('exception') is not None or not(P/'proof-01.stdout').read_bytes() or(P/'proof-01.stderr').read_bytes():raise ValueError('existing actual positive missing')
 base=[p for p in P.iterdir() if p.is_file()];C.mkdir();cases=[]
 for name,driver,marker in [('extent-failure','capture-helpers.py','required successful current extent invocation'),('capture-failure','prove.py','required successful current invocation helpers-capture-01'),('missing-caller','prove.py','current-row-source-02.json'),('zero-ranges','prove.py','missing/zero original ranges')]:
  q=C/name;q.mkdir()
  for f in base:shutil.copyfile(f,q/f.name)
  if name=='extent-failure':
   f=q/'helper-extents-01.status.json';x=json.loads(f.read_text());x['exit']=3;f.write_text(json.dumps(x))
  elif name=='capture-failure':
   f=q/'helpers-capture-01.status.json';x=json.loads(f.read_text());x['exception']='labelled synthetic upstream exception';f.write_text(json.dumps(x))
  elif name=='missing-caller':(q/'current-row-source-02.json').unlink()
  else:
   f=q/'helper-source-01.json';x=json.loads(f.read_text());x['ranges']=[];f.write_text(json.dumps(x))
  dest=q/'rejected-result.json';argv=[sys.executable,'-B',str(q/driver),str(dest)]
  r=subprocess.run(argv,stdin=subprocess.DEVNULL,capture_output=True,timeout=45)
  (q/'actual.stdout').write_bytes(r.stdout);(q/'actual.stderr').write_bytes(r.stderr)
  accepted=r.returncode!=0 and not dest.exists() and marker in r.stderr.decode(errors='replace')
  inputs=[dict(path=f.name,bytes=f.stat().st_size,sha256=sha(f)) for f in q.iterdir() if f.is_file() and f.name not in ['actual.stdout','actual.stderr']]
  receipt=dict(case=name,argv=argv,driver_sha256=sha(q/driver),terminal=True,exit=r.returncode,exception=None,expected=marker,refused_without_result=accepted,inputs=inputs)
  (q/'actual.status.json').write_text(json.dumps(receipt,indent=2))
  if not accepted:raise ValueError('concrete invocation control failed '+name)
  # Keep exact changed inputs plus identities of unchanged base members.
  for f in list(q.iterdir()):
   if f.is_file() and f.name not in ['actual.stdout','actual.stderr','actual.status.json'] and(P/f.name).is_file() and f.read_bytes()==(P/f.name).read_bytes():f.unlink()
  cases.append(receipt)
 M=module('producer',P/'prove.py');G=module('cfg',P/'prove_owner_reload_order.py');ix={}
 for name in ['current-row-source-01.json','current-row-source-02.json','helper-source-01.json']:
  for q in json.loads((P/name).read_text())['ranges']:
   ix.update({int(i['pc'],16):i for i in q['instructions']})
 raw=json.loads((P/'carrier-result-01.json').read_text());import struct
 d=bytes.fromhex(next(q for q in raw['original_data'] if q['address']=='0x305044')['bytes']);targets=[0x120000+k for k in struct.unpack('<13I',d)];table=(P/'action_data_us.st2e').read_bytes()
 source=[]
 for label,pc,key,value in [('64bit-row-add',0x304934,'args','r15, rcx'),('builder-uses-latched-ID',0x304edc,'args','edx, r13w'),('signed-helper-upper-bound',0x305456,'mnemonic','jg')]:
  x=copy.deepcopy(ix);x[pc][key]=value
  try:M.derive(x,targets,table,G)
  except ValueError as e:
   if 'original operation changed' not in str(e):raise
   source.append(dict(label=label,pc=hex(pc),change={key:value},refused=str(e),class_='Synthetic source assertion control, not original-code execution'))
  else:raise ValueError('changed source accepted '+label)
 altered=bytearray(table);_,stride,offset=struct.unpack_from('<III',table,4);altered[offset+511*stride+0x2c]|=0x40
 try:M.derive(ix,targets,altered,G)
 except ValueError as e:
  if 'stock row takes target side-effect branch' not in str(e):raise
  source.append(dict(label='row511-bit6-set',refused=str(e),class_='Supplied resource countercontrol, not live data'))
 else:raise ValueError('changed resource accepted')
 with out.open('x') as f:json.dump(dict(complete=True,driver_sha256=sha(Path(__file__)),actual_positive=dict(receipt='proof-01.status.json',sha256=sha(P/'proof-01.status.json'),credit='existing producer invocation, not rerun'),actual_cli_negatives=cases,source_countercontrols=source,limits='Producer controls only; no native/emulated/game observations or independent acceptance.'),f,indent=2)
 print('VALIDATED four actual upstream/zero-case refusals and four claim countercontrols; original positive reused')
if __name__=='__main__':main()
