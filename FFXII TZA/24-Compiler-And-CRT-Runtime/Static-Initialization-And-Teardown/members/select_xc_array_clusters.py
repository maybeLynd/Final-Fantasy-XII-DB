"""select_xc_array_clusters.py -- FABLE-REQ-SWE2-EC7-XC-INITIALISERS.

Census-wide selector for the remaining multi-member form clusters inside the
MSVC .CRT$XI dynamic-initialiser array (008C31D0..008C5678, read from the
shipping EXE).  Every declared cluster's membership rule is:

    member  <=>  body is an array entry
             AND body size / call set / tail-jump set match the cluster's
             AND body shares the cluster's derived fixed-byte skeleton
             AND body is not A-measured
             AND body is not already declared in another family

The skeleton check runs over the WHOLE function census, not just the array:
every skeleton twin must itself satisfy the cluster predicate, so no matching
body outside the declared set can silently exist.

Clusters written (each its own TSV next to this script):

  atexit-teardown-registration-stubs.tsv  12 B:  lea rcx,[T]; jmp atexit
                                            registers teardown fn T, no ctor.
  record-ctor-00662c00-initialisers.tsv   43 B:  call 00662C00 (3-field record
                                            ctor), call atexit, ret.
  record-ctor-00616210-initialisers.tsv   77/89/91 B: call 00616210 (bigger
                                            record ctor -> 0062CD40), jmp atexit.
  counter-append-initialisers.tsv         54 B:  append object to a counted
                                            table, jmp atexit.
  zeroinit-record-initialisers.tsv        57 B:  zero a 0x30-byte record,
                                            jmp atexit.
  record-ctor-006d58d0-initialisers.tsv   230 B: call 006D58D0 (flag-set record
                                            ctor), jmp atexit.
  callback-record-006155b0-registrars.tsv 33 B:  lea r9/r8/rdx,[3 fns];
                                            lea rcx,[obj]; jmp 006155B0.
  ctor-00808fe4-initialisers.tsv          60 B:  call 00808FE4, jmp atexit.
  (the three 42 B array callers of 005DC6F0 are byte-form members of the
   generated Runtime.NamedRegistryRecord.StaticInitializer family and are
   appended to that TSV, not declared here)
  alloc-record-0067ffb0-initialisers.tsv  59/68 B: call 0067FFB0 (aligned-size
                                            record ctor), jmp atexit.
  grow-helper-initialisers.tsv            66/86 B: call one of the three cloned
                                            grow helpers 006BFC60 / 006C2380 /
                                            006B8D20 (identical heads),
                                            jmp atexit.
  zeroinit-3q-initialisers.tsv            35 B:  zero three qwords, jmp atexit.
  ctor-0060df70-initialisers.tsv          49 B:  call 0060DF70, jmp atexit.

Two further clusters write their TSV under the EASTL members directory and
are declared on the EASTL page instead of this one:

  eastl-basicstring-variant-initialisers.tsv
                                        228/74 B: same allocator_memory_log
                                            tag "EASTL basic_string"
                                            (008F6600) + 001EDF00 ctor pair
                                            as the 51-member family, other
                                            generated body shapes.
  eastl-container-static-initialisers.tsv
                                        39/76/137 B: same mechanism with the
                                            "EASTL vector" / "EASTL map" /
                                            "EASTL list" tags.

Run:  python select_xc_array_clusters.py [--write]
"""

import io, os, re, sys, glob, struct, collections

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..'))
EXE = os.path.join(REPO, 'Database', 'Tools', 'work', 'exe', 'FFXII_TZA.exe')
FUNCS = os.path.join(REPO, 'Database', 'Tools', 'work', 'graph', 'functions.tsv')
DB = os.path.join(REPO, 'Database', 'FFXII TZA')
HERE = os.path.dirname(os.path.abspath(__file__))
ATEXIT = 0x00808B90
ARR_LO, ARR_HI = 0x008C31D0, 0x008C5678

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

# ---- .CRT$XI array -------------------------------------------------------
ARR = [q for q in (struct.unpack_from('<Q', D, foff(a))[0]
                   for a in range(ARR_LO, ARR_HI, 8)) if q]

# ---- per-body call / tail-jump facts -------------------------------------
# Decoded, not byte-scanned: a raw scan catches 0xE8/0xE9 bytes sitting inside
# an immediate or displacement and reports calls that do not exist.
from capstone import Cs, CS_ARCH_X86, CS_MODE_64                   # noqa: E402
from capstone.x86 import X86_OP_MEM, X86_REG_RIP                   # noqa: E402
MD = Cs(CS_ARCH_X86, CS_MODE_64)
MD.detail = True

