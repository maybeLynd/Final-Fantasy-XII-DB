"""t0_attribution.py - SN-1: the disputed 62 evctrl globals, and what an archived-macro match does and does not identify
(FABLE, Claude Opus 5.5, 2026-09-28).

OPUS's Part 11 (sn1-layouts/sn1_neither_partition.py) explains 188 of the 272 'neither' variable instructions as archived
macro code: the macro invoked on (A) or after a case label next to (E) the tagged logical line expands to text that names
T0[operand]. That test is MEMBERSHIP: the name occurs somewhere in the expansion. It is consistent with the direct binding.
This control measures whether membership also identifies the statement that emitted the instruction. It does not re-run the
partition's arithmetic; it loads the wrapper through OPUS's repaired prerequisite interface (sn1_prereq.run, 0b26f50c4), so
a failed, missing or malformed wrapper or producer stops this run before anything is computed.

  P  prerequisite: sn1_neither_partition.py exits 0 with exactly P N A E L U Z C and FAILS 0 (it carries the producer
     sn1_variable_binding.py's Q T S B A G D X in turn)
  G  the 62 evctrl operands 0x01..0x3E: each descriptor 0A03..0A40 has exactly ONE T2 record, carrying one name, T0[n]
     (Part 10's check D compares the first name; this pins the record shape the page states)
  T  one tag, many instructions: the 188 A/E records fall on far fewer distinct q0 tags, and most of those tags are shared
     by records with DIFFERENT operands - so the tag names the invocation, not a statement
  L  more than one candidate statement: in some records T0[operand] occurs on two or more lines of the expansion, so
     membership leaves several statements that could have emitted it
  C  control (not new, restated from Part 11 check C): T0[operand + 1] passes the same membership test in 52 records -
     membership is weak evidence even for the name, let alone for the statement
  Not claimed: which expansion statement emits any instruction, a compiler rule, or anything about the 84 records whose
  macros the archive does not carry (their text is not in the archive; nothing here stands in for it).
"""
import collections, importlib.util, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
L11 = os.path.join(HERE, "..", "sn1-layouts")
fails = 0
def check(tag, ok, text):
    global fails
    fails += not ok; print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))

_ps = importlib.util.spec_from_file_location("sn1_prereq", os.path.join(L11, "sn1_prereq.py"))
PR = importlib.util.module_from_spec(_ps); _ps.loader.exec_module(PR)
W, why = PR.run(os.path.join(L11, "sn1_neither_partition.py"), [os.path.join(L11, "sn1_neither_partition.py")] + sys.argv[1:],
                ("P", "N", "A", "E", "L", "U", "Z", "C"), ("nb", "classify", "MAC", "NAMES", "Q", "nth_line", "calls", "VB"))
check("P", why is None, "prerequisite sn1_neither_partition.py: %s" % (why or "exit 0, PASS P N A E L U Z C, FAILS 0"))
if why:
    print("FAILS %d" % fails); sys.exit(1)

g2 = W.VB.t2("evctrl"); rows = [W.VB.VT["evctrl"][k][0] for k in range(1, 0x3F)]
shape = [len(g2.get(d, [])) for d in rows]
check("G", len(rows) == 62 and rows == list(range(0xA03, 0xA41)) and shape == [1] * 62
      and all(g2[d][0] == W.NAMES["evctrl"][k] for k, d in enumerate(rows, 1)),
      "evctrl 0x01..0x3E: %d descriptors 0A03..0A40, T2 records per descriptor %s, name == T0[n] in %d"
      % (len(rows), dict(__import__("collections").Counter(shape)), sum(g2.get(d, [b""])[0] == W.NAMES["evctrl"][k] for k, d in enumerate(rows, 1))))

def body_lines(m, names, depth=0, seen=None):
    """every archived macro body line reachable from the macros in `names` (the wrapper's expand(), kept as lines)"""
    seen = set() if seen is None else seen; out = []
    if depth >= 6: return out
    for c in names:
        if c in W.MAC[m] and c not in seen:
            seen.add(c)
            for l in W.MAC[m][c]:
                out.append(l)
                out += body_lines(m, set(re.findall(r"[^\W\d]\w*", l)), depth + 1, seen)
    return out
def named(name, text): return re.search(r"(?<![\w・])" + re.escape(name) + r"(?![\w・])", text) is not None

recs = []   # (module, scope, tag, operand, bucket, lines naming T0[operand] in the expansion)
for m, i, k, op, n, ln in W.nb:
    name = W.NAMES[m][n].decode("cp932", "replace"); line = ln.decode("cp932", "replace").split("//")[0]
    c = W.classify(m, i, k, name, line)
    if c not in ("A", "E"): continue
    src = line if c == "A" else W.nth_line(m, i, k, -1)
    tag = next(s for s in W.Q.scopes if (s[0], s[1]) == (m, i))[2][k][:2]   # (q0 line, block)
    hits = sum(named(name, l) for l in body_lines(m, set(W.calls(src))))
    recs.append((m, i, tag, n, c, hits))

by_tag = collections.defaultdict(list)
for m, i, tag, n, c, h in recs: by_tag[(m, i, tag)].append(n)
shared = [t for t, ns in by_tag.items() if len(set(ns)) > 1]
in_shared = sum(len(by_tag[t]) for t in shared)
check("T", len(recs) == 188 and len(by_tag) < len(recs) // 2 and in_shared > len(recs) // 2,
      "the %d A/E records fall on %d distinct tags; %d tags carry two or more different operands, holding %d of the %d records; "
      "largest tag: %d records, %d operands"
      % (len(recs), len(by_tag), len(shared), in_shared, len(recs),
         max(len(v) for v in by_tag.values()), max(len(set(v)) for v in by_tag.values())))
multi = [r for r in recs if r[5] >= 2]
zero = [r for r in recs if r[5] == 0]
check("L", len(multi) > 0 and not zero,
      "T0[operand] is on 2+ expansion lines in %d of %d records (max %d lines); on exactly 1 in %d; on none in %d"
      % (len(multi), len(recs), max(r[5] for r in recs), sum(r[5] == 1 for r in recs), len(zero)))
ctl = 0
for m, i, k, op, n, ln in W.nb:
    if 0 <= n + 1 < len(W.NAMES[m]):
        ctl += W.classify(m, i, k, W.NAMES[m][n + 1].decode("cp932", "replace"), ln.decode("cp932", "replace").split("//")[0]) in ("A", "E")
check("C", ctl == 52, "control: T0[operand + 1] passes the same membership test in %d records (Part 11 C: 52)" % ctl)
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
