"""A source-derived recipe and discriminating conditional calculations, not execution."""
import hashlib,importlib.util,json,struct,sys
from pathlib import Path
import capstone
W=Path(__file__).resolve().parent;R=W/'retained';sha=lambda b:hashlib.sha256(b).hexdigest()
raw=json.loads((W/'raw.json').read_text());ref=raw['reference']
assert raw['driver_sha256']==sha((W/'source.py').read_bytes())==sha((R/'driver-before-run.py').read_bytes())
assert sha((R/'shipping-reader.py').read_bytes())==ref['reader_sha256'] and sha((R/'reg_tracking.py').read_bytes())==ref['policy_sha256']
sp=importlib.util.spec_from_file_location('rd',R/'shipping-reader.py');rd=importlib.util.module_from_spec(sp);sp.loader.exec_module(rd);image,ss=rd.load_image();assert sha(image)==ref['exe_sha256']=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
sp=importlib.util.spec_from_file_location('roles',R/'reg_tracking.py');roles=importlib.util.module_from_spec(sp);sp.loader.exec_module(roles)
code=(R/'original353.bin').read_bytes();assert code==rd.img_rd(image,ss,0x712180,353) and sha(code)==ref['body_sha256']
assert sha((R/'extent-manifest.json').read_bytes())==ref['parent_manifest_sha256'];extent=json.loads((R/'extent-raw.json').read_text());assert code.hex()==extent['observation']['raw_hex'] and extent['reference']['exe_sha256']==ref['exe_sha256']
cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True;seq=list(cs.disasm(code,0x712180));by={i.address:i for i in seq};assert len(seq)==82 and sum(i.size for i in seq)==353 and not any(i.mnemonic=='call' for i in seq)
records=[dict(pc=hex(i.address),bytes=i.bytes.hex(),op=i.mnemonic,args=i.op_str,memory=[dict(operand=j,size=o.size,base=i.reg_name(o.mem.base),index=i.reg_name(o.mem.index),disp=o.mem.disp,kind=roles.op_kind(i,o,j)) for j,o in enumerate(i.operands) if o.type==capstone.CS_OP_MEM]) for i in seq];assert records==raw['source']
def exact(pc,op,args):assert by[pc].mnemonic==op and by[pc].op_str==args,(hex(pc),op,args)
for pc,op,args in [(0x712180,'mov','r10, rcx'),(0x712183,'test','rcx, rcx'),(0x712186,'je','0x7122dd'),(0x71218C,'test','edx, edx'),(0x71218E,'js','0x7121b3'),(0x712190,'mov','eax, 7'),(0x71219C,'cmp','edx, eax'),(0x71219E,'cmovl','eax, edx'),(0x7121A1,'movsxd','rdx, eax'),(0x7121B3,'test','r8d, r8d'),(0x7121B6,'js','0x71222d'),(0x7121BF,'mov','eax, 0xa'),(0x7121C4,'mov','ecx, 0x13'),(0x7121C9,'cmovne','eax, ecx'),(0x7121CC,'cmp','r8d, eax'),(0x7121CF,'cmovl','eax, r8d'),(0x7121D3,'cdqe',''),(0x7121D5,'imul','rcx, rax, 0x1c'),(0x712225,'test','r9d, r9d'),(0x712228,'jns','0x712236'),(0x71222A,'mov','r9d, edx'),(0x71222D,'test','r9d, r9d'),(0x712230,'js','0x7122dd'),(0x712236,'mov','eax, 9'),(0x71223B,'cmp','r9d, eax'),(0x71223E,'cmovl','eax, r9d'),(0x712242,'cdqe',''),(0x712244,'imul','rcx, rax, 0x38'),(0x7122DD,'mov','rax, r10'),(0x7122E0,'ret','')]:exact(pc,op,args)
for pc,a in [(0x712195,0x1F3C5B0),(0x7121B8,0xD9F05E),(0x7121D9,0x1F3C5F0),(0x712248,0x1F3C820)]:
 i=by[pc];o=next(o for o in i.operands if o.type==capstone.CS_OP_MEM);assert i.reg_name(o.mem.base)=='rip' and i.address+i.size+o.mem.disp==a and raw['targets'][hex(pc)]==hex(a)
