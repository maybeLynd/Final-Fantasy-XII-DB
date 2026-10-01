# (FABLE, Claude Opus 5.5, 2026-09-26) - published copy; runs from any working directory.
# bl1_file_vs_runtime.py [ROOT...] - the packed namespace's member attribute word w4, read two ways over every shipped
# .phyre file: (1) its full vocabulary, with the members that carry bit 31 and bits 5-6; (2) a join of each member
# record to the runtime registrations in phyre-field-schema.tsv by (class name, member name), tabulating the runtime
# attribute against the file word. Record layout as the namespace page gives it: class record 9 words (w2 name,
# w3 member count), member record 6 words (w0 name, w4 attributes), members contiguous in class order.
# Control: the bit-31 total must equal the 2,239 the namespace page has published since before this script existed.
import os, struct, sys, collections
ROOTS = sys.argv[1:] or ["D:/FFXII MP Mod/extracted"]
HERE = os.path.dirname(os.path.abspath(__file__))
TSV = os.path.join(HERE, "..", "..", "Reflection-And-Class-Metadata", "phyre-field-schema.tsv")
rt = {}
for l in open(TSV, encoding="utf-8"):
    p = l.rstrip("\n").split("\t")
    if p[0] == "class_leaf" or len(p) < 6: continue
    try: rt.setdefault((p[0], p[2]), set()).add(int(p[5], 16))
    except ValueError: pass
multi = [k for k, v in rt.items() if len(v) > 1]
files = []
for R in ROOTS:
    for dp, dn, fn in os.walk(R):
        files += [os.path.join(dp, f) for f in fn if f.lower().endswith(".phyre")]
voc = collections.Counter(); ex = {}; b31 = collections.Counter(); b56 = collections.Counter()
pairs = collections.Counter(); diff = collections.Counter(); joined = same = 0; jkeys = set()
for path in sorted(files):
    d = open(path, "rb").read()
    hs, ns = struct.unpack_from("<II", d, 4); b = d[hs:hs + ns]
    A, nC, nM, sp = struct.unpack_from("<IIII", b, 8)
    base = 0x20 + 4 * A; mb = base + 36 * nC; pool = mb + 24 * nM
    s = lambda o: b[pool + o:b.find(b"\0", pool + o)].decode("latin-1")
    mi = 0
    for k in range(nC):
        w = struct.unpack_from("<9I", b, base + 36 * k); cn = s(w[2])
        for q in range(w[3]):
            m = struct.unpack_from("<6I", b, mb + 24 * (mi + q)); mn = s(m[0]); a = m[4]
            voc[a] += 1; ex.setdefault(a, "%s::%s" % (cn, mn))
            if a & 0x80000000: b31["%s::%s" % (cn.split("<")[0], mn)] += 1
            if a & 0x60: b56["%s::%s = 0x%X" % (cn, mn, a)] += 1
            if (cn, mn) in rt:
                joined += 1; jkeys.add((cn, mn)); ra = next(iter(rt[(cn, mn)]))
                pairs[(ra, a)] += 1
                if ra == a: same += 1
                else: diff["%s::%s runtime 0x%X file 0x%X" % (cn, mn, ra, a)] += 1
        mi += w[3]
print("files %d, member records %d" % (len(files), sum(voc.values())))
print("\n(1) w4 vocabulary:")
for a, n in sorted(voc.items()): print("  0x%08X %7d  e.g. %s" % (a, n, ex[a]))
print("  bit 31 on:", dict(b31), "total", sum(b31.values()))
print("  bit 1 without bit 31:", sum(n for a, n in voc.items() if a & 2 and not a & 0x80000000),
      " bit 1 with bit 31:", sum(n for a, n in voc.items() if a & 2 and a & 0x80000000))
print("  bits 5-6 on %d distinct members, %d records" % (len(b56), sum(b56.values())))
for k, n in sorted(b56.items()): print("    %5d  %s" % (n, k))
print("\n(2) join to the runtime schema (multi-valued runtime keys: %d)" % len(multi))
print("  joined %d records over %d fields; identical %d" % (joined, len(jkeys), same))
for (ra, a), n in sorted(pairs.items()): print("  runtime 0x%02X -> file 0x%08X : %d" % (ra, a, n))
for k, n in sorted(diff.items()): print("  differs: %5d  %s" % (n, k))
print("\ncontrol (bit-31 total == 2,239, the namespace page's published figure):",
      "PASS" if sum(b31.values()) == 2239 else "FAIL (%d)" % sum(b31.values()))
