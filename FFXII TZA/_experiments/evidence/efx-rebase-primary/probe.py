"""Bounded offline execution of shipping EFX resolver/rebase instructions.

Reuses the established Unicorn/PE extraction method. Controlled state is injected;
there is no live initialization, resource move, scheduling or native handler proof.
"""
import hashlib
import json
from pathlib import Path
import struct
import sys

sys.path.insert(0, 'Database/Tools/work/ASTRA/python-libs')
import unicorn
from unicorn.x86_const import *

WORK = Path('Database/Tools/work/ASTRA')
EVID = Path('Database/FFXII TZA/_experiments/evidence')
sources = [WORK/'efx-rebase-primary.json', WORK/'efx-rebase-repairs.json',
           EVID/'efx-input-lifetime-flag/retention.json']
catalog = {int(b['address'], 16): b for p in sources
           for b in json.loads(p.read_text())['bodies']}
addresses = (0x3AB7F0, 0x36B130, 0x3B3480, 0x24D970,
             0x3AA3D0, 0x3A9BA0, 0x3A9860, 0x442460, 0x24D940, 0x3A8FF0)
raw = Path(r'D:\SteamLibrary\steamapps\common\FINAL FANTASY XII THE ZODIAC AGE\x64\FFXII_TZA.exe').read_bytes()
sha = hashlib.sha256(raw).hexdigest()
assert sha == '73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
pe = struct.unpack_from('<I', raw, 60)[0]
ib = struct.unpack_from('<Q', raw, pe+48)[0]
assert ib == 0x120000
st = pe+24+struct.unpack_from('<H', raw, pe+20)[0]

def extract(a, n):
    for j in range(struct.unpack_from('<H', raw, pe+6)[0]):
        _, rva, size, disk = struct.unpack_from('<IIII', raw, st+j*40+8)
        d = a-ib-rva
        if 0 <= d and d+n <= size:
            return raw[disk+d:disk+d+n]
    raise ValueError(hex(a))

bodies = {a: extract(a, catalog[a]['bytes']) for a in addresses}
for a, b in bodies.items():
    assert hashlib.sha256(b).hexdigest() == catalog[a]['sha256']
instructions = {int(i['address'], 16) for a in addresses
                for i in catalog[a]['instructions']}
MASK = (1 << 64)-1
SP, STOP = 0x60001808, 0x70000000
CTX, TAB800, TABA00, SLOT = 0x50000000, 0x50002000, 0x50004000, 0x500000
NV = (UC_X86_REG_RBX, UC_X86_REG_RBP, UC_X86_REG_RSI, UC_X86_REG_RDI,
      UC_X86_REG_R12, UC_X86_REG_R13, UC_X86_REG_R14, UC_X86_REG_R15)
ARGS = (UC_X86_REG_RCX, UC_X86_REG_RDX, UC_X86_REG_R8, UC_X86_REG_R9)

