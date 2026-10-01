"""A allocator retry local predicates; source controls, no FF12 execution."""
import hashlib,importlib.util,json,struct,sys
from pathlib import Path
import capstone
W=Path(__file__).resolve().parent;R=W/'retained';sha=lambda b:hashlib.sha256(b).hexdigest()
sys.path.insert(0,'Database/Tools/analysis-kit/gfz-scripts');import team,reg_tracking as roles
ok,why=team.board_status(team.BOARD);assert ok,why;t=next(t for t in json.loads(team.BOARD.read_text())['tasks'] if t['id']=='ASTRA-ALLOCATOR-RETRY-RETURN-DOMAIN');assert t['status']=='ACTIVE' and t['agent']=='ASTRA'
R.mkdir(exist_ok=False);(R/'driver-before-run.py').write_bytes(Path(__file__).read_bytes())
p=Path('Database/FFXII TZA/_experiments/evidence/license-check-exec/check.py');pol=Path(roles.__file__);(R/'shipping-reader.py').write_bytes(p.read_bytes());(R/'reg_tracking.py').write_bytes(pol.read_bytes())
sp=importlib.util.spec_from_file_location('rd',p);rd=importlib.util.module_from_spec(sp);sp.loader.exec_module(rd);d,ss=rd.load_image();assert sha(d)=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True;ii={};bodies=[]
for a,n,name in [(0x36A190,10,'entry-thunk'),(0x36A1A0,141,'allocation-wrapper'),(0x36BFE0,261,'retry')]:
    b=rd.img_rd(d,ss,a,n);seq=list(cs.disasm(b,a));assert sum(i.size for i in seq)==n and seq[-1].mnemonic==('jmp' if n==10 else 'ret')
    (R/(name+'.bin')).write_bytes(b);records=[]
    for i in seq:
        records.append(dict(pc=hex(i.address),bytes=i.bytes.hex(),op=i.mnemonic,args=i.op_str,memory=[dict(operand_index=j,size=o.size,base=i.reg_name(o.mem.base),index=i.reg_name(o.mem.index),disp=o.mem.disp,kind=roles.op_kind(i,o,j)) for j,o in enumerate(i.operands) if o.type==capstone.CS_OP_MEM],written=sorted(roles.written(i))))
    bodies.append(dict(entry=hex(a),bytes=n,name=name,sha256=sha(b),instructions=records));ii.update({i.address:i for i in seq})
# PE unwind records corroborate the two nonleaf ranges, not callback semantics.
pe=struct.unpack_from('<I',d,0x3C)[0];rv,size=struct.unpack_from('<II',d,pe+24+112+3*8);pdata=rd.img_rd(d,ss,rd.IMG_LO+rv,size);extent=[]
for j in range(0,len(pdata)-11,12):
    start,end,u=struct.unpack_from('<III',pdata,j)
    if rd.IMG_LO+start in (0x36A1A0,0x36BFE0):
        record=pdata[j:j+12];extent.append(dict(entry=hex(rd.IMG_LO+start),end=hex(rd.IMG_LO+end),unwind=hex(rd.IMG_LO+u),directory_rva=hex(rv),record_offset=j,record_hex=record.hex()))
assert len(extent)==2 and {(x['entry'],x['end']) for x in extent}=={('0x36a1a0','0x36a22d'),('0x36bfe0','0x36c0e5')}
raw=dict(reference=dict(exe_sha256=sha(d),base=hex(rd.IMG_LO),reader_sha256=sha(p.read_bytes()),policy_sha256=sha(pol.read_bytes())),driver_sha256=sha(Path(__file__).read_bytes()),tools=dict(python=sys.version,python_sha256=sha(Path(sys.executable).read_bytes()),capstone=capstone.__version__),bodies=bodies,extent=extent)
(W/'raw-source.json').write_text(json.dumps(raw,indent=2)+'\n')
assert ii[0x36A190].op_str=='edx, 1' and ii[0x36A195].operands[0].imm==0x36A1A0
assert ii[0x36A1B4].op_str=='esi, edx' and ii[0x36A1E2].op_str=='dword ptr [rsp + 0x28], esi' and ii[0x36A1EB].op_str=='qword ptr [rsp + 0x20], rbp' and ii[0x36A1F0].operands[0].imm==0x36BFE0
# After push r14/sub20, incoming arguments5/6 are at currentRSP+50/+58.
retry=[i for a,i in ii.items() if 0x36BFE0<=a<0x36C0E5]
stack=[]
for i in retry:
    for j,o in enumerate(i.operands):
        if o.type==capstone.CS_OP_MEM and o.mem.base==capstone.x86_const.X86_REG_RSP:stack.append(dict(pc=hex(i.address),disp=o.mem.disp,size=o.size,kind=roles.op_kind(i,o,j)))
assert not any(x['kind'] in ('r','rw','?') and (x['disp']<0x60 and x['disp']+x['size']>0x50) for x in stack)
assert not any(i.mnemonic=='lea' and any(o.type==capstone.CS_OP_MEM and o.mem.base==capstone.x86_const.X86_REG_RSP for o in i.operands) for i in retry)
# All local branches terminate in-body or retry, calls treated opaque returning.
for i in retry:
    if i.mnemonic.startswith('j'):assert i.operands[0].type==capstone.CS_OP_IMM and i.operands[0].imm in {j.address for j in retry}
