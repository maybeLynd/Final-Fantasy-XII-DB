"""A original resource lookup and selected embedded RT_STRING, no native execution."""
import sys
sys.dont_write_bytecode=True
import hashlib,json,struct,subprocess,types
from pathlib import Path
import capstone
W=Path(__file__).resolve().parent;R=W/'retained';sha=lambda b:hashlib.sha256(b).hexdigest()
assert (W/'check.py').is_file();compile((W/'check.py').read_bytes(),str(W/'check.py'),'exec')
if (W/'raw.json').exists():subprocess.run([sys.executable,str(W/'check.py')],check=True);sys.exit(0)
sys.path.insert(0,'Database/Tools/analysis-kit/gfz-scripts');import team
ok,d=team.board_status(team.BOARD);assert ok,d;t=next(t for t in json.loads(team.BOARD.read_text())['tasks'] if t['id']=='ASTRA-NATIVE-FILTER-MESSAGE-RESOURCE');assert t['agent']=='ASTRA' and t['status']=='ACTIVE'
assert not R.exists();R.mkdir();files=[]
for n in ['shipping-reader.py','reg_tracking.py']:
 p=Path('Database/FFXII TZA/_experiments/evidence/script-store-saturation/retained')/n;b=p.read_bytes();c='8db582868ae4a72bae3f9e76c1d709844e9d9d93';assert b==subprocess.check_output(['git','show',c+':'+p.as_posix()]);(R/n).write_bytes(b);files.append(dict(path=p.as_posix(),commit=c,copy=n,sha256=sha(b)))
rd=types.ModuleType('reader');rd.__file__=str((R/'shipping-reader.py').resolve());exec(compile((R/'shipping-reader.py').read_bytes(),rd.__file__,'exec'),rd.__dict__);image,ss=rd.load_image();assert sha(image)=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
read=lambda pc,n:rd.img_rd(image,ss,pc,n)
roles=types.ModuleType('roles');exec(compile((R/'reg_tracking.py').read_bytes(),'actual reviewed access policy','exec'),roles.__dict__);cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True
functions=[];slots=set()
for name,entry,n in [('lookup',0x19a510,148),('selector',0x19a5b0,159),('module-getter',0x80c51c,124)]:
 code=read(entry,n);(R/(name+'.bin')).write_bytes(code);todo=[entry];seen={};term=[]
 while todo:
  pc=todo.pop()
  if pc in seen:continue
  assert entry<=pc<entry+n;i=next(cs.disasm(code[pc-entry:pc-entry+15],pc));assert pc+i.size<=entry+n;seen[pc]=i
  if i.mnemonic in ('ret','int3','ud2'):term.append(dict(pc=hex(pc),kind=i.mnemonic));continue
  if i.mnemonic.startswith('j'):
   assert i.operands[0].type==capstone.CS_OP_IMM;todo.append(i.operands[0].imm)
   if i.mnemonic=='jmp':continue
  todo.append(pc+i.size)
 rows=[]
 for i in sorted(seen.values(),key=lambda i:i.address):
  if i.mnemonic=='call' and i.operands[0].type==capstone.CS_OP_MEM:slots.add(i.address+i.size+i.operands[0].mem.disp)
  rows.append(dict(pc=hex(i.address),hex=i.bytes.hex(),mnemonic=i.mnemonic,args=i.op_str,written=sorted(roles.written(i)),memory=[roles.op_kind(i,o,j) for j,o in enumerate(i.operands) if o.type==capstone.CS_OP_MEM]))
 assert max(pc+i.size for pc,i in seen.items())==entry+n
 functions.append(dict(name=name,entry=hex(entry),bytes=n,sha256=sha(code),instructions=rows,terminals=term,limits='Local source reachability assumes call returns; INT3 is a trap boundary, not adjacent-function fallthrough'))
base=0x120000;pe=struct.unpack_from('<I',image,0x3c)[0];opt=pe+24;imp,impsz=struct.unpack_from('<II',image,opt+120);root,sz=struct.unpack_from('<II',image,opt+128)
assert image[pe:pe+4]==b'PE\0\0' and struct.unpack_from('<H',image,opt)[0]==0x20b and struct.unpack_from('<Q',image,opt+24)[0]==base
def string(pc):
 b=bytearray()
 for n in range(256):
  x=read(pc+len(b),1)
  if x==b'\0':return b.decode('ascii'),(bytes(b)+b'\0').hex()
  b+=x
 raise AssertionError('Unterminated import string')
