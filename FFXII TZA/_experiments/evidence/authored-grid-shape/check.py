"""Check original instructions and an authored map case independently of capture notes."""
import hashlib,importlib.util,json,math,struct,sys,capstone
from pathlib import Path
from capstone import Cs,CS_ARCH_X86,CS_MODE_64
w=Path(__file__).resolve().parent;s=json.loads((w/'source.json').read_text())
assert s['capstone_version']==capstone.__version__ and s['python_version']==sys.version
assert Path(s['python_executable']).resolve()==Path(sys.executable).resolve()
assert hashlib.sha256(Path(sys.executable).read_bytes()).hexdigest()==s['python_sha256']
reader=Path(s['reader_path']);assert hashlib.sha256(reader.read_bytes()).hexdigest()==s['reader_sha256']
spec=importlib.util.spec_from_file_location('shipping_reader',reader);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
raw,secs=m.load_image();assert m.SHA==s['exe_sha256']
ins={}
for b in s['bodies']:
 e=int(b['entry'],0);original=m.img_rd(raw,secs,e,b['size'])
 assert original.hex()==b['raw_hex'] and hashlib.sha256(original).hexdigest()==b['sha256']
 ii=list(Cs(CS_ARCH_X86,CS_MODE_64).disasm(original,e))
 assert ii[0].address==e and ii[-1].mnemonic=='ret' and ii[-1].address+ii[-1].size==e+b['size']
 assert [{'pc':hex(i.address),'bytes':i.bytes.hex(),'op':i.mnemonic,'args':i.op_str} for i in ii]==b['instructions']
 ins.update({i.address:i for i in ii})
def instr(pc,op,args):
 i=ins[pc];assert(i.mnemonic,i.op_str)==(op,args),(hex(pc),i.mnemonic,i.op_str)
def dest(pc):
 i=ins[pc];return i.address+i.size+i.operands[1].mem.disp
md=Cs(CS_ARCH_X86,CS_MODE_64);md.detail=True
for pc in (0x38416D,):
 i=next(md.disasm(m.img_rd(raw,secs,pc,7),pc));assert i.address==pc and i.mnemonic=='mov'
 assert i.address+i.size+i.operands[0].mem.disp==0x2AEDFB0
instr(0x384219,'mov','ecx, dword ptr [rcx + 0x20]')
instr(0x38421C,'call','0x20e600');instr(0x384236,'mov','dword ptr [rcx + 0x20], eax')
instr(0x38423B,'call','0x20e600');instr(0x384240,'mov','ecx, dword ptr [rax + 8]')
instr(0x384243,'call','0x20e600');instr(0x384267,'mov','dword ptr [rax + 8], ebx')
instr(0x384279,'mov','ecx, dword ptr [rax + 0xc]')
instr(0x3842A0,'mov','dword ptr [rax + 0xc], ebx')
instr(0x20E600,'mov','eax, ecx')
instr(0x20E602,'add','rax, qword ptr [rip + 0x1d74f27]')
instr(0x20E620,'sub','ecx, dword ptr [rip + 0x1d74f0a]')
prior=Path(s['prior_constructor_source']);b=prior.read_bytes()
assert hashlib.sha256(b).hexdigest()==s['prior_constructor_source_sha256']
p=json.loads(b);assert p['exe_sha256']==s['exe_sha256']
bb={int(x['entry'],0):x for x in p['bodies']}
assert int(bb[0x383740]['size'])==252 and int(bb[0x3924b0]['size'])==607
getter={int(x['pc'],0):(x['op'],x['args']) for x in bb[0x383740]['instructions']}
assert getter[0x383771]==('mov','ecx, dword ptr [rax + 0x20]')
assert getter[0x383779]==('call','0x20e600') and getter[0x38377E]==('movsx','ecx, word ptr [rax + 4]')
assert getter[0x38379C]==('movsx','ecx, word ptr [rax + 6]')
assert getter[0x3837CD]==('movzx','ecx, byte ptr [rax]') and getter[0x3837D7][0]=='imul'
assert getter[0x383805]==('movzx','ecx, byte ptr [rax + 1]') and getter[0x38380E][0]=='imul'
mpk=Path(s['map_pack']['path']);d=mpk.read_bytes();a=s['map_pack']
assert len(d)==a['bytes'] and hashlib.sha256(d).hexdigest()==a['sha256']
n=struct.unpack_from('<I',d,0)[0];sizes=struct.unpack_from('<%dI'%n,d,4)
pos=((n+1)*4+0x3f)&~0x3f;section=None
for i,z in enumerate(sizes):
 if not z:continue
 pos+=0x40;assert pos+z<=len(d)
 if i==4:section=d[pos:pos+z];break
 pos+=z
