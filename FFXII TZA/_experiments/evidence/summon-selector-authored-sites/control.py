"""Concrete composite completeness/status and literal-gap refusal controls."""
import hashlib,json,shutil,subprocess,sys
from pathlib import Path
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent;sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
s=json.loads((P/'reduce-01.status.json').read_text());v=json.loads((P/'result-01.json').read_text())
if s.get('terminal') is not True or s.get('exit')!=0 or s.get('exception') is not None or s['driver_sha256']!=sha(P/'reduce.py') or v['driver_sha256']!=sha(P/'reduce.py') or v.get('producer_complete') is not True or v['entry_count']!=10045 or not(P/'reduce-01.stdout').read_bytes() or(P/'reduce-01.stderr').read_bytes():raise RuntimeError('valid nonempty positive missing')
W=P/'controls-01';W.mkdir(exist_ok=False);cases=[]
names=['collect.py','resume.py','raw-01.json','raw-02.json','retained-native-source.json','native-source-lineage.json']+[t+x for t in ['collect-01','resume-01'] for x in ['.status.json','.stdout','.stderr']]
for case in ['unrelated-upstream-fail','empty-suffix','coherent-gap-literal']:
 d=W/case;d.mkdir()
 for n in names:shutil.copyfile(P/n,d/n)
 shutil.copytree(P/'raw',d/'raw');shutil.copytree(P/'raw-02',d/'raw-02')
 if case=='unrelated-upstream-fail':
  st=json.loads((d/'resume-01.status.json').read_text());st['exit']=1;(d/'resume-01.status.json').write_text(json.dumps(st,indent=2)+'\n');expected='RuntimeError: required collector status failed/stale resume-01'
 elif case=='empty-suffix':
  new=json.loads((d/'raw-02.json').read_text());new['coverage']=[];(d/'raw-02.json').write_text(json.dumps(new,indent=2)+'\n');expected='RuntimeError: missing/duplicate composite entry'
 else:
  old=json.loads((d/'raw-01.json').read_text());new=json.loads((d/'raw-02.json').read_text());r=next(r for r in new['coverage'] if r['previous_layout_status']);f=d/'raw-02'/r['retained_raw'];b=f.read_bytes()
  if len(b)<0x103:raise RuntimeError('gap control too short')
  f.write_bytes(b[:0x100]+bytes.fromhex('584430')+b[0x103:]);r['sha256']=sha(f)
  next(q for q in old['coverage'] if q['path']==r['path'])['sha256']=r['sha256'];(d/'raw-01.json').write_text(json.dumps(old,indent=2)+'\n');new['parent_raw_sha256']=sha(d/'raw-01.json');(d/'raw-02.json').write_text(json.dumps(new,indent=2)+'\n');expected='RuntimeError: gap whole-byte control changed'
 out=d/'result.json';argv=[sys.executable,'-B',str(P/'reduce.py'),str(out),'--src',str(d)];r=subprocess.run(argv,stdin=subprocess.DEVNULL,capture_output=True,timeout=15);(d/'stdout').write_bytes(r.stdout);(d/'stderr').write_bytes(r.stderr);last=r.stderr.decode(errors='replace').splitlines()[-1] if r.stderr else ''
 row={'case':case,'argv':argv,'exit':r.returncode,'terminal':True,'exception':None,'diagnostic':last,'expected':expected,'result_absent':not out.exists(),'stdout_empty':not r.stdout,'producer_sha256':sha(P/'reduce.py'),'control_sha256':sha(Path(__file__))};row['passed']=r.returncode!=0 and last==expected and row['result_absent'] and row['stdout_empty'];(d/'receipt.json').write_text(json.dumps(row,indent=2)+'\n');cases.append(row)
complete=len(cases)==3 and all(r['passed'] for r in cases);(W/'result.json').write_text(json.dumps({'complete':complete,'cases':cases,'limits':'Actual reducer CLI controls; no archive reread/native/game tests, prefix budget failure never declared successful.'},indent=2)+'\n');print(json.dumps({'complete':complete,'cases':[{k:r[k] for k in ['case','passed','diagnostic']} for r in cases]}));raise SystemExit(0 if complete else 1)
