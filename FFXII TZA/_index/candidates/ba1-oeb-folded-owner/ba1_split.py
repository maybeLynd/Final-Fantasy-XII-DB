"""ba1_split.py - OPUS (Claude Opus 5.5), 2026-09-28, for BA-1 (the folded vtable addresses' owners).

STATIC. Splits every folded vtable address by what records (or voids) its owner, then checks, against the admitted
evidence base, whether anything shipped says which object file's copy the linker kept. That is the negative an OUT OF
EVIDENCE BOUNDARY proposal must carry (FRONTIER batch-K 27b, guard part 3).

Inputs: Tools/work/rtti/methods.tsv, vtables.tsv, classes.tsv (the RTTI recovery), and FFXII_TZA.exe's own RTTI class
hierarchy descriptors (read here from each vtable's complete object locator at vtable-8).

Checks:
  S1  the population reproduces: 6,886 vtable targets, 2,611 folded (more than one class), 108 across namespaces
      (FABLE's reduction: strip template arguments, drop the last '::' component).
  S2  every folded address falls in exactly one class:
        INHERITANCE          one class R of the set is a base (by the exe's hierarchy) of every other member: one
                             function, inherited; the owner is R and the hierarchy records it.
        ONE-TEMPLATE-FAMILY  every member is an instantiation of one template.
        STUB                 a straight-line body of 8 bytes or less ending in ret, with no branch or call.
        FOLDED               the rest: distinct classes' byte-identical methods merged by /OPT:ICF.
  C1  control for INHERITANCE: 0079C140 (1,404 B) is INHERITANCE with root Phyre::PFramework::PApplication
      (FABLE, 2026-09-16: slot 28 of both GameApplication and its base).
  C2  control for STUB: 0016D680 (4 B, 1,349 classes) is a STUB.
  N0  the image carries no symbol table: COFF PointerToSymbolTable 0, NumberOfSymbols 0.
  N1  its RSDS record names the PDB: FF12X64.pdb, GUID {46AA5C98-1328-4CCB-9701-806D753BD26C}, age 1.
  N2  address layout (a translation unit's functions are contiguous) as a class-level witness:
      - control: on unambiguous methods, unanimous nearest single-class neighbours give the right class at >= 95%;
      - measured on FOLDED: how many are placed by that rule inside their own sharing set.
  N3  the same at namespace level, on the FOLDED addresses whose set spans more than one namespace.
Writes ba1_split.tsv (every folded address: class, root or family, size, layout verdicts). Exit 1 on a failed check.
"""
import bisect, collections, csv, os, struct, sys
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
EXE = os.path.join(DB, "Tools", "work", "exe", "FFXII_TZA.exe")
RT = os.path.join(DB, "Tools", "work", "rtti")
d = open(EXE, "rb").read()
B = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]
nsec, optsz = struct.unpack_from("<H", d, pe + 6)[0], struct.unpack_from("<H", d, pe + 20)[0]
SECS = [struct.unpack_from("<IIII", d, pe + 24 + optsz + i * 40 + 8) for i in range(nsec)]
fails = 0


def check(tag, ok, text):
    global fails
    fails += 0 if ok else 1
    print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))


def off(rva):
    for vs, va, rs, ro in SECS:
        if va <= rva < va + max(vs, rs) and rva - va < rs:
            return ro + rva - va
    return None


def cstr(rva):
    o = off(rva)
    return d[o:d.index(b"\0", o)].decode("latin-1")


MD = Cs(CS_ARCH_X86, CS_MODE_64)


def stub(a):
    """(True, text) when the body is straight-line, ends in ret and is 8 bytes or less."""
    o, n, text = off(a - B), 0, []
    for ins in MD.disasm(d[o:o + 16], a):
        text.append(ins.mnemonic + (" " + ins.op_str if ins.op_str else ""))
        n += ins.size
        if ins.mnemonic.startswith("j") or ins.mnemonic.startswith("call") or n > 8:
            return False, "; ".join(text)
        if ins.mnemonic == "ret":
            return True, "; ".join(text)
    return False, "; ".join(text)


def body_len(a):
    """Bytes to the first ret / jmp at or past every forward branch target (an estimate; reported, not gated)."""
    o, maxt = off(a - B), a
    for ins in MD.disasm(d[o:o + 8192], a):
        if ins.mnemonic.startswith("j") and ins.op_str.startswith("0x"):
            t = int(ins.op_str, 16)
            if ins.mnemonic == "jmp" and ins.address >= maxt:
                return ins.address + ins.size - a
            maxt = max(maxt, t)
        elif ins.mnemonic in ("ret", "int3") or ins.mnemonic == "jmp":
            if ins.address >= maxt:
                return ins.address + (ins.size if ins.mnemonic != "int3" else 0) - a
    return None


def strip_templates(n):
    out, dep = [], 0
    for ch in n:
        if ch == "<":
            dep += 1
        elif ch == ">":
            dep -= 1
        elif dep == 0:
            out.append(ch)
    return "".join(out)


def ns(n):
    parts = strip_templates(n).split("::")
    return "::".join(parts[:-1]) if len(parts) > 1 else "(global)"


# the exe's own hierarchy: class -> every base named by its class hierarchy descriptor (the class itself included)
m2n = {r["mangled"]: r["class"] for r in csv.DictReader(open(os.path.join(RT, "classes.tsv"), encoding="utf-8"), delimiter="\t")}
bases = collections.defaultdict(set)
for r in csv.DictReader(open(os.path.join(RT, "vtables.tsv"), encoding="utf-8"), delimiter="\t"):
    vt, cl = int(r["vtable"], 16), r["class"]
    if cl in bases:
        continue
    col = struct.unpack_from("<Q", d, off(vt - 8 - B))[0] - B
    if off(col) is None or struct.unpack_from("<I", d, off(col))[0] != 1:
        continue
    chd = struct.unpack_from("<i", d, off(col) + 16)[0]
    nb, bca = struct.unpack_from("<Ii", d, off(chd) + 8)
    for k in range(nb):
        bcd = struct.unpack_from("<i", d, off(bca) + 4 * k)[0]
        nm = cstr(struct.unpack_from("<i", d, off(bcd))[0] + 16)
        bases[cl].add(m2n.get(nm, nm))

