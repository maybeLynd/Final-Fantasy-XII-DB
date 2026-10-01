"""EXP-084: the EFX source rebase family under isolated original execution.

Executes the shipped bodies at their real VAs. The contract's own section 13
named this harness: "plant a small arena, record the encoded offsets, rebase to
a second base and check every link - with the two deltas driven separately."

Bodies (all bytes extracted from the authority image, hash-checked):
  0036B130  handle resolver (tagged slot -> [slot+8] + 0x40)
  003AB7F0  resolver wrapper (tag check, truncate, sext(low32) <= 0x40 guard)
  0024D940  rebase object base +0x390 (delta32, walk 003A8FF0)
  0024D970  rebase template base +0x858 (delta32, walks 3AA3D0/3A9BA0/3A9860)
  0024D540  combined path, executed as a SLICE 0024D619..0024D686: the publish
            gate [rbp+2]&4, resolver call, both 64-bit equality guards, all
            four walk invocations and both publishes. The prologue
            (0x2D7FC0/0x3B3D20/0x3A3740/0x3A3A00/0x39D200/0024FCF0) and the loop
            epilogue (0x229EA0/0x24BFD0/0x24B7B0) lie outside the contract's
            claim and are disclosed-not-executed.
  003B3480  the section-1 driver. rdx=0 path fully real; rdx!=0 stubs 0024ED80
            (ret) - that callee only publishes the second object's field
            pointers to globals, disclosed boundary stub; the rebase after it
            is real.
  003A8FF0  repair walk: outer list via [holder+8]; per outer node bumps
            +0x100/+0x108, inner head +0x118 dereferenced, inner nodes +0x18/
            +0x20 bumped, inner next +0x30, outer next +8.
  003A9BA0  repair walk: 768-slot table via [02EBEF78]->holder->base; per
            non-null entry calls 005004C0(entry+delta, delta) then entry+=delta.
  003A9860  repair walk: 320-slot table via [02EBEF90]->holder->base; calls
            00442460(entry+delta, delta) then entry+=delta.
  003AA3D0  repair dispatcher: head = *G_LIST (a pointer); node byte +0x0E ==
            0x52 -> 00501420, == 0x56 -> 00503F10; next = 0020E600([node]).
  00501420  [rcx+0xB0] += sext(delta) when nonzero.
  00503F10  stored u32 arena offset at +0x10: decode, +sext(delta), re-encode.
  005004C0 -> 00538910 -> 00538996: two-level type dispatch; the default arm
            (type > 0xAB after -0x42) is `mov rax,rcx; ret`. Planted slots use
            type 0xD2: real dispatch executed, no per-type interior.
  00442460  type byte +0x282; planted type 9 -> `mov rax,rcx; ret`.
  0020E600/0020E620  the arena codec pair (executed in EXP-083 too).

Injected fixture globals (disclosed, not observed in a live process):
  [01F83530] codec arena base; [02EBEF70] cell holding the 003AA3D0 list head;
  [02EBEF78]/[02EBEF90] cells holding the two table-holder pointers;
  [02EBEF88] cell holding the 003A8FF0 outer-list holder; [02EC32C4]/
  [02EC32CC] the 005004C0 stats gates (zero -> skip); [02F97340] the driver's
  published-context cell.
"""
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
imgbase = struct.unpack_from('<Q', raw, pe + 48)[0]
table = pe + 24 + struct.unpack_from('<H', raw, pe + 20)[0]

def extract(va, size):
    for n in range(struct.unpack_from('<H', raw, pe + 6)[0]):
        _, rva, length, disk = struct.unpack_from('<4I', raw, table + 40 * n + 8)
        if rva <= va - imgbase < rva + length:
            return raw[disk + va - imgbase - rva:disk + va - imgbase - rva + size]
    raise AssertionError(hex(va))

# exact body extents, each ending at its own ret / tail-jump
BODIES = {0x36B130: 0x29, 0x3AB7F0: 0x63, 0x24D940: 0x2F, 0x24D970: 0x49,
          0x24D540: 0x24D6B0 - 0x24D540,
          0x3B3480: 0xC8, 0x3A8FF0: 0x72, 0x3A9BA0: 0x69, 0x3A9860: 0x69,
          0x3AA3D0: 0x5C, 0x501420: 0x1A, 0x503F10: 0x3C,
          0x5004C0: 0x5006B0 - 0x5004C0,   # whole body incl. the 0x5006A9 arm
          0x538910: 0x8A, 0x442460: 0x55,
          0x20E600: 10, 0x20E620: 9}
BODY = {va: extract(va, sz) for va, sz in BODIES.items()}

DEC_BASE = 0x01F83530
G_LIST   = 0x02EBEF70
G_TAB768 = 0x02EBEF78
G_OUTER  = 0x02EBEF88
G_TAB320 = 0x02EBEF90
G_PUBCTX = 0x02F97340
STACK    = 0x60000808
RETURN   = 0x60002000
FX       = 0x30000000
HI       = 0x1_0000_0000
MID      = 0x4000_0000            # page for the nonzero-base terminator case

NONVOL = (UC_X86_REG_RBX, UC_X86_REG_RBP, UC_X86_REG_RSI, UC_X86_REG_RDI,
          UC_X86_REG_R12, UC_X86_REG_R13, UC_X86_REG_R14, UC_X86_REG_R15)
U64 = 0xFFFF_FFFF_FFFF_FFFF

def sext32(v):
    v &= 0xFFFF_FFFF
    return v - 0x1_0000_0000 if v & 0x8000_0000 else v

