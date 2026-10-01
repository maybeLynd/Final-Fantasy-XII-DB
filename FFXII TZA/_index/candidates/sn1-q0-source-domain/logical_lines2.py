"""logical_lines2.py - v2 (on ASTRA-REQ-FABLE-SN1-CP932-CONTINUATION: the continuation test walks the line as CP932, so a
trail byte 5C inside a double-byte character is not a backslash; v1 counted two mapctrl comment lines ending in '能' = 94 5C). SN-1: q0's line numbers count LOGICAL source lines, with backslash-continued physical lines folded into one
(FABLE, Claude Opus 5.5, 2026-09-28, on ASTRA-REQ-FABLE-SN1-LOGICAL-SOURCE). DATA from the archive, .sbn lines read through the
block's own 32-line map as in entry_lines.py.

  L1 backslash-continued physical lines per block: evctrl block 0 has 544 of 2,456; ctrl block 0 has 19; mapctrl block 0 has none (its
     physical 977 and 1187 end in CP932 '能' = 94 5C, not a backslash - L0); btlctrl block 0 and every block 1 and 2 have none
  L2 evctrl scope 1: q0 lines 417, 418, 708, 709 (pcs 22, 34, 3230, 3242), read as 1-based LOGICAL lines, land on physical 961
     'askpos( 6 , ...)', 962 'mesopenspeed( 6 , 0 );', 1252 'askpos(...)', 1253 'mesopenspeed(...)'; the direct physical reading
     source[line - 1] lands on unrelated text for every one
  L3 entry_lines.py's samples are unaffected: no continuation precedes btlctrl block 2 line 5 or mapctrl block 0 line 389, so there
     logical and physical lines coincide; and blocks 2 have no continuations, so D2's six end-plus-one records stay one past the end
  L4 the assignment at evctrl pc 16 (the statement before pc 22) carries the same q0 line, 417: which source statement a q0 line
     names is not always singular, and the compiler's grouping rule is not established here
  C  control: removing one trailing backslash before physical line 961 (in memory) moves the logical mapping of pc 22 off the
     askpos statement, so L2 depends on the continuation count, not on a coincidence
"""
import os, struct, sys
DIR = sys.argv[1] if len(sys.argv) > 1 else r"D:/FFXII_TZA_extract/ps2data/image/ff12/in/bin"
BS = bytes([92])
fails = 0
def ok(tag, cond, msg):
    global fails
    print(("PASS " if cond else "FAIL ") + tag + "  " + msg); fails += (not cond)
def sbn_lines(m, blk):
    s = open(os.path.join(DIR, m + ".sbn"), "rb").read()
    nb = struct.unpack_from("<I", s, 0)[0]; bo = struct.unpack_from("<%dI" % nb, s, 4)
    if blk >= nb: return None
    o = bo[blk]; L, base = struct.unpack_from("<II", s, o); p = o + 8; starts, rem = [], L
    while rem > 0:
        k = min(32, rem); starts += [base + r for r in struct.unpack_from("<%dH" % k, s, p)]; p += 2 * k; rem -= k
        if rem > 0: base = struct.unpack_from("<I", s, p)[0]; p += 4
    return [s[a:s.find(bytes([0]), a)] for a in starts]
