"""select_two_member_descriptor_registrars.py - the 38 thread-safe guarded initialisers
that each build a Phyre class descriptor registering exactly two members named m_count
and m_els (the count + elements pair of a resizable-array-style reflection layout).

EC-7 family C member selector. Re-derives membership from the shipping EXE, independently
of _index/candidates/phyre-two-member-descriptor-39.tsv (OPUS's assembled candidate list -
cross-checked, never trusted):

  1. seed = every 815-byte census body listed in the candidate file (39);
  2. derive the skeleton: byte positions where every seed agrees (545 of 815 - the other
     270 are operands: descriptor, guard, member records, vftables, dtor);
  3. search EVERY 815-byte census body for that skeleton;
  4. membership requires provenance on top of the form: the body contains a disp32
     resolving to 00D27728 ("m_count") AND one resolving to 00D32DC0 ("m_els") - each
     literal exists exactly once in the image, so the pair names THIS member layout;
     skeleton matches failing the literal pair are boundary siblings, not members;
  5. controls: every member calls the three descriptor-constructor targets 006372A0,
     006373D0, 00632D80 (the accepted AbstractClassDescriptor base-aware family's own
     named controls) and _Init_thread_header 008092FC exactly four times;
  6. refuse to write if any member is A-measured, declared by another family, if the
     census-wide skeleton count is not 39, or if provenance is ambiguous.

Reads: Database/Tools/work/exe/FFXII_TZA.exe, Database/Tools/work/graph/functions.tsv,
       _index/candidates/phyre-two-member-descriptor-39.tsv (seed only).
Usage: python select_two_member_descriptor_registrars.py [--write]
"""
import io, os, struct, sys, collections

ROOT = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(ROOT, "..", "..", "..", "..", ".."))
EXE = os.path.join(REPO, "Database", "Tools", "work", "exe", "FFXII_TZA.exe")
FUNCS = os.path.join(REPO, "Database", "Tools", "work", "graph", "functions.tsv")
DB = os.path.join(REPO, "Database", "FFXII TZA")
CAND = os.path.join(DB, "_index", "candidates", "phyre-two-member-descriptor-39.tsv")
OUT = os.path.join(ROOT, "two-member-descriptor-registrars.tsv")

SIZE = 815
LIT_M_COUNT = 0x00D27728
LIT_M_ELS = 0x00D32DC0
CONTROL_CALLS = {0x006372A0, 0x006373D0, 0x00632D80}
INIT_THREAD_HEADER = 0x008092FC
SELF = "members/two-member-descriptor-registrars.tsv"

sys.path.insert(0, os.path.join(REPO, "Database", "Tools", "analysis-kit", "gfz-scripts"))
import check_dispositions as CD

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
    p = l.split("\t")
    try:
        sizes[int(p[0], 16)] = int(p[2])
    except (ValueError, IndexError):
        pass

seeds = []
for l in io.open(CAND, encoding="utf-8", errors="replace"):
    t = l.split("\t")[0]
    try:
        seeds.append(int(t, 16))
    except ValueError:
        pass
assert all(sizes.get(e) == SIZE for e in seeds), "seed not an 815-byte census body"

blobs = [d[off(e):off(e) + SIZE] for e in seeds]
fixed = [i for i in range(SIZE) if len({b[i] for b in blobs}) == 1]
sig = bytes(blobs[0][i] for i in fixed)

skeleton_hits = sorted(e for e, sz in sizes.items()
                       if sz == SIZE and off(e) is not None
                       and bytes(d[off(e) + i] for i in fixed) == sig)


def body_facts(e):
    """disp32 literals referenced anywhere, and e8 call-target counts."""
    o = off(e)
    lits = set()
    calls = collections.Counter()
    for i in range(SIZE - 4):
        rel = struct.unpack_from("<i", d, o + i)[0]
        t = e + i + 4 + rel
        if t in (LIT_M_COUNT, LIT_M_ELS):
            lits.add(t)
        if d[o + i] == 0xE8:
            calls[e + i + 5 + struct.unpack_from("<i", d, o + i + 1)[0]] += 1
    return lits, calls


facts = {e: body_facts(e) for e in skeleton_hits}
members = [e for e in skeleton_hits if facts[e][0] == {LIT_M_COUNT, LIT_M_ELS}]
siblings = [e for e in skeleton_hits if e not in members]

a_set, _eo, _ai, _da = CD.measure_a(DB, sizes)
dec = {}
for doc, parts in CD.parse_families(DB):
    if len(parts) < 5 or parts[1] not in ("B", "C", "D"):
        continue
    if parts[2] == SELF:
        continue  # self: this family's own declaration is what --write produces
    try:
        for m in CD.read_members(doc, parts[2]):
            dec[m] = parts[0]
    except (IOError, OSError, ValueError):
        pass

a_excl = [e for e in members if e in a_set]
if a_excl:
    print("A-measured members EXCLUDED          : %s"
          % ", ".join("%08X" % e for e in a_excl))
    members = [e for e in members if e not in a_set]

ctl_ok = sum(1 for e in members if CONTROL_CALLS <= set(facts[e][1]))
hdr4 = sum(1 for e in members if facts[e][1][INIT_THREAD_HEADER] == 4)

print("seed bodies (815 B, candidate list)  : %d" % len(seeds))
print("derived skeleton: identical positions: %d of %d" % (len(fixed), SIZE))
print("skeleton matches, census-wide        : %d" % len(skeleton_hits))
print("m_count+m_els provenance members     : %d" % len(members))
print("skeleton siblings failing literals   : %d  %s"
      % (len(siblings), " ".join("%08X" % e for e in siblings)))
print("member == candidate set minus A      : %s" % (set(members) == set(seeds) - a_set))
print("members calling all 3 control ctors  : %d" % ctl_ok)
print("members calling _Init_thread_hdr x4  : %d" % hdr4)
print("members already declared             : %d" % sum(1 for e in members if e in dec))

if "--write" in sys.argv:
    assert len(skeleton_hits) == 39
    assert len(members) == 38, len(members)
    assert not siblings, siblings
    assert set(members) == set(seeds) - a_set
    assert ctl_ok == len(members) and hdr4 == len(members)
    assert not any(e in a_set for e in members)
    assert not any(e in dec for e in members)
    with io.open(OUT, "w", encoding="utf-8", newline="\n") as f:
        f.write("# 38 thread-safe guarded initialisers, each building one Phyre class descriptor\n")
        f.write("# that registers exactly two members named m_count and m_els - the count +\n")
        f.write("# elements pair of a resizable-array-style reflection layout. PROVENANCE IS\n")
        f.write("# THE MEMBER-NAMED LITERALS: every member contains disp32 references to BOTH\n")
        f.write("# 00D27728 \"m_count\" and 00D32DC0 \"m_els\", each unique in the image, passed\n")
        f.write("# to the member-registration calls 00632960/00632A10. Form-derived: 545 of\n")
        f.write("# 815 byte positions identical; all members also call the three descriptor\n")
        f.write("# constructors 006372A0/006373D0/00632D80 and _Init_thread_header x4.\n")
        f.write("# select_two_member_descriptor_registrars.py --write\n")
        f.write("entry\tsize\n")
        for e in members:
            f.write("%08X\t%d\n" % (e, SIZE))
    print("wrote", os.path.relpath(OUT, REPO))
