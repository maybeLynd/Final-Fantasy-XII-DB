"""The PC font data under gamedata/d3d11/artdata/font: fontlist.ah, <font>.dat, <font>.ker, <font>.fex.

Read-only over FFXII_TZA.vbf (set FF12_VBF). Rules as the code applies them:
- 001B4930 reads the language's fontlist.ah (chosen by 001B44A0) one whitespace-separated name at a time
  and requests <dir><name>.dat;
- 001B4D70 reads the .dat: a 0x28-byte header (+0x04 glyph count, +0x1C flags) then 0x24-byte glyph records
  until the buffer end (001B4ED2-001B4F52); 001FDF80 compares the stored glyphs with the header count;
  flags bit 0 requests <name>.ker (001B5024 -> 001B5750), bit 1 requests <name>.fex (001B5045 -> 001B5480);
- 001B5230 reads the .ker as 12-byte records {u32 first, u32 second, i32 adjust} to the buffer end;
- 001B4C00 reads the .fex as records {u32 key, i32 n, u32 value[n]} to the buffer end, abandoning the file
  when a key repeats (001FDB90 returns false).
Reports, per language directory, which .dat/.ker/.fex the list and flags request, whether each requested
file parses exactly by these rules, and which shipped files nothing requests.
Positive control: the extension census lists 34 .ker and 14 .fex entries.
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


def fex_walk(d):
    pos = 0; keys = set(); recs = 0; vals = 0
    while pos < len(d):
        if pos + 8 > len(d):
            return recs, vals, "header past the end at %d" % pos
        k, n = struct.unpack_from("<Ii", d, pos); pos += 8
        if k in keys:
            return recs, vals, "repeated key 0x%08X at %d (001FDB90 refuses; file abandoned)" % (k, pos - 8)
        keys.add(k)
        if n > 0 and pos + 4 * n > len(d):
            return recs, vals, "values past the end at %d (n = %d)" % (pos, n)
        pos += 4 * max(n, 0); recs += 1; vals += max(n, 0)
    return recs, vals, "exact"


ROOT = "gamedata/d3d11/artdata/font/"
ker = sorted(p for p in names if p.lower().endswith(".ker"))
fex = sorted(p for p in names if p.lower().endswith(".fex"))
dat = sorted(p for p in names if p.lower().startswith(ROOT) and p.lower().endswith(".dat"))
print("control: .ker entries:", len(ker), "(published 34); .fex entries:", len(fex), "(published 14); font .dat:", len(dat))
langs = sorted({p[len(ROOT):].split("/")[0] for p in ker + fex + dat})
print("language directories:", langs, "; fontlist.ah exists for:", sorted(l for l in langs if ROOT + l + "/fontlist.ah" in names))
requested = set()
C = collections.Counter
datshape = C(); flags = C(); kershape = C(); fexshape = C()
for lang in langs:
    lp = ROOT + lang + "/fontlist.ah"
    if lp not in names:
        continue
    lst = read_all(lp).decode("latin1").split()
    row = []
    for nm in lst:
        dp = ROOT + lang + "/" + nm + ".dat"
        if dp not in names:
            row.append("%s: .dat missing" % nm); continue
        requested.add(dp)
        d = read_all(dp)
        cnt, fl = struct.unpack_from("<I", d, 4)[0], struct.unpack_from("<I", d, 0x1C)[0]
        body = len(d) - 0x28
        datshape["size == 0x28 + 0x24 * count" if body % 0x24 == 0 and body // 0x24 == cnt else "size other"] += 1
        flags[fl] += 1
        parts = ["%s(f%d)" % (nm, fl)]
        if fl & 1:
            kp = ROOT + lang + "/" + nm + ".ker"
            if kp in names:
                requested.add(kp); k = read_all(kp)
                kershape["requested .ker: size % 12 == 0" if len(k) % 12 == 0 else "requested .ker: size % 12 != 0"] += 1
                parts.append("ker %d pairs" % (len(k) // 12))
            else:
                kershape["requested .ker missing"] += 1; parts.append("ker MISSING")
        if fl & 2:
            xp = ROOT + lang + "/" + nm + ".fex"
            if xp in names:
                requested.add(xp); r, v, why = fex_walk(read_all(xp))
                fexshape["requested .fex: " + ("exact" if why == "exact" else "not exact")] += 1
                parts.append("fex %d keys %d values %s" % (r, v, why))
            else:
                fexshape["requested .fex missing"] += 1; parts.append("fex MISSING")
        row.append(" ".join(parts))
    print("%s (%d fonts): %s" % (lang, len(lst), "; ".join(row)))
print(".dat shape:", sorted(datshape.items()), "; flags:", sorted(flags.items()))
print(".ker:", sorted(kershape.items()), "; .fex:", sorted(fexshape.items()))
print("font .dat not requested by a list:", [p[len(ROOT):] for p in dat if p not in requested])
print(".ker not requested:", [p[len(ROOT):] for p in ker if p not in requested])
print(".fex not requested:", [p[len(ROOT):] for p in fex if p not in requested])
for p in fex:
    if p not in requested:
        r, v, why = fex_walk(read_all(p))
        d = read_all(p)
        print("  unrequested %s: by the parser's rules %d records, %s; first words %s" % (p[len(ROOT):], r, why, [hex(x) for x in struct.unpack_from("<6I", d, 0)]))
        # the same bytes read as 12-byte {key, index, value} triples - a reading of the data, not of any parser
        trip = [struct.unpack_from("<III", d, o) for o in range(0, len(d) - len(d) % 12, 12)]
        seq = collections.defaultdict(int); ok = len(d) % 12 == 0
        for k, i, v in trip:
            ok = ok and i == seq[k]; seq[k] += 1
        print("    as {key, index, value} triples: size %% 12 == %d, %d triples, %d keys, every key's indices run 0,1,2,...: %s" % (len(d) % 12, len(trip), len(seq), ok))
print("all .ker sizes are multiples of 12:", all(len(read_all(p)) % 12 == 0 for p in ker))
