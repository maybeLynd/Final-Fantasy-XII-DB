"""Actual prerequisite/identity refusals and an original read detection control."""
import hashlib, importlib.util, json, pathlib, shutil, subprocess, sys
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
W=pathlib.Path(__file__).resolve().parent;sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
out=W/'namebinding-callback-inputs-controls-01'
if out.exists():raise ValueError('immutable controls exist')
d=W/'prove-namebinding-callback-inputs.py';p=json.loads((W/'namebinding-callback-inputs-result-01.json').read_text());st=json.loads((W/'namebinding-callback-inputs-positive-01.status.json').read_text())
if st['exit']!=0 or st['checker_sha256']!=sha(d) or p['checker_sha256']!=sha(d) or p['producer_complete'] is not True:raise ValueError('positive missing/stale')
if any(sha(W/x['path'])!=x['sha256'] for x in p['source_pins']+p['required_invocation_receipts']):raise ValueError('positive prerequisite changed')
spec=importlib.util.spec_from_file_location('callback_control_producer',d);M=importlib.util.module_from_spec(spec);spec.loader.exec_module(M)
v=json.loads((W/'namebinding-callback-inputs-source-01.json').read_text());ix={int(i['pc'],16):i for q in v['ranges'] for i in q['instructions']}
md=Cs(CS_ARCH_X86,CS_MODE_64);md.detail=True
# An actual original CMP reads R8D; an earlier MOV fully replaces it. Test the
# same producer's alias sets/API against those original instructions. This is
# a detection control, not entry at this interior address or native execution.
detect=[]
for pc,read,kill in [(0x4090a6,True,False),(0x4090a3,False,True)]:
 i=ix[pc];dec=next(md.disasm(bytes.fromhex(i['bytes']),pc));rr,ww=dec.regs_access();reads={dec.reg_name(q) for q in rr};writes={dec.reg_name(q) for q in ww}
 observed_read=bool(reads&M.FAMILIES[1]);observed_kill=bool(writes&M.FULL_WRITES[1])
 if (observed_read,observed_kill)!=(read,kill):raise ValueError('original register read/kill detection control failed')
 detect.append(dict(pc=hex(pc),bytes=i['bytes'],R8_input_read=observed_read,R8_full_kill=observed_kill))
out.mkdir();records=[]
core=['capture-namebinding-callback-inputs.py','namebinding-callback-inputs-capture-01.status.json','namebinding-callback-inputs-capture-01.stdout','namebinding-callback-inputs-capture-01.stderr','namebinding-callback-inputs-source-01.json']
for label,names,error in [('failed-capture',core[:4],'capture failed/stale'),('changed-early-call',core+['namebinding-callback-inputs-retained-provenance-01.json','namebinding-callback-inputs-retained-source-01.json'],'reference byte identity changed'),('missing-retained-callback',core+['namebinding-callback-inputs-retained-provenance-01.json'],'FileNotFoundError')]:
 c=out/label;c.mkdir()
 for n in names:shutil.copyfile(W/n,c/n)
 if label=='failed-capture':
  f=c/'namebinding-callback-inputs-capture-01.status.json';q=json.loads(f.read_text());q['exit']=1;f.write_text(json.dumps(q,indent=2)+'\n')
 elif label=='changed-early-call':
  f=c/'namebinding-callback-inputs-source-01.json';q=json.loads(f.read_text());rg=next(r for r in q['ranges'] if r['start']=='0x32f3d0');i=next(i for i in rg['instructions'] if i['pc']=='0x32f40b')
  if i['args']!='0x5c5230':raise ValueError('call mutation preimage changed')
  raw=bytearray.fromhex(i['bytes']);raw[1:]=(0x5c5240-(0x32f40b+5)).to_bytes(4,'little',signed=True);i.update(bytes=raw.hex(),args='0x5c5240')
  rg['sha256']=hashlib.sha256(bytes.fromhex(''.join(x['bytes'] for x in rg['instructions']))).hexdigest();f.write_text(json.dumps(q,indent=2)+'\n')
 target=c/'unexpected-result.json';argv=[sys.executable,str(d),str(target),str(c)];r=subprocess.run(argv,capture_output=True)
 (c/'stdout').write_bytes(r.stdout);(c/'stderr').write_bytes(r.stderr)
 rec=dict(case=label,argv=argv,exit=r.returncode,expected_error=error,expected_error_seen=error in r.stderr.decode(errors='replace'),result_absent=not target.exists())
 (c/'status.json').write_text(json.dumps(rec,indent=2)+'\n')
 if not(r.returncode and rec['expected_error_seen'] and rec['result_absent']):raise ValueError('actual refusal failed '+label)
 records.append(rec)
(out/'result.json').write_text(json.dumps(dict(status='PASS_ACTUAL_CALLBACK_INPUT_CONTROLS_INDEPENDENT_PENDING',driver_sha256=sha(pathlib.Path(__file__)),checker_sha256=sha(d),positive_reused=dict(path='namebinding-callback-inputs-result-01.json',sha256=sha(W/'namebinding-callback-inputs-result-01.json')),original_detection_controls=detect,refusals=records,limits='Detection checks original register read/full kill through the producer alias policy; not extra native execution, natural state or proof the entire dataflow analyzer has no defects. Three actual CLI refusals; sufficient positive reused.'),indent=2)+'\n')
print('Original read/kill detection control and three actual producer refusals complete')