def mk(base=0, patches=None):
    u = unicorn.Uc(unicorn.UC_ARCH_X86, unicorn.UC_MODE_64)
    for lo, sz in [(0x200000, 0x200000), (0x442000, 0x1000), (0x500000, 0x1000),
                   (0x503000, 0x2000), (0x501000, 0x1000), (0x538000, 0x1000),
                   (0x01F83000, 0x1000), (0x02EBE000, 0x12000),
                   (0x02F97000, 0x1000),
                   (FX, 0x40000), (HI, 0x40000), (MID, 0x1000),
                   (0x60000000, 0x4000)]:
        u.mem_map(lo, sz)
    for va, body in BODY.items():
        b = body
        for off, want, new in (patches or {}).get(va, []):
            assert b[off:off + len(want)] == want, '%X+%X' % (va, off)
            b = b[:off] + new + b[off + len(want):]
        u.mem_write(va, b)
    u.mem_write(DEC_BASE, struct.pack('<Q', base))
    u.mem_write(STACK, struct.pack('<Q', RETURN))
    u.reg_write(UC_X86_REG_RSP, STACK)
    u.reg_write(UC_X86_REG_EFLAGS, 2)
    saved = {r: 0x11000 + r for r in NONVOL}
    for r, v in saved.items():
        u.reg_write(r, v)
    log = dict(reads=[], writes=[], visits=[], invalid=[])
    u.hook_add(unicorn.UC_HOOK_MEM_READ,
               lambda uc, ac, a, n, v, d: log['reads'].append([a, n]))
    u.hook_add(unicorn.UC_HOOK_MEM_WRITE,
               lambda uc, ac, a, n, v, d: log['writes'].append([a, n, v]))
    u.hook_add(unicorn.UC_HOOK_CODE,
               lambda uc, a, n, d: log['visits'].append(a))
    u.hook_add(unicorn.UC_HOOK_MEM_UNMAPPED,
               lambda uc, ac, a, n, v, d: log['invalid'].append([ac, a, n]) or False)
    return u, log, saved

def fixw(log):
    """fixture writes: exclude the stack window."""
    return [w for w in log['writes'] if not 0x60000000 <= w[0] < 0x60004000]

def fixr(log):
    return [r for r in log['reads'] if not 0x60000000 <= r[0] < 0x60004000]

CASES = []

def case(name, entry, args=(), regs=None, setup=None, base=0, patches=None,
         check=None, end=RETURN, note='', cap=300000, nonvol=True,
         may_loop=False):
    CASES.append(dict(name=name, entry=entry, args=args, regs=regs or {},
                      setup=setup, base=base, patches=patches or {},
                      check=check, end=end, note=note, cap=cap, nonvol=nonvol, may_loop=may_loop))

def run(c):
    u, log, saved = mk(c['base'], c['patches'])
    if c['setup']:
        c['setup'](u)
    for reg, val in zip((UC_X86_REG_RCX, UC_X86_REG_RDX, UC_X86_REG_R8), c['args']):
        u.reg_write(reg, val)
    for reg, val in c['regs'].items():
        u.reg_write(reg, val)
    fault = None
    try:
        u.emu_start(c['entry'], c['end'], count=c['cap'])
    except unicorn.UcError as x:
        fault = dict(errno=x.errno, text=str(x), rip=u.reg_read(UC_X86_REG_RIP),
                     invalid=log['invalid'][:])
    obs = dict(rax=u.reg_read(UC_X86_REG_RAX), rip=u.reg_read(UC_X86_REG_RIP),
               reached_end=(fault is None and u.reg_read(UC_X86_REG_RIP) == c['end']),
               returned=(fault is None and c['end'] == RETURN
                         and u.reg_read(UC_X86_REG_RIP) == RETURN
                         and u.reg_read(UC_X86_REG_RSP) == STACK + 8),
               nonvol_ok=all(u.reg_read(r) == v for r, v in saved.items()),
               n_reads=len(fixr(log)), n_writes=len(fixw(log)),
               visits=sorted(set(log['visits'])), fault=fault,
               write_set=sorted({a for a, n, v in fixw(log)}))
    return u, obs, log

def q(u, a):
    return struct.unpack('<Q', u.mem_read(a, 8))[0]

def dw(u, a):
    return struct.unpack('<I', u.mem_read(a, 4))[0]

# ---------------- shared fixture builders ----------------
SLOT  = FX + 0x30000
H     = SLOT | 1                       # tagged handle whose slot is SLOT
N1    = FX + 0x31000
N_A, N_B, N_C = FX + 0x32000, FX + 0x32400, FX + 0x32800
T768  = FX + 0x08000
T320  = FX + 0x0A000
TEMPLATE = FX + 0x37000
OBJ390   = FX + 0x38000
CTX   = FX + 0x3A000
SEC   = FX + 0x3B000
ITEM  = FX + 0x3C000
OLD   = FX + 0x10000
NEW   = FX + 0x14000

def put_slot(u, val64):
    u.mem_write(SLOT + 8, struct.pack('<Q', val64))

def put_outer(u, addr, n100, n108, inner_head, nxt):
    u.mem_write(addr, bytes([0xCC]) * 0x140)
    u.mem_write(addr + 0x100, struct.pack('<Q', n100))
    u.mem_write(addr + 0x108, struct.pack('<Q', n108))
    u.mem_write(addr + 0x118, struct.pack('<Q', inner_head))
    u.mem_write(addr + 8, struct.pack('<Q', nxt))

def put_inner(u, addr, n18, n20, nxt):
    u.mem_write(addr, bytes([0xCC]) * 0x40)
    u.mem_write(addr + 0x18, struct.pack('<Q', n18))
    u.mem_write(addr + 0x20, struct.pack('<Q', n20))
    u.mem_write(addr + 0x30, struct.pack('<Q', nxt))

def put_node(u, addr, typeb, off10=0, b0=0, nextoff=0):
    u.mem_write(addr, bytes([0xCC]) * 0xC0)
    u.mem_write(addr + 0x0E, bytes([typeb]))
    u.mem_write(addr + 0x10, struct.pack('<I', off10 & 0xFFFFFFFF))
    u.mem_write(addr + 0xB0, struct.pack('<Q', b0 & U64))
    u.mem_write(addr + 0, struct.pack('<I', nextoff & 0xFFFFFFFF))

