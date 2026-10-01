"""Original collection/removal state changes with controlled grant and presentation."""
import hashlib
import json
import struct
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / 'Tools/work/ASTRA/python-libs'))
import capstone
import unicorn
from unicorn.x86_const import *

HERE = Path(__file__).resolve().parent
raw = Path(r'D:\SteamLibrary\steamapps\common\FINAL FANTASY XII THE ZODIAC AGE\x64\FFXII_TZA.exe').read_bytes()
assert hashlib.sha256(raw).hexdigest() == '73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
pe = struct.unpack_from('<I', raw, 60)[0]
base = struct.unpack_from('<Q', raw, pe + 48)[0]
table = pe + 24 + struct.unpack_from('<H', raw, pe + 20)[0]

def extract(va, size):
    for n in range(struct.unpack_from('<H', raw, pe + 6)[0]):
        _, rva, length, disk = struct.unpack_from('<4I', raw, table + 40*n + 8)
        if rva <= va-base < rva+length:
            return raw[disk+va-base-rva:disk+va-base-rva+size]
    raise AssertionError(hex(va))

BODIES={va:extract(va,size) for va,size in [(0x319920,215),(0x3197B0,113),(0x2FB2A0,33)]}
NODE,PREV,NEXT=0x50000100,0x50000200,0x50000300
HEAD,TAIL,COUNTER,PRESENCE=0x2EC1360,0x2EC1368,0x22C3174,0x22BE7F0
STACK,RETURN,INVENTORY,PRESENT,CLEAR=0x60000808,0x60002000,0x300B80,0x28F000,0x2FB2A0
COLLECTOR=0xFEDC1234

