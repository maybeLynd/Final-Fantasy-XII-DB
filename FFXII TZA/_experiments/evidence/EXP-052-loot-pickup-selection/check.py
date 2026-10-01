"""Original nearest-loot selection, presence reader and squared-XZ geometry."""
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

BODIES = {va: extract(va, size) for va, size in [(0x319850, 197), (0x2FB310, 38), (0x3A1960, 31)]}
HEAD, LIMIT, PRESENCE, COOKIE = 0x2EC1360, 0x2F973B8, 0x22BE7F0, 0x1F44830
ACTOR, NODES, OUTPUT, STACK, RETURN, CHECK = 0x50000000, 0x50001000, 0x50002000, 0x60000808, 0x60002000, 0x808C40

def run(name, entries, expected_slot, improvements, limit=100.0, mutant=False, scratch=0xA5):
    u = unicorn.Uc(unicorn.UC_ARCH_X86, unicorn.UC_MODE_64)
    pages = {v & ~4095 for v in list(BODIES) + [HEAD, LIMIT, COOKIE, ACTOR, NODES, OUTPUT, CHECK]}
    pages |= {PRESENCE & ~4095, (PRESENCE + 10*32) & ~4095}
    for page in sorted(pages):
        u.mem_map(page, 4096)
    u.mem_map(0x60000000, 0x3000)
    u.mem_write(0x60000000, bytes([scratch])*0x3000)
    for va, blob in BODIES.items():
        if mutant and va == 0x319850:
            assert blob[0x88:0x8A] == b'\x76\x0E'
            blob = blob[:0x88] + b'\x72' + blob[0x89:]
        u.mem_write(va, blob)
    u.mem_write(COOKIE, struct.pack('<Q', 0x12345678))
    u.mem_write(LIMIT, struct.pack('<f', limit))
    u.mem_write(ACTOR + 0xE0, struct.pack('<4f', 0, 0, 0, 777))
    u.mem_write(HEAD, struct.pack('<Q', NODES if entries else 0))
    for i, (slot, active, xyz) in enumerate(entries):
        node = NODES + i*0x60
        u.mem_write(node, struct.pack('<I', slot))
        u.mem_write(node+4, struct.pack('<I', 0xDEADBEEF))  # node state is not the eligibility test here.
        u.mem_write(node+0x18, struct.pack('<Q', node+0x60 if i+1<len(entries) else 0))
        u.mem_write(PRESENCE+slot*32, bytes([active]))
        u.mem_write(PRESENCE+slot*32+16, struct.pack('<4f', *xyz, 1234))
    initial = bytes([0xCC])*4096
    u.mem_write(OUTPUT, initial)
    monitored = [ACTOR, NODES, PRESENCE & ~4095, (PRESENCE+320) & ~4095, HEAD & ~4095, LIMIT & ~4095]
    snapshots = {p: bytes(u.mem_read(p, 4096)) for p in monitored}
    u.mem_write(STACK, struct.pack('<Q', RETURN))
    u.reg_write(UC_X86_REG_RSP, STACK)
    u.reg_write(UC_X86_REG_RCX, ACTOR)
    u.reg_write(UC_X86_REG_RDX, OUTPUT)
    saved = {UC_X86_REG_RBX: 0x11112222, UC_X86_REG_RBP: 0x33334444,
             UC_X86_REG_RSI: 0x55556666, UC_X86_REG_RDI: 0x77778888, UC_X86_REG_XMM6: 0x123456789ABCDEF}
    for reg, value in saved.items():
        u.reg_write(reg, value)
    visits, calls, writes, cookie_checks = [], [], [], []
    def step(uc, address, size, data):
        visits.append(address)
        if address == RETURN:
            uc.emu_stop()
        elif address == 0x2FB310:
            calls.append(dict(va=address, slot=uc.reg_read(UC_X86_REG_ECX)))
        elif address == 0x3A1960:
            calls.append(dict(va=address, xyz=list(struct.unpack('<3f', uc.mem_read(uc.reg_read(UC_X86_REG_RDX), 12)))))
        elif address == CHECK:
            cookie_checks.append(uc.reg_read(UC_X86_REG_RCX))
            assert cookie_checks[-1] == 0x12345678
            rsp = uc.reg_read(UC_X86_REG_RSP)
            uc.reg_write(UC_X86_REG_RIP, struct.unpack('<Q', uc.mem_read(rsp, 8))[0])
            uc.reg_write(UC_X86_REG_RSP, rsp+8)  # only controlled dependency; preserve return EAX.
    u.hook_add(unicorn.UC_HOOK_CODE, step)
    u.hook_add(unicorn.UC_HOOK_MEM_WRITE, lambda uc, access, address, size, value, data:
               writes.append(dict(address=address, bytes=size, value=value & ((1 << (8*size))-1))) if not 0x60000000 <= address < 0x60003000 else None)
    u.emu_start(0x319850, 0, count=3000)
    assert u.reg_read(UC_X86_REG_RIP) == RETURN and u.reg_read(UC_X86_REG_RSP) == STACK+8
    assert cookie_checks == [0x12345678]
    assert all(u.reg_read(r) == v for r, v in saved.items())
    assert all(bytes(u.mem_read(p, 4096)) == b for p, b in snapshots.items())
    expected = bytearray(initial)
    if expected_slot != -1:
        xyz = next(xyz for slot, active, xyz in entries if slot == expected_slot)
        expected[:16] = struct.pack('<3f', *xyz) + bytes([scratch])*4
    actual = bytes(u.mem_read(OUTPUT, 4096))
    slot = u.reg_read(UC_X86_REG_EAX)
    if slot >= 0x80000000:
        slot -= 0x100000000
    expected_calls = []
    for s, active, xyz in entries:
        expected_calls.append(dict(va=0x2FB310, slot=s))
        if active:
            expected_calls.append(dict(va=0x3A1960, xyz=list(xyz)))
    # NaN records are compared through their source bit encoding, not Python NaN equality.
    call_ok = len(calls) == len(expected_calls) and all(
        a['va'] == b['va'] and (a.get('slot') == b.get('slot')) and
        ('xyz' not in a or struct.pack('<3f', *a['xyz']) == struct.pack('<3f', *b['xyz']))
        for a, b in zip(calls, expected_calls))
    # Unicorn exposes a 16-byte write as two 8-byte hook events.
    expected_writes = []
    for s in improvements:
        xyz = next(xyz for slot_id, active, xyz in entries if slot_id == s)
        payload = struct.pack('<3f', *xyz) + bytes([scratch])*4
        expected_writes += [dict(address=OUTPUT+i, bytes=8, value=struct.unpack_from('<Q', payload, i)[0]) for i in (0, 8)]
    return dict(name=name, matches=slot == expected_slot and actual == bytes(expected) and call_ok and writes == expected_writes,
                slot=slot, expected_slot=expected_slot, output_hex=actual[:16].hex(), calls=calls, writes=writes,
                visited=visits, scratch_byte=scratch, limit=limit, stop='returned', cookie='controlled check passed')