def setup_tables(u, e768=(), e320=()):
    u.mem_write(T768, bytes(0x1800))
    u.mem_write(T320, bytes(0xA00))
    u.mem_write(FX + 0x20000, struct.pack('<Q', T768))
    u.mem_write(FX + 0x20100, struct.pack('<Q', T320))
    u.mem_write(G_TAB768, struct.pack('<Q', FX + 0x20000))
    u.mem_write(G_TAB320, struct.pack('<Q', FX + 0x20100))
    for i, v in e768:
        u.mem_write(T768 + i * 8, struct.pack('<Q', v & U64))
    for i, v in e320:
        u.mem_write(T320 + i * 8, struct.pack('<Q', v & U64))

def setup_outer(u, head):
    u.mem_write(FX + 0x21000, bytes(0x20))
    u.mem_write(FX + 0x21000 + 8, struct.pack('<Q', head))
    u.mem_write(G_OUTER, struct.pack('<Q', FX + 0x21000))

def setup_nodelist(u, head):
    u.mem_write(FX + 0x21100, bytes(0x20))
    u.mem_write(FX + 0x21100, struct.pack('<Q', head))
    u.mem_write(G_LIST, struct.pack('<Q', FX + 0x21100))

def empty_world(u):
    setup_tables(u)
    setup_outer(u, 0)
    setup_nodelist(u, 0)

def full_world(u, base_858=OLD, delta=NEW - OLD):
    """all four walk structures populated relative to base_858."""
    e768 = FX + 0x34000
    e320 = FX + 0x35500
    setup_tables(u, e768=[(5, e768)], e320=[(7, e320)])
    u.mem_write(e768 + delta + 0x44, bytes([0xD2]))    # post-shift object
    u.mem_write(e320 + delta + 0x282, bytes([9]))
    setup_outer(u, FX + 0x22000)
    put_outer(u, FX + 0x22000, base_858 + 0x5000, base_858 + 0x6000,
              FX + 0x23000, 0)
    put_inner(u, FX + 0x23000, base_858 + 0x7000, base_858 + 0x8000, 0)
    setup_nodelist(u, N_A)
    put_node(u, N_A, 0x52, b0=base_858 + 0x9000, nextoff=N_B)
    put_node(u, N_B, 0x56, off10=0x2000, nextoff=0)

# ---------------- resolver + wrapper ----------------
def expect_rax(want, n_r=None, n_w=None):
    def ck(u, obs, log):
        bad = []
        if obs['rax'] != want:
            bad.append('rax=%X want %X' % (obs['rax'], want))
        if n_r is not None and obs['n_reads'] != n_r:
            bad.append('fixture reads=%d want %d' % (obs['n_reads'], n_r))
        if n_w is not None and obs['n_writes'] != n_w:
            bad.append('fixture writes=%d want %d' % (obs['n_writes'], n_w))
        return bad
    return ck

case('res-handle-zero', 0x3AB7F0, (0,), check=expect_rax(0, n_r=0, n_w=0),
     note='handle 0 -> 0; nothing read')
case('res-untagged', 0x3AB7F0, (SLOT,),
     setup=lambda u: put_slot(u, FX + 0x1000),
     check=expect_rax(SLOT, n_w=0),
     note='untagged input returned unchanged - never resolved')
case('res-tagged2', 0x3AB7F0, (SLOT | 2,),
     setup=lambda u: put_slot(u, FX + 0x1000),
     check=expect_rax(FX + 0x1040),
     note='handle low bits 10 also tagged - masked to the slot, resolved')
case('res-below-bound', 0x3AB7F0, (0xFFFFF,),
     check=expect_rax(0, n_w=0),
     note='tagged but < 0x100000 -> resolver 0 -> wrapper guard keeps 0')
case('res-valid', 0x3AB7F0, (H,),
     setup=lambda u: put_slot(u, FX + 0x1000),
     check=expect_rax(FX + 0x1040),
     note='returns [slot+8]+0x40')
case('res-no-generation-read', 0x3AB7F0, (H,),
     setup=lambda u: (put_slot(u, FX + 0x1000), u.mem_write(SLOT + 6, b'\xAA\xAA')),
     check=lambda u, obs, log: (
         [] if obs['rax'] == FX + 0x1040 else ['rax wrong'])
         + ([] if all(not (SLOT + 6 <= a < SLOT + 8) for a, n in fixr(log))
            else ['slot+6 was read - generation check present']),
     note='the resolver reads [slot+8] only; +6 generation word never touched')
case('res-slot-zero', 0x3AB7F0, (H,),
     setup=lambda u: put_slot(u, 0),
     check=expect_rax(0),
     note='null slot -> +0x40 = 0x40 -> sext(0x40) <= 0x40 -> rejected to 0')
case('res-high-4gib-boundary', 0x3AB7F0, (H,),
     setup=lambda u: put_slot(u, HI),
     check=expect_rax(0),
     note='HAZARD EXECUTED: valid base at exactly 4 GiB -> result low32 0x40 '
          '-> sext <= 0x40 -> caller gets 0, pointer silently lost')
case('res-high-wrap-c0', 0x3AB7F0, (H,),
     setup=lambda u: put_slot(u, 0x1_FFFFFFC0),
     check=expect_rax(0),
     note='HAZARD: low32 0xFFFFFFC0 + 0x40 wraps to 0 -> rejected')
case('res-high-wrap-ff', 0x3AB7F0, (H,),
     setup=lambda u: put_slot(u, 0xFFFFFFFF),
     check=expect_rax(0),
     note='HAZARD: low32 0xFFFFFFFF + 0x40 wraps to 0x3F -> rejected')
case('res-neg-low32-kept', 0x3AB7F0, (H,),
     setup=lambda u: put_slot(u, 0x2_80000000),
     check=expect_rax(0x2_80000040),
     note='low32(result) bit31 set -> sext negative -> unsigned huge -> guard '
          'PASSES: valid high bases outside the wrap band survive')

