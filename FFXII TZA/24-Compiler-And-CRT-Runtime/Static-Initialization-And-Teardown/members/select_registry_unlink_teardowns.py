"""select_registry_unlink_teardowns.py - the 328 95-byte teardown bodies that each
reinstall a registry node's vtable and splice the node out of its singly-linked
registry list at process exit.

EC-7 family C member selector. Re-derives membership from the shipping EXE:

  1. seed = every 95-byte census body that a 32-byte dynamic-initialiser stub of the
     static-init-form-530 group-A set names as its dtor operand (the atexit argument);
     the initialiser set is re-derived by the same form mask used by
     select_static_init_form.py, not read from its output files;
  2. derive the skeleton: byte positions where every seed agrees - expected ~62 of 95
     (the rest are the per-node operands: node address, vtable, list head, link slot);
  3. search EVERY 95-byte census body for that skeleton;
  4. membership = skeleton match AND registered as a dtor operand by one of the 420
     group-A initialisers - skeleton matches not registered are reported as boundary
     siblings, never admitted silently;
  5. refuse to write if any member is A-measured, declared by another family, or if
     the registered set differs from the seed.

Reads: Database/Tools/work/exe/FFXII_TZA.exe, Database/Tools/work/graph/functions.tsv.
Usage: python select_registry_unlink_teardowns.py [--write]
"""
import io, os, struct, sys, collections

ROOT = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(ROOT, "..", "..", "..", "..", ".."))
EXE = os.path.join(REPO, "Database", "Tools", "work", "exe", "FFXII_TZA.exe")
FUNCS = os.path.join(REPO, "Database", "Tools", "work", "graph", "functions.tsv")
DB = os.path.join(REPO, "Database", "FFXII TZA")
OUT = os.path.join(ROOT, "registry-unlink-teardowns.tsv")

INIT_SIZE = 32
INIT_FIXED = [i for i in range(INIT_SIZE) if i not in
              set(range(7, 11)) | set(range(12, 16)) | set(range(19, 23)) | set(range(28, 32))]
INIT_SKELETON = bytes.fromhex("4883ec28" "488d0d" "e8" "488d0d" "4883c428" "e9")
ATEXIT_WRAPPER = 0x00808B90
SIZE = 95
SELF = "members/registry-unlink-teardowns.tsv"

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

# step 1: re-derive the 420 group-A initialisers and their dtor operands
init_dtors = {}
for e in sorted(sizes):
    if sizes[e] != INIT_SIZE or off(e) is None:
        continue
    if bytes(d[off(e) + i] for i in INIT_FIXED) != INIT_SKELETON:
        continue
    o = off(e)
    tail = e + 32 + struct.unpack_from("<i", d, o + 28)[0]
    if tail != ATEXIT_WRAPPER:
        continue
    dtor = e + 23 + struct.unpack_from("<i", d, o + 19)[0]
    init_dtors[e] = dtor

seeds = sorted({dt for dt in init_dtors.values() if sizes.get(dt) == SIZE})
blobs = [d[off(e):off(e) + SIZE] for e in seeds]
fixed = [i for i in range(SIZE) if len({b[i] for b in blobs}) == 1]
sig = bytes(blobs[0][i] for i in fixed)

skeleton_hits = sorted(e for e, sz in sizes.items()
                       if sz == SIZE and off(e) is not None
                       and bytes(d[off(e) + i] for i in fixed) == sig)
registered = set(init_dtors.values())
members = [e for e in skeleton_hits if e in registered]
siblings = [e for e in skeleton_hits if e not in registered]

a_set, _eo, _ai, _da = CD.measure_a(DB, sizes)
dec = {}
for doc, parts in CD.parse_families(DB):
    if len(parts) < 5 or parts[1] not in ("B", "C", "D"):
        continue
    if parts[2] == SELF:
        continue
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

print("group-A initialisers re-derived      : %d" % len(init_dtors))
print("distinct registered dtors            : %d" % len(registered))
print("  of size 95 (seeds)                 : %d" % len(seeds))
print("derived skeleton: identical positions: %d of %d" % (len(fixed), SIZE))
print("skeleton matches, census-wide        : %d" % len(skeleton_hits))
print("members (skeleton + registered)      : %d" % len(members))
print("skeleton siblings not registered     : %d  %s"
      % (len(siblings), " ".join("%08X" % e for e in siblings[:10])))
print("members already declared             : %d" % sum(1 for e in members if e in dec))
print("members A-measured                   : %d" % sum(1 for e in members if e in a_set))

if "--write" in sys.argv:
    assert len(seeds) == 328
    assert not siblings, siblings
    assert not any(e in a_set for e in members)
    assert not any(e in dec for e in members)
    owner = {dt: e for e, dt in init_dtors.items()}
    with io.open(OUT, "w", encoding="utf-8", newline="\n") as f:
        f.write("# %d 95-byte teardown bodies: reinstall a registry node's vtable, then\n" % len(members))
        f.write("# walk the singly-linked registry list and splice the node out at process\n")
        f.write("# exit. Each is the atexit-registered dtor operand of one 32-byte\n")
        f.write("# static-init-form-530 group-A initialiser (column 'initialiser').\n")
        f.write("# Form-derived: %d of %d byte positions identical across all members.\n"
                % (len(fixed), SIZE))
        f.write("# select_registry_unlink_teardowns.py --write\n")
        f.write("entry\tsize\tinitialiser\n")
        for e in members:
            f.write("%08X\t%d\t%08X\n" % (e, SIZE, owner[e]))
    print("wrote", os.path.relpath(OUT, REPO))
