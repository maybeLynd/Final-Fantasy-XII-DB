"""x_negatives.py - SN-1's residue, q3's head word X: the readings tested and how far each got (FABLE, Claude Opus 5.5,
2026-09-28). DATA from the archive (the four .dbg and .ebp files). This is a negative record for a disposition guard, not an answer.

  N1 btlctrl scopes 18 and 19: identical q0 flag layout and identical q3 maps, X = 1 and 2. Their bytecode (48 B each) differs in
     exactly two bytes, one push operand (4f 62 00 against 4f f9 01); their function tables have the same offsets and differ in one
     name-pool offset; their source lines differ (2218-2231 against 2239-2252)
  N2 simple formulas floor or ceil(feature / k) + c, k in 1..128, c in -3..3, over 14 per-scope features (code bytes, instructions (directory and q0),
     functions, jump-table entries, statements, source lines, 3-byte and 1-byte opcodes, pushes, jumps, q1 words, stack begin, table
     spans) and the sums of any two with floor(sum / k): the best reaches fewer than 40 of the 50 scopes
  N3 X as boundary crossings on a module-global grid (the code's absolute start in the script section or the file, grids of 8 to
     128 bytes, three forms): the best reaches fewer than 30 of 50
  C  control: the same search finds q2's count law, ceil(q0's instruction starts / 32), in all 50 - so it can find a law of this
     shape when one exists (with the .ebp directory's instruction count it is 49: evctrl scope 1's shared code tail)
"""
import itertools, os, struct, sys
DIR = sys.argv[1] if len(sys.argv) > 1 else r"D:/FFXII_TZA_extract/ps2data/image/ff12/in/bin"
fails = 0
def ok(tag, cond, msg):
    global fails
    print(("PASS " if cond else "FAIL ") + tag + "  " + msg); fails += (not cond)
rows = []; pair = {}
for m in ("ctrl", "btlctrl", "evctrl", "mapctrl"):
    b = open(os.path.join(DIR, m + ".dbg"), "rb").read(); e = open(os.path.join(DIR, m + ".ebp"), "rb").read()
    o0 = struct.unpack_from("<I", b, 0)[0]; ns = struct.unpack_from("<I", b, o0)[0]
    offs = struct.unpack_from("<%dI" % (4 * ns + 1), b, o0 + 4)
    ins0 = sum(b[offs[0] + 4 * k + 3] for k in range((offs[1] - offs[0]) // 4))
    D = base = None
    for o in range(0, len(e) - 0x40, 4):
        if struct.unpack_from("<I", e, o + 0xC)[0] == ins0 and struct.unpack_from("<I", e, o + 0x24)[0] == 0:
            for bs in range(0, o, 4):
                if struct.unpack_from("<I", e, bs + 0x18)[0] + 4 + bs == o: D, base = o, bs; break
            if D: break
    for i in range(ns):
        q0, q1, q2, q3 = offs[4 * i:4 * i + 4]; n0 = (q1 - q0) // 4
        recs = [struct.unpack_from("<HBB", b, q0 + 4 * k) for k in range(n0)]
        X = struct.unpack_from("<I", b, q3)[0]; q2c = struct.unpack_from("<I", b, q2)[0]
        ent = struct.unpack_from("<IHHIIIIIIHH", e, D + 0x30 * i)
        start, nins, nameOff, listOff, sepa, stack = ent[3], ent[4], ent[5], ent[6], ent[7], ent[8]
        nf = struct.unpack_from("<I", e, base + nameOff)[0]; nj = struct.unpack_from("<I", e, base + listOff)[0]
        code = e[base + start: base + start + n0]
        ops, k = [], 0
        while k < len(code):
            ops.append(code[k]); k += 1 if code[k] < 0x48 else 3
        F = {"n0": n0, "ins": nins, "q0ins": sum(r[2] for r in recs), "nf": nf, "nj": nj, "lines": len(set((r[0], r[1]) for r in recs)),
             "stmts": sum(1 for j in range(n0) if recs[j][2] == 1 and (j == 0 or recs[j][:2] != recs[j - 1][:2])),
             "ops3": sum(1 for o in ops if o >= 0x48), "ops1": sum(1 for o in ops if o < 0x48), "push": sum(1 for o in ops if o == 0x4F),
             "jmp": sum(1 for o in ops if 0x48 <= o < 0x60 and o not in (0x4F, 0x5D)), "q1": (q2 - q1) // 4, "stack": stack, "span": sepa - listOff}
        rows.append((m, i, X, F, start, base, q2c))
        if m == "btlctrl" and i in (18, 19):
            fn = [struct.unpack_from("<II", e, base + nameOff + 4 + 8 * j) for j in range(nf)]
            pair[i] = (X, code, fn, (min(r[0] for r in recs if r[0]), max(r[0] for r in recs)), recs)
(x18, c18, f18, l18, r18), (x19, c19, f19, l19, r19) = pair[18], pair[19]
diff = [j for j in range(min(len(c18), len(c19))) if c18[j] != c19[j]]
ok("N1", (x18, x19) == (1, 2) and [r[2] for r in r18] == [r[2] for r in r19] and diff == [33, 34] and [o for n, o in f18] == [o for n, o in f19]
   and sum(1 for a, b2 in zip(f18, f19) if a[0] != b2[0]) == 1 and l18 != l19,
   "X %d / %d; code differs at bytes %s; function offsets equal, one name offset differs; lines %s / %s" % (x18, x19, diff, l18, l19))
names = list(rows[0][3])
def search(target):
    best = 0
    for f in names:
        for kk in range(1, 129):
            for c in range(-3, 4):
                for mode in (0, 1):
                    hit = sum(1 for r in rows if ((r[3][f] // kk) if mode == 0 else (-(-r[3][f] // kk))) + c == target(r))
                    best = max(best, hit)
    for f, g in itertools.combinations(names, 2):
        for kk in range(1, 65):
            best = max(best, sum(1 for r in rows if (r[3][f] + r[3][g]) // kk == target(r)))
    return best
bx = search(lambda r: r[2])
ok("N2", bx < 40, "best simple formula for X reaches %d of %d scopes" % (bx, len(rows)))
bg = 0
for bias in (0, 1):
    for g in (8, 16, 32, 64, 128):
        for form in (0, 1, 2):
            hit = 0
            for m, i, X, F, start, base, q2c in rows:
                s = start + (base if bias else 0); n = F["n0"]; cross = (s + n - 1) // g - s // g
                hit += ([cross, cross + 1, (n + g - 1) // g][form] == X)
            bg = max(bg, hit)
ok("N3", bg < 30, "best module-global grid reading reaches %d of %d" % (bg, len(rows)))
bq = search(lambda r: r[6])
ok("C", bq == len(rows), "the same search finds q2's count law ceil(q0 instruction starts / 32) in %d of %d" % (bq, len(rows)))
print("FAILS", fails); sys.exit(1 if fails else 0)
