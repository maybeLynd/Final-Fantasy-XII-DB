"""Readonly source/import/role/branch controls, not original code execution."""
import hashlib,importlib.util,json,sys
from pathlib import Path
import capstone
W=Path(__file__).resolve().parent;R=W/'retained';sha=lambda b:hashlib.sha256(b).hexdigest()
r=json.loads((W/'result.json').read_text());raw=json.loads((W/'raw-source.json').read_text())
assert r['driver_sha256']==raw['driver_sha256']==sha((W/'capture.py').read_bytes())==sha((R/'driver-before-run.py').read_bytes())
assert r['reference']==raw['reference'] and r['reference']['exe_sha256']=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
assert sha((R/'shipping-reader.py').read_bytes())==r['reference']['reader_sha256'] and sha((R/'reg_tracking.py').read_bytes())==r['reference']['policy_sha256']
sp=importlib.util.spec_from_file_location('rr',R/'shipping-reader.py');rd=importlib.util.module_from_spec(sp);sp.loader.exec_module(rd);image,secs=rd.load_image();assert sha(image)==r['reference']['exe_sha256']
sp=importlib.util.spec_from_file_location('reviewed_roles',R/'reg_tracking.py');roles=importlib.util.module_from_spec(sp);sp.loader.exec_module(roles)
cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True;ii={}
assert len(raw['bodies'])==3 and sum(b['bytes'] for b in raw['bodies'])==717
for b in raw['bodies']:
    code=(R/(b['name']+'.bin')).read_bytes();a=int(b['entry'],16);assert code==rd.img_rd(image,secs,a,b['bytes']) and sha(code)==b['sha256']
    seq=list(cs.disasm(code,a));assert sum(i.size for i in seq)==len(code)
    records=[]
    for i in seq:
        records.append(dict(pc=hex(i.address),bytes=i.bytes.hex(),op=i.mnemonic,args=i.op_str,memory=[dict(operand_index=j,size=o.size,base=i.reg_name(o.mem.base),index=i.reg_name(o.mem.index),disp=o.mem.disp,kind=roles.op_kind(i,o,j)) for j,o in enumerate(i.operands) if o.type==capstone.CS_OP_MEM],written=sorted(roles.written(i))))
    assert records==b['instructions'];ii.update({i.address:i for i in seq})
p=json.loads((R/'parent-source.json').read_text());pb=next(b for b in p['bodies'] if b['entry']=='0x3924b0');assert bytes.fromhex(pb['raw_hex'])==(R/'builder.bin').read_bytes() and pb['sha256']=='0a7ec1000ef3d48a471ff9200675b11ef90717fedcb53b50afa84a4281e236f5'
# Structural source detector: sole post-return conditional is JE over the init;
# opaque unlock calls remain and RBX is locally unchanged until RAX receives it.
assert ii[0x3845B5].op_str=='rbx, rax' and ii[0x3845B8].op_str=='rax, rax'
assert ii[0x3845BB].mnemonic=='je' and ii[0x3845BB].operands[0].imm==0x3845CB
assert ii[0x3845C6].operands[0].imm==0x36C660 and ii[0x3845DA].op_str=='rax, rbx'
for i in ii.values():
    if 0x3845B8<=i.address<0x3845DA:assert 'rbx' not in roles.written(i)
original=(R/'wrapper.bin').read_bytes();mut=(R/'labelled-je-to-jne.bin').read_bytes();delta=[j for j,(a,b) in enumerate(zip(original,mut)) if a!=b]
assert len(original)==len(mut) and delta==[0x3845BB-0x384580] and original[delta[0]]==0x74 and mut[delta[0]]==0x75
mj=next(i for i in cs.disasm(mut,0x384580) if i.address==0x3845BB);assert mj.mnemonic=='jne' and mj.operands[0].imm==0x3845CB
assert sha(mut)!=sha(original) # actual immutable-source binding predicate refuses mutant
assert [c['name'] for c in r['cases']]==['returning-zero','returning-nonzero']
for c in r['cases']:
    path=c['path'];assert path['visited'][0]=='0x3845b5' and path['visited'][-1]=='0x3845e7' and len(path['visited'])>0
    assert path['calls']==(['0x36c110','0x36c140'] if c['name']=='returning-zero' else ['0x36c660','0x36c110','0x36c140'])
    assert path['initializer']==(c['name']=='returning-nonzero')
assert r['source_controls']['branch']['null_path']['initializer']
bb=(R/'builder.bin').read_bytes();dm=(R/'labelled-clear-destination.bin').read_bytes();delta=[j for j,(a,b) in enumerate(zip(bb,dm)) if a!=b]
assert len(bb)==len(dm) and delta==[0x392674-0x3924B0+2] and dm[delta[0]]==0xCB and bb[delta[0]]==0xC8 and sha(dm)!=sha(bb)
mi=next(i for i in cs.disasm(dm,0x3924B0) if i.address==0x392674);assert mi.op_str=='rcx, rbx' and ii[0x392674].op_str=='rcx, rax'
pcs=[0x39266F,0x392672,0x392674,0x392677,0x39267E];assert [i.address for i in ii.values() if pcs[0]<=i.address<=pcs[-1]]==pcs
assert [ii[a].mnemonic for a in pcs]==['movsxd','xor','mov','mov','call']
assert ii[pcs[0]].op_str=='r8, ebx' and ii[pcs[1]].op_str=='edx, edx' and ii[pcs[-1]].operands[0].imm==0x861EC0
store=ii[pcs[3]];o=store.operands[0];assert roles.op_kind(store,o,0)=='w' and o.size==8 and store.address+store.size+o.mem.disp==0x2AEE0A0
b=r['memset_import'];assert b['name']=='memset'
for ak,bk in [('descriptor_va','descriptor_hex'),('lookup_va','lookup_hex'),('name_va','name_hex'),('dll_va','dll_hex')]:
    value=bytes.fromhex(b[bk]);assert rd.img_rd(image,secs,int(b[ak],16),len(value))==value
th=ii[0x861EC0];assert th.address+th.size+th.operands[0].mem.disp==int(b['iat'],16)
assert r['caller']['pcs']==[hex(a) for a in pcs] and r['caller']['base_store']=='0x2aee0a0' and r['caller']['store_before_call'] and not r['caller']['conditional_guard']
assert len(r['consumers'])==3
for c in r['consumers']:assert sha((R/c['retained']).read_bytes())==c['retained_sha256']
if (W/'manifest.json').exists():
    members=json.loads((W/'manifest.json').read_text())['members'];assert members
    for x in members:
        data=(W/x['path']).read_bytes();assert len(data)==x['bytes'] and sha(data)==x['sha256']
print('PASS_STATIC_ALLOC_RETURN exact caller/wrapper/import/role policy; null-v-nonnull conditional paths and branch/destination controls; no native allocator return/OOM/CRT/health proof')
