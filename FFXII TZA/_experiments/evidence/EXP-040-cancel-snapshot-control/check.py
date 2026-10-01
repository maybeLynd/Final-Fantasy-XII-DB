"""Isolated original cancellation gates/stores. No calls are stubbed or executed."""
import hashlib
import json
from pathlib import Path
import struct
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[4]/'Tools/work/ASTRA/python-libs'))
import capstone
import unicorn
from unicorn.x86_const import UC_X86_REG_RIP,UC_X86_REG_RSP,UC_X86_REG_RCX,UC_X86_REG_RBX,UC_X86_REG_RBP,UC_X86_REG_RSI
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'EXP-032-command-snapshot'))
from command_snapshot import snapshot

identity=json.loads((HERE/'identity.json').read_text())
raw=Path(r'D:\SteamLibrary\steamapps\common\FINAL FANTASY XII THE ZODIAC AGE\x64\FFXII_TZA.exe').read_bytes()
assert hashlib.sha256(raw).hexdigest()==identity['exe_sha256']
START,END=0x3105D0,0x310772
file_offset=identity['file_offset']+START-identity['begin']
code=raw[file_offset:file_offset+END-START]
assert code[:3]==bytes.fromhex('4885c9') and code[-1:]==b'\xc3'
UNIT,ACTOR,STACK,RETURN=0x50000000,0x50010000,0x60000800,0x60001000


def machine(unit):
    uc=unicorn.Uc(unicorn.UC_ARCH_X86,unicorn.UC_MODE_64)
    uc.mem_map(0x310000,0x1000);uc.mem_write(START,code)
    uc.mem_map(UNIT,0x1000);uc.mem_write(UNIT,unit)
    uc.mem_map(0x60000000,0x2000);uc.mem_write(STACK,struct.pack('<Q',RETURN))
    uc.mem_map(0x208D000,0x1000);uc.mem_write(0x208D45C,struct.pack('<I',77))
    uc.reg_write(UC_X86_REG_RSP,STACK)
    return uc


def execute(uc,start,stop):
    visited=[]
    writes=[]
    def step(emu,address,size,data):
        visited.append(address)
        if address==stop:emu.emu_stop()
    uc.hook_add(unicorn.UC_HOOK_CODE,step)
    uc.hook_add(unicorn.UC_HOOK_MEM_WRITE,lambda u,a,address,size,value,data:writes.append(dict(address=address,bytes=size)))
    uc.emu_start(start,0,count=100)
    assert uc.reg_read(UC_X86_REG_RIP)==stop and len(visited)<100
    return dict(start=start,stop=stop,visited=visited,writes=writes)


def initial(flags):
    value=bytearray((i*37+19)%256 for i in range(0xF50))
    value[0]=1
    struct.pack_into('<Q',value,0x10,ACTOR)
    value[0xEA9]=0
    struct.pack_into('<I',value,0x700,flags)
    struct.pack_into('<Q',value,0x708,0xFEDCBA9876543210)
    struct.pack_into('<I',value,0x710,0x87654321)
    struct.pack_into('<H',value,0x714,0x1234)
    return bytes(value)


class Reader:
    def __init__(self,uc):self.uc=uc
    def read(self,address,size):return bytes(self.uc.mem_read(address,size))


cases=[]
for flags in (0,3,0xFFFFFFFF):
    before=initial(flags);uc=machine(before)
    uc.reg_write(UC_X86_REG_RBX,UNIT);uc.reg_write(UC_X86_REG_RSI,UNIT+0x80);uc.reg_write(UC_X86_REG_RBP,0)
    before_snapshot=snapshot(Reader(uc),UNIT,0,ACTOR)
    trace=execute(uc,0x3106B9,0x31072F)
    after=bytes(uc.mem_read(UNIT,len(before)))
    after_snapshot=snapshot(Reader(uc),UNIT,0,ACTOR)
    expected=bytearray(before)
    expected[0x730:0x748]=before[0x718:0x730]
    struct.pack_into('<I',expected,0x700,flags&0xFFFFFFFC)
    for offset,size in ((0x6B7,2),(0x6B4,1),(0x768,8),(0x760,8),(0x6D8,8),
                        (0x6D0,8),(0x75C,4),(0x708,8),(0x710,4)):
        expected[offset:offset+size]=b'\0'*size
    expected[0x714:0x716]=b'\xff\xff'
    assert after==bytes(expected),'whole-unit local effects differ'
    assert after_snapshot['live']['context_is_sentinel']
    assert after_snapshot['live']['target_focus_handle']==0
    assert after_snapshot['live']['action_id']==0xFFFF
    assert after_snapshot['action_phase']==0
    assert after_snapshot['shadow']==before_snapshot['shadow']
    assert all(UNIT<=x['address'] and x['address']+x['bytes']<=UNIT+len(before) for x in trace['writes'])
    cases.append(dict(flags=flags,trace=trace,before=before_snapshot,after=after_snapshot,
                      changed_offsets=[i for i,(a,b) in enumerate(zip(before,after)) if a!=b],
                      copied_shadow=after[0x730:0x748].hex(),unit_after_sha256=hashlib.sha256(after).hexdigest()))

# Entry gates execute actual prologue/epilogue, returning only when no native call is reached.
gates=[]
for kind in ('null_unit','null_stats','nonzero_stats'):
    before=bytearray(initial(3))
    struct.pack_into('<Q',before,0x698,0 if kind=='null_stats' else 0x50020000)
    uc=machine(bytes(before));uc.reg_write(UC_X86_REG_RCX,0 if kind=='null_unit' else UNIT)
    stop=0x310605 if kind=='nonzero_stats' else RETURN
    trace=execute(uc,START,stop)
    assert bytes(uc.mem_read(UNIT,len(before)))==bytes(before)
    if stop==RETURN:assert uc.reg_read(UC_X86_REG_RSP)==STACK+8
    gates.append(dict(kind=kind,trace=trace,rsp=uc.reg_read(UC_X86_REG_RSP)))

# The earlier unnamed-byte reset is separate: stop before resource-release call.
before=initial(3);uc=machine(before);uc.reg_write(UC_X86_REG_RBX,UNIT)
prefix=execute(uc,0x31060A,0x310618)
after=bytes(uc.mem_read(UNIT,len(before)));expected=bytearray(before);expected[0x6B6]=0
assert after==bytes(expected)

result=dict(status='PASS',scope='isolated original gates and local writes; no native calls or live game',
            exe_sha256=identity['exe_sha256'],begin=START,end=END,file_offset=file_offset,
            code_sha256=hashlib.sha256(code).hexdigest(),unicorn=unicorn.__version__,capstone=capstone.__version__,
            source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            snapshot_sha256=hashlib.sha256((HERE.parent/'EXP-032-command-snapshot/command_snapshot.py').read_bytes()).hexdigest(),
            cases=cases,gates=gates,unnamed_prefix=prefix)
cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64)
disassembly='\n'.join(('%08X %-24s %s %s'%(x.address,x.bytes.hex(),x.mnemonic,x.op_str)).rstrip() for x in cs.disasm(code,START))+'\n'
for name,data in [('full-function.bin',code),('full-disassembly.txt',disassembly.encode()),('result.json',(json.dumps(result,indent=2)+'\n').encode())]:
    with (HERE/name).open('xb') as output:output.write(data)
print('PASS: three command-store cases, three original entry gates, one separate unnamed-byte reset; no calls executed')
