"""sn1_q3_x_content.py - OPUS (Claude Opus 5.5), 2026-09-28. DATA from the archive (the four .dbg/.sbn/.ebp files).
SN-1's residue after FABLE's q3 decode (_index/candidates/sn1-q3-page-map/): q3 = {u32 X; u32 map[E]; pad}, and only the
head word X is unexplained. FRONTIER's re-scope (batch-K extension, FABLE-REQ-FRONTIER-SN1-RULING-PREMISE) left open
whether X is statically answerable or OEB. This narrows it; it does not answer it.

  G  X FOLLOWS THE INSTRUCTION STREAM, NOT POSITION: five groups of scopes share one shape (the same opcode and length
     sequence) while their variable ids and literals differ, across modules and code positions (and, in four of the five,
     source lines; sc0 is the shared systemctrl.ath header).
     In the four groups whose pattern of 16-bit immediates >= 0x100 is the same, X is the same - {ctrl, btlctrl, evctrl,
     mapctrl} sc0 (X 3), btlctrl sc10 / mapctrl sc6 (6), btlctrl sc12 / sc16 / mapctrl sc2 (6), evctrl sc6 / sc8 (11);
     in the one group where that pattern differs (btlctrl sc18 / sc19, below) X differs. A signed-byte class (>= 0x80)
     is not the split: btlctrl sc10 / mapctrl sc6 differ in it and share X
  P  AND OF MORE THAN THE MAP, THE LAYOUT OR THE TEXT LENGTH: btlctrl sc18 / sc19 have the same q0 instruction layout,
     the same q3 map and code differing only at bytes 33-34 - the event id pushed for eventread (0x62, ev_evt_t0098,
     against 0x1F9, ev_evt_t0505) - yet X = 1 / 2; sc19's source span is the SHORTER (183 against 188 bytes)
  B  NOT A 64-BYTE PAGE COUNT OF ANY GRID: mapctrl sc1's X = 254 exceeds the 252 64-byte pages its 16,028 code bytes
     can touch under any alignment
  N  THREE LAW FAMILIES, each fails: (1) distinct (block, line // K) pages over q0's records, K 16 / 32 / 64, 1- or
     0-based, logical or physical lines, instruction starts or all records; (2) scope-relative P-byte code pages
     containing byte value v, P 8..128, v 0..255, +0 / +1; (3) a compact-encoding size (3-byte ops with an immediate
     < 256 counted as 2 bytes: all, pushes only, or signed-byte range) under ceil / floor+1 / round (size / K) + c,
     K 8..128, c -1..1. The best reaches, in order, fewer than 12, 28 and 33 of the 50 scopes
  C  CONTROL: search (3), with no compaction, recovers E = ceil(codeBytes / 32) in 50 of 50 - it finds a law of this
     shape when the target has one
Not claimed: what X counts, or that it is unanswerable; no reader of q3 exists in the image (d450f72e0), so the
consumer cannot be read either. FABLE's x_negatives.py (N1-N3, C) holds the earlier families.
Usage: python sn1_q3_x_content.py [dir]
"""
import collections, importlib.util, math, os, struct, sys
DIR = sys.argv[1] if len(sys.argv) > 1 else r"D:/FFXII_TZA_extract/ps2data/image/ff12/in/bin"
HERE = os.path.dirname(os.path.abspath(__file__))
fails = 0
def check(tag, ok, text):
    global fails
    fails += not ok; print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))
_ps = importlib.util.spec_from_file_location("sn1_prereq", os.path.join(HERE, "sn1_prereq.py")); PR = importlib.util.module_from_spec(_ps); _ps.loader.exec_module(PR)
Q, why = PR.run(os.path.join(HERE, "sn1_q0_domain.py"), [sys.argv[0], DIR], ("I", "A", "R", "Z", "E", "C"), ("scopes", "groups_of", "lines_of"))
check("Q", why is None, "prerequisite sn1_q0_domain.py: %s" % (why or "exit 0, PASS I A R Z E C, FAILS 0"))
if why: print("FAILS %d" % fails); sys.exit(1)
MODS = ("ctrl", "btlctrl", "evctrl", "mapctrl")
X, N0 = {}, {}
for m in MODS:
    b = open(os.path.join(DIR, m + ".dbg"), "rb").read(); o0 = struct.unpack_from("<I", b, 0)[0]; ns = struct.unpack_from("<I", b, o0)[0]
    offs = struct.unpack_from("<%dI" % (4 * ns + 1), b, o0 + 4)
    for i in range(ns):
        X[(m, i)] = struct.unpack_from("<I", b, offs[4 * i + 3])[0]; N0[(m, i)] = (offs[4 * i + 1] - offs[4 * i]) // 4
EBP = {m: open(os.path.join(DIR, m + ".ebp"), "rb").read()[0x80:] for m in MODS}
SBN = {m: open(os.path.join(DIR, m + ".sbn"), "rb").read() for m in MODS}
S = {}
for m, i, recs, ce, q, st, nxt in Q.scopes:
    code = EBP[m][st:st + ce]; starts = [k for k in range(ce) if recs[k][2] == 1]
    ins = [(code[k], (starts[a + 1] if a + 1 < len(starts) else ce) - k, code[k + 1:(starts[a + 1] if a + 1 < len(starts) else ce)]) for a, k in enumerate(starts)]
    S[(m, i)] = dict(code=code, recs=recs[:ce], ins=ins, lines=(min(r[0] for r in recs[:ce]), max(r[0] for r in recs[:ce])), st=st)
