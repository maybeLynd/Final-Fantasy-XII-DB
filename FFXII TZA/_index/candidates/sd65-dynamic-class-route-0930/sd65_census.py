"""sd65_census.py - which shipped .phyre class records ask the cluster loader for the dynamic route (OPUS, 2026-09-30;
register SD-65). Reads every .phyre namespace in FFXII_TZA.vbf (vbfextract.py) and counts, per class name:
  - w7 (+0x1C) values, and how many records set bit 0 - the bit the loader 0059AC00 tests before it builds a dynamic
    class (0059AC95) or dynamic members (0059AE28);
  - w0 (+0x00), read as the 1-based super-class index the dynamic-class path uses (0059AC9F, "Unable to find super
    class %d (of %d)"): the name it points at, and whether it is ever out of range;
  - w3 (+0x0C) member counts, and whether the class leaf has any static registration in phyre-field-schema.tsv.
Writes sd65_census.json beside itself and prints a summary ending in the controls.
"""
import collections, json, os, struct, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, r"C:\Users\Kristian\source\repos\XIIOnline\agent_flow\tools")
import vbfextract  # noqa: E402

VBF = r"D:\FFXII MP Mod\FFXII_TestClient1\FFXII_TZA.vbf"
TSV = os.path.join(HERE, "..", "..", "..", "22-Middleware-PhyreEngine", "Reflection-And-Class-Metadata", "phyre-field-schema.tsv")
static = set()
for l in open(TSV, encoding="utf-8"):
    p = l.rstrip("\r\n").split("\t")
    if p and p[0] and p[0] != "class_leaf":
        static.add(p[0])

f = open(VBF, "rb")
names, blocks = vbfextract.load_index(f)
phy = [n for n in names if n.lower().endswith(".phyre")]
w7 = collections.defaultdict(collections.Counter)
sup = collections.defaultdict(collections.Counter)
nmem = collections.defaultdict(collections.Counter)
bit0, oob, files = [], 0, 0
for p in phy:
    d = vbfextract.read_entry(f, names, blocks, p)
    hsz, nssz = struct.unpack_from("<II", d, 4)
    ns = d[hsz:hsz + nssz]
    nT, nC, nM, _ = struct.unpack_from("<IIII", ns, 8)
    coff = 0x20 + 4 * nT
    poff = coff + 36 * nC + 24 * nM
    nm = lambda o: ns[poff + o:ns.index(b"\0", poff + o)].decode("ascii", "replace")
    recs = [struct.unpack_from("<9I", ns, coff + 36 * c) for c in range(nC)]
    cn = [nm(w[2]) for w in recs]
    files += 1
    for k, w in enumerate(recs):
        w7[cn[k]][w[7]] += 1
        nmem[cn[k]][w[3]] += 1
        if w[7] & 1:
            bit0.append((p, cn[k]))
        if w[0] == 0:
            sup[cn[k]]["(none)"] += 1
        elif w[0] - 1 < nC:
            sup[cn[k]][cn[w[0] - 1]] += 1
        else:
            oob += 1
out = {"files": files, "bit0_records": bit0[:50], "bit0_total": len(bit0), "super_out_of_range": oob,
       "classes": {c: {"w7": dict(w7[c]), "super": dict(sup[c]), "members": dict(nmem[c]), "static": c.split("<")[0] in static}
                   for c in sorted(w7)}}
json.dump(out, open(os.path.join(HERE, "sd65_census.json"), "w"), indent=1, sort_keys=True)
vals = collections.Counter()
for c in w7:
    vals.update(w7[c])
print("files %d, class names %d" % (files, len(w7)))
print("w7 values over all class records:", dict(sorted(vals.items())))
print("records with w7 bit 0 set: %d" % len(bit0))
print("w0 out of range: %d" % oob)
dyn_cand = sorted(c for c in w7 if max(nmem[c]) > 0 and c.split("<")[0] not in static)
print("classes declaring members with no row in phyre-field-schema.tsv (%d):" % len(dyn_cand))
for c in dyn_cand:
    print("   %-48s members %s  super %s" % (c, dict(nmem[c]), dict(sup[c])))
print("control: files == 35984 %s; bit-0 records == 0 %s" % ("PASS" if files == 35984 else "FAIL",
                                                             "PASS" if not bit0 else "FAIL"))
