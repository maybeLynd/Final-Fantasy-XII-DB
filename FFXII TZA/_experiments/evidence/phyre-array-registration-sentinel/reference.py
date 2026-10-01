import csv,hashlib,json,struct
from pathlib import Path
import capstone
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[4]
path=ROOT/'Database/Tools/work/exe/FFXII_TZA.exe';raw=path.read_bytes()
sha=hashlib.sha256(raw).hexdigest();assert sha=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
pe=struct.unpack_from('<I',raw,0x3c)[0];opt=struct.unpack_from('<H',raw,pe+20)[0];secs=[]
for i in range(struct.unpack_from('<H',raw,pe+6)[0]):
 o=pe+24+opt+i*40;vs,va,rs,ro=struct.unpack_from('<IIII',raw,o+8);secs.append((0x120000+va,min(vs,rs),ro))
def read(a,n):
 for v,s,o in secs:
  if v<=a and a+n<=v+s:return raw[o+a-v:o+a-v+n]
 raise ValueError('unbacked original image range')
md=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);md.detail=True
functions={x['entry']:x for x in csv.DictReader((ROOT/'Database/Tools/work/graph/functions.tsv').open(),delimiter='\t')}
addresses=[0x5d9890,0x5cf0f0,0x5e67c0,0x1614c0,0x632a10,0x632960]
r={'exe_sha256':sha,'method':'A static original descriptor identity, not execution','capstone':capstone.__version__,'bodies':[]}
for a in addresses:
 n=int(functions[f'{a:08X}']['body_bytes']);assert 0<n<512;b=read(a,n);ins=list(md.disasm(b,a));assert ins[-1].address+ins[-1].size==a+n
 r['bodies'].append({'address':hex(a),'bytes':n,'hex':b.hex(),'sha256':hashlib.sha256(b).hexdigest(),'instructions':[{'a':hex(i.address),'bytes':i.bytes.hex(),'op':i.mnemonic,'args':i.op_str} for i in ins]})
 print('\n',hex(a),n)
 for i in ins:print(f'{i.address:08X} {i.mnemonic:8} {i.op_str}')
 # Capture referenced strings only; the reducer will require exact type name.
 for i in ins:
  for op in i.operands:
   if op.type==capstone.x86.X86_OP_MEM and op.mem.base==capstone.x86.X86_REG_RIP:
    t=i.address+i.size+op.mem.disp
    try:s=read(t,128).split(b'\0',1)[0]
    except ValueError:continue
    if s in [b'PMeshInstanceSegmentContext',b'm_streamBindings']:
     r.setdefault('strings',{})[s.decode()]={'address':hex(t),'bytes_hex':(s+b'\0').hex(),'text':s.decode()}
r['static_initializer_descriptor']='0x02CB6D80'
r['final_descriptor_vtable']={'address':'0x00D38540','slot60_address':'0x00D385A0','slot60_hex':read(0xd385a0,8).hex(),'slot60':hex(struct.unpack('<Q',read(0xd385a0,8))[0])}
assert r['final_descriptor_vtable']['slot60']=='0x5cf0f0'
# Own-object RTTI absence cannot be inferred from template RTTI hits.
needle=b'.?AVPMeshInstanceSegmentContext@';r['own_class_rtti_v_hits']=raw.count(needle);r['own_class_rtti_u_hits']=raw.count(needle.replace(b'AV',b'AU'))
r['positive_own_class_rtti_hits']=raw.count(b'.?AVPAnimatableComponent@');assert r['positive_own_class_rtti_hits']>0
assert r.get('strings',{}).get('PMeshInstanceSegmentContext') and r['strings'].get('m_streamBindings') and r['own_class_rtti_v_hits']==r['own_class_rtti_u_hits']==0
(HERE/'reference.json').write_text(json.dumps(r,indent=2)+'\n')
