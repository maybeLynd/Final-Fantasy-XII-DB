"""Real prerequisite CLI controls plus bounded classifier countermodels."""
import copy,hashlib,importlib.util,json,shutil,subprocess,sys
from pathlib import Path
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent;sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def mod(name,file):
 s=importlib.util.spec_from_file_location(name,P/file);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
M=mod('producer','prove.py');G=mod('cfg','prove_owner_reload_order.py');need=M.need
positive=json.loads((P/'result-02.json').read_text());need(positive.get('producer_complete') is True and positive['driver_sha256']==sha(P/'prove.py'),'current valid positive required')
ix={}
for file in ['source-01.json','retained-prefix-01.json','retained/queue-source-02.json']:
 for r in json.loads((P/file).read_text())['ranges']:
  if file=='retained-prefix-01.json' and r['start']!='0x306bd0':continue
  for i in r['instructions']:ix[int(i['pc'],16)]=i
d=json.loads((P/'data-01.json').read_text());need(M.derive(ix,d,G)==positive['facts'],'actual positive derive differs')
F=P/'controls-01';need(not F.exists(),'immutable controls already exist');F.mkdir();cli=[]
for label in ['valid-disposable-CLI','failed-capture-status','missing-prefix-lineage','failed-data-with-output-present','missing-retained-queue']:
 q=F/label;q.mkdir()
 for p in P.iterdir():
  if p.is_file():shutil.copyfile(p,q/p.name)
 shutil.copytree(P/'retained',q/'retained')
 if label=='failed-capture-status':
  z=json.loads((q/'capture-02.status.json').read_text());z['exit']=7;(q/'capture-02.status.json').write_text(json.dumps(z))
 elif label=='missing-prefix-lineage':(q/'retained-lineage-01.json').unlink()
 elif label=='failed-data-with-output-present':
  z=json.loads((q/'data-01.status.json').read_text());z['exit']=7;(q/'data-01.status.json').write_text(json.dumps(z))
 elif label=='missing-retained-queue':(q/'retained/queue-source-02.json').unlink()
 out=q/'new-result.json';r=subprocess.run([sys.executable,'-B',str(q/'prove.py'),str(out)],capture_output=True,timeout=15)
 z=dict(terminal=True,exit=r.returncode,exception=None,result_written=out.exists(),driver_sha256=sha(q/'prove.py'));(q/'status.json').write_text(json.dumps(z,indent=2));(q/'stdout').write_bytes(r.stdout);(q/'stderr').write_bytes(r.stderr)
 if label=='valid-disposable-CLI':need(r.returncode==0 and not r.stderr and r.stdout and out.exists() and json.loads(out.read_text())['facts']==positive['facts'],'concrete portable positive failed')
 else:
  token={'failed-capture-status':b'required successful current invocation capture-02','missing-prefix-lineage':b'retained-lineage-01.json','failed-data-with-output-present':b'required successful current invocation data-01','missing-retained-queue':b'queue-source-02.json'}[label]
  need(r.returncode!=0 and not out.exists() and token in r.stderr,'negative failed at wrong prerequisite '+label)
 cli.append(dict(case=label,status=z,limits='Actual disposable producer CLI; no FF12 instruction execution'))
mut=[]
for label,pc,field,value in [('narrow-classifier-before-range',0x306c84,'args','ax, 0xff6c'),('signed-range-branch',0x306c8c,'mnemonic','jg'),('kind4-publishes7',0x306cb7,'args','ebx, 7'),('byte-divisor',0x306c7c,'args','ecx, byte ptr [rax + 8]'),('queue-sign-extends-word',0x3068c7,'mnemonic','movsx'),('bypass-classifier-arithmetic',0x306c6c,'jmp','0x306cdb')]:
 v=copy.deepcopy(ix)
 if field=='jmp':v[pc]['mnemonic']='jmp';v[pc]['args']=value
 else:v[pc][field]=value
 try:M.derive(v,copy.deepcopy(d),G)
 except ValueError as e:mut.append(dict(case=label,pc=hex(pc),field=field,after=value,refusal=str(e),limits='Synthetic mutation of actual source derive, not EXE patch/native execution'))
 else:raise ValueError('classifier source mutation survived '+label)
need(len(cli)==5 and len(mut)==6,'zero/incomplete control run')
with(P/'control-result-01.json').open('x') as f:json.dump(dict(complete=True,driver_sha256=sha(Path(__file__)),producer_sha256=sha(P/'prove.py'),positive_result_sha256=sha(P/'result-02.json'),CLI_cases=cli,synthetic_source_cases=mut,limits='Producer controls and portable execution only; conditional invariant not natural reachability or independent acceptance.'),f,indent=2)
print('VALIDATED one actual portable positive, four discriminating CLI failures and six source controls')
