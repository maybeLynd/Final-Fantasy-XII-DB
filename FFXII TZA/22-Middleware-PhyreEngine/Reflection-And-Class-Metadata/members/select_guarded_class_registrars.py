"""select_guarded_class_registrars.py - the thread-safe guarded class-
registration tree inside the atexit tail. Emits ONE TSV:

  guarded-class-registration-stubs.tsv - every member, with an information
  column naming the auxiliary callees that are themselves of the guarded form
  (call _Init_thread_header, _Init_thread_footer and atexit), whoever owns them.

ONE FAMILY (FABLE ruling e862a1dae, _index/candidates/fable-gcr-split-ruling-0929,
applied by SWE2-EC7 2026-09-29). This selector used to split the members into
"leaf stubs" (auxiliary calls meet no other member) and "orchestrators" (they
meet at least one). That split moved bodies whenever another family's
bookkeeping moved (00665870 and 00666380 flipped when their callees were
measured A), and the code-defined alternative flips 53 of 99: neither names a
kind of code. Membership is unchanged - the fixpoint below; the sibling-call
fact survives only as the information column, and a body's column may change
as other families change while its membership may not. The retired
guarded-class-registration-orchestrators.tsv is still read as a seed source if
present (history), never written.

Every member is a census body that:

  1. calls _Init_thread_header 008092FC AND _Init_thread_footer 0080929C
     (the MSVC thread-safe magic-static guard pair);
  2. calls the atexit wrapper 00808B90 (registers its teardown);
  3. calls at least one auxiliary target, and EVERY auxiliary target is
     already-explained code: a member of a declared B/C/D family, an
     A-measured function, one of the shared registration-machinery helpers
     (frontier helpers called by >=2 members - the family's named
     shared-target control), or another member of the family
     (orchestration edge; membership is the fixpoint over rule 3).

The predicate IS the form: these bodies are the compiler-emitted guarded
registration stubs of the Phyre/PType class tree - the same machinery the
accepted two-member (m_count + m_els) registrar family names as its
controls. Members vary in size 182..3757 bytes because each registers a
different member set; the call-set signature is what binds them.

Self-bounding check: the same predicate is applied to EVERY census body;
any hit that is not a member must already be owned by another family or
A-measured. Refuses to write otherwise.

Usage: python select_guarded_class_registrars.py [--write]
"""
import io, os, struct, sys, collections

ROOT = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(ROOT, "..", "..", "..", "..", ".."))
EXE = os.path.join(REPO, "Database", "Tools", "work", "exe", "FFXII_TZA.exe")
FUNCS = os.path.join(REPO, "Database", "Tools", "work", "graph", "functions.tsv")
DB = os.path.join(REPO, "Database", "FFXII TZA")
TAIL643 = os.path.join(DB, "_index", "candidates", "atexit-anchor-tail-643.tsv")
OUT_LEAF = os.path.join(ROOT, "guarded-class-registration-stubs.tsv")
OUT_ORCH = os.path.join(ROOT, "guarded-class-registration-orchestrators.tsv")

HDR, FTR, AX = 0x8092FC, 0x80929C, 0x808B90
SELFS = {"members/guarded-class-registration-stubs.tsv",
         "members/guarded-class-registration-orchestrators.tsv"}

sys.path.insert(0, os.path.join(REPO, "Database", "Tools", "analysis-kit", "gfz-scripts"))
import check_dispositions as CD
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

d = io.open(EXE, "rb").read()
pe = struct.unpack_from("<I", d, 0x3C)[0]
nsec = struct.unpack_from("<H", d, pe + 6)[0]
optsz = struct.unpack_from("<H", d, pe + 20)[0]
base = struct.unpack_from("<Q", d, pe + 24 + 24)[0]
secs = []
for i in range(nsec):
    o = pe + 24 + optsz + i * 40
    vsz, va, rsz, ptr = struct.unpack_from("<IIII", d, o + 8)
    secs.append((va, vsz, ptr, rsz))


def off(va):
    r = va - base
    for sva, vsz, ptr, rsz in secs:
        if sva <= r < sva + max(vsz, rsz):
            return ptr + (r - sva)
    return None


sizes = {}
for l in io.open(FUNCS, encoding="utf-8", errors="replace"):
    p = l.rstrip("\n").split("\t")
    try:
        sizes[int(p[0], 16)] = int(p[2])
    except (ValueError, IndexError):
        pass

md = Cs(CS_ARCH_X86, CS_MODE_64)
_call_cache = {}


def calls(e):
    """Direct call targets plus direct jmp targets (the atexit tail is a
    jmp in the leaf stubs and a call in the guarded registrars)."""
    if e not in _call_cache:
        sz = sizes.get(e)
        o = off(e)
        if sz is None or o is None:
            _call_cache[e] = frozenset()
        else:
            _call_cache[e] = frozenset(
                int(i.op_str, 16)
                for i in md.disasm(d[o:o + sz], e)
                if i.mnemonic in ("call", "jmp") and i.op_str.startswith("0x")
                and not (e <= int(i.op_str, 16) < e + sz))
    return _call_cache[e]


def load_members(path):
    out = set()
    if not os.path.exists(path):
        return out
    for l in io.open(path, encoding="utf-8", errors="replace"):
        t = l.split("\t")[0].strip()
        try:
            out.add(int(t, 16))
        except ValueError:
            pass
    return out


a_set, _eo, _ai, _da = CD.measure_a(DB, sizes)
dec = {}
for doc, parts in CD.parse_families(DB):
    if len(parts) < 5 or parts[1] not in ("B", "C", "D"):
        continue
    if parts[2] in SELFS:
        continue
    try:
        for m in CD.read_members(doc, parts[2]):
            dec[m] = parts[0]
    except (IOError, OSError, ValueError):
        pass

