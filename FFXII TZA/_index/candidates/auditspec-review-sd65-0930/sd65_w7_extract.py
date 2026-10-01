"""sd65_w7_extract.py - SWE2-AUDIT-SPEC (2026-09-30): the w7 census from a second reader and a second copy of the data.
Walks the loose full-game extract D:/FFXII_TZA_extract (not the VBF the author read), counts .phyre files per top
directory, and tallies the class-record word at +0x1C (w7, the byte the loader tests at 0059AC95) over every class
record: header u32 +4 = header size, +8 = namespace size; namespace u32 +8/+0xC = type / class counts; class records
(36 bytes) start at namespace + 0x20 + 4 * types."""
import os, struct, collections
ROOT = "D:/FFXII_TZA_extract"
w7 = collections.Counter(); files = collections.Counter(); bad = 0; recs = 0
for dp, dn, fn in os.walk(ROOT):
    for f in fn:
        if not f.lower().endswith(".phyre"): continue
        top = os.path.relpath(dp, ROOT).replace("\\", "/").split("/")[0]
        files[top] += 1
        try:
            with open(os.path.join(dp, f), "rb") as h: d = h.read(0x400000)
            hsz, nssz = struct.unpack_from("<II", d, 4)
            nT, nC = struct.unpack_from("<II", d, hsz + 8)
            co = hsz + 0x20 + 4 * nT
            for c in range(nC):
                w7[struct.unpack_from("<I", d, co + 36 * c + 0x1C)[0]] += 1; recs += 1
        except Exception:
            bad += 1
print("phyre files by top directory:", dict(files), "total", sum(files.values()), "unparsed", bad)
print("class records", recs, "w7 values:", dict(sorted(w7.items())))
print("records with w7 bit 0 set:", sum(n for v, n in w7.items() if v & 1))
