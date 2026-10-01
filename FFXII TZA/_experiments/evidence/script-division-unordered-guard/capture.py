"""A exact OPDIV predicate, source initialization and result paths; no execution."""
import sys
sys.dont_write_bytecode=True
import hashlib,json,subprocess,types,inspect,struct
from pathlib import Path
import capstone
W=Path(__file__).resolve().parent;R=W/'retained';sha=lambda b:hashlib.sha256(b).hexdigest()
assert callable(inspect.getfile) and Path(inspect.__file__).resolve().parent!=W
assert (W/'check.py').is_file();compile((W/'check.py').read_bytes(),str(W/'check.py'),'exec')
if (W/'raw.json').exists():subprocess.run([sys.executable,str(W/'check.py')],check=True);sys.exit(0)
sys.path.insert(0,'Database/Tools/analysis-kit/gfz-scripts');import team
ok,d=team.board_status(team.BOARD);assert ok,d;t=next(t for t in json.loads(team.BOARD.read_text())['tasks'] if t['id']=='ASTRA-SCRIPT-DIVISION-UNORDERED-GUARD');assert t['agent']=='ASTRA' and t['status']=='ACTIVE'
assert not R.exists();R.mkdir();files=[]
for n in ['shipping-reader.py','reg_tracking.py']:
 p=Path('Database/FFXII TZA/_experiments/evidence/script-store-saturation/retained')/n;b=p.read_bytes();c='8db582868ae4a72bae3f9e76c1d709844e9d9d93';assert b==subprocess.check_output(['git','show',c+':'+p.as_posix()]);(R/n).write_bytes(b);files.append(dict(path=p.as_posix(),commit=c,sha256=sha(b),copy=n))
reader=(R/'shipping-reader.py').read_bytes();assert sha(reader)=='4dfa511d2b92c41473e88dd535f900ac9bdc0c34f7c51ec54807652ac0f30e32';rd=types.ModuleType('shipping_reader');rd.__file__=str((R/'shipping-reader.py').resolve());exec(compile(reader,'certified original reader','exec'),rd.__dict__)
image,ss=rd.load_image();assert sha(image)=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
roles=types.ModuleType('roles');policy=(R/'reg_tracking.py').read_bytes();exec(compile(policy,'shared reviewed adapter','exec'),roles.__dict__);cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True
def rows(b,pc):
 ii=list(cs.disasm(b,pc));assert sum(i.size for i in ii)==len(b)
 return [dict(pc=hex(i.address),hex=i.bytes.hex(),mnemonic=i.mnemonic,args=i.op_str,written=sorted(roles.written(i)),memory=[dict(kind=roles.op_kind(i,o,j),size=o.size) for j,o in enumerate(i.operands) if o.type==capstone.CS_OP_MEM]) for i in ii]
blocks=[]
for name,pc,n in [('opdiv298.bin',0x25f0ac,298),('initial162.bin',0x25e4c0,162),('int-zero64.bin',0x25e682,64)]:
 b=rd.img_rd(image,ss,pc,n);(R/name).write_bytes(b);blocks.append(dict(path=name,pc=hex(pc),bytes=n,sha256=sha(b),instructions=rows(b,pc)))
table=rd.img_rd(image,ss,0x261df8+0x15*4,4);descriptor=rd.img_rd(image,ss,0x1efea60+0x14*24,24);namepc=struct.unpack_from('<Q',descriptor,8)[0];namebytes=rd.img_rd(image,ss,namepc,32)
for n,b in [('dispatch4.bin',table),('descriptor24.bin',descriptor),('name32.bin',namebytes)]:(R/n).write_bytes(b)
assert 0x120000+struct.unpack('<I',table)[0]==0x25f0ac and namebytes.split(b'\0')[0]==b'OPDIV'
p=Path('Database/FFXII TZA/_index/candidates/bf1-opcode-semantics/README.md');working=p.read_bytes();c=subprocess.check_output(['git','log','-1','--format=%H','--',p.as_posix()],text=True).strip();b=subprocess.check_output(['git','show',c+':'+p.as_posix()]);(R/'consumer-before.md').write_bytes(b)
(R/'preparation-before-boundary-fix.bin').write_bytes((W/'preparation-before-boundary-fix.bin').read_bytes());(R/'preparation-boundary-note.json').write_text(json.dumps(dict(stage='Preparation only, no raw/result',cause='Companion read began25E67B inside an instruction, produced meaningless sal decode',affected_conclusions=[],correction='Capture actual branch target25E682 with64 fully decoded bytes; do not treat arbitrary adjacent offset as validated entry',limits='OPDIV298 decoded validly; invalid companion never evidence/test PASS'),indent=2)+'\n')
raw=dict(method='A STATIC_ONLY original OPDIV identity/float guard/initialization/result source; flag-domain conditional calculations only, no guest/original-code/native/live execution',reference=dict(exe_sha256=sha(image),imagebase='0x120000',entry='0x25f0ac',opcode='0x15',name='OPDIV',name_address=hex(namepc),table_sha256=sha(table),descriptor_sha256=sha(descriptor),name_sha256=sha(namebytes),adapter_sha256=sha(policy),files=files),blocks=blocks,consumer=dict(path=p.as_posix(),commit=c,sha256=sha(b),working_sha256=sha(working),working_matches=working==b),tools=dict(python=sys.version,python_sha256=sha(Path(sys.executable).read_bytes()),capstone=capstone.__version__,providers=[dict(path=str(Path(p).resolve()),sha256=sha(Path(p).read_bytes())) for p in [capstone.__file__,capstone._cs._name]]),driver_sha256=sha(Path(__file__).read_bytes()),limits='Source predicate/local setup and conditional output paths only. No actual opcode/calls/stack transitions/arithmetic outcome/native flags/unmasked exceptions/gamecaller/live observation. Float path preconditions supplied/locally source-backed EBP1/XMM7+0; other callbacks/native effects not executed. Integer INT_MIN/-1 and game exception policy not settled. PC OFF/no saves/config/reference changes/S19 unapproved/fullL1+L2 NOT_MET')
(W/'raw.json').write_text(json.dumps(raw,indent=2)+'\n');print('CAPTURE79 source guard hypothesis only',flush=True);subprocess.run([sys.executable,str(W/'check.py')],check=True)
