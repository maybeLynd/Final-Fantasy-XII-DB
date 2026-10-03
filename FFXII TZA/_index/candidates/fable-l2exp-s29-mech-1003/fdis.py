"""dis.py - FABLE scratch: disassemble whole .pdata bodies, or list raw references.

  python dis.py fn VA [VA...]     whole .pdata function holding VA (chained .pdata followed by start/end)
  python dis.py refs VA [HI]      raw reference index (rawref.text_refs + data_refs)
  python dis.py at VA N           N bytes linear from VA
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rawref import Img, text_refs, data_refs, fmt_ref  # noqa: E402

img = Img.load()
cmd = sys.argv[1]
if cmd == "fn":
    for a in sys.argv[2:]:
        va = int(a, 16)
        pd = img.pdata(va)
        print("== %08X pdata %s" % (va, "%08X-%08X" % pd if pd else None))
        s, e = pd
        for ci in img.cs.disasm(img.read(s, e - s), s):
            print("%08X  %-24s %s %s" % (ci.address, ci.bytes.hex(), ci.mnemonic, ci.op_str))
elif cmd == "at":
    va = int(sys.argv[2], 16)
    n = int(sys.argv[3], 0)
    for ci in img.cs.disasm(img.read(va, n), va):
        print("%08X  %-24s %s %s" % (ci.address, ci.bytes.hex(), ci.mnemonic, ci.op_str))
elif cmd == "refs":
    lo = int(sys.argv[2], 16)
    hi = int(sys.argv[3], 16) if len(sys.argv) > 3 else lo + 1
    refs, unc = text_refs(img, lo, hi)
    for r in refs:
        print(fmt_ref(r))
    print("unconfirmed:", ["%08X" % u for u in unc])
    for d in data_refs(img, lo, hi):
        print("DATA %s %08X %s %08X" % d)

if cmd == "root":
    import struct
    po = img.off(img.base + img.exc_rva)
    ents = []
    for i in range(img.exc_size // 12):
        b, e, u = struct.unpack_from("<III", img.d, po + i * 12)
        ui = img.off(img.base + u)
        fl = img.d[ui] >> 3
        n = img.d[ui + 2]
        r = b
        if fl & 4:
            co = ui + 4 + ((n + 1) & ~1) * 2
            r = struct.unpack_from("<I", img.d, co)[0]
        ents.append((b + img.base, e + img.base, r + img.base))
    first = dict((b, r) for b, e, r in ents)
    frags = {}
    for b, e, r in ents:
        k = 0
        while r in first and first[r] != r and k < 16:
            r = first[r]; k += 1
        frags.setdefault(r, []).append((b, e))
    for a in sys.argv[2:]:
        va = int(a, 16)
        for r, parts in frags.items():
            if any(s <= va < e for s, e in parts):
                print("%08X root %08X parts %s" % (va, r, ["%08X-%08X" % p for p in sorted(parts)]))
