"""select_verb_adapters.py -- FABLE-REQ-SWE2-EC7-VERB-ADAPTER-FAMILY.

Selects the pure script-verb adapter callbacks: functions the ScriptVM verb
tables register whose decoded body only pops operands, calls at most one
native, and writes / pushes the result -- no loop, no second native.

Membership rule:

    member  <=>  address appears as begin (+0x00), poll (+0x08) or result
                 (+0x18) in a record of one of the five verb tables, read
                 from the shipping EXE (never from a TSV)
             AND every decoded direct call / external tail-jump target is
                 either a VM helper, the toolchain epilogue, or ONE shared
                 native (the single non-helper target; a body whose only
                 non-helper site is `call/jmp _guard_check_icall` counts the
                 guarded indirect call as that one native)
             AND no decoded branch or jump targets an earlier address in the
                 same body (no loop)
             AND no indirect call/jump remains unexplained (a `call rax`
                 outside the guard pattern rejects)
             AND the function is on the current frontier (not A-measured,
                 not declared by another family)

The five tables and the record layout are the ones
`VMNativeCommandDispatch_InitializeFamilyTables` (003DC2D0) installs and the
three accessors (003DC240 / 003DC270 / 003DC2A0) read:

    table + 0x00   s32   command count
    record N = table + 8 + 32*N:   +0x00 begin   +0x08 poll
                                   +0x10 unused  +0x18 result

    0x01EED700  family 0        1,496 commands
    0x01F281B0  family 3          147 commands
    0x01F29418  family 5            1 command
    0x01F29440  family 7          104 commands
    0x01F26720  default (fam 2)   212 commands, shared by twelve families

Allowed helper targets (the operand / result primitives, all named in the
census): 00267DB0 VMValueStack_PopNumericDiscard, 00267E10
VMValueStack_PopInt32CoerceFloat32, 00267F60 VMValueStack_PushFloat32Bits,
00267F90 VMValueStack_PushInt32, 0026B4C0 VMResult_WriteFloat32,
0026B4E0 VMResult_WriteInt32 -- plus 00808C40 __security_check_cookie, the
/GS epilogue (toolchain, not a native), and 0016D6A0 _guard_check_icall only
when it is the body's single non-helper site (the guarded indirect call IS
the native call; recorded as `indirect` in the native column).

Outputs (in this directory):

  scriptvm-verb-adapter-callbacks.tsv   one row per member:
                                        address, family (verb family index),
                                        verb_id, verb_name, role,
                                        native_callee; a callback shared by
                                        several slots lists them all.
  scriptvm-verb-adapter-leftovers.tsv   frontier callbacks that fail the
                                        predicate, with the reason
                                        (multi-native(N) / loop / indirect).

Verb ids / names are joined from scriptvm-verb-table.tsv by call_id --
explanation columns only; membership never consults them.

Run:  python select_verb_adapters.py [--write]
"""

import csv, io, os, re, sys, glob, struct, collections

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..'))
EXE = os.path.join(REPO, 'Database', 'Tools', 'work', 'exe', 'FFXII_TZA.exe')
FUNCS = os.path.join(REPO, 'Database', 'Tools', 'work', 'graph', 'functions.tsv')
DB = os.path.join(REPO, 'Database', 'FFXII TZA')
HERE = os.path.dirname(os.path.abspath(__file__))
VTAB = os.path.join(HERE, '..', 'scriptvm-verb-table.tsv')
OUT = os.path.join(HERE, 'scriptvm-verb-adapter-callbacks.tsv')
LEFTOVER = os.path.join(HERE, 'scriptvm-verb-adapter-leftovers.tsv')

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

SIZES = {}
for l in io.open(FUNCS, encoding='utf-8', errors='replace'):
    p = l.split('\t')
    try:
        SIZES[int(p[0], 16)] = int(p[2])
    except (ValueError, IndexError):
        pass

# ---- the five verb tables, read from the image ---------------------------
TABLES = [(0x01EED700, 0), (0x01F281B0, 3), (0x01F29418, 5),
          (0x01F29440, 7), (0x01F26720, 2)]
CB = collections.defaultdict(list)          # addr -> [(call_id, role)]
for base, fam in TABLES:
    cnt = struct.unpack_from('<i', D, foff(base))[0]
    for i in range(cnt):
        rec = base + 8 + 32 * i
        for off, role in ((0, 'begin'), (8, 'poll'), (0x18, 'result')):
            q = struct.unpack_from('<Q', D, foff(rec + off))[0]
            if q:
                CB[q].append((fam << 12 | i, role))
print('table records read from image: %d distinct callbacks' % len(CB))

VERBS = {}
for row in csv.DictReader(io.open(VTAB, encoding='utf-8'), delimiter='\t'):
    VERBS[int(row['call_id'], 16)] = row['verb']

