"""Original deferred focus commit with explicit controlled teardown interventions."""
import hashlib,json,struct,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[4]/'Tools/work/ASTRA/python-libs'))
import capstone,unicorn
from unicorn.x86_const import *
HERE=Path(__file__).resolve().parent
raw=Path(r'D:\SteamLibrary\steamapps\common\FINAL FANTASY XII THE ZODIAC AGE\x64\FFXII_TZA.exe').read_bytes()
assert hashlib.sha256(raw).hexdigest()=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
pe=struct.unpack_from('<I',raw,60)[0];base=struct.unpack_from('<Q',raw,pe+48)[0]
table=pe+24+struct.unpack_from('<H',raw,pe+20)[0]
found=[]
for n in range(struct.unpack_from('<H',raw,pe+6)[0]):
    _,rva,length,disk=struct.unpack_from('<4I',raw,table+40*n+8)
    if rva<=0x358BC0-base<rva+length:
        offset=disk+0x358BC0-base-rva;found.append(raw[offset:offset+156])
assert len(found)==1
code=found[0];assert code[-1:]==b'\xC3'
CURRENT,PENDING,KIND=0x22C7FE0,0x22C7FE4,0x22C7FF8
PAGE,STACK,RETURN,ACTOR,TAIL=0x22C7000,0x60000800,0x60001000,0x50000100,0x2681D0
STUBS=(0x3588B0,0x358B40,0x259800,0x25A680,0x25A690)