# seeds: tail-643 frontier + this family's own previous members
# (the exclusion is applied below - a prior member that has since been
# A-measured or declared elsewhere must NOT be re-admitted through the seed)
seeds = set()
for l in io.open(TAIL643, encoding="utf-8", errors="replace"):
    if l.startswith("#"):
        continue
    p = l.split("\t")
    try:
        e = int(p[0], 16)
    except ValueError:
        continue
    if e not in a_set and e not in dec:
        seeds.add(e)
for e in set(load_members(OUT_LEAF)) | set(load_members(OUT_ORCH)):   # OUT_ORCH: retired, read if present
    if e not in a_set and e not in dec:
        seeds.add(e)
seeds = sorted(seeds)
print("seeds (tail-643 frontier + prior members): %d" % len(seeds))

# shared-machinery helpers: frontier aux targets called by >=2 seeds
fanin = collections.defaultdict(set)
aux = {e: calls(e) - {HDR, FTR, AX} for e in seeds}
for e, a in aux.items():
    for t in a:
        fanin[t].add(e)
MACH = {t for t, cs in fanin.items()
        if len(cs) >= 2 and t not in dec and t not in a_set}
known = set(dec) | a_set | MACH
print("shared machinery helpers (frontier, fan-in>=2): %d" % len(MACH))
for t in sorted(MACH):
    print("   %08X  x%d" % (t, len(fanin[t])))

# fixpoint over seeds
mem = set()
changed = True
while changed:
    changed = False
    for e in seeds:
        if e in mem:
            continue
        c = calls(e)
        if not ({HDR, FTR, AX} <= c):
            continue
        a = aux[e]
        if a and all(t in known or t in mem for t in a):
            mem.add(e)
            changed = True

# census-wide twin check: same predicate over every census body
hits = []
for e, sz in sizes.items():
    if sz > 8192 or off(e) is None:
        continue
    c = calls(e)
    if {HDR, FTR, AX} <= c:
        a = c - {HDR, FTR, AX}
        if a and all(t in known or t in mem for t in a):
            hits.append(e)
outside = [h for h in hits if h not in mem]
bad = [h for h in outside if h not in dec and h not in a_set]
own = collections.Counter(dec.get(h, "A") for h in outside)
print("members: %d   census predicate hits: %d (owned/A: %d, free: %d)"
      % (len(mem), len(hits), len(outside) - len(bad), len(bad)))
print("   non-member ownership:", ", ".join("%s x%d" % kv for kv in own.most_common(8)))
if bad:
    print("   FREE predicate hits (would be unaccounted twins):")
    for h in sorted(bad):
        print("     %08X %dB" % (h, sizes[h]))

# information column: auxiliary callees of the guarded form (the ruling's GUARDED set), whoever owns them
GUARDED = {e for e, sz in sizes.items() if sz <= 8192 and off(e) is not None and {HDR, FTR, AX} <= calls(e)}
gcol = {e: sorted(t for t in aux[e] if t in GUARDED) for e in mem}
print("members: %d (one family); with a guarded-form auxiliary callee: %d (information only; census guarded-form bodies %d)"
      % (len(mem), sum(1 for e in mem if gcol[e]), len(GUARDED)))

if "--write" in sys.argv:
    assert not bad, ["%08X" % h for h in bad]
    with io.open(OUT_LEAF, "w", encoding="utf-8", newline="\n") as fp:
        fp.write("# %d thread-safe guarded class-registration stubs - one family (FABLE ruling e862a1dae).\n" % len(mem))
        fp.write("# Each is a compiler-emitted magic-static guarded initialiser: calls\n")
        fp.write("# _Init_thread_header 008092FC and _Init_thread_footer 0080929C around the\n")
        fp.write("# registration payload and registers a teardown via the atexit wrapper\n")
        fp.write("# 00808B90. Every other call target is already-explained code: a declared\n")
        fp.write("# family member, an A-measured helper, or one of the shared frontier\n")
        fp.write("# machinery helpers (006388C0 PType find/register, 00632960 member-reg,\n")
        fp.write("# 005A7A40, 00632FB0, 006B66C0/006B67D0, 00632D80, 0063DC80/0063DF90/\n")
        fp.write("# 0063DFA0, 00632A70, 00632C90, 00639160, 005A0470, 00632BE0, 005CC8A0,\n")
        fp.write("# 00225690, 00584730, 00616210, 006B6820, 006B8D20) - the family's\n")
        fp.write("# shared-target control. Members register distinct member sets, so sizes\n")
        fp.write("# vary; the call-set predicate is the form. Census-wide the predicate is\n")
        fp.write("# self-bounding: every non-member match is owned by another family or A.\n")
        fp.write("# The last column is INFORMATION, not identity: auxiliary callees that are\n")
        fp.write("# themselves of the guarded form, whoever owns them (the former\n")
        fp.write("# leaf/orchestrator split, retired by FABLE ruling e862a1dae).\n")
        fp.write("# address\tsize\taux call targets (excl. guard pair + atexit)\tguarded-form aux callees\n")
        for e in sorted(mem):
            fp.write("%08X\t%d\t%s\t%s\n" % (e, sizes[e],
                                             ",".join("%08X" % t for t in sorted(aux[e])),
                                             ",".join("%08X" % t for t in gcol[e]) or "-"))
    print("wrote", OUT_LEAF, len(mem))
else:
    print("dry run - pass --write to emit the TSVs")