def facts(e):
    """(direct call targets, tail-jump targets leaving the body)."""
    c, t = [], []
    for ins in MD.disasm(body(e), e):
        if ins.op_str.startswith('0x'):
            tgt = int(ins.op_str, 16)
            if ins.mnemonic == 'call':
                c.append(tgt)
            elif ins.mnemonic == 'jmp' and not (e <= tgt < e + SIZES[e]):
                t.append(tgt)
    return frozenset(c), frozenset(t)

CALLS = {e: facts(e) for e in ARR if e in SIZES}

EASTL_DIR = os.path.join(REPO, 'Database', 'FFXII TZA',
                         '23-Third-Party-Libraries', 'EASTL', 'members')
PHYRE_DIR = os.path.join(REPO, 'Database', 'FFXII TZA',
                         '22-Middleware-PhyreEngine', 'Subsystem-Map', 'members')
MODULE_HEAD = 0x02CACC90

def lea_targets(e):
    """All targets of 48 8D /r (lea reg,[rip+disp32]) instructions."""
    out = set()
    o = foff(e)
    for i in range(SIZES[e] - 6):
        if D[o + i] == 0x48 and D[o + i + 1] == 0x8D \
                and D[o + i + 2] & 0xC7 == 0x05:
            out.add(e + i + 7 + struct.unpack_from('<i', D, o + i + 3)[0])
    return out

LEAS = {e: lea_targets(e) for e in ARR if e in SIZES}

def rip_refs(e):
    """All RIP-relative operand targets, decoded."""
    out = set()
    for ins in MD.disasm(body(e), e):
        for op in ins.operands:
            if op.type == X86_OP_MEM and op.mem.base == X86_REG_RIP:
                out.add(ins.address + ins.size + op.mem.disp)
    return out

REFS = {e: rip_refs(e) for e in ARR if e in SIZES}

# ---- exclusions ----------------------------------------------------------
OWN = {
    'atexit-teardown-registration-stubs.tsv',
    'record-ctor-00662c00-initialisers.tsv',
    'record-ctor-00616210-initialisers.tsv',
    'counter-append-initialisers.tsv',
    'zeroinit-record-initialisers.tsv',
    'record-ctor-006d58d0-initialisers.tsv',
    'callback-record-006155b0-registrars.tsv',
    'ctor-00808fe4-initialisers.tsv',
    'alloc-record-0067ffb0-initialisers.tsv',
    'grow-helper-initialisers.tsv',
    'zeroinit-3q-initialisers.tsv',
    'ctor-0060df70-initialisers.tsv',
    'eastl-basicstring-variant-initialisers.tsv',
    'eastl-container-static-initialisers.tsv',
    'phyre-module-utility-registrars.tsv',
    'xc-initializer-leftovers.tsv',   # the NOT-declared tail; never a member set
}
DECLARED = {}
for f in glob.glob(os.path.join(DB, '**', 'members', '*.tsv'), recursive=True):
    base = os.path.basename(f)
    if base in OWN:
        continue                       # our own TSVs: allow re-runs
    for l in io.open(f, encoding='utf-8', errors='replace'):
        t = l.strip().split('\t')[0].upper()
        if re.fullmatch(r'[0-9A-F]{8}', t):
            DECLARED[t] = base

sys.path.insert(0, os.path.join(REPO, 'Database', 'Tools', 'analysis-kit',
                                'gfz-scripts'))
import check_dispositions as CD                     # noqa: E402
A_SET, _, _, _ = CD.measure_a(DB, SIZES)

FRONTIER = [e for e in ARR if e in SIZES
            and '%08X' % e not in DECLARED and e not in A_SET]
print('array entries: %d   frontier: %d' % (len(ARR), len(FRONTIER)))

# ---- cluster predicates --------------------------------------------------
def calls_are(*tgts):
    s = frozenset(tgts)
    return lambda e: CALLS[e][0] == s

def tail_are(*tgts):
    s = frozenset(tgts)
    return lambda e: CALLS[e][1] == s

