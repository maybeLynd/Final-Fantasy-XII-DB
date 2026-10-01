"""entry_lines.py - SN-1: q0's line numbers are 1-based in the samples that can tell (FABLE, Claude Opus 5.5, 2026-09-28, on
ASTRA-REQ-FABLE-SN1-ENTRY-LINES). DATA from the archive: the .dbg q0 record, the .ebp bytecode at the same pc, and the .sbn line the
record names, located through the block's own 32-line map (OPUS's reading in ../sn1-layouts/sn1_layouts.py: u16 offsets per page,
each page's base the u32 before it).

  E1 four statements whose bytecode pushes a literal that the source line states: btlctrl scope 1 pc 531 (push 0, 'loop_flg = 0;'),
     pc 537 (push 1, 'mapjump_menu_flg = 1;'), mapctrl scope 1 pc 729 (push 2, 'dvar(2, test);'), pc 736 (push 3, 'dvar(3, ...)').
     Read as 1-based, each q0 line names exactly that statement; read as 0-based, none does (a different literal or a blank line)
  E2 consequence for q0_domain.py D2: under 1-based lines the nine records with line == lineCount name each block's last line,
     and the six past it name one line beyond the end of the block
  C  control: shifting every sampled q0 line by one (a perturbation of the stored coordinate) breaks all four 1-based matches, so
     E1 depends on the stored value, not on a coincidence of neighbouring lines
  Not claimed: a universal compiler rule, the cause of the six end-plus-one records, or anything about SN-1's X
"""
import os, re, struct, sys
DIR = sys.argv[1] if len(sys.argv) > 1 else r"D:/FFXII_TZA_extract/ps2data/image/ff12/in/bin"
fails = 0
def ok(tag, cond, msg):
    global fails
    print(("PASS " if cond else "FAIL ") + tag + "  " + msg); fails += (not cond)
def sbn_lines(m, blk):
    s = open(os.path.join(DIR, m + ".sbn"), "rb").read()
    nb = struct.unpack_from("<I", s, 0)[0]; bo = struct.unpack_from("<%dI" % nb, s, 4)
    o = bo[blk]; L, base = struct.unpack_from("<II", s, o); p = o + 8; starts, rem = [], L
    while rem > 0:
        k = min(32, rem); starts += [base + r for r in struct.unpack_from("<%dH" % k, s, p)]; p += 2 * k; rem -= k
        if rem > 0: base = struct.unpack_from("<I", s, p)[0]; p += 4
    return [s[a:s.find(bytes([0]), a)].decode("latin-1").strip() for a in starts]
def q0(m, sc):
    b = open(os.path.join(DIR, m + ".dbg"), "rb").read()
    o0 = struct.unpack_from("<I", b, 0)[0]; ns = struct.unpack_from("<I", b, o0)[0]
    offs = struct.unpack_from("<%dI" % (4 * ns + 1), b, o0 + 4)
    a, z = offs[4 * sc], offs[4 * sc + 1]
    return [struct.unpack_from("<HBB", b, a + 4 * k) for k in range((z - a) // 4)]
def code(m, sc):
    e = open(os.path.join(DIR, m + ".ebp"), "rb").read()
    ins0 = sum(r[2] for r in q0(m, 0))
    for o in range(0, len(e) - 0x40, 4):
        if struct.unpack_from("<I", e, o + 0xC)[0] == ins0 and struct.unpack_from("<I", e, o + 0x24)[0] == 0:
            for bs in range(0, o, 4):
                if struct.unpack_from("<I", e, bs + 0x18)[0] + 4 + bs == o:
                    return e[bs + struct.unpack_from("<I", e, o + 0x30 * sc + 8)[0]:]
SAMPLES = [("btlctrl", 1, 531, 0, r"^loop_flg\s*=\s*0;"), ("btlctrl", 1, 537, 1, r"^mapjump_menu_flg\s*=\s*1;"),
           ("mapctrl", 1, 729, 2, r"^dvar\(2,"), ("mapctrl", 1, 736, 3, r"^dvar\(3,")]
res = []
for m, sc, pc, lit, pat in SAMPLES:
    ln, bk, fl = q0(m, sc)[pc]; L = sbn_lines(m, bk); c = code(m, sc)
    push = c[pc] == 0x4F and struct.unpack_from("<H", c, pc + 1)[0] == lit
    one = bool(re.match(pat, L[ln - 1])); zero = ln < len(L) and bool(re.match(pat, L[ln]))
    shifted = bool(re.match(pat, L[ln])) if ln < len(L) else False           # stored line + 1, read 1-based
    res.append((m, pc, ln, bk, fl, push, one, zero, shifted, L[ln - 1][:30], L[ln][:30] if ln < len(L) else "<end>"))
ok("E1", all(r[4] == 1 and r[5] and r[6] and not r[7] for r in res),
   "; ".join("%s pc %d line %d: push ok %s, 1-based %r, 0-based %r" % (r[0], r[1], r[2], r[5], r[9], r[10]) for r in res))
counts = {m: [struct.unpack_from("<I", open(os.path.join(DIR, m + ".sbn"), "rb").read(), o)[0]
              for o in struct.unpack_from("<%dI" % struct.unpack_from("<I", open(os.path.join(DIR, m + ".sbn"), "rb").read(), 0)[0],
                                          open(os.path.join(DIR, m + ".sbn"), "rb").read(), 4)] for m in ("btlctrl", "mapctrl")}
ok("E2", counts["btlctrl"][2] == 558 and counts["mapctrl"][2] == 557,
   "1-based: line 558 is btlctrl block 2's last line and 559 one past it; line 557 is mapctrl block 2's last and 558 one past")
ok("C", not any(r[8] for r in res), "the stored line shifted by one matches none of the four statements")
print("FAILS", fails); sys.exit(1 if fails else 0)
