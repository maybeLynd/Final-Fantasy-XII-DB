"""sn1_logical_lines.py - SN-1 (OPUS, Claude Opus 5.5, 2026-09-28): q0's line numbers count LOGICAL source lines. For
ASTRA-REQ-OPUS-SN1-LOGICAL-SOURCE (_experiments/evidence/sn1-evctrl-jump-binding/). DATA from the archive (the four .dbg /
.sbn / .ebp files); nothing runs. Written without ASTRA's code; the parser and resolver are sn1_q0_domain.py's.

  K  a continuation line is one whose last character, decoded cp932, is a backslash: 19 in ctrl block 0 (from line 40, the
     eventlist / mimiclist initialisers), 544 in evctrl block 0, none elsewhere. A byte test also flags mapctrl block 0 lines
     977 and 1187 - comments whose last byte 0x5C is the trail byte of a Shift-JIS character, not a backslash
  A  ASTRA's four evctrl anchors: scope 1 pc 22 / 34 / 3230 / 3242 start statements whose CALLPOPA (0x5D), on the same q0 line,
     calls verb 0x13 / 0x1A / 0x13 / 0x1A, named askpos / mesopenspeed by evctrl.dbg's own section 0; their q0 lines 417 / 418 / 708 / 709 are logical lines at
     physical 961 / 962 / 1252 / 1253, which call exactly those verbs; physical line - 1 shows neither
  V  every CALLPOPA instruction start in all four modules, its verb name (from the module's .dbg) looked for on the logical line
     and on the physical line q0 names: ctrl 17 both / 221 logical only / 0 physical only; evctrl 3 / 264 / 1; btlctrl 558 / 0 / 0;
     mapctrl 283 / 0 / 0. The one physical-only call (evctrl scope 9, record 56, q0 line 1733) is logical line 1733 = physical
     2277, `h_bosseventlist01()`, a macro whose body (physical 870-884) calls mesopenspeed: the logical reading holds there too.
     Calls whose name is on neither line are macro or alias calls; they decide nothing
  D  the domain does not change: logical line counts are 958 (ctrl 0) and 1912 (evctrl 0), the rest equal to the physical
     ones; the same six records exceed their block and the same nine equal its count (all in block 2, which has no
     continuation)
  C  controls: with the byte test (not cp932) the mapctrl calls after line 977 match only the physical line (156), so the
     Shift-JIS rule is required; with physical numbering ctrl and evctrl miss 485 calls the logical reading places
  L  sn1_q0_domain.py lookup() now returns the logical line (its physical lines); ASTRA's four anchors resolve to 961 / 962 /
     1252 / 1253 and the earlier btlctrl / mapctrl anchors are unchanged
A logical line is the attribution unit: it may hold several statements (ASTRA: the assignment at pc 16 shares line 417 with
the call at pc 22), so a coordinate names a logical line, not one statement. Not claimed: the compiler's rule itself, the
evctrl scope 1 q1 / jump-table binding (160 / 158), the six EOF+1 records' cause, SN-1 X.
Usage: python sn1_logical_lines.py [dir]
"""
import collections, contextlib, importlib.util, io, os, struct, sys
DIR = sys.argv[1] if len(sys.argv) > 1 else r"D:/FFXII_TZA_extract/ps2data/image/ff12/in/bin"
HERE = os.path.dirname(os.path.abspath(__file__))
fails = 0
def check(name, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", name, detail)); fails += not ok
spec = importlib.util.spec_from_file_location("q0dom", os.path.join(HERE, "sn1_q0_domain.py"))
Q = importlib.util.module_from_spec(spec); sys.argv = [sys.argv[0], DIR]; qfail = None
with contextlib.redirect_stdout(io.StringIO()):
    try: spec.loader.exec_module(Q)
    except SystemExit as e: qfail = e.code
check("I", qfail == 0, "sn1_q0_domain.py runs clean (FAILS 0); its parser is checked against sn1_layouts.py there")
MODS = ("ctrl", "btlctrl", "evctrl", "mapctrl")
SBN = {m: open(os.path.join(DIR, m + ".sbn"), "rb").read() for m in MODS}
def text(m, i, bk=0):
    s = SBN[m]; a = Q.lines_of[m][bk][i]; return s[a:s.index(b"\0", a)]
def byte_groups(s, starts):                       # the rejected detector: raw byte 0x5C at the end
    groups, cont = [], False
    for i, a in enumerate(starts):
        if not cont: groups.append([])
        groups[-1].append(i); cont = s[a:s.index(b"\0", a)].rstrip(b"\r\n \t").endswith(b"\\")
    return groups
cont = {(m, bk): [g[:-1] for g in G if len(g) > 1] for m in MODS for bk, G in enumerate(Q.groups_of[m])}
ncont = {k: sum(len(x) for x in v) for k, v in cont.items() if v}
bg = byte_groups(SBN["mapctrl"], Q.lines_of["mapctrl"][0]); bytecont = [g[0] + 1 for g in bg if len(g) > 1]
check("K", ncont == {("ctrl", 0): 19, ("evctrl", 0): 544} and cont[("ctrl", 0)][0][0] == 39 and bytecont == [977, 1187]
      and all(text("mapctrl", i - 1)[-1:] == b"\\" and 0x81 <= text("mapctrl", i - 1)[-2] <= 0xFC for i in bytecont),
      "continuation lines (cp932): %s; a byte test adds mapctrl block 0 lines %s, whose final 0x5C is a Shift-JIS trail byte" % (ncont, bytecont))
def verbs(m):
    b = open(os.path.join(DIR, m + ".dbg"), "rb").read(); pool = struct.unpack_from("<I", b, 8)[0]; N = {}
    for k, s in enumerate(struct.unpack_from("<16I", b, 0x2C)):
        c = struct.unpack_from("<I", b, s)[0]
        for i, o in enumerate(struct.unpack_from("<%dI" % c, b, s + 4) if c else ()):
            N[(k << 12) + i] = b[pool + o:b.index(b"\0", pool + o)]
    return N
EBP = {m: open(os.path.join(DIR, m + ".ebp"), "rb").read()[0x80:] for m in MODS}
scope = {(s[0], s[1]): s for s in Q.scopes}
def calls(m, groups_of):
    N = verbs(m); out = []
    for mm, i, recs, ce, q, st, nxt in Q.scopes:
        if mm != m: continue
        for k in range(min(ce, (nxt - st) if nxt else ce)):
            ln, bk, fl = recs[k]
            if fl != 1 or EBP[m][st + k] != 0x5D or ln == 0: continue
            nm = N.get(struct.unpack_from("<H", EBP[m], st + k + 1)[0])
            if not nm: continue
            G = groups_of[bk]
            lg = b" ".join(text(m, j, bk) for j in G[ln - 1]) if ln <= len(G) else b""
            ph = text(m, ln - 1, bk) if ln <= len(Q.lines_of[m][bk]) else b""
            has = lambda t: nm + b"(" in t.replace(b" (", b"(")
            out.append((i, k, ln, nm, has(lg), has(ph)))
    return out
N = verbs("evctrl"); m, i, recs, ce, q, st, nxt = scope[("evctrl", 1)]; aok = []
for pc, vid, ln, phys in ((22, 0x13, 417, 961), (34, 0x1A, 418, 962), (3230, 0x13, 708, 1252), (3242, 0x1A, 709, 1253)):
    v = Q.lookup(Q.groups_of["evctrl"], ce, pc, recs[pc]); nm = N[vid]
    k = pc                                             # pc is the statement's first instruction; its call carries the same line
    while k < ce and not (recs[k][2] == 1 and EBP["evctrl"][st + k] == 0x5D): k += 1
    aok.append(recs[pc][2] == 1 and all(recs[j][0] == ln for j in range(pc, k + 1)) and struct.unpack_from("<H", EBP["evctrl"], st + k + 1)[0] == vid and recs[pc][0] == ln
               and v[0] == "LINE" and v[1] + 1 == phys and nm + b"(" in text("evctrl", phys - 1).replace(b" (", b"(") and nm + b"(" not in text("evctrl", ln - 1))
check("A", aok == [True] * 4 and N[0x13] == b"askpos" and N[0x1A] == b"mesopenspeed",
      "evctrl scope 1 pc 22 / 34 / 3230 / 3242: CALLPOPA askpos / mesopenspeed, q0 lines 417 / 418 / 708 / 709 -> physical 961 / 962 / 1252 / 1253")
T = {}
for mm in MODS:
    cs = calls(mm, Q.groups_of[mm]); T[mm] = (sum(a and b for *_, a, b in cs), sum(a and not b for *_, a, b in cs), sum(b and not a for *_, a, b in cs))
odd = [(i, k, ln) for i, k, ln, nm, a, b in calls("evctrl", Q.groups_of["evctrl"]) if b and not a]
g1733 = Q.groups_of["evctrl"][0][1732]
macro = [j + 1 for j in range(len(Q.lines_of["evctrl"][0])) if text("evctrl", j).startswith(b"#macro h_bosseventlist01()")]
body = b"".join(text("evctrl", j) for j in range(869, 884))
check("V", T == {"ctrl": (17, 221, 0), "evctrl": (3, 264, 1), "btlctrl": (558, 0, 0), "mapctrl": (283, 0, 0)} and odd == [(9, 56, 1733)]
      and g1733 == [2276] and text("evctrl", 2276).strip() == b"h_bosseventlist01()" and macro == [870] and b"mesopenspeed(" in body,
      "verb on the logical line / only logical / only physical: %s; the one physical-only call is logical 1733 = physical 2277, the macro "
      "h_bosseventlist01() (defined at 870), whose body calls mesopenspeed" % T)
LC = {mm: [len(G) for G in Q.groups_of[mm]] for mm in MODS}
over, eq = [], []
for mm, i, recs, ce, q, st, nxt in Q.scopes:
    for k, (ln, bk, fl) in enumerate(recs[:ce]):
        if ln > LC[mm][bk]: over.append((mm, i, k))
        elif ln == LC[mm][bk]: eq.append((mm, i, k))
check("D", LC["ctrl"][0] == 958 and LC["evctrl"][0] == 1912 and all(LC[mm][b] == len(Q.lines_of[mm][b]) for mm in MODS for b in range(len(LC[mm])) if (mm, b) not in (("ctrl", 0), ("evctrl", 0)))
      and [x[:2] for x in over] == [("btlctrl", 1)] * 3 + [("mapctrl", 1)] * 3 and len(eq) == 9,
      "logical counts ctrl 0 = 958, evctrl 0 = 1912, others physical; past the block: %d (the six), equal to the count: %d (the nine)" % (len(over), len(eq)))
bgm = [byte_groups(SBN["mapctrl"], x) for x in Q.lines_of["mapctrl"]]
Tb = calls("mapctrl", bgm)
check("C", (sum(a and not b for *_, a, b in Tb), sum(b and not a for *_, a, b in Tb)) == (0, 156) and T["ctrl"][1] + T["evctrl"][1] == 485,
      "byte-test grouping on mapctrl: %d logical-only, %d physical-only calls (it wrongly shifts the numbering); physical numbering misses %d ctrl / evctrl calls"
      % (sum(a and not b for *_, a, b in Tb), sum(b and not a for *_, a, b in Tb), T["ctrl"][1] + T["evctrl"][1]))
ea = [Q.lookup(Q.groups_of[m2], scope[(m2, i2)][3], pc, scope[(m2, i2)][2][pc])[1] for m2, i2, pc in (("btlctrl", 1, 531), ("btlctrl", 1, 537), ("mapctrl", 1, 729), ("mapctrl", 1, 736))]
check("L", ea == [3, 4, 387, 388], "lookup() keeps the earlier anchors (physical indices %s) and resolves evctrl's through the logical lines (A)" % ea)
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
