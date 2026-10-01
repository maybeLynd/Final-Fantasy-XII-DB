"""Readonly source/extent/domain/alias controls; no native or FF12 execution."""
import hashlib,importlib.util,json,struct
from pathlib import Path
import capstone
from source_rules import facts,conditional_tail,check_extent
W=Path(__file__).resolve().parent;R=W/'retained';sha=lambda b:hashlib.sha256(b).hexdigest()
r=json.loads((W/'result.json').read_text());raw=json.loads((W/'raw-source.json').read_text());assert r['reference']==raw['reference']
assert r['driver_sha256']==raw['driver_sha256']==sha((W/'capture.py').read_bytes())==sha((R/'driver-before-run.py').read_bytes())
assert r['rules_sha256']==raw['rules_sha256']==sha((W/'source_rules.py').read_bytes())==sha((R/'source-rules-before-run.py').read_bytes())
for x in raw['tools']['provider_files']:assert sha(Path(x['path']).read_bytes())==x['sha256'] and Path(x['path']).stat().st_size==x['bytes']
for name,key in [('shipping-reader.py','reader_sha256'),('reg_tracking.py','policy_sha256')]:assert sha((R/name).read_bytes())==r['reference'][key]
sp=importlib.util.spec_from_file_location('rd',R/'shipping-reader.py');rd=importlib.util.module_from_spec(sp);sp.loader.exec_module(rd);d,ss=rd.load_image();assert sha(d)==r['reference']['exe_sha256']=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
sp=importlib.util.spec_from_file_location('roles',R/'reg_tracking.py');roles=importlib.util.module_from_spec(sp);sp.loader.exec_module(roles)
cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True;ii={}
assert len(raw['bodies'])==2 and sum(b['bytes'] for b in raw['bodies'])==716
for b in raw['bodies']:
 a=int(b['entry'],16);code=(R/(b['name']+'.bin')).read_bytes();assert code==rd.img_rd(d,ss,a,b['bytes']) and sha(code)==b['sha256']
 seq=list(cs.disasm(code,a));assert sum(i.size for i in seq)==len(code);records=[]
 for i in seq:
  records.append(dict(pc=hex(i.address),bytes=i.bytes.hex(),op=i.mnemonic,args=i.op_str,memory=[dict(operand_index=j,size=o.size,base=i.reg_name(o.mem.base),index=i.reg_name(o.mem.index),disp=o.mem.disp,kind=roles.op_kind(i,o,j)) for j,o in enumerate(i.operands) if o.type==capstone.CS_OP_MEM],written=sorted(roles.written(i))))
 assert records==b['instructions'];ii.update({i.address:i for i in seq})
for x in raw['extents']:
 rec=rd.img_rd(d,ss,rd.IMG_LO+int(x['directory_rva'],16)+x['record_offset'],12);assert rec.hex()==x['record_hex'];a,e,u=struct.unpack('<III',rec)
 assert [hex(v+rd.IMG_LO) for v in [a,e,u]]==[x['entry'],x['end'],x['unwind']]
 assert rd.img_rd(d,ss,int(x['unwind'],16),len(bytes.fromhex(x['unwind_hex']))).hex()==x['unwind_hex']
