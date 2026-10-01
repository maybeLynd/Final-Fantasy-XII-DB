"""select_descriptor_flag_registrars.py - the descriptor-registration initialisers
in the 64-byte flag-variant form. Two provenance populations, one instruction
encoding:

  * the four bodies 0016C280/2C0/300/340 - the frontier remainder of OPUS's
    measured 331-body run 0016AB00..0016D540 (the other 327 are declared by the
    PInputs semantic-name-registry, MSVC-generic and Phyre module-utility
    initialiser families);
  * the thirty bodies 00161200..001692E0 - the 64-byte cluster of OPUS's
    atexit-anchor tail-643 worklist (atexit-anchor-tail-643.tsv), all sharing
    this same opcode layout - only the operand immediates differ.

EC-7 family C member selector. Re-derives membership from the shipping EXE and
the database's own declared-member TSVs, never from a pasted list:

  1. seeds = the union of this TSV's previous members (re-read, not trusted)
     plus the 64-byte entries of the tail-643 candidate file - 34 bodies;
  2. derive the skeleton: byte positions where all 34 agree (39 of 64 - the
     25 varying positions are the object/record/dtor/flag disp32 and the
     call/jmp rel32 operands);
  3. scan EVERY census body of the same size for that skeleton - twins must
     equal the seed set, so the form is self-bounding;
  4. per-member provenance controls: the call target is a member of a declared
     AbstractClassDescriptor constructor family AND the lea'd dtor target is a
     member of a declared teardown family AND the flag word is exactly
     object+0xFC AND the tail is 00808B90 (atexit);
  5. refuse to write if any member is A-measured, declared by another family,
     if either provenance control fails, or if census twins exist beyond the
     seed set.

Reads: Database/Tools/work/exe/FFXII_TZA.exe, Database/Tools/work/graph/functions.tsv,
       members/abstract-class-descriptor-base-aware-constructors.tsv,
       members/abstract-class-descriptor-constructors.tsv,
       members/class-descriptor-static-teardowns.tsv,
       members/xc-registered-static-object-teardowns.tsv (if present),
       _index/candidates/atexit-anchor-tail-643.tsv.
Usage: python select_descriptor_flag_registrars.py [--write]
"""
import io, os, struct, sys, collections

ROOT = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(ROOT, "..", "..", "..", "..", ".."))
EXE = os.path.join(REPO, "Database", "Tools", "work", "exe", "FFXII_TZA.exe")
FUNCS = os.path.join(REPO, "Database", "Tools", "work", "graph", "functions.tsv")
DB = os.path.join(REPO, "Database", "FFXII TZA")
CTORS = [os.path.join(ROOT, "abstract-class-descriptor-base-aware-constructors.tsv"),
         os.path.join(ROOT, "abstract-class-descriptor-constructors.tsv")]
TEARDOWNS = [os.path.join(ROOT, "class-descriptor-static-teardowns.tsv"),
             os.path.join(ROOT, "xc-registered-static-object-teardowns.tsv")]
TAIL643 = os.path.join(DB, "_index", "candidates", "atexit-anchor-tail-643.tsv")
OUT = os.path.join(ROOT, "descriptor-flag-registrars.tsv")

SIZE = 64
ATEXIT = 0x808B90
SELF = "members/descriptor-flag-registrars.tsv"

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


# seeds: previous members of this TSV + the tail-643's 64-byte candidate rows
seeds = set(load_members(OUT))
for l in io.open(TAIL643, encoding="utf-8", errors="replace"):
    if l.startswith("#"):
        continue
    p = l.split("\t")
    if len(p) >= 2:
        try:
            e, sz = int(p[0], 16), int(p[1])
        except ValueError:
            continue
        if sz == SIZE:
            seeds.add(e)
seeds = sorted(e for e in seeds if sizes.get(e) == SIZE and off(e) is not None)
print("seeds (previous members + tail-643 64B rows): %d" % len(seeds))

