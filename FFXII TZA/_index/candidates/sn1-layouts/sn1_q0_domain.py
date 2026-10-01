"""sn1_q0_domain.py - SN-1 (OPUS, Claude Opus 5.5, 2026-09-28): the domain of q0's source coordinates, for
ASTRA-REQ-OPUS-SN1-SOURCE-DOMAIN (_experiments/evidence/sn1-q0-source-coordinate-domain/). DATA from the archive (the four
.dbg / .sbn / .ebp files); no compiler, game or emulator runs. Written without ASTRA's or FABLE's code; the .sbn line table is
read with OPUS's own parser (sn1_layouts.py sbn_blocks / sbn_group_read, checked here to be the published definitions).

  I  the parser used here is sn1_layouts.py's, unchanged (AST source of both functions equal)
  A  under the parser's line counts, exactly six non-pad records name a line past their block under either numbering:
     btlctrl scope 1 records 3978..3980 (block 2, line 559 of 558) and mapctrl scope 1 records 5201..5203 (block 2, line 558
     of 557), each one flag-1 record plus two flag-0 records; nine records have line == lineCount (addressable only counting
     from 1); no non-pad record has line 0, so no record is addressable only counting from 0. That asymmetry does not prove
     the convention, and the cause of the six stays unknown
  Z  THE ZERO SUFFIX IS PADDING, and its 0..3 range is forced. codeEnd = the last flag-1 record + the length of the opcode
     at that byte of the script's .ebp code (0x03-0x47 one byte, 0x48-0x63 three - the length rule DATA verified). In all 50
     scopes: the q0 record count is codeEnd rounded up to a multiple of 4 (so the q0 table is a multiple of 16 bytes), every
     record at or past codeEnd is (0, 0, 0), and every record before it is not. q0 and q1 start on a 16-byte boundary in all
     50 scopes; q2 and q3 do not (the pad keeps q1 aligned). The .ebp packs scripts back to back without alignment, so a
     pad record's position is not a byte of this script: in the 45 scopes whose next script starts at codeEnd, those bytes
     are the next script's code. codeEnd comes from the .ebp opcode in 49 scopes; evctrl scope 1's last instruction lies 143 bytes
     past its directory span (DATA's recorded shared tail), so there it is q0's own extent (last non-zero record + 1)
     Rejected: a fixed end mark (16 scopes have no zero record); the published 0..2 bound (5 scopes have 3); a zero record
     inside a stream (none)
  E  the q3 page map's E = 1 + floor((len - 1) / 32) is the same over the padded count and over codeEnd in all 50 scopes (a
     multiple-of-4 pad cannot cross a multiple-of-32 boundary), so the page map's exactness does not discriminate them
  R  THE GUARDED RESOLVER. resolve() returns PAD for a record at or past codeEnd (not a coordinate), UNRESOLVED when no
     numbering addresses the line, and otherwise both candidate line indices (0-based, 1-based) - it never clamps and never
     picks a convention. Tallies: 53,710 both, 9 one-based-only, 0 zero-based-only, 6 unresolved, 59 pad = 53,784 records
  C  controls: a clamping resolver (min(line, lineCount - 1)) returns text for the six and is rejected; a suffix counter
     bounded at 2 misses five scopes; a planted non-zero record past codeEnd breaks Z; lengthening codeEnd by one breaks Z
Not claimed: why six coordinates name a missing line, which numbering the compiler used, or why the writer aligns q1.
Usage: python sn1_q0_domain.py [dir]
"""
import ast, os, struct, sys
DIR = sys.argv[1] if len(sys.argv) > 1 else r"D:/FFXII_TZA_extract/ps2data/image/ff12/in/bin"
MODS = ("ctrl", "btlctrl", "evctrl", "mapctrl")
HERE = os.path.dirname(os.path.abspath(__file__))
fails = 0


