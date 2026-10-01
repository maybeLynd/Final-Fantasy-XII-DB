"""SWE2-AUDIT-SEM UC1-SPAN checks, part 2 (own code).
X2 the widened hunt of part 1 filtered: an RVA-valued cell that lies inside a DIR64-relocated qword is a pointer half
   (the producer's rule) and is dropped; every remaining hit is printed with its VA, alignment, whether it is itself
   relocated, and the 32 bytes around it.
S2 where SEAD 007EE7C0's one rva32-bytes occurrence and libvpx's four va64 occurrences sit, and the control-map
   layout around them (01CDB290..01CDB3C0 as qwords)."""
import struct, os, collections
import img

raw = img.raw
# DIR64 reloc set
relo = set()
dd = img.opt_dd(5) if hasattr(img, "opt_dd") else None
rs = [s for s in img.secs if s[0].startswith(".reloc")][0]
blob = raw[rs[3]:rs[3] + rs[4]]
o = 0
while o + 8 <= len(blob):
    page, size = struct.unpack_from("<II", blob, o)
    if size < 8:
        break
    for k in range(8, size, 2):
        e = struct.unpack_from("<H", blob, o + k)[0]
        if e >> 12 == 10:
            relo.add(img.BASE + page + (e & 0xFFF))
    o += size
print("DIR64 relocated cells:", len(relo))

def va_of(fileoff):
    for name, rva, vsz, rptr, rsz in img.secs:
        if rptr <= fileoff < rptr + rsz:
            return img.BASE + rva + (fileoff - rptr), name
    return None, None

import csv
HERE = os.path.dirname(os.path.abspath(__file__))
TSV = next(p for p in (os.path.join(HERE, "..", "ec7-uc1-span-rows-0929", "uc1-span-tests.tsv"),
                       os.path.join(HERE, "..", "..", "..", "..", "FFXII TZA", "_index", "candidates",
                                    "ec7-uc1-span-rows-0929", "uc1-span-tests.tsv")) if os.path.exists(p))
rows = list(csv.DictReader(open(TSV, encoding="utf-8"), delimiter="\t"))
targets = {int(r["body"], 16) for r in rows if r["family"] == "PPFX" and r["refs"] == "0"}
kept = []
for name, rva, vsz, rptr, rsz in img.secs:
    if name in (".text", ".pdata", ".reloc"):
        continue
    b = raw[rptr:rptr + rsz]
    for i in range(len(b) - 8):
        va = img.BASE + rva + i
        q = struct.unpack_from("<Q", b, i)[0]
        d = struct.unpack_from("<I", b, i)[0] + img.BASE
        for kind, val in (("va64", q), ("rva32", d)):
            if val in targets:
                inside_rel = any((va - k) in relo for k in range(0, 8)) and kind == "rva32"
                if inside_rel:
                    continue
                kept.append((val, kind, va, va % 8, va in relo, b[max(0, i - 8):i + 16].hex()))
print("X2 hits left after dropping pointer halves:", len(kept))
for t, kind, va, al, isrel, ctx in kept:
    print("   body %08X  %s cell %08X (mod 8 = %d, relocated=%s)  bytes %s" % (t, kind, va, al, isrel, ctx))

print("S2:")
for t, lab in ((0x007EE7C0, "SEAD"), (0x0016EE40, "vpx"), (0x0016EE80, "vpx"), (0x0016EFF0, "vpx"), (0x0016F030, "vpx")):
    for pat, kind in ((struct.pack("<Q", t), "va64"), (struct.pack("<I", t - img.BASE), "rva32")):
        i = raw.find(pat)
        while i != -1:
            va, sec = va_of(i)
            print("   %s %08X %s at %s %s relocated=%s" % (lab, t, kind, "%08X" % va if va else "?", sec, va in relo))
            i = raw.find(pat, i + 1)
print("   control map 01CDB290..01CDB3C0:")
for a in range(0x01CDB290, 0x01CDB3C0, 8):
    print("     %08X %016X %s" % (a, struct.unpack("<Q", img.rd(a, 8))[0], "R" if a in relo else ""))