# ---------------- 00501420 / 00503F10 leaf repairs ----------------
case('b0-bump', 0x501420, (N1, 0x400),
     setup=lambda u: put_node(u, N1, 0x52, b0=FX + 0x5000),
     check=lambda u, o, l: [] if q(u, N1 + 0xB0) == FX + 0x5400 else ['+0xB0 wrong'],
     note='[+0xB0] += sext(delta)')
case('b0-negdelta', 0x501420, (N1, 0xFFFFFC00),
     setup=lambda u: put_node(u, N1, 0x52, b0=FX + 0x5000),
     check=lambda u, o, l: [] if q(u, N1 + 0xB0) == FX + 0x4C00 else ['+0xB0 wrong'],
     note='delta -0x400 sign-extends: +0xB0 moves down')
case('b0-null-skipped', 0x501420, (N1, 0x400),
     setup=lambda u: put_node(u, N1, 0x52, b0=0),
     check=lambda u, o, l: [] if q(u, N1 + 0xB0) == 0 and N1 + 0xB0 not in o['write_set']
         else ['null +0xB0 written'],
     note='[+0xB0]==0 -> untouched, not even rewritten')

case('off-valid-delta', 0x503F10, (N1, 0x400),
     setup=lambda u: put_node(u, N1, 0x56, off10=0x2000),
     check=lambda u, o, l: [] if dw(u, N1 + 0x10) == 0x2400 else ['off wrong'],
     note='off 0x2000 + 0x400 -> 0x2400')
case('off-valid-negdelta', 0x503F10, (N1, 0xFFFFFC00),
     setup=lambda u: put_node(u, N1, 0x56, off10=0x2000),
     check=lambda u, o, l: [] if dw(u, N1 + 0x10) == 0x1C00 else ['off wrong'],
     note='delta sign-extends: 0x2000 - 0x400 -> 0x1C00')
case('off-zero-base0', 0x503F10, (N1, 0x400),
     setup=lambda u: put_node(u, N1, 0x56, off10=0),
     check=lambda u, o, l: [] if dw(u, N1 + 0x10) == 0 and N1 + 0x10 not in o['write_set']
         else ['zero offset written'],
     note='base 0: offset 0 decodes to 0 -> skipped, NOT rewritten')
case('off-zero-baseNZ', 0x503F10, (N1, 0x400), base=0x40000000,
     setup=lambda u: put_node(u, N1, 0x56, off10=0),
     check=lambda u, o, l: [] if dw(u, N1 + 0x10) == 0x400 else
         ['stored=%X' % dw(u, N1 + 0x10)],
     note='base!=0: offset 0 decodes to base -> repaired: a 0-offset becomes '
          'the delta (0x400). Null-offset semantics depend on base==0.')
case('off-wrap-past-4gib', 0x503F10, (N1, 0x2000),
     setup=lambda u: put_node(u, N1, 0x56, off10=0xFFFFF000),
     check=lambda u, o, l: [] if dw(u, N1 + 0x10) == 0x1000 else
         ['stored=%X' % dw(u, N1 + 0x10)],
     note='0xFFFFF000 + 0x2000 = 0x1_00001000 -> stored 0x1000: silently '
          're-enters the arena low')
case('off-delta-underflow', 0x503F10, (N1, 0xFFFFFE00),
     setup=lambda u: put_node(u, N1, 0x56, off10=0x100),
     check=lambda u, o, l: [] if dw(u, N1 + 0x10) == 0xFFFFFF00 else
         ['stored=%X' % dw(u, N1 + 0x10)],
     note='off 0x100 - 0x200 -> p below base -> stored 0xFFFFFF00, decodes to '
          'base+0xFFFFFF00 - a wrong-side pointer, no signal')

# ---------------- dispatcher 003AA3D0 ----------------
def list3(u):
    setup_nodelist(u, N_A)
    put_node(u, N_A, 0x52, b0=FX + 0x6000, nextoff=N_B)
    put_node(u, N_B, 0x56, off10=0x2000, nextoff=N_C)
    put_node(u, N_C, 0x99, nextoff=0)

def ck_list3(u, o, l):
    bad = []
    if q(u, N_A + 0xB0) != FX + 0x6400: bad.append('N_A+0xB0 not bumped')
    if dw(u, N_B + 0x10) != 0x2400: bad.append('N_B+0x10 not repaired')
    if N_C + 0x10 in o['write_set'] or N_C + 0xB0 in o['write_set']:
        bad.append('type-0x99 node touched')
    if not o['returned']: bad.append('no clean return')
    return bad

case('disp-two-types-and-skip', 0x3AA3D0, (0x400,), setup=list3, check=ck_list3,
     note='0x52 bumps +0xB0, 0x56 repairs +0x10, 0x99 untouched; offset-0 '
          'terminator decodes to 0 under base 0')

def list3_mid(u):
    """nonzero base: the 'terminator' offset 0 decodes to the base itself.
    Nodes live inside the arena: address = base + stored offset."""
    put_node(u, MID + 0x100, 0x52, b0=MID + 0x500, nextoff=0x200)
    put_node(u, MID + 0x200, 0x56, off10=0x900, nextoff=0x300)
    put_node(u, MID + 0x300, 0x99, nextoff=0)
    put_node(u, MID, 0x99, nextoff=0)      # arena-base object: keeps looping
    setup_nodelist(u, MID + 0x100)

case('disp-nonzero-base-no-terminator', 0x3AA3D0, (0x400,), base=0x40000000,
     setup=list3_mid, cap=20000, nonvol=False, may_loop=True,
     check=lambda u, o, l: [] if (not o['reached_end'] and o['fault'] is None)
         else ['terminated or faulted - terminator DID work: %s' % o['fault']],
     note='base!=0: decode(0)=base -> offset-0 terminator never null -> the '
          'walk re-enters at the arena base forever. Executed: hits the '
          'instruction cap, no fault. A second base-must-be-0 witness.')