cases = [
    run('empty-list', [], -1, []),
    run('inactive-nearest', [(1, 0, (1, 0, 0)), (9, 1, (3, 0, 0))], 9, [9]),
    run('progressive-improvements', [(8, 1, (8, 0, 0)), (2, 1, (3, 0, 0)), (4, 1, (6, 0, 0))], 2, [8, 2]),
    run('ties-keep-list-first', [(8, 1, (3, 0, 4)), (2, 1, (0, 0, 5))], 8, [8]),
    run('strict-limit', [(0, 1, (10, 0, 0))], -1, []),
    run('outside-limit', [(0, 1, (11, 0, 0))], -1, []),
    run('vertical-distance-ignored', [(9, 1, (1, 10000, 0)), (0, 1, (2, 0, 0))], 9, [9]),
    run('any-nonzero-presence', [(7, 0x80, (2, 0, 0))], 7, [7]),
    run('zero-limit-excludes-coincident', [(0, 1, (0, 0, 0))], -1, [], limit=0),
    run('unordered-distance-skipped', [(0, 1, (float('nan'), 0, 0)), (1, 1, (2, 0, 0))], 1, [1]),
    run('fourth-lane-stack-provenance', [(5, 1, (1, 2, 3))], 5, [5], scratch=0x5A),
]
assert all(c['matches'] for c in cases), [(c['name'], c['matches'], c['writes']) for c in cases]
fault = run('mutant-accepts-equal-distance', [(8, 1, (3, 0, 4)), (2, 1, (0, 0, 5))], 8, [8], mutant=True)
assert not fault['matches'] and fault['slot'] == 2
result = dict(status='PASS', method='three original bodies; synthetic list/presence/threshold; controlled security-cookie dependency',
              exe_sha256=hashlib.sha256(raw).hexdigest(), source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              cases=cases, equal_distance_mutant=fault)
# Encode diagnostic nonfinite operands explicitly; never emit nonstandard JSON NaN.
def safe(value):
    if isinstance(value, float) and value != value:
        return 'NaN'
    if isinstance(value, list):
        return [safe(v) for v in value]
    if isinstance(value, dict):
        return {k: safe(v) for k, v in value.items()}
    return value
(HERE/'result.json').write_text(json.dumps(safe(result), indent=2, allow_nan=False)+'\n')
cs = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
for va, blob in BODIES.items():
    (HERE/f'{va:08X}.bin').write_bytes(blob)
(HERE/'disassembly.txt').write_text('\n'.join(f'{i.address:08X} {i.bytes.hex():24} {i.mnemonic} {i.op_str}'.rstrip()
    for va, blob in BODIES.items() for i in cs.disasm(blob, va))+'\n')
print('PASS: eleven original nearest-pickup cases; equal-distance mutant detected')