check("X", len(S) == 50 and all(0 <= N0[k] - len(S[k]["code"]) <= 3 for k in S), "50 scopes; q0 length = code bytes + 0..3 pad in every scope")
# G
grp = collections.defaultdict(list)
for k, s in S.items(): grp[tuple((op, ln) for op, ln, arg in s["ins"])].append(k)
multi = sorted(sorted(v) for v in grp.values() if len(v) > 1)
def wide(k, lim): return tuple(struct.unpack("<H", arg)[0] >= lim for op, ln, arg in S[k]["ins"] if ln == 3)
def sbyte(k): return tuple(0x80 <= struct.unpack("<H", arg)[0] < 0xFF80 for op, ln, arg in S[k]["ins"] if ln == 3)
same_w = [v for v in multi if len({wide(k, 0x100) for k in v}) == 1]
diff_w = [v for v in multi if len({wide(k, 0x100) for k in v}) > 1]
g_ok = (len(multi) == 5 and len(same_w) == 4 and diff_w == [[("btlctrl", 18), ("btlctrl", 19)]]
        and all(len({X[k] for k in v}) == 1 for v in same_w) and all(len({X[k] for k in v}) == len(v) for v in diff_w)
        and all(len({S[k]["code"] for k in v}) > 1 for v in multi) and sum(len({S[k]["lines"] for k in v}) > 1 for v in multi) == 4
        and len({sbyte(k) for k in (("btlctrl", 10), ("mapctrl", 6))}) == 2 and X[("btlctrl", 10)] == X[("mapctrl", 6)])
check("G", g_ok, "same-shape groups %s: X %s; same >= 0x100 pattern and one X in %d, different pattern and different X in %s; "
      "btlctrl sc10 / mapctrl sc6 differ in the >= 0x80 class and share X %d"
      % (multi, [[X[k] for k in v] for v in multi], len(same_w), diff_w, X[("btlctrl", 10)]))
# P
a, b_ = S[("btlctrl", 18)], S[("btlctrl", 19)]
diff = [j for j in range(len(a["code"])) if a["code"][j] != b_["code"][j]]
def span(m, s):
    g = Q.groups_of[m][0]; lo, hi = s["lines"]
    z = Q.lines_of[m][0][g[hi - 1][-1]]
    return SBN[m].index(b"\0", z) - Q.lines_of[m][0][g[lo - 1][0]]
sa, sb = span("btlctrl", a), span("btlctrl", b_)
check("P", len(a["code"]) == len(b_["code"]) == 48 and diff == [33, 34] and a["code"][32:35] == bytes([0x4F, 0x62, 0x00]) and b_["code"][32:35] == bytes([0x4F, 0xF9, 0x01])
      and [r[2] for r in a["recs"]] == [r[2] for r in b_["recs"]] and (X[("btlctrl", 18)], X[("btlctrl", 19)]) == (1, 2) and sb < sa,
      "btlctrl sc18 / sc19: code differs only at bytes %s (push 0x62 / 0x1F9), same instruction layout, X 1 / 2; source span %d / %d bytes" % (diff, sa, sb))
# B
n1 = N0[("mapctrl", 1)]
check("B", X[("mapctrl", 1)] == 254 and (n1 + 63) // 64 + 1 == 252, "mapctrl sc1: X %d > %d, the most 64-byte pages %d bytes can touch" % (X[("mapctrl", 1)], (n1 + 63) // 64 + 1, n1))
# N (1) line pages
best1 = 0
for K in (16, 32, 64):
    for zero in (0, 1):
        for phys in (0, 1):
            for sel in ("starts", "all"):
                g = 0
                for (m, i), s in S.items():
                    pages = set()
                    for L, blk, fl in (r[:3] for r in s["recs"]):
                        if sel == "starts" and fl != 1: continue
                        v = L
                        if phys:
                            gg = Q.groups_of[m][blk]
                            if not 1 <= L <= len(gg): continue
                            v = gg[L - 1][0] + 1
                        pages.add((blk, (v - zero) // K))
                    g += len(pages) == X[(m, i)]
                best1 = max(best1, g)
# N (2) byte-value pages
best2 = 0
for P in (8, 16, 32, 64, 128):
    for v in range(256):
        cnt = {k: sum(1 for p in range(0, len(s["code"]), P) if v in s["code"][p:p + P]) for k, s in S.items()}
        for c in (0, 1):
            best2 = max(best2, sum(cnt[k] + c == X[k] for k in S))
# N (3) compact size, and C
def size(ins, rule):
    t = 0
    for op, ln, arg in ins:
        if ln == 3 and rule != "none":
            v = struct.unpack("<H", arg)[0]
            if (rule == "all" and v < 256) or (rule == "push" and op == 0x4F and v < 256) or (rule == "signed" and (v < 128 or v >= 0xFF80)):
                t += 2; continue
        t += ln
    return t
def law(target, rules):
    best = 0
    for rule in rules:
        sz = {k: size(s["ins"], rule) for k, s in S.items()}
        for K in range(8, 129):
            for f in ("ceil", "floor1", "round"):
                for c in (-1, 0, 1):
                    best = max(best, sum(((math.ceil(v / K) if f == "ceil" else v // K + 1 if f == "floor1" else int(v / K + 0.5)) + c) == target[k] for k, v in sz.items()))
    return best
best3 = law(X, ("all", "push", "signed", "none"))
check("N", best1 < 12 and best2 < 28 and best3 < 33, "best fits of X: line pages %d, byte-value pages %d, compact size %d, of 50" % (best1, best2, best3))
E = {k: 1 + (N0[k] - 1) // 32 for k in S}
check("C", law(E, ("none",)) == 50, "the size-law search recovers E = ceil(codeBytes / 32) in %d of 50" % law(E, ("none",)))
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