# ---------------- table walks ----------------
def table_fixture(delta):
    def st(u):
        setup_tables(u, e768=[(5, FX + 0x34000)], e320=[(7, FX + 0x35500)])
        u.mem_write(FX + 0x34000 + delta + 0x44, bytes([0xD2]))
        u.mem_write(FX + 0x35500 + delta + 0x282, bytes([9]))
    return st

case('walk768-delta-applied', 0x3A9BA0, (0x400,), setup=table_fixture(0x400),
     check=lambda u, o, l: [] if q(u, T768 + 5 * 8) == FX + 0x34400
         and 0x5004C0 in o['visits'] else ['entry or dispatch wrong'],
     note='entry[5] += 0x400; 005004C0 reached with (entry+delta, delta); '
          '767 null slots skipped')
case('walk320-delta-applied', 0x3A9860, (0x400,), setup=table_fixture(0x400),
     check=lambda u, o, l: [] if q(u, T320 + 7 * 8) == FX + 0x35900
         and 0x442460 in o['visits'] else ['entry or dispatch wrong'],
     note='entry[7] += 0x400; 00442460 reached; 319 null slots skipped')
case('walk768-negdelta', 0x3A9BA0, (0xFFFFFC00,), setup=table_fixture(-0x400),
     check=lambda u, o, l: [] if q(u, T768 + 5 * 8) == FX + 0x33C00 else
         ['entry wrong'],
     note='delta -0x400: sign-extended, entry moves down; object read at its '
          'post-shift address')
case('walk8FF0-lists', 0x3A8FF0, (0x400,),
     setup=lambda u: (setup_outer(u, FX + 0x22000),
                      put_outer(u, FX + 0x22000, FX + 0x5000, FX + 0x6000,
                                FX + 0x23000, 0),
                      put_inner(u, FX + 0x23000, FX + 0x7000, FX + 0x8000, 0)),
     check=lambda u, o, l: [] if (
         q(u, FX + 0x22000 + 0x100) == FX + 0x5400
         and q(u, FX + 0x22000 + 0x108) == FX + 0x6400
         and q(u, FX + 0x23000 + 0x18) == FX + 0x7400
         and q(u, FX + 0x23000 + 0x20) == FX + 0x8400) else ['list fields wrong'],
     note='outer +0x100/+0x108 and inner +0x18/+0x20 all += sext(delta)')
case('walk8FF0-negdelta', 0x3A8FF0, (0xFFFFFC00,),
     setup=lambda u: (setup_outer(u, FX + 0x22000),
                      put_outer(u, FX + 0x22000, FX + 0x5000, FX + 0x6000,
                                FX + 0x23000, 0),
                      put_inner(u, FX + 0x23000, FX + 0x7000, FX + 0x8000, 0)),
     check=lambda u, o, l: [] if (
         q(u, FX + 0x22000 + 0x100) == FX + 0x4C00
         and q(u, FX + 0x23000 + 0x18) == FX + 0x6C00) else ['fields wrong'],
     note='negative delta sign-extends through the same path')

# ---------------- standalone rebasers ----------------
def ck_reb858(newbase, delta32):
    s = sext32(delta32)
    def ck(u, o, l):
        bad = []
        if q(u, TEMPLATE + 0x858) != newbase:
            bad.append('+0x858=%X want %X' % (q(u, TEMPLATE + 0x858), newbase))
        if q(u, T768 + 5 * 8) != (FX + 0x34000 + s) & U64:
            bad.append('table768 entry wrong')
        if q(u, T320 + 7 * 8) != (FX + 0x35500 + s) & U64:
            bad.append('table320 entry wrong')
        if q(u, N_A + 0xB0) != (OLD + 0x9000 + s) & U64:
            bad.append('node +0xB0 wrong')
        if dw(u, N_B + 0x10) != (0x2000 + s) & 0xFFFFFFFF:
            bad.append('node +0x10 off wrong')
        for want in (0x3AA3D0, 0x3A9BA0, 0x3A9860):
            if want not in o['visits']:
                bad.append('walk %X not visited' % want)
        return bad
    return ck

case('reb970-exact-small', 0x24D970, (TEMPLATE, NEW),
     setup=lambda u: (full_world(u),
                      u.mem_write(TEMPLATE + 0x858, struct.pack('<Q', OLD))),
     check=ck_reb858(NEW, NEW - OLD),
     note='delta +0x4000: all three walk families shift their links; +0x858 '
          'published as the full new qword')
case('reb970-negdelta', 0x24D970, (TEMPLATE, OLD - 0x400),
     setup=lambda u: (full_world(u, delta=-0x400),
                      u.mem_write(TEMPLATE + 0x858, struct.pack('<Q', OLD))),
     check=ck_reb858(OLD - 0x400, -0x400),
     note='delta -0x400 through the full three-walk path')

def ck_reb390(newbase, delta32):
    s = sext32(delta32)
    def ck(u, o, l):
        bad = []
        if q(u, OBJ390 + 0x390) != newbase:
            bad.append('+0x390 wrong')
        if 0x3A8FF0 not in o['visits']:
            bad.append('003A8FF0 not visited')
        if 0x3AA3D0 in o['visits']:
            bad.append('858 dispatcher wrongly ran')
        return bad
    return ck

case('reb940-exact-small', 0x24D940, (OBJ390, NEW),
     setup=lambda u: (full_world(u),
                      u.mem_write(OBJ390 + 0x390, struct.pack('<Q', OLD))),
     check=ck_reb390(NEW, NEW - OLD),
     note='delta +0x4000: only 003A8FF0 walks; +0x390 published')

# the sharpened boundary: -2 GiB <= delta < +2 GiB, using 003A8FF0 payloads
# (bumped values need not be mapped - they are data, not structure links)
def wide_world(u, old):
    setup_tables(u); setup_outer(u, FX + 0x22000); setup_nodelist(u, 0)
    put_outer(u, FX + 0x22000, old + 0x5000, old + 0x6000, FX + 0x23000, 0)
    put_inner(u, FX + 0x23000, old + 0x7000, old + 0x8000, 0)
    u.mem_write(OBJ390 + 0x390, struct.pack('<Q', old))

