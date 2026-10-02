"""Actual upstream-failure refusals and focused original-source countermodels."""
import copy,hashlib,importlib.util,json,shutil,subprocess,sys
from pathlib import Path
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent;sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def mod(name,file):
 s=importlib.util.spec_from_file_location(name,P/file);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
M=mod('producer','prove.py');G=mod('cfg','prove_owner_reload_order.py')
positive=json.loads((P/'result-03.json').read_text());need=lambda ok,msg: M.need(ok,msg)
need(positive.get('producer_complete') is True and positive['driver_sha256']==sha(P/'prove.py'),'valid current positive required')
x=json.loads((P/'source-02.json').read_text());d=json.loads((P/'data-01.json').read_text());ix={int(i['pc'],16):i for i in x['ranges'][0]['instructions']}
need(M.derive(ix,d,G)==positive['facts'],'positive derive must match actual result')
F=P/'controls-01';need(not F.exists(),'immutable control folder exists');F.mkdir();cli=[]
for label in ['failed-extent-with-output-present','failed-capture-exit','missing-data-status','missing-table-data']:
 q=F/label;q.mkdir()
 for p in P.iterdir():
  if p.is_file():shutil.copyfile(p,q/p.name)
 if label=='failed-extent-with-output-present':
  s=json.loads((q/'extent-01.status.json').read_text());s['exit']=7;(q/'extent-01.status.json').write_text(json.dumps(s))
 elif label=='failed-capture-exit':
  s=json.loads((q/'capture-02.status.json').read_text());s['exit']=7;(q/'capture-02.status.json').write_text(json.dumps(s))
 elif label=='missing-data-status':(q/'data-01.status.json').unlink()
 else:(q/'data-01.json').unlink()
 out=q/'negative-result.json';r=subprocess.run([sys.executable,'-B',str(q/'prove.py'),str(out)],capture_output=True,timeout=15)
 s=dict(terminal=True,exit=r.returncode,exception=None,result_written=out.exists(),driver_sha256=sha(q/'prove.py'))
 (q/'stdout').write_bytes(r.stdout);(q/'stderr').write_bytes(r.stderr);(q/'status.json').write_text(json.dumps(s,indent=2))
 need(r.returncode!=0 and not out.exists() and bool(r.stderr),'upstream failure was suppressed '+label);cli.append(dict(case=label,status=s,limits='Real CLI on disposable inputs; no native FF12 execution'))
cases=[('wrong-table-kind4',None,None,None),('wrong-stride-width',0x3068b2,'args','ecx, byte ptr [rax + 8]'),('signed-division',0x3068b8,'mnemonic','idiv'),('wrong-queue-width',0x3068d4,'args','word ptr [rip + 0x1fbb89e], ax'),('wrong-low16-conversion',0x3068c7,'mnemonic','movsx'),('bypass-arithmetic-dominance',0x306854,'jmp','0x3068d4')];mut=[]
for name,pc,field,after in cases:
 y=copy.deepcopy(ix);z=copy.deepcopy(d)
 if pc is None:z['relative_dwords'][3]=z['relative_dwords'][0]
 elif field=='jmp':y[pc]['mnemonic']='jmp';y[pc]['args']=after
 else:y[pc][field]=after
 try:M.derive(y,z,G)
 except ValueError as e:mut.append(dict(case=name,pc=hex(pc) if pc else 'dispatch DWORD3',field=field,after=after,refusal=str(e),limits='Synthetic mutation of actual derive annotations/data, not an EXE patch or code execution'))
 else:raise ValueError('source mutation survived '+name)
need(len(cli)==4 and len(mut)==6,'zero/incomplete controls')
with(P/'control-result-01.json').open('x') as f:json.dump(dict(complete=True,driver_sha256=sha(Path(__file__)),producer_sha256=sha(P/'prove.py'),positive_result_sha256=sha(P/'result-03.json'),CLI_cases=cli,synthetic_source_cases=mut,limits='Producer controls only, independent acceptance pending. Previous invalid capture/proof retained without semantic credit.'),f,indent=2)
print('VALIDATED four actual upstream refusals and six focused source controls, including arithmetic-bypass regression')
