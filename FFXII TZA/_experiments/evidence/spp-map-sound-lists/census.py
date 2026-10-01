"""Every SPP1 map-sound list in the archive: the loose .spp and slot 10 of every .mpk.

Read-only over FFXII_TZA.vbf (set FF12_VBF). The .mpk split is the arena splitter's (see
mpk-map-pack-slots/census.py). SPP1 fields as the code reads them: +0x04 u32 count (00363774, 00346291,
003469D5); +0x08 u32 passed to the SeSep walk as its byte length (00363627 -> 002DF070); +0x0C u32
offset of the SeSep bank from the list's start, used when no separate bank is given (00363607);
+0x20 u32 id[count] (00363791, 0034629A, 003469DA). The SeSep walk (002DF070) is replayed exactly:
remaining = (length + 15) & ~15; while remaining > 16: chunk magic 'SeSe' + 'p', size = +0x0C with bit 31
cleared, stop if remaining < size, register (+0x08 id), remaining -= size, advance by size.
Reports, for each list: whether the walk consumes the whole length, whether the registered chunk ids
are the listed ids, the id ranges and bit 31, and the per-weather table at +0x1A (00363B40), and the header words and table no reader was found for.
Positive control: the extension census lists 1 .spp and 550 .mpk entries.
FABLE, 2026-09-13.
"""
import sys, os, io, struct, zlib, collections
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../../Tools/analysis-kit/gfz-scripts"))
from census_format_magics import load_index

BLOCK = 0x10000
f = io.open(os.environ["FF12_VBF"], "rb")
names, blocks = load_index(f)


def read_all(path):
    sb, size, off = names[path]
    n = (size + BLOCK - 1) // BLOCK
    out = b""
    f.seek(off)
    for i in range(n):
        csize = blocks[sb + i] or BLOCK
        expected = BLOCK if i < n - 1 else size - BLOCK * (n - 1)
        chunk = f.read(csize)
        if csize != expected:
            chunk = zlib.decompress(chunk)
        out += chunk
    assert len(out) == size
    return out


def mc(c, n=None):
    items = sorted(c.items(), key=lambda kv: (-kv[1], str(kv[0])))
    return items if n is None else items[:n]


def walk(buf, length):
    """002DF070 replayed; returns (ids registered, bytes left, stop reason)."""
    rem = (length + 15) & ~15
    pos = 0; ids = []
    while rem > 16:
        if pos + 16 > len(buf):
            return ids, rem, "past the buffer"
        if buf[pos:pos + 4] != b"SeSe" or buf[pos + 4] != 0x70:
            return ids, rem, "magic"
        size = struct.unpack_from("<I", buf, pos + 12)[0] & 0x7FFFFFFF
        if rem < size:
            return ids, rem, "size"
        ids.append(struct.unpack_from("<I", buf, pos + 8)[0])
        rem -= size; pos += size
        if size == 0:
            return ids, rem, "zero size"
    return ids, rem, "end"


lists = []
spp = sorted(p for p in names if p.lower().endswith(".spp"))
mpk = sorted(p for p in names if p.lower().endswith(".mpk"))
print("control: .spp entries:", len(spp), "(published 1); .mpk entries:", len(mpk), "(published 550)")
for p in spp:
    b = read_all(p)
    boff = struct.unpack_from("<I", b, 0x0C)[0]
    lists.append((p, b, b[boff:], "loose: embedded bank at +0x0C"))   # 003635E0 with no bank: bank = list + [list+0x0C]
slot10 = 0; no_bank = 0
for p in mpk:
    d = read_all(p)
    n = struct.unpack_from("<I", d, 0)[0]
    sz = struct.unpack_from("<%dI" % n, d, 4)
    pos = ((n + 1) * 4 + 0x3F) & ~0x3F
    sec = {}
    for i, s in enumerate(sz):
        if not s:
            continue
        sec[i] = d[pos + 0x40:pos + 0x40 + s]
        pos += 0x40 + s
    if 10 in sec:
        slot10 += 1
        if 0 not in sec:
            no_bank += 1
        lists.append((p, sec[10], sec.get(0, b""), "mpk: slot-0 bank"))   # 003775D0 passes slot 0 as the bank
print("SPP1 lists: %d (%d loose .spp + %d .mpk slot 10; slot 10 without a slot 0: %d)" % (len(lists), len(spp), slot10, no_bank))

