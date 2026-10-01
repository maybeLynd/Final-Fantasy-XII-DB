"""SWE2-AUDIT-SEM RC-28(3) attack (own code): does the shipped staff roll request any accented menu04 name row
894..944? Independent of the producer's evaluator: a plain textual parse of the us decompile of men_z0005.
  - every call of any verb whose name starts with fsroll_ is listed by verb and argument shape;
  - literal arguments are decoded (hex/decimal); names = bit 15 clear, roles = bit 15 set;
  - every non-literal argument is printed with its enclosing loop header lines so its range is read by hand.
Negative control: the literal set must contain rows the producer says are requested (e.g. 0, 1) and must contain
none of 894..944 only if that is true; positive control: rows 894..944 exist in the fr menu04 (producer's S0/S2),
not re-derived here - scope is the request side only.
"""
import re, collections
F = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\pub140-scratch\corpus\us\men_z0005.txt"
L = open(F, encoding="utf-8", errors="replace").read().splitlines()
verbs = collections.Counter()
lit = collections.defaultdict(list)
nonlit = []
for n, line in enumerate(L, 1):
    for m in re.finditer(r"\b(fsroll_\w+)\s*\(([^)]*)\)", line):
        v, arg = m.group(1), m.group(2).strip()
        verbs[v] += 1
        if re.fullmatch(r"0x[0-9a-fA-F]+|\d+", arg):
            lit[v].append((int(arg, 0), n))
        elif arg:
            nonlit.append((n, v, arg))
print("fsroll_* verbs:", dict(verbs))
for v in sorted(lit):
    if v.startswith("fsroll_name"):
        vals = [x for x, _ in lit[v]]
        names = sorted({x for x in vals if not x & 0x8000})
        roles = sorted({x & 0x7FFF for x in vals if x & 0x8000})
        print("%s: %d literal calls; name ids %d distinct (min %s max %s); role ids %d distinct" % (
            v, len(vals), len(names), names[0] if names else "-", names[-1] if names else "-", len(roles)))
print("non-literal fsroll_* arguments:", len(nonlit))
for n, v, a in nonlit:
    ctx = [L[k - 1].strip() for k in range(max(1, n - 6), n) if re.search(r"\b(for|while|if|regI|=)\b", L[k - 1])]
    print("  line %d %s(%s)   context: %s" % (n, v, a, " | ".join(ctx[-4:])))
allnames = {x for v in lit if v.startswith("fsroll_name") for x, _ in lit[v] if not x & 0x8000}
hit = sorted(x for x in allnames if 894 <= x <= 944)
print("literal name ids in 894..944:", hit)
print("max literal name id:", max(allnames))

# ranges of the (K + regI0) arguments, from the nearest preceding for-header (searched up to 12 lines back)
ranges = []
unparsed = []
for n, v, a in nonlit:
    if not v.startswith("fsroll_name"):
        continue
    m = re.fullmatch(r"\(?(\d+|0x[0-9a-fA-F]+) \+ regI0\)?", a)
    hdr = None
    for k in range(n - 1, max(0, n - 13), -1):
        h = re.search(r"for \(regI0 = (\d+); regI0 < (\d+); regI0 = \(regI0 \+ (\d+)\)\)", L[k - 1])
        if h:
            hdr = tuple(int(g) for g in h.groups())
            break
    if not m or not hdr:
        unparsed.append((n, v, a))
        continue
    K = int(m.group(1), 0)
    ids = list(range(K + hdr[0], K + hdr[1], hdr[2]))
    ranges.append((n, v, K, hdr, ids))
loopids = {i for r in ranges for i in r[4] if not i & 0x8000}
print("loop-argument name calls parsed:", len(ranges), " unparsed:", unparsed)
print("loop name ids: %d distinct, max %d; in 894..944: %s" % (len(loopids), max(loopids), sorted(i for i in loopids if 894 <= i <= 944)))
tot = allnames | loopids
print("ALL requested name ids: %d distinct (producer: 638); in 894..944: %s" % (len(tot), sorted(i for i in tot if 894 <= i <= 944)))
