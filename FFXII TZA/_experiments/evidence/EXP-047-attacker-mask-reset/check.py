"""Original reset wrappers: stop at native delegate, then test a controlled return separately."""
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
raw = Path(r'D:\SteamLibrary\steamapps\common\FINAL FANTASY XII THE ZODIAC AGE\x64\FFXII_TZA.exe').read_bytes()
assert hashlib.sha256(raw).hexdigest() == '73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
pe = struct.unpack_from('<I', raw, 60)[0]
base = struct.unpack_from('<Q', raw, pe+48)[0]
table = pe+24+struct.unpack_from('<H', raw, pe+20)[0]
sections = [struct.unpack_from('<4I', raw, table+40*n+8)
            for n in range(struct.unpack_from('<H', raw, pe+6)[0])]


def extract(va, size):
    offsets = [disk+va-base-rva for _, rva, length, disk in sections if rva <= va-base < rva+length]
    assert len(offsets) == 1
    return raw[offsets[0]:offsets[0]+size]


codes = {0x322050: extract(0x322050, 44), 0x322080: extract(0x322080, 89),
         0x263E30: extract(0x263E30, 5)}
assert codes[0x263E30] == bytes.fromhex('488b4130c3')
UNIT, ACTOR, BOUND_ACTOR, STACK, RETURN = 0x50000100, 0x51000100, 0x51000200, 0x60000800, 0x60001000
DELEGATE = 0x3220E0
STUB_RESULT = 0xFEDCBA9876543210


def execute(name, entry, argument, actor_unit, unit_actor, complete=False, mutant=False):
    u = unicorn.Uc(unicorn.UC_ARCH_X86, unicorn.UC_MODE_64)
    for page in (0x322000, 0x263000, 0x50000000, 0x51000000):
        u.mem_map(page, 0x2000)
    for address, code in codes.items():
        if mutant and address == 0x322050:
            assert code[9:19] == bytes.fromhex('c781a40e000000000000')
            code = code[:9] + b'\x90'*10 + code[19:]
        u.mem_write(address, code)
    before = bytearray((i*19+7)%256 for i in range(0x2000))
    struct.pack_into('<Q', before, 0x110, unit_actor)
    struct.pack_into('<I', before, 0xFA4, 0x80000021)
    before[0xFA8] = 3
    u.mem_write(0x50000000, bytes(before))
    actor_before = bytearray(b'\xA5'*0x2000)
    struct.pack_into('<Q', actor_before, 0x130, actor_unit)
    u.mem_write(0x51000000, bytes(actor_before))
    u.mem_map(0x60000000, 0x2000)
    u.mem_write(STACK, struct.pack('<Q', RETURN))
    for reg, value in ((UC_X86_REG_RCX, argument), (UC_X86_REG_RSP, STACK),
                       (UC_X86_REG_RBX, 0xABCDEF0123456789), (UC_X86_REG_RDI, 0x123456789ABCDEF0)):
        u.reg_write(reg, value)
    visited, writes, delegates = [], [], []
    def step(uc, address, size, data):
        visited.append(address)
        if address == RETURN:
            uc.emu_stop()
        elif address == DELEGATE:
            delegates.append(dict(rcx=uc.reg_read(UC_X86_REG_RCX), rsp=uc.reg_read(UC_X86_REG_RSP)))
            if not complete:
                uc.emu_stop()
            else:
                rsp = uc.reg_read(UC_X86_REG_RSP)
                destination = struct.unpack('<Q', uc.mem_read(rsp, 8))[0]
                uc.reg_write(UC_X86_REG_RAX, STUB_RESULT)
                uc.reg_write(UC_X86_REG_RSP, rsp+8)
                uc.reg_write(UC_X86_REG_RIP, destination)
    u.hook_add(unicorn.UC_HOOK_CODE, step)
    u.hook_add(unicorn.UC_HOOK_MEM_WRITE, lambda uc, access, address, size, value, data:
               writes.append(dict(address=address, bytes=size)))
    u.emu_start(entry, 0, count=100)
    resetting = entry == 0x322050 or (argument != 0 and actor_unit != 0)
    expected = bytearray(before)
    footprint = []
    if resetting:
        struct.pack_into('<I', expected, 0xFA4, 0)
        expected[0xFA8] = 0
        footprint = [dict(address=UNIT+0xEA4, bytes=4), dict(address=UNIT+0xEA8, bytes=1)]
        if complete:
            struct.pack_into('<I', expected, 0x108, STUB_RESULT & 0xFFFFFFFF)
            footprint.append(dict(address=UNIT+8, bytes=4))
    assert len(delegates) == 1 and delegates[0]['rcx'] == (unit_actor if resetting else argument)
    assert u.reg_read(UC_X86_REG_RIP) == (RETURN if complete else DELEGATE)
    if complete:
        assert u.reg_read(UC_X86_REG_RSP) == STACK+8
        assert u.reg_read(UC_X86_REG_RBX) == 0xABCDEF0123456789
        assert u.reg_read(UC_X86_REG_RDI) == 0x123456789ABCDEF0
        assert u.reg_read(UC_X86_REG_RAX) == STUB_RESULT
    assert bytes(u.mem_read(0x51000000, 0x2000)) == bytes(actor_before)
    after = bytes(u.mem_read(0x50000000, 0x2000))
    actual_writes = [w for w in writes if 0x50000000 <= w['address'] < 0x50002000]
    return dict(name=name, mode='controlled delegate return' if complete else 'stop before delegate; no stubs',
                matches=after == bytes(expected) and actual_writes == footprint,
                delegate=delegates, visited=visited, writes=writes,
                before_mask=0x80000021, before_count=3,
                after_mask=struct.unpack_from('<I', after, 0xFA4)[0], after_count=after[0xFA8],
                unit_before=bytes(before[0x100:0x1050]).hex(), unit_after=after[0x100:0x1050].hex())


fixtures = [('unit',0x322050,UNIT,UNIT,BOUND_ACTOR), ('unit-null-actor',0x322050,UNIT,UNIT,0),
            ('actor-bound',0x322080,ACTOR,UNIT,BOUND_ACTOR), ('actor-no-unit',0x322080,ACTOR,0,BOUND_ACTOR),
            ('null-actor',0x322080,0,0,BOUND_ACTOR)]
cases = [execute(*fixture, complete=complete) for complete in (False,True) for fixture in fixtures]
assert all(case['matches'] for case in cases)
fault = execute(*fixtures[0], mutant=True)
assert not fault['matches']
result = dict(status='PASS', exe_sha256=hashlib.sha256(raw).hexdigest(),
              source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              cases=cases, omitted_mask_clear_mutant=fault, native_delegate_executed=False)
cs = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
for va, code in codes.items():
    (HERE/f'{va:08X}.bin').write_bytes(code)
disasm = '\n'.join(f'{i.address:08X} {i.bytes.hex():24} {i.mnemonic} {i.op_str}'.rstrip()
                   for va, code in codes.items() for i in cs.disasm(code, va))+'\n'
(HERE/'disassembly.txt').write_text(disasm)
(HERE/'result.json').write_text(json.dumps(result,indent=2)+'\n')
print('PASS: five original prefixes, five controlled-return cases, omitted reset detected')