def q0(m, sc):
    b = open(os.path.join(DIR, m + ".dbg"), "rb").read()
    o0 = struct.unpack_from("<I", b, 0)[0]; ns = struct.unpack_from("<I", b, o0)[0]
    offs = struct.unpack_from("<%dI" % (4 * ns + 1), b, o0 + 4)
    a, z = offs[4 * sc], offs[4 * sc + 1]
    return [struct.unpack_from("<HBB", b, a + 4 * k) for k in range((z - a) // 4)]
def last_char_is_ascii_backslash(t):
    """Walk the line as CP932: a lead byte 0x81-0x9F or 0xE0-0xFC takes the next byte as its trail, so a trail byte 0x5C (as in
    '能' = 94 5C) is part of a double-byte character, not a backslash. True only when the final character is a single-byte 0x5C."""
    t = t.rstrip(b" \t\r\n"); i, last = 0, None
    while i < len(t):
        c = t[i]
        if (0x81 <= c <= 0x9F or 0xE0 <= c <= 0xFC) and i + 1 < len(t): last = t[i:i + 2]; i += 2
        else: last = t[i:i + 1]; i += 1

    return last == BS
cont = last_char_is_ascii_backslash
raw_cont = lambda t: t.rstrip(b" \t\r\n").endswith(BS)      # v1's test, kept only as the control's defect
def logical_to_physical(L, ln):
    """1-based logical line -> 0-based index of its first physical line."""
    logical, i = 0, 0
    while i < len(L):
        logical += 1
        if logical == ln: return i
        while i < len(L) and cont(L[i]): i += 1
        i += 1
    return None
counts = {}
for m in ("ctrl", "btlctrl", "evctrl", "mapctrl"):
    for b in range(3):
        L = sbn_lines(m, b)
        if L is not None: counts[(m, b)] = (len(L), sum(1 for t in L if cont(t)), next((i + 1 for i, t in enumerate(L) if cont(t)), None))
M0 = sbn_lines("mapctrl", 0)
cp932_neg = [(i + 1, M0[i].rstrip(b" \t\r\n")[-2:].hex()) for i in (976, 1186)]
ok("L0", all(raw_cont(M0[i]) and not cont(M0[i]) for i in (976, 1186)) and all(h == "945c" for n, h in cp932_neg)
   and any(cont(t) for t in sbn_lines("evctrl", 0)),
   "mapctrl physical 977 and 1187 end in CP932 94 5C ('能'): v1's raw-byte test called them continuations, the CP932 walk does not %s; "
   "evctrl's ASCII continuations are still found" % cp932_neg)
ok("L1", counts[("evctrl", 0)][:2] == (2456, 544) and counts[("ctrl", 0)][1] == 19 and counts[("mapctrl", 0)][1] == 0
   and counts[("btlctrl", 0)][1] == 0 and all(v[1] == 0 for (m, b), v in counts.items() if b > 0),
   "continued lines (physical, continued, first): %s" % {"%s %d" % k: v for k, v in counts.items()})
E = sbn_lines("evctrl", 0); Q = q0("evctrl", 1)
want = {22: b"askpos(", 34: b"mesopenspeed(", 3230: b"askpos(", 3242: b"mesopenspeed("}
rows = []
for pc, stem in want.items():
    ln, bk, fl = Q[pc]; p = logical_to_physical(E, ln)
    rows.append((pc, ln, bk, fl, p + 1, E[p].strip().startswith(stem), E[ln - 1].strip().startswith(stem)))
ok("L2", all(r[2] == 0 and r[3] == 1 and r[5] and not r[6] for r in rows) and [r[4] for r in rows] == [961, 962, 1252, 1253],
   "(pc, q0 line, block, flag, physical, logical match, direct match): %s" % rows)
Bq = q0("btlctrl", 1); Mq = q0("mapctrl", 1)
ok("L3", counts[("btlctrl", 2)][1] == 0 and Mq[736][0] == 389 and counts[("mapctrl", 0)][1] == 0 and Bq[537][1] == 2,
   "no continuation before btlctrl block 2 line 5 or anywhere in mapctrl block 0; blocks 2 have none")
ok("L4", Q[16][0] == Q[22][0] == 417 and Q[16][2] == 1 and Q[22][2] == 1, "pc 16 and pc 22 both start instructions and both carry line 417")
E2 = list(E); k = max(i for i in range(960) if cont(E2[i])); E2[k] = E2[k].rstrip(b" \t\r\n")[:-1]
p2 = logical_to_physical(E2, Q[22][0])
ok("C", not E2[p2].strip().startswith(b"askpos("), "with one continuation removed (physical %d), pc 22's line lands on physical %d: %r" % (k + 1, p2 + 1, E2[p2].strip()[:30]))
print("FAILS", fails); sys.exit(1 if fails else 0)
