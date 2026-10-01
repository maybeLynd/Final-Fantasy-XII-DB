"""The navigation dataset (slot 4 of every map pack), parsed exactly as the pathfinder reads it.

Read-only over an extracted copy of the game (set FF12_EXTRACT; default D:/FFXII_TZA_extract).
The layout is the one the code reads, not one guessed from the bytes:
  header   +0x06 u16 triangle count (00383A30 loop bound)   +0x0A u16 region count (00382FF0, 00383850)
           +0x0C vertices  +0x10 triangles  +0x14 portals  +0x18 regions  +0x1C adjacency  +0x20 grid
           (the six offsets 00384160 rebases, plus +0x28, and the grid's own +8 / +0xC)
  vertex   8 B  f32 x, f32 z                                   (00382D10, 00382EA0 callers)
  triangle 8 B  u16 v[3], u16 region                           (00382D10; 00383A30 reads +6)
  portal   8 B  u16 vA, u16 vB, u8 +4, u8 +5, u8 +6            (00383850)
  region   0x22 B  +2 u16 triangle count, +0x14 u16 triangle index[]   (00383F10)
  adjacency  regionCount x regionCount u16, portal index, 0 = no portal   (00383850)
  grid     u8 cellW, u8 cellH, u8 cols, u8 rows, i16 originX, i16 originZ, +8 cell table, +0xC list pool
           cell table: cols*rows u16, 0xFFFF = empty, else offset into the pool of a 0xFF-terminated region list

Every test below is one the layout could fail. HYPOTHESES (not read from code, tested here): header +4 is the
vertex count and +8 the portal count. Positive control: the map-pack census found slot 4 in 461 files.
FABLE, 2026-09-19.
"""
import os, struct, glob, collections

ROOT = os.environ.get("FF12_EXTRACT", "D:/FFXII_TZA_extract")
paths = sorted(glob.glob(os.path.join(ROOT, "ps2data", "plan_master", "map_ctrl", "**", "*.mpk"), recursive=True))
print("control: .mpk files found:", len(paths), "(published 550)")


def slot4(d):
    count = struct.unpack_from("<I", d, 0)[0]
    sizes = struct.unpack_from("<%dI" % count, d, 4)
    pos = ((count + 1) * 4 + 0x3F) & ~0x3F
    for i, s in enumerate(sizes):
        if not s:
            continue
        pos += 0x40
        if i == 4:
            return d[pos:pos + s]
        pos += s
    return None


u16 = lambda b, o: struct.unpack_from("<H", b, o)[0]
u32 = lambda b, o: struct.unpack_from("<I", b, o)[0]
fails = collections.Counter()
ok = collections.Counter()
b4 = collections.Counter(); b6 = collections.Counter(); gated = collections.Counter()
maxreg = 0; maxtri_per_region = 0; nfiles = 0; regions_total = 0; portals_total = 0
hyp_v = hyp_p = 0


def check(name, cond):
    (ok if cond else fails)[name] += 1
    return cond


