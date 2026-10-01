"""Original four-function resolver chain against explicit synthetic memory.
No stubs, game process or writes to the reference executable. Fresh emulator/case.
"""
import hashlib,json,struct,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[4]/'Tools/work/ASTRA/python-libs'))
import unicorn,capstone
from unicorn.x86_const import UC_X86_REG_RCX,UC_X86_REG_RAX,UC_X86_REG_RSP,UC_X86_REG_RIP
HERE=Path(__file__).resolve().parent
exe=Path(r'D:\SteamLibrary\steamapps\common\FINAL FANTASY XII THE ZODIAC AGE\x64\FFXII_TZA.exe').read_bytes()
digest=hashlib.sha256(exe).hexdigest()
assert digest=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
pe=struct.unpack_from('<I',exe,60)[0];base=struct.unpack_from('<Q',exe,pe+48)[0]
table=pe+24+struct.unpack_from('<H',exe,pe+20)[0]
bodies={}
for va,size in [(0x31B7E0,42),(0x3588B0,143),(0x263FF0,21),(0x263E30,5)]:
    for i in range(struct.unpack_from('<H',exe,pe+6)[0]):
        _,rva,length,off=struct.unpack_from('<4I',exe,table+40*i+8)
        if rva<=va-base<rva+length:
            start=off+va-base-rva;bodies[va]=exe[start:start+size]
assert len(bodies)==4
cases=[('valid',{},0x50003000),('gate_off',{'gate':0},0),('handle_zero',{'handle':0},0),
 ('manager4',{'manager':4},0x50003000),('manager5',{'manager':5},0),
 ('no_vector',{'vector':0},0),('no_storage',{'storage':0},0),
 ('manager_disabled',{'enabled':0},0),('capacity_equal',{'capacity':1},0),
 ('capacity_negative',{'capacity':-1},0),('count_equal',{'count':1},0),
 ('count_negative',{'count':-1},0),('null_entry',{'entry':0},0),
 ('discriminator_mismatch',{'word':8},0),('word_upper_bits',{'word':0x807},0),
 ('bit31_alias',{'high':0x80000000},0x50003000),('no_battle_unit',{'unit':0},0)]
results=[]
for name,changes,expected in cases:
    p=dict(gate=0x10,manager=2,index=1,disc=7,vector=0x50000000,storage=0x50002000,
           enabled=1,capacity=2,count=2,entry=0x50001000,word=7,unit=0x50003000,high=0)
    p.update(changes)
    handle=p.get('handle',p['high']|(p['disc']<<20)|(p['manager']<<16)|p['index'])
    uc=unicorn.Uc(unicorn.UC_ARCH_X86,unicorn.UC_MODE_64)
    pages=set()
    for va,blob in bodies.items():pages.update(range(va&~4095,((va+len(blob)-1)&~4095)+4096,4096))
    for page in sorted(pages):uc.mem_map(page,4096)
    for va,blob in bodies.items():uc.mem_write(va,blob)
    for addr,size in [(0x2089000,4096),(0x2098000,0x3000),(0x50000000,0x4000),(0x60000000,0x2000)]:uc.mem_map(addr,size)
    def put(addr,fmt,value):uc.mem_write(addr,struct.pack(fmt,value))
    put(0x2089340,'<B',p['gate'])
    manager=0x2098E10+p['manager']*0x288
    put(manager,'<Q',p['storage']);put(manager+8,'<Q',p['vector'])
    put(manager+0x10,'<B',p['enabled']);put(manager+0x20,'<i',p['capacity'])
    put(0x50000000,'<i',p['count']);put(0x50000010,'<Q',p['entry'])
    put(0x50001016,'<H',p['word']);put(0x50001030,'<Q',p['unit'])
    put(0x60000800,'<Q',0x60001000)
    uc.reg_write(UC_X86_REG_RSP,0x60000800);uc.reg_write(UC_X86_REG_RCX,handle)
    before=bytes(uc.mem_read(0x50000000,0x4000));visited=[];resolved=[]
    def hook(emu,address,size,user):
        visited.append(address)
        if address==0x263E30:resolved.append(emu.reg_read(UC_X86_REG_RCX))
        if address==0x60001000:emu.emu_stop()
    uc.hook_add(unicorn.UC_HOOK_CODE,hook)
    uc.emu_start(0x31B7E0,0x60001001,count=200)
    assert uc.reg_read(UC_X86_REG_RIP)==0x60001000 and len(visited)<200
    assert uc.reg_read(UC_X86_REG_RSP)==0x60000808
    actual=uc.reg_read(UC_X86_REG_RAX)
    assert actual==expected,(name,actual,expected)
    assert before==bytes(uc.mem_read(0x50000000,0x4000))
    results.append(dict(name=name,fixture=p,handle=handle,expected=expected,actual=actual,
                        resolved_actors=resolved,visited=visited,returned=True,fixture_unchanged=True))
for name in ['result.json','manifest.json','disassembly.txt']:assert not (HERE/name).exists()
dis=[]
for va,blob in bodies.items():
    path=HERE/('%08X.bin'%va);assert not path.exists();path.write_bytes(blob)
    for ins in capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64).disasm(blob,va):
        dis.append(('%08X %-24s %s %s'%(ins.address,ins.bytes.hex(),ins.mnemonic,ins.op_str)).rstrip())
(HERE/'disassembly.txt').write_text('\n'.join(dis)+'\n')
(HERE/'result.json').write_text(json.dumps(dict(status='PASS',scope='original resolver chain, synthetic memory only',
 exe_sha256=digest,source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
 unicorn=unicorn.__version__,capstone=capstone.__version__,results=results),indent=2)+'\n')
files={p.name:dict(bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest())
       for p in HERE.iterdir() if p.is_file() and p.name!='manifest.json'}
(HERE/'manifest.json').write_text(json.dumps(dict(files=files),indent=2)+'\n')
print('PASS17 original-chain cases; declared return boundary reached in every case')