def run(name, entry, args, writes, observations):
    u = unicorn.Uc(unicorn.UC_ARCH_X86, unicorn.UC_MODE_64)
    pages = set(range(0x60000000, 0x60003000, 4096))
    for a, data in list(bodies.items())+writes:
        pages.update(range(a & ~4095, (a+len(data)+4095) & ~4095, 4096))
    for a, n in observations:
        pages.update(range(a & ~4095, (a+n+4095) & ~4095, 4096))
    for a in sorted(pages):
        u.mem_map(a, 4096)
    for a, data in bodies.items():
        u.mem_write(a, data)
    for a, data in writes:
        u.mem_write(a, data)
    before = {hex(a): bytes(u.mem_read(a, n)).hex() for a, n in observations}
    saved = {r: 0xA100000000000000+i for i, r in enumerate(NV)}
    saved.update({UC_X86_REG_XMM6+i: 0x123456789ABCDEF0123456789ABCDEF ^ i
                  for i in range(10)})
    for r, v in saved.items():
        u.reg_write(r, v)
    for r, v in zip(ARGS, args):
        u.reg_write(r, v & MASK)
    u.reg_write(UC_X86_REG_RSP, SP)
    u.reg_write(UC_X86_REG_EFLAGS, 2)
    u.reg_write(UC_X86_REG_MXCSR, 0x1F80)
    u.mem_write(SP, struct.pack('<Q', STOP))
    events, calls, visited, invalid = [], [], {}, []

    def code(uc, a, n, _):
        assert a in instructions, 'unexpected instruction '+hex(a)
        visited[hex(a)] = visited.get(hex(a), 0)+1
        if a in bodies:
            calls.append({'event_index': len(events), 'target': hex(a),
                          'args': [hex(uc.reg_read(r)) for r in ARGS]})

    def memory(uc, access, a, n, v, _):
        if 0x60000000 <= a and a+n <= 0x60003000:
            return
        events.append([hex(uc.reg_read(UC_X86_REG_RIP)),
                       'W' if access == unicorn.UC_MEM_WRITE else 'R', hex(a), n,
                       hex(v & ((1 << (n*8))-1)) if access == unicorn.UC_MEM_WRITE
                       else bytes(uc.mem_read(a, n)).hex()])

    def bad(uc, access, a, n, v, _):
        invalid.append([hex(uc.reg_read(UC_X86_REG_RIP)), access, hex(a), n])
        return False

    u.hook_add(unicorn.UC_HOOK_CODE, code)
    u.hook_add(unicorn.UC_HOOK_MEM_READ | unicorn.UC_HOOK_MEM_WRITE, memory)
    u.hook_add(unicorn.UC_HOOK_MEM_INVALID, bad)
    error = None
    try:
        u.emu_start(entry, STOP, count=30000)
    except (unicorn.UcError, AssertionError) as e:
        error = str(e)
    return dict(name=name, entry=hex(entry), args=[hex(v & MASK) for v in args],
                injected_writes=[[hex(a), b.hex()] for a, b in writes],
                before=before, after={hex(a): bytes(u.mem_read(a, n)).hex()
                                     for a, n in observations},
                calls=calls, visited=visited, memory=events, invalid=invalid,
                rax=hex(u.reg_read(UC_X86_REG_RAX)), error=error,
                returned=error is None and u.reg_read(UC_X86_REG_RIP) == STOP,
                stack_ok=u.reg_read(UC_X86_REG_RSP) == SP+8,
                nonvolatile_ok=all(u.reg_read(r) == v for r, v in saved.items()),
                code_unchanged=all(bytes(u.mem_read(a, len(b))) == b
                                   for a, b in bodies.items()))

def q(v):
    return struct.pack('<Q', v & MASK)

out = dict(exe_sha256=sha, unicorn_version=unicorn.__version__, stubs=[],
           source_hashes={str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},
           body_sha256={hex(a): hashlib.sha256(b).hexdigest() for a, b in bodies.items()},
           limits=['Injected slots, globals, contexts, tables and payload bytes; no live initialization.',
                   'Context linked-list head and A00 table entries null; their nonempty handler effects omitted.',
                   '800 subtype9 takes the original direct-return path; other subtype effects omitted.',
                   'No resource moved; changed provider/base values are controlled interventions.',
                   'Instance repair entered directly; caller binding and presentation effects omitted.'], cases=[])
output = WORK/'efx-rebase-result.json'

def bank(c):
    out['cases'].append(c)
    output.write_text(json.dumps(out, indent=2)+'\n', encoding='utf-8')
    assert c['returned'] and c['stack_ok'] and c['nonvolatile_ok'] and c['code_unchanged'] and not c['invalid'], c['name']
    print(c['name'], c['rax'], len(c['memory']), 'events')

# First nonempty slot resolution is the feasibility/readability positive control.
for name, argument, payload, expected in (
        ('provider-positive', SLOT | 3, 0x40002000, 0x40002000),
        ('provider-above2', SLOT | 3, 0x80002000, 0x80002000),
        ('provider-above4', SLOT | 3, 0x180002000, 0x180002000),
        ('provider-low40-rejected', SLOT | 3, 0x100000040, 0),
        ('provider-low41-accepted', SLOT | 3, 0x100000041, 0x100000041),
        ('provider-null', 0, 0, 0),
        ('provider-invalid-small-tag', 0x80003, 0, 0),
        ('provider-unaligned-tag1', SLOT | 1, 0x40002000, 0x40002000),
        ('provider-untagged-full', 0x180002000, 0, 0x180002000)):
    c = run(name, 0x3AB7F0, (argument, 0, 0, 0),
            [(SLOT, bytes(8)+q(payload-0x40))], [(SLOT, 16)])
    c['prediction'] = dict(return_value=hex(expected))
    c['prediction_matches'] = int(c['rax'], 16) == expected
    bank(c)
    assert c['prediction_matches'], name