def run(name,position='single',entries=None,remove=False,counter=7,repeat=1,mutant=False):
    if entries is None:entries=[(0x1001,3),(0xFFFF,99),(0,0),(0x2002,0x80000001),(0xFFFF,0),(0xFFFF,0),(0x1007,7)]
    assert len(entries)==7
    u=unicorn.Uc(unicorn.UC_ARCH_X86,unicorn.UC_MODE_64)
    pages={v&~4095 for v in list(BODIES)+[NODE,HEAD,COUNTER,PRESENCE,PRESENCE+320,INVENTORY,PRESENT]}
    for p in sorted(pages):u.mem_map(p,4096)
    u.mem_map(0x60000000,0x3000)
    for va,blob in BODIES.items():
        if mutant and va==0x319920:
            at=0x319943-va;assert blob[at:at+5]==b'\xBE\x07\x00\x00\x00'
            blob=blob[:at+1]+b'\x06'+blob[at+2:]
        u.mem_write(va,blob)
    for p in (NODE&~4095,HEAD&~4095,COUNTER&~4095,PRESENCE&~4095,(PRESENCE+320)&~4095):u.mem_write(p,b'\xA5'*4096)
    prev=PREV if position in ('tail','middle') else 0
    nxt=NEXT if position in ('head','middle') else 0
    u.mem_write(NODE,struct.pack('<I',9));u.mem_write(NODE+4,struct.pack('<II',3,0x12345678))
    u.mem_write(NODE+16,struct.pack('<QQ',prev,nxt));u.mem_write(NODE+0x58,struct.pack('<I',0x89ABCDEF))
    for i,(item,qty) in enumerate(entries):
        u.mem_write(NODE+0x20+i*8,struct.pack('<H',item));u.mem_write(NODE+0x24+i*8,struct.pack('<I',qty))
    if prev:u.mem_write(prev+0x18,struct.pack('<Q',NODE))
    if nxt:u.mem_write(nxt+0x10,struct.pack('<Q',NODE))
    u.mem_write(HEAD,struct.pack('<QQ',prev or NODE,nxt or NODE));u.mem_write(COUNTER,struct.pack('<I',counter))
    u.mem_write(PRESENCE+9*32,b'\x01')
    events=[];visits=[];callback_states=[]
    def read(address,size):return bytes(u.mem_read(address,size))
    def snapshot():return dict(node=read(NODE,0x60).hex(),head=struct.unpack('<Q',read(HEAD,8))[0],
        tail=struct.unpack('<Q',read(TAIL,8))[0],counter=struct.unpack('<I',read(COUNTER,4))[0],presence=read(PRESENCE+9*32,1).hex())
    def call(va,args):return dict(kind='call',va=va,args=args)
    def step(uc,address,size,data):
        visits.append(address)
        if address==RETURN:uc.emu_stop();return
        if address==CLEAR:events.append(call(CLEAR,[uc.reg_read(UC_X86_REG_ECX)]));return
        if address not in (INVENTORY,PRESENT):return
        if address==INVENTORY:args=[uc.reg_read(UC_X86_REG_ECX),uc.reg_read(UC_X86_REG_EDX),uc.reg_read(UC_X86_REG_R8D)]
        else:args=[uc.reg_read(UC_X86_REG_ECX),uc.reg_read(UC_X86_REG_EDX),struct.unpack('<I',read(uc.reg_read(UC_X86_REG_R8),4))[0]]
        events.append(call(address,args));callback_states.append(dict(va=address,state=snapshot()))
        # Explicit no-effect dependencies: inventory and presentation are not executed.
        uc.reg_write(UC_X86_REG_RAX,0xBADF00D);uc.reg_write(UC_X86_REG_RCX,0xBADF00D);uc.reg_write(UC_X86_REG_RDX,0xBADF00D)
        rsp=uc.reg_read(UC_X86_REG_RSP);uc.reg_write(UC_X86_REG_RIP,struct.unpack('<Q',read(rsp,8))[0]);uc.reg_write(UC_X86_REG_RSP,rsp+8)
    u.hook_add(unicorn.UC_HOOK_CODE,step)
    u.hook_add(unicorn.UC_HOOK_MEM_WRITE,lambda uc,access,address,size,value,data:
        events.append(dict(kind='write',address=address,bytes=size,value=value&((1<<(size*8))-1))) if not 0x60000000<=address<0x60003000 else None)
    results=[]
    for iteration in range(repeat):
        start_events=len(events);start_states=len(callback_states);start_visits=len(visits)
        before=snapshot()
        memory={p:bytearray(read(p,4096)) for p in (NODE&~4095,HEAD&~4095,COUNTER&~4095,PRESENCE&~4095,(PRESENCE+320)&~4095)}
        expected=[]
        def write(address,size,value):
            expected.append(dict(kind='write',address=address,bytes=size,value=value))
            memory[address&~4095][address&4095:(address&4095)+size]=value.to_bytes(size,'little')
        node=bytes.fromhex(before['node']);prev_now,nxt_now=struct.unpack_from('<QQ',node,16)
        grant_calls=[call(INVENTORY,[item,qty,1]) for item,qty in entries if item!=0xFFFF] if not remove else []
        expected.extend(grant_calls)
        counter_after=before['counter'] if remove else (before['counter']+1)&0xFFFFFFFF
        if not remove:write(COUNTER,4,counter_after)
        write(prev_now+0x18 if prev_now else HEAD,8,nxt_now)
        write(nxt_now+0x10 if nxt_now else TAIL,8,prev_now)
        expected.append(call(PRESENT,[struct.unpack_from('<I',node,0x58)[0],3,COLLECTOR]))
        expected.append(call(CLEAR,[9]));write(PRESENCE+9*32,1,0)
        for offset,size in [(4,8),(0x18,8),(0x10,8),(0x58,4)]:write(NODE+offset,size,0)
        saved={UC_X86_REG_RBX:111,UC_X86_REG_RBP:222,UC_X86_REG_RSI:333,UC_X86_REG_RDI:444,UC_X86_REG_R14:555}
        for reg,v in saved.items():u.reg_write(reg,v)
        u.mem_write(STACK,struct.pack('<Q',RETURN));u.reg_write(UC_X86_REG_RSP,STACK);u.reg_write(UC_X86_REG_RCX,NODE);u.reg_write(UC_X86_REG_EDX,COLLECTOR)
        u.emu_start(0x3197B0 if remove else 0x319920,0,count=1000)
        assert u.reg_read(UC_X86_REG_RIP)==RETURN and u.reg_read(UC_X86_REG_RSP)==STACK+8 and u.reg_read(UC_X86_REG_EAX)==0
        assert all(u.reg_read(r)==v for r,v in saved.items())
        observed_states=callback_states[start_states:]
        expected_states=[dict(va=INVENTORY,state=before) for c in grant_calls]
        present_state=dict(before,counter=counter_after,head=before['head'] if prev_now else nxt_now,tail=before['tail'] if nxt_now else prev_now)
        expected_states.append(dict(va=PRESENT,state=present_state))
        results.append(dict(matches=events[start_events:]==expected and observed_states==expected_states and all(read(p,4096)==bytes(b) for p,b in memory.items()),
            before=before,after=snapshot(),events=events[start_events:],callback_states=observed_states,visited=visits[start_visits:]))
    return dict(name=name,method='original bodies; no-effect inventory/presentation dependencies',remove=remove,position=position,iterations=results)

full=[(0x1000+i,i+1) for i in range(7)];empty=[(0xFFFF,99)]*7
cases=[run('singleton-mixed'),run('head-all-seven',position='head',entries=full),run('tail-no-items',position='tail',entries=empty),
 run('middle-mixed',position='middle'),run('remove-middle',position='middle',remove=True),run('remove-singleton',remove=True),
 run('counter-wrap',counter=0xFFFFFFFF),run('repeat-retired-singleton',repeat=2)]
assert all(i['matches'] for c in cases for i in c['iterations'])
fault=run('mutant-skips-seventh',entries=full,mutant=True)
assert not fault['iterations'][0]['matches']
result=dict(status='PASS',exe_sha256=hashlib.sha256(raw).hexdigest(),source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),cases=cases,seventh_entry_mutant=fault)
(HERE/'result.json').write_text(json.dumps(result,indent=2)+'\n')
cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64)
for va,blob in BODIES.items():(HERE/f'{va:08X}.bin').write_bytes(blob)
(HERE/'disassembly.txt').write_text('\n'.join(f'{i.address:08X} {i.bytes.hex():24} {i.mnemonic} {i.op_str}'.rstrip() for va,blob in BODIES.items() for i in cs.disasm(blob,va))+'\n')
print('PASS: eight collection/removal cases, nine calls; omitted seventh grant detected')
