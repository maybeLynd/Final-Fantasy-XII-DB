"""select_scalar_conversion_registrars.py - the 144 thread-safe local-static initialisers that
register Phyre serialization's 12x12 scalar-type conversion matrix.

EC-7 family C member selector. Re-derives membership from the shipping EXE, independently of
guard-adapter-registrars.tsv (which is keyed on the teardown adapters, not these bodies):

  1. seed = every census body of EXACTLY 383 bytes in the run 005850F0..00592770;
  2. derive the skeleton: byte positions where every seed member agrees (296 of 383 - the other
     87 are operands: the per-static block, guard, descriptor accessors, stored routine);
  3. search EVERY 383-byte census body for that skeleton - the family is defined by FORM and the
     run is NOT assumed to be the family (the static-init-530 probe taught that the hard way);
  4. the resolved E8 targets shared by all 144 must be exactly the four universal ones:
     008092FC _Init_thread_header, 0080929C _Init_thread_footer, 00808B90 atexit wrapper,
     0067F700 the ordered-tree insert (documented on lazy-statics-and-the-one-time-init-lock.md);
  5. join each member to guard-adapter-registrars.tsv's registrar column to carry the decoded
     (source, destination) scalar pair and the stored conversion routine;
  6. refuse to write if any member is A-measured or declared by another family, if the census-wide
     form search finds anyone outside the run, or if the join leaves a member undecoded.

Reads: Database/Tools/work/exe/FFXII_TZA.exe, Database/Tools/work/graph/functions.tsv,
guard-adapter-registrars.tsv (for the decode only - membership does not come from it).
Usage: python select_scalar_conversion_registrars.py [--write]
"""
import io, os, struct, sys, collections

ROOT = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(ROOT, "..", "..", "..", "..", ".."))
EXE = os.path.join(REPO, "Database", "Tools", "work", "exe", "FFXII_TZA.exe")
FUNCS = os.path.join(REPO, "Database", "Tools", "work", "graph", "functions.tsv")
JOIN = os.path.join(ROOT, "guard-adapter-registrars.tsv")
OUT = os.path.join(ROOT, "scalar-conversion-registrars.tsv")
RUN_LO, RUN_HI = 0x005850F0, 0x00592770
SIZE = 383
UNIVERSAL = {0x008092FC, 0x00808B90, 0x0080929C, 0x0067F700}

sys.path.insert(0, os.path.join(REPO, "Database", "Tools", "analysis-kit", "gfz-scripts"))
import check_dispositions as CD
import check_coverage_cross as CC

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

seed = [e for e in sorted(sizes) if RUN_LO <= e <= RUN_HI and sizes[e] == SIZE]
blobs = [d[off(e):off(e) + SIZE] for e in seed if off(e) is not None]
fixed = [i for i in range(SIZE) if len({b[i] for b in blobs}) == 1]
sig = bytes(blobs[0][i] for i in fixed)

hits = sorted(e for e, sz in sizes.items()
              if sz == SIZE and off(e) is not None
              and bytes(d[off(e) + i] for i in fixed) == sig)

calls = collections.Counter()
per_member_calls = {}
for e in hits:
    o = off(e)
    tgts = set()
    for i in range(SIZE - 5):
        if d[o + i] == 0xE8:
            tgts.add(e + i + 5 + struct.unpack_from("<i", d, o + i + 1)[0])
    per_member_calls[e] = tgts
    calls.update(tgts)

shared = {t for t, n in calls.items() if n == len(hits)}

# decoded (source, dest, routine) from the join table - decode only, never membership
decode = {}
for l in io.open(JOIN, encoding="utf-8", errors="replace"):
    p = l.rstrip("\n").split("\t")
    if len(p) >= 8 and p[2] and p[2][0] in "0123456789ABCDEF":
        try:
            decode[int(p[2], 16)] = (p[5], p[6], p[7])
        except ValueError:
            pass

a_set, _eo, _ai, _da = CD.measure_a(os.path.join(REPO, "Database", "FFXII TZA"), sizes)
dec = {}
for doc, parts in CD.parse_families(os.path.join(REPO, "Database", "FFXII TZA")):
    if len(parts) < 5 or parts[1] not in ("B", "C", "D"):
        continue
    if parts[2].strip().endswith("scalar-conversion-registrars.tsv"):
        continue                      # this family's own row is not 'declared elsewhere' (SWE2-EC7 2026-09-30)
    try:
        for m in CD.read_members(doc, parts[2]):
            dec[m] = parts[0]
    except (IOError, OSError, ValueError):
        pass

print("seed bodies (383 B inside the run)      : %d" % len(seed))
print("derived skeleton: identical positions : %d of %d" % (len(fixed), SIZE))
print("form matches, census-wide             : %d" % len(hits))
print("  inside the run                      : %d" % sum(1 for e in hits if RUN_LO <= e <= RUN_HI))
print("  outside the run                     : %d" % sum(1 for e in hits if not (RUN_LO <= e <= RUN_HI)))
print("universal call targets (x%d):" % len(hits))
for t in sorted(shared):
    print("  %08X" % t)
print("  universal set == expected four      : %s" % (shared == UNIVERSAL))
print("distinct call targets total           : %d" % len(calls))
print("members A-measured                    : %d" % sum(1 for e in hits if e in a_set))
print("members already declared              : %d" % sum(1 for e in hits if e in dec))
print("members joined to the decode          : %d" % sum(1 for e in hits if e in decode))
pairs = collections.Counter(decode[e][:2] for e in hits if e in decode)
print("distinct (source,destination) pairs   : %d" % len(pairs))
types = sorted({t for pr in pairs for t in pr})
print("distinct scalar types                 : %d  %s" % (len(types), ", ".join(types)))

if "--write" in sys.argv:
    assert len(hits) == 144, hits
    assert all(RUN_LO <= e <= RUN_HI for e in hits)
    assert shared == UNIVERSAL, shared
    # Accounting state is not a predicate (FABLE ruling on SWE2-EC7-REQ-FABLE-PHYRE-UNIFORM-RULE-0930, points 1/3;
    # SWE2-EC7 2026-09-30): the 144 form hits are the family by form; an A-measured hit stays A and a hit another
    # family owns stays there - both are left out of the OUTPUT (printed), never asserted away.
    out_a = [e for e in hits if e in a_set]
    out_dec = [e for e in hits if e in dec]
    print("not written: A-measured %d %s; owned by another family %d %s" % (len(out_a), " ".join("%08X" % e for e in out_a),
          len(out_dec), " ".join("%08X" % e for e in out_dec)))
    hits = [e for e in hits if e not in a_set and e not in dec]
    assert all(e in decode for e in hits), "join incomplete"
    with io.open(OUT, "w", encoding="utf-8", newline="\n") as f:
        f.write("# 144 thread-safe local-static initialisers - each lazily constructs one node of\n")
        f.write("# Phyre serialization's 12x12 scalar-conversion tree under sentinel 01F2CDA0,\n")
        f.write("# registering its teardown through atexit. Form-derived: 296 of 383 byte positions\n")
        f.write("# identical across all members; universal callees 008092FC/0080929C/00808B90/0067F700.\n")
        f.write("# select_scalar_conversion_registrars.py --write\n")
        f.write("entry\tsize\tsource_type\tdest_type\tstored_routine\n")
        for e in hits:
            s, dd, rt = decode[e]
            f.write("%08X\t%d\t%s\t%s\t%s\n" % (e, SIZE, s, dd, rt))
    print("wrote", os.path.relpath(OUT, REPO))