def check(name, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", name, detail)); fails += not ok


def sbn_blocks(b):
    n = struct.unpack_from("<I", b, 0)[0]; offs = struct.unpack_from("<%dI" % n, b, 4)
    return list(zip(offs, list(offs[1:]) + [len(b)]))


def sbn_group_read(b, o):
    L, base = struct.unpack_from("<II", b, o); p = o + 8; lines, groups, rem = [], [base], L
    while rem > 0:
        k = min(32, rem); lines += [base + r for r in struct.unpack_from("<%dH" % k, b, p)]; p += 2 * k; rem -= k
        if rem > 0:
            base = struct.unpack_from("<I", b, p)[0]; p += 4; groups.append(base)
    return L, groups, lines, p


def defs(path):
    src = open(path, encoding="utf-8").read(); tree = ast.parse(src)
    return {n.name: ast.get_source_segment(src, n) for n in tree.body if isinstance(n, ast.FunctionDef)}


pub, here = defs(os.path.join(HERE, "sn1_layouts.py")), defs(os.path.abspath(__file__))
check("I", all(pub.get(f) == here.get(f) for f in ("sbn_blocks", "sbn_group_read")), "sbn_blocks / sbn_group_read equal sn1_layouts.py's")


def oplen(op):
    return 1 if 0x03 <= op <= 0x47 else 3 if 0x48 <= op <= 0x63 else None


def resolve(lines, code_end, k, rec, clamp=False):
    """q0 record k of a scope -> ('PAD',) | ('UNRESOLVED', line, block) | ('LINE', idx0 or None, idx1 or None, texts)."""
    ln, bk, fl = rec
    if k >= code_end:
        return ("PAD",)
    if bk >= len(lines):
        return ("UNRESOLVED", ln, bk)
    L = len(lines[bk])
    if clamp:                                   # the rejected consumer: indexes the last line instead of reporting a gap
        ln = min(ln, L - 1)
    i0 = ln if ln < L else None                 # counting from 0
    i1 = ln - 1 if 1 <= ln <= L else None       # counting from 1
    if i0 is None and i1 is None:
        return ("UNRESOLVED", ln, bk)
    return ("LINE", i0, i1)


def logical_groups(s, starts):
    """Physical line indices per LOGICAL line: a line whose last character (decoded cp932, so a Shift-JIS trail byte 0x5C is
    not a backslash) is a backslash continues into the next (sn1_logical_lines.py K, 2026-09-28)."""
    groups, cont = [], False
    for i, a in enumerate(starts):
        if not cont: groups.append([])
        groups[-1].append(i)
        cont = s[a:s.index(b"\0", a)].decode("cp932", "replace").rstrip("\r\n \t").endswith("\\")
    return groups


def lookup(groups, code_end, k, rec):
    """One-based LOGICAL source lookup: q0's line counts logical lines, continuation lines folded (sn1_logical_lines.py V;
    first written 2026-09-28 as physical line - 1 on four literal anchors in blocks with no continuation, sn1_entry_lines.py S).
    A logical line may hold several statements and a statement may span several physical lines, so the result is the logical
    line's physical lines, not one statement. Not a proven compiler rule. The tag can also run one logical line LATE
    (sn1_variable_binding.py A / G): the returned line is an addressable coordinate, not the emitting statement's exact line.
    ('LINE', first physical index, [physical indices]) | ('UNRESOLVED', line, block) | ('PAD',)."""
    ln, bk, fl = rec
    if k >= code_end: return ("PAD",)
    if bk >= len(groups) or not 1 <= ln <= len(groups[bk]): return ("UNRESOLVED", ln, bk)
    g = groups[bk][ln - 1]
    return ("LINE", g[0], g)


scopes = []   # (module, i, recs, code_end, q offsets, ebp script start, next start or None)
internal = []  # scopes whose codeEnd comes from q0's own extent
lines_of = {}
groups_of = {}
for m in MODS:
    s = open(os.path.join(DIR, m + ".sbn"), "rb").read()
    lines_of[m] = [sbn_group_read(s, o)[2] for o, e in sbn_blocks(s)]
    groups_of[m] = [logical_groups(s, x) for x in lines_of[m]]
    c = open(os.path.join(DIR, m + ".ebp"), "rb").read()[0x80:]          # the EBP2 script chunk (marker 0x8000000B)
    dr = struct.unpack_from("<I", c, 0x18)[0]; n = struct.unpack_from("<I", c, dr)[0]
    starts = [struct.unpack_from("<I", c, dr + 4 + j * 0x30 + 8)[0] for j in range(n)]
    b = open(os.path.join(DIR, m + ".dbg"), "rb").read()
    o0 = struct.unpack_from("<I", b, 0)[0]; ns = struct.unpack_from("<I", b, o0)[0]
    offs = struct.unpack_from("<%dI" % (4 * ns + 1), b, o0 + 4)
    for i in range(ns):
        q = offs[4 * i:4 * i + 4]; n0 = (q[1] - q[0]) // 4
        recs = [struct.unpack_from("<HBB", b, q[0] + 4 * k) for k in range(n0)]
        last = max(k for k in range(n0) if recs[k][2] == 1); st = starts[i]
        nxt = min([x for x in starts if x > st], default=None)
        if (nxt is None or st + last < nxt) and oplen(c[st + last]):
            ce = last + oplen(c[st + last])                                  # from the script's own .ebp bytes
        else:                                                                # the last instruction lies outside the script's span
            ce = max(k for k in range(n0) if recs[k] != (0, 0, 0)) + 1; internal.append((m, i, st + last - (nxt or 0)))
        scopes.append((m, i, recs, ce, q, st, nxt))

# A / R
cat = {"both": 0, "one": 0, "zero": 0, "unres": [], "pad": 0}
one = []
for m, i, recs, ce, q, st, nxt in scopes:
    for k, r in enumerate(recs):
        v = resolve(lines_of[m], ce, k, r)
        if v[0] == "PAD": cat["pad"] += 1
        elif v[0] == "UNRESOLVED": cat["unres"].append((m, i, k, r[0], r[1], r[2]))
        elif v[1] is not None and v[2] is not None: cat["both"] += 1
        elif v[2] is not None: cat["one"] += 1; one.append((m, i, k))
        else: cat["zero"] += 1
SIX = [("btlctrl", 1, 3978, 559, 2, 1), ("btlctrl", 1, 3979, 559, 2, 0), ("btlctrl", 1, 3980, 559, 2, 0),
       ("mapctrl", 1, 5201, 558, 2, 1), ("mapctrl", 1, 5202, 558, 2, 0), ("mapctrl", 1, 5203, 558, 2, 0)]
counts = {m: [len(x) for x in lines_of[m]] for m in MODS}
check("A", cat["unres"] == SIX and cat["one"] == 9 and cat["zero"] == 0 and counts["btlctrl"][2] == 558 and counts["mapctrl"][2] == 557
      and all(k < len(recs) - 50 for m, i, k, *_ in cat["unres"] for m2, i2, recs, *_r in scopes if (m2, i2) == (m, i)),
      "unresolved under either numbering: %s; line == lineCount: %d; addressable only from 0: %d" % (cat["unres"], cat["one"], cat["zero"]))
total = sum(len(s[2]) for s in scopes)
check("R", (cat["both"], cat["one"], cat["zero"], len(cat["unres"]), cat["pad"]) == (53710, 9, 0, 6, 59) and total == 53784,
      "resolver tallies both %d, one-based-only %d, zero-based-only %d, unresolved %d, pad %d (of %d records)"
      % (cat["both"], cat["one"], cat["zero"], len(cat["unres"]), cat["pad"], total))

# Z
def pad_law(recs, ce):
    n0 = len(recs)
    return n0 == -(-ce // 4) * 4 and all(r == (0, 0, 0) for r in recs[ce:]) and all(r != (0, 0, 0) for r in recs[:ce])
zlaw = sum(pad_law(recs, ce) for m, i, recs, ce, q, st, nxt in scopes)
al01 = sum(q[0] % 16 == 0 and q[1] % 16 == 0 for m, i, recs, ce, q, st, nxt in scopes)
al23 = sum(q[2] % 16 == 0 and q[3] % 16 == 0 for m, i, recs, ce, q, st, nxt in scopes)
packed = [(m, i) for m, i, recs, ce, q, st, nxt in scopes if nxt is not None and nxt == st + ce]
notpacked = [(m, i, nxt - st, ce) for m, i, recs, ce, q, st, nxt in scopes if nxt is not None and nxt != st + ce]
suf = {(m, i): len(recs) - ce for m, i, recs, ce, q, st, nxt in scopes}
three = sorted(k for k, v in suf.items() if v == 3)
check("Z", len(scopes) == 50 and zlaw == 50 and al01 == 50 and al23 < 50 and len(packed) == 45 and notpacked == [("evctrl", 1, 6130, 6274)]
      and internal == [("evctrl", 1, 143)]
      and sorted(set(suf.values())) == [0, 1, 2, 3] and sum(v == 0 for v in suf.values()) == 16 and three == [("btlctrl", 22), ("ctrl", 1), ("evctrl", 3), ("mapctrl", 1), ("mapctrl", 3)],
      "q0 count = codeEnd rounded up to 4 in %d / 50 (codeEnd from the .ebp opcode in 49; from q0's own extent in %s, whose last "
      "instruction lies past its directory span); q0, q1 16-aligned in %d / 50 (q2 and q3 both in %d); next script starts at codeEnd in "
      "%d scopes (the other with a successor: %s, DATA's recorded evctrl scope 1 tail); pad 0..3, 3 at %s; %d scopes with no pad"
      % (zlaw, internal, al01, al23, len(packed), notpacked, three, sum(v == 0 for v in suf.values())))


# E
check("E", all(1 + (len(recs) - 1) // 32 == 1 + (ce - 1) // 32 for m, i, recs, ce, q, st, nxt in scopes),
      "the page-map length E is the same over the padded count and over codeEnd in all 50 scopes")

# C
m, i, recs, ce, q, st, nxt = next(s for s in scopes if (s[0], s[1]) == ("btlctrl", 1))
clamped = [resolve(lines_of[m], ce, k, recs[k], clamp=True)[0] for k in (3978, 3979, 3980)]
m2, i2, recs2, ce2, *_ = next(s for s in scopes if len(s[2]) > s[3])
p2 = list(recs2); p2[ce2] = (1, 0, 0)
two = sum(min(v, 2) != v for v in suf.values())
check("C", clamped == ["LINE"] * 3 and not pad_law(p2, ce2) and not pad_law(recs2, ce2 + 1) and two == 5,
      "clamp mutant resolves the missing line (%s); a planted record past codeEnd and codeEnd + 1 each break Z; a 0..2 bound misses %d scopes"
      % (clamped, two))
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