case('reb-delta-neg2gib-exact', 0x24D940, (OBJ390, HI + 0x30010000 - 0x80000000),
     setup=lambda u: wide_world(u, HI + 0x30010000),
     check=lambda u, o, l: [] if (
         q(u, FX + 0x22000 + 0x100) == HI + 0x30015000 - 0x80000000
         and q(u, OBJ390 + 0x390) == HI + 0x30010000 - 0x80000000
         and 0x3A8FF0 in o['visits']) else ['boundary -2GiB wrong'],
     note='delta exactly -2^31 (low32 diff 0x80000000 -> sext -2^31): EXACT - '
          'the published base and every link move the same -2 GiB')
case('reb-delta-pos2gib-minus1', 0x24D940, (OBJ390, 0x30010000 + 0x7FFFFFFF),
     setup=lambda u: wide_world(u, 0x30010000),
     check=lambda u, o, l: [] if (
         q(u, FX + 0x22000 + 0x100) == 0x30015000 + 0x7FFFFFFF
         and q(u, OBJ390 + 0x390) == 0x30010000 + 0x7FFFFFFF) else
         ['+2GiB-1 wrong'],
     note='delta +0x7FFFFFFF: exact - the inclusive edge of the signed window')
case('reb-delta-pos2gib-diverges', 0x24D940, (OBJ390, 0x30010000 + 0x80000000),
     setup=lambda u: wide_world(u, 0x30010000),
     check=lambda u, o, l: [] if (
         q(u, FX + 0x22000 + 0x100) == (0x30015000 - 0x80000000) & U64
         and q(u, OBJ390 + 0x390) == 0x30010000 + 0x80000000) else
         ['+2GiB divergence wrong'],
     note='delta +2^31: base published +2 GiB up, links moved -2 GiB down '
          '(0xFFFFFFFFB0015000). SILENT divergence, executed - no signal.')
case('reb-delta-4gib-noop', 0x24D940, (OBJ390, HI + 0x30010000),
     setup=lambda u: wide_world(u, 0x30010000),
     check=lambda u, o, l: [] if (
         q(u, FX + 0x22000 + 0x100) == 0x30015000
         and q(u, OBJ390 + 0x390) == HI + 0x30010000) else ['4GiB noop wrong'],
     note='delta +4 GiB: low32 delta 0 -> every link frozen, base published '
          '4 GiB higher. The §6 ASTRA observation, executed.')

# ---------------- driver 003B3480 ----------------
def driver_world(u, tag4=True, handle=0, off864=0, stored858=None,
                 sec390=None, stub_ed80=False):
    u.mem_write(CTX, bytes(0x880))
    # the rdx=0 publish block re-points the walk globals at these ctx fields:
    #   [02EBEF70] -> &ctx[0x18] (003AA3D0 list head cell)
    #   [02EBEF90] -> &ctx[0x848] (320-table base cell)
    #   [02EBEF78] -> &ctx[0x850] (768-table base cell)
    u.mem_write(CTX + 0x18, struct.pack('<Q', N_A))
    u.mem_write(CTX + 0x848, struct.pack('<Q', T320))
    u.mem_write(CTX + 0x850, struct.pack('<Q', T768))
    if tag4:
        u.mem_write(CTX + 2, bytes([4]))
    if stored858 is not None:
        u.mem_write(CTX + 0x858, struct.pack('<Q', stored858 & U64))
    u.mem_write(CTX + 0x860, struct.pack('<I', handle & 0xFFFFFFFF))
    u.mem_write(CTX + 0x864, struct.pack('<I', off864 & 0xFFFFFFFF))
    if sec390 is not None:
        u.mem_write(SEC, bytes(0x400))
        u.mem_write(SEC + 0x390, struct.pack('<Q', sec390 & U64))
    if stub_ed80:
        u.mem_write(0x24ED80, b'\xC3')   # disclosed boundary stub

case('drv-unpublished-noop', 0x3B3480, (CTX, 0),
     setup=lambda u: driver_world(u, tag4=False),
     check=lambda u, o, l: [] if (o['n_writes'] == 0 and 0x3AB7F0 not in o['visits'])
         else ['gate clear but ran: writes=%d' % o['n_writes']],
     note='bit +2&4 clear: returns at once - no resolver call, no writes')
case('drv-same-base-noop', 0x3B3480, (CTX, 0),
     setup=lambda u: (driver_world(u, handle=H, stored858=FX + 0x1040),
                      put_slot(u, FX + 0x1000), empty_world(u)),
     check=lambda u, o, l: [] if (
         q(u, G_PUBCTX) == CTX and q(u, CTX + 0x858) == FX + 0x1040
         and 0x24D970 not in o['visits'] and 0x3AB7F0 in o['visits']) else
         ['publish or no-op wrong'],
     note='resolved == stored +0x858 -> 64-bit compare equal -> publish ran, '
          'rebase skipped')
case('drv-rebases-858', 0x3B3480, (CTX, 0),
     setup=lambda u: (driver_world(u, handle=H, stored858=OLD),
                      put_slot(u, FX + 0x1000 - 0x40),
                      full_world(u, delta=FX + 0x1000 - OLD)),
     check=lambda u, o, l: [] if (
         q(u, CTX + 0x858) == FX + 0x1000 and 0x24D970 in o['visits']
         and q(u, T768 + 5 * 8) == FX + 0x34000 - OLD + FX + 0x1000) else
         ['driver rebase wrong'],
     note='resolved FX+0x1000 != stored OLD -> 0024D970 runs inside the driver')
case('drv-rdx0-skips-390', 0x3B3480, (CTX, 0),
     setup=lambda u: (driver_world(u, handle=H, stored858=OLD),
                      put_slot(u, FX + 0x1000 - 0x40),
                      full_world(u, delta=FX + 0x1000 - OLD)),
     check=lambda u, o, l: [] if 0x24D940 not in o['visits'] else
         ['+0x390 rebased despite rdx==0'],
     note='rdx==0: the +0x390 branch is guarded by test rdi,rdi - never runs')
