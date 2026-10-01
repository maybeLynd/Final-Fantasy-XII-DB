"""A: original PUSHP source plus conditional packing calculations, no execution."""
import sys
sys.dont_write_bytecode=True
import hashlib,json,struct,subprocess,types,inspect
from pathlib import Path
import capstone
W=Path(__file__).resolve().parent;R=W/'retained';sha=lambda b:hashlib.sha256(b).hexdigest()
# Check the actual invocation/import path, not just a renamed helper's existence.
assert callable(inspect.getfile) and Path(inspect.__file__).resolve().parent!=W
if (W/'raw.json').exists():subprocess.run([sys.executable,str(W/'check.py')],check=True);sys.exit(0)
sys.path.insert(0,'Database/Tools/analysis-kit/gfz-scripts');import team
ok,d=team.board_status(team.BOARD);assert ok,d;t=next(t for t in json.loads(team.BOARD.read_text())['tasks'] if t['id']=='ASTRA-SCRIPT-REFERENCE-OFFSET-CARRY');assert t['agent']=='ASTRA' and t['status']=='ACTIVE'
assert not R.exists();R.mkdir();files=[]
for n in ['shipping-reader.py','reg_tracking.py']:
 p=Path('Database/FFXII TZA/_experiments/evidence/script-store-saturation/retained')/n;b=p.read_bytes();assert b==subprocess.check_output(['git','show','8db582868ae4a72bae3f9e76c1d709844e9d9d93:'+p.as_posix()]);(R/n).write_bytes(b);files.append(dict(path=p.as_posix(),bytes=len(b),sha256=sha(b),verified_at='8db582868ae4a72bae3f9e76c1d709844e9d9d93'))
reader=(R/'shipping-reader.py').read_bytes();assert sha(reader)=='4dfa511d2b92c41473e88dd535f900ac9bdc0c34f7c51ec54807652ac0f30e32'
rd=types.ModuleType('shipping_reader');rd.__file__=str((R/'shipping-reader.py').resolve());exec(compile(reader,'retained certified reader','exec'),rd.__dict__)
image,ss=rd.load_image();assert sha(image)=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
code=rd.img_rd(image,ss,0x268100,164);table=rd.img_rd(image,ss,0x2681a4,24);(R/'pushp164.bin').write_bytes(code);(R/'scale-table24.bin').write_bytes(table)
policy=(R/'reg_tracking.py').read_bytes();roles=types.ModuleType('roles');exec(compile(policy,'shared reviewed adapter source','exec'),roles.__dict__)
cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True
ii=list(cs.disasm(code,0x268100));assert sum(i.size for i in ii)==164 and ii[-1].address==0x2681a3 and ii[-1].mnemonic=='ret'
rows=[dict(pc=hex(i.address),hex=i.bytes.hex(),mnemonic=i.mnemonic,args=i.op_str,written=sorted(roles.written(i)),memory=[dict(kind=roles.op_kind(i,o,j),base=i.reg_name(o.mem.base),index=i.reg_name(o.mem.index),scale=o.mem.scale,disp=o.mem.disp,size=o.size) for j,o in enumerate(i.operands) if o.type==capstone.CS_OP_MEM]) for i in ii]
p=Path('Database/FFXII TZA/01-Script-VM-Native-Bridge/Interpreter-Core/script-variables-and-their-storage-classes.md');primary=p.read_bytes();commit=subprocess.check_output(['git','log','-1','--format=%H','--',p.as_posix()],text=True).strip();assert primary==subprocess.check_output(['git','show',commit+':'+p.as_posix()]);(R/'consumer-before.md').write_bytes(primary)
(R/'failed-inspect-source.bin').write_bytes((W/'failed-inspect-source.bin').read_bytes())
failure=dict(stage='Preparation import before image/code read/raw/result',cause='Own inspect.py shadowed Python standard-library inspect; Capstone imported it and Unicorn requested missing inspect.getfile',affected_conclusions=[],correction='Retain inert original source, rename prepare-source.py; capture/default assert actual inspect module origin/getfile before reader',limits='No original/guest/native/live execution occurred in failed preparation')
(R/'preparation-failure.json').write_text(json.dumps(failure,indent=2)+'\n')
raw=dict(method='A STATIC_ONLY full shipping PUSHP source/scaling/packing/epilogue and conditional32bit arithmetic; no original-code/guest/native/live execution',reference=dict(exe_sha256=sha(image),imagebase='0x120000',entry='0x268100',bytes=164,source_sha256=sha(code),table_sha256=sha(table),files=files,adapter_sha256=sha(policy)),instructions=rows,table_targets=[hex(0x120000+n) for n in struct.unpack('<6I',table)],consumer=dict(path=p.as_posix(),commit=commit,sha256=sha(primary)),import_control=dict(inspect_file=inspect.__file__,getfile_callable=True,own_shadow_module_absent=not (W/'inspect.py').exists()),driver_sha256=sha(Path(__file__).read_bytes()),tools=dict(python=sys.version,python_sha256=sha(Path(sys.executable).read_bytes()),capstone=capstone.__version__,providers=[dict(path=str(Path(p).resolve()),sha256=sha(Path(p).read_bytes())) for p in [capstone.__file__,capstone._cs._name]]),limits='Conditional injected descriptor/index values, not actual shipped references/validity/normal caller/frame/bank/init/lifetime/native fault/live or all malformed safety. Original resolver call not executed/stubbed. PC OFF/S19/fullL1+L2 NOT_MET')
(W/'raw.json').write_text(json.dumps(raw,indent=2)+'\n');print('CAPTURE76 original reference packing source',flush=True);subprocess.run([sys.executable,str(W/'check.py')],check=True)
