"""Readonly source/order/binding controls; no FF12 instructions executed."""
import hashlib, importlib.util, json, struct
from pathlib import Path
import capstone
W=Path(__file__).resolve().parent; R=W/'retained'
sha=lambda b:hashlib.sha256(b).hexdigest()
r=json.loads((W/'result.json').read_text()); raw=json.loads((W/'raw-source.json').read_text())
assert r['reference']==raw['reference']
assert r['driver_sha256']==raw['driver_sha256']==sha((W/'capture.py').read_bytes())==sha((R/'driver-before-run.py').read_bytes())
for x in raw['tools']['provider_files']:
    assert sha(Path(x['path']).read_bytes())==x['sha256'] and Path(x['path']).stat().st_size==x['bytes']
for name,key in [('shipping-reader.py','reader_sha256'),('reg_tracking.py','policy_sha256')]:
    assert sha((R/name).read_bytes())==r['reference'][key]
sp=importlib.util.spec_from_file_location('rd',R/'shipping-reader.py'); rd=importlib.util.module_from_spec(sp); sp.loader.exec_module(rd)
d,ss=rd.load_image(); assert sha(d)==r['reference']['exe_sha256']=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
sp=importlib.util.spec_from_file_location('roles',R/'reg_tracking.py'); roles=importlib.util.module_from_spec(sp); sp.loader.exec_module(roles)
cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64); cs.detail=True; ii={}
assert len(raw['bodies'])==2 and sum(b['bytes'] for b in raw['bodies'])==74
for b in raw['bodies']:
    a=int(b['entry'],16); code=(R/(b['name']+'.bin')).read_bytes()
    assert code==rd.img_rd(d,ss,a,b['bytes']) and sha(code)==b['sha256']
    seq=list(cs.disasm(code,a)); assert sum(i.size for i in seq)==len(code)
    records=[]
    for i in seq:
        records.append(dict(pc=hex(i.address),bytes=i.bytes.hex(),op=i.mnemonic,args=i.op_str,memory=[dict(operand_index=j,size=o.size,base=i.reg_name(o.mem.base),index=i.reg_name(o.mem.index),disp=o.mem.disp,kind=roles.op_kind(i,o,j)) for j,o in enumerate(i.operands) if o.type==capstone.CS_OP_MEM],written=sorted(roles.written(i))))
    assert records==b['instructions']; ii.update({i.address:i for i in seq})
x=raw['extent']; rec=rd.img_rd(d,ss,rd.IMG_LO+int(x['directory_rva'],16)+x['record_offset'],12)
assert rec.hex()==x['record_hex']; a,e,u=struct.unpack('<III',rec)
assert a+rd.IMG_LO==0x2341C0 and e+rd.IMG_LO==0x2341FE
parent=json.loads((R/'teardown-parent-raw.json').read_text()); manifest=json.loads((R/'teardown-parent-manifest.json').read_text())
assert sha((R/'teardown-parent-raw.json').read_bytes())==r['reference']['parent_raw_sha256']
assert sha((R/'teardown-parent-manifest.json').read_bytes())==r['reference']['parent_manifest_sha256']
assert parent['reference']['exe_sha256']==r['reference']['exe_sha256']
assert next(b for b in manifest['members'] if b['path']=='raw-source.json')['sha256']==r['reference']['parent_raw_sha256']
tb=next(b for b in parent['bodies'] if b['name']=='teardown')
assert tb['entry']=='0x392710' and tb['bytes']==45 and sha(rd.img_rd(d,ss,0x392710,45))==tb['sha256']
assert next(b for b in manifest['members'] if b['path']=='retained/teardown.bin')['sha256']==tb['sha256']
caller=[i for a,i in ii.items() if 0x2341C0<=a<0x2341FE]
assert not any(i.mnemonic.startswith('j') for i in caller[:-1])
assert caller[-1].mnemonic=='jmp' and caller[-1].operands[0].imm==0x2FA470
calls=[dict(pc=hex(i.address),target=hex(i.operands[0].imm)) for i in caller if i.mnemonic=='call']
assert calls==r['calls'] and len(calls)==8
assert [(x['pc'],x['target']) for x in calls[:4]]==[('0x2341c4','0x30fe60'),('0x2341c9','0x383a20'),('0x2341d0','0x306570'),('0x2341d5','0x392710')]
store=ii[0x383A20]; o=store.operands[0]
assert store.mnemonic=='mov' and o.type==capstone.CS_OP_MEM and o.size==8
assert store.address+store.size+o.mem.disp==0x2AEDFB0 and store.operands[1].imm==0 and roles.op_kind(store,o,0)=='w'
assert ii[0x383A2B].mnemonic=='ret'
def ordered(code):
    seq=list(cs.disasm(code,0x2341C0))
    rc=[i.address for i in seq if i.mnemonic=='call' and i.operands[0].imm==0x383A20]
    gc=[i.address for i in seq if i.mnemonic=='call' and i.operands[0].imm==0x392710]
    return len(rc)==len(gc)==1 and rc[0]<gc[0]
original=(R/'area-caller.bin').read_bytes(); m=(R/'labelled-swapped-call-targets.bin').read_bytes()
expected=bytearray(original)
for pc,target in [(0x2341C9,0x392710),(0x2341D5,0x383A20)]:
    j=pc-0x2341C0; assert expected[j]==0xE8; expected[j+1:j+5]=struct.pack('<i',target-(pc+5))
assert m==expected and len(m)==62 and ordered(original) and not ordered(m) and sha(original)!=sha(m)
assert r['normal_order']==dict(root_clear_call='0x2341c9',grid_teardown_call='0x2341d5',intervening_call='0x2341d0',intervening_target='0x306570',root_store_cell='0x2aedfb0',root_store_bytes=8,root_store_value=0,tail='0x2fa470')
assert r['control']==dict(private_root_call='0x2341d5',private_grid_call='0x2341c9',private_order_reversed=True,immutable_source_binding_refuses=True)
assert sha((R/'root-type-preimage.tsv').read_bytes())==r['consumer']['retained_sha256']
assert b'002341C0' in (R/'root-type-preimage.tsv').read_bytes() and b'00392710' in (R/'root-type-preimage.tsv').read_bytes()
for x in raw['tools']['provider_files']: assert sha(Path(x['path']).read_bytes())==x['sha256']
if (W/'manifest.json').exists():
    members=json.loads((W/'manifest.json').read_text())['members']; assert members
    for x in members:
        b=(W/x['path']).read_bytes(); assert len(b)==x['bytes'] and sha(b)==x['sha256']
print('PASS_ROOT_CALL_ORDER exact74B/PE/parent45B/shared-store-role/source-order/swapped-call-target-control; opaque306570 prevents root-zero-stability inference')
