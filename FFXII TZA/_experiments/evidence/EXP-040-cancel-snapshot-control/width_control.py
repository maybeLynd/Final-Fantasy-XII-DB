"""One private pointer-width mutant checks detection of uncleared context high bits."""
import hashlib
import json
from pathlib import Path
import struct
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[4]/'Tools/work/ASTRA/python-libs'))
import unicorn
from unicorn.x86_const import UC_X86_REG_RIP,UC_X86_REG_RBX,UC_X86_REG_RBP,UC_X86_REG_RSI
HERE=Path(__file__).resolve().parent
original=(HERE/'full-function.bin').read_bytes()
offset=0x310722-0x3105D0
assert original[offset:offset+7]==bytes.fromhex('4889ab08070000')
changed=bytearray(original);changed[offset]=0x40
results=[]
for name,blob in [('original',original),('dword_context_reset',bytes(changed))]:
    uc=unicorn.Uc(unicorn.UC_ARCH_X86,unicorn.UC_MODE_64)
    uc.mem_map(0x310000,0x1000);uc.mem_write(0x3105D0,blob)
    uc.mem_map(0x50000000,0x1000)
    uc.mem_write(0x50000708,struct.pack('<Q',0xFEDCBA9876543210))
    uc.reg_write(UC_X86_REG_RBX,0x50000000);uc.reg_write(UC_X86_REG_RBP,0);uc.reg_write(UC_X86_REG_RSI,0x50000080)
    def stop(u,address,size,data):
        if address==0x31072F:u.emu_stop()
    uc.hook_add(unicorn.UC_HOOK_CODE,stop)
    uc.emu_start(0x3106B9,0,count=100)
    assert uc.reg_read(UC_X86_REG_RIP)==0x31072F
    context=struct.unpack('<Q',uc.mem_read(0x50000708,8))[0]
    assert context==(0 if name=='original' else 0xFEDCBA9800000000)
    results.append(dict(name=name,code_sha256=hashlib.sha256(blob).hexdigest(),context=context,
                        detected=context!=0,boundary=uc.reg_read(UC_X86_REG_RIP)))
assert (HERE/'full-function.bin').read_bytes()==original
with (HERE/'width-control.json').open('x') as output:
    json.dump(dict(status='PASS',mutation_va=0x310722,original_byte=0x48,mutant_byte=0x40,
                   source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),results=results),output,indent=2)
print('PASS: original clears all64 context bits; private32-bit-store mutant detected')
