"""t0_scope.py - SN-1: how far the operand -> T0 binding is proven, per module and index range (FABLE, Claude Opus 5.5,
2026-09-28, correcting this record's T2 section). DATA from the archive (.dbg T0 / T2, .ebp operand table).

  S1 the .ebp operand table (EBP2 chunk +0x28) and the .dbg T0 table have equal counts in all four modules (56 / 92 / 115 / 127);
     equal counts do not by themselves bind entry n to T0[n]
  S2 the T2 route (descriptor -> T2 record name) covers 106 of the 390 entries: 71 whose T2 record carries the single name T0[n]
     and 35 whose T2 record carries two names, T0[n] among them; none names only T0[n + 1]. Per module the covered indices are
     ctrl 0; btlctrl 0-4; evctrl 0-0x43; mapctrl 1-2, 4-0x21
  S3 the other 284 entries have no T2 record (descriptor classes 1 file, 2 local, 4, 7 array); for them the binding rests on
     source-text samples only
  S4 V1's five samples: only mapctrl 0x20 lies in a T2-covered range; evctrl 0x61, btlctrl 0x0D and 0x0E and mapctrl 0x52 have no
     T2 record - so the T2 route corroborates one of the five, not V1 as a whole
  C  control: against T0 shifted by one entry the same T2 test finds no single-name T0[n] match in any module, so S2 would see a
     shifted table
  Not claimed: T0[operand] for the 284 entries beyond the sampled ones, the compiler's rule, or live variable values
"""
import os, struct, sys
DIR = sys.argv[1] if len(sys.argv) > 1 else r"D:/FFXII_TZA_extract/ps2data/image/ff12/in/bin"
fails = 0
def ok(tag, cond, msg):
    global fails
    print(("PASS " if cond else "FAIL ") + tag + "  " + msg); fails += (not cond)
def load(m):
    b = open(os.path.join(DIR, m + ".dbg"), "rb").read()
    h = struct.unpack_from("<16I", b, 0); pool, T0, T2 = h[2], h[1], h[5]
    name = lambda p: b[pool + p:b.index(bytes([0]), pool + p)].decode("latin-1")
    c0 = struct.unpack_from("<I", b, T0)[0]; T0n = [name(x) for x in struct.unpack_from("<%dI" % c0, b, T0 + 4)]
    c2 = struct.unpack_from("<I", b, T2)[0]; P = struct.unpack_from("<%dI" % (2 * c2), b, T2 + 4)
    t2 = {}
    for i in range(c2): t2.setdefault(P[2 * i], []).append(name(P[2 * i + 1]))
    e = open(os.path.join(DIR, m + ".ebp"), "rb").read()
    o0 = struct.unpack_from("<I", b, 0)[0]; ns = struct.unpack_from("<I", b, o0)[0]
    offs = struct.unpack_from("<%dI" % (4 * ns + 1), b, o0 + 4)
    ins0 = sum(b[offs[0] + 4 * k + 3] for k in range((offs[1] - offs[0]) // 4))
    base = None
    for o in range(0, len(e) - 0x40, 4):
        if struct.unpack_from("<I", e, o + 0xC)[0] == ins0 and struct.unpack_from("<I", e, o + 0x24)[0] == 0:
            for bs in range(0, o, 4):
                if struct.unpack_from("<I", e, bs + 0x18)[0] + 4 + bs == o: base = bs; break
            if base is not None: break
    tbl = base + struct.unpack_from("<I", e, base + 0x28)[0]; cnt = struct.unpack_from("<I", e, tbl)[0]
    desc = [struct.unpack_from("<I", e, tbl + 4 + 8 * n)[0] for n in range(cnt)]
    return T0n, t2, desc
def classify(T0n, t2, desc):
    out = {}
    for n, d in enumerate(desc):
        names = t2.get(d, [])
        if not names: out[n] = "none"
        elif names == [T0n[n]]: out[n] = "single"
        elif T0n[n] in names: out[n] = "multi"
        elif n + 1 < len(T0n) and T0n[n + 1] in names: out[n] = "shifted"
        else: out[n] = "other"
    return out
MODS = ("ctrl", "btlctrl", "evctrl", "mapctrl")
D = {m: load(m) for m in MODS}
K = {m: classify(*D[m]) for m in MODS}
counts = {m: (len(D[m][0]), len(D[m][2])) for m in MODS}
ok("S1", all(a == b for a, b in counts.values()) and [counts[m][0] for m in MODS] == [56, 92, 115, 127],
   "T0 / operand-table counts %s" % counts)
tot = {k: sum(list(K[m].values()).count(k) for m in MODS) for k in ("single", "multi", "shifted", "other", "none")}
def ranges(m):
    v = [n for n, k in K[m].items() if k in ("single", "multi")]; out = []; s = p = None
    for x in v:
        if s is None: s = p = x
        elif x == p + 1: p = x
        else: out.append((s, p)); s = p = x
    if s is not None: out.append((s, p))
    return ",".join("%X-%X" % r if r[0] != r[1] else "%X" % r[0] for r in out)
cov = {m: ranges(m) for m in MODS}
ok("S2", tot["single"] == 71 and tot["multi"] == 35 and tot["shifted"] == 0 and tot["other"] == 0
   and cov == {"ctrl": "0", "btlctrl": "0-4", "evctrl": "0-43", "mapctrl": "1-2,4-21"},
   "T2-covered: single %d, two-name %d, shifted %d, other %d; ranges %s" % (tot["single"], tot["multi"], tot["shifted"], tot["other"], cov))
cls = {}
for m in MODS:
    for n, k in K[m].items():
        if k == "none": c = (D[m][2][n] >> 24) & 7; cls[c] = cls.get(c, 0) + 1
ok("S3", tot["none"] == 284 and set(cls) == {1, 2, 4, 7}, "no T2 record: %d entries, by descriptor class %s" % (tot["none"], dict(sorted(cls.items()))))
samples = {("evctrl", 0x61): "test_load_flg", ("btlctrl", 0x0D): "loop_flg", ("btlctrl", 0x0E): "mapjump_menu_flg",
           ("mapctrl", 0x52): "test", ("mapctrl", 0x20): "mp_debugmenu_flg"}
s4 = {"%s %X" % k: (D[k[0]][0][k[1]] == v, K[k[0]][k[1]]) for k, v in samples.items()}
ok("S4", all(a for a, _ in s4.values()) and [k for _, k in s4.values()].count("none") == 4 and s4["mapctrl 20"][1] == "single",
   "V1 samples (T0 name matches, T2 status): %s" % s4)
shifted = {m: sum(1 for k in classify(D[m][0][1:] + [""], D[m][1], D[m][2]).values() if k == "single") for m in MODS}
ok("C", not any(shifted.values()), "single-name matches against T0 shifted by one: %s" % shifted)
print("FAILS", fails); sys.exit(1 if fails else 0)