assert section is not None and pos==a['slot_offset']
assert section==(w/'slot4.bin').read_bytes() and len(section)==a['slot_size']
assert hashlib.sha256(section).hexdigest()==a['slot_sha256']
assert struct.unpack_from('<I',section,0)[0]==1
ofs=[struct.unpack_from('<I',section,o)[0] for o in (0xC,0x10,0x14,0x18,0x1C,0x20)]
assert all(0<o<len(section) for o in ofs) and ofs[-1]==a['grid_offset']
g=ofs[-1];assert section[g:g+16].hex()==a['grid_header_hex']
cw,ch,cols,rows=struct.unpack_from('<4B',section,g)
ox,oz=struct.unpack_from('<hh',section,g+4);table,pool=struct.unpack_from('<II',section,g+8)
assert [cw,ch]==a['cell_size'] and [cols,rows]==a['counts'] and [ox,oz]==a['origin']
assert [cw*cols,ch*rows]==a['rectangle_size']==[50,50]
assert table+2*cols*rows<=len(section) and 0<pool<len(section)
nr=struct.unpack_from('<H',section,10)[0];assert nr==a['region_count'] and 0<nr<=128
live=0
for k in range(cols*rows):
 t=struct.unpack_from('<H',section,table+2*k)[0]
 if t==0xffff:continue
 live+=1;q=pool+t;assert q<len(section)
 while q<len(section) and section[q]!=0xff:assert section[q]<nr;q+=1
 assert q<len(section)
assert live==a['nonempty_cells']==100
f=lambda v:struct.unpack('<f',struct.pack('<f',v))[0]
def calc(initial,quant):
 w=h=50.;nx=math.trunc(f(w/initial));ny=math.trunc(f(h/initial))
 refined=max(f(w/nx),f(h/ny));cell=f((math.floor(refined) if quant else refined)+1.)
 co=math.trunc(f(f(w+f(cell-1.))/cell));ro=math.trunc(f(f(h+f(cell-1.))/cell))
 return {'initial':initial,'initial_counts':[nx,ny],'refined':refined,'cell':cell,'shape':[co,ro],'conditional_allocation_argument':co*ro*37+36}
c0=f(math.sqrt(f(f(50.*50.)/275.)))
word=struct.unpack('<I',struct.pack('<f',c0))[0]
neighbours=[struct.unpack('<f',struct.pack('<I',word+i))[0] for i in (-2,-1,0,1,2)]
correct=[calc(x,True) for x in neighbours];wrong=[calc(x,False) for x in neighbours]
assert {tuple(x['shape']) for x in correct}=={(13,13)} and {tuple(x['shape']) for x in wrong}=={(12,12)}
assert {x['cell'] for x in correct}=={4.} and {x['cell'] for x in wrong}=={4.125}
assert correct[2]['initial_counts']==[16,16] and correct[2]['refined']==3.125
out={'status':'PASS_STATIC_AUTHOR_CASE','source':'exact verified image loader/codec plus immutable prior builder/getter','asset':'one shipped extracted MPK slot4 checked by full-file SHA and valid100 region lists','condition':'If this authored header is supplied through the source loader/getter with ordinary f32 nearest, the original builder cell4/13x13/arg6289 differs from omit-floor+1 cell4.125/12x12/arg5364. Initial sqrtf ±2 adjacent f32 values leave both shapes unchanged.','original_conditional':correct[2],'omitted_floor_conditional':wrong[2],'sqrtf_neighbourhood':neighbours,'new_original_code_or_live_executions':0,'limits':'No observed game load, builder invocation, malloc, imported DLL execution, lifetime, or 461-map prevalence.'}
(w/'validation.json').write_text(json.dumps(out,indent=2)+'\n')
print(out['status'],'50x50 authored header; source shape13x13 vs omitted-floor12x12 (conditional), no original execution',flush=True)
