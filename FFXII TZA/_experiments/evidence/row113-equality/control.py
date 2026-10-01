"""Focused actual arithmetic proof admission and original-code mutation controls."""
import hashlib,json,shutil,subprocess,sys
from pathlib import Path
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent;sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
st=json.loads((P/'proof-01.status.json').read_text());v=json.loads((P/'result-01.json').read_text())
if st.get('exit')!=0 or st.get('terminal') is not True or st.get('exception') is not None or st['driver_sha256']!=sha(P/'prove.py') or v['driver_sha256']!=sha(P/'prove.py') or v.get('producer_complete') is not True or len(v['boundary_witnesses'])!=24 or not(P/'proof-01.stdout').read_bytes() or(P/'proof-01.stderr').read_bytes():raise RuntimeError('valid positive missing/incomplete')
W=P/'proof-controls-01';W.mkdir(exist_ok=False);rows=[]
for label in ['failed-capture','missing-parent-proof-status','bad-high-half']:
 d=W/label;d.mkdir()
 for n in ['capture.py','capture-01.status.json','capture-01.stdout','capture-01.stderr','source-01.json']:shutil.copyfile(P/n,d/n)
 shutil.copytree(P/'retained',d/'retained')
 if label=='failed-capture':
  changed='capture-01.status.json';s=json.loads((d/changed).read_text());s['exit']=1;(d/changed).write_text(json.dumps(s,indent=2)+'\n');expected='RuntimeError: upstream capture failed/incomplete'
 elif label=='missing-parent-proof-status':
  changed='retained/presentation-index-domain-proof-01.status.json';(d/changed).unlink();expected='FileNotFoundError:'
 else:
  changed='source-01.json';s=json.loads((d/changed).read_text());b=s['ranges'][0];i=next(i for i in b['instructions'] if i['pc']=='0x30ce6c')
  if i['bytes']!='33d2' or i['mnemonic']!='xor' or i['args']!='edx, edx':raise RuntimeError('highhalf mutation preimage changed')
  i['bytes']='0bd2';i['mnemonic']='or';b['sha256']=hashlib.sha256(bytes.fromhex(''.join(i['bytes'] for i in b['instructions']))).hexdigest()
  (d/changed).write_text(json.dumps(s,indent=2)+'\n');expected='RuntimeError: original byte mismatch'
 out=d/'result.json';argv=[sys.executable,'-B',str(P/'prove.py'),str(out),'--src',str(d)]
 run=subprocess.run(argv,stdin=subprocess.DEVNULL,capture_output=True,timeout=20);(d/'stdout').write_bytes(run.stdout);(d/'stderr').write_bytes(run.stderr)
 diagnostic=run.stderr.decode(errors='replace').splitlines()[-1] if run.stderr else ''
 matched=diagnostic==expected if label!='missing-parent-proof-status' else diagnostic.startswith(expected) and 'presentation-index-domain-proof-01.status.json' in diagnostic
 row={'case':label,'argv':argv,'terminal':True,'exit':run.returncode,'exception':None,'diagnostic':diagnostic,'expected_error':expected,'expected_error_seen':matched,'stdout_empty':not run.stdout,'result_absent':not out.exists(),'changed_path':changed,'changed_sha256':sha(d/changed) if(d/changed).exists() else None,'baseline_source_sha256':sha(P/'source-01.json'),'baseline_retained_sha256':{p.name:sha(p) for p in(P/'retained').iterdir() if p.is_file()},'control_sha256':sha(Path(__file__)),'producer_sha256':sha(P/'prove.py')}
 row['passed']=run.returncode!=0 and matched and row['stdout_empty'] and row['result_absent'];(d/'receipt.json').write_text(json.dumps(row,indent=2)+'\n');rows.append(row)
complete=len(rows)==3 and all(r['passed'] for r in rows)
(W/'result.json').write_text(json.dumps({'complete':complete,'cases':rows,'limits':'Three actual proofCLI admission refusals, not original-code/game executions. Terminalproof01 required as positive.'},indent=2)+'\n')
print(json.dumps({'complete':complete,'cases':[{'case':r['case'],'passed':r['passed'],'diagnostic':r['diagnostic']} for r in rows]}));raise SystemExit(0 if complete else 1)
