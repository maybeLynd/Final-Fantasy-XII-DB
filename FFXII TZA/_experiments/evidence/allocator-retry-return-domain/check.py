"""Readonly original-source/extent/predicate controls; no FF12 execution."""
import hashlib,importlib.util,json,struct
from pathlib import Path
import capstone
W=Path(__file__).resolve().parent;R=W/'retained';sha=lambda b:hashlib.sha256(b).hexdigest()
r=json.loads((W/'result.json').read_text());raw=json.loads((W/'raw-source.json').read_text());assert r['reference']==raw['reference']
assert r['driver_sha256']==raw['driver_sha256']==sha((W/'capture.py').read_bytes())==sha((R/'driver-before-run.py').read_bytes())
for n,k in [('shipping-reader.py','reader_sha256'),('reg_tracking.py','policy_sha256')]:assert sha((R/n).read_bytes())==r['reference'][k]
sp=importlib.util.spec_from_file_location('rd',R/'shipping-reader.py');rd=importlib.util.module_from_spec(sp);sp.loader.exec_module(rd);d,ss=rd.load_image();assert sha(d)==r['reference']['exe_sha256']=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
sp=importlib.util.spec_from_file_location('roles',R/'reg_tracking.py');roles=importlib.util.module_from_spec(sp);sp.loader.exec_module(roles)
cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True;ii={};assert len(raw['bodies'])==3 and sum(x['bytes'] for x in raw['bodies'])==412
for b in raw['bodies']:
    a=int(b['entry'],16);code=(R/(b['name']+'.bin')).read_bytes();assert code==rd.img_rd(d,ss,a,b['bytes']) and sha(code)==b['sha256']
    seq=list(cs.disasm(code,a));assert sum(i.size for i in seq)==len(code);records=[]
    for i in seq:
        records.append(dict(pc=hex(i.address),bytes=i.bytes.hex(),op=i.mnemonic,args=i.op_str,memory=[dict(operand_index=j,size=o.size,base=i.reg_name(o.mem.base),index=i.reg_name(o.mem.index),disp=o.mem.disp,kind=roles.op_kind(i,o,j)) for j,o in enumerate(i.operands) if o.type==capstone.CS_OP_MEM],written=sorted(roles.written(i))))
    assert records==b['instructions'];ii.update({i.address:i for i in seq})
assert len(raw['extent'])==2
for x in raw['extent']:
    rec=rd.img_rd(d,ss,rd.IMG_LO+int(x['directory_rva'],16)+x['record_offset'],12);assert rec.hex()==x['record_hex'];b,e,u=struct.unpack('<III',rec);assert (hex(b+rd.IMG_LO),hex(e+rd.IMG_LO),hex(u+rd.IMG_LO))==(x['entry'],x['end'],x['unwind'])
assert ii[0x36A190].op_str=='edx, 1' and ii[0x36A195].operands[0].imm==0x36A1A0
assert ii[0x36A1E2].op_str=='dword ptr [rsp + 0x28], esi' and ii[0x36A1EB].op_str=='qword ptr [rsp + 0x20], rbp' and ii[0x36A1F0].operands[0].imm==0x36BFE0
assert ii[0x36A1CE].op_str=='ebp, ebp' and ii[0x36A1B4].op_str=='esi, edx'
assert ii[0x36A1FB].mnemonic=='je' and ii[0x36A1FB].operands[0].imm==0x36A218
for pc,op,reg,target in [(0x36C0AE,'test','edi, edi',None),(0x36C0B0,'jne',None,0x36C0C1),(0x36C0B2,'test','rax, rax',None),(0x36C0B5,'jne',None,0x36C0CA),(0x36C0B7,'test','esi, esi',None),(0x36C0B9,'jne',None,0x36C013),(0x36C0BF,'jmp',None,0x36C0CA),(0x36C0C1,'test','rax, rax',None),(0x36C0C4,'je',None,0x36C013)]:
    i=ii[pc];assert i.mnemonic==op
    if reg:assert i.op_str==reg
    if target:assert i.operands[0].imm==target
assert len(r['cases'])==8 and len({(c['final_pointer_nonzero'],c['local_EDI_nonzero'],c['local_ESI_nonzero']) for c in r['cases']})==8
for c in r['cases']:
    ptr,reclaim,cb=c['final_pointer_nonzero'],c['local_EDI_nonzero'],c['local_ESI_nonzero'];ret=ptr or (not reclaim and not cb)
    assert c['decision']['outcome']==('return epilogue' if ret else 'retry backedge') and c['decision']['target']==('0x36c0ca' if ret else '0x36c013') and c['decision']['pcs'][0]=='0x36c0ae'
original=(R/'retry.bin').read_bytes();mut=(R/'labelled-retry-jne-to-je.bin').read_bytes();assert len(original)==len(mut);delta=[j for j,(a,b) in enumerate(zip(original,mut)) if a!=b];assert delta==[0x36C0B9-0x36BFE0+1] and original[delta[0]]==0x85 and mut[delta[0]]==0x84 and sha(original)!=sha(mut)
mi=next(i for i in cs.disasm(mut,0x36BFE0) if i.address==0x36C0B9);assert mi.mnemonic=='je' and mi.operands[0].imm==0x36C013
controls=r['private_branch_control']['cases'];assert len(controls)==2
for c in controls:
    cb=c['local_ESI_nonzero'];assert c['original']['outcome']==('retry backedge' if cb else 'return epilogue') and c['private']['outcome']==('return epilogue' if cb else 'retry backedge')
f=r['flag_boundary'];assert f['callee_push_sub_delta']=='0x28' and f['local_incoming5_disp']=='0x50' and f['local_incoming6_disp']=='0x58' and not f['local_read_5_or_6'] and not f['local_entry_stack_address_escape']
stack=[]
for a,i in ii.items():
    if not 0x36BFE0<=a<0x36C0E5:continue
    for j,o in enumerate(i.operands):
        if o.type==capstone.CS_OP_MEM and o.mem.base==capstone.x86_const.X86_REG_RSP:stack.append(dict(pc=hex(a),disp=o.mem.disp,size=o.size,kind=roles.op_kind(i,o,j)))
assert stack==f['local_stack_accesses'] and stack and not any(x['kind'] in ('r','rw','?') and x['disp']<0x60 and x['disp']+x['size']>0x50 for x in stack)
assert sha((R/'memory-page-preimage.md').read_bytes())==r['consumer']['excerpt_sha256']
if (W/'manifest.json').exists():
    members=json.loads((W/'manifest.json').read_text())['members'];assert members
    for x in members:
        b=(W/x['path']).read_bytes();assert len(b)==x['bytes'] and sha(b)==x['sha256']
print('PASS_RETRY_SOURCE exact412B/2extentrecords/branchpredicate/sourceflip/ABIlocalargreadboundary; no actualnull/OOM/loadedcallback/reclaim/native failurepolicy proof')
