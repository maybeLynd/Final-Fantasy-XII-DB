"""rc5_join.py - RC-5 (ORACLE, 2026-09-30).  Joins the authored set ids (rc5_verbs.tsv: eventread 0xE7, eventread_e8 0xE8,
summoneventread 0x198) and the fixed native set id 212 (0025DAE8, manager 1, from manager 0's update 0025D9E0) with the
kind-8 rows of rc5_paths.tsv (region 1 = 'us'; the (set id, name) pairs are identical in every region, rc5_paths.py).
Reads the set id as the LAST pushed operand (eventread_e8: [r8+4] = edx, the operand after the manager operand;
eventread: the single operand).  Prints, per verb, how many distinct constant set ids land on a kind-8 event path, the
names they select, and the classified names (flag A sum_..0001, flag B spc_, sum_ JSON only).
Control: set id 212 must name pre_z0000 (the native preload)."""
import collections, io, os
HERE = os.path.dirname(os.path.abspath(__file__))
name = {}
for i, l in enumerate(io.open(os.path.join(HERE, "rc5_paths.tsv"), encoding="utf-8")):
    p = l.rstrip("\n").split("\t")
    if i and p[0] == "1" and p[2] == "8" and p[8] == "MATCH" and p[7] == "in-array":
        name[int(p[4])] = (p[10], p[11])
fails = 0
if name.get(212, ("",))[0] != "pre_z0000":
    fails += 1
ids = collections.defaultdict(collections.Counter)
dyn = collections.Counter()
for i, l in enumerate(io.open(os.path.join(HERE, "rc5_verbs.tsv"), encoding="utf-8")):
    p = l.rstrip("\n").split("\t")
    if i == 0 or p[4] not in ("eventread", "eventread_e8", "summoneventread"):
        continue
    v = p[7].split(";")[-1] if p[7] else ""
    if v.lstrip("-").isdigit():
        ids[p[4]][int(v)] += 1
    else:
        dyn[(p[4], p[1], v or p[6])] += 1
ids["native 0025DAE8"][212] += 1
allcls = collections.Counter()
for verb, c in ids.items():
    hit = [s for s in c if s in name]
    miss = sorted(s for s in c if s not in name)
    cls = collections.Counter(name[s][1] or "-" for s in hit)
    flagged = sorted((name[s][0], s) for s in hit if name[s][1])
    print("%-16s distinct constant set ids %4d | on an event path %4d | not %s | classes %s" % (verb, len(c), len(hit), miss, dict(cls)))
    if flagged:
        print("   classified names selected:", flagged)
    for s in hit:
        allcls[name[s][0]] += c[s]
print("non-constant set-id sites:", dict(dyn))
print("classified names in the table (any set id):", sorted((v[0], k) for k, v in name.items() if v[1]))
print("FAILS", fails)
