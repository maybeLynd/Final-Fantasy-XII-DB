"""EXP-083: resource entry membership tree under isolated original execution.

Executes the shipped bodies, unstubbed, at their real VAs (closed call graph):
  0020E600 offset->pointer decoder (adds [01F83530] as qword)
  0020E620 pointer->offset encoder (subtracts [01F83530] as dword)
  0036B410 insert-entry (rewrites node links to enc(0), owns the empty-root case)
  0036B4E0 insert-walk   (signed key compare at 0036B50D; equal goes right)
  0036B490/0036B5A0     child-replace helpers (parent +0x24 / +0x28 slots)
  0036C790 remove       (root cases; non-root promotes right, reinserts left)
  0036D170 tagged add   (handle ABI, generation check, membership bit +0x15&2)
  0036A000 tagged remove(returns obj+0x40; clears bit; helper leaves links stale)
  003AB880/003AB940     wrappers: (h&3)!=0 -> tagged op, else identity/void

Only globals touched: [01F83530] decoder base (.bss in the image, written here
as an injected fixture value) and the arena-record table [022D7FD0+i*0xA8],
whose +0x50 qword is each tree root.
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

BODIES = {0x20E600: 10, 0x20E620: 9, 0x36A000: 161, 0x36B410: 124,
          0x36B490: 71, 0x36B4E0: 177, 0x36B5A0: 71, 0x36C790: 359,
          0x36D170: 133, 0x3AB880: 42, 0x3AB940: 30}
BODY = {va: extract(va, sz) for va, sz in BODIES.items()}

DEC_BASE   = 0x01F83530          # qword decoder base global (.bss)
TREE_TABLE = 0x022D7FD0          # arena records, 0xA8 bytes each; root at +0x50
STACK      = 0x60000808          # entry RSP, post-call ABI alignment
RETURN     = 0x60002000          # mapped return landing pad
ARENA      = 0x30000000          # synthetic node storage (low pointers)
SLOT       = 0x30004000          # synthetic handle-table slot
RD, WR = unicorn.UC_MEM_READ_UNMAPPED, unicorn.UC_MEM_WRITE_UNMAPPED

def tree_ctx(index):
    return TREE_TABLE + index * 0xA8

def put_node(u, addr, key=0, left=0, right=0, parent=0, f3e=0, f15=0, idx=0,
             gen=0, fill=0xA5):
    u.mem_write(addr, bytes([fill]) * 0x40)
    u.mem_write(addr + 3, bytes([idx]))
    u.mem_write(addr + 0x15, bytes([f15]))
    u.mem_write(addr + 0x18, struct.pack('<i', key))
    u.mem_write(addr + 0x1C, struct.pack('<H', gen))
    u.mem_write(addr + 0x24, struct.pack('<III', left, right, parent))
    u.mem_write(addr + 0x3E, struct.pack('<H', f3e))

def get_node(u, addr):
    left, right, parent = struct.unpack('<III', u.mem_read(addr + 0x24, 12))
    return dict(key=struct.unpack('<i', u.mem_read(addr + 0x18, 4))[0],
                left=left, right=right, parent=parent,
                f15=u.mem_read(addr + 0x15, 1)[0],
                f3e=struct.unpack('<H', u.mem_read(addr + 0x3E, 2))[0])

NONVOL = (UC_X86_REG_RBX, UC_X86_REG_RBP, UC_X86_REG_RSI, UC_X86_REG_RDI,
          UC_X86_REG_R12, UC_X86_REG_R13, UC_X86_REG_R14, UC_X86_REG_R15)

def mk(base=0, patches=None):
    u = unicorn.Uc(unicorn.UC_ARCH_X86, unicorn.UC_MODE_64)
    u.mem_map(0x20E000, 0x1A0000)            # all bodies, real VAs
    u.mem_map(0x01F83000, 0x1000)            # decoder base global
    u.mem_map(0x022D7000, 0x2000)            # arena record table
    u.mem_map(ARENA, 0x10000)                # synthetic nodes/slots
    u.mem_map(0x60000000, 0x3000)            # stack + return pad
    for va, body in BODY.items():
        b = body
        if patches and va in patches:
            off, want, new = patches[va]
            assert b[off:off + len(want)] == want, hex(va + off)
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
               lambda uc, ac, a, n, v, d: log['reads'].append([a, n]),
               begin=0, end=0x5FFFFFFF)
    u.hook_add(unicorn.UC_HOOK_MEM_WRITE,
               lambda uc, ac, a, n, v, d: log['writes'].append([a, n, v]),
               begin=0, end=0x5FFFFFFF)
    u.hook_add(unicorn.UC_HOOK_CODE,
               lambda uc, a, n, d: log['visits'].append(a))
    u.hook_add(unicorn.UC_HOOK_MEM_UNMAPPED,
               lambda uc, ac, a, n, v, d: log['invalid'].append([ac, a, n]) or False)
    return u, log, saved

def run(name, entry, args=(), setup=None, base=0, patches=None,
        expect=None, probe=None, steps=None, note=''):
    u, log, saved = mk(base, patches)
    if setup:
        setup(u)
    seq = steps if steps else [(entry, args)]
    fault = None
    mid = []
    for i, (e, a, *rest) in enumerate(seq):
        for reg, val in zip((UC_X86_REG_RCX, UC_X86_REG_RDX, UC_X86_REG_R8), a):
            u.reg_write(reg, val)
        try:
            u.emu_start(e, RETURN, count=200000)
        except unicorn.UcError as x:
            fault = dict(errno=x.errno, text=str(x), step=i,
                         rip=u.reg_read(UC_X86_REG_RIP),
                         invalid=log['invalid'][:])
            break
        if rest and rest[0]:
            mid.append(rest[0](u))
        if i + 1 < len(seq):
            u.reg_write(UC_X86_REG_RSP, STACK)
            u.mem_write(STACK, struct.pack('<Q', RETURN))
    obs = dict(rax=u.reg_read(UC_X86_REG_RAX),
               returned=(fault is None
                         and u.reg_read(UC_X86_REG_RIP) == RETURN
                         and u.reg_read(UC_X86_REG_RSP) == STACK + 8),
               nonvol_ok=all(u.reg_read(r) == v for r, v in saved.items()),
               fault=fault)
    fails = []
    if expect:
        expect(u, obs, log, fails)
    rec = dict(name=name, entry='0x%X' % entry,
               args=['0x%X' % a for a in args], base='0x%X' % base,
               note=note, observed=obs, mid=mid,
               probe=probe(u) if probe else None, fails=fails,
               reads=log['reads'], writes=log['writes'],
               visited=sorted(set(log['visits'])))
    rec['ok'] = not fails
    return rec

def expect(cond, msg, fails):
    if not cond:
        fails.append(msg)

def e_clean(obs, log, fails, no_writes=False, must_visit=None, not_visit=None):
    expect(obs['returned'], 'no clean return: %s' % obs, fails)
    expect(obs['nonvol_ok'], 'nonvolatile register damage', fails)
    if no_writes:
        expect(log['writes'] == [], 'unexpected writes %s' % log['writes'], fails)
    for a in (must_visit or []):
        expect(a in log['visits'], 'never executed 0x%X' % a, fails)
    for a in (not_visit or []):
        expect(a not in log['visits'], 'unexpectedly executed 0x%X' % a, fails)

def e_fault(obs, fails, kind, addr):
    expect(obs['fault'] is not None, 'expected fault, got clean run', fails)
    if obs['fault']:
        got = [(ac, a) for ac, a, n in obs['fault']['invalid']]
        expect((kind, addr) in got, 'fault %s@%X not in %s' % (kind, addr, got), fails)

cases = []

# == A. codec pair ===========================================================
def codec_pair(ptr, base):
    u, log, saved = mk(base)
    u.reg_write(UC_X86_REG_RCX, ptr)
    u.emu_start(0x20E620, RETURN, count=100)
    enc = u.reg_read(UC_X86_REG_EAX)
    u.reg_write(UC_X86_REG_RCX, enc)
    u.reg_write(UC_X86_REG_RSP, STACK)
    u.mem_write(STACK, struct.pack('<Q', RETURN))
    u.emu_start(0x20E600, RETURN, count=100)
    return enc, u.reg_read(UC_X86_REG_RAX), log

CODEC_PRED = {
    'codec-identity-low':         ('0x30001000', '0x30001000', True),
    'codec-null-zero-base':       ('0x0',        '0x0',        True),
    'codec-above-4gib-alias':     ('0x8000',     '0x8000',     False),
    'codec-nonzero-base-inblock': ('0x8000',     '0x130008000', True),
    'codec-below-base-wrap':      ('0xfffffff8', '0x22ffffff8', False),
    'codec-null-nonzero-base':    ('0xd0000000', '0x200000000', False),
}
for nm, ptr, base in [
    ('codec-identity-low',         0x30001000,   0),
    ('codec-null-zero-base',       0,            0),
    ('codec-above-4gib-alias',     0x100008000,  0),
    ('codec-nonzero-base-inblock', 0x130008000,  0x130000000),
    ('codec-below-base-wrap',      0x12FFFFFF8,  0x130000000),
    ('codec-null-nonzero-base',    0,            0x130000000)]:
    enc, dec, log = codec_pair(ptr, base)
    rt = dec == ptr
    fails = []
    pe_, pd_, prt = CODEC_PRED[nm]
    expect('0x%x' % enc == pe_, 'enc %x != predicted %s' % (enc, pe_), fails)
    expect('0x%x' % dec == pd_, 'dec %x != predicted %s' % (dec, pd_), fails)
    expect(rt == prt, 'round_trip %s != %s' % (rt, prt), fails)
    cases.append(dict(name=nm, entry='codec-pair', args=['0x%X' % ptr],
                      base='0x%X' % base,
                      note='enc=%08X dec=%X' % (enc, dec),
                      observed=dict(enc='0x%08X' % enc, dec='0x%X' % dec,
                                    round_trip=rt),
                      mid=None, probe=None, fails=fails,
                      reads=log['reads'], writes=[],
                      visited=sorted(set(log['visits'])), ok=not fails))

# == B. insert ===============================================================
A, B, C, D = (ARENA + x for x in (0x1000, 0x1100, 0x1200, 0x1300))

def s_empty(u):
    pass

def s_root_a(u):
    put_node(u, A, key=100)
    u.mem_write(tree_ctx(0) + 0x50, struct.pack('<Q', A))

def s_abc(u):
    s_root_a(u)
    put_node(u, B, key=-5, parent=A)
    put_node(u, C, key=200, parent=A)
    u.mem_write(A + 0x24, struct.pack('<I', B))
    u.mem_write(A + 0x28, struct.pack('<I', C))

def s_poisoned_b(u):
    s_root_a(u)
    put_node(u, B, key=-5, left=0xDEADBEEF, right=0xDEADBEEF,
             parent=0xDEADBEEF, f3e=0xBEEF)

def s_high_node(u):
    s_root_a(u)
    u.mem_map(0x100008000, 0x1000)
    put_node(u, 0x100008000, key=50)
    u.mem_map(0x8000, 0x1000)
    put_node(u, 0x8000, key=1000)

def ins(node, ctx=0):
    return (tree_ctx(ctx), node, 0x12DD)

cases.append(run('ins-empty-root', 0x36B410, ins(A),
    lambda u: put_node(u, A, key=100),
    expect=lambda u, o, l, f: (
        e_clean(o, l, f, must_visit=[0x36B457]),
        expect(struct.unpack('<Q', u.mem_read(tree_ctx(0) + 0x50, 8))[0] == A,
               'root not stored as full pointer', f),
        n := get_node(u, A),
        expect(n['left'] == n['right'] == n['parent'] == 0 and n['f3e'] == 0,
               'fresh node links/+3E not cleared: %s' % n, f),
        expect(any(a == tree_ctx(0) + 0x50 and sz == 8 for a, sz, v in l['writes']),
               'root store was not an 8-byte write', f)),
    note='empty tree: root at ctx+0x50 stored as a full qword; links enc(0)=0'))

cases.append(run('ins-left-signed', 0x36B410, ins(B),
    lambda u: (s_root_a(u), put_node(u, B, key=-5)),
    expect=lambda u, o, l, f: (
        e_clean(o, l, f, must_visit=[0x36B543]),
        expect(get_node(u, A)['left'] == B, 'A.left != enc(B)', f),
        expect(get_node(u, B)['parent'] == A, 'B.parent != enc(A)', f),
        expect(get_node(u, A)['right'] == 0, 'A.right touched', f),
        expect(get_node(u, A)['f3e'] == 0 and get_node(u, B)['f3e'] == 0,
               '+3E not cleared at both ends', f)),
    note='key -5 under key 100 must go LEFT (signed jle); unsigned goes right'))

cases.append(run('ins-right', 0x36B410, ins(C),
    lambda u: (s_root_a(u), put_node(u, C, key=200)),
    expect=lambda u, o, l, f: (
        e_clean(o, l, f, must_visit=[0x36B561]),
        expect(get_node(u, A)['right'] == C, 'A.right != enc(C)', f),
        expect(get_node(u, C)['parent'] == A, 'C.parent != enc(A)', f)),
    note='key 200 under key 100 goes right'))

cases.append(run('ins-equal-right', 0x36B410, ins(D),
    lambda u: (s_abc(u), put_node(u, D, key=100)),
    expect=lambda u, o, l, f: (
        e_clean(o, l, f),
        expect(get_node(u, C)['left'] == D,
               'equal key did not pass right of A then left of C', f),
        expect(get_node(u, D)['parent'] == C, 'D.parent != enc(C)', f)),
    note='key 100 equal to A: jle still takes the right arm, then left of C(200)'))

cases.append(run('ins-clears-stale-links', 0x36B410, ins(B), s_poisoned_b,
    expect=lambda u, o, l, f: (
        e_clean(o, l, f),
        n := get_node(u, B),
        expect(n['left'] == 0 and n['right'] == 0 and n['parent'] == A,
               'stale links not rewritten: %s' % n, f),
        expect(n['f3e'] == 0, '+3E not cleared', f)),
    note='0036B410 rewrites all three links with enc(0) before the walk'))

cases.append(run('ins-null-node', 0x36B410, (tree_ctx(0), 0, 0x12DD), s_empty,
    expect=lambda u, o, l, f: e_clean(o, l, f, no_writes=True),
    note='null node returns before touching the tree'))

cases.append(run('ins-null-tree-faults', 0x36B410, (0, A, 0x12DD), s_empty,
    expect=lambda u, o, l, f: e_fault(o, f, RD, 0x50),
    note='ctx=0 insert reads [0x50] for the root -> original fault'))

cases.append(run('ins-nonzero-base-faults', 0x36B410, ins(B), s_empty,
    base=0x30000000,
    steps=[(0x36B410, ins(A),
            lambda u: dict(a_links=struct.unpack('<III', u.mem_read(A + 0x24, 12)))),
           (0x36B410, ins(B))],
    expect=lambda u, o, l, f: e_fault(o, f, RD, 0x100000018),
    note='G=0x30000000: original insert writes A links enc(0)=D0000000, which '
         'decode to 0x1_0000_0000, not null - the second insert descends and '
         'faults reading its key. The tree cannot express an empty child '
         'under any nonzero base.'))

cases.append(run('ins-high-node-silent-alias', 0x36B410, (tree_ctx(0), 0x100008000, 0x12DD),
    s_high_node,
    expect=lambda u, o, l, f: (
        e_clean(o, l, f),
        expect(get_node(u, A)['left'] == 0x8000,
               'A.left != truncated enc(1_0000_8000)=0x8000', f)),
    note='G=0: a node above 4GiB links as its low dword 0x8000 - silent '
         'truncation, no fault at insert time'))

cases.append(run('ins-walk-follows-alias', 0x36B4E0, (A, ARENA + 0x1400, 0x4BF),
    lambda u: (s_high_node(u),
               u.mem_write(A + 0x24, struct.pack('<I', 0x8000)),
               put_node(u, ARENA + 0x1400, key=60)),
    expect=lambda u, o, l, f: (
        e_clean(o, l, f),
        expect(get_node(u, 0x8000)['left'] == ARENA + 0x1400,
               'new node not attached under the WRONG low node 0x8000', f),
        expect(get_node(u, ARENA + 0x1400)['parent'] == 0x8000,
               'new node parent != 0x8000', f)),
    note='walk decodes A.left=0x8000 to the planted wrong node (key 1000) and '
         'inserts key 60 beneath it: silent misdirection, still no fault'))

# == C. remove ===============================================================
P_, N_, L_, R_ = (ARENA + x for x in (0x1500, 0x1600, 0x1700, 0x1800))

def s_root_left_only(u):
    put_node(u, A, key=100)
    put_node(u, B, key=-5, parent=A)
    u.mem_write(A + 0x24, struct.pack('<I', B))
    u.mem_write(tree_ctx(0) + 0x50, struct.pack('<Q', A))

def s_root_right_only(u):
    put_node(u, A, key=100)
    put_node(u, C, key=200, parent=A)
    u.mem_write(A + 0x28, struct.pack('<I', C))
    u.mem_write(tree_ctx(0) + 0x50, struct.pack('<Q', A))

def s_leaf_b(u):
    s_abc(u)

def s_nonroot_left(u):
    put_node(u, P_, key=50)
    put_node(u, N_, key=10, parent=P_, left=L_)
    put_node(u, L_, key=-20, parent=N_)
    u.mem_write(P_ + 0x24, struct.pack('<I', N_))
    u.mem_write(tree_ctx(0) + 0x50, struct.pack('<Q', P_))

def s_nonroot_both(u):
    put_node(u, P_, key=50)
    put_node(u, N_, key=80, parent=P_, left=L_, right=R_)
    put_node(u, L_, key=60, parent=N_)
    put_node(u, R_, key=90, parent=N_)
    u.mem_write(P_ + 0x28, struct.pack('<I', N_))
    u.mem_write(tree_ctx(0) + 0x50, struct.pack('<Q', P_))

def rem(node, ctx=0):
    return (tree_ctx(ctx), node, 0x1263)

cases.append(run('rem-root-empty', 0x36C790, rem(A), s_root_a,
    expect=lambda u, o, l, f: (
        e_clean(o, l, f, must_visit=[0x36C82C]),
        expect(struct.unpack('<Q', u.mem_read(tree_ctx(0) + 0x50, 8))[0] == 0,
               'root not cleared', f)),
    note='removing a lone root writes 0 to ctx+0x50'))

cases.append(run('rem-root-left-only', 0x36C790, rem(A), s_root_left_only,
    expect=lambda u, o, l, f: (
        e_clean(o, l, f, must_visit=[0x36C815]),
        expect(struct.unpack('<Q', u.mem_read(tree_ctx(0) + 0x50, 8))[0] == B,
               'root not replaced by left', f),
        expect(get_node(u, B)['parent'] == 0, 'B.parent not cleared', f)),
    note='root with only a left child: left promoted to root'))

cases.append(run('rem-root-right-only', 0x36C790, rem(A), s_root_right_only,
    expect=lambda u, o, l, f: (
        e_clean(o, l, f, must_visit=[0x36C7E6]),
        expect(struct.unpack('<Q', u.mem_read(tree_ctx(0) + 0x50, 8))[0] == C,
               'root not replaced by right', f),
        expect(get_node(u, C)['parent'] == 0, 'C.parent not cleared', f)),
    note='root with only a right child: right promoted to root'))

cases.append(run('rem-root-both-reinserts-left', 0x36C790, rem(A), s_abc,
    expect=lambda u, o, l, f: (
        e_clean(o, l, f, must_visit=[0x36C804, 0x36B543]),
        expect(struct.unpack('<Q', u.mem_read(tree_ctx(0) + 0x50, 8))[0] == C,
               'right not promoted to root', f),
        expect(get_node(u, C)['parent'] == 0, 'C.parent not cleared', f),
        expect(get_node(u, C)['left'] == B, 'left subtree not reinserted', f),
        expect(get_node(u, B)['parent'] == C, 'B.parent not reseated to C', f)),
    note='executes the rebalance the contract left underived: root removal '
         'promotes right, then re-inserts the whole left subtree via 0036B4E0'))

cases.append(run('rem-leaf-stale-parent', 0x36C790, rem(B), s_leaf_b,
    expect=lambda u, o, l, f: (
        e_clean(o, l, f, must_visit=[0x36B490]),
        expect(get_node(u, A)['left'] == 0, 'parent slot not cleared', f),
        expect(get_node(u, B)['parent'] == A,
               'removed leaf parent link was rewritten', f),
        expect(not any(a == B + 0x24 or a == B + 0x28 or a == B + 0x2C
                       for a, n, v in l['writes']),
               'helper wrote the removed node links', f)),
    note='executed check of the carried claim: the standalone remove leaves '
         'the removed node\'s own links stale (parent still points at A)'))

cases.append(run('rem-nonroot-left-only', 0x36C790, rem(N_), s_nonroot_left,
    expect=lambda u, o, l, f: (
        e_clean(o, l, f, must_visit=[0x36B490]),
        expect(get_node(u, P_)['left'] == L_,
               'left subtree not spliced into parent left slot', f),
        expect(get_node(u, L_)['parent'] == P_,
               'L.parent not reseated to P', f)),
    note='non-root without right child: 0036B490 splices the left subtree '
         'into the parent slot that held the node'))

cases.append(run('rem-nonroot-both-promotes-right', 0x36C790, rem(N_), s_nonroot_both,
    expect=lambda u, o, l, f: (
        e_clean(o, l, f, must_visit=[0x36C848, 0x36C889]),
        expect(get_node(u, P_)['right'] == R_,
               'right child not promoted into parent slot', f),
        expect(get_node(u, R_)['parent'] == P_, 'R.parent not reseated', f),
        expect(get_node(u, R_)['left'] == L_,
               'left subtree not reinserted under promoted right', f),
        expect(get_node(u, L_)['parent'] == R_, 'L.parent not reseated', f),
        n := get_node(u, N_),
        expect(n['left'] == L_ and n['right'] == R_ and n['parent'] == P_,
               'removed node links were rewritten: %s' % n, f)),
    note='non-root with both children: right promoted into the parent slot, '
         'left reinserted under it; removed node keeps its stale links'))

cases.append(run('rem-null-node', 0x36C790, (tree_ctx(0), 0, 0x1263), s_empty,
    expect=lambda u, o, l, f: e_clean(o, l, f, no_writes=True),
    note='null node returns immediately'))

cases.append(run('rem-null-tree-nonroot-ok', 0x36C790, (0, N_, 0x1263), s_nonroot_left,
    expect=lambda u, o, l, f: (
        e_clean(o, l, f, must_visit=[0x36B490]),
        expect(get_node(u, P_)['left'] == L_, 'splice failed', f),
        expect(not any(a < 0x1000 for a, n, v in l['writes']),
               'write near null ctx: %s' % l['writes'], f)),
    note='ctx is only the root holder: non-root removal never dereferences it'))

cases.append(run('rem-null-tree-root-faults', 0x36C790, (0, A, 0x1263), s_root_left_only,
    expect=lambda u, o, l, f: e_fault(o, f, WR, 0x50),
    note='removing a root with ctx=0 faults writing the new root to [0x50]'))

# == D. tagged add/remove ====================================================
OBJ = ARENA + 0x2000

def s_slot(u, gen=5, obj=OBJ):
    u.mem_write(SLOT, b'\0' * 0x20)
    u.mem_write(SLOT + 6, struct.pack('<H', gen))
    u.mem_write(SLOT + 8, struct.pack('<Q', obj))

def s_obj(u, key=42, idx=2, gen=5, f15=0):
    put_node(u, OBJ, key=key, idx=idx, gen=gen, f15=f15)

def s_member_obj(u):
    s_slot(u); s_obj(u, f15=2)

def s_member_tree(u):
    s_member_obj(u)
    u.mem_write(tree_ctx(2) + 0x50, struct.pack('<Q', OBJ))

cases.append(run('tag-add-valid', 0x36D170, (SLOT | 1,),
    lambda u: (s_slot(u), s_obj(u)),
    expect=lambda u, o, l, f: (
        e_clean(o, l, f, must_visit=[0x36B410]),
        expect(struct.unpack('<Q', u.mem_read(tree_ctx(2) + 0x50, 8))[0] == OBJ,
               'not inserted into arena[2] tree', f),
        n := get_node(u, OBJ),
        expect(n['f15'] & 2, 'membership bit not set', f),
        expect(n['f3e'] == 0, '+3E not cleared', f)),
    note='handle slot|1, gen match, not member: inserts into the tree selected '
         'by obj+3, sets +0x15 bit 1, clears +0x3E'))

cases.append(run('tag-add-already-member', 0x36D170, (SLOT | 1,), s_member_obj,
    expect=lambda u, o, l, f: e_clean(o, l, f, no_writes=True,
                                      not_visit=[0x36B410]),
    note='membership bit already set: no call, no writes (idempotent add)'))

cases.append(run('tag-add-gen-mismatch', 0x36D170, (SLOT | 1,),
    lambda u: (s_slot(u, gen=5), s_obj(u, gen=9)),
    expect=lambda u, o, l, f: e_clean(o, l, f, no_writes=True,
                                      not_visit=[0x36B410]),
    note='word[slot+6] != word[obj+0x1C]: refused before the membership test'))

for nm, h in [('tag-add-null-handle', 0), ('tag-add-untagged', SLOT),
              ('tag-add-small-handle', 0xFFFD)]:
    cases.append(run(nm, 0x36D170, (h,), lambda u: (s_slot(u), s_obj(u)),
        expect=lambda u, o, l, f: e_clean(o, l, f, no_writes=True,
                                          not_visit=[0x36B410]),
        note='handle gate refuses before any write'))

cases.append(run('tag-add-null-obj-faults', 0x36D170, (SLOT | 1,),
    lambda u: s_slot(u, obj=0),
    expect=lambda u, o, l, f: e_fault(o, f, RD, 0x1C),
    note='UNLIKE remove, add has no null-object check: slot+8=0 faults reading '
         'the generation at [0x1C]'))

cases.append(run('tag-add-index-overflow-faults', 0x36D170, (SLOT | 1,),
    lambda u: (s_slot(u), s_obj(u, idx=0x10)),
    expect=lambda u, o, l, f: e_fault(o, f, RD, 0x50),
    note='obj+3 >= 0xF -> ctx=0 -> insert reads [0x50]; the table boundary is '
         'observed as an original fault'))

cases.append(run('tag-remove-valid', 0x36A000, (SLOT | 1,), s_member_tree,
    expect=lambda u, o, l, f: (
        e_clean(o, l, f, must_visit=[0x36C790]),
        expect(o['rax'] == OBJ + 0x40, 'return != obj+0x40', f),
        expect(struct.unpack('<Q', u.mem_read(tree_ctx(2) + 0x50, 8))[0] == 0,
               'root not cleared', f),
        expect(not (get_node(u, OBJ)['f15'] & 2), 'membership bit not cleared', f)),
    note='member remove: tree removal runs, +0x15 bit 1 cleared, returns '
         'obj+0x40'))

cases.append(run('tag-remove-not-member', 0x36A000, (SLOT | 1,),
    lambda u: (s_slot(u), s_obj(u, f15=0)),
    expect=lambda u, o, l, f: (
        e_clean(o, l, f, no_writes=True, not_visit=[0x36C790]),
        expect(o['rax'] == OBJ + 0x40,
               'non-member still returns obj+0x40 (got %X)' % o['rax'], f)),
    note='NOT a member: skips the helper and the bit clear, still returns '
         'obj+0x40'))

cases.append(run('tag-remove-gen-mismatch', 0x36A000, (SLOT | 1,),
    lambda u: (s_slot(u, gen=5), s_obj(u, gen=9, f15=2)),
    expect=lambda u, o, l, f: (
        e_clean(o, l, f, no_writes=True, not_visit=[0x36C790]),
        expect(o['rax'] == 0, 'expected 0 return', f)),
    note='generation mismatch: returns 0, object untouched'))

cases.append(run('tag-remove-null-obj', 0x36A000, (SLOT | 1,),
    lambda u: s_slot(u, obj=0),
    expect=lambda u, o, l, f: (
        e_clean(o, l, f, no_writes=True, not_visit=[0x36C790]),
        expect(o['rax'] == 0, 'expected 0 return', f)),
    note='remove DOES check slot+8 for null - the asymmetry with add'))

# == E. wrappers =============================================================
cases.append(run('wrap-add-null', 0x3AB940, (0,),
    lambda u: (s_slot(u), s_obj(u)),
    expect=lambda u, o, l, f: e_clean(o, l, f, no_writes=True,
                                      not_visit=[0x36D170]),
    note='003AB940(0): returns without calling the tagged add'))

cases.append(run('wrap-add-untagged', 0x3AB940, (SLOT,),
    lambda u: (s_slot(u), s_obj(u)),
    expect=lambda u, o, l, f: e_clean(o, l, f, no_writes=True,
                                      not_visit=[0x36D170]),
    note='h&3==0: returns without the tagged add'))

cases.append(run('wrap-add-tagged', 0x3AB940, (SLOT | 1,),
    lambda u: (s_slot(u), s_obj(u)),
    expect=lambda u, o, l, f: (
        e_clean(o, l, f, must_visit=[0x36D170, 0x36B410]),
        expect(get_node(u, OBJ)['f15'] & 2, 'add did not run', f)),
    note='h&3!=0 tail-jumps into 0036D170'))

cases.append(run('wrap-remove-null', 0x3AB880, (0,), s_member_obj,
    expect=lambda u, o, l, f: (
        e_clean(o, l, f, no_writes=True, not_visit=[0x36A000]),
        expect(o['rax'] == 0, 'null handle must return 0', f)),
    note='003AB880(0): returns 0'))

cases.append(run('wrap-remove-untagged-identity', 0x3AB880, (SLOT,), s_member_obj,
    expect=lambda u, o, l, f: (
        e_clean(o, l, f, no_writes=True, not_visit=[0x36A000]),
        expect(o['rax'] == SLOT, 'untagged must return the handle itself', f)),
    note='h&3==0: returns the input handle unchanged, no call'))

cases.append(run('wrap-remove-tag2-tagged', 0x3AB880, (SLOT | 2,), s_member_tree,
    expect=lambda u, o, l, f: (
        e_clean(o, l, f, must_visit=[0x36A000, 0x36C790]),
        expect(o['rax'] == OBJ + 0x40, 'expected obj+0x40', f)),
    note='h=slot|2 (h&3==2, h&1==0): still dispatched as tagged'))

cases.append(run('wrap-remove-tagged', 0x3AB880, (SLOT | 1,), s_member_tree,
    expect=lambda u, o, l, f: (
        e_clean(o, l, f, must_visit=[0x36A000, 0x36C790]),
        expect(o['rax'] == OBJ + 0x40, 'expected obj+0x40', f)),
    note='h&3!=0 tail-jumps into 0036A000'))

# == F. mutants: each must be caught by its discriminating case ==============
def mut(name, va, off, want, new, spec, detect, why):
    r = run(name, spec['entry'], spec['args'], spec['setup'],
            patches={va: (off, want, new)}, probe=spec.get('probe'),
            note=why)
    r['detected'] = detect(r)
    return r

mutants = [
    mut('mut-unsigned-order', 0x36B4E0, 0x36B50D - 0x36B4E0,
        bytes.fromhex('7e1a'), bytes.fromhex('761a'),
        dict(entry=0x36B410, args=ins(B),
             setup=lambda u: (s_root_a(u), put_node(u, B, key=-5)),
             probe=lambda u: dict(a_left=get_node(u, A)['left'],
                                  a_right=get_node(u, A)['right'])),
        lambda r: r['probe'] and r['probe']['a_right'] == B,
        'jle->jbe at 0036B50D: unsigned compare sends key -5 RIGHT'),
    mut('mut-equal-left', 0x36B4E0, 0x36B50D - 0x36B4E0,
        bytes.fromhex('7e1a'), bytes.fromhex('7c1a'),
        dict(entry=0x36B410, args=ins(D),
             setup=lambda u: (s_abc(u), put_node(u, D, key=100)),
             probe=lambda u: dict(b_right=get_node(u, B)['right'],
                                  c_left=get_node(u, C)['left'])),
        lambda r: r['probe'] and r['probe']['b_right'] == D
                  and r['probe']['c_left'] == 0,
        'jle->jl at 0036B50D: equal key now goes LEFT'),
    mut('mut-member-mask4', 0x36D170, 0x36D1A7 - 0x36D170,
        bytes.fromhex('02'), bytes.fromhex('04'),
        dict(entry=0x36D170, args=(SLOT | 1,), setup=s_member_obj),
        lambda r: 0x36B410 in r['visited'] or bool(r['writes']),
        'test byte [rbx+0x15] mask 2->4: a member inserts a second time'),
    mut('mut-remove-root-flip', 0x36C790, 0x36C7DD - 0x36C790,
        bytes.fromhex('7558'), bytes.fromhex('7458'),
        dict(entry=0x36C790, args=rem(B), setup=s_leaf_b,
             probe=lambda u: dict(a_left=get_node(u, A)['left'])),
        lambda r: any(a == tree_ctx(0) + 0x50 for a, n, v in r['writes'])
                  or (r['probe'] and r['probe']['a_left'] != 0),
        'jne->je at 0036C7DD: non-root removal takes the root path and '
        'clears the tree root'),
    mut('mut-wrapper-mask1', 0x3AB880, 0x3AB88B - 0x3AB880,
        bytes.fromhex('f6c203'), bytes.fromhex('f6c201'),
        dict(entry=0x3AB880, args=(SLOT | 2,), setup=s_member_tree),
        lambda r: r['observed']['rax'] == (SLOT | 2)
                  and 0x36A000 not in r['visited'],
        'test dl,3 -> test dl,1: handle slot|2 wrongly reads untagged'),
]

result = dict(
    status='PASS' if (all(c['ok'] for c in cases)
                      and all(m['detected'] for m in mutants)) else 'FAIL',
    method='isolated original-code execution, Unicorn 2.1.4, no stubs',
    live_game=False,
    exe_sha256=hashlib.sha256(raw).hexdigest(),
    source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    bodies=[dict(address='0x%X' % va, bytes=len(b),
                 sha256=hashlib.sha256(b).hexdigest())
            for va, b in sorted(BODY.items())],
    cases=cases, mutants=mutants)
(HERE / 'result.json').write_text(json.dumps(result, indent=2) + '\n')
(HERE / 'bodies.json').write_text(json.dumps(
    {'0x%X' % va: b.hex() for va, b in sorted(BODY.items())}, indent=1) + '\n')
cs = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
(HERE / 'disassembly.txt').write_text('\n'.join(
    '%08X  %s' % (va, '\n'.join(
        ('         %08X %-24s %s %s' % (
            i.address, i.bytes.hex(), i.mnemonic, i.op_str)).rstrip()
        for i in cs.disasm(b, va)))
    for va, b in sorted(BODY.items())) + '\n')
bad = [c['name'] for c in cases if not c['ok']]
undetected = [m['name'] for m in mutants if not m['detected']]
print('%s: %d cases, %d mutants detected; bad=%s undetected=%s' %
      (result['status'], len(cases), len(mutants) - len(undetected), bad, undetected))
