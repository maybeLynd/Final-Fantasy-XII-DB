"""arm0_census.py - count @FMW entries by format arm (u32 +0x34) over every .cm/.ca under D:/FFXII_TZA_extract (FABLE re-run of a subagent census, 2026-09-29). Prints the file count, arms by extension, then each arm-0 entry (path, entry offset, length)."""
import os, struct, collections, sys
root = r"D:\FFXII_TZA_extract"
arms = collections.Counter(); hits = []
nfiles = 0
for dp, dn, fn in os.walk(root):
    for f in fn:
        if not f.lower().endswith((".cm", ".ca")): continue
        p = os.path.join(dp, f)
        d = open(p, "rb").read()
        if len(d) < 0x40: continue
        nfiles += 1
        try:
            var, clen, cnt = struct.unpack_from("<III", d, 4)
            base = 0x40 if var == 1 else 0x30
            if cnt > 100000: continue
            for i in range(cnt):
                o = base + struct.unpack_from("<I", d, base + i*4)[0]
                if o + 0x44 > len(d): continue
                if d[o:o+4] == b"@FMW":
                    arm = struct.unpack_from("<I", d, o+0x34)[0]
                    arms[(f[-3:], arm)] += 1
                    if arm == 0:
                        hits.append((p, o, struct.unpack_from("<I", d, o+8)[0]))
        except struct.error:
            pass
print(nfiles, dict(arms))
for h in hits: print(h[0], hex(h[1]), hex(h[2]))
