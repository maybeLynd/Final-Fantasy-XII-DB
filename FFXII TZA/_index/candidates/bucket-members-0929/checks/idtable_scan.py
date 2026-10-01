"""idtable_scan.py ID [ID ...] : 8-aligned {u32 id, u32 any, u64 -> printable string} records in .rdata/.data - the
shape of the menu resource tables walked by 00393460 / 003934F0 (control: 0xC1 at 00D237E0 'q_img_c')."""
import sys, struct
exec(open("peek.py").read())
ids = [int(x, 0) for x in sys.argv[1:]] + [0xC1]
fails = 0; found = {}
for (va, vs, ro, rs) in secs[1:3]:
    n = min(vs, rs)
    for p in range(0, n - 16, 8):
        a, b, ptr = struct.unpack_from("<IIQ", d, ro + p)
        if a in ids and 0x8C2000 <= ptr < 0x1DF0000:
            s = cstr(ptr)
            if s and 2 <= len(s) < 40 and all(32 <= ord(c) < 127 for c in s):
                found.setdefault(a, []).append((va + p, b, s))
for i in ids:
    print(hex(i), found.get(i, [])[:12], "count", len(found.get(i, [])))
ok = any(x[0] == 0xD237E0 for x in found.get(0xC1, []))
print("CONTROL 0xC1 @ 00D237E0:", "PASS" if ok else "FAIL"); fails += not ok
print("FAILS", fails)
