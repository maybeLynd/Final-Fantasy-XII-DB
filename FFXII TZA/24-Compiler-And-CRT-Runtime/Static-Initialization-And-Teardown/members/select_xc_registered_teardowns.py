"""select_xc_registered_teardowns.py -- FABLE-REQ-SWE2-EC7-XC-TEARDOWNS-ADDENDUM.

Covers the static TEARDOWN functions the .CRT$XI dynamic-initialiser array
registers with the atexit wrapper 00808B90.  Membership is REGISTRATION-
derived, not form-derived:

    member  <=>  some .CRT$XI array entry (read from the shipping EXE) loads
                 this address into rcx immediately before its call/jump to
                 00808B90
             AND the address is a census function on the frontier
                 (not A-measured, not declared by another family)

The required control travels per member: the TSV records the registering
initializer's address next to every teardown, so 100 % of members are
atexit-registered by a named .CRT$XI site.

The letter follows the paired object, per the request.  Only anchors this
script verifies in the image qualify a group for C:

  C members - the object is provably library / toolchain:

    phre-render-pass-unregister-thunks    12B: lea rcx,[node]; jmp 005DDD60,
                                          the documented render-pass
                                          unregister for the name-keyed
                                          registry at 02CBF998
                                          (22-Middleware-PhyreEngine/
                                          Post-Process-Chain, section 7a).
    phre-render-pass-unregister-inlined   larger bodies: the same unregister
                                          with 005DDD60 inlined; every member
                                          references head 02CBF998 directly.
    crt-noop-static-teardowns             12B: lea rcx,[obj]; jmp 0016D6A0,
                                          the shared ret-0 stub - teardowns
                                          of statics that need none.
    crt-criticalsection-teardowns         14B: lea rcx,[CS]; jmp [IAT] - the
                                          import slot resolves to KERNEL32!
                                          DeleteCriticalSection; paired with
                                          the declared Platform.Windows.
                                          CriticalSection initialisers.
    phyre-module-utility-teardowns        85B: unlink a PUtility node from the
                                          module list headed at 02CACC90;
                                          paired with the declared Phyre
                                          module-utility registrars.
    crt-eh-vector-iterator-teardowns      28/30B: tail-jump the CRT
                                          eh_vector_destructor_iterator
                                          00809054.

  B members - the object owner is NOT proven library (GFZ labels hint at SEAD
  audio, Phyre reflection and render registries for many, but a routing hint
  is not the verification this file performs; the anchors that could not be
  tied to a documented owner - list heads 02E9FD60 / 02E522D0, helpers
  007DF700 / 00680030 / 006D5940 / 00633390 - keep these at B).  The class
  explanation is the registration itself: each row names its registering
  .CRT$XI initialiser and thereby the static object it constructs.

Outputs (in this directory):

  xc-registered-library-teardowns.tsv   the C members above
  xc-registered-static-teardowns.tsv    the B members above

Run:  python select_xc_registered_teardowns.py [--write]
"""

import io, os, re, sys, glob, struct, collections

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..'))
EXE = os.path.join(REPO, 'Database', 'Tools', 'work', 'exe', 'FFXII_TZA.exe')
FUNCS = os.path.join(REPO, 'Database', 'Tools', 'work', 'graph', 'functions.tsv')
DB = os.path.join(REPO, 'Database', 'FFXII TZA')
HERE = os.path.dirname(os.path.abspath(__file__))
ATEXIT = 0x00808B90
ARR_LO, ARR_HI = 0x008C31D0, 0x008C5678

OUT_C = os.path.join(HERE, 'xc-registered-library-teardowns.tsv')
OUT_B = os.path.join(HERE, 'xc-registered-static-teardowns.tsv')
OWN = {os.path.basename(OUT_C), os.path.basename(OUT_B)}

D = io.open(EXE, 'rb').read()
pe = struct.unpack_from('<I', D, 0x3C)[0]
NSEC = struct.unpack_from('<H', D, pe + 6)[0]
OPTSZ = struct.unpack_from('<H', D, pe + 20)[0]
BASE = struct.unpack_from('<Q', D, pe + 48)[0]
SECS = []
for i in range(NSEC):
    o = pe + 24 + OPTSZ + i * 40
    vsz, va, rsz, ptr = struct.unpack_from('<IIII', D, o + 8)
    SECS.append((va, vsz, ptr, rsz))

def foff(va):
    r = va - BASE
    for sva, vsz, ptr, rsz in SECS:
        if sva <= r < sva + rsz:
            return ptr + (r - sva)
    raise KeyError(hex(va))

