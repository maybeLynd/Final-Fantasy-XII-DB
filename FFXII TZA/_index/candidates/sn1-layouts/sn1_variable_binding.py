"""sn1_variable_binding.py - SN-1 (OPUS, Claude Opus 5.5, 2026-09-28): which name a variable operand carries. For
ASTRA-REQ-OPUS-SN1-VARIABLE-BINDING (_experiments/evidence/sn1-variable-name-binding/). DATA from the archive; nothing runs.
Written without ASTRA's code; the .sbn parser, logical-line lookup and T0 reading are OPUS's (sn1_q0_domain.py,
sn1_front_tables.py F2).

  T  THE OPERAND'S TABLE. The EBP2 script chunk's header word 10 (+0x28) is the offset of {u32 count; {u32 descriptor; u32 x}
     [count]} (x is 0 in all but 19 entries): counts 56 / 92 / 115 / 127, equal to the .dbg T0 name counts. evctrl entry 0x61 is 0x01000905 (ASTRA's record),
     entry 0 is 0x30000000 (the id T2 gives global_flag[0]), and entries 0x01..0x3E are 0x00000A03..0x00000A40 - one run of
     consecutive offsets
  S  ASTRA's five samples reproduce by the direct reading name = T0[operand]: evctrl POPV 0x61 at scope 1 pc 16 test_load_flg
     (q0 names line 417, the call that follows; the assignment's own text is logical line 416 - ASTRA's attribution grouping); btlctrl POPV 0x0D / 0x0E
     loop_flg / mapjump_menu_flg; mapctrl PUSHDBG 0x52 / 0x20 test / mp_debugmenu_flg
  B  THE DISCRIMINATOR, every PUSHV / POPV / PUSHDBG instruction start in the four modules: is T0[operand] on the instruction's
     logical source line? ctrl, btlctrl and mapctrl: T0[operand] on the line far more often than T0[operand +- 1]. evctrl,
     operands 0x01..0x3E (the g_btl_* run): T0[operand + 1] on the tagged line in 59 statements, T0[operand] in none.
     *Corrected 2026-09-28 (OPUS, check A below): this first read as 'T0's order is not the operand's order - name an operand
     only after a per-module check'. That was wrong. The tagged line is one logical line LATE for these assignments (ASTRA's
     assignment-attribution finding): the preceding logical line carries T0[operand] in all 63 of them, so the binding is
     T0[operand] there too.* The operand + 1 / operand - 1 counts in B are the controls, on the same lines.
  A  THE ATTRIBUTION: evctrl operands 0x01..0x3E - T0[operand] is on the logical line BEFORE the tagged one in all 63 statements
     (a consecutive run of one-line assignments, so the tagged line shows the next variable, T0[operand + 1])
  G  THE TAG-DISPLACEMENT CENSUS, every PUSHV / POPV / PUSHDBG: T0[operand] on the tagged line / only on the preceding logical
     line / neither, per module and opcode. A one-line-late tag occurs in all four modules and is not the rule (the tagged
     line holds the name far more often overall): so neither 'the tag is the statement's line' nor 'minus one' is universal
  D  THE DIRECTORY TRIANGULATION (no source line): every operand-table descriptor that is also a .dbg T2 id - 106 across the
     four modules, 68 in evctrl including 0A03..0A40 - has the T2 name T0[k], and none T0[k+1] (ASTRA-REQ-OPUS-SN1-GLOBAL-NAME-CONTROL)
  X  case 25's first line (T0[1]'s assignment) carries no scope-1 instruction and its code (POPV 0x01) is tagged with T0[2]'s
     line: the one-line-late tag of A, not a table offset (first read as where an offset starts)
Not claimed: the compiler's rule for when the tag runs late, what the descriptor classes mean, any name scope rule, any live
value. Lines with no variable name (macros, braces) decide nothing.
Usage: python sn1_variable_binding.py [dir]
"""
import collections, contextlib, importlib.util, io, os, re, struct, sys
DIR = sys.argv[1] if len(sys.argv) > 1 else r"D:/FFXII_TZA_extract/ps2data/image/ff12/in/bin"
HERE = os.path.dirname(os.path.abspath(__file__))
fails = 0
def check(name, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", name, detail)); fails += not ok
# Q (2026-09-28, FRONTIER-REQ-OPUS-SN1-NEITHER-PARTITION-PREREQ): the q0 lookup is a checked prerequisite. Until then its
# SystemExit was swallowed here, so a failing sn1_q0_domain.py still fed this control. sn1_prereq.run refuses a missing,
# crashing, non-zero, malformed or FAIL-printing run, or one whose check set changed.
_ps = importlib.util.spec_from_file_location("sn1_prereq", os.path.join(HERE, "sn1_prereq.py")); PR = importlib.util.module_from_spec(_ps); _ps.loader.exec_module(PR)
Q, why = PR.run(os.path.join(HERE, "sn1_q0_domain.py"), [sys.argv[0], DIR], ("I", "A", "R", "Z", "E", "C"), ("scopes", "lookup", "groups_of", "lines_of"))
check("Q", why is None, "prerequisite sn1_q0_domain.py: %s" % (why or "exit 0, PASS I A R Z E C, FAILS 0"))
if why: print("FAILS %d" % fails); sys.exit(1)
MODS = ("ctrl", "btlctrl", "evctrl", "mapctrl")
def t0(m):
    b = open(os.path.join(DIR, m + ".dbg"), "rb").read(); h = struct.unpack_from("<16I", b, 0); pool, T0 = h[2], h[1]
    c = struct.unpack_from("<I", b, T0)[0]
    return [b[pool + x:b.index(b"\0", pool + x)] for x in struct.unpack_from("<%dI" % c, b, T0 + 4)]
NAMES = {m: t0(m) for m in MODS}
EBP = {m: open(os.path.join(DIR, m + ".ebp"), "rb").read()[0x80:] for m in MODS}
SBN = {m: open(os.path.join(DIR, m + ".sbn"), "rb").read() for m in MODS}
def vtable(m):
    c = EBP[m]; o = struct.unpack_from("<I", c, 0x28)[0]; n = struct.unpack_from("<I", c, o)[0]
    return [struct.unpack_from("<II", c, o + 4 + 8 * i) for i in range(n)]
VT = {m: vtable(m) for m in MODS}
ev = VT["evctrl"]
check("T", [len(VT[m]) for m in MODS] == [len(NAMES[m]) for m in MODS] == [56, 92, 115, 127]
      and ev[0x61][0] == 0x01000905 and ev[0][0] == 0x30000000 and [ev[i][0] for i in range(1, 0x3F)] == list(range(0xA03, 0xA41)),
      "table counts %s = T0 counts; evctrl [0x61] = %08X, [0] = %08X, [1..0x3E] = 0A03..0A40" % ([len(VT[m]) for m in MODS], ev[0x61][0], ev[0][0]))
def line_of(m, i, k):
    mm, ii, recs, ce, q, st, nxt = next(s for s in Q.scopes if (s[0], s[1]) == (m, i))
    v = Q.lookup(Q.groups_of[m], ce, k, recs[k])
    if v[0] != "LINE": return None
    s = SBN[m]; bk = recs[k][1]
    return b" ".join(s[Q.lines_of[m][bk][j]:s.index(b"\0", Q.lines_of[m][bk][j])] for j in v[2]).split(b"//")[0]
def on(m, idx, line):
    nm = NAMES[m]
    return 0 <= idx < len(nm) and re.search(rb"(?<![A-Za-z0-9_])" + re.escape(nm[idx]) + rb"(?![A-Za-z0-9_])", line) is not None
OPS = {0x48: "PUSHV", 0x49: "POPV", 0x4A: "PUSHDBG"}
inst = []   # (module, scope, pc, op, operand, line)
for m in MODS:
    E = EBP[m]
    for mm, i, recs, ce, q, st, nxt in Q.scopes:
        if mm != m: continue
        for k in range(min(ce, (nxt - st) if nxt else ce)):
            if recs[k][2] == 1 and E[st + k] in OPS:
                ln = line_of(m, i, k)
                if ln is not None: inst.append((m, i, k, E[st + k], struct.unpack_from("<H", E, st + k + 1)[0], ln))
def find(m, i, pc, op): return next(x for x in inst if (x[0], x[1]) == (m, i) and pc <= x[2] < pc + 8 and x[3] == op)   # pc = the statement start
SAMPLES = [("evctrl", 1, 16, 0x49, 0x61, b"test_load_flg"), ("btlctrl", 1, 531, 0x49, 0x0D, b"loop_flg"), ("btlctrl", 1, 537, 0x49, 0x0E, b"mapjump_menu_flg"),
           ("mapctrl", 1, 729, 0x4A, 0x52, b"test"), ("mapctrl", 1, 736, 0x4A, 0x20, b"mp_debugmenu_flg")]
sok = []
for m, i, pc, op, n, nm in SAMPLES:
    x = find(m, i, pc, op)
    if m == "evctrl":   # q0 gives the call's line 417; the assignment's own text is logical line 416 (ASTRA's grouping)
        g = Q.groups_of[m][0]; txt = lambda L: b" ".join(SBN[m][Q.lines_of[m][0][j]:SBN[m].index(b"\0", Q.lines_of[m][0][j])] for j in g[L - 1])
        rec = next(s_ for s_ in Q.scopes if (s_[0], s_[1]) == (m, i))[2][x[2]]
        sok.append(x[3] == op and x[4] == n and NAMES[m][n] == nm and rec[0] == 417 and not on(m, n, x[5]) and on(m, n, txt(416)))
    else:
        sok.append(x[3] == op and x[4] == n and NAMES[m][n] == nm and on(m, n, x[5]))
check("S", sok == [True] * 5, "the five samples: operand, opcode and T0[operand] on the logical line: %s" % sok)
tal = collections.Counter()
for m, i, k, op, n, ln in inst:
    tal[(m, "n")] += on(m, n, ln); tal[(m, "n+1")] += on(m, n + 1, ln) and not on(m, n, ln); tal[(m, "n-1")] += on(m, n - 1, ln) and not on(m, n, ln)
blk = [(on("evctrl", n, ln), on("evctrl", n + 1, ln)) for m, i, k, op, n, ln in inst if m == "evctrl" and 1 <= n <= 0x3E]
hi = [(on("evctrl", n, ln), on("evctrl", n + 1, ln)) for m, i, k, op, n, ln in inst if m == "evctrl" and n >= 0x41]
check("B", all(tal[(m, "n")] > 5 * (tal[(m, "n+1")] + tal[(m, "n-1")]) for m in ("ctrl", "btlctrl", "mapctrl"))
      and sum(b for a, b in blk if not a) == 59 and sum(a for a, b in blk) == 0 and sum(a for a, b in hi) > 5 * sum(b and not a for a, b in hi),
      "direct T0[operand] / only T0[operand+1] / only T0[operand-1] per module: %s; evctrl operands 0x01..0x3E: T0[operand+1] %d, T0[operand] %d; "
      "operands >= 0x41: T0[operand] %d, only T0[operand+1] %d"
      % ({m: (tal[(m, "n")], tal[(m, "n+1")], tal[(m, "n-1")]) for m in MODS}, sum(b for a, b in blk if not a), sum(a for a, b in blk),
         sum(a for a, b in hi), sum(b and not a for a, b in hi)))
def prev_line(m, i, k):
    """the logical line before the one q0 tags for record k of scope i"""
    rec = next(s_ for s_ in Q.scopes if (s_[0], s_[1]) == (m, i))[2][k]
    g = Q.groups_of[m][rec[1]]; L = rec[0] - 1
    if not 1 <= L <= len(g): return b""
    s = SBN[m]
    return b" ".join(s[Q.lines_of[m][rec[1]][j]:s.index(bytes(1), Q.lines_of[m][rec[1]][j])] for j in g[L - 1]).split(b"//")[0]
att = [(on("evctrl", n, ln), on("evctrl", n, prev_line(m, i, k))) for m, i, k, op, n, ln in inst if m == "evctrl" and 1 <= n <= 0x3E]
check("A", len(att) == 63 and all(p for h, p in att) and not any(h for h, p in att),
      "evctrl operands 0x01..0x3E: T0[operand] on the preceding logical line in %d of %d statements, on the tagged line in %d" % (sum(p for h, p in att), len(att), sum(h for h, p in att)))
G = collections.Counter()
for m, i, k, op, n, ln in inst:
    here = on(m, n, ln); G[(m, "here" if here else ("prev" if on(m, n, prev_line(m, i, k)) else "neither"))] += 1
check("G", all(G[(m, "prev")] > 0 for m in MODS) and sum(G[(m, "here")] for m in MODS) > 3 * sum(G[(m, "prev")] for m in MODS),
      "T0[operand] on the tagged line / only on the preceding line / neither: %s" % {m: (G[(m, "here")], G[(m, "prev")], G[(m, "neither")]) for m in MODS})
# D (2026-09-28, for ASTRA-REQ-OPUS-SN1-GLOBAL-NAME-CONTROL): THE DIRECTORY TRIANGULATION, independent of any source line. The
# .dbg T2 directory (sn1_front_tables.py F3) is {count; {u32 id; u32 namePos}[count]}. Every operand-table descriptor that is also a
# T2 id is compared by name with T0 at the same index: equal to T0[k] in every case, to T0[k+1] in none.
def t2(m):
    b = open(os.path.join(DIR, m + ".dbg"), "rb").read(); h = struct.unpack_from("<16I", b, 0); pool, T2 = h[2], h[5]
    c = struct.unpack_from("<I", b, T2)[0]; P = struct.unpack_from("<%dI" % (2 * c), b, T2 + 4); out = collections.defaultdict(list)
    for i_ in range(c): out[P[2 * i_]].append(b[pool + P[2 * i_ + 1]:b.index(bytes(1), pool + P[2 * i_ + 1])])
    return out
tri = {}
for m in MODS:
    D2 = t2(m); hit = [(k_, D2[dsc]) for k_, (dsc, x_) in enumerate(VT[m]) if dsc in D2]
    tri[m] = (len(hit), sum(NAMES[m][k_] in nm for k_, nm in hit), sum(k_ + 1 < len(NAMES[m]) and NAMES[m][k_ + 1] in nm and NAMES[m][k_] not in nm for k_, nm in hit))
g62 = t2("evctrl")
check("D", all(n_ == a_ and s_ == 0 for n_, a_, s_ in tri.values()) and sum(n_ for n_, a_, s_ in tri.values()) == 106
      and all(g62.get(VT["evctrl"][k_][0], [None])[0] == NAMES["evctrl"][k_] for k_ in range(1, 0x3F)),
      "descriptors that are T2 ids / whose T2 name is T0[k] / is T0[k+1] instead: %s; evctrl 0x01..0x3E (0A03..0A40) name T0[k] through T2" % tri)
# X (2026-09-28): evctrl case 25 opens at physical line 1575, `g_btl_<Earth Dragon> = DEF_BTL_BOSS_ENTRY` (T0[1]); no scope-1
# instruction's q0 line is 1575's logical line, and the case's code at scope 1 pc 5010 / 5013 (PUSHII 1; POPV 0x01) is tagged with
# physical 1576, `g_btl_<Mimic Queen> = ...` (T0[2]). First read (6414b46d4) as where a T0 / table offset starts; by A it is the
# one-line-late tag: POPV 0x01 is T0[1]'s store. Operand 0x40 (pc 5004) is T0[0x40] g_com_debug_flag.
Tx = [SBN["evctrl"][a_:SBN["evctrl"].index(bytes(1), a_)] for a_ in Q.lines_of["evctrl"][0]]
sc1 = next(x_ for x_ in Q.scopes if (x_[0], x_[1]) == ("evctrl", 1)); r1, st1 = sc1[2], sc1[5]
g0 = Q.groups_of["evctrl"][0]
lg = {j: L + 1 for L, grp in enumerate(g0) for j in grp}          # physical index -> logical line
used = {r[0] for r in r1 if r[1] == 0}
check("X", Tx[1574].strip().startswith(NAMES["evctrl"][1]) and Tx[1575].strip().startswith(NAMES["evctrl"][2]) and lg[1574] not in used
      and EBP["evctrl"][st1 + 5010] == 0x4F and EBP["evctrl"][st1 + 5013] == 0x49 and struct.unpack_from("<H", EBP["evctrl"], st1 + 5014)[0] == 1
      and r1[5013][0] == lg[1575] and struct.unpack_from("<H", EBP["evctrl"], st1 + 5005)[0] == 0x40 and NAMES["evctrl"][0x40] == b"g_com_debug_flag",
      "case 25's first line (T0[1]'s assignment, physical 1575) carries no scope-1 instruction; its code POPV 0x01 is tagged with 1576 (T0[2]) - the late tag of A; operand 0x40 = T0[0x40]")
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