# ---- body facts (decoded, never byte-scanned) ------------------------------
from capstone import Cs, CS_ARCH_X86, CS_MODE_64                  # noqa: E402
MD = Cs(CS_ARCH_X86, CS_MODE_64)

HELP = {0x00267DB0, 0x00267E10, 0x00267F60, 0x00267F90,
        0x0026B4C0, 0x0026B4E0,          # VMValueStack_/VMResult_ primitives
        0x00808C40}                      # __security_check_cookie (toolchain)
GUARD = 0x0016D6A0                       # _guard_check_icall

def classify(e):
    """('adapter', native|None|'indirect') or ('reject', reason)."""
    calls, tails, loop, ind = set(), set(), False, False
    for ins in MD.disasm(D[foff(e):foff(e) + SIZES[e]], e):
        tgt = int(ins.op_str, 16) if ins.op_str.startswith('0x') else None
        if ins.mnemonic == 'call':
            if tgt is None:
                ind = True
            else:
                calls.add(tgt)
        elif ins.mnemonic == 'jmp':
            if tgt is None:
                ind = True
            elif not (e <= tgt < e + SIZES[e]):
                tails.add(tgt)
            elif tgt < ins.address:
                loop = True
        elif ins.mnemonic.startswith('j') and tgt is not None \
                and tgt < ins.address:
            loop = True
    natives = (calls | tails) - HELP
    guarded = natives == {GUARD}
    if guarded:
        natives = set()
    if ind:
        return 'reject', 'indirect'
    if loop:
        return 'reject', 'loop'
    if len(natives) > 1:
        return 'reject', 'multi-native(%d)' % len(natives)
    if natives:
        return 'adapter', '%08X' % next(iter(natives))
    return 'adapter', 'indirect' if guarded else 'none'

# ---- frontier --------------------------------------------------------------
sys.path.insert(0, os.path.join(REPO, 'Database', 'Tools', 'analysis-kit',
                                'gfz-scripts'))
import check_dispositions as CD                     # noqa: E402

RES = CD.evaluate(DB, SIZES)
POOL = set(RES['frontier_set'])
A_SET = set(CD.measure_a(DB, SIZES)[0])
# re-run safe: members this family's own TSV declared last time re-enter the pool
# UNLESS since measured A - A beats a declaration (the checker's refusal cure)
if os.path.exists(OUT):
    for l in io.open(OUT, encoding='utf-8', errors='replace'):
        t = l.split('\t')[0].strip()
        if re.fullmatch(r'[0-9A-Fa-f]{8}', t) and int(t, 16) not in A_SET:
            POOL.add(int(t, 16))

members, leftovers = [], []
for a in sorted(CB):
    if a not in POOL:
        continue
    kind, native = classify(a)
    refs = CB[a]
    fams = ','.join('%X' % (cid >> 12) for cid, _ in
                    sorted(set((cid, r) for cid, r in refs)))
    verbs = ';'.join('%04X:%s(%s)' % (cid, VERBS.get(cid, '?'), role)
                     for cid, role in refs)
    if kind == 'adapter':
        members.append((a, fams, verbs, native))
    else:
        leftovers.append((a, fams, verbs, native))

print('frontier callbacks: %d' % sum(1 for a in CB if a in POOL))
print('adapters: %d   leftovers: %d' % (len(members), len(leftovers)))
print('leftover reasons: %s' % dict(collections.Counter(
    n for _a, _f, _v, n in leftovers)))
print('adapter natives: %s' % dict(collections.Counter(
    'indirect' if n == 'indirect' else 'none' if n == 'none' else 'one-native'
    for _a, _f, _v, n in members)))

if '--write' in sys.argv:
    with io.open(OUT, 'w', encoding='utf-8', newline='\n') as f:
        f.write('address\tfamily\tverb_id\tverb_name\trole\tnative_callee\n')
        for a, fams, verbs, native in members:
            ids = ';'.join('%04X' % cid for cid, _ in CB[a])
            names = ';'.join(VERBS.get(cid, '?') for cid, _ in CB[a])
            roles = ';'.join(role for _cid, role in CB[a])
            f.write('%08X\t%s\t%s\t%s\t%s\t%s\n'
                    % (a, fams, ids, names, roles, native))
    with io.open(LEFTOVER, 'w', encoding='utf-8', newline='\n') as f:
        f.write('address\tfamily\tverb_id\tverb_name\trole\treject_reason\n')
        for a, fams, verbs, native in leftovers:
            ids = ';'.join('%04X' % cid for cid, _ in CB[a])
            names = ';'.join(VERBS.get(cid, '?') for cid, _ in CB[a])
            roles = ';'.join(role for _cid, role in CB[a])
            f.write('%08X\t%s\t%s\t%s\t%s\t%s\n'
                    % (a, fams, ids, names, roles, native))
    print('wrote %s (%d) and %s (%d)'
          % (os.path.basename(OUT), len(members),
             os.path.basename(LEFTOVER), len(leftovers)))
