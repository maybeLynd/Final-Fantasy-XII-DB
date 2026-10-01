"""Actual proof-path controls, cause-specific refusals and required positive."""
import hashlib,json,shutil,subprocess,sys
from pathlib import Path
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
st=json.loads((P/'proof-01.status.json').read_text());pos=json.loads((P/'result-01.json').read_text())
if st.get('exit')!=0 or st.get('terminal') is not True or st.get('exception') is not None or st['driver_sha256']!=sha(P/'prove.py') or pos['driver_sha256']!=sha(P/'prove.py') or not(P/'proof-01.stdout').read_bytes() or(P/'proof-01.stderr').read_bytes() or pos.get('producer_complete') is not True or len(pos['equal_branch']['cases'])!=256 or len(pos['graphs'])!=1:raise RuntimeError('positive prerequisite incomplete')
W=P/'proof-controls-02';W.mkdir(exist_ok=False);rows=[]
for label in ['failed-capture','missing-source','zero-bodies','coherent-type-subtraction-change']:
 d=W/label;d.mkdir()
 for name in ['capture.py','capture-01.status.json','capture-01.stdout','capture-01.stderr','source-01.json']:shutil.copyfile(P/name,d/name)
 shutil.copytree(P/'retained',d/'retained')
 changed='source-01.json'
 if label=='failed-capture':
  changed='capture-01.status.json';v=json.loads((d/changed).read_text());v['exit']=1;(d/changed).write_text(json.dumps(v,indent=2)+'\n');expected='RuntimeError: upstream capture failed/incomplete'
 elif label=='missing-source':(d/changed).unlink();expected='FileNotFoundError:'
 elif label=='zero-bodies':
  v=json.loads((d/changed).read_text());v['ranges']=[];(d/changed).write_text(json.dumps(v,indent=2)+'\n');expected='ValueError: missing/zero original ranges'
 else:
  # Update bytes, decode text and local body hash coherently; same size/count
  # and roles still validate, but this is not the certified shipping function.
  v=json.loads((d/changed).read_text());r=v['ranges'][0];i=next(i for i in r['instructions'] if i['pc']=='0x3092d6')
  if i['bytes']!='83e81b' or i['args']!='eax, 0x1b':raise RuntimeError('mutation preimage changed')
  i['bytes']='83e81a';i['args']='eax, 0x1a';r['sha256']=hashlib.sha256(bytes.fromhex(''.join(i['bytes'] for i in r['instructions']))).hexdigest()
  (d/changed).write_text(json.dumps(v,indent=2)+'\n');expected='RuntimeError: original byte mismatch'
 out=d/'result.json';argv=[sys.executable,'-B',str(P/'prove.py'),str(out),'--src',str(d)]
 run=subprocess.run(argv,stdin=subprocess.DEVNULL,capture_output=True,timeout=20)
 (d/'stdout').write_bytes(run.stdout);(d/'stderr').write_bytes(run.stderr)
 diagnostic=run.stderr.decode(errors='replace').splitlines()[-1] if run.stderr else ''
 matched=diagnostic==expected if label!='missing-source' else diagnostic.startswith(expected) and 'source-01.json' in diagnostic
 row={'case':label,'argv':argv,'exit':run.returncode,'terminal':True,'exception':None,'diagnostic':diagnostic,'expected_error':expected,'expected_error_seen':matched,'stdout_empty':not run.stdout,'result_absent':not out.exists(),'changed_file':changed,'changed_sha256':sha(d/changed) if(d/changed).exists() else None,'baseline_sha256':{n:sha(P/n) for n in ['capture.py','capture-01.status.json','capture-01.stdout','capture-01.stderr','source-01.json','retained/selector-callers-raw-01.json','retained/selector-callers.py']},'producer_sha256':sha(P/'prove.py'),'control_sha256':sha(Path(__file__))}
 row['passed']=run.returncode!=0 and matched and row['stdout_empty'] and row['result_absent'];(d/'receipt.json').write_text(json.dumps(row,indent=2)+'\n');rows.append(row)
complete=len(rows)==4 and all(r['passed'] for r in rows)
(W/'result.json').write_text(json.dumps({'complete':complete,'status':'FOUR_ACTUAL_PREREQUISITE_REFUSALS' if complete else'INVALID_CONTROL','cases':rows,'limits':'Host admission controls, not original-code/native/game executions; exact terminal proof01 is the positive.'},indent=2)+'\n')
print(json.dumps({'complete':complete,'cases':[{'case':r['case'],'passed':r['passed'],'diagnostic':r['diagnostic']} for r in rows]}));raise SystemExit(0 if complete else 1)