assert by[0x7121B8].mnemonic=='cmp' and by[0x7121B8].operands[0].size==1 and by[0x7121B8].operands[1].imm==0
pairs=[[],[],[]]
for pos,i in enumerate(seq):
 if i.mnemonic!='mov' or i.operands[0].type!=capstone.CS_OP_MEM or i.reg_name(i.operands[0].mem.base)!='r10':continue
 o=i.operands[0];prev=seq[pos-1];assert o.size==4 and roles.op_kind(i,o,0)=='w' and prev.mnemonic=='mov' and prev.operands[1].type==capstone.CS_OP_MEM and prev.operands[0].reg==i.operands[1].reg
 load=prev.operands[1];assert prev.reg_name(load.mem.base)=='rcx' and load.size==4 and roles.op_kind(prev,load,1)=='r'
 group=0 if i.address<0x7121B3 else 1 if i.address<0x712225 else 2
 pairs[group].append(dict(read_pc=hex(prev.address),write_pc=hex(i.address),source_offset=load.mem.disp,destination_offset=o.mem.disp))
assert [[x['source_offset'] for x in g] for g in pairs]==[[0,4],list(range(0,28,4)),list(range(0,56,4))]
assert [[x['destination_offset'] for x in g] for g in pairs]==[[0x4C,0x54],[0x7C,0x84,0x88,0xCC,0x8C,0xE4,0xE8],list(range(0x90,0xC8,4))]
assert by[0x712207].op_str=='edx, dword ptr [rcx + 0x10]' and by[0x71220A].op_str=='dword ptr [r10 + 0x8c], edx'
assert next(x for x in records if x['pc']=='0x712195')['memory'][0]['kind']=='addr' and next(x for x in records if x['pc']=='0x7121a7')['memory'][0]['kind']=='w'
for t in raw['tables']:
 data=(R/(t['name']+'.bin')).read_bytes();assert data.hex()==t['raw_hex'] and sha(data)==t['sha256'] and len(data)==t['rows']*t['stride'] and data==rd.img_rd(image,ss,int(t['entry'],16),len(data))
 assert t['words']==[list(struct.unpack_from('<'+'I'*(t['stride']//4),data,j*t['stride'])) for j in range(t['rows'])]
assert [t['rows'] for t in raw['tables']]==[8,20,10]
assert (R/'mode-byte.bin').read_bytes()==rd.img_rd(image,ss,0xD9F05E,1)==bytes.fromhex(raw['mode_byte']['file_hex'])
for mapping in raw['mappings']:
 a,n=int(mapping['entry'],16),mapping['bytes'];s=mapping['section'];off=mapping['file_offset'];assert int(s['entry'],16)<=a and a+n<=int(s['entry'],16)+min(s['virtual_bytes'],s['raw_bytes'])
 assert off==s['raw_offset']+a-int(s['entry'],16) and image[off:off+n]==rd.img_rd(image,ss,a,n)
control=raw['control'];private=bytearray(code);private[0x71222A-0x712180:0x71222D-0x712180]=b'\x90'*3
assert private.hex()==control['private_hex'] and sha(private)==control['private_sha256']!=ref['body_sha256']
mutated=list(cs.disasm(private,0x712180));assert [dict(pc=hex(i.address),bytes=i.bytes.hex(),op=i.mnemonic,args=i.op_str) for i in mutated]==control['decoded']
assert [i.mnemonic for i in mutated if 0x71222A<=i.address<0x71222D]==['nop']*3
signed=lambda x:((x&0xFFFFFFFF)^0x80000000)-0x80000000
def recipe(target,first,second,third,flag,fallback):
 result=dict(target=hex(target),selectors_low32_signed=[signed(x) for x in [first,second,third]],mode_nonzero=bool(flag),rows=[None,None,None],writes=[])
 if not target:return result
 a,b,c=result['selectors_low32_signed']
 def apply(group,row):
  result['rows'][group]=row;words=raw['tables'][group]['words'][row]
  for x in pairs[group]:result['writes'].append(dict(destination_offset=hex(x['destination_offset']),word=f'{words[x["source_offset"]//4]:08x}'))
 if a>=0:apply(0,min(a,7))
 if b>=0:
  row=min(b,19 if flag else 10);apply(1,row)
  if c<0 and fallback:c=signed(raw['tables'][1]['words'][row][4])
 result['third_effective_signed']=c
 if c>=0:apply(2,min(c,9))
 return result
has_fallback=by[0x71222A].mnemonic=='mov' and by[0x71222A].op_str=='r9d, edx';assert has_fallback
examples=dict(null=recipe(0,0,0,0,0,has_fallback),all_negative=recipe(1,-1,-1,-1,0,has_fallback),selected_second_negative_third=recipe(1,-1,0,-1,0,has_fallback),explicit_third=recipe(1,-1,0,9,0,has_fallback),upper_clamps_mode_zero=recipe(1,0x7FFFFFFF,0x7FFFFFFF,0x7FFFFFFF,0,has_fallback),upper_clamps_mode_nonzero=recipe(1,0x7FFFFFFF,0x7FFFFFFF,0x7FFFFFFF,1,has_fallback))
assert not examples['null']['writes'] and not examples['all_negative']['writes']
assert examples['selected_second_negative_third']['rows']==[None,0,1] and len(examples['selected_second_negative_third']['writes'])==21
assert examples['explicit_third']['rows']==[None,0,9] and next(x for x in examples['explicit_third']['writes'] if x['destination_offset']=='0x8c')['word']=='00000001'
assert examples['upper_clamps_mode_zero']['rows']==[7,10,9] and examples['upper_clamps_mode_nonzero']['rows']==[7,19,9]
negative_control=recipe(1,-1,0,-1,0,False);assert negative_control['rows']==[None,0,None] and len(negative_control['writes'])==7
assert all(1<=signed(row[4])<=5 for row in raw['tables'][1]['words']), 'All bounded original second rows supply a nonnegative third default'
for x in raw['tools']['providers']:assert sha(Path(x['path']).read_bytes())==x['sha256'] and Path(x['path']).stat().st_size==x['bytes']
assert sha(Path(sys.executable).read_bytes())==raw['tools']['python_sha256']
result=dict(method=raw['method'],reference=ref,ordered_write_pairs=pairs,conditional_examples=examples,private_source_control=negative_control,interpretation='Null target returns unchanged; first negative selector skips its group, second negative skips its group, but third negative is not independent skip: a selected second row supplies its +10 word through EDX->R9D. All20 original bounded second rows have defaults1..5, so this condition selects third row. Nonnegative supplied third takes precedence and cap9, while target+8C still stores the second-row default rather than that effective third selector. Original upper caps7 and(modebyte!=0 ?19:10) and9, scattered DWORD transfers/order and raw bit patterns preserved; no object/system/field semantic meaning guessed.',limits=raw['limits']+' Conditional recipes additionally require valid stable tables and destination disjoint from tables/mode byte; no generic overlap or object extent/lifetime guarantee. Source field envelope is maxwrite+E8 width4, not a constructor size.',cleanup=raw['cleanup'])
if (W/'result.json').exists():assert json.loads((W/'result.json').read_text())==result
else:(W/'result.json').write_text(json.dumps(result,indent=2)+'\n')
if (W/'manifest.json').exists():
 for x in json.loads((W/'manifest.json').read_text())['members']:
  data=(W/x['path']).read_bytes();assert len(data)==x['bytes'] and sha(data)==x['sha256']
print('PASS_SELECTOR_COUPLING56 source353B/shareddefault store-LEA/3table bindings/signed guards/caps/source-only fallback bypass discriminator; original static recipe, not execution or named type/admission proof')