by = collections.defaultdict(set)
for r in csv.DictReader(open(os.path.join(RT, "methods.tsv"), encoding="utf-8"), delimiter="\t"):
    by[int(r["address"], 16)].add(r["class"])
folded = sorted(a for a in by if len(by[a]) > 1)
cross = {a for a in folded if len({ns(c) for c in by[a]}) > 1}
check("S1", (len(by), len(folded), len(cross)) == (6886, 2611, 108),
      "population: %d vtable targets, %d folded, %d across namespaces" % (len(by), len(folded), len(cross)))

kind, why, size = {}, {}, {}
for a in folded:
    cs = by[a]
    roots = sorted(r for r in cs if all(c == r or r in bases.get(c, ()) for c in cs))
    ok, text = stub(a)
    size[a] = body_len(a)
    if roots:
        kind[a], why[a] = "INHERITANCE", roots[0]
    elif len({strip_templates(c) for c in cs}) == 1:
        kind[a], why[a] = "ONE-TEMPLATE-FAMILY", strip_templates(next(iter(cs)))
    elif ok:
        kind[a], why[a] = "STUB", text
    else:
        kind[a], why[a] = "FOLDED", ""
tally = collections.Counter(kind.values())
tx = collections.Counter(kind[a] for a in cross)
check("S2", sum(tally.values()) == len(folded), "split of %d: %s; of the 108 across namespaces: %s"
      % (len(folded), dict(sorted(tally.items())), dict(sorted(tx.items()))))
check("C1", kind.get(0x79C140) == "INHERITANCE" and why.get(0x79C140) == "Phyre::PFramework::PApplication",
      "0079C140: %s %s" % (kind.get(0x79C140), why.get(0x79C140)))
check("C2", kind.get(0x16D680) == "STUB", "0016D680 (%d classes): %s [%s]" % (len(by[0x16D680]), kind.get(0x16D680), why.get(0x16D680)))

nsym = struct.unpack_from("<II", d, pe + 12)
check("N0", nsym == (0, 0), "COFF PointerToSymbolTable 0x%X, NumberOfSymbols %d" % nsym)
i = d.find(b"RSDS")
g = d[i + 4:i + 20]
guid = "%08X-%04X-%04X-%s-%s" % (struct.unpack_from("<I", g)[0], struct.unpack_from("<H", g, 4)[0],
                                 struct.unpack_from("<H", g, 6)[0], g[8:10].hex().upper(), g[10:16].hex().upper())
age, path = struct.unpack_from("<I", d, i + 20)[0], d[i + 24:d.index(b"\0", i + 24)].decode()
check("N1", path.endswith("FF12X64.pdb") and guid == "46AA5C98-1328-4CCB-9701-806D753BD26C" and age == 1,
      "RSDS {%s} age %d %s" % (guid, age, path))

single = sorted(a for a in by if len(by[a]) == 1)
owner = {a: next(iter(by[a])) for a in single}


def layout(a, key, k=2, window=0x4000):
    """The unanimous key of the k nearest single-class vtable targets on each side (within window), else None."""
    i, got = bisect.bisect_left(single, a), []
    for rng in (range(i - 1, -1, -1), range(i, len(single))):
        n = 0
        for j in rng:
            if abs(single[j] - a) > window or n == k:
                break
            if single[j] != a:
                got.append(key(owner[single[j]]))
                n += 1
    return got[0] if len(got) >= 2 and len(set(got)) == 1 else None


verdict = {}
for lvl, key in (("class", lambda c: c), ("namespace", ns)):
    h = m = 0
    for a in single:
        p = layout(a, key)
        if p is not None:
            h, m = h + (p == key(owner[a])), m + (p != key(owner[a]))
    pop = [a for a in folded if kind[a] == "FOLDED" and (lvl == "class" or a in cross)]
    t = collections.Counter()
    for a in pop:
        p = layout(a, key)
        v = "in-set" if p in {key(c) for c in by[a]} else "outside-set" if p else "none"
        verdict[(lvl, a)] = (v, p or "")
        t[v] += 1
    tag = "N2" if lvl == "class" else "N3"
    check(tag, h / max(1, h + m) >= 0.95, "%s level - control %d/%d = %.4f on unambiguous methods (coverage %d of %d); "
          "on %d FOLDED%s: %s" % (lvl, h, h + m, h / max(1, h + m), h + m, len(single), len(pop),
                                   "" if lvl == "class" else " across namespaces", dict(sorted(t.items()))))

with open(os.path.join(HERE, "ba1_split.tsv"), "w", encoding="utf-8", newline="\n") as f:
    f.write("address\tclasses\tacross_namespaces\tkind\troot_family_or_stub\tbody_bytes_est\tlayout_class\tlayout_namespace\n")
    for a in folded:
        vc = verdict.get(("class", a), ("", ""))
        vn = verdict.get(("namespace", a), ("", ""))
        f.write("%08X\t%d\t%s\t%s\t%s\t%s\t%s\t%s\n" % (a, len(by[a]), "yes" if a in cross else "no", kind[a], why[a],
                                                   size[a] if size[a] is not None else "", " ".join(vc).strip(),
                                                   " ".join(vn).strip()))
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
