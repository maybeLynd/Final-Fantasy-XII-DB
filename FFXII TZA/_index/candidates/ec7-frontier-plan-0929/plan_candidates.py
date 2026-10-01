# plan_candidates.py - candidate member lists for the 2026-09-29 frontier plan (NOT declarations).
#   cand-slot10-placement-ctors.tsv  RTTI-exclusive slot 10 (+0x50) of Phyre::PClassDescriptorConcrete<T>,
#                                    body null-checks rdx and returns 1; with the A/declared positive control
#   cand-selector-admits.tsv         frontier bodies an existing family's own selector would admit today
import os, sys, io, csv, struct, collections
ROOT = r"C:\Users\Kristian\source\repos\XIIOnline"
sys.path.insert(0, ROOT + r"\Database\Tools\analysis-kit\gfz-scripts")
import check_dispositions as CD
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
DB = ROOT + r"\Database\FFXII TZA"; WK = ROOT + r"\Database\Tools\work"; OUT = WK + r"\SWE2-EC7\plan"
os.makedirs(OUT, exist_ok=True)
sizes = CD.load_functions(); r = CD.evaluate(DB, sizes)
front, claimed = r["frontier_set"], r["claimed_set"]; A = CD.measure_a(DB, sizes)[0]
d = open(WK + r"\exe\FFXII_TZA.exe", "rb").read()
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = []
for i in range(n):
    o = pe + 24 + opt + i * 40; vs, va, rs, ro = struct.unpack_from("<IIII", d, o + 8); secs.append((0x120000 + va, vs, ro, rs))
def off(a):
    for va, vs, ro, rs in secs:
        if va <= a < va + rs: return ro + (a - va)
md = Cs(CS_ARCH_X86, CS_MODE_64)
app = collections.defaultdict(list)
for row in csv.DictReader(open(WK + r"\rtti\methods.tsv", encoding="utf-8", errors="replace"), delimiter="\t"):
    try: app[int(row["address"], 16)].append((row["class"], row["slot"]))
    except (ValueError, TypeError): pass
def shape_ok(a):
    t = [(x.mnemonic, x.op_str) for x in md.disasm(d[off(a):off(a) + sizes[a]], a)]
    return any(m == "test" and o == "rdx, rdx" for m, o in t) and any(m == "mov" and o in ("al, 1", "eax, 1") for m, o in t)
owner = {}
for doc, parts in CD.parse_families(DB):
    try:
        for m in CD.read_members(doc, parts[2]): owner.setdefault(m, parts[0].strip())
    except Exception: pass
bodies = sorted(a for a, ap in app.items() if ap and all(c.startswith("Phyre::PClassDescriptorConcrete<") and s == "10" for c, s in ap))
stat = collections.Counter()
with io.open(os.path.join(OUT, "cand-slot10-placement-ctors.tsv"), "w", encoding="utf-8", newline="\n") as f:
    f.write("entry\tbytes\tstatus\tdeclared_by\tshape_nullcheck_ret1\tclass\n")
    for a in bodies:
        st = "frontier" if a in front else "A" if a in A else "declared" if a in claimed else "other"
        ok = shape_ok(a); stat[(st, ok)] += 1
        f.write("%08X\t%d\t%s\t%s\t%s\t%s\n" % (a, sizes[a], st, owner.get(a, "") if st == "declared" else "", "Y" if ok else "N",
                                            app[a][0][0][:120]))
print("slot10", sorted(stat.items()))
drift = DB + r"\_index\candidates\ec7-refused-family-repair-0929\selector-drift.tsv"
k = collections.Counter()
with io.open(os.path.join(OUT, "cand-selector-admits.tsv"), "w", encoding="utf-8", newline="\n") as f:
    f.write("family\tselector\tentry\tbytes\n")
    for row in csv.DictReader(open(drift, encoding="utf-8"), delimiter="\t"):
        if row["change"] == "would-admit" and int(row["address"], 16) in front:
            f.write("%s\t%s\t%s\t%d\n" % (row["family"], row["selector"], row["address"], sizes[int(row["address"], 16)]))
            k[row["family"]] += 1
print("selector admits (frontier only)", sum(k.values()), dict(k))