def body(e):
    return D[foff(e):foff(e) + SIZES[e]]

SIZES = {}
for l in io.open(FUNCS, encoding='utf-8', errors='replace'):
    p = l.split('\t')
    try:
        SIZES[int(p[0], 16)] = int(p[2])
    except (ValueError, IndexError):
        pass

ARR = [q for q in (struct.unpack_from('<Q', D, foff(a))[0]
                   for a in range(ARR_LO, ARR_HI, 8)) if q]

from capstone import Cs, CS_ARCH_X86, CS_MODE_64                  # noqa: E402
from capstone.x86 import (X86_OP_MEM, X86_OP_REG, X86_OP_IMM,     # noqa: E402
                          X86_REG_RIP, X86_REG_RCX)
MD = Cs(CS_ARCH_X86, CS_MODE_64)
MD.detail = True

def teardown_operand(e):
    """The address loaded into rcx just before this entry's atexit transfer."""
    try:
        ins = list(MD.disasm(body(e), e))
    except KeyError:
        return None
    idx = None
    for i, x in enumerate(ins):
        if x.mnemonic in ('call', 'jmp') and x.op_str.startswith('0x') \
                and int(x.op_str, 16) == ATEXIT:
            idx = i
    if idx is None:
        return None
    for x in reversed(ins[:idx + 1]):
        if x.mnemonic == 'lea' and x.operands[0].type == X86_OP_REG \
                and x.operands[0].reg == X86_REG_RCX:
            op = x.operands[1]
            if op.type == X86_OP_MEM and op.mem.base == X86_REG_RIP:
                return x.address + x.size + op.mem.disp
            return None
        if x.mnemonic == 'mov' and x.operands \
                and x.operands[0].reg == X86_REG_RCX:
            return x.operands[1].imm if x.operands[1].type == X86_OP_IMM else None
    return None

PAIRS = {}                       # teardown -> registering array entry
for e in ARR:
    if e in SIZES:
        t = teardown_operand(e)
        if t is not None:
            PAIRS[t] = e
print('initialisers with a decoded rcx teardown operand: %d' % len(PAIRS))

def facts(e):
    calls, tails, refs = set(), set(), set()
    for ins in MD.disasm(body(e), e):
        if ins.op_str.startswith('0x'):
            tg = int(ins.op_str, 16)
            if ins.mnemonic == 'call':
                calls.add(tg)
            elif ins.mnemonic == 'jmp' and not (e <= tg < e + SIZES[e]):
                tails.add(tg)
        for op in ins.operands:
            if op.type == X86_OP_MEM and op.mem.base == X86_REG_RIP:
                refs.add(ins.address + ins.size + op.mem.disp)
    return frozenset(calls), frozenset(tails), frozenset(refs)

# ---- frontier --------------------------------------------------------------
sys.path.insert(0, os.path.join(REPO, 'Database', 'Tools', 'analysis-kit',
                                'gfz-scripts'))
import check_dispositions as CD                     # noqa: E402

RES = CD.evaluate(DB, SIZES)
A_SET, _, _, _ = CD.measure_a(DB, SIZES)
POOL = set(RES['frontier_set'])
for out in (OUT_C, OUT_B):                            # re-run safe
    if os.path.exists(out):
        for l in io.open(out, encoding='utf-8', errors='replace'):
            t = l.split('#')[0].strip().split('\t')[0]
            if re.fullmatch(r'[0-9A-Fa-f]{8}', t):
                POOL.add(int(t, 16))
POOL -= A_SET                        # A always beats a generated declaration

CAND = sorted(t for t in PAIRS if t in POOL and t in SIZES)
print('atexit-registered teardowns on the frontier: %d' % len(CAND))

# ---- letter split -----------------------------------------------------------
RENDER_HEAD = 0x02CBF998     # Phyre render-pass registry (Post-Process-Chain 7a)
RENDER_UNREG = 0x005DDD60    # its documented unregister helper
RET0 = 0x0016D6A0            # shared ret-0 stub
MODULE_HEAD = 0x02CACC90     # PUtility module list (fifteen-modules page)
EHVEC = 0x00809054           # eh_vector_destructor_iterator

