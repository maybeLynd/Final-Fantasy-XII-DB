"""sd127_indep.py - SWE2-AUDIT-SPEC independent re-derivation for SD-127 (battle-HUD layout keys read through a base).
Uses ../auditspec-review-sd141-0930/sdx.py (pefile + capstone + numpy, certified image; not retool.py / `pe`).

The key set is re-built from the same two data files the package names (the battle-HUD page's backticked
addresses x layout-key-readers.tsv), so the set is the package's definition, not re-derived.

  A  every .text operand starting in [01E0C000 - 0x40, 01E0D100) in every form (rip / image-base-relative with any
     base or index / absolute disp32) - for each HUD key: covering operands by form; every indexed or non-rip operand
     with its nearest HUD key at or above its start.
  B  every rip lea with target in [01E0C000 - 0x100, 01E0D100): the nearest HUD key at or above the target and the
     distance (the README's "no other lea target within 0x40 of a HUD key").
  C  relocations and raw abs64/abs32/rva32 values into [01E0C000, 01E0D100).
  Controls: K1 SD-121's 0036E414 image-base-relative operand; K2 a scale-1 base+index operand in the block is decoded
  and flagged indexed; K3 004001D0's lea of 01E0C590 appears in B; K4 the DIR64 control of sd141_indep (01F2E330).
"""
import bisect, csv, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "auditspec-review-sd141-0930"))
import sdx  # noqa: E402

DB = os.path.join(HERE, "..", "..", "..")
page = open(os.path.join(DB, "16-UI", "Battle-Hud", "the-battle-hud-layout-readers.md"), encoding="utf-8").read()
cited = set(int(x, 16) for x in re.findall(r"`(00[0-9A-F]{6})`", page))
rows = list(csv.DictReader(open(os.path.join(DB, "16-UI", "Layout-Parameter-System", "members", "layout-key-readers.tsv"),
                                encoding="utf-8"), delimiter="\t"))
hud = {int(r["global"], 16): r["key"] for r in rows if int(r["reader"], 16) in cited}
allkeys = {int(r["global"], 16): r["key"] for r in rows}
HK = sorted(hud)
LO, HI = 0x01E0C000, 0x01E0D100
fails = 0


def check(tag, ok, text):
    global fails
    fails += 0 if ok else 1
    print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))


def next_key(a):
    j = bisect.bisect_left(HK, a)
    return HK[j] if j < len(HK) else None


print("HUD keys: %d (TSV rows %d, distinct TSV globals %d); lowest %08X highest %08X" % (
    len(hud), len(rows), len(allkeys), HK[0], HK[-1]))

print("== A. operands in the block")
A = sdx.window(LO, HI, 0x40)
print("  operands starting in window: %d (rip %d, ibrel %d, abs32 %d)" % (
    len(A), sum(h["form"] == "rip" for h in A), sum(h["form"] == "ibrel" for h in A), sum(h["form"] == "abs32" for h in A)))
nonrip = [h for h in A if h["form"] != "rip"]
for h in nonrip:
    k = next_key(h["start"])
    print("  NONRIP " + sdx.fmt(h), " root %08X" % (sdx.root(h["addr"]) or 0),
          " next HUD key %s +0x%X" % ("%08X" % k if k else "-", (k - h["start"]) if k else 0))
cov = {}
for h in A:
    if h["lea"]:
        continue
    w = max(h["width"], 1)
    for k in HK:
        if h["start"] <= k < h["start"] + w:
            cov.setdefault(k, []).append(h)
wide_off = [(k, h) for k, hs in cov.items() for h in hs if h["start"] != k]
print("  operands covering a HUD key from a different start (wide / misaligned): %d" % len(wide_off))
for k, h in wide_off:
    print("    key %08X %-34s <- %s" % (k, hud[k], sdx.fmt(h)))
nonrip_cov = [(k, h) for k, hs in cov.items() for h in hs if h["form"] != "rip"]
print("  non-rip operands covering a HUD key: %d" % len(nonrip_cov))

print("== B. rip leas into the block")
B = sdx.rip_leas(LO - 0x100, HI)
for s, r, t in sorted(B, key=lambda x: (x[2], x[0])):
    k = next_key(t)
    d = (k - t) if k is not None else None
    print("  %08X lea %-4s -> %08X  root %08X  next HUD key %s at +0x%X%s%s" % (
        s, r, t, sdx.root(s) or 0, "%08X %s" % (k, hud[k]) if k else "-", d if d is not None else 0,
        "  <= 0x40" if d is not None and d <= 0x40 else "", "  (console installer)" if sdx.root(s) == 0x001AF470 else ""))
near = [(s, r, t) for s, r, t in B if sdx.root(s) != 0x001AF470 and next_key(t) is not None and next_key(t) - t <= 0x40]
print("  leas outside 001AF470: %d; with a HUD key within 0x40 at or above the target: %d -> %s" % (
    sum(1 for s, r, t in B if sdx.root(s) != 0x001AF470), len(near),
    sorted(set("%08X@%08X" % (sdx.root(s) or 0, t) for s, r, t in near))))

print("== C. stored pointers into the block")
C1 = sdx.relocs_into(LO, HI)
print("  relocations: %d %s" % (len(C1), ["%08X->%08X" % x for x in C1]))
C2 = [r for r in sdx.data_refs(LO, HI) if r[3] != ".text"]
print("  raw values outside .text: %d" % len(C2))
for r in C2[:30]:
    print("    %s at %08X = %08X (%s)" % r)

print("== controls")
k1 = sdx.window(0x022D97B0, 0x022D97B4, 0)
check("K1", any(h["addr"] == 0x0036E414 and h["form"] == "ibrel" for h in k1), "image-base-relative: 0036E414 decoded")
k2 = [h for h in nonrip if h["indexed"] and "*" not in h["op"] and h["base"]]
check("K2", len(k2) > 0, "scale-1 base+index image-base-relative operands in the block are decoded: %s" % (
    ["%08X %s" % (h["addr"], h["op"]) for h in k2]))
check("K3", any(s >= 0x004001D0 and t == 0x01E0C590 and sdx.root(s) == 0x004001D0 for s, r, t in B),
      "lea control: 004001D0's lea of 01E0C590 found")
check("K4", len(sdx.relocs_into(0x01F2E330, 0x01F2E370)) >= 6, "relocation control (01F2E330 self pointers)")
print("FAILS %d" % fails)
