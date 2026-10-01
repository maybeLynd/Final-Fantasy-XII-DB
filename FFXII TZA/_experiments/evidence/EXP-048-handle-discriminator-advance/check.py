"""Original advance, encode and resolve composition; synthetic memory, no stubs."""
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
for va,size in ((0x2659D0,24),(0x3589B0,38),(0x31B7E0,42),(0x3588B0,143),(0x263FF0,21),(0x263E30,5)):
    for n in range(struct.unpack_from('<H',raw,pe+6)[0]):
        _,rva,length,disk=struct.unpack_from('<4I',raw,table+40*n+8)
        if rva<=va-base<rva+length:
            offset=disk+va-base-rva;bodies[va]=raw[offset:offset+size]
assert len(bodies)==6
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


cases=[]
for word in (0,1,0x7FE,0x7FF,0x800,0xFFFF):
    f=Fixture(word)
    old=f.call(0x3589B0,ACTOR)
    assert old['rax']==((word&0x7FF)<<20)|(2<<16)|1
    prior=f.call(0x31B7E0,old['rax'])
    assert prior['rax']==(UNIT if word<=0x7FF else 0)
    advance=f.call(0x2659D0,ACTOR)
    expected=((word+1)&0x7FF) or 1
    assert f.word()==expected and advance['rax']==expected
    new=f.call(0x3589B0,ACTOR)
    stale=f.call(0x31B7E0,old['rax']);current=f.call(0x31B7E0,new['rax'])
    assert stale['rax']==0 and current['rax']==UNIT
    cases.append(dict(initial_word=word,next_word=f.word(),old_encoding=old,prior_resolution=prior,
                      advance=advance,new_encoding=new,stale_resolution=stale,current_resolution=current))
# A complete finite period distinguishes temporary invalidation from permanent uniqueness.
f=Fixture(1);original=f.call(0x3589B0,ACTOR)['rax'];sequence=[]
for _ in range(2047):
    f.call(0x2659D0,ACTOR);sequence.append(f.word())
assert sequence==list(range(2,2048))+[1]
assert f.call(0x3589B0,ACTOR)['rax']==original
cycle_resolution=f.call(0x31B7E0,original)
assert cycle_resolution['rax']==UNIT
fault=Fixture(0x7FF,mutant=True);fault.call(0x2659D0,ACTOR)
assert fault.word()==0 and fault.word()!=1
result=dict(status='PASS',method='six original bodies; synthetic stable registry; no stubs or game process',
    exe_sha256=hashlib.sha256(raw).hexdigest(),source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    cases=cases,cycle=dict(advances=2047,initial_word=1,final_word=f.word(),original_handle=original,
        words_sha256=hashlib.sha256(struct.pack('<2047H',*sequence)).hexdigest(),old_handle_resolution=cycle_resolution),
    mutant=dict(change='remove zero-to-one CMOVE',initial_word=0x7FF,observed_word=fault.word(),required_word=1))
cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64)
for va,blob in bodies.items():(HERE/f'{va:08X}.bin').write_bytes(blob)
(HERE/'disassembly.txt').write_text('\n'.join(f'{i.address:08X} {i.bytes.hex():24} {i.mnemonic} {i.op_str}'.rstrip()
    for va,blob in bodies.items() for i in cs.disasm(blob,va))+'\n')
(HERE/'result.json').write_text(json.dumps(result,indent=2)+'\n')
print('PASS: six advance/encode/resolve cases; 2047-step finite period; zero-wrap fault detected')