case('drv-rdx-390-differs', 0x3B3480, (CTX, SEC),
     setup=lambda u: (driver_world(u, handle=H, stored858=FX + 0x1040,
                                   sec390=OLD, stub_ed80=True),
                      put_slot(u, FX + 0x1000), full_world(u)),
     check=lambda u, o, l: [] if (
         q(u, SEC + 0x390) == FX + 0x1040 and 0x24D940 in o['visits']
         and 0x24D970 not in o['visits']) else ['390 path wrong'],
     note='rdx!=0 (0024ED80 stubbed): +0x858 already equal -> skipped; '
          '+0x390 differs -> 0024D940 runs. The 1+3 split in the driver.')
case('drv-rdx-390-equal', 0x3B3480, (CTX, SEC),
     setup=lambda u: (driver_world(u, handle=H, stored858=FX + 0x1040,
                                   sec390=FX + 0x1040, stub_ed80=True),
                      put_slot(u, FX + 0x1000), empty_world(u)),
     check=lambda u, o, l: [] if (
         0x24D940 not in o['visits'] and 0x24D970 not in o['visits']) else
         ['a walk ran on equal bases'],
     note='rdx!=0, +0x390 already equal -> 64-bit guard skips 0024D940 too')

# ---------------- combined-path slice 0024D619..0024D686 ----------------
SLICE_STOP = {0x24D540: [(0x24D686 - 0x24D540,
                         bytes.fromhex('488b'), bytes.fromhex('ebfe'))]}
SLICE_END = 0x24D686
# disclosed slice terminator: the loop-advance insn at 0024D686 is patched to
# `jmp $`; emu until=0024D686 stops at the TB boundary whether the patch is
# reached by fall-through or by the je branches. The insn is never executed.

def comb_world(u, tag4=4, handle=H, off864=0, stored858=None, item390=None):
    u.mem_write(ITEM, bytes(0x400))
    u.mem_write(ITEM + 0x340, struct.pack('<Q', CTX))
    driver_world(u, tag4=bool(tag4), handle=handle, off864=off864,
                 stored858=stored858)
    if item390 is not None:
        u.mem_write(ITEM + 0x390, struct.pack('<Q', item390 & U64))

case('comb-borrow-clear-skip', 0x24D619, regs={UC_X86_REG_RDI: ITEM}, patches=dict(SLICE_STOP), end=SLICE_END, nonvol=False,
     setup=lambda u: comb_world(u, tag4=0, stored858=OLD),
     check=lambda u, o, l: [] if 0x3AB7F0 not in o['visits'] else
         ['resolver ran despite clear gate'],
     note='context +2&4 clear -> the whole rebase block skipped')
case('comb-identical-858', 0x24D619, regs={UC_X86_REG_RDI: ITEM}, patches=dict(SLICE_STOP), end=SLICE_END, nonvol=False,
     setup=lambda u: (comb_world(u, stored858=FX + 0x1040, item390=FX + 0x1040),
                      put_slot(u, FX + 0x1000), empty_world(u)),
     check=lambda u, o, l: [] if (
         0x3AA3D0 not in o['visits'] and 0x3A9BA0 not in o['visits']
         and 0x3A9860 not in o['visits'] and 0x3A8FF0 not in o['visits']
         and o['reached_end']) else ['a walk ran on identical bases'],
     note='resolved == +0x858 == +0x390: both 64-bit guards skip all four walks')
case('comb-low32-same-high-diff', 0x24D619, regs={UC_X86_REG_RDI: ITEM}, patches=dict(SLICE_STOP), end=SLICE_END, nonvol=False,
     setup=lambda u: (comb_world(u, stored858=HI + 0x30001040,
                                 item390=HI + 0x30001040),
                      put_slot(u, FX + 0x1000), full_world(u, delta=0)),
     check=lambda u, o, l: [] if (
         0x3AA3D0 in o['visits'] and 0x3A8FF0 in o['visits']
         and q(u, CTX + 0x858) == FX + 0x1040
         and q(u, ITEM + 0x390) == FX + 0x1040
         and q(u, FX + 0x22000 + 0x100) == OLD + 0x5000) else
         ['high-diff case wrong'],
     note='low32 equal, high64 differs: the 64-BIT guards fire, all four '
          'walks run with delta32 == 0 (links unchanged), both bases '
          'republished to the low base. Compare-guard is 64-bit, delta 32-bit.')
case('comb-390-differs-only', 0x24D619, regs={UC_X86_REG_RDI: ITEM}, patches=dict(SLICE_STOP), end=SLICE_END, nonvol=False,
     setup=lambda u: (comb_world(u, stored858=FX + 0x1040, item390=OLD),
                      put_slot(u, FX + 0x1000), full_world(u)),
     check=lambda u, o, l: [] if (
         0x3A8FF0 in o['visits'] and 0x3AA3D0 not in o['visits']
         and q(u, ITEM + 0x390) == FX + 0x1040) else ['390-only split wrong'],
     note='+0x858 equal -> three walks skipped; +0x390 differs -> 003A8FF0 '
          'alone runs. The split is per-field, not per-object.')
case('comb-off864-negative', 0x24D619, regs={UC_X86_REG_RDI: ITEM}, patches=dict(SLICE_STOP), end=SLICE_END, nonvol=False,
     setup=lambda u: (comb_world(u, stored858=OLD, off864=0xFFFFFC00,
                                 item390=FX + 0xC00),
                      put_slot(u, FX + 0x1000 - 0x40),
                      full_world(u, delta=FX + 0xC00 - OLD)),
     check=lambda u, o, l: [] if (
         q(u, CTX + 0x858) == FX + 0xC00
         and 0x3AA3D0 in o['visits']
         and 0x3A8FF0 not in o['visits']
         and q(u, ITEM + 0x390) == FX + 0xC00) else
         ['signed +0x864 path wrong'],
     note='+0x864 sign-extends: resolved FX+0x1000 + (-0x400) -> new base '
          'FX+0xC00; the three 858-walks run, +0x390 already equal -> skipped')

