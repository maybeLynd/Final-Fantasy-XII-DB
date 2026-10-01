"""sn1_neither_partition.py - OPUS (Claude Opus 5.5), 2026-09-28. DATA from the archive (the four .dbg/.sbn/.ebp files).
Part 11: the 272 variable-operand records whose T0 name is on NEITHER the tagged logical line NOR the one before it
(Part 9's census G). It runs the published producer sn1_variable_binding.py UNCHANGED and partitions exactly those
records - but only when the producer's own result is clean (check P, below). The binding rule is not touched: T0[operand]
names the variable directly (Parts 9 and 10); nothing here is a +1 rule.

ATEL source defines macros as `#macro NAME(params)` ... `#endm`. A macro's code is tagged at the INVOKING line, so its
variable is in the macro body, not on the line.

  P  THE PREREQUISITE (2026-09-28, FRONTIER-REQ-OPUS-SN1-NEITHER-PARTITION-PREREQ): sn1_prereq.run requires the producer
     to exist, run to its own exit 0, print only PASS lines for exactly its checks Q T S B A G D X and then 'FAILS 0', and
     define the objects used here; the producer's Q in turn requires the same of sn1_q0_domain.py. Anything else is a FAIL
     and the run stops before N. *Until then this file exec'd the producer with its sys.exit disabled and its output
     discarded, so with mapctrl's T0 count edited 127 -> 126 in the producer's check T the producer said FAILS 1 / exit 1
     and this wrapper FAILS 0 / exit 0.* test_sn1_prereq.py runs this file on valid and broken copies
  N  THE POPULATION: the producer's own records and predicate give 272 (evctrl 134, mapctrl 135, btlctrl 3)
  A  ARCHIVED MACRO ON THE TAGGED LINE: the line calls a #macro defined in the module's .sbn, and T0[operand] appears in its
     transitive expansion (evctrl 114: h_sinariolost01..10 -> scenariolost(...); mapctrl 54)
  E  ARCHIVED MACRO ONE LINE AFTER A case LABEL: the tag lands on `case N:` and the next logical line calls an archived
     macro whose expansion names T0[operand] (evctrl scope 7: `case N:` then h_jyotyuevNN() -> stayev_base(...), 20 records,
     localresult and stay_event01 per case)
  L  goto AFTER AN UNARCHIVED CALL: the tag lands on `goto BENRI_DEBUG;` and the line before calls a name no archived
     #macro defines (mapctrl, 12 records, g_menu_telepo_dest after YM_テレポクリスタル全部ON();)
  U  UNARCHIVED CALL ON THE TAGGED LINE: the line calls a name that no archived #macro defines, and that name occurs in the
     module's .sbn ONLY at its invocations - its body is in a header outside the archive (mapctrl 69: YM_テレポクリスタル全部ON,
     TK_セーブメニュー呼び出し; btlctrl 3: ISDEBUG, FF12_DEBUG_GLOBAL_FLAG_ALL_BITON / BITOFF)
  Z  NOTHING ELSE: A + E + L + U = 272
  C  CONTROL: the same macro-expansion test with the NEXT T0 name (T0[operand + 1]) explains far fewer of A + E, so the
     test is not trivially true for any name
So 188 of the 272 are explained from archived text; the remaining 84 (L + U) stop at macro bodies the archive does not
carry. The missing discriminator is those headers' text, not a new rule.
Usage: python sn1_neither_partition.py [dir]
"""
import collections, contextlib, io, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
fails = 0
def check(tag, ok, text):
    global fails
    fails += not ok; print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))
import importlib.util
_ps = importlib.util.spec_from_file_location("sn1_prereq", os.path.join(HERE, "sn1_prereq.py")); PR = importlib.util.module_from_spec(_ps); _ps.loader.exec_module(PR)
VB, why = PR.run(os.path.join(HERE, "sn1_variable_binding.py"), [os.path.join(HERE, "sn1_variable_binding.py")] + sys.argv[1:],
                 ("Q", "T", "S", "B", "A", "G", "D", "X"), ("inst", "on", "prev_line", "NAMES", "Q", "SBN"))
check("P", why is None, "prerequisite sn1_variable_binding.py: %s" % (why or "exit 0, PASS Q T S B A G D X, FAILS 0"))
if why: print("FAILS %d" % fails); sys.exit(1)
inst, on, prev_line, NAMES, Q, SBN = VB.inst, VB.on, VB.prev_line, VB.NAMES, VB.Q, VB.SBN
nb = [(m, i, k, op, n, ln) for m, i, k, op, n, ln in inst if not on(m, n, ln) and not on(m, n, prev_line(m, i, k))]
cnt = collections.Counter(m for m, *_ in nb)
check("N", len(nb) == 272 and cnt == {"evctrl": 134, "mapctrl": 135, "btlctrl": 3}, "the producer's neither-population: %d %s" % (len(nb), dict(cnt)))
MAC = {}
for m in SBN:
    D, cur = {}, None
    for l in (x.decode("cp932", "replace") for x in SBN[m].split(b"\x00")):
        mm = re.match(r"\s*#macro\s+(\w+)", l)
        if mm: cur = mm.group(1); D[cur] = []; continue
        if re.match(r"\s*#endm", l): cur = None; continue
        if cur is not None: D[cur].append(l.split("//")[0])
    MAC[m] = D
