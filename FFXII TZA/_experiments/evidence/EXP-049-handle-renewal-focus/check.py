"""Original renewal and focus lookup; stop before native refresh."""
import hashlib
import json
from pathlib import Path
import struct
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[4]/'Tools/work/ASTRA/python-libs'))
import capstone
import unicorn
from unicorn.x86_const import *
HERE=Path(__file__).resolve().parent
raw=Path(r'D:\SteamLibrary\steamapps\common\FINAL FANTASY XII THE ZODIAC AGE\x64\FFXII_TZA.exe').read_bytes()
assert hashlib.sha256(raw).hexdigest()=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
pe=struct.unpack_from('<I',raw,60)[0];base=struct.unpack_from('<Q',raw,pe+48)[0]
table=pe+24+struct.unpack_from('<H',raw,pe+20)[0]
bodies={}
for va,size in ((0x2659D0,24),(0x3589B0,38),(0x31B7E0,42),(0x3588B0,143),(0x263FF0,21),(0x263E30,5),(0x3220E0,176),(0x327150,117),(0x236820,37),(0x236850,7)):
    for n in range(struct.unpack_from('<H',raw,pe+6)[0]):
        _,rva,length,disk=struct.unpack_from('<4I',raw,table+40*n+8)
        if rva<=va-base<rva+length:
            offset=disk+va-base-rva;bodies[va]=raw[offset:offset+size]
assert len(bodies)==10
for va in (0x31B7E0,0x3588B0,0x263FF0,0x263E30):
    assert bodies[va]==(HERE.parent/'EXP-034-focus-resolver'/f'{va:08X}.bin').read_bytes()
ACTOR,UNIT,STACK,RETURN=0x50001000,0x50003000,0x60000800,0x60001000


class Fixture:
    def __init__(self,word,mutant=False):
        self.u=unicorn.Uc(unicorn.UC_ARCH_X86,unicorn.UC_MODE_64)
        pages=set()
        for va,blob in bodies.items():pages.update(range(va&~4095,((va+len(blob)-1)&~4095)+4096,4096))
        for page in sorted(pages):self.u.mem_map(page,4096)
        for va,blob in bodies.items():
            if mutant and va==0x2659D0:
                assert blob[16:19]==bytes.fromhex('0f44c2')
                blob=blob[:16]+b'\x90'*3+blob[19:]
            self.u.mem_write(va,blob)
        for addr,size in ((0x2089000,4096),(0x2098000,0x3000),(0x50000000,0x4000),(0x60000000,0x2000)):
            self.u.mem_map(addr,size)
        self.u.mem_write(ACTOR,bytes((i*29+7)%256 for i in range(0x1000)))
        for address,fmt,value in ((0x2089340,'<B',0x10),(0x2098E10+2*0x288,'<Q',0x50002000),
            (0x2098E18+2*0x288,'<Q',0x50000000),(0x2098E20+2*0x288,'<B',1),
            (0x2098E30+2*0x288,'<i',2),(0x50000000,'<i',2),(0x50000010,'<Q',ACTOR),
            (ACTOR,'<H',1),(ACTOR+0x15,'<B',2),(ACTOR+0x16,'<H',word),(ACTOR+0x30,'<Q',UNIT)):
            self.u.mem_write(address,struct.pack(fmt,value))
        self.visited=[];self.writes=[]
        self.u.hook_add(unicorn.UC_HOOK_CODE,self.step)
        self.u.hook_add(unicorn.UC_HOOK_MEM_WRITE,self.write)
    def step(self,u,address,size,data):
        self.visited.append(address)
        if address==RETURN:u.emu_stop()
    def write(self,u,access,address,size,value,data):
        if not 0x60000000<=address<0x60002000:self.writes.append(dict(address=address,bytes=size))
    def word(self):return struct.unpack('<H',self.u.mem_read(ACTOR+0x16,2))[0]
    def call(self,va,arg):
        self.visited=[];self.writes=[]
        before=bytes(self.u.mem_read(ACTOR,0x1000))
        self.u.mem_write(STACK,struct.pack('<Q',RETURN))
        self.u.reg_write(UC_X86_REG_RSP,STACK);self.u.reg_write(UC_X86_REG_RCX,arg)
        self.u.emu_start(va,0,count=200)
        assert self.u.reg_read(UC_X86_REG_RIP)==RETURN and self.u.reg_read(UC_X86_REG_RSP)==STACK+8
        after=bytes(self.u.mem_read(ACTOR,0x1000))
        if va==0x2659D0:
            assert self.writes==[dict(address=ACTOR+0x16,bytes=2)]
            assert before[:0x16]==after[:0x16] and before[0x18:]==after[0x18:]
        else:assert not self.writes and before==after
        return dict(rax=self.u.reg_read(UC_X86_REG_RAX),visited=list(self.visited),writes=list(self.writes))


STATE=0x70000000
REFRESH=0x326500


