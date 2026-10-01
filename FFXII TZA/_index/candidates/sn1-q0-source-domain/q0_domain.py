"""q0_domain.py - SN-1: q0's source coordinates against the .sbn blocks they name (FABLE, Claude Opus 5.5, 2026-09-28, on
ASTRA-REQ-FABLE-SN1-SOURCE-DOMAIN). DATA from the archive.

  D1 each .sbn begins {u32 nBlocks; u32 blockOff[nBlocks]}, and each block {u32 lineCount; u32 textOff; ...}; per module the
     block line counts are read here
  D2 every q0 record {u16 line; u8 block; u8 flag} whose line is >= its block's lineCount is listed: exactly two groups, btlctrl
     scope 1 records 3978..3980 (block 2, line 559 of 558) and mapctrl scope 1 records 5201..5203 (block 2, line 558 of 557) - each a
     start-flag record plus two continuation records, well inside the scope. Line 559 of a 558-line block is out of range whether
     the lines count from 0 or from 1
  D3 the all-zero records at each scope's end are a suffix of 0 to 3 records, not 0 to 2: the scopes with 3 are listed
  C  controls: every other record's line is < its block's lineCount (so D2's two groups are not an artefact of reading the wrong
     block's count), and the zero-suffix counter reports a non-zero suffix on a planted trailing zero record
"""
import os, struct, sys
DIR = sys.argv[1] if len(sys.argv) > 1 else r"D:/FFXII_TZA_extract/ps2data/image/ff12/in/bin"
fails = 0
def ok(tag, cond, msg):
    global fails
    print(("PASS " if cond else "FAIL ") + tag + "  " + msg); fails += (not cond)
counts = {}; bad = []; zsuf = {}; total = 0
def suffix(recs):
    k = 0
    while k < len(recs) and recs[-1 - k] == (0, 0, 0): k += 1
    return k
for m in ("ctrl", "btlctrl", "evctrl", "mapctrl"):
    s = open(os.path.join(DIR, m + ".sbn"), "rb").read()
    nb = struct.unpack_from("<I", s, 0)[0]; bo = struct.unpack_from("<%dI" % nb, s, 4)
    counts[m] = [struct.unpack_from("<I", s, o)[0] for o in bo]
    b = open(os.path.join(DIR, m + ".dbg"), "rb").read()
    o0 = struct.unpack_from("<I", b, 0)[0]; ns = struct.unpack_from("<I", b, o0)[0]
    offs = struct.unpack_from("<%dI" % (4 * ns + 1), b, o0 + 4)
    for i in range(ns):
        q0, q1 = offs[4 * i], offs[4 * i + 1]; n0 = (q1 - q0) // 4
        recs = [struct.unpack_from("<HBB", b, q0 + 4 * k) for k in range(n0)]
        zs = suffix(recs); zsuf[(m, i)] = zs; body = recs[:n0 - zs]
        for k, (ln, bk, fl) in enumerate(body):
            total += 1
            if bk >= len(counts[m]) or ln >= counts[m][bk]: bad.append((m, i, k, ln, bk, fl, counts[m][bk] if bk < len(counts[m]) else None, n0))
print("block line counts:", counts)
ok("D1", counts["btlctrl"][2] == 558 and counts["mapctrl"][2] == 557, "btlctrl block 2 = %d lines, mapctrl block 2 = %d" % (counts["btlctrl"][2], counts["mapctrl"][2]))
over1 = [(m, i, k, ln, bk, fl) for m, i, k, ln, bk, fl, c, n0 in bad if ln > c]          # invalid even counting lines from 1
at_count = [(m, i, k, ln, bk, fl) for m, i, k, ln, bk, fl, c, n0 in bad if ln == c]       # valid only counting from 1
ok("D2", over1 == [("btlctrl", 1, 3978, 559, 2, 1), ("btlctrl", 1, 3979, 559, 2, 0), ("btlctrl", 1, 3980, 559, 2, 0),
                   ("mapctrl", 1, 5201, 558, 2, 1), ("mapctrl", 1, 5202, 558, 2, 0), ("mapctrl", 1, 5203, 558, 2, 0)] and len(at_count) == 9
   and all(k < n0 - 50 for m, i, k, ln, bk, fl, c, n0 in bad),
   "past the block under either convention: %s; line == lineCount (valid only counting from 1): %d records; all well inside their scope"
   % (over1, len(at_count)))
three = sorted(k for k, v in zsuf.items() if v == 3)
ok("D3", max(zsuf.values()) == 3 and min(zsuf.values()) == 0 and three == [("btlctrl", 22), ("ctrl", 1), ("evctrl", 3), ("mapctrl", 1), ("mapctrl", 3)],
   "zero suffix per scope ranges %d..%d; suffix 3 at %s; %d zero records in all" % (min(zsuf.values()), max(zsuf.values()), three, sum(zsuf.values())))
ok("C", total - len(bad) > 30000 and suffix([(1, 0, 1), (0, 0, 0)]) == 1 and suffix([(1, 0, 1)]) == 0,
   "%d in-range records besides the fifteen above; the suffix counter sees a planted zero record" % (total - len(bad)))
print("FAILS", fails); sys.exit(1 if fails else 0)