def expand(m, text, depth=0, seen=None):
    seen = set() if seen is None else seen; out = text
    if depth < 6:
        for c in set(re.findall(r"[^\W\d]\w*", text)):
            if c in MAC[m] and c not in seen:
                seen.add(c); out += " " + expand(m, " ".join(MAC[m][c]), depth + 1, seen)
    return out
def named(name, text): return re.search(r"(?<![\w・])" + re.escape(name) + r"(?![\w・])", text) is not None
KW = {"if", "while", "for", "switch", "return", "case"}
def calls(text): return [c for c in re.findall(r"([^\W\d][\w・]*)\s*\(", text) if c not in KW]
def nth_line(m, i, k, d):
    rec = next(s for s in Q.scopes if (s[0], s[1]) == (m, i))[2][k]
    gg = Q.groups_of[m][rec[1]]; L = rec[0] - d
    if not 1 <= L <= len(gg): return ""
    s = SBN[m]
    return b" ".join(s[Q.lines_of[m][rec[1]][j]:s.index(bytes(1), Q.lines_of[m][rec[1]][j])] for j in gg[L - 1]).split(b"//")[0].decode("cp932", "replace")
def classify(m, i, k, name, line):
    if any(c in MAC[m] for c in calls(line)) and named(name, expand(m, line)): return "A"
    if re.match(r"\s*case\b", line):
        nxt = nth_line(m, i, k, -1)
        if any(c in MAC[m] for c in calls(nxt)) and named(name, expand(m, nxt)): return "E"
    if re.match(r"\s*goto\b", line):
        p = nth_line(m, i, k, 1)
        if calls(p) and not any(c in MAC[m] for c in calls(p)): return "L"
    if calls(line) and not any(c in MAC[m] for c in calls(line)): return "U"
    return "Z"
P = collections.Counter(); U_names = collections.Counter(); unarch_ok = True
for m, i, k, op, n, ln in nb:
    name = NAMES[m][n].decode("cp932", "replace"); line = ln.decode("cp932", "replace").split("//")[0]
    c = classify(m, i, k, name, line); P[(m, c)] += 1
    if c in ("U", "L"):
        callee = [x for x in calls(line if c == "U" else nth_line(m, i, k, 1)) if x not in MAC[m]][0]
        U_names[(m, callee)] += 1
        body = SBN[m].decode("cp932", "replace")
        uses = [l for l in body.split("\x00") if re.search(r"(?<![\w・])" + re.escape(callee) + r"\s*\(", l)]
        unarch_ok &= all(not re.match(r"\s*#(macro|define)", l) for l in uses)
check("A", P[("evctrl", "A")] == 114 and P[("mapctrl", "A")] == 54, "archived macro on the tagged line: evctrl %d, mapctrl %d" % (P[("evctrl", "A")], P[("mapctrl", "A")]))
check("E", P[("evctrl", "E")] == 20, "archived macro one line after a case label: evctrl %d" % P[("evctrl", "E")])
check("L", P[("mapctrl", "L")] == 12, "goto after an unarchived call: mapctrl %d" % P[("mapctrl", "L")])
check("U", P[("mapctrl", "U")] == 69 and P[("btlctrl", "U")] == 3 and unarch_ok,
      "unarchived call on the tagged line: mapctrl %d, btlctrl %d; each callee occurs only as an invocation: %s" % (P[("mapctrl", "U")], P[("btlctrl", "U")], sorted(U_names.items())))
check("Z", sum(v for (m, c), v in P.items() if c == "Z") == 0 and sum(P.values()) == 272, "nothing else: %s" % dict(P))
ctl = 0
for m, i, k, op, n, ln in nb:
    if 0 <= n + 1 < len(NAMES[m]):
        name = NAMES[m][n + 1].decode("cp932", "replace"); line = ln.decode("cp932", "replace").split("//")[0]
        ctl += classify(m, i, k, name, line) in ("A", "E")
ae = P[("evctrl", "A")] + P[("mapctrl", "A")] + P[("evctrl", "E")]
check("C", ctl * 3 < ae, "control: T0[operand + 1] passes the same macro test in %d records, against %d for T0[operand]" % (ctl, ae))
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