def run(name,gate=0x10,focus_match=True,enabled=1,backpointer=UNIT,selector=3,null=False,mutant=False):
    f=Fixture(7);u=f.u
    u.mem_map(STATE,0x6000);u.mem_map(0x2EBF000,0x1000);u.mem_map(0x208E000,0x1000)
    u.mem_map(0x326000,0x1000)
    state_before=bytearray(b'\xA5'*0x6000)
    state_before[0x5AA4]=selector
    stats=STATE+8+3*0x1C8
    state_before[stats-STATE+4]=3
    u.mem_write(STATE,bytes(state_before))
    old_handle=(7<<20)|(2<<16)|1
    new_handle=(8<<20)|(2<<16)|1
    for address,fmt,value in ((0x2EBF190,'<Q',STATE),(0x208E688,'<Q',UNIT),(0x208E6A0,'<i',1),
                              (UNIT+0x698,'<Q',stats),(UNIT+8,'<I',old_handle if focus_match else old_handle+1),
                              (ACTOR+0x30,'<Q',backpointer),(0x2089340,'<B',gate),
                              (0x2098E20+2*0x288,'<B',enabled)):
        u.mem_write(address,struct.pack(fmt,value))
    if mutant:
        blob=bodies[0x3220E0]
        assert blob[0x93:0x99]==bytes.fromhex('8988a45a0000')
        # Same instruction length, but store CL instead of ECX: adjacent bytes stay stale.
        u.mem_write(0x322173,b'\x88\x88\xa4\x5a\x00\x00')
    actor_before=bytes(u.mem_read(ACTOR,0x1000))
    unit_before=bytes(u.mem_read(UNIT,0x1000))
    refresh=[]
    def stop(emu,address,size,data):
        if address==REFRESH:
            refresh.append(address);emu.emu_stop()
    u.hook_add(unicorn.UC_HOOK_CODE,stop)
    u.mem_write(STACK,struct.pack('<Q',RETURN))
    u.reg_write(UC_X86_REG_RSP,STACK);u.reg_write(UC_X86_REG_RCX,0 if null else ACTOR)
    error=None
    try:u.emu_start(0x3220E0,0,count=400)
    except unicorn.UcError as exc:error=str(exc)
    if null:
        assert error and u.reg_read(UC_X86_REG_RIP)==0x2659D0
        assert not f.writes and not refresh
        return dict(name=name,status='EXPECTED_UNMAPPED_NULL_READ',error=error,visited=f.visited,writes=f.writes)
    assert error is None
    matched=focus_match and selector<=0x27
    wanted=3 if gate&0x10 and enabled and backpointer else 0xFF
    expected=bytearray(state_before)
    if matched:struct.pack_into('<I',expected,0x5AA4,wanted)
    expected_actor=bytearray(actor_before);struct.pack_into('<H',expected_actor,0x16,8)
    assert bytes(u.mem_read(ACTOR,0x1000))==bytes(expected_actor)
    assert bytes(u.mem_read(UNIT,0x1000))==unit_before
    assert u.reg_read(UC_X86_REG_RIP)==(REFRESH if matched else RETURN)
    if not matched:
        assert u.reg_read(UC_X86_REG_RSP)==STACK+8 and u.reg_read(UC_X86_REG_RAX)==new_handle
    writes=[dict(address=ACTOR+0x16,bytes=2)]
    if matched:writes.append(dict(address=STATE+0x5AA4,bytes=4))
    # Both encodings bracket the increment, before the original focus lookup.
    calls=[a for a in f.visited if a in (0x3589B0,0x2659D0,0x327150,REFRESH)]
    assert calls==[0x3589B0,0x2659D0,0x3589B0,0x327150]+([REFRESH] if matched else [])
    actual=bytes(u.mem_read(STATE,0x6000))
    return dict(name=name,status='STOP_BEFORE_NATIVE_REFRESH' if matched else 'RETURNED',
                matches=actual==bytes(expected) and f.writes==writes,call_order=calls,
                visited=f.visited,writes=f.writes,selector_before=state_before[0x5AA4:0x5AA8].hex(),
                selector_after=actual[0x5AA4:0x5AA8].hex(),old_handle=old_handle,new_handle=new_handle,
                resulting_word=f.word(),refresh_executed=False)


cases=[run('focused'),run('other-focus',focus_match=False),run('no-focus',selector=0xFF),
       run('battle-gate-off',gate=0),run('manager-disabled',enabled=0),
       run('no-unit-backpointer',backpointer=0),run('null-actor',null=True)]
assert all(c.get('matches',True) for c in cases)
fault=run('byte-store-mutant',mutant=True);assert not fault['matches']
result=dict(status='PASS',method='ten original bodies; synthetic memory; native refresh not executed; no stubs',
    exe_sha256=hashlib.sha256(raw).hexdigest(),source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    cases=cases,byte_store_mutant=fault)
cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64)
for va,blob in bodies.items():(HERE/f'{va:08X}.bin').write_bytes(blob)
(HERE/'disassembly.txt').write_text('\n'.join(f'{i.address:08X} {i.bytes.hex():24} {i.mnemonic} {i.op_str}'.rstrip()
    for va,blob in bodies.items() for i in cs.disasm(blob,va))+'\n')
(HERE/'result.json').write_text(json.dumps(result,indent=2)+'\n')
print('PASS: seven renewal/focus boundaries; dword-store fault detected; native refresh omitted')

