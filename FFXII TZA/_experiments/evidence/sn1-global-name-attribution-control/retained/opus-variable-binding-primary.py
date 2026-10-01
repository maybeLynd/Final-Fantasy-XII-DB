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
     logical source line? ctrl, btlctrl and mapctrl bind directly (T0[operand] on the line far more often than T0[operand +- 1]).
     evctrl does NOT, for one block: for operands 0x01..0x3E (the g_btl_* run), T0[operand + 1] is on the line in 59
     statements and T0[operand] in none; from operand 0x41 up the direct reading holds again. So the equal counts (T) do not
     make T0's order the operand's order: a consumer must not name an operand T0[operand] without a per-module check
     The operand + 1 / operand - 1 counts in B are the controls, on the same lines.
  X  where it starts: case 25's first line (T0[1]'s assignment) carries no scope-1 instruction; its code (POPV 0x01) sits on T0[2]'s line
Not claimed: why evctrl's g_btl_* block is offset by one (whether the table holds T0[1]'s variable at all), what the
descriptor classes mean, any name scope rule, any live value. Lines with no variable name (macros, braces) decide nothing.
Usage: python sn1_variable_binding.py [dir]
"""
import collections, contextlib, importlib.util, io, os, re, struct, sys
DIR = sys.argv[1] if len(sys.argv) > 1 else r"D:/FFXII_TZA_extract/ps2data/image/ff12/in/bin"
HERE = os.path.dirname(os.path.abspath(__file__))
fails = 0
def check(name, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", name, detail)); fails += not ok
spec = importlib.util.spec_from_file_location("q0dom", os.path.join(HERE, "sn1_q0_domain.py"))
Q = importlib.util.module_from_spec(spec); sys.argv = [sys.argv[0], DIR]
with contextlib.redirect_stdout(io.StringIO()):
    try: spec.loader.exec_module(Q)
    except SystemExit: pass
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
# X (2026-09-28): WHERE THE OFFSET STARTS. evctrl case 25 opens at physical line 1575, `g_btl_<Earth Dragon> = DEF_BTL_BOSS_ENTRY`
# (T0[1]); no scope-1 instruction's q0 line is 1575's logical line. The case's code at scope 1 pc 5010 / 5013 is PUSHII 1; POPV 0x01,
# attributed to physical 1576, `g_btl_<Mimic Queen> = ...` (T0[2]). So T0 carries a name at index 1 that this case compiles no
# store for, and the table's run starts with the next name at index 1. Where (whether) the table holds the first name is not
# established; operand 0x40 (pc 5004) binds T0[0x40] g_com_debug_flag again.
Tx = [SBN["evctrl"][a_:SBN["evctrl"].index(bytes(1), a_)] for a_ in Q.lines_of["evctrl"][0]]
sc1 = next(x_ for x_ in Q.scopes if (x_[0], x_[1]) == ("evctrl", 1)); r1, st1 = sc1[2], sc1[5]
g0 = Q.groups_of["evctrl"][0]
lg = {j: L + 1 for L, grp in enumerate(g0) for j in grp}          # physical index -> logical line
used = {r[0] for r in r1 if r[1] == 0}
check("X", Tx[1574].strip().startswith(NAMES["evctrl"][1]) and Tx[1575].strip().startswith(NAMES["evctrl"][2]) and lg[1574] not in used
      and EBP["evctrl"][st1 + 5010] == 0x4F and EBP["evctrl"][st1 + 5013] == 0x49 and struct.unpack_from("<H", EBP["evctrl"], st1 + 5014)[0] == 1
      and r1[5013][0] == lg[1575] and struct.unpack_from("<H", EBP["evctrl"], st1 + 5005)[0] == 0x40 and NAMES["evctrl"][0x40] == b"g_com_debug_flag",
      "case 25's first line (T0[1]'s assignment, physical 1575) carries no scope-1 instruction; its code POPV 0x01 is attributed to 1576 (T0[2]); operand 0x40 = T0[0x40]")
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
