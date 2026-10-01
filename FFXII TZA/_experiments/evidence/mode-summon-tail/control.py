"""Actual prefix-proof controls for stack prerequisite and receiver store width."""
import hashlib,json,shutil,subprocess,sys
from pathlib import Path
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent;sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
st=json.loads((P/'proof-01.status.json').read_text());v=json.loads((P/'result-01.json').read_text())
if st.get('exit')!=0 or st.get('terminal') is not True or st.get('exception') is not None or st['driver_sha256']!=sha(P/'prove.py') or v['driver_sha256']!=sha(P/'prove.py') or v.get('producer_complete') is not True or len(v['graphs'])!=2 or len(v['immediate_receiver_stores'])!=4 or not(P/'proof-01.stdout').read_bytes() or(P/'proof-01.stderr').read_bytes():raise RuntimeError('valid positive missing/incomplete')
W=P/'proof-controls-01';W.mkdir(exist_ok=False);rows=[]
names=['capture.py','capture-stack-probe.py','source-01.json','stack-probe-source-01.json']+[t+s for t in ['capture-01','stack-capture-01'] for s in ['.status.json','.stdout','.stderr']]
for label in ['failed-stack-capture','missing-stack-source','coherent-store-width']:
 d=W/label;d.mkdir()
 for n in names:shutil.copyfile(P/n,d/n)
 if label=='failed-stack-capture':
  changed='stack-capture-01.status.json';s=json.loads((d/changed).read_text());s['exit']=1;(d/changed).write_text(json.dumps(s,indent=2)+'\n');expected='RuntimeError: upstream capture failed/incomplete stack-capture-01'
 elif label=='missing-stack-source':changed='stack-probe-source-01.json';(d/changed).unlink();expected='FileNotFoundError:'
 else:
  changed='source-01.json';s=json.loads((d/changed).read_text());r=s['ranges'][2];i=next(i for i in r['instructions'] if i['pc']=='0x273e9e')
  if i['bytes']!='488901' or i['args']!='qword ptr [rcx], rax':raise RuntimeError('store-width preimage changed')
  i['bytes']='408901';i['args']='dword ptr [rcx], eax';i['memory'][0]['size']=4;r['sha256']=hashlib.sha256(bytes.fromhex(''.join(i['bytes'] for i in r['instructions']))).hexdigest()
  (d/changed).write_text(json.dumps(s,indent=2)+'\n');expected='RuntimeError: original byte mismatch'
 out=d/'result.json';argv=[sys.executable,'-B',str(P/'prove.py'),str(out),'--src',str(d)];run=subprocess.run(argv,stdin=subprocess.DEVNULL,capture_output=True,timeout=20)
 (d/'stdout').write_bytes(run.stdout);(d/'stderr').write_bytes(run.stderr);diag=run.stderr.decode(errors='replace').splitlines()[-1] if run.stderr else ''
 matched=diag==expected if label!='missing-stack-source' else diag.startswith(expected) and 'stack-probe-source-01.json' in diag
 row={'case':label,'argv':argv,'exit':run.returncode,'terminal':True,'exception':None,'diagnostic':diag,'expected_error':expected,'expected_error_seen':matched,'stdout_empty':not run.stdout,'result_absent':not out.exists(),'changed_path':changed,'changed_sha256':sha(d/changed) if(d/changed).exists() else None,'baseline_sha256':{n:sha(P/n) for n in names},'producer_sha256':sha(P/'prove.py'),'control_sha256':sha(Path(__file__))}
 row['passed']=run.returncode!=0 and matched and row['stdout_empty'] and row['result_absent'];(d/'receipt.json').write_text(json.dumps(row,indent=2)+'\n');rows.append(row)
complete=len(rows)==3 and all(r['passed'] for r in rows)
(W/'result.json').write_text(json.dumps({'complete':complete,'cases':rows,'limits':'Actual host admission controls, no native/game executions; original terminalproof01 is positive.'},indent=2)+'\n')
print(json.dumps({'complete':complete,'cases':[{'case':r['case'],'passed':r['passed'],'diagnostic':r['diagnostic']} for r in rows]}));raise SystemExit(0 if complete else 1)
