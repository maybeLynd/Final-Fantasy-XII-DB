"""assignment_attribution.py - SN-1: a q0 coordinate addresses a logical source line, but that line need not be the statement that
emitted the code (FABLE, Claude Opus 5.5, 2026-09-28, on ASTRA-REQ-FABLE-SN1-ASSIGNMENT-ATTRIBUTION). DATA from the archive; lines
through the block's own 32-line map, continuations folded with the CP932-aware test of logical_lines2.py, variables through T0 as in
variable_binding.py.

  A1 four evctrl pairs "PUSHII v / POPV 0x61" (0x61 = T0 test_load_flg; the pc named is the POPV, the push 3 bytes before, both one tag): scope 1 pc 5394 (v 1), scope 1 pc 5598 (v 0), scope 5 pc 1278
     (v 99), scope 9 pc 582 (v 99). Each start record's 1-based logical line lands on a statement that is NOT that assignment - a
     'test_event_count = 0' or a closing brace - and the physical line just before it is exactly 'test_load_flg = v' with the pushed v
  A2 the rule is not a universal 'minus one': in btlctrl scope 1 pc 531 the assignment 'loop_flg = 0;' carries its own line, and the
     evctrl askpos call at pc 22 carries its own line 417 (entry_lines.py E1, logical_lines2.py L2) - which source statement a
     tagged group contains varies, and no emission rule is claimed
  C  controls: the preceding-line match needs the right variable and the right literal - T0 entry 0x60 or the literal + 1
     matches none of the four preceding lines
"""
import os, re, struct, sys
DIR = sys.argv[1] if len(sys.argv) > 1 else r"D:/FFXII_TZA_extract/ps2data/image/ff12/in/bin"
BS = bytes([92])
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
    return [s[a:s.find(bytes([0]), a)] for a in starts]
def cont(t):
    t = t.rstrip(b" \t\r\n"); i, last = 0, None
    while i < len(t):
        c = t[i]
        if (0x81 <= c <= 0x9F or 0xE0 <= c <= 0xFC) and i + 1 < len(t): last = t[i:i + 2]; i += 2
        else: last = t[i:i + 1]; i += 1
    return last == BS
def logical_to_physical(L, ln):
    logical, i = 0, 0
    while i < len(L):
        logical += 1
        if logical == ln: return i
        while i < len(L) and cont(L[i]): i += 1
        i += 1
    return None
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
def t0(m):
    b = open(os.path.join(DIR, m + ".dbg"), "rb").read()
    h = struct.unpack_from("<16I", b, 0); pool, T0 = h[2], h[1]; c = struct.unpack_from("<I", b, T0)[0]
    return [b[pool + x:b.index(bytes([0]), pool + x)].decode("latin-1") for x in struct.unpack_from("<%dI" % c, b, T0 + 4)]
E = sbn_lines("evctrl", 0); T = t0("evctrl")
def assign_re(var, v): return re.compile(rb"^\s*" + re.escape(var.encode()) + rb"\s*=\s*" + str(v).encode() + rb"\s*;?")
rows = []
for sc, pc in ((1, 5394), (1, 5598), (5, 1278), (9, 582)):
    c = code("evctrl", sc); Q = q0("evctrl", sc)
    # ASTRA's pc is the POPV; its PUSHII is the 3-byte instruction before it, and both carry the same q0 tag
    push, v = c[pc - 3], struct.unpack_from("<H", c, pc - 2)[0]; popv, op = c[pc], struct.unpack_from("<H", c, pc + 1)[0]
    ln, bk, fl = Q[pc]
    assert Q[pc - 3] == Q[pc], "push and POPV carry different tags"
    p = logical_to_physical(E, ln)
    tagged, before = E[p].strip(), E[p - 1].strip()
    rows.append(dict(sc=sc, pc=pc, push=push, v=v, popv=popv, op=op, var=T[op], ln=ln, bk=bk, fl=fl, phys=p + 1,
                     tagged_is=bool(assign_re(T[op], v).match(tagged)), before_is=bool(assign_re(T[op], v).match(before)),
                     before_wrong_var=bool(assign_re(T[op - 1], v).match(before)), before_wrong_lit=bool(assign_re(T[op], v + 1).match(before)),
                     tagged=tagged[:28], before=before[:28]))
ok("A1", all(r["push"] == 0x4F and r["popv"] == 0x49 and r["op"] == 0x61 and r["var"] == "test_load_flg" and r["bk"] == 0 and r["fl"] == 1
             and not r["tagged_is"] and r["before_is"] for r in rows),
   "; ".join("sc %d pc %d push %d popv %s -> tag %d = physical %d %r, preceding %r" % (r["sc"], r["pc"], r["v"], r["var"], r["ln"], r["phys"], r["tagged"], r["before"]) for r in rows))
B = sbn_lines("btlctrl", 2); bq = q0("btlctrl", 1)[531]; own = B[bq[0] - 1].strip()
Eq = q0("evctrl", 1)[22]; call = E[logical_to_physical(E, Eq[0])].strip()
ok("A2", own.startswith(b"loop_flg") and Eq[0] == 417 and call.startswith(b"askpos("),
   "btlctrl pc 531 carries its own statement %r; evctrl pc 22 carries its own %r at line 417" % (own[:20], call[:20]))
ok("C", not any(r["before_wrong_var"] or r["before_wrong_lit"] for r in rows) and all(r["before_is"] for r in rows),
   "operand 0x60 or literal + 1 matches none of the preceding lines; only the exact variable and literal do")
print("FAILS", fails); sys.exit(1 if fails else 0)
