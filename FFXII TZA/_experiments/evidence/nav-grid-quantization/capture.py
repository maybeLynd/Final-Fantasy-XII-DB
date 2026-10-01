import csv,hashlib,importlib.util,io,json,struct,sys
from pathlib import Path
import capstone
HERE=Path(__file__).resolve().parent;sha=lambda b:hashlib.sha256(b).hexdigest()
reader=Path('Database/FFXII TZA/_experiments/evidence/license-check-exec/check.py')
sp=importlib.util.spec_from_file_location('verified_reader',reader);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
raw,secs=m.load_image();cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True
bodies=[];ins={}
for a,n in [(0x3924B0,607),(0x383740,252),(0x20E600,10),(0x861F14,6),(0x861F86,6)]:
 b=m.img_rd(raw,secs,a,n);ii=list(cs.disasm(b,a));assert sum(i.size for i in ii)==n
 assert ii[-1].mnemonic==('jmp' if n==6 else 'ret')
 bodies.append({'entry':hex(a),'size':n,'sha256':sha(b),'raw_hex':b.hex(),
  'instructions':[{'pc':hex(i.address),'bytes':i.bytes.hex(),'op':i.mnemonic,'args':i.op_str} for i in ii]})
 ins.update({i.address:i for i in ii})
def rip(pc):
 i=ins[pc];o=next(o for o in i.operands if o.type==capstone.CS_OP_MEM and o.mem.base==capstone.x86_const.X86_REG_RIP)
 return i.address+i.size+o.mem.disp
sites={'bitset_bytes':0x3924CB,'minA':0x392590,'minB':0x3925A0,'maxA':0x3925B1,'maxB':0x3925C1,
 'stack_copy074':0x3925DB,'stack_copy084':0x3925F4,'cell_size':0x392627,'rows':0x392654,'cols':0x39265D,
 'bitset_array':0x392677,'byte_array':0x3926EC,'working_mask':0x3926F3,'one':0x39260C,'nav_root':0x383755}
bindings={k:{'site':hex(v),'address':hex(rip(v))} for k,v in sites.items()}
assert rip(0x39262F)==rip(0x39260C)==0x1CEBBA8
constant=m.img_rd(raw,secs,rip(0x39260C),4);assert constant==struct.pack('<f',1.)
wanted={rip(a):a for a in [0x861F14,0x861F86]};imports=[]
pe=struct.unpack_from('<I',raw,0x3C)[0];ir,sz=struct.unpack_from('<II',raw,pe+24+112+8)
rd=lambda r,n:m.img_rd(raw,secs,m.IMG_LO+r,n)
for d in range(0,sz,20):
 desc=rd(ir+d,20);oft,_,_,name,ft=struct.unpack('<IIIII',desc)
 if not ft:break
 for k in range(1000):
  entry=rd(oft+8*k,8);v=struct.unpack('<Q',entry)[0]
  if not v:break
  addr=m.IMG_LO+ft+8*k
  if addr in wanted:
   assert not v>>63
   dll=rd(name,80).split(b'\0')[0];fn=rd(v+2,80).split(b'\0')[0]
   imports.append({'thunk':hex(wanted[addr]),'iat':hex(addr),'dll':dll.decode(),'name':fn.decode(),
    'descriptor_address':hex(m.IMG_LO+ir+d),'descriptor_hex':desc.hex(),
    'lookup_address':hex(m.IMG_LO+oft+8*k),'lookup_hex':entry.hex(),
    'hint_name_address':hex(m.IMG_LO+v),'hint_name_hex':rd(v,2+len(fn)+1).hex(),
    'dll_name_address':hex(m.IMG_LO+name),'dll_name_hex':(dll+b'\0').hex()})
assert {(x['thunk'],x['name']) for x in imports}=={('0x861f14','sqrtf'),('0x861f86','floorf')}
ret=HERE/'retained';ret.mkdir(exist_ok=True);refs=[]
for p in [reader,Path('Database/FFXII TZA/06-Movement-And-Navigation/CONTRACT-corridor-query-family.md'),
 Path('Database/FFXII TZA/04-Actor-Entity/Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md'),
 Path('Database/FFXII TZA/_types/types.tsv'),Path('Database/FFXII TZA/_types/fields.tsv')]:
 b=p.read_bytes();out=b;scope='complete file'
 if p.suffix=='.tsv':
  lines=b.splitlines(keepends=True);chosen=[lines[0]]+[x for x in lines[1:] if x.startswith(b'NavGridParams\t')]
  assert len(chosen)>1;out=b''.join(chosen);scope='Exact header and NavGridParams rows only; full source hash retained, not a mirror/census.'
 (ret/p.name).write_bytes(out);refs.append({'path':p.as_posix(),'full_source_bytes':len(b),'full_source_sha256':sha(b),
  'retained':'retained/'+p.name,'retained_bytes':len(out),'retained_sha256':sha(out),'scope':scope})
s={'method':'A exact original flow/operands and qualified import identity; arithmetic illustrations conditional, not execution',
 'exe_path':m.EXE,'exe_sha256':sha(raw),'image_base':hex(m.IMG_LO),'capstone_version':capstone.__version__,
 'python_version':sys.version,'python_sha256':sha(Path(sys.executable).read_bytes()),
 'bodies':bodies,'bindings':bindings,'constant_hex':constant.hex(),'imports':imports,'references':refs,
 'limits':'No new isolated/native/live run, no DLL implementation/actual allocation or initialized map observation. Intended named math/f32 round-nearest for illustrations; positive dimensions only. Native callbacks/release/lifetime, authored occurrence, exceptional states and all-byte defaults unclaimed.'}
(HERE/'source.json').write_text(json.dumps(s,indent=2)+'\n');print('Captured exact builder/getter/codec, import-name controls, constant and consumer preimages.',flush=True)
