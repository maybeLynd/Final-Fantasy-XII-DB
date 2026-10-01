"""sd127_leas.py - SWE2-AUDIT-SPEC (SD-127 review, 2026-09-30). Handed-on / indexed analysis of every rip lea near the
battle-HUD keys, and a full-form census around the 11 HUD keys OUTSIDE the package's block 01E0C000..01E0D100.

  L  every rip lea with target in [01E0BF00, 01E0D100) outside the console installer (001AF470..001B018F, the .pdata
     gap it occupies), plus every rip lea with target within 0x400 below any of the 11 outside keys: sdx.track() from the
     lea (linear candidate walk): memory accesses through the base (resolved address, width, indexed), calls with the
     base in an argument register (handed on), stores of the base.
  X  the 11 keys outside the block: every operand starting within 0x40 below .. the key in every form; covering ones.
  I  the indexed image-base-relative operands inside the block (from sd127_indep A) with the instructions before them,
     so the index bound can be read.
  Control: track(0060890A) (SD-141's handed-on base) must report call 005DEC50 with rdx = 02CB8160; track(0040032C)
  must report 01E0C590 handed to a callee.
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
HK = sorted(hud)
LO, HI = 0x01E0C000, 0x01E0D100
OUT = [k for k in HK if not (LO <= k < HI)]
INST = (0x001AF470, 0x001B0190)
fails = 0


def check(tag, ok, text):
    global fails
    fails += 0 if ok else 1
    print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))


def keys_in(a, w):
    return [k for k in HK if a <= k < a + max(w, 1)]


print("== L. lea bases")
leas = [x for x in sdx.rip_leas(0x01E0BF00, HI) if not (INST[0] <= x[0] < INST[1])]
for k in OUT:
    leas += sdx.rip_leas(k - 0x400, k + 1)
leas = sorted(set(leas))
flag = []
for s, r, t in leas:
    tgt, acc, calls, stores = sdx.track(s)
    hitk = [(a, txt, ad, w, ix) for a, txt, ad, w, ix, lea in acc if not lea and keys_in(ad, w)]
    idx = [(a, txt, ad, w) for a, txt, ad, w, ix, lea in acc if ix]
    mx = max([ad + max(w, 1) - tgt for a, txt, ad, w, ix, lea in acc if not lea] or [0])
    nk = HK[bisect.bisect_left(HK, tgt)] if bisect.bisect_left(HK, tgt) < len(HK) else None
    print("  %08X lea %-4s %08X root %08X | next key +0x%X | accesses %d (max extent +0x%X) indexed %d | handed on %d | stored %d%s" % (
        s, r, t, sdx.root(s) or 0, (nk - t) if nk else 0, len(acc), mx, len(idx), len(calls), len(stores),
        "  KEY-HIT" if hitk else ""))
    for c in calls:
        print("      hand-on %08X %s %s" % c)
    for a, txt, ad, w in idx:
        print("      indexed %08X %s  (base %08X w%d)" % (a, txt, ad, w))
    for x in stores:
        print("      stored  %08X %s" % x)
    for a, txt, ad, w, ix in hitk:
        print("      KEY     %08X %s -> %08X %s" % (a, txt, ad, [hud[k] for k in keys_in(ad, w)]))
    if hitk or calls or idx or stores:
        flag.append(s)
print("  %d lea sites walked; %d with a hand-on, index, store or key hit" % (len(leas), len(flag)))

print("== X. operands near the 11 keys outside the block")
xcov = []
for k in OUT:
    A = sdx.window(k, k + 4, 0x40)
    nonrip = [h for h in A if h["form"] != "rip"]
    cov = [h for h in A if h["covers"]]
    wide = [h for h in cov if h["start"] != k]
    print("  %08X %-30s operands %d (non-rip %d); covering %d (%s)%s" % (
        k, hud[k], len(A), len(nonrip), len(cov), ", ".join("%08X %s w%d" % (h["addr"], h["form"], h["width"]) for h in cov),
        "; WIDE/misaligned: " + ", ".join(sdx.fmt(h) for h in wide) if wide else ""))
    for h in nonrip:
        print("     NONRIP " + sdx.fmt(h))
    xcov += [h for h in cov if h["form"] != "rip"]

print("== I. indexed image-base-relative operands in the block, with context")
for a in (0x00266588, 0x00266B83, 0x0027E122, 0x002AECA3, 0x002AEE26):
    print("  -- %08X  root %08X" % (a, sdx.root(a) or 0))
    o = sdx.off(a - 0x40)
    ins = [i for i in sdx.md.disasm(sdx.raw[o:o + 0x50], a - 0x40)]
    # keep the decode that lands on a
    if not any(i.address == a for i in ins):
        for back in range(0x40, 0, -1):
            ins = list(sdx.md.disasm(sdx.raw[sdx.off(a - back):sdx.off(a - back) + back + 8], a - back))
            if any(i.address == a for i in ins):
                break
    for i in ins:
        if i.address <= a:
            print("     %08X %s %s" % (i.address, i.mnemonic, i.op_str))

print("== controls")
t, acc, calls, st = sdx.track(0x0060890A)
check("T1", any(c[1] == "0x5dec50" and c[2].get("rdx") == "02CB8160" for c in calls), "track() reports SD-141's hand-on "
      "00608999 call 005DEC50 rdx=02CB8160")
t, acc, calls, st = sdx.track(0x0040032C)
check("T2", any("01E0C590" in c[2].values() for c in calls), "track() reports 004001D0 handing 01E0C590 on: %s" % calls[:3])
check("X0", not xcov, "no non-rip operand covers any of the 11 outside keys")
print("FAILS %d" % fails)
