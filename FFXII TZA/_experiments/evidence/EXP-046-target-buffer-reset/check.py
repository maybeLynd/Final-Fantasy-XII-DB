"""Original reset wrapper; imported memset is an explicit controlled stub."""
import hashlib
import json
from pathlib import Path
import struct
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[4] / 'Tools/work/ASTRA/python-libs'))
import capstone
import unicorn
from unicorn.x86_const import *

HERE = Path(__file__).resolve().parent
EXE = Path(r'D:\SteamLibrary\steamapps\common\FINAL FANTASY XII THE ZODIAC AGE\x64\FFXII_TZA.exe')
raw = EXE.read_bytes()
assert hashlib.sha256(raw).hexdigest() == '73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
pe = struct.unpack_from('<I', raw, 60)[0]
base = struct.unpack_from('<Q', raw, pe + 48)[0]
table = pe + 24 + struct.unpack_from('<H', raw, pe + 20)[0]
sections = [struct.unpack_from('<4I', raw, table + 40*n + 8)
            for n in range(struct.unpack_from('<H', raw, pe + 6)[0])]


def offset(rva):
    matches = [disk + rva - start for virtual, start, size, disk in sections if start <= rva < start + size]
    assert len(matches) == 1
    return matches[0]


def string(rva):
    return raw[offset(rva):].split(b'\0', 1)[0].decode('ascii')


code = raw[offset(0x316CF0-base):offset(0x316CF0-base)+57]
assert code[-1:] == b'\xc3'
thunk = raw[offset(0x861EC0-base):offset(0x861EC0-base)+6]
assert thunk[:2] == b'\xff\x25'
iat = 0x861EC6 + struct.unpack_from('<i', thunk, 2)[0]
imports = []
directory = struct.unpack_from('<I', raw, pe+24+112+8)[0]
cursor = offset(directory)
while True:
    original, stamp, forward, name, first = struct.unpack_from('<5I', raw, cursor)
    if not any((original, stamp, forward, name, first)):
        break
    index = 0
    while True:
        entry = struct.unpack_from('<Q', raw, offset(original or first)+index*8)[0]
        if not entry:
            break
        if base+first+index*8 == iat:
            assert not entry >> 63
            imports.append(dict(dll=string(name), symbol=string(entry+2), iat=iat))
        index += 1
    cursor += 20
assert len(imports) == 1 and imports[0]['symbol'] == 'memset'
MEMORY, BUFFER, STACK, RETURN = 0x50000000, 0x50000100, 0x60000800, 0x60001000


def execute(blob, flag, count):
    u = unicorn.Uc(unicorn.UC_ARCH_X86, unicorn.UC_MODE_64)
    u.mem_map(0x316000, 0x1000)
    u.mem_write(0x316CF0, blob)
    u.mem_map(0x861000, 0x1000)
    u.mem_write(0x861EC0, thunk)
    before = bytearray((i*29+11)%256 for i in range(0x1000))
    before[0x100] = flag
    struct.pack_into('<i', before, 0x104, count)
    u.mem_map(MEMORY, 0x1000)
    u.mem_write(MEMORY, bytes(before))
    u.mem_map(0x60000000, 0x2000)
    u.mem_write(STACK, struct.pack('<Q', RETURN))
    for reg, value in ((UC_X86_REG_RSP, STACK), (UC_X86_REG_RCX, BUFFER),
                       (UC_X86_REG_RBX, 0xFEDCBA9876543210), (UC_X86_REG_RDI, 0x123456789ABCDEF0)):
        u.reg_write(reg, value)
    visited, writes, calls = [], [], []
    def step(uc, address, size, data):
        visited.append(address)
        if address == RETURN:
            uc.emu_stop()
        elif address == 0x861EC0:
            dest, value, size = [uc.reg_read(reg) for reg in (UC_X86_REG_RCX, UC_X86_REG_RDX, UC_X86_REG_R8)]
            calls.append(dict(destination=dest, value=value, bytes=size, method='controlled imported memset stub'))
            assert dest == BUFFER and value == 0 and 0 <= size <= 0x208
            uc.mem_write(dest, bytes([value & 255])*size)
            rsp = uc.reg_read(UC_X86_REG_RSP)
            resume = struct.unpack('<Q', uc.mem_read(rsp, 8))[0]
            uc.reg_write(UC_X86_REG_RAX, dest)
            uc.reg_write(UC_X86_REG_RSP, rsp+8)
            uc.reg_write(UC_X86_REG_RIP, resume)
    u.hook_add(unicorn.UC_HOOK_CODE, step)
    u.hook_add(unicorn.UC_HOOK_MEM_WRITE,
               lambda uc, access, address, size, value, data: writes.append(dict(address=address, bytes=size)))
    u.emu_start(0x316CF0, 0, count=50)
    assert u.reg_read(UC_X86_REG_RIP) == RETURN and u.reg_read(UC_X86_REG_RSP) == STACK+8
    assert u.reg_read(UC_X86_REG_RBX) == 0xFEDCBA9876543210
    assert u.reg_read(UC_X86_REG_RDI) == 0x123456789ABCDEF0
    assert u.reg_read(UC_X86_REG_RAX) == BUFFER
    after = bytes(u.mem_read(MEMORY, 0x1000))
    expected = bytearray(before)
    expected[0x100:0x308] = b'\0'*0x208
    expected[0x100] = flag & 1
    data_writes = [w for w in writes if MEMORY <= w['address'] < MEMORY+0x1000]
    assert data_writes == [dict(address=BUFFER, bytes=1), dict(address=BUFFER, bytes=1), dict(address=BUFFER+1, bytes=2)]
    return dict(flag=flag, count=count, calls=calls, visited=visited, original_instruction_writes=writes,
                fill_stub_writes_not_in_instruction_hook=True, buffer_before=bytes(before[0x100:0x308]).hex(),
                buffer_after=after[0x100:0x308].hex(), return_rax=u.reg_read(UC_X86_REG_RAX),
                matches=after == bytes(expected) and len(calls)==1 and calls[0]['bytes']==0x208)


cases = [execute(code, flag, count) for flag, count in ((0,0), (1,1), (0xFE,32), (0xFF,-1))]
assert all(case['matches'] for case in cases)
# Truncate only the declared fill extent; wrapper still returns normally.
assert code[15:21] == bytes.fromhex('41b808020000')
mutant = bytearray(code)
struct.pack_into('<I', mutant, 17, 0x108)
fault = execute(bytes(mutant), 0xFF, 32)
assert not fault['matches']
disassembly = '\n'.join(f'{i.address:08X} {i.bytes.hex():24} {i.mnemonic} {i.op_str}'.rstrip()
    for i in capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64).disasm(code, 0x316CF0))+'\n'
result = dict(status='PASS', method='original reset wrapper, controlled imported memset stub; no native DLL execution',
              exe_sha256=hashlib.sha256(raw).hexdigest(), function_sha256=hashlib.sha256(code).hexdigest(),
              source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(), imports=imports,
              cases=cases, extent_mutant=fault, unicorn=unicorn.__version__)
for name, data in [('function.bin',code), ('thunk.bin',thunk), ('disassembly.txt',disassembly.encode()),
                   ('result.json',(json.dumps(result,indent=2)+'\n').encode())]:
    with (HERE/name).open('xb') as output:
        output.write(data)
print(disassembly)
print(imports)
print('PASS: four original wrapper cases with explicit fill stub; truncated extent detected')