imports=[]
for rva in range(imp,imp+impsz,20):
 desc=read(base+rva,20);ilt,stamp,fwd,name,iat=struct.unpack('<5I',desc)
 if not any((ilt,stamp,fwd,name,iat)):break
 for j in range(4096):
  raw=read(base+(ilt or iat)+8*j,8);value=int.from_bytes(raw,'little')
  if not value:break
  slot=base+iat+8*j
  if slot in slots:
   dll,dllhex=string(base+name);symbol,symbolhex=(None,None) if value>>63 else string(base+value+2)
   imports.append(dict(slot=hex(slot),dll=dll,symbol=symbol,ordinal=(value&0xffff) if value>>63 else None,descriptor_pc=hex(base+rva),descriptor_hex=desc.hex(),lookup_pc=hex(base+(ilt or iat)+8*j),lookup_hex=raw.hex(),dll_hex=dllhex,symbol_hex=symbolhex))
 else:raise AssertionError('Unterminated lookup')
else:raise AssertionError('Unterminated imports')
assert {int(x['slot'],16) for x in imports}==slots
directories=[]
def directory(off):
 assert 0<=off<=sz-16;header=read(base+root+off,16);named,ids=struct.unpack_from('<HH',header,12);count=named+ids;assert count<=4096 and off+16+8*count<=sz
 raw=read(base+root+off,16+8*count);copy='directory-'+hex(off)[2:]+'.bin';(R/copy).write_bytes(raw);directories.append(dict(offset=off,copy=copy,sha256=sha(raw)))
 return [dict(key=k,target=t) for j in range(count) for k,t in [struct.unpack_from('<II',raw,16+8*j)]]
def select(off,key):
 m=[e for e in directory(off) if e['key']==key];assert len(m)==1;return m[0]
typ=select(0,6);assert typ['target']>>31;block=select(typ['target']&0x7fffffff,0x784);assert block['target']>>31;langs=directory(block['target']&0x7fffffff);assert 0<len(langs)<=16;strings=[]
for e in langs:
 assert not e['key']>>31 and not e['target']>>31 and e['target']<=sz-16
 data=read(base+root+e['target'],16);rva,n,cp,res=struct.unpack('<4I',data);assert res==0 and 32<=n<=65536
 raw=read(base+rva,n);copy='strings-'+hex(e['key'])[2:]+'.bin';(R/copy).write_bytes(raw);strings.append(dict(language=hex(e['key']),data_entry_offset=e['target'],data_entry_hex=data.hex(),data_rva=hex(rva),size=n,codepage=cp,copy=copy,sha256=sha(raw)))
p=Path('Database/FFXII TZA/_experiments/evidence/native-exception-filter-tail/raw.json');c='4641092c065cb50c160ad7e2505586df4de03966';b=p.read_bytes();assert b==subprocess.check_output(['git','show',c+':'+p.as_posix()]);(R/'parent81-raw.json').write_bytes(b)
p=p.parent/'retained/filter240.bin';b=p.read_bytes();assert b==subprocess.check_output(['git','show',c+':'+p.as_posix()]) and b==read(0x79ad50,240);(R/'parent81-filter240.bin').write_bytes(b)
providers=[dict(path=str(Path(capstone.__file__).resolve()),sha256=sha(Path(capstone.__file__).read_bytes()))]
for p in sorted(Path(capstone.__file__).resolve().parent.rglob('*.dll')):providers.append(dict(path=str(p),sha256=sha(p.read_bytes())))
assert any(p['path'].lower().endswith('.dll') for p in providers)
raw=dict(method='A shipping original helper/selector/module-getter source and selected embedded RT_STRING block; no execution',reference=dict(exe_sha256=sha(image),files=files,parent81_commit=c,parent81_raw_sha256=sha((R/'parent81-raw.json').read_bytes()),parent81_filter_sha256=sha((R/'parent81-filter240.bin').read_bytes())),tools=dict(python=sys.version,python_sha256=sha(Path(sys.executable).read_bytes()),capstone=capstone.__version__,provider_files=providers),functions=functions,imports=imports,resource=dict(root_rva=hex(root),directory_bytes=sz,type=6,block='0x784',id='0x7837',entry=7,directories=directories,strings=strings),driver_sha256=sha(Path(__file__).read_bytes()),limits='Embedded strings and exact source module-order/block/prefix rules only. No actual registry initialization/HMODULE binding/FindResource language selection/resource-load result/visiblemessage/pointerlifetime/nativecallbacks/exceptionreach/EXP127cause. Boundary checks do not prove malformed-resource safety. Local source paths assume calls return; traps do not fall into next function. PC OFF/S19/fullL1+L2 NOT_MET')
(W/'raw.json').write_text(json.dumps(raw,indent=2)+'\n');print('CAPTURE82 selected original message resource and helper source',flush=True);subprocess.run([sys.executable,str(W/'check.py')],check=True)