blobs = [d[off(e):off(e) + SIZE] for e in seeds]
fixed = [i for i in range(SIZE) if len({b[i] for b in blobs}) == 1]
sig = bytes(blobs[0][i] for i in fixed)
print("derived skeleton: identical positions: %d of %d" % (len(fixed), SIZE))

skeleton_hits = sorted(e for e, sz in sizes.items()
                       if sz == SIZE and off(e) is not None
                       and bytes(d[off(e) + i] for i in fixed) == sig)
print("skeleton matches, census-wide        : %d" % len(skeleton_hits))


def facts(e):
    """The flag-variant operands: object, .rdata record, dtor, flag word,
    ctor call target, tail target."""
    o = off(e)
    b = d[o:o + SIZE]
    return dict(
        obj=e + 11 + struct.unpack_from("<i", b, 7)[0],
        ctor=e + 16 + struct.unpack_from("<i", b, 12)[0],
        rec=e + 23 + struct.unpack_from("<i", b, 19)[0],
        obj2=e + 30 + struct.unpack_from("<i", b, 26)[0],
        dtor=e + 37 + struct.unpack_from("<i", b, 33)[0],
        flag=e + 43 + struct.unpack_from("<i", b, 39)[0],
        flag2=e + 55 + struct.unpack_from("<i", b, 51)[0],
        tail=e + 64 + struct.unpack_from("<i", b, 60)[0],
    )


ctors = set().union(*[load_members(p) for p in CTORS])
teardowns = set().union(*[load_members(p) for p in TEARDOWNS])
print("declared descriptor ctors loaded     : %d" % len(ctors))
print("declared teardowns loaded            : %d" % len(teardowns))

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

members, refused = [], []
for e in skeleton_hits:
    f = facts(e)
    ok = (f["ctor"] in ctors and f["dtor"] in teardowns
          and f["obj"] == f["obj2"] and f["flag"] == f["flag2"]
          and f["flag"] == f["obj"] + 0xFC and f["tail"] == ATEXIT
          and e not in a_set and e not in dec)
    (members if ok else refused).append((e, f))
    if not ok:
        print("%08X  REFUSED ctor=%08X dtor=%08X flag=%08X tail=%08X"
              % (e, f["ctor"], f["dtor"], f["flag"], f["tail"]))

print("members: %d   refused: %d" % (len(members), len(refused)))

if "--write" in sys.argv:
    assert not refused, ["%08X" % e for e, _ in refused]
    assert sorted(e for e, _ in members) == seeds, \
        "census twins differ from seed set - the form is not self-bounding"
    with io.open(OUT, "w", encoding="utf-8", newline="\n") as fp:
        fp.write("# %d descriptor-registration initialisers - the 64-byte flag-variant form:\n"
                 % len(members))
        fp.write("# construct a descriptor-family static via a declared AbstractClassDescriptor\n")
        fp.write("# ctor (base-aware or plain), install an .rdata record pointer into the object,\n")
        fp.write("# clear bit1 and set bit3 of the object's +0xFC flag word, then register the\n")
        fp.write("# object's declared static teardown via the atexit wrapper 00808B90. Members\n")
        fp.write("# come from two populations with one encoding: the frontier remainder of the\n")
        fp.write("# 331-body run 0016AB00..0016D540 (4 bodies) and the 64-byte cluster of the\n")
        fp.write("# atexit-anchor tail-643 worklist (30 bodies). The skeleton is derived over the\n")
        fp.write("# union and bounds itself: a census-wide scan of 64-byte bodies finds exactly\n")
        fp.write("# these %d, no twins.\n" % len(members))
        fp.write("# address\tsize\tobject\t.rdata record\tctor (declared)\tdtor (declared)\n")
        for e, f in members:
            fp.write("%08X\t%d\t%08X\t%08X\t%08X\t%08X\n"
                     % (e, SIZE, f["obj"], f["rec"], f["ctor"], f["dtor"]))
    print("wrote", OUT, len(members), "rows")
else:
    print("members:", len(members), "(dry run - pass --write to emit the TSV)")