check_extent(raw['extents']);refused=False
try:check_extent(raw['extents'][:1])
except AssertionError:refused=True
assert refused and len(raw['extents'])==6
code=(R/'populator.bin').read_bytes();f=facts(code);assert f==r['source_facts'] and f['pointer_limit']==128 and f['authored_unsigned_min_limit']==32 and f['registry_base']==160
for pc,j,role in [(0x392777,0,'w'),(0x3928B9,0,'rw'),(0x3927E0,1,'addr')]:assert roles.op_kind(ii[pc],ii[pc].operands[j],j)==role
g=ii[0x32A6B0];o=g.operands[1];assert g.address+g.size+o.mem.disp==0x209A670 and ii[0x32A6B7].op_str=='eax, dword ptr [rax + 0x22c]'
assert ii[0x32A6BD].mnemonic=='ret' and [ii[a].mnemonic for a in [0x32A6B0,0x32A6B7]]==['mov','mov']
m=(R/'labelled-pointer-limit-129.bin').read_bytes();n=(R/'labelled-single-count-read.bin').read_bytes();expected=bytearray(code);j=0x3927FF-0x392740;expected[j+1:j+5]=struct.pack('<I',129);assert m==expected
expected=bytearray(code);j=0x392991-0x392740;expected[j:j+5]=b'\x90'*5;assert n==expected
assert facts(m)['pointer_limit']==facts(m)['authored_base']==129 and not facts(n)['conditional_second_getter']
cases=[conditional_tail(f,a,b) for a,b in [(127,127),(128,129),(127,129),(-1,2),(0,-1)]];assert cases==r['conditional_examples'] and cases[2]['last_id']==288
assert conditional_tail(facts(n),127,129)['last_id']==286 and sha(m)!=sha(code) and sha(n)!=sha(code)
assert r['controls']==dict(private_pointer_limit=129,private_authored_base=129,original_inconsistent_last_id=288,single_read_control_last_id=286,immutable_source_refuses_both=True)
assert sha((R/'teardown-parent-raw.json').read_bytes())==r['reference']['parent_raw_sha256']
bind=json.loads((R/'teardown-parent-raw.json').read_text())['memset_import']
for ak,bk in [('descriptor_va','descriptor_hex'),('lookup_va','lookup_hex'),('name_va','name_hex'),('dll_va','dll_hex')]:
 value=bytes.fromhex(bind[bk]);assert rd.img_rd(d,ss,int(bind[ak],16),len(value))==value
for c in r['consumers']:assert sha((R/c['retained']).read_bytes())==c['retained_sha256']
b=json.loads((W/'trailer-binding-result.json').read_text());T=R/'trailer-binding'
assert b['reference']==raw['reference'] and b['driver_sha256']==sha((W/'bind_trailer.py').read_bytes())==sha((T/'driver-before-run.py').read_bytes())
getter=(T/'root-return-getter.bin').read_bytes();assert getter==rd.img_rd(d,ss,0x383840,8) and sha(getter)==b['getter']['sha256']
seq=list(cs.disasm(getter,0x383840));assert len(seq)==2 and seq[0].mnemonic=='mov' and seq[0].op_str.startswith('rax, qword ptr [rip') and seq[1].mnemonic=='ret'
assert seq[0].address+seq[0].size+seq[0].operands[1].mem.disp==0x2AEDFB0 and roles.op_kind(seq[0],seq[0].operands[1],1)=='r'
assert ii[0x3928E7].operands[0].imm==0x383840 and ii[0x3928F4].op_str=='r15, rax'
assert ii[0x392909].op_str=='dword ptr [rax + 0x24], edx' and ii[0x392920].op_str=='ecx, dword ptr [r15 + 0x28]' and ii[0x392924].operands[0].imm==0x20E600
assert ii[0x392929].op_str=='edx, word ptr [rdi + rax]' and ii[0x39295E].op_str=='rdi, 0x20'
for pc,args in [(0x392946,'xmm3, dword ptr [rcx + 0xc]'),(0x39293A,'xmm3, dword ptr [rcx + 0xc]'),(0x39293F,'xmm3, dword ptr [rcx + 0x10]'),(0x39294B,'xmm2, dword ptr [rcx + 8]'),(0x392950,'xmm1, dword ptr [rcx + 4]')]:assert ii[pc].op_str==args
for c in b['consumers']:assert sha((T/c['retained']).read_bytes())==c['retained_sha256']
bad=W/'invalid-single-unwind-assumption';failure=json.loads((bad/'diagnostic.json').read_text());assert failure['status']=='INVALID_EXTENT_PRECONDITION'
assert sha((bad/'capture-before-fix.py').read_bytes())==failure['driver_sha256']==sha((bad/'retained-partial/driver-before-run.py').read_bytes())
assert (bad/'retained-partial/populator.bin').read_bytes()==code and not (bad/'result.json').exists()
for x in raw['tools']['provider_files']:assert sha(Path(x['path']).read_bytes())==x['sha256']
if (W/'manifest.json').exists():
 members=json.loads((W/'manifest.json').read_text())['members'];assert members
 for x in members:
  data=(W/x['path']).read_bytes();assert len(data)==x['bytes'] and sha(data)==x['sha256']
print('PASS_NAV_POPULATION source716B+getter8B/six chained PE ranges/root-only refusal/shared store-LEA-RMW/ID domains/two-read control/trailer consumer binding/retained invalid first run; no live race or whole memory-safety proof')
