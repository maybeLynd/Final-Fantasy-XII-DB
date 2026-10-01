# (FABLE, Claude Opus 5.5, 2026-09-26) - published copy; runs from any working directory.
# w3_census.py [ROOT...] - what the packed namespace's member word w3 measures, over every shipped .phyre file.
#
# Population control: the file and member totals must equal the contract's full-archive figures (35,984 files,
# 2,192,621 members); a different root prints a different population and FAILS instead of silently answering for it.
#
# Checks:
#  L1 classes split by the w3 of their object-pointer members (w4 bit 1): 1 or 8, never both in one class.
#  L2 in the 1-byte group every class is PACKED: sorted by w2, w2[0] == 0 and w2[i+1] == w2[i] + w3[i] * max(1, w5[i]),
#     with no alignment padding (records are not stored in offset order); PArray-class members there are 5 bytes wide.
#  L3 in the 8-byte group every member's w2 equals the runtime-registered offset (phyre-field-schema.tsv), and
#     PArray-class members are 16 bytes wide - the native layout.
#  L4 D3D11_RENDER_TARGET_BLEND_DESC's member widths sum to 29 (seven 4-byte fields and a 1-byte mask), the w3 that
#     CD3D11_BLEND_DESC.RenderTarget carries; the native sizeof is 32, so 29 is the packed width, not the sizeof.
#  L5 in every packed-layout class (the 8-byte group excluded), class word w1's low 28 bits = the parent's packed
#     size + the members' width sum: the class's cumulative packed size.
# Sensitivity: L2's packing test must reject a planted native class (PParameterBuffer, first member at 8), so a test
# that passes everything cannot pass L2.
import os, struct, sys, collections
ROOTS = sys.argv[1:] or ["D:/FFXII_TZA_extract"]
HERE = os.path.dirname(os.path.abspath(__file__))
TSV = os.path.join(HERE, "..", "..", "Reflection-And-Class-Metadata", "phyre-field-schema.tsv")
rt = {}
for l in open(TSV, encoding="utf-8"):
    p = l.rstrip("\n").split("\t")
    if p[0] == "class_leaf" or len(p) < 6: continue
    try: rt.setdefault((p[0], p[2]), set()).add(int(p[3], 16))
    except ValueError: pass
files = []
for R in ROOTS:
    for dp, dn, fn in os.walk(R):
        files += [os.path.join(dp, f) for f in fn if f.lower().endswith(".phyre")]
nmem = 0
cls_ptr = collections.defaultdict(set)          # class -> pointer w3 values
cls_info = {}                                   # class -> (members as (name, w2, w3, w4, w5, typename)) first seen
cls_w1 = {}                                     # class -> class record word 1
cls_parent = {}                                 # class -> parent class name (class w0, 1-based)
parr = collections.defaultdict(collections.Counter)   # group-less: class -> Counter of PArray-member w3
for path in sorted(files):
    d = open(path, "rb").read()
    hs, ns = struct.unpack_from("<II", d, 4); b = d[hs:hs + ns]
    A, nC, nM, sp = struct.unpack_from("<IIII", b, 8)
    nmem += nM
    base = 0x20 + 4 * A; mb = base + 36 * nC; pool = mb + 24 * nM
    s = lambda o: b[pool + o:b.find(b"\0", pool + o)].decode("latin-1")
    cls = [struct.unpack_from("<9I", b, base + 36 * k) for k in range(nC)]
    names = [s(w[2]) for w in cls]
    mi = 0
    for k in range(nC):
        cn = names[k]
        ms = []
        for q in range(cls[k][3]):
            m = struct.unpack_from("<6I", b, mb + 24 * (mi + q))
            tn = s(struct.unpack_from("<I", b, 0x20 + 4 * m[1])[0]) if m[1] < A else names[m[1] - A - 1]
            ms.append((s(m[0]), m[2], m[3], m[4], m[5], tn))
            if m[4] & 2: cls_ptr[cn].add(m[3])
            if tn.startswith("PArray<") and not m[4] & 2: parr[cn][m[3]] += 1
        mi += cls[k][3]
        cls_info.setdefault(cn, ms); cls_w1.setdefault(cn, cls[k][1])
        if cls[k][0]: cls_parent.setdefault(cn, names[cls[k][0] - 1])