# IAT slot -> import name, so the critsec group's indirect tail can be
# verified rather than assumed.
def import_names():
    out = {}
    ddir = pe + 24 + 112
    imp_rva = struct.unpack_from('<I', D, ddir + 8)[0]
    o = foff(BASE + imp_rva)
    while True:
        oft, _ts, _fc, name_rva, ft = struct.unpack_from('<IIIII', D, o)
        if oft == 0 and name_rva == 0 and ft == 0:
            break
        dll = D[foff(BASE + name_rva):].split(b'\0')[0].decode('utf-8',
                                                               'replace')
        src = foff(BASE + (oft or ft))
        k = 0
        while True:
            ent = struct.unpack_from('<Q', D, src + k * 8)[0]
            if ent == 0:
                break
            if not (ent >> 63):
                hn = D[foff(BASE + (ent & 0x7FFFFFFFFFFFFFFF)) + 2:] \
                    .split(b'\0')[0].decode('utf-8', 'replace')
                out[BASE + ft + k * 8] = '%s!%s' % (dll, hn)
            k += 1
        o += 20
    return out

IAT = import_names()

def iat_tail(e):
    """The import name of `jmp qword [rip+x]`, if that is the body's tail."""
    for ins in MD.disasm(body(e), e):
        if ins.mnemonic == 'jmp':
            for op in ins.operands:
                if op.type == X86_OP_MEM and op.mem.base == X86_REG_RIP:
                    return IAT.get(ins.address + ins.size + op.mem.disp)
    return None

F = {t: facts(t) for t in CAND}

def group_of(t):
    c, tl, refs = F[t]
    if SIZES[t] == 12 and tl == frozenset([RENDER_UNREG]):
        return 'phyre-render-pass-unregister-thunks'
    if RENDER_HEAD in refs:
        return 'phyre-render-pass-unregister-inlined'
    if SIZES[t] == 12 and tl == frozenset([RET0]):
        return 'crt-noop-static-teardowns'
    if MODULE_HEAD in refs:
        return 'phyre-module-utility-teardowns'
    if SIZES[t] == 14 and not c and not tl \
            and (iat_tail(t) or '').endswith('DeleteCriticalSection'):
        return 'crt-criticalsection-teardowns'
    if tl == frozenset([EHVEC]):
        return 'crt-eh-vector-iterator-teardowns'
    return None                       # -> B group

C_MEM, B_MEM = [], []
for t in CAND:
    g = group_of(t)
    (C_MEM if g else B_MEM).append((t, g or ''))

print('C (library/toolchain object): %d   B (unproven owner): %d'
      % (len(C_MEM), len(B_MEM)))
print('C groups: %s' % dict(collections.Counter(g for _t, g in C_MEM)))

if '--write' in sys.argv:
    with io.open(OUT_C, 'w', encoding='utf-8', newline='\n') as f:
        f.write('# xc-registered-library-teardowns -- EC-7 family C.\n')
        f.write('# %d teardowns of library/toolchain-owned statics; every row\n'
                % len(C_MEM))
        f.write('# is the rcx operand a .CRT$XI initialiser loads immediately\n')
        f.write('# before its call/jump to the atexit wrapper 00808B90.\n')
        f.write('# select_xc_registered_teardowns.py --write\n')
        f.write('entry\tgroup\tsize\tregistering_init\tcalls\ttail\n')
        for t, g in C_MEM:
            c, tl, _r = F[t]
            f.write('%08X\t%s\t%d\t%08X\t%s\t%s\n'
                    % (t, g, SIZES[t], PAIRS[t],
                       ','.join('%08X' % x for x in sorted(c)) or '-',
                       ','.join('%08X' % x for x in sorted(tl)) or '-'))
    with io.open(OUT_B, 'w', encoding='utf-8', newline='\n') as f:
        f.write('# xc-registered-static-teardowns -- EC-7 family B.\n')
        f.write('# %d atexit-registered teardowns of statics whose owner is\n'
                % len(B_MEM))
        f.write('# not proven library; the class explanation is the\n')
        f.write('# registration itself: each row names the .CRT$XI\n')
        f.write('# initialiser that registers it (and hence the object it\n')
        f.write('# constructs). select_xc_registered_teardowns.py --write\n')
        f.write('entry\tsize\tregistering_init\tcalls\ttail\n')
        for t, _g in B_MEM:
            c, tl, _r = F[t]
            f.write('%08X\t%d\t%08X\t%s\t%s\n'
                    % (t, SIZES[t], PAIRS[t],
                       ','.join('%08X' % x for x in sorted(c)) or '-',
                       ','.join('%08X' % x for x in sorted(tl)) or '-'))
    print('wrote %s (%d) and %s (%d)'
          % (os.path.basename(OUT_C), len(C_MEM),
             os.path.basename(OUT_B), len(B_MEM)))
