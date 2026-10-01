"""A original filter local continuation; callbacks are not executed."""
import sys
sys.dont_write_bytecode=True
import hashlib,json,struct,subprocess,types
from pathlib import Path
import capstone
W=Path(__file__).resolve().parent;R=W/'retained';sha=lambda b:hashlib.sha256(b).hexdigest()
assert (W/'check.py').is_file();compile((W/'check.py').read_bytes(),str(W/'check.py'),'exec')
if (W/'raw.json').exists():subprocess.run([sys.executable,str(W/'check.py')],check=True);sys.exit(0)
sys.path.insert(0,'Database/Tools/analysis-kit/gfz-scripts');import team
ok,d=team.board_status(team.BOARD);assert ok,d
t=next(t for t in json.loads(team.BOARD.read_text())['tasks'] if t['id']=='ASTRA-NATIVE-EXCEPTION-FILTER-TAIL');assert t['agent']=='ASTRA' and t['status']=='ACTIVE'
assert not R.exists();R.mkdir();files=[]
for n in ['shipping-reader.py','reg_tracking.py']:
 p=Path('Database/FFXII TZA/_experiments/evidence/script-store-saturation/retained')/n;b=p.read_bytes();c='8db582868ae4a72bae3f9e76c1d709844e9d9d93';assert b==subprocess.check_output(['git','show',c+':'+p.as_posix()]);(R/n).write_bytes(b);files.append(dict(path=p.as_posix(),commit=c,copy=n,sha256=sha(b)))
rd=types.ModuleType('reader');rd.__file__=str((R/'shipping-reader.py').resolve());exec(compile((R/'shipping-reader.py').read_bytes(),rd.__file__,'exec'),rd.__dict__)
image,ss=rd.load_image();assert sha(image)=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
read=lambda pc,n:rd.img_rd(image,ss,pc,n)
code=read(0x79ad50,240);(R/'filter240.bin').write_bytes(code)
roles=types.ModuleType('roles');exec(compile((R/'reg_tracking.py').read_bytes(),'actual reviewed access policy','exec'),roles.__dict__)
cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True
ii=list(cs.disasm(code,0x79ad50));assert sum(i.size for i in ii)==240 and ii[-1].address==0x79ae3f and ii[-1].mnemonic=='ret'
rows=[dict(pc=hex(i.address),hex=i.bytes.hex(),mnemonic=i.mnemonic,args=i.op_str,written=sorted(roles.written(i)),memory=[roles.op_kind(i,o,j) for j,o in enumerate(i.operands) if o.type==capstone.CS_OP_MEM]) for i in ii]
slots={i.address+i.size+i.operands[0].mem.disp for i in ii if i.mnemonic=='call' and i.operands[0].type==capstone.CS_OP_MEM}
# Only slots referenced by this exact filter, with ordinal imports retained as such.
pe=struct.unpack_from('<I',image,0x3c)[0];opt=pe+24;base=0x120000
assert image[pe:pe+4]==b'PE\0\0' and struct.unpack_from('<H',image,opt)[0]==0x20b and struct.unpack_from('<Q',image,opt+24)[0]==base
imp,size=struct.unpack_from('<II',image,opt+120)
def string(pc):
 b=bytearray()
 for _ in range(256):
  x=read(pc+len(b),1)
  if x==b'\0':return b.decode('ascii'),bytes(b)+b'\0'
  b+=x
 raise AssertionError('Unterminated import string')
imports=[]
for rva in range(imp,imp+size,20):
 desc=read(base+rva,20);ilt,stamp,forwarder,name,iat=struct.unpack('<5I',desc)
 if not any((ilt,stamp,forwarder,name,iat)):break
 for j in range(4096):
  raw=read(base+(ilt or iat)+8*j,8);value=int.from_bytes(raw,'little')
  if not value:break
  slot=base+iat+8*j
  if slot in slots:
   dll,dllraw=string(base+name);symbol=None;symbolraw=None
   if not value>>63:symbol,symbolraw=string(base+value+2)
   imports.append(dict(slot=hex(slot),dll=dll,ordinal=(value&0xffff) if value>>63 else None,symbol=symbol,descriptor_pc=hex(base+rva),descriptor_hex=desc.hex(),lookup_pc=hex(base+(ilt or iat)+8*j),lookup_hex=raw.hex(),dll_pc=hex(base+name),dll_hex=dllraw.hex(),symbol_hex=symbolraw.hex() if symbolraw else None))
 else:raise AssertionError('Unterminated import lookup')
else:raise AssertionError('Unterminated import directory')
assert {int(x['slot'],16) for x in imports}==slots
caption=bytearray()
for n in range(128):
 x=read(0x8f3dc0+2*n,2);caption+=x
 if x==b'\0\0':break
else:raise AssertionError('Caption not terminated')
(R/'caption.bin').write_bytes(caption)
consumer=Path('Database/FFXII TZA/24-Compiler-And-CRT-Runtime/Runtime-Service-Surface/what-the-game-asks-windows-for.md')
c=subprocess.check_output(['git','log','-1','--format=%H','--',consumer.as_posix()],text=True).strip();body=subprocess.check_output(['git','show',c+':'+consumer.as_posix()]);(R/'consumer-primary.md').write_bytes(body)
raw=dict(method='A verified shipping filter240B, original import descriptors/lookups and conditional local paths; callbacks not executed',reference=dict(exe_sha256=sha(image),entry='0x79ad50',ret='0x79ae3f',code_sha256=sha(code),files=files,consumer_path=consumer.as_posix(),consumer_commit=c,consumer_sha256=sha(body),current_consumer_sha256=sha(consumer.read_bytes())),tools=dict(python=sys.version,python_sha256=sha(Path(sys.executable).read_bytes()),capstone=capstone.__version__),instructions=rows,imports=imports,caption=dict(pc='0x8f3dc0',hex=caption.hex(),utf16=caption[:-2].decode('utf-16le')),
 local_paths=[dict(condition='gate zero',branches={'0x79ad77':True}),dict(condition='gate nonzero/text null',branches={'0x79ad77':False,'0x79adf7':True}),dict(condition='gate nonzero/text nonnull',branches={'0x79ad77':False,'0x79adf7':False})],
 driver_sha256=sha(Path(__file__).read_bytes()),limits='Local CFG assumes calls return normally; no original-code/native/live execution, callbacks/OS effects not established. OLEAUT32 ordinal4/6 identity only, names/effects unproved. Requested text7837 is not captured visible text. Startup source not observed filter installation/reachability. Return1 not proof actual process exits. EXP127 fatal error cause remains unknown. PC OFF/S19 parked/fullL1+L2 NOT_MET')
(W/'raw.json').write_text(json.dumps(raw,indent=2)+'\n');print('CAPTURE81 original static filter tail',flush=True);subprocess.run([sys.executable,str(W/'check.py')],check=True)
