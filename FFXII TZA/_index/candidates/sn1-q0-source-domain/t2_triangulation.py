"""t2_triangulation.py - SN-1: the T0 index binding checked by a route that does not use source text (FABLE, Claude Opus 5.5,
2026-09-28, on ASTRA-REQ-FABLE-SN1-GLOBAL-NAME-CONTROL). DATA from the archive.

Three independent tables meet on one variable index n:
  - the .ebp variable descriptor table (image header +0x28, {u32 count; 8-byte records}; the resolver reads the record's first dword,
    [table + 4 + 8n]) gives n's native descriptor;
  - the .dbg T2 global directory ({count; {id; namePos}}, header +0x14) names every global by that same descriptor dword;
  - the .dbg T0 table ({count; nameOffset}, header +0x04) names index n directly.

  G1 evctrl indices 1 .. 0x3E: every native descriptor is a class-0 (global) width-0 (u8) descriptor, each matches exactly ONE T2
     record, and that record's name is T0[n]; none is T0[n + 1]
  G2 the sampled file variable test_load_flg (T0[0x61]) has a class-1 descriptor and, as a file variable, no T2 match
  C  controls: T0 read one slot on (n + 1) matches no T2 name for any of the 62; the descriptor + 1 matches no T2 record's name T0[n]
  So the T0 binding in variable_binding.py is confirmed without source text. The source-text alignment an on()-style predicate reports
  (the unshifted name missing from a tagged group, the next name present) comes from the next-line tagging in
  assignment_attribution.py, not from a shifted variable table - it must not be read as a +1 rename.
  Not claimed: other modules or scopes, type-flag meanings, native values, lifetime or reachability.
"""
import os, struct, sys
DIR = sys.argv[1] if len(sys.argv) > 1 else r"D:/FFXII_TZA_extract/ps2data/image/ff12/in/bin"
fails = 0
def ok(tag, cond, msg):
    global fails
    print(("PASS " if cond else "FAIL ") + tag + "  " + msg); fails += (not cond)
m = "evctrl"
b = open(os.path.join(DIR, m + ".dbg"), "rb").read()
h = struct.unpack_from("<16I", b, 0); pool, T0, T2 = h[2], h[1], h[5]
name = lambda p: b[pool + p:b.index(bytes([0]), pool + p)].decode("latin-1")
c0 = struct.unpack_from("<I", b, T0)[0]; T0n = [name(x) for x in struct.unpack_from("<%dI" % c0, b, T0 + 4)]
c2 = struct.unpack_from("<I", b, T2)[0]; P = struct.unpack_from("<%dI" % (2 * c2), b, T2 + 4)
t2 = {}
for i in range(c2): t2.setdefault(P[2 * i], []).append(name(P[2 * i + 1]))
e = open(os.path.join(DIR, m + ".ebp"), "rb").read()
o0 = struct.unpack_from("<I", b, 0)[0]; ns = struct.unpack_from("<I", b, o0)[0]
offs = struct.unpack_from("<%dI" % (4 * ns + 1), b, o0 + 4)
ins0 = sum(b[offs[0] + 4 * k + 3] for k in range((offs[1] - offs[0]) // 4))
base = None
for o in range(0, len(e) - 0x40, 4):
    if struct.unpack_from("<I", e, o + 0xC)[0] == ins0 and struct.unpack_from("<I", e, o + 0x24)[0] == 0:
        for bs in range(0, o, 4):
            if struct.unpack_from("<I", e, bs + 0x18)[0] + 4 + bs == o: base = bs; break
        if base is not None: break
tbl = base + struct.unpack_from("<I", e, base + 0x28)[0]; cnt = struct.unpack_from("<I", e, tbl)[0]
desc = lambda n: struct.unpack_from("<I", e, tbl + 4 + 8 * n)[0]
rows = []
for n in range(1, 0x3F):
    d = desc(n); names = t2.get(d, [])
    rows.append((n, d, (d >> 24) & 7, d >> 28, names, T0n[n], T0n[n + 1]))
ok("G1", len(rows) == 62 and all(r[2] == 0 and r[3] == 0 and len(r[4]) == 1 and r[4][0] == r[5] and r[4][0] != r[6] for r in rows),
   "descriptors %08X .. %08X: 62 of 62 class 0 width 0, one T2 record each, named T0[n] (e.g. n 1 %r, n 0x3E %r); table count %d"
   % (rows[0][1], rows[-1][1], rows[0][5], rows[-1][5], cnt))
d61 = desc(0x61)
ok("G2", T0n[0x61] == "test_load_flg" and (d61 >> 24) & 7 == 1 and d61 not in t2,
   "T0[0x61] %s: descriptor %08X, class %d, T2 match %s" % (T0n[0x61], d61, (d61 >> 24) & 7, t2.get(d61)))
ok("C", not any(r[6] in r[4] for r in rows) and not any(T0n[r[0]] in t2.get(r[1] + 1, []) for r in rows),
   "T0[n + 1] matches no T2 name for any of the 62; descriptor + 1 never names T0[n]")
print("FAILS", fails); sys.exit(1 if fails else 0)
