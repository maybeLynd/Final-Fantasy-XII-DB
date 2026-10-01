"""sn1_entry_lines.py - SN-1 (OPUS, Claude Opus 5.5, 2026-09-28): which line a q0 coordinate names, from literal anchors. For
ASTRA-REQ-OPUS-SN1-ENTRY-LINES (_experiments/evidence/sn1-named-entry-line-convention/). DATA from the archive; nothing runs.
Written without ASTRA's code. Opcode names from the interpreter page's table (0x46 DVAR, 0x49 POPV, 0x4A PUSHDBG, 0x4F PUSHII;
0x03-0x47 one byte, 0x48-0x63 three: opcode + u16 immediate).

  I  the .sbn parser and the guarded resolver are sn1_q0_domain.py's (which checks the parser against sn1_layouts.py)
  S  four statements whose bytecode carries a literal that the source line must show. At each pc the q0 record is an
     instruction start (flag 1), and the instructions up to the next flag-1 record of another line share its coordinate:
       btlctrl scope 1 pc 531  PUSHII 0; POPV 0x0D           q0 (line 4, block 2)
       btlctrl scope 1 pc 537  PUSHII 1; POPV 0x0E           q0 (line 5, block 2)
       mapctrl scope 1 pc 729  PUSHII 2; PUSHDBG 0x52; DVAR  q0 (line 388, block 0)
       mapctrl scope 1 pc 736  PUSHII 3; PUSHDBG 0x20; DVAR  q0 (line 389, block 0)
     Counting lines from 1 (text index line - 1), each line assigns / dvar()s exactly the pushed literal
     (`loop_flg = 0`, `mapjump_menu_flg = 1`, `dvar(2, ...)`, `dvar(3, ...)`). Counting from 0, none does
     (`mapjump_menu_flg = 1` for 0, a blank line for 1, `dvar(3, ...)` for 2, `switch(...)` for 3)
  C  controls: the same test with the immediate + 1, or with q0's line + 1 under the 1-based reading (the same text as the
     0-based reading), matches none of the four
  L  lookup() - the one-based source lookup the resolver offers (logical lines since sn1_logical_lines.py; these anchors' blocks
     have no continuation line, so logical = physical there) - returns exactly those four texts; over all 53,784 records
     it gives 53,719 lines, 6 UNRESOLVED (the EOF+1 coordinates) and 59 PAD, and never clamps
Not claimed: a universal compiler convention (four anchors in two modules); what POPV 0x0D / PUSHDBG 0x52 name; the cause of the
six missing lines; SN-1 X. evctrl scope 1's shared tail is not read here.
Usage: python sn1_entry_lines.py [dir]
"""
import os, re, struct, sys, importlib.util, io, contextlib
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
    except SystemExit as e: qfail = e.code
check("I", qfail == 0 and hasattr(Q, "lookup") and hasattr(Q, "resolve"), "sn1_q0_domain.py runs clean (FAILS 0) and provides resolve() / lookup()")


def text(m, blk, idx):
    s = open(os.path.join(DIR, m + ".sbn"), "rb").read()
    o, e = Q.sbn_blocks(s)[blk]; L, groups, lines, p = Q.sbn_group_read(s, o)
    a = lines[idx]; z = s.index(b"\0", a)
    return s[a:z].decode("ascii", "replace").strip()   # comments carry Shift-JIS; only the ASCII statement is tested


def decode(c, pc, n):
    out = []
    for _ in range(n):
        op = c[pc]
        if 0x48 <= op <= 0x63: out.append((op, struct.unpack_from("<H", c, pc + 1)[0])); pc += 3
        else: out.append((op, None)); pc += 1
    return out


scope = {(s[0], s[1]): s for s in Q.scopes}
ebp = {m: open(os.path.join(DIR, m + ".ebp"), "rb").read()[0x80:] for m in ("btlctrl", "mapctrl")}
PUSHII, POPV, PUSHDBG, DVAR = 0x4F, 0x49, 0x4A, 0x46
ANCH = [("btlctrl", 1, 531, [(PUSHII, 0), (POPV, 0x0D)], (4, 2)), ("btlctrl", 1, 537, [(PUSHII, 1), (POPV, 0x0E)], (5, 2)),
        ("mapctrl", 1, 729, [(PUSHII, 2), (PUSHDBG, 0x52), (DVAR, None)], (388, 0)),
        ("mapctrl", 1, 736, [(PUSHII, 3), (PUSHDBG, 0x20), (DVAR, None)], (389, 0))]


def shows(t, ops, lit):
    t = t.split("//")[0].strip()                                  # a trailing comment is not part of the statement
    if ops[-1][0] == DVAR: return re.match(r"dvar\(\s*%d\s*," % lit, t) is not None
    return re.match(r"\w+\s*=\s*%d\s*;?$" % lit, t) is not None


one, zero, cimm, cline, got = [], [], [], [], []
for m, i, pc, ops, coord in ANCH:
    mm, ii, recs, ce, q, st, nxt = scope[(m, i)]
    ln, bk, fl = recs[pc]
    dec = decode(ebp[m], st + pc, len(ops))
    ok_bind = fl == 1 and (ln, bk) == coord and dec == ops
    lit = ops[0][1]
    t1, t0, t2 = text(m, bk, ln - 1), text(m, bk, ln), text(m, bk, ln)   # 1-based, 0-based, 1-based with line + 1
    one.append(ok_bind and shows(t1, ops, lit)); zero.append(shows(t0, ops, lit))
    cimm.append(shows(t1, ops, lit + 1)); cline.append(shows(t2, ops, lit))
    got.append((m, pc, t1, t0))
check("S", all(one) and not any(zero), "one-based: %s; zero-based: %s; texts %s" % (one, zero, [(m, pc, a.split("//")[0].strip(), b.split("//")[0].strip()) for m, pc, a, b in got]))
check("C", not any(cimm) and not any(cline), "immediate + 1 matches %d, line + 1 matches %d (of 4)" % (sum(cimm), sum(cline)))
tal = {"LINE": 0, "UNRESOLVED": 0, "PAD": 0}; lk = []
for m, i, recs, ce, q, st, nxt in Q.scopes:
    for k, r in enumerate(recs):
        v = Q.lookup(Q.groups_of[m], ce, k, r); tal[v[0]] += 1   # logical since sn1_logical_lines.py (these blocks have no continuation)
        if (m, i, k) in [(a[0], a[1], a[2]) for a in ANCH]:
            lk.append(text(m, r[1], v[1]) == got[[a[2] for a in ANCH].index(k)][2])
check("L", lk == [True] * 4 and tal == {"LINE": 53719, "UNRESOLVED": 6, "PAD": 59}, "lookup() on the anchors %s; tallies %s" % (lk, tal))
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