assert ii[0x36C0A9].operands[0].imm==0x36BC60 and ii[0x36C0AE].op_str=='edi, edi' and ii[0x36C0B2].op_str=='rax, rax' and ii[0x36C0B7].op_str=='esi, esi' and ii[0x36C0C1].op_str=='rax, rax'
def decision(code,pointer_nonzero,reclaim_nonzero,callback_nonzero):
    seq={i.address:i for i in cs.disasm(code,0x36BFE0)};pc=0x36C0AE;seen=[];zf=None
    for _ in range(12):
        if pc==0x36C013:return dict(outcome='retry backedge',pcs=seen,target=hex(pc))
        if pc==0x36C0CA:return dict(outcome='return epilogue',pcs=seen,target=hex(pc))
        i=seq[pc];seen.append(hex(pc))
        if i.mnemonic=='test':
            v={'edi, edi':reclaim_nonzero,'esi, esi':callback_nonzero,'rax, rax':pointer_nonzero}[i.op_str];zf=not v
        if i.mnemonic in ('je','jne','jmp'):
            take=True if i.mnemonic=='jmp' else zf if i.mnemonic=='je' else not zf;pc=i.operands[0].imm if take else pc+i.size
        else:pc+=i.size
    raise AssertionError('decision did not reach bounded exit')
code=(R/'retry.bin').read_bytes();cases=[]
for ptr in (False,True):
    for reclaim in (False,True):
        for callback in (False,True):
            dec=decision(code,ptr,reclaim,callback);expected='return epilogue' if ptr or (not reclaim and not callback) else 'retry backedge';assert dec['outcome']==expected
            cases.append(dict(final_pointer_nonzero=ptr,local_EDI_nonzero=reclaim,local_ESI_nonzero=callback,decision=dec))
mut=bytearray(code);off=0x36C0B9-0x36BFE0;assert mut[off:off+2]==bytes.fromhex('0f85');mut[off+1]=0x84;(R/'labelled-retry-jne-to-je.bin').write_bytes(mut)
controls=[dict(local_ESI_nonzero=cb,original=decision(code,False,False,cb),private=decision(bytes(mut),False,False,cb)) for cb in (False,True)]
assert all(x['original']['outcome']!=x['private']['outcome'] for x in controls) and sha(mut)!=sha(code)
# Wrapper local null return gate after retry; source forbids header writes on null.
assert ii[0x36A1F5].op_str=='rbx, rax' and ii[0x36A1F8].op_str=='rax, rax' and ii[0x36A1FB].mnemonic=='je' and ii[0x36A1FB].operands[0].imm==0x36A218
canon=Path('Database/FFXII TZA/24-Compiler-And-CRT-Runtime/Memory-And-Allocation/where-the-games-memory-comes-from.md');text=canon.read_bytes();lines=text.splitlines(keepends=True);excerpt=b''.join(lines[:110]);(R/'memory-page-preimage.md').write_bytes(excerpt)
assert b'never checks whether the memory it just' in excerpt and b'instant close to desktop with no' in excerpt
assert sha(p.read_bytes())==raw['reference']['reader_sha256'] and sha(pol.read_bytes())==raw['reference']['policy_sha256']
result=dict(method='A exact source/ABI and conditional final-diamond calculations; no FF12/native/emulator/live execution',reference=raw['reference'],driver_sha256=raw['driver_sha256'],cases=cases,private_branch_control=dict(site=hex(0x36C0B9),from_op='jne',to_op='je',cases=controls,immutable_source_binding_refuses=sha(mut)!=sha(code)),flag_boundary=dict(thunk_sets_EDX=1,wrapper_saves_ESI=True,wrapper_sixth_arg_site=hex(0x36A1E2),wrapper_fifth_arg_zero_site=hex(0x36A1EB),callee_push_sub_delta=hex(0x28),local_incoming5_disp=hex(0x50),local_incoming6_disp=hex(0x58),local_stack_accesses=stack,local_read_5_or_6=False,local_entry_stack_address_escape=False),consumer=dict(path=canon.as_posix(),full_source_sha256=sha(text),excerpt_sha256=sha(excerpt)),interpretation='The thunk flag1 does not by itself prove a success-or-fatal result: the exact retry body locally returns finalRAX zero when EDI=0 and ESI=0; otherwise a zero finalRAX retries. Nonzero finalRAX returns for all local EDI/ESI cases. Local fifth/sixth argument writes are not consumed by this callee body. Opaque callback/reclaim/native allocator results and normal reachability are separate.',limits='Branch predicates are evaluated at the final diamond, not fabricated initialized arena/game observations. EDI/ESI are low32 state at that site, not proven count/boolean native semantics. Incoming stack read absence scoped to this exact body, no callee/callback stack-introspection/ABI lifetime claim. Actual null/OOM/error message/process termination/CRT/native allocator policy not observed. Existing selection initialization/depth/mask invariants reused, not recensus.')
(W/'result.json').write_text(json.dumps(result,indent=2)+'\n');print('CAPTURE_RETRY_SOURCE nullable return iff finalRAXzero and localEDI/ESIzero; otherwise null retries; flag1 local stack-slot unused; original branch-control distinguishes; not actual OOM')