C = collections.Counter
magic = C(); counts = C(); stop = C(); order = C(); w10 = C(); w12 = C(); w14 = C(); w1c = C(); a_rule = C(); b_rule = C(); end_rule = C()
idrange = C(); bit31 = C(); dup_ids = C(); tailA = C(); tailB = C(); first = None; endsz = C(); x1012 = C()
wcount = C(); widx = C(); wshape = C(); tailAbytes = C()
for p, b, bank, kind in lists:
    magic[b[:4]] += 1
    cnt, length, end = struct.unpack_from("<III", b, 4)
    counts[cnt] += 1
    u10, u12 = struct.unpack_from("<HH", b, 0x10)
    w10[u10] += 1; w12[u12] += 1
    w14[struct.unpack_from("<I", b, 0x14)[0]] += 1; w1c[struct.unpack_from("<I", b, 0x1C)[0]] += 1
    A, B = struct.unpack_from("<HH", b, 0x18)
    ids_end = 0x20 + 4 * cnt
    a_rule["+0x18 == align16(0x20 + 4*count)" if A == (ids_end + 15) & ~15 else "+0x18 other"] += 1
    b_rule["+0x1A == 0" if B == 0 else ("+0x18 < +0x1A < +0x0C" if A < B < end else "+0x1A other")] += 1
    end_rule[kind + (": +0x0C == list size" if end == len(b) else ": +0x0C == %s" % ("start of the embedded bank" if kind.startswith("loose") else "other"))] += 1
    endsz["list size - +0x0C = %d" % (len(b) - end)] += 1
    x1012[(u10, "FFFF" if u12 == 0xFFFF else "map-like")] += 1
    if B:   # 00363B40: u16 n at list+B, i16 index[i] at +2+2i for i < min(n, 3); an index is used when 0 <= index < count and id > 0
        n = struct.unpack_from("<H", b, B)[0]
        wcount[n] += 1
        idx = struct.unpack_from("<%dh" % min(n, 7), b, B + 2)
        wshape["all %d indices in 0..count-1" % min(n, 3) if all(0 <= x < cnt for x in idx[:3]) else "some index outside 0..count-1"] += 1
        for x in idx[:3]:
            widx["-1" if x == -1 else "in range" if 0 <= x < cnt else "other"] += 1
    tailAbytes["nonzero" if any(b[A:(B or end)]) else "all zero"] += 1
    if A < (B or end):
        tailA[(B or end) - A] += 1
    if B:
        tailB[end - B] += 1
    ids = list(struct.unpack_from("<%dI" % cnt, b, 0x20))
    reg, rem, why = walk(bank, length)
    stop["%s: walk stops at %s with %s" % (kind, why, "< 16 bytes left" if rem <= 16 else "%d bytes left" % rem)] += 1
    order["chunk ids == listed ids, in order" if reg == ids else ("same set" if set(reg) == set(ids) else "different")] += 1
    dup_ids["ids distinct" if len(set(ids)) == len(ids) else "duplicate ids"] += 1
    for x in ids:
        bit31[bool(x & 0x80000000)] += 1
        v = x & 0x7FFFFFFF
        idrange["1000..1999" if 1000 <= v < 2000 else "10000..19999" if 10000 <= v < 20000 else "50000..59999" if 50000 <= v < 60000 else "other"] += 1
    if first is None:
        first = (p, cnt, length, hex(end), (A, B), ids[:12], reg[:12])
print("magic:", [(k.hex(), v) for k, v in mc(magic)])
print("count (top):", mc(counts, 12), "; range", min(counts), "..", max(counts))
print("SeSep walk with +0x08 as the length:", mc(stop))
print("ids:", mc(order), mc(dup_ids), "; range", mc(idrange), "; bit 31 set", mc(bit31))
print("+0x0C:", mc(end_rule))
print("+0x18 / +0x1A:", mc(a_rule), mc(b_rule), "; bytes from +0x18 to the next boundary (top):", mc(tailA, 6), "; from +0x1A to +0x0C (top):", mc(tailB, 6))
print("unread header +0x10 u16:", mc(w10, 6), "; +0x12 u16 (top):", mc(w12, 6), "; distinct", len(w12), "; +0x14:", mc(w14, 4), "; +0x1C:", mc(w1c, 4))
print("weather table at +0x1A: u16 n", mc(wcount), "; first min(n,3) indices:", mc(wshape), mc(widx), "; bytes +0x18..: ", mc(tailAbytes))
print("list size minus +0x0C:", mc(endsz, 8), "; +0x10 against +0x12:", mc(x1012))
print("first list:", first)
