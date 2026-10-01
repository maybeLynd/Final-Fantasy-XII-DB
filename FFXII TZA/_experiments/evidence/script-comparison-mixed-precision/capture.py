"""A source composition using retained original conversion evidence; no guest."""
import sys
sys.dont_write_bytecode=True
import hashlib,json,subprocess,types,inspect
from pathlib import Path
import capstone
W=Path(__file__).resolve().parent;R=W/'retained';sha=lambda b:hashlib.sha256(b).hexdigest()
assert callable(inspect.getfile) and Path(inspect.__file__).resolve().parent!=W
assert (W/'check.py').is_file();compile((W/'check.py').read_bytes(),str(W/'check.py'),'exec')
if (W/'raw.json').exists():subprocess.run([sys.executable,str(W/'check.py')],check=True);sys.exit(0)
sys.path.insert(0,'Database/Tools/analysis-kit/gfz-scripts');import team
ok,d=team.board_status(team.BOARD);assert ok,d
t=next(t for t in json.loads(team.BOARD.read_text())['tasks'] if t['id']=='ASTRA-SCRIPT-COMPARISON-MIXED-PRECISION');assert t['status']=='ACTIVE' and t['agent']=='ASTRA'
assert not R.exists();R.mkdir();files=[]
for name in ['shipping-reader.py','reg_tracking.py']:
 p=Path('Database/FFXII TZA/_experiments/evidence/script-store-saturation/retained')/name;b=p.read_bytes();c='8db582868ae4a72bae3f9e76c1d709844e9d9d93';assert b==subprocess.check_output(['git','show',c+':'+p.as_posix()]);(R/name).write_bytes(b);files.append(dict(path=p.as_posix(),commit=c,sha256=sha(b),copy=name))
reader=(R/'shipping-reader.py').read_bytes();assert sha(reader)=='4dfa511d2b92c41473e88dd535f900ac9bdc0c34f7c51ec54807652ac0f30e32'
rd=types.ModuleType('shipping_reader');rd.__file__=str((R/'shipping-reader.py').resolve());exec(compile(reader,'certified original reader','exec'),rd.__dict__)
image,ss=rd.load_image();assert sha(image)=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
code=rd.img_rd(image,ss,0x25d740,413);(R/'compare413.bin').write_bytes(code)
roles=types.ModuleType('roles');policy=(R/'reg_tracking.py').read_bytes();exec(compile(policy,'shared reviewed adapter','exec'),roles.__dict__)
cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True;ii=list(cs.disasm(code,0x25d740));assert sum(i.size for i in ii)==413
rows=[dict(pc=hex(i.address),hex=i.bytes.hex(),mnemonic=i.mnemonic,args=i.op_str,written=sorted(roles.written(i)),memory=[dict(kind=roles.op_kind(i,o,j),size=o.size) for j,o in enumerate(i.operands) if o.type==capstone.CS_OP_MEM]) for i in ii]
c='c4cbbfb8abe0bd5e73daf47d92c9378923292c29';prior=Path('Database/FFXII TZA/_experiments/evidence/script-popv-float-rounding')
for name in ['result.json','feasibility-raw.json','runner-adapted.py','manifest.json']:
 p=prior/name;b=p.read_bytes();assert b==subprocess.check_output(['git','show',c+':'+p.as_posix()]);out='prior72-'+name;(R/out).write_bytes(b);files.append(dict(path=p.as_posix(),commit=c,sha256=sha(b),copy=out))
raw=dict(method='A STATIC_ONLY original full comparator source plus retained72 B conversion values, conditional composition; no new original-code/guest/native/live execution',reference=dict(exe_sha256=sha(image),entry='0x25d740',imagebase='0x120000',bytes=413,code_sha256=sha(code),adapter_sha256=sha(policy),files=files),instructions=rows,import_control=dict(inspect_file=inspect.__file__,getfile_callable=True,own_shadow_absent=not (W/'inspect.py').exists()),tools=dict(python=sys.version,python_sha256=sha(Path(sys.executable).read_bytes()),capstone=capstone.__version__,providers=[dict(path=str(Path(p).resolve()),sha256=sha(Path(p).read_bytes())) for p in [capstone.__file__,capstone._cs._name]]),driver_sha256=sha(Path(__file__).read_bytes()),limits='Predicted valid depth2/tag1-or2 paths and finite values under supplied masked MXCSR. Not executed mixed comparator, actual game rounding/caller/authored values/native flags/unmasked/fault handlers/other tags/full interpreter/live. Retained72 initial labels source/invocation-derived additive correction, not new initial-state measurement. PC OFF; no saves/config/reference changes; S19 spent extension unapproved; full L1+L2 NOT_MET')
(W/'raw.json').write_text(json.dumps(raw,indent=2)+'\n');print('CAPTURE78 source and retained72 only',flush=True);subprocess.run([sys.executable,str(W/'check.py')],check=True)
