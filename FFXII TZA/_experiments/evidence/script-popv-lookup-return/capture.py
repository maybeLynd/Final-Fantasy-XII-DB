import hashlib,json,subprocess,sys,types
from pathlib import Path
import capstone
sys.dont_write_bytecode=True
W=Path(__file__).resolve().parent;R=W/'retained';sha=lambda b:hashlib.sha256(b).hexdigest()
if (W/'raw.json').exists():subprocess.run([sys.executable,str(W/'check.py')],check=True);sys.exit(0)
sys.path.insert(0,'Database/Tools/analysis-kit/gfz-scripts');import team
ok,d=team.board_status(team.BOARD);assert ok,d;t=next(t for t in json.loads(team.BOARD.read_text())['tasks'] if t['id']=='ASTRA-SCRIPT-POPV-LOOKUP-RETURN');assert t['agent']=='ASTRA' and t['status']=='ACTIVE'
assert not R.exists();R.mkdir();P=Path('Database/FFXII TZA/_experiments/evidence/script-store-saturation/retained');files=[]
for n in ['shipping-reader.py','reg_tracking.py','original194.bin']:
 p=P/n;b=p.read_bytes();assert b==subprocess.check_output(['git','show','8db582868ae4a72bae3f9e76c1d709844e9d9d93:'+p.as_posix()]);(R/n).write_bytes(b);files.append(dict(path=p.as_posix(),sha256=sha(b),verified_at='8db582868ae4a72bae3f9e76c1d709844e9d9d93'))
rd=types.ModuleType('reader');rd.__file__=str((R/'shipping-reader.py').resolve());exec(compile((R/'shipping-reader.py').read_bytes(),'existing certified reader source','exec'),rd.__dict__);image,ss=rd.load_image();assert sha(image)=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
lookup=rd.img_rd(image,ss,0x32f240,32);caller=rd.img_rd(image,ss,0x267f1e,30);prefix=rd.img_rd(image,ss,0x26d530,23);assert prefix==(R/'original194.bin').read_bytes()[:23]
for n,b in [('lookup32.bin',lookup),('caller30.bin',caller),('store-prefix23.bin',prefix)]: (R/n).write_bytes(b)
policy=(R/'reg_tracking.py').read_bytes();roles=types.ModuleType('roles');exec(compile(policy,'shared reviewed adapter source','exec'),roles.__dict__);cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True
def decode(b,pc):return [dict(pc=hex(i.address),hex=i.bytes.hex(),mnemonic=i.mnemonic,args=i.op_str,reads=sorted(set(roles.canon(i.reg_name(r)) for r in i.regs_access()[0])),writes=sorted(roles.written(i)),memory=[dict(kind=roles.op_kind(i,o,j),size=o.size,base=i.reg_name(o.mem.base),index=i.reg_name(o.mem.index),scale=o.mem.scale,disp=o.mem.disp) for j,o in enumerate(i.operands) if o.type==capstone.CS_OP_MEM]) for i in cs.disasm(b,pc)]
consumer='Database/FFXII TZA/01-Script-VM-Native-Bridge/Interpreter-Core/script-variables-and-their-storage-classes.md';b=Path(consumer).read_bytes();(R/'consumer-before.md').write_bytes(b)
raw=dict(method='A exact original closed lookup/caller/store-prefix disassembly; no original/guest/native/live execution',reference=dict(exe_sha256=sha(image),imagebase=hex(rd.IMG_LO),selected67_files=files,lookup=dict(entry='0x32f240',bytes=32,sha256=sha(lookup)),caller=dict(entry='0x267f1e',bytes=30,sha256=sha(caller)),store_prefix=dict(entry='0x26d530',bytes=23,sha256=sha(prefix)),access_adapter_sha256=sha(policy)),tools=dict(python=sys.version,python_sha256=sha(Path(sys.executable).read_bytes()),capstone=capstone.__version__,providers=[dict(path=str(Path(p).resolve()),sha256=sha(Path(p).read_bytes())) for p in [capstone.__file__,capstone._cs._name]]),driver_sha256=sha(Path(__file__).read_bytes()),lookup=decode(lookup,0x32f240),caller=decode(caller,0x267f1e),store_prefix=decode(prefix,0x26d530),consumer=dict(path=consumer,sha256=sha(b)),limits='Original local source contract only, no actualtablevalues/nativefault/callerreachability/writer/othercallbacks/lifetime orliveproof.70 raw/result immutable; evidence may narrow its former omitted-helper gap. PC OFF/S19/fullL1+L2 NOT_MET')
(W/'raw.json').write_text(json.dumps(raw,indent=2)+'\n');print('CAPTURE71 static lookup/caller return use; reducer required',flush=True);subprocess.run([sys.executable,str(W/'check.py')],check=True)
