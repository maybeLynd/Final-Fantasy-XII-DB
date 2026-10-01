"""SWE2-AUDIT-SEM own EFX element-type census (GI-8 correction 1), independent of type_census.py and of its embedded
file list. Carriers scanned by byte search for the magics EFX0010 / EFX0009 / EFX0008 at ANY offset:
  every .efx, .efb, .cm and .mpk file in D:/FFXII_TZA_extract (os.walk, extension match, case-insensitive).
Each magic starts a stream; +0xC = stream size (dword); chunks {u32 len, u16 flag, u16 type} from +0x10 to the size.
A stream counts only if its chunk walk ends exactly at the size (so a false magic hit is refused). Element type = byte
+0xE of each type-0xA00 chunk. Also counts files per extension that carry at least one valid stream, and the magic
version totals. Controls: the producer's pins - 55 distinct types, 0x04 = 173 chunks, 0xA3 = 447, EFX0009 x1,
EFX0008 x7 - are compared, not assumed.
Extensions outside {.efx,.efb,.cm,.mpk} are NOT scanned here (limit): the producer's claim that only .cm/.mpk carry
embedded streams rests on its own full-extract byte search."""
import os, struct, collections, sys
ROOT = "D:/FFXII_TZA_extract"
EXTS = (".efx", ".efb", ".cm", ".mpk")
MAG = (b"EFX0010", b"EFX0009", b"EFX0008")
types = collections.Counter()
ver = collections.Counter()
carriers = collections.Counter()
streams = collections.Counter()
bad = 0
nfiles = collections.Counter()
for dp, dn, fn in os.walk(ROOT):
    for f in fn:
        ext = os.path.splitext(f)[1].lower()
        if ext not in EXTS:
            continue
        nfiles[ext] += 1
        b = open(os.path.join(dp, f), "rb").read()
        found = 0
        for m in MAG:
            p = b.find(m)
            while p >= 0:
                if p + 0x10 <= len(b):
                    size = struct.unpack_from("<I", b, p + 0xC)[0]
                    end = p + size
                    q = p + 0x10
                    ok = 16 < size <= len(b) - p
                    ts = []
                    while ok and q < end:
                        if q + 8 > end:
                            ok = False
                            break
                        ln, flag, ty = struct.unpack_from("<IHH", b, q)
                        if ln < 8 or q + ln > end:
                            ok = False
                            break
                        if ty == 0xA00 and q + 0xF <= end:
                            ts.append(b[q + 0xE])
                        q += ln
                    if ok and q == end:
                        found += 1
                        ver[m.decode()] += 1
                        streams[ext] += 1
                        types.update(ts)
                    else:
                        bad += 1
                p = b.find(m, p + 1)
        if found:
            carriers[ext] += 1
print("files scanned per extension:", dict(nfiles))
print("files carrying >=1 valid stream:", dict(carriers))
print("valid streams per carrier extension:", dict(streams))
print("magic hits refused (walk did not end at size):", bad)
print("version magics over valid streams:", dict(ver))
print("0xA00 records:", sum(types.values()), " distinct element types:", len(types))
print("types:", " ".join("%02X:%d" % (t, n) for t, n in sorted(types.items())))
chk = [("55 distinct", len(types) == 55), ("0x04 = 173", types[0x04] == 173), ("0xA3 = 447", types[0xA3] == 447),
       ("EFX0009 x1", ver["EFX0009"] == 1), ("EFX0008 x7", ver["EFX0008"] == 7),
       ("once-authored types", sorted("%02X" % t for t, n in types.items() if n == 1))]
for name, v in chk:
    print("pin", name, "->", v)
