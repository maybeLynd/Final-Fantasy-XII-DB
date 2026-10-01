"""select_descriptor_flag_registrars_compact.py - the 53-byte compact encoding
of the descriptor-registration initialiser. Same idiom as the 64-byte
descriptor-flag form, one flag operation fewer:

    sub rsp,28 ; lea rcx,[obj] ; call <ctor> ; and dword [obj+0xFC],~2
    lea rax,[rec] ; lea rcx,[dtor] ; mov [obj],rax ; add rsp,28 ; jmp 00808B90

The 64-byte form clears bit1 AND sets bit3 (`mov eax,[flag]; and ~2; or 8;
mov [flag],eax`); this compact form only clears bit1 (`and dword [flag],~2`)
and writes the record pointer before the teardown lea. Same provenance class,
different toolchain encoding - declared as its own row.

EC-7 family C member selector:

  1. seeds = the 53-byte entries of the tail-643 candidate file - 5 bodies;
  2. derive the skeleton over the seeds; scan EVERY 53-byte census body for
     it - twins must equal the seed set, so the form is self-bounding;
  3. per-member provenance controls: call target is a member of a declared
     AbstractClassDescriptor constructor family; the lea'd dtor target is a
     member of a declared teardown family; flag word is exactly object+0xFC;
     tail is 00808B90 (atexit);
  4. refuse to write if any member is A-measured, declared by another family,
     or if census twins exist beyond the seed set.

Usage: python select_descriptor_flag_registrars_compact.py [--write]
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
             os.path.join(REPO, "Database", "FFXII TZA",
                          "24-Compiler-And-CRT-Runtime",
                          "Static-Initialization-And-Teardown", "members",
                          "xc-registered-static-teardowns.tsv")]
TAIL643 = os.path.join(DB, "_index", "candidates", "atexit-anchor-tail-643.tsv")
OUT = os.path.join(ROOT, "descriptor-flag-registrars-compact.tsv")

SIZE = 53
ATEXIT = 0x808B90
SELF = "members/descriptor-flag-registrars-compact.tsv"

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


# seeds: the tail-643's 53-byte candidate rows (5), plus this TSV's own
# previous members so re-runs stay self-describing
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
print("seeds (tail-643 53B rows + prior members): %d" % len(seeds))

blobs = [d[off(e):off(e) + SIZE] for e in seeds]
fixed = [i for i in range(SIZE) if len({b[i] for b in blobs}) == 1]
sig = bytes(blobs[0][i] for i in fixed)
print("derived skeleton: identical positions: %d of %d" % (len(fixed), SIZE))

skeleton_hits = sorted(e for e, sz in sizes.items()
                       if sz == SIZE and off(e) is not None
                       and bytes(d[off(e) + i] for i in fixed) == sig)
print("skeleton matches, census-wide        : %d" % len(skeleton_hits))


def facts(e):
    """Compact-form operands: object, .rdata record, dtor, flag word,
    ctor call target, tail target."""
    o = off(e)
    b = d[o:o + SIZE]
    return dict(
        obj=e + 0x0B + struct.unpack_from("<i", b, 7)[0],
        ctor=e + 0x10 + struct.unpack_from("<i", b, 12)[0],
        flag=e + 0x17 + struct.unpack_from("<i", b, 0x12)[0],
        rec=e + 0x1E + struct.unpack_from("<i", b, 0x1A)[0],
        dtor=e + 0x25 + struct.unpack_from("<i", b, 0x21)[0],
        obj2=e + 0x2C + struct.unpack_from("<i", b, 0x28)[0],
        tail=e + 0x35 + struct.unpack_from("<i", b, 0x31)[0],
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

members, owned, refused = [], [], []
for e in skeleton_hits:
    f = facts(e)
    if e in a_set or e in dec:
        owned.append((e, f))
        continue
    ok = (f["ctor"] in ctors and f["dtor"] in teardowns
          and f["obj"] == f["obj2"] and f["flag"] == f["obj"] + 0xFC
          and f["tail"] == ATEXIT)
    (members if ok else refused).append((e, f))
    if not ok:
        print("%08X  REFUSED ctor=%08X dtor=%08X flag=%08X tail=%08X"
              % (e, f["ctor"], f["dtor"], f["flag"], f["tail"]))

owner_split = collections.Counter(dec.get(e, "A") for e, _ in owned)
print("members: %d   owned by other families: %d (%s)   refused: %d"
      % (len(members), len(owned), ", ".join("%s x%d" % kv for kv in owner_split.most_common(5)),
         len(refused)))

if "--write" in sys.argv:
    assert not refused, ["%08X" % e for e, _ in refused]
    assert sorted(e for e, _ in members) == sorted(s for s in seeds
                                                 if s not in a_set and s not in dec), \
        "frontier members differ from seed set - the form is not self-bounding"
    with io.open(OUT, "w", encoding="utf-8", newline="\n") as fp:
        fp.write("# %d descriptor-registration initialisers - the 53-byte compact form:\n"
                 % len(members))
        fp.write("# construct a descriptor-family static via a declared AbstractClassDescriptor\n")
        fp.write("# ctor, clear bit1 of the object's +0xFC flag word (`and dword [flag],~2` -\n")
        fp.write("# no bit3 set, unlike the 64-byte form), install an .rdata record pointer,\n")
        fp.write("# then register the object's declared static teardown via the atexit wrapper\n")
        fp.write("# 00808B90. The skeleton bounds itself: a census-wide scan of 53-byte bodies\n")
        fp.write("# finds exactly these %d, no twins.\n" % len(members))
        fp.write("# address\tsize\tobject\t.rdata record\tctor (declared)\tdtor (declared)\n")
        for e, f in members:
            fp.write("%08X\t%d\t%08X\t%08X\t%08X\t%08X\n"
                     % (e, SIZE, f["obj"], f["rec"], f["ctor"], f["dtor"]))
    print("wrote", OUT, len(members), "rows")
else:
    print("members:", len(members), "(dry run - pass --write to emit the TSV)")