def context_case(name, old, new, flag=4, raw_source=None):
    delta = (new-old) & 0xFFFFFFFF
    signed_delta = delta if delta < 0x80000000 else delta-(1 << 32)
    ctx = bytearray(0x890)
    ctx[2] = flag
    ctx[0x848:0x850] = q(TAB800)
    ctx[0x850:0x858] = q(TABA00)
    ctx[0x858:0x860] = q(old)
    ctx[0x860:0x864] = struct.pack('<I', SLOT | 3 if raw_source is None else raw_source)
    t = bytearray(0xA00)
    # Entry zero is a nonzero skip control; first and last entries exercise loop bounds.
    t[0:8] = q(old+0x800)
    t[8:16] = q(old+0x100)
    t[-8:] = q(old+0x1000)
    writes = [(CTX, bytes(ctx)), (TAB800, bytes(t)), (TABA00, bytes(0x1800)),
              (SLOT, bytes(8)+q(new-0x40)), (0x2EBEF00, bytes(0x100)),
              (0x2F97000, bytes(0x1000))]
    for offset in (0x100, 0x1000):
        payload = bytearray(0x300)
        payload[0x282] = 9
        writes.append(((old+offset+signed_delta) & MASK, bytes(payload)))
    c = run(name, 0x3B3480, (CTX, 0, 0, 0), writes,
            [(CTX, 0x890), (TAB800, 0xA00), (TABA00, 0x1800),
             (0x2EBEF00, 0x100), (0x2F97000, 0x1000)])
    c['prediction'] = dict(old=hex(old), new=hex(new), delta32=hex(delta),
                           signed_delta=signed_delta, table0=hex(old+0x800),
                           table1=hex((old+0x100+(signed_delta if flag & 4 else 0)) & MASK),
                           table_last=hex((old+0x1000+(signed_delta if flag & 4 else 0)) & MASK),
                           stored_base=hex(new if flag & 4 else old))
    bank(c)

context_case('context-positive-forward', 0x40000000, 0x40002000)
context_case('context-positive-backward', 0x40002000, 0x40000000)
context_case('context-fourGiB-difference', 0x40000000, 0x140000000)
context_case('context-flag-clear', 0x40000000, 0x40002000, flag=0)
# Caller sign-extends the untagged source field; equal base isolates this input boundary.
context_case('context-untagged-above2-sign-extension', 0xFFFFFFFF80002000,
             0xFFFFFFFF80002000, raw_source=0x80002000)

# Direct instance repair: two outer nodes and two nested nodes; no null-field filtering.
INSTANCE, NODE1, NODE2, SUB1, SUB2 = 0x51000000, 0x51001000, 0x51002000, 0x51003000, 0x51004000
instance = bytearray(0x3B0)
instance[0x390:0x398] = q(0x40000000)
node1, node2, sub1, sub2 = bytearray(0x120), bytearray(0x120), bytearray(0x38), bytearray(0x38)
node1[8:16] = q(NODE2)
node1[0x100:0x108] = q(0x40000100)
node1[0x108:0x110] = q(0)
node1[0x118:0x120] = q(SUB1)
node2[0x100:0x108] = q(0x40000200)
node2[0x108:0x110] = q(0x40000300)
sub1[0x18:0x20] = q(0x40000400)
sub1[0x20:0x28] = q(0)
sub1[0x30:0x38] = q(SUB2)
sub2[0x18:0x20] = q(0x40000500)
sub2[0x20:0x28] = q(0x40000600)
control = bytearray(16)
control[8:16] = q(NODE1)
writes = [(INSTANCE, bytes(instance)), (NODE1, bytes(node1)), (NODE2, bytes(node2)),
          (SUB1, bytes(sub1)), (SUB2, bytes(sub2)), (INSTANCE+0x1B8, bytes(control)),
          (0x2EBEF88, q(INSTANCE+0x1B8))]
c = run('instance-direct-negative-delta', 0x24D940, (INSTANCE, 0x3FFFF000, 0, 0),
        writes, [(a, len(b)) for a, b in writes])
c['prediction'] = dict(delta=-0x1000, stored_base='0x3ffff000',
                       field_offsets={'outer': ['0x100', '0x108'], 'inner': ['0x18', '0x20']},
                       zero_fields_become='0xfffffffffffff000', traversal_links_unchanged=True)
bank(c)
assert len(out['cases']) == 15
