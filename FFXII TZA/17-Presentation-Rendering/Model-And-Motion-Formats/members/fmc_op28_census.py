"""@FMC op-0x28 authored-value census — SWE2-DATA, UQ-218 pass 15.

Walks every .cm/.ca @FMC entry and collects the dword operand (+4) of
every op-0x28 command, with the entry's name. Code side (certified
image): 0x28 -> 00520720 -> 003E6AA0 (obj+0x304 bits 27-31, dirty bit
27) -> dirty pass 00427DE0 -> 003B3C00 (range-check 0..10, handle table
02E9D480) -> 0024FE70(effectCtx, lane): byte[def+0xA+lane] selects
dword[def+0x2C+4*map] -> 0020E600 -> 00333280 child spawn (lane at
child+0x11). So the authored dword is a REQUEST LANE into an 11-entry
per-effect authored map, not a global enum; lane 0 = no request.

Walker note (corrected 2026-09-30): the command head u16 packs
{len:9, op:7} where len is the TOTAL command size — advance co += len.
An earlier pass's co += 2+len desynced the stream and produced a
garbage value set; the totals below are the corrected run.

    FF12_VBF=<archive> python fmc_op28_census.py
"""
import sys, os, io, struct, zlib, collections
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts"))
from census_format_magics import load_index

BLOCK = 0x10000
f = io.open(os.environ["FF12_VBF"], "rb")
names, blocks = load_index(f)

def read_all(p):
    sb, size, off = names[p]
    n = (size + BLOCK - 1) // BLOCK
    out = b""
    f.seek(off)
    for i in range(n):
        cs = blocks[sb + i] or BLOCK
        exp = BLOCK if i < n - 1 else size - BLOCK * (n - 1)
        c = f.read(cs)
        if cs != exp:
            c = zlib.decompress(c)
        out += c
    return out

hits = collections.defaultdict(list)
total = 0
for p in sorted(names):
    pl = p.lower()
    if not (pl.endswith(".ca") or pl.endswith(".cm")):
        continue
    d = read_all(p)
    if len(d) < 0x40:
        continue
    var, clen, cnt = struct.unpack_from("<III", d, 4)
    base = 0x40 if var == 1 else 0x30
    for i in range(cnt):
        v = struct.unpack_from("<I", d, base + i * 4)[0]
        if var == 1 and v == 0:
            continue
        o = base + v
        if d[o:o + 4] != b"@FMC":
            continue
        nm = d[o + 0x10:o + 0x30].split(b"\0")[0].decode("ascii", "replace")
        elen = struct.unpack_from("<I", d, o + 8)[0]
        rend = o + elen
        ro, ri, rcount = o + 0x30, 0, struct.unpack_from("<I", d, o + 0x0C)[0]
        while ro + 6 <= rend and ri < rcount:
            subc = d[ro + 3]
            rlen = struct.unpack_from("<H", d, ro + 4)[0]
            if rlen < 6 or ro + rlen > rend:
                break
            so = ro + 6
            for _ in range(subc):
                key, cw = struct.unpack_from("<HH", d, so)
                cc = cw & 0x3F
                slen = (cw >> 6) & 0x3FF
                co, cend = so + 4, so + slen
                while co + 2 <= cend:
                    head = struct.unpack_from("<H", d, co)[0]
                    op = head & 0x7F
                    clen2 = (head >> 7) & 0x1FF
                    if clen2 < 2 or co + clen2 > cend:
                        co = cend
                        break
                    if op == 0x28 and clen2 >= 8:
                        val = struct.unpack_from("<I", d, co + 4)[0]
                        hits[val].append((p, nm))
                        total += 1
                    co += clen2
                so += slen
            ro += rlen
            ri += 1

fails = 0
def check(name, cond, detail=""):
    global fails
    if not cond:
        fails += 1
    print(("FAIL " if not cond else "ok   ") + name, detail)

check("total op-0x28 commands == 115", total == 115, "got %d" % total)
v1 = hits.get(1, [])
check("value 1 authored 112x in exactly 4 monster files",
      len(v1) == 112 and {p.split("/")[-1] for p, _ in v1}
      == {"m1043_10.ca", "m1044_10.ca", "m1132_10.ca", "m1133_10.ca"},
      "%d entries" % len(v1))
check("value 1 block names are the locomotion/reaction set",
      {nm for _, nm in v1}
      == {"ready", "knockback_s", "knockback_l", "c_turbo", "ev_walk", "avoid"})
v10 = hits.get(10, [])
check("value 10 authored 3x, all in m1143_10.ca",
      len(v10) == 3 and all(p.endswith("m1143_10.ca") for p, _ in v10),
      [(p.split("/")[-1], nm) for p, nm in v10])
check("value 10 names are knockback_l/dead",
      sorted(nm for _, nm in v10) == ["dead", "knockback_l", "knockback_l"])
check("no other authored lane values", set(hits) <= {1, 10}, sorted(hits))
check("every value inside the 003B3C00 range-check 0..10",
      all(0 <= v <= 10 for v in hits))
print("FAILS", fails)
sys.exit(1 if fails else 0)