def run(name,current=0x1111,pending=0x2222,kind=1,replacement=None,prepare_kind=None,new_actor=False,mutant=False):
    u=unicorn.Uc(unicorn.UC_ARCH_X86,unicorn.UC_MODE_64)
    for page in sorted({a&~4095 for a in STUBS+(0x358BC0,TAIL)}):u.mem_map(page,4096)
    blob=code
    if mutant:
        assert blob[0x64:0x6A]==bytes.fromhex('8b0dbaf3f601')
        blob=blob[:0x64]+b'\x90'*6+blob[0x6A:]
    u.mem_write(0x358BC0,blob);u.mem_map(PAGE,4096);u.mem_map(0x60000000,0x2000)
    before=bytearray(b'\xA5'*4096)
    struct.pack_into('<I',before,CURRENT-PAGE,current);struct.pack_into('<I',before,PENDING-PAGE,pending)
    before[KIND-PAGE]=kind;u.mem_write(PAGE,bytes(before))
    calls=[];writes=[];interventions=[];visited=[];tail=[]
    changed=current!=pending
    ordinary=current!=0 and (kind if prepare_kind is None else prepare_kind)!=2
    teardown=0x25A680 if ordinary else 0x25A690
    expected_pending=replacement if kind and changed and replacement is not None else pending
    def step(uc,address,size,data):
        visited.append(address)
        if address==RETURN:uc.emu_stop();return
        if address==TAIL:
            tail.append(uc.reg_read(UC_X86_REG_RCX));uc.emu_stop();return
        if address not in STUBS:return
        rcx=uc.reg_read(UC_X86_REG_RCX);rdx=uc.reg_read(UC_X86_REG_RDX)
        args=[];result=0
        if address==0x3588B0:
            args=[rcx]
            is_old=changed and not any(c['va']==address for c in calls)
            result=ACTOR if is_old or new_actor else 0
        elif address==0x259800:
            args=[rcx]
            if prepare_kind is not None:
                uc.mem_write(KIND,bytes([prepare_kind]));interventions.append(dict(at=address,address=KIND,value=prepare_kind,bytes=1))
        elif address in (0x25A680,0x25A690):
            args=[rcx,rdx]
            if replacement is not None:
                uc.mem_write(PENDING,struct.pack('<I',replacement));uc.mem_write(KIND,b'\x01')
                interventions.extend([dict(at=address,address=PENDING,value=replacement,bytes=4),
                                      dict(at=address,address=KIND,value=1,bytes=1)])
        calls.append(dict(va=address,args=args,result=result,method='controlled dependency'))
        rsp=uc.reg_read(UC_X86_REG_RSP);resume=struct.unpack('<Q',uc.mem_read(rsp,8))[0]
        uc.reg_write(UC_X86_REG_RAX,result)
        uc.reg_write(UC_X86_REG_RCX,0xBADF00D)  # legal volatile clobber; reread must recover pending.
        uc.reg_write(UC_X86_REG_RSP,rsp+8);uc.reg_write(UC_X86_REG_RIP,resume)
    u.hook_add(unicorn.UC_HOOK_CODE,step)
    u.hook_add(unicorn.UC_HOOK_MEM_WRITE,lambda uc,access,address,size,value,data:
        writes.append(dict(address=address,bytes=size,value=value)) if not 0x60000000<=address<0x60002000 else None)
    u.mem_write(STACK,struct.pack('<Q',RETURN));u.reg_write(UC_X86_REG_RSP,STACK)
    u.emu_start(0x358BC0,0,count=200)
    assert u.reg_read(UC_X86_REG_RIP)==(TAIL if kind and new_actor else RETURN)
    assert u.reg_read(UC_X86_REG_RSP)==(STACK if kind and new_actor else STACK+8)
    if tail:assert tail==[ACTOR]
    expected=bytearray(before)
    if kind:
        struct.pack_into('<I',expected,PENDING-PAGE,expected_pending)
        struct.pack_into('<I',expected,CURRENT-PAGE,expected_pending);expected[KIND-PAGE]=0
    expected_calls=[]
    if kind and changed:expected_calls=[(0x3588B0,[current]),(0x358B40,[]),(0x259800,[0]),(teardown,[ACTOR,0])]
    if kind:expected_calls.append((0x3588B0,[expected_pending]))
    expected_writes=[dict(address=CURRENT,bytes=4,value=expected_pending),dict(address=KIND,bytes=1,value=0)] if kind else []
    after=bytes(u.mem_read(PAGE,4096))
    return dict(name=name,matches=after==bytes(expected) and writes==expected_writes and
                [(c['va'],c['args']) for c in calls]==expected_calls,
                before=dict(current=current,pending=pending,kind=kind),
                after=dict(current=struct.unpack_from('<I',after,CURRENT-PAGE)[0],
                           pending=struct.unpack_from('<I',after,PENDING-PAGE)[0],kind=after[KIND-PAGE]),
                calls=calls,original_writes=writes,controlled_interventions=interventions,visited=visited,
                stop='before new-actor tail callee' if tail else 'returned',tail_actor=tail)


cases=[run('no-request',kind=0),run('same-handle',pending=0x1111),run('ordinary'),run('alternate',kind=2),
       run('zero-current',current=0),run('replacement',replacement=0x3333),run('replacement-zero',replacement=0),
       run('kind-updated-before-branch',prepare_kind=2),run('kind-cleared-after-entry',prepare_kind=0),
       run('same-handle-new-actor',pending=0x1111,new_actor=True)]
assert all(c['matches'] for c in cases)
fault=run('omitted-pending-reread',replacement=0x3333,mutant=True);assert not fault['matches']
result=dict(status='PASS',method='original full commit body; controlled dependencies/interventions; final actor tail callee omitted',
    exe_sha256=hashlib.sha256(raw).hexdigest(),source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    cases=cases,omitted_reread_mutant=fault)
(HERE/'function.bin').write_bytes(code);(HERE/'result.json').write_text(json.dumps(result,indent=2)+'\n')
cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64)
(HERE/'disassembly.txt').write_text('\n'.join(f'{i.address:08X} {i.bytes.hex():24} {i.mnemonic} {i.op_str}'.rstrip()
    for i in cs.disasm(code,0x358BC0))+'\n')
print('PASS: ten commit boundaries; omitted pending reread detected')
