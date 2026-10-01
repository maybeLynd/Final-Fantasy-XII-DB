"""select_eastl_string_static_inits.py - the 52 static eastl::basic_string<char>
initialisers that construct the embedded logging allocator, fill the three-pointer string
from a literal, and atexit-register the teardown.

EC-7 family C member selector. Re-derives membership from the shipping EXE, independently
of _index/candidates/eastl-basic-string-init-52.tsv (OPUS's assembled candidate list -
cross-checked, never trusted):

  1. seed = every 240-byte census body listed in the candidate file (52);
  2. derive the skeleton: byte positions where every seed agrees (178 of 240 - the other
     62 are operands: the static object's addresses, the literal, the dtor);
  3. search EVERY 240-byte census body for that skeleton - the family is defined by FORM
     plus PROVENANCE, and the run is not assumed;
  4. membership requires all three provenance facts on top of the form:
       a. the body leas 008F6600 - the ASCII literal "EASTL basic_string", the
          allocator_memory_log tag; the code names its own library type;
       b. the body calls 001EDF00 (allocator_memory_log ctor) EXACTLY twice - once for a
          stack copy, once for the allocator embedded at +0x18 of the static object;
       c. the body's last instruction tail-jumps 00808B90, the CRT atexit wrapper.
     Any skeleton match failing a provenance test is reported as a boundary sibling, not
     silently admitted;
  5. refuse to write if any member is A-measured, declared by another family, if the
     census-wide count is not 52, or if any skeleton match's provenance is ambiguous.

Reads: Database/Tools/work/exe/FFXII_TZA.exe, Database/Tools/work/graph/functions.tsv,
       _index/candidates/eastl-basic-string-init-52.tsv (seed only).
Usage: python select_eastl_string_static_inits.py [--write]
"""
import io, os, struct, sys, collections

ROOT = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(ROOT, "..", "..", "..", "..", ".."))
EXE = os.path.join(REPO, "Database", "Tools", "work", "exe", "FFXII_TZA.exe")
FUNCS = os.path.join(REPO, "Database", "Tools", "work", "graph", "functions.tsv")
DB = os.path.join(REPO, "Database", "FFXII TZA")
CAND = os.path.join(DB, "_index", "candidates", "eastl-basic-string-init-52.tsv")
OUT = os.path.join(ROOT, "eastl-string-static-initialisers.tsv")

SIZE = 240
TAG_STRING = 0x008F6600        # "EASTL basic_string"
ALLOC_CTOR = 0x001EDF00        # eastl::allocator_memory_log ctor, 14 B
ATEXIT_WRAPPER = 0x00808B90

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
assert all(sizes.get(e) == SIZE for e in seeds), "seed not a 240-byte census body"

blobs = [d[off(e):off(e) + SIZE] for e in seeds]
fixed = [i for i in range(SIZE) if len({b[i] for b in blobs}) == 1]
sig = bytes(blobs[0][i] for i in fixed)

skeleton_hits = sorted(e for e, sz in sizes.items()
                       if sz == SIZE and off(e) is not None
                       and bytes(d[off(e) + i] for i in fixed) == sig)


def body_facts(e):
    """Scan the 32-bit operands of rip-relative leas, e8 calls and the final e9."""
    o = off(e)
    leas, calls, tail = set(), collections.Counter(), None
    for i in range(SIZE - 4):
        b0 = d[o + i]
        if b0 == 0xE8:
            calls[e + i + 5 + struct.unpack_from("<i", d, o + i + 1)[0]] += 1
        elif b0 == 0xE9:
            tail = e + i + 5 + struct.unpack_from("<i", d, o + i + 1)[0]
        elif b0 == 0x8D and i >= 1 and d[o + i - 1] == 0x48:
            modrm = d[o + i + 1]
            if modrm in (0x05, 0x0D, 0x15, 0x1D, 0x25, 0x2D, 0x35, 0x3D):
                leas.add(e + i + 6 + struct.unpack_from("<i", d, o + i + 2)[0])
    return leas, calls, tail


facts = {e: body_facts(e) for e in skeleton_hits}
members = [e for e in skeleton_hits
           if TAG_STRING in facts[e][0]
           and facts[e][1][ALLOC_CTOR] == 2
           and facts[e][2] == ATEXIT_WRAPPER]
siblings = [e for e in skeleton_hits if e not in members]

a_set, _eo, _ai, _da = CD.measure_a(DB, sizes)
dec = {}
for doc, parts in CD.parse_families(DB):
    if len(parts) < 5 or parts[1] not in ("B", "C", "D"):
        continue
    if parts[2] == "members/eastl-string-static-initialisers.tsv":
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

print("seed bodies (240 B, candidate list)  : %d" % len(seeds))
print("derived skeleton: identical positions: %d of %d" % (len(fixed), SIZE))
print("skeleton matches, census-wide        : %d" % len(skeleton_hits))
print("provenance-passing members           : %d" % len(members))
print("skeleton siblings failing provenance : %d  %s"
      % (len(siblings), " ".join("%08X" % e for e in siblings)))
print("member == candidate set minus A      : %s" % (set(members) == set(seeds) - a_set))
print("members A-measured                   : %d" % sum(1 for e in members if e in a_set))
print("members already declared             : %d" % sum(1 for e in members if e in dec))

if "--write" in sys.argv:
    assert len(members) == 51, len(members)
    assert not siblings, siblings
    assert set(members) == set(seeds) - a_set
    assert not any(e in a_set for e in members)
    assert not any(e in dec for e in members)
    with io.open(OUT, "w", encoding="utf-8", newline="\n") as f:
        f.write("# 51 static eastl::basic_string<char> initialisers - each constructs the\n")
        f.write("# allocator_memory_log embedded at +0x18 of a static string object, fills the\n")
        f.write("# three-pointer string from a literal (allocating via the allocator vtable,\n")
        f.write("# or the shared empty byte 02EBA2E0), then atexit-registers the teardown through\n")
        f.write("# 00808B90. PROVENANCE IS THE LITERAL: every member leas 008F6600 \"EASTL\n")
        f.write("# basic_string\" and calls 001EDF00 exactly twice. Form-derived: 178 of 240 byte\n")
        f.write("# positions identical across all members.\n")
        f.write("# select_eastl_string_static_inits.py --write\n")
        f.write("entry\tsize\n")
        for e in members:
            f.write("%08X\t%d\n" % (e, SIZE))
    print("wrote", os.path.relpath(OUT, REPO))