# ---------------- mutants ----------------
M = {
 'mut-walk-zeroextend': (0x3A8FF0, 0x3A9000 - 0x3A8FF0,
                         bytes.fromhex('4c63c9'), bytes.fromhex('4189c9')),
 'mut-guard-cmova':     (0x3AB7F0, 0x3AB838 - 0x3AB7F0,
                         bytes.fromhex('480f46c3'), bytes.fromhex('480f47c3')),
 'mut-guard-32bit':     (0x24D540, 0x24D63C - 0x24D540,
                         bytes.fromhex('483bb558080000'),
                         bytes.fromhex('903bb558080000')),
 'mut-off-nullrepair':  (0x503F10, 0x503F2B - 0x503F10,
                         bytes.fromhex('7414'), bytes.fromhex('7514')),
 'mut-tag-mask1':       (0x3AB7F0, 0x3AB803 - 0x3AB7F0,
                         bytes.fromhex('f6c203'), bytes.fromhex('f6c201')),
 'mut-390-skip-flip':   (0x24D540, 0x24D670 - 0x24D540,
                         bytes.fromhex('7414'), bytes.fromhex('7514')),
 'mut-858-skip-flip':   (0x24D540, 0x24D643 - 0x24D540,
                         bytes.fromhex('7424'), bytes.fromhex('7524')),
}

def mutant(name, src_name, patch_key, check, note):
    src = next(c for c in CASES if c['name'] == src_name)
    va, off, want, new = M[patch_key]
    merged = {k: list(v) for k, v in src['patches'].items()}
    merged.setdefault(va, []).append((off, want, new))
    case(name, src['entry'], src['args'], regs=dict(src['regs']),
         setup=src['setup'], base=src['base'], nonvol=src['nonvol'],
         may_loop=src['may_loop'],
         patches=merged, check=check, end=src['end'], cap=src['cap'], note=note)

mutant('mut1-walk-zeroextend-killed', 'walk8FF0-negdelta', 'mut-walk-zeroextend',
       lambda u, o, l: [] if q(u, FX + 0x22000 + 0x100) ==
           (FX + 0x5000 + 0xFFFFFC00) & U64 else ['mutant not expressed'],
       'movsxd->mov r9d: delta -0x400 zero-extends to +0xFFFFFC00; stored '
       'pointer proves the original sign-extends')
mutant('mut2-guard-cmova-killed', 'res-valid', 'mut-guard-cmova',
       lambda u, o, l: [] if o['rax'] == 0 else ['mutant not expressed'],
       'cmovbe->cmova: a valid resolved base is now zeroed')
mutant('mut3-guard-32bit-killed', 'comb-low32-same-high-diff', 'mut-guard-32bit',
       lambda u, o, l: [] if (
           0x3AA3D0 not in o['visits'] and 0x3A8FF0 in o['visits']
           and q(u, CTX + 0x858) == HI + 0x30001040) else
           ['mutant not expressed'],
       'cmp rsi,qword -> cmp esi,dword: equal low32 makes the mutant skip the '
       'three 858-walks AND the publish - the stale high base remains while '
       'the 390 side still rebases down to it')
mutant('mut4-off-nullrepair-killed', 'off-zero-base0', 'mut-off-nullrepair',
       lambda u, o, l: [] if dw(u, N1 + 0x10) == 0x400 else
           ['mutant not expressed'],
       'je->jne on the decode-null guard: offset 0 (decoded null) now gets '
       'repaired and rewritten as the delta - null offsets are destroyed')
mutant('mut5-tag-mask1-killed', 'res-tagged2', 'mut-tag-mask1',
       lambda u, o, l: [] if o['rax'] == (SLOT | 2) else ['mutant not expressed'],
       'test dl,3 -> test dl,1: a low-bits-10 handle passes through raw '
       'instead of resolving to the slot target')
mutant('mut6-390-skip-flip-killed', 'comb-identical-858', 'mut-390-skip-flip',
       lambda u, o, l: [] if 0x3A8FF0 in o['visits'] else
           ['mutant not expressed'],
       'je->jne on the +0x390 guard: identical bases now run 003A8FF0')
mutant('mut7-858-skip-flip-killed', 'comb-identical-858', 'mut-858-skip-flip',
       lambda u, o, l: [] if (0x3AA3D0 in o['visits'] and 0x3A9BA0 in o['visits']
           and 0x3A9860 in o['visits']) else ['mutant not expressed'],
       'je->jne on the +0x858 guard: identical bases now run all three walks')

# ---------------- run ----------------
def main():
    results = []
    nfail = 0
    for c in CASES:
        u, obs, log = run(c)
        bad = c['check'](u, obs, log) if c['check'] else []
        if c['end'] == RETURN and not obs['returned'] and not c['may_loop']:
            bad = bad + ['no clean return: %s' % obs['fault']]
        if c['end'] != RETURN and not obs['reached_end'] and 'nonzero-base' not in c['name']:
            bad = bad + ['slice end not reached: %s' % obs['fault']]
        if c['nonvol'] and not obs['nonvol_ok']:
            bad = bad + ['nonvolatile clobbered']
        if bad:
            nfail += 1
        results.append(dict(name=c['name'], note=c['note'], fail=bad,
                            obs={k: v for k, v in obs.items() if k != 'visits'},
                            visits=[hex(v) for v in obs['visits']]))
        print('%-38s %s %s' % (c['name'], 'FAIL' if bad else 'ok',
                               '; '.join(bad)))
    print('%d cases, %d failing' % (len(results), nfail))
    (HERE / 'result.json').write_text(json.dumps(results, indent=1))
    (HERE / 'bodies.json').write_text(json.dumps(
        {hex(va): dict(size=len(b), sha256=hashlib.sha256(b).hexdigest(),
                       bytes=b.hex())
         for va, b in BODY.items()}, indent=1))

if __name__ == '__main__':
    main()