CLUSTERS = [
    ('atexit-teardown-registration-stubs',
     lambda e: SIZES[e] == 12 and CALLS[e][0] == frozenset()
               and CALLS[e][1] == frozenset([ATEXIT])),
    ('record-ctor-00662c00-initialisers',
     lambda e: SIZES[e] == 43
               and CALLS[e][0] == frozenset([0x00662C00, ATEXIT])),
    ('record-ctor-00616210-initialisers',
     lambda e: SIZES[e] in (77, 89, 91)
               and CALLS[e][0] == frozenset([0x00616210])
               and CALLS[e][1] == frozenset([ATEXIT])),
    ('counter-append-initialisers',
     lambda e: SIZES[e] == 54 and CALLS[e][0] == frozenset()
               and CALLS[e][1] == frozenset([ATEXIT])),
    ('zeroinit-record-initialisers',
     lambda e: SIZES[e] == 57 and CALLS[e][0] == frozenset()
               and CALLS[e][1] == frozenset([ATEXIT])),
    ('record-ctor-006d58d0-initialisers',
     lambda e: SIZES[e] == 230
               and CALLS[e][0] == frozenset([0x006D58D0])
               and CALLS[e][1] == frozenset([ATEXIT])),
    ('callback-record-006155b0-registrars',
     lambda e: SIZES[e] == 33 and CALLS[e][0] == frozenset()
               and CALLS[e][1] == frozenset([0x006155B0])),
    ('ctor-00808fe4-initialisers',
     lambda e: SIZES[e] == 60
               and CALLS[e][0] == frozenset([0x00808FE4])
               and CALLS[e][1] == frozenset([ATEXIT])),
    ('alloc-record-0067ffb0-initialisers',
     lambda e: SIZES[e] in (59, 68)
               and CALLS[e][0] == frozenset([0x0067FFB0])
               and CALLS[e][1] == frozenset([ATEXIT])),
    ('grow-helper-initialisers',
     lambda e: SIZES[e] in (66, 86)
               and CALLS[e][0] <= frozenset([0x006BFC60, 0x006C2380, 0x006B8D20])
               and CALLS[e][0]
               and CALLS[e][1] == frozenset([ATEXIT])),
    ('zeroinit-3q-initialisers',
     lambda e: SIZES[e] == 35 and CALLS[e][0] == frozenset()
               and CALLS[e][1] == frozenset([ATEXIT])),
    ('ctor-0060df70-initialisers',
     lambda e: SIZES[e] == 49
               and CALLS[e][0] == frozenset([0x0060DF70])
               and CALLS[e][1] == frozenset([ATEXIT])),
    # EASTL-tagged clusters: TSV lives under the EASTL members dir.
    ('eastl-basicstring-variant-initialisers',
     lambda e: 0x001EDF00 in CALLS[e][0]
               and 0x008F6600 in LEAS[e]
               and CALLS[e][1] == frozenset([ATEXIT]),
     EASTL_DIR),
    ('eastl-container-static-initialisers',
     lambda e: 0x001EDF00 in CALLS[e][0]
               and LEAS[e] & frozenset([0x008C5F58, 0x008F4120, 0x008F3CC0])
               and CALLS[e][1] == frozenset([ATEXIT]),
     EASTL_DIR),
    # Phyre module-utility registrars: append one PUtility<Module> object to
    # the bounded (cap 0xFF) module list headed at 02CACC90, install the
    # module's vtable, tail-jump atexit.  86 B, no calls.
    ('phyre-module-utility-registrars',
     lambda e: SIZES[e] == 86 and CALLS[e][0] == frozenset()
               and CALLS[e][1] == frozenset([ATEXIT])
               and MODULE_HEAD in REFS[e],
     PHYRE_DIR),
]

# ---- derive skeleton, verify census-wide, write ---------------------------
def skeleton(members):
    b0 = body(members[0])
    fixed = [i for i in range(len(b0))
             if all(body(m)[i] == b0[i] for m in members[1:])]
    return fixed

def skeleton_hits(members):
    """Census-wide entries matching the cluster's fixed positions."""
    fixed = skeleton(members)
    b0 = body(members[0])
    sz = SIZES[members[0]]
    hits = []
    for e in SIZES:
        if SIZES[e] != sz:
            continue
        try:
            bb = body(e)
        except KeyError:
            continue
        if all(bb[i] == b0[i] for i in fixed):
            hits.append(e)
    return hits