fails = 0
def check(name, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", name, detail)); fails += (not ok)
check("population: 35,984 files and 2,192,621 members (the contract's full-archive figures)",
      len(files) == 35984 and nmem == 2192621, "(%d files, %d members)" % (len(files), nmem))
both = [c for c, v in cls_ptr.items() if len(v) > 1]
g1 = sorted(c for c, v in cls_ptr.items() if v == {1}); g8 = sorted(c for c, v in cls_ptr.items() if v == {8})
other = sorted(c for c, v in cls_ptr.items() if len(v) == 1 and not v <= {1, 8})
check("L1 pointer w3 is 1 or 8, one value per class", not both and not other,
      "(1-byte %d classes, 8-byte %d classes; mixed %s, other %s)" % (len(g1), len(g8), both, other))
print("     8-byte group: %s" % ", ".join(g8))
def start_of(c):
    # a derived class's packed members begin where its parent's packed size (the parent's w1 low 28 bits) ends:
    # PAnimationChannelBase starts at 13 = PAnimationChannelTarget's size, PAnimationChannel at 18 = its parent's
    par = cls_parent.get(c)
    return (cls_w1[par] & 0x0FFFFFFF) if par in cls_w1 else 0
def packed(ms, start=0):
    # records are not stored in offset order (PLODGroup lists m_levels at 42 first), so sort by w2 before testing
    ms = sorted(ms, key=lambda m: m[1])
    return bool(ms) and ms[0][1] == start and all(ms[i + 1][1] == ms[i][1] + ms[i][2] * max(1, ms[i][4]) for i in range(len(ms) - 1))
def width(ms): return sum(m[2] * max(1, m[4]) for m in ms)
np1 = [c for c in g1 if not packed(cls_info[c], start_of(c))]
check("L2 every 1-byte-group class is packed (cumulative offsets from its parent's packed size, no padding)", not np1, str(np1[:8]))
p1 = collections.Counter(v for c in g1 for v in parr.get(c, {}))
check("L2 PArray members in the 1-byte group are 5 bytes wide", set(p1) <= {5}, str(dict(p1)))
check("L2 sensitivity: the planted native class PParameterBuffer (first member at 8) is NOT packed",
      "PParameterBuffer" in cls_info and not packed(cls_info["PParameterBuffer"]))
mism, unjoined, joined8 = [], [], 0
for c in g8:
    leaf = c.split("::")[-1]
    for (mn, w2, w3, w4, w5, tn) in cls_info[c]:
        r = rt.get((leaf, mn))
        if r is None: unjoined.append((c, mn)); continue
        joined8 += 1
        if w2 not in r: mism.append((c, mn, w2, sorted(r)))
check("L3 every joined 8-byte-group member's w2 is its runtime-registered offset", not mism and joined8 > 0,
      "(%d joined, %d without a runtime row: %s; mismatches %s)" % (joined8, len(unjoined), unjoined[:4], mism[:4]))
p8 = collections.Counter(v for c in g8 for v in parr.get(c, {}))
check("L3 PArray members in the 8-byte group are 16 bytes wide", set(p8) <= {16}, str(dict(p8)))
bd = cls_info.get("D3D11_RENDER_TARGET_BLEND_DESC")
if bd:
    widths = [m[2] for m in bd]
    print("     D3D11_RENDER_TARGET_BLEND_DESC: %s" % [(m[0], m[1], m[2]) for m in bd])
    rtm = [m for m in cls_info.get("CD3D11_BLEND_DESC", []) if m[0] == "RenderTarget"]
    check("L4 blend-desc member widths sum to 29 and RenderTarget carries w3 = 29",
          sum(widths) == 29 and packed(bd) and rtm and rtm[0][2] == 29, "(widths %s, RenderTarget %s)" % (widths, rtm))
else:
    check("L4 D3D11_RENDER_TARGET_BLEND_DESC present", False)
# L5: class w1's low 28 bits against the width sum, for every packed class in the corpus (not only pointer carriers)
agree = collections.Counter()
for c, ms in cls_info.items():
    if not ms or c in g8 or not packed(ms, start_of(c)): continue
    agree[(cls_w1[c] >> 28, (cls_w1[c] & 0x0FFFFFFF) == start_of(c) + width(ms))] += 1
print("     L5 packed classes by w1 kind nibble and (low 28 bits == width sum): %s" % dict(sorted(agree.items())))
bad = sum(n for (k, ok), n in agree.items() if not ok)
check("L5 in every packed-layout class, class w1's low 28 bits = parent's packed size + the members' width sum", bad == 0, "(%d disagree)" % bad)
withm = [c for c, ms in cls_info.items() if ms]
pk = [c for c in withm if c not in g8 and packed(cls_info[c], start_of(c))]
neither = sorted(c for c in withm if c not in g8 and c not in pk)
print("     classes with members %d: packed-layout %d, native (8-byte pointer) group %d, neither %d %s"
      % (len(withm), len(pk), len(g8), len(neither), neither[:12]))
print("FAILS %d" % fails); sys.exit(1 if fails else 0)