for p in paths:
    n = slot4(open(p, "rb").read())
    if n is None:
        continue
    nfiles += 1
    ntri, nreg = u16(n, 6), u16(n, 0xA)
    oV, oT, oP, oR, oA, oG = (u32(n, o) for o in (0xC, 0x10, 0x14, 0x18, 0x1C, 0x20))
    if not check("first u32 is 1", u32(n, 0) == 1):
        continue
    if not check("six offsets inside the section", all(0 < o < len(n) for o in (oV, oT, oP, oR, oA, oG))):
        continue
    check("region count <= 0x80 (the search's fixed arrays)", nreg <= 0x80)
    maxreg = max(maxreg, nreg)
    nvert_by_gap = (oT - oV) // 8
    hyp_v += (nvert_by_gap - u16(n, 4) in (1, 2))   # the array ends with 8 or 16 bytes of padding, to a 16-byte boundary
    nvert_by_gap = u16(n, 4)                          # index bounds below are tested against the HEADER count
    # triangles
    tri_ok = reg_ok = True
    for t in range(ntri):
        a, b, c, r = struct.unpack_from("<4H", n, oT + 8 * t)
        tri_ok &= max(a, b, c) < nvert_by_gap
        reg_ok &= r < nreg
    check("every triangle vertex index < header vertex count (+4)", tri_ok)
    check("every triangle's region id (+6) < region count", reg_ok)
    # regions
    back_ok = cnt_ok = True
    for r in range(nreg):
        k = u16(n, oR + 0x22 * r + 2)
        maxtri_per_region = max(maxtri_per_region, k)
        cnt_ok &= k <= 7
        for j in range(min(k, 7)):
            t = u16(n, oR + 0x22 * r + 0x14 + 2 * j)
            back_ok &= t < ntri and u16(n, oT + 8 * t + 6) == r
    regions_total += nreg
    check("a region lists at most 7 triangles (0x22 - 0x14 = 14 bytes)", cnt_ok)
    check("every triangle a region lists names that region back", back_ok)
    # adjacency + portals
    adj = struct.unpack_from("<%dH" % (nreg * nreg), n, oA)
    nport = max(adj) + 1 if adj else 1
    hyp_p += (u16(n, 8) in (nport, nport - 1))
    portals_total += nport - 1
    check("adjacency diagonal is 0 (no portal to itself)", all(adj[i * nreg + i] == 0 for i in range(nreg)))
    check("adjacency is symmetric in WHERE portals exist", all((adj[i * nreg + j] != 0) == (adj[j * nreg + i] != 0) for i in range(nreg) for j in range(nreg)))
    pv_ok = True
    for q in set(adj) - {0}:
        va, vb, g4, g5, g6 = struct.unpack_from("<HHBBB", n, oP + 8 * q)
        pv_ok &= va < nvert_by_gap and vb < nvert_by_gap
        b4[g4] += 1; b6[g6] += 1
        if g4 != 0xFF:
            gated[g5] += 1
    check("every portal's two vertex indices < header vertex count (+4)", pv_ok)
    # grid
    cw, ch, cols, rows = struct.unpack_from("<4B", n, oG)
    oC, oL = u32(n, oG + 8), u32(n, oG + 0xC)
    if check("grid sub-offsets inside the section, cell size non-zero", 0 < oC < len(n) and 0 < oL < len(n) and cw and ch):
        lst_ok = True
        for c in range(cols * rows):
            e = u16(n, oC + 2 * c)
            if e == 0xFFFF:
                continue
            q = oL + e
            while q < len(n) and n[q] != 0xFF:
                lst_ok &= n[q] < nreg
                q += 1
            lst_ok &= q < len(n)
        check("every grid cell's list is 0xFF-terminated region ids", lst_ok)

print("files with a slot 4:", nfiles, "(published 461)")
print("regions in all:", regions_total, "; largest region count in one file:", maxreg, "; most triangles one region lists:", maxtri_per_region)
print("portals in all (by highest adjacency entry):", portals_total)
for k in sorted(set(ok) | set(fails)):
    print("  %-72s pass %4d  fail %4d" % (k, ok[k], fails[k]))
print("hypothesis: header +4 == vertex count (offset gap / 8, less one or two entries of padding):", hyp_v, "of", nfiles)
print("hypothesis: header +8 == portal count (highest adjacency entry, or that + 1):", hyp_p, "of", nfiles)
print("portal byte +4 (0xFF = not script-gated):", sorted(b4.items(), key=lambda kv: -kv[1])[:8])
print("portal byte +6 (mover-class mask):", sorted(b6.items(), key=lambda kv: -kv[1])[:10])
print("gated portals by map id (+5):", len(gated), "distinct ids; largest id", max(gated) if gated else None, "; gated portals", sum(gated.values()))