write = '--write' in sys.argv
grand = 0
for spec in CLUSTERS:
    name, pred = spec[0], spec[1]
    outdir = spec[2] if len(spec) > 2 else HERE
    cand = [e for e in FRONTIER if pred(e)]
    cand.sort()
    if not cand:
        print('%-42s 0 candidates -- SKIPPED' % name)
        continue
    # per-size skeleton check: every census twin must itself satisfy pred
    szs = sorted({SIZES[e] for e in cand})
    twins = []
    for sz in szs:
        twins += skeleton_hits([e for e in cand if SIZES[e] == sz])
    outside = [e for e in twins if e not in set(cand)]
    print('%-42s %3d members  size(s)=%s  skeleton-twin-outside=%s'
          % (name, len(cand), szs, ['%08X' % e for e in outside]))
    grand += len(cand)
    if write:
        os.makedirs(outdir, exist_ok=True)
        out = os.path.join(outdir, name + '.tsv')
        with io.open(out, 'w', encoding='utf-8', newline='\n') as fh:
            fh.write('# %s -- EC-7 family C, XC-array cluster.\n' % name)
            fh.write('# %d members of the .CRT$XI dynamic-initialiser array\n'
                     % len(cand))
            fh.write('# sharing one (size, call-set, tail-set) signature;\n')
            fh.write('# select_xc_array_clusters.py --write\n')
            fh.write('entry\tsize\tcalls\ttail\n')
            for e in cand:
                c, t = CALLS[e]
                fh.write('%08X\t%d\t%s\t%s\n'
                         % (e, SIZES[e],
                            ','.join('%08X' % x for x in sorted(c)),
                            ','.join('%08X' % x for x in sorted(t))))
        print('   wrote %s' % out)

print('TOTAL new members: %d' % grand)

# ---- generated-family extension ------------------------------------------
# The three 42-byte array callers of 005DC6F0 left in the frontier carry the
# exact byte form of the generated Runtime.NamedRegistryRecord.StaticInitializer
# family (members/runtime-namedregistryrecord-staticinitializer.tsv): same
# size, same callee, same skeleton.  They are undiscovered members, not a new
# family -- verify the form and append them to that TSV.
GEN_DIR = os.path.join(REPO, 'Database', 'FFXII TZA',
                       '24-Compiler-And-CRT-Runtime', 'Generated-Families',
                       'members')
GEN_TSV = os.path.join(GEN_DIR,
                       'runtime-namedregistryrecord-staticinitializer.tsv')
nrr = sorted(e for e in FRONTIER
             if SIZES[e] == 42
             and 0x005DC6F0 in CALLS[e][0]
             and CALLS[e][1] == frozenset([ATEXIT]))
known = [int(t.strip().split('\t')[0], 16)
         for t in io.open(GEN_TSV, encoding='utf-8', errors='replace')
         if re.fullmatch(r'[0-9A-Fa-f]{8}', t.strip().split('\t')[0])]
fixed = [i for i in range(42)
         if all(body(e)[i] == body(nrr[0])[i]
                for e in nrr[1:] + known[:8])] if nrr else []
print('named-registry-record extensions: %d  (fixed positions shared with '
      'the declared form: %d/42)' % (len(nrr), len(fixed)))
if write and nrr:
    with io.open(GEN_TSV, 'a', encoding='utf-8', newline='\n') as fh:
        for e in nrr:
            fh.write('%08X\n' % e)
    print('   appended %d rows to %s' % (len(nrr), GEN_TSV))

# leftovers: frontier array members in no declared cluster
covered = set()
for spec in CLUSTERS:
    covered |= {e for e in FRONTIER if spec[1](e)}
rest = [e for e in FRONTIER if e not in covered and e not in nrr]
print('frontier array members left undeclared: %d' % len(rest))
if write:
    out = os.path.join(HERE, 'xc-initializer-leftovers.tsv')
    with io.open(out, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write('# xc-initializer-leftovers -- NOT a family.\n')
        fh.write('# %d frontier .CRT$XI entries matching no declared cluster;\n'
                 % len(rest))
        fh.write('# %d distinct (size, call-set, tail-set) shapes -- a '
                 'singleton tail.\n'
                 % len({(SIZES[e], CALLS[e][0], CALLS[e][1]) for e in rest}))
        fh.write('# select_xc_array_clusters.py --write\n')
        fh.write('entry\tsize\tcalls\ttail\n')
        for e in sorted(rest):
            c, t = CALLS[e]
            fh.write('%08X\t%d\t%s\t%s\n'
                     % (e, SIZES[e],
                        ','.join('%08X' % x for x in sorted(c)) or '-',
                        ','.join('%08X' % x for x in sorted(t)) or '-'))
    print('   wrote %s' % out)
