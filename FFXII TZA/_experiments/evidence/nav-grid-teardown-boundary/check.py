"""Readonly source/guard/type-range controls; no original/native instructions."""
import hashlib,importlib.util,json,struct
from pathlib import Path
import capstone
W=Path(__file__).resolve().parent;R=W/'retained';sha=lambda b:hashlib.sha256(b).hexdigest()
r=json.loads((W/'result.json').read_text());raw=json.loads((W/'raw-source.json').read_text());assert r['reference']==raw['reference']
assert r['driver_sha256']==raw['driver_sha256']==sha((W/'capture.py').read_bytes())==sha((R/'driver-before-run.py').read_bytes())
for x in raw['tools']['provider_files']:assert sha(Path(x['path']).read_bytes())==x['sha256'] and Path(x['path']).stat().st_size==x['bytes']
for n,k in [('shipping-reader.py','reader_sha256'),('reg_tracking.py','policy_sha256')]:assert sha((R/n).read_bytes())==r['reference'][k]
sp=importlib.util.spec_from_file_location('rd',R/'shipping-reader.py');rd=importlib.util.module_from_spec(sp);sp.loader.exec_module(rd);d,ss=rd.load_image();assert sha(d)==r['reference']['exe_sha256']=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
sp=importlib.util.spec_from_file_location('roles',R/'reg_tracking.py');roles=importlib.util.module_from_spec(sp);sp.loader.exec_module(roles)
cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True;ii={};assert len(raw['bodies'])==4 and sum(x['bytes'] for x in raw['bodies'])==69
for b in raw['bodies']:
    a=int(b['entry'],16);code=(R/(b['name']+'.bin')).read_bytes();assert code==rd.img_rd(d,ss,a,b['bytes']) and sha(code)==b['sha256']
    seq=list(cs.disasm(code,a));assert sum(i.size for i in seq)==len(code);records=[]
    for i in seq:
        records.append(dict(pc=hex(i.address),bytes=i.bytes.hex(),op=i.mnemonic,args=i.op_str,memory=[dict(operand_index=j,size=o.size,base=i.reg_name(o.mem.base),index=i.reg_name(o.mem.index),disp=o.mem.disp,kind=roles.op_kind(i,o,j)) for j,o in enumerate(i.operands) if o.type==capstone.CS_OP_MEM],written=sorted(roles.written(i))))
    assert records==b['instructions'];ii.update({i.address:i for i in seq})
x=raw['extent'];rec=rd.img_rd(d,ss,rd.IMG_LO+int(x['directory_rva'],16)+x['record_offset'],12);assert rec.hex()==x['record_hex'];a,e,u=struct.unpack('<III',rec);assert a+rd.IMG_LO==0x392710 and e+rd.IMG_LO==0x39273D
load=ii[0x392714];o=load.operands[1];assert load.reg_name(load.operands[0].reg)=='rcx' and o.type==capstone.CS_OP_MEM and o.size==8 and load.address+load.size+o.mem.disp==0x2AEE0A0 and roles.op_kind(load,o,1)=='r'
assert ii[0x39271B].op_str=='rcx, rcx' and ii[0x39271E].mnemonic=='je' and ii[0x39271E].operands[0].imm==0x392725 and ii[0x392720].operands[0].imm==0x3844F0
assert ii[0x3844F0].operands[0].imm==0x3697F0 and ii[0x3697F0].op_str=='rcx, rcx' and ii[0x3697F3].operands[0].imm==0x3697FC and ii[0x3697F5].op_str=='edx, edx' and ii[0x3697F7].operands[0].imm==0x369860
lea=ii[0x392727];o=lea.operands[1];assert lea.mnemonic=='lea' and lea.reg_name(lea.operands[0].reg)=='rcx' and lea.address+lea.size+o.mem.disp==0x2AEE060 and roles.op_kind(lea,o,1)=='addr'
assert ii[0x392725].op_str=='edx, edx' and ii[0x39272E].op_str=='r8d, 0x460' and ii[0x392738].mnemonic=='jmp' and ii[0x392738].operands[0].imm==0x861EC0
original=(R/'teardown.bin').read_bytes();m=(R/'labelled-release-je-to-jne.bin').read_bytes();s=(R/'labelled-parameter-only-clear.bin').read_bytes();assert len(original)==len(m)==len(s)==45
assert [j for j,(a,b) in enumerate(zip(original,m)) if a!=b]==[0x39271E-0x392710] and m[0x39271E-0x392710]==0x75 and sha(m)!=sha(original)
mi=next(i for i in cs.disasm(m,0x392710) if i.address==0x39271E);assert mi.mnemonic=='jne' and mi.operands[0].imm==0x392725
p=0x39272E-0x392710;assert s[:p+2]==original[:p+2] and s[p+2:p+6]==struct.pack('<I',0x60) and s[p+6:]==original[p+6:] and sha(s)!=sha(original)
si=next(i for i in cs.disasm(s,0x392710) if i.address==0x39272E);assert si.op_str=='r8d, 0x60'
b=r['source_bindings'];assert b['heap_cell']=='0x2aee0a0' and b['clear_destination']=='0x2aee060' and b['clear_bytes']==0x460 and b['clear_end_exclusive']=='0x2aee4c0' and b['parameter_span_bytes']==0x60 and b['following_span_start']=='0x2aee0c0' and b['following_span_bytes']==0x400 and not b['nav_root_02AEDFB0_in_clear_range']
assert 0x2AEE060+0x460==0x2AEE4C0 and not 0x2AEE060<=0x2AEDFB0<0x2AEE4C0
assert r['controls']==dict(branch=dict(original_null_skips_release=True,private_null_reaches_release=True,same_target=True),clear_span=dict(original_covers_table_head=True,private_parameter_only_excludes_table_head=True),immutable_source_refuses_both=True)
bind=raw['memset_import'];parent=json.loads((R/'allocation-parent-result.json').read_text());assert bind==parent['memset_import'] and bind['name']=='memset'
for ak,bk in [('descriptor_va','descriptor_hex'),('lookup_va','lookup_hex'),('name_va','name_hex'),('dll_va','dll_hex')]:
    value=bytes.fromhex(bind[bk]);assert rd.img_rd(d,ss,int(bind[ak],16),len(value))==value
for c in r['consumers']:assert sha((R/c['retained']).read_bytes())==c['retained_sha256']
assert b'NavGridParams\t0x60' in (R/'nav-types-preimage.tsv').read_bytes() and b'ARRAY 0x02AEE0C0' in (R/'nav-types-preimage.tsv').read_bytes()
for x in raw['tools']['provider_files']:assert sha(Path(x['path']).read_bytes())==x['sha256']
if (W/'manifest.json').exists():
    members=json.loads((W/'manifest.json').read_text())['members'];assert members
    for x in members:
        data=(W/x['path']).read_bytes();assert len(data)==x['bytes'] and sha(data)==x['sha256']
print('PASS_TEARDOWN_SOURCE exact69B/PEextent/conditionalrelease-route/LEAaddr/fillrange/control/qualifiedimport; nativeeffects/lifetimeordering/128capacity not established')
