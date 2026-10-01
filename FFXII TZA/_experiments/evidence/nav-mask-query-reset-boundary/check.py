"""Readonly source/flow/global-pointer controls; no FF12/native execution."""
import hashlib,importlib.util,json,struct
from pathlib import Path
import capstone
W=Path(__file__).resolve().parent;R=W/'retained';sha=lambda b:hashlib.sha256(b).hexdigest()
tool=json.loads((W/'validation-tool-identity.json').read_text());assert tool['capstone_version']==capstone.__version__
for x in tool['files']:assert sha(Path(x['path']).read_bytes())==x['sha256'] and Path(x['path']).stat().st_size==x['bytes']
r=json.loads((W/'result.json').read_text());raw=json.loads((W/'raw-source.json').read_text());assert r['reference']==raw['reference']
assert r['driver_sha256']==raw['driver_sha256']==sha((W/'capture.py').read_bytes())==sha((R/'driver-before-run.py').read_bytes())
for n,k in [('shipping-reader.py','reader_sha256'),('reg_tracking.py','policy_sha256'),('allocation-parent-result.json','parent_result_sha256'),('allocation-parent-manifest.json','parent_manifest_sha256')]:assert sha((R/n).read_bytes())==r['reference'][k]
sp=importlib.util.spec_from_file_location('rd',R/'shipping-reader.py');rd=importlib.util.module_from_spec(sp);sp.loader.exec_module(rd);d,ss=rd.load_image();assert sha(d)==r['reference']['exe_sha256']=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
sp=importlib.util.spec_from_file_location('roles',R/'reg_tracking.py');roles=importlib.util.module_from_spec(sp);sp.loader.exec_module(roles)
cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True;ii={};assert len(raw['bodies'])==2 and sum(x['bytes'] for x in raw['bodies'])==298
for b in raw['bodies']:
    a=int(b['entry'],16);code=(R/(b['name']+'.bin')).read_bytes();assert code==rd.img_rd(d,ss,a,b['bytes']) and sha(code)==b['sha256']
    seq=list(cs.disasm(code,a));assert sum(i.size for i in seq)==len(code);records=[]
    for i in seq:
        records.append(dict(pc=hex(i.address),bytes=i.bytes.hex(),op=i.mnemonic,args=i.op_str,memory=[dict(operand_index=j,size=o.size,base=i.reg_name(o.mem.base),index=i.reg_name(o.mem.index),disp=o.mem.disp,kind=roles.op_kind(i,o,j)) for j,o in enumerate(i.operands) if o.type==capstone.CS_OP_MEM],written=sorted(roles.written(i))))
    assert records==b['instructions'];ii.update({i.address:i for i in seq})
x=raw['extent'];rec=rd.img_rd(d,ss,rd.IMG_LO+int(x['directory_rva'],16)+x['record_offset'],12);assert rec.hex()==x['record_hex'];a,e,u=struct.unpack('<III',rec);assert a+rd.IMG_LO==0x3912E0 and e+rd.IMG_LO==0x391404
for pc,target,size,reg in [(0x3912F9,0x2AEE0B8,4,'r8'),(0x391302,0x2AEE0B0,8,'rcx'),(0x3913B1,0x2AEE0B0,8,'rdx'),(0x3913E8,0x2AEE0B0,8,'rax')]:
    i=ii[pc];o=i.operands[1];assert o.type==capstone.CS_OP_MEM and o.mem.base==capstone.x86_const.X86_REG_RIP and o.size==size and i.address+i.size+o.mem.disp==target and i.reg_name(i.operands[0].reg)==reg and roles.op_kind(i,o,1)=='r'
assert ii[0x3912F9].mnemonic=='movsxd' and ii[0x391309].op_str=='edx, edx' and ii[0x39130E].mnemonic=='call' and ii[0x39130E].operands[0].imm==0x861EC0
assert not any(i.mnemonic.startswith('j') or i.mnemonic=='call' for a,i in ii.items() if 0x3912E0<=a<0x39130E)
assert [hex(a) for a,i in ii.items() if 0x3912E0<=a<0x391404 and i.mnemonic=='call']==['0x39130e']
o=ii[0x3913C4];assert o.mnemonic=='or' and o.op_str=='byte ptr [rdx + rax - 1], cl' and roles.op_kind(o,o.operands[0],0)=='rw'
# Actual source guards reject a wrong register and an omitted call. Only bytes/
# bindings are tested, not the native clearing effect.
original=(R/'query.bin').read_bytes();m=(R/'labelled-wrong-clear-register.bin').read_bytes();z=(R/'labelled-omitted-clear-call.bin').read_bytes();assert len(m)==len(z)==len(original)
assert [j for j,(a,b) in enumerate(zip(original,m)) if a!=b]==[0x391302-0x3912E0+2] and m[0x391302-0x3912E0+2]==0x15
mi=next(i for i in cs.disasm(m,0x3912E0) if i.address==0x391302);assert mi.op_str.startswith('rdx, qword ptr') and not mi.op_str.startswith('rcx, qword ptr') and sha(m)!=sha(original)
p=0x39130E-0x3912E0;assert z[:p]==original[:p] and z[p:p+5]==b'\x90'*5 and z[p+5:]==original[p+5:] and sha(z)!=sha(original)
zi=next(i for i in cs.disasm(z,0x3912E0) if i.address==0x39130E);assert zi.mnemonic=='nop'
b=raw['memset_import'];parent=json.loads((R/'allocation-parent-result.json').read_text());assert b==parent['memset_import'] and b['name']=='memset'
for ak,bk in [('descriptor_va','descriptor_hex'),('lookup_va','lookup_hex'),('name_va','name_hex'),('dll_va','dll_hex')]:
    value=bytes.fromhex(b[bk]);assert rd.img_rd(d,ss,int(b[ak],16),len(value))==value
th=ii[0x861EC0];assert th.address+th.size+th.operands[0].mem.disp==int(b['iat'],16)
assert r['bindings']==dict(clear_pointer_cell='0x2aee0b0',or_pointer_cell='0x2aee0b0',returned_pointer_cell='0x2aee0b0',clear_length_cell='0x2aee0b8',call='0x39130e',or_write='0x3913c4')
assert r['controls']==dict(original_entry_binding=True,private_wrong_register_rejected=True,private_omitted_call_rejected=True,original_binding_refuses_both=True)
for c in r['consumers']:assert sha((R/c['retained']).read_bytes())==c['retained_sha256']
for x in tool['files']:assert sha(Path(x['path']).read_bytes())==x['sha256']
if (W/'manifest.json').exists():
    members=json.loads((W/'manifest.json').read_text())['members'];assert members
    for x in members:
        data=(W/x['path']).read_bytes();assert len(data)==x['bytes'] and sha(data)==x['sha256']
print('PASS_MASK_RESET_SOURCE exact298B/PEextent/globalclear-OR-return provenance/defaultpolicy/sourceguards/qualifiedimport; actualnativeclear/initializedpointer/threadatomicity unproved')
